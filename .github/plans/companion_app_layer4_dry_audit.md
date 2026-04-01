# Layer 4 — DRY Audit

**Project:** companion_app
**Input:** Layer 3 Blueprints (26 blueprints across 5 phases, ~4680 lines)
**Date:** 2026-03-31
**Methodology:** Single-pass consolidation analysis per CCE heuristics

---

## Audit Summary

| ID | Category | Action | Targets | Impact |
|---|---|---|---|---|
| C1 | Extract helper | **EXTRACT** `requireGm()` | 5 form actions (BP 3.2, 4.2b, 4.3b, 4.3e×2) | ~35 lines saved |
| C2 | Simplify loads | **SIMPLIFY** GM check in load functions | 2 load fns (BP 4.3b, 4.3e) | ~16 lines saved, 2 DB queries eliminated |
| C3 | Bug fix | **FIX** missing `await` on `getDb()` | ~6 call sites (Phase 4) | Runtime error prevention |
| C4 | Consistency | **FIX** Svelte 4 → Svelte 5 runes | 2 files (BP 3.5, 3.6) | Convention alignment |
| C5 | Extract utility | **OPTIONAL** `processFormFields()` | 2 form actions (4.3b, 4.3e) | ~7 lines saved |
| C6 | Skip | **SKIP** UNIQUE constraint handling | 2 sites | Below threshold (identical 4-line try/catch) |
| C7 | Skip | **SKIP** Catalog slug validation guard | ~8 sites | Below threshold (2-line guard) |

**Net reduction:** ~58 lines removed, ~22 lines added (helper + utility) = **~36 net lines saved**
**Bug fixes:** 2 categories (C3, C4) — both must be applied regardless of DRY preference

---

## C1: Extract `requireGm()` Helper — **EXTRACT**

### Problem

Five form actions across three blueprints repeat an identical 8-line GM re-validation pattern:

```typescript
const session = await locals.auth();
if (!session?.user?.id) throw error(401, 'Unauthorized');
const db = await getDb(platform!.env);
const playerRow = await db.execute({
  sql: 'SELECT is_gm FROM players WHERE id = ?',
  args: [session.user.id],
});
if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
  throw error(403, 'Forbidden');
}
```

**Occurrences (5 form actions):**

| Blueprint | File | Action |
|---|---|---|
| 3.2 | `admin/assign/+page.server.ts` | `actions.assign` |
| 4.2b | `library/[catalog]/+page.server.ts` | `actions.delete` |
| 4.3b | `library/[catalog]/new/+page.server.ts` | `actions.create` |
| 4.3e | `library/[catalog]/[id]/edit/+page.server.ts` | `actions.update` |
| 4.3e | `library/[catalog]/[id]/edit/+page.server.ts` | `actions.delete` |

### Proposed Extraction

**New file:** `companion/src/lib/server/auth.ts`

```typescript
import { error } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import type { Client } from '@libsql/client';

/**
 * Validates the current session belongs to a GM player.
 * Returns the DB client for downstream reuse.
 *
 * Use in form actions where parent() layout data is unavailable.
 */
export async function requireGm(
  locals: App.Locals,
  platform: App.Platform | undefined
): Promise<{ db: Client; userId: string }> {
  const session = await locals.auth();
  if (!session?.user?.id) throw error(401, 'Unauthorized');

  const db = await getDb(platform!.env);
  const result = await db.execute({
    sql: 'SELECT is_gm FROM players WHERE id = ?',
    args: [session.user.id],
  });
  if ((result.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  return { db, userId: session.user.id };
}
```

### Call-site transformation

Before (8 lines per site):
```typescript
const session = await locals.auth();
if (!session?.user?.id) throw error(401, 'Unauthorized');
const db = await getDb(platform!.env);
const playerRow = await db.execute({ sql: 'SELECT is_gm FROM players WHERE id = ?', args: [session.user.id] });
if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) throw error(403, 'Forbidden');
```

After (1 line per site):
```typescript
const { db } = await requireGm(locals, platform);
```

### Quantified gain

- 5 sites × 8 lines = 40 lines removed
- 15-line helper added
- **Net: ~25 lines saved, 1 reusable auth primitive**
- Bonus: each call site also gets `db` — no separate `getDb()` call needed

### Design rationale

Form actions cannot access `parent()` layout data (confirmed in BP 3.2 DEV DECISION). The DB re-query is **required** for security. But the boilerplate is identical — extraction is safe. The helper throws SvelteKit `error()` on failure, which SvelteKit catches and converts to the proper HTTP response — no special error handling needed at call sites.

---

## C2: Simplify GM Check in Load Functions — **SIMPLIFY**

### Problem

Two Phase 4 load functions (BP 4.3b, 4.3e) perform a **redundant** DB query to check GM status, despite having access to `parent()` which already provides `player.is_gm` from the root layout (BP 3.3).

**BP 4.3b load (`new/+page.server.ts`):**
```typescript
const { player } = await parent();
const db = getDb(platform!.env);   // ← also missing await (C3)
const playerRow = await db.execute({
  sql: 'SELECT is_gm FROM players WHERE id = ?',
  args: [player.id],
});
if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
  throw error(403, 'Forbidden');
}
```

**BP 4.3e load (`[id]/edit/+page.server.ts`):** Same pattern.

### Why these are redundant

- Load functions DO run layout load functions — `parent()` returns fresh data from the root layout's DB query *within the same request*
- The root layout (BP 3.3) already queries `SELECT id, is_gm FROM players WHERE id = ?`
- `player.is_gm` is trustworthy — it came from the DB moments earlier in the same request chain
- The admin layout (BP 3.3) uses exactly this pattern: `const { player } = await parent(); if (player.is_gm !== 1) throw error(403, 'Forbidden');`

### Proposed simplification

Replace the 8-line DB re-query with the 2-line parent check (matching the admin layout pattern):

```typescript
const { player } = await parent();
if (player.is_gm !== 1) throw error(403, 'Forbidden');
```

### Quantified gain

- 2 sites × 8 lines → 2 sites × 2 lines = **12 lines saved, 2 unnecessary DB queries eliminated per request**

### Clarification

This applies ONLY to load functions. Form actions still need `requireGm()` (C1) because they cannot access `parent()`.

---

## C3: Fix Missing `await` on `getDb()` — **BUG FIX**

### Problem

`getDb()` is declared `async` in BP 1.4:
```typescript
export async function getDb(env: App.Platform['env']): Promise<Client> {
  const client = createClient({ url: env.TURSO_DATABASE_URL, authToken: env.TURSO_AUTH_TOKEN });
  await client.execute('PRAGMA foreign_keys = ON');
  return client;
}
```

Phase 3 blueprints correctly use `await`:
```typescript
const db = await getDb(platform!.env);  // ✓ BP 3.2, 3.3, 3.5, 3.6
```

Phase 4 blueprints **drop** `await`:
```typescript
const db = getDb(platform!.env);  // ✗ BP 4.1, 4.2b, 4.3b, 4.3e
```

Without `await`, `db` is a `Promise<Client>`, not a `Client`. Any subsequent `db.execute()` call would fail at runtime with `TypeError: db.execute is not a function`.

### Affected sites

| Blueprint | File | Context |
|---|---|---|
| 4.1 | `library/+page.server.ts` | load function |
| 4.2b | `library/[catalog]/+page.server.ts` | load function + delete action |
| 4.3b | `library/[catalog]/new/+page.server.ts` | load function + create action |
| 4.3e | `library/[catalog]/[id]/edit/+page.server.ts` | load function + update action + delete action |

### Resolution

- Sites covered by C1 (`requireGm` extraction): the helper handles `await getDb()` internally — no manual fix needed
- Sites covered by C2 (load simplification): the redundant `getDb` call is removed entirely — no fix needed
- Remaining sites (BP 4.1 load, BP 4.2b load): add `await`

**Residual fixes after C1 + C2:**

| Blueprint | Fix |
|---|---|
| 4.1 load | `const db = getDb(...)` → `const db = await getDb(...)` |
| 4.2b load | `const db = getDb(...)` → `const db = await getDb(...)` |
| 4.3b load | Removed by C2 (no standalone getDb call) |
| 4.3b create action | Covered by C1 (requireGm handles getDb) |
| 4.3e load | Needs `await` for the entry fetch: `const db = await getDb(...)` |
| 4.3e update action | Covered by C1 |
| 4.3e delete action | Covered by C1 |

---

## C4: Standardize Svelte 5 Runes — **CONSISTENCY FIX**

### Problem

The project specification mandates Svelte 5 runes (`$state`, `$derived`, `$props`, `{@render children()}`, `onclick`). Phase 4 blueprints follow this correctly. However, two Phase 3 blueprints use Svelte 4 syntax:

**BP 3.5 — `characters/+page.svelte`:**
```svelte
export let data: PageData;                     // ← Svelte 4 (should be $props())
```

**BP 3.6 — `characters/[id]/+page.svelte`:**
```svelte
export let data: PageData;                     // ← Svelte 4
let activeTab: TabId = 'overview';             // ← Svelte 4 (should be $state)
on:click={() => (activeTab = tab)}             // ← Svelte 4 (should be onclick)
```

### Resolution

Update both files to Svelte 5 runes:

**BP 3.5:**
```svelte
let { data }: { data: PageData } = $props();
```

**BP 3.6:**
```svelte
let { data }: { data: PageData } = $props();
let activeTab: TabId = $state('overview');
// on:click → onclick
```

### Impact

Zero lines saved — this is a correctness/convention fix. Both files compile under Svelte 5's compatibility mode, but the runes API is the project standard.

---

## C5: Extract `processFormFields()` Utility — **OPTIONAL**

### Problem

The create action (BP 4.3b) and update action (BP 4.3e) share identical form field processing logic:

```typescript
for (const field of config.formFields) {
  const raw = formData.get(field.key);
  let value: unknown;
  if (field.type === 'number') {
    const parsed = parseFloat(String(raw ?? ''));
    value = Number.isFinite(parsed) ? parsed : null;
  } else {
    value = raw ? String(raw).trim() || null : null;
  }
  if (field.key === 'name' && !value) errors.name = 'Name is required';
  // ... push to columns/values (create) or setClauses/values (edit)
}
```

### Proposed extraction

**Add to:** `companion/src/lib/server/catalog-utils.ts`

```typescript
import type { CatalogEntry } from '$lib/catalog-config';

interface ProcessedFields {
  values: Record<string, unknown>;
  errors: Record<string, string>;
}

export function processFormFields(
  config: CatalogEntry,
  formData: FormData
): ProcessedFields {
  const values: Record<string, unknown> = {};
  const errors: Record<string, string> = {};

  for (const field of config.formFields) {
    const raw = formData.get(field.key);
    if (field.type === 'number') {
      const parsed = parseFloat(String(raw ?? ''));
      values[field.key] = Number.isFinite(parsed) ? parsed : null;
    } else {
      values[field.key] = raw ? String(raw).trim() || null : null;
    }
    if (field.key === 'name' && !values[field.key]) {
      errors.name = 'Name is required';
    }
  }

  return { values, errors };
}
```

Call sites build SQL from `values` keys:
```typescript
const { values, errors } = processFormFields(config, formData);
if (Object.keys(errors).length > 0) return { errors };
// Create: INSERT INTO ... (keys) VALUES (placeholders)
// Update: SET key = ?, key = ? ... WHERE id = ?
```

### Quantified gain

- 2 sites × ~12 lines → 2 sites × ~3 lines + ~18 line utility = **~6 lines saved**
- Marginal line reduction, but **eliminates risk of the two field-processing loops diverging**

### Recommendation

**Optional.** The gain is below the 30% DRY threshold for proactive extraction. However, it does provide correctness insurance — if a field processing rule changes (e.g., adding `maxLength` validation), it only needs to change in one place. Developer's call at implementation time.

---

## C6: UNIQUE Constraint Handling — **SKIP**

Two identical 4-line try/catch blocks (create action, update action). Below extraction threshold — the SQL operations inside the try block are different (INSERT vs UPDATE), so extraction would require parameterizing the entire SQL execution, not just the error handler. The error text match (`'UNIQUE constraint failed'`) is a Turso/SQLite-specific string — if it ever changes, a grep finds both sites instantly.

## C7: Catalog Slug Validation — **SKIP**

Eight instances of `const config = CATALOG_CONFIG[params.catalog]; if (!config) throw error(404, ...)`. This is a 2-line guard that reads clearly inline. Extracting it into `getCatalogConfig(slug)` would save zero lines (still need the variable assignment + the null check) and add indirection.

---

## Implementation Plan

Apply in this order during Phase-by-phase implementation:

| Order | ID | When to apply | Blueprint amendment |
|---|---|---|---|
| 1 | C3 | During Phase 4 implementation | Fix `await` in BP 4.1, 4.2b, 4.3e load |
| 2 | C4 | During Phase 3 implementation | Update BP 3.5 + 3.6 to Svelte 5 runes |
| 3 | C1 | Create `$lib/server/auth.ts` (Phase 3 step 1), then use in BP 3.2 + all Phase 4 form actions | New file; amend BP 3.2, 4.2b, 4.3b, 4.3e |
| 4 | C2 | During Phase 4 implementation | Simplify BP 4.3b + 4.3e load functions |
| 5 | C5 | Developer discretion at Phase 4 | Optional; create `$lib/server/catalog-utils.ts` if desired |

---

## Files Added by This Audit

| File | Purpose |
|---|---|
| `companion/src/lib/server/auth.ts` | `requireGm()` helper (C1) |
| `companion/src/lib/server/catalog-utils.ts` | `processFormFields()` utility (C5, optional) |

---

*Layer 4 DRY Audit complete. Ready for user review.*