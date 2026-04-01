# companion_app — Layer 5: Pure Signal Brief

> **Stack:** SvelteKit (Svelte 5 runes) on Cloudflare Pages, Turso (libSQL) database, Discord OAuth via `@auth/sveltekit`. Single deployment, edge runtime. Companion web app for a medieval Shadowrun 3e TTRPG campaign (6 players, ~18 characters). Two core features: **Game Library** (11 `ref_*` catalog tables from GM Excel workbooks, GM CRUD + player browse) and **Character Viewer** (read-only view of Roll20-synced characters — 1 `characters` table with 129 scalar cols + 10 `rep_*` tables). Sync model: full-snapshot push from Roll20 → `POST /api/sync` with timing-safe SHA-256 campaign secret auth. All code lives in `companion/` subdirectory within the existing `sheet` repo.

**Svelte version constraint:** Svelte 5 runes ONLY — `$state`, `$derived`, `$props`, `{@render children()}`, `onclick`. NO `export let`, `<slot />`, `on:click`, or Svelte 4 patterns.

**Database access constraint:** `getDb()` is async. Every call site MUST use `await getDb(platform!.env)`.

---

## Phase 0 — Roll20 Sheet Updates

**Goal:** Add missing fields, remove 20 Questions, complete sync handler to collect all 10 repeating sections.

**Files modified:** `sheet.html` (HTML + CSS + Sheet Worker), `sheet.css`

### Implementation Order

| Step | What | Blueprint | File Region |
|------|------|-----------|-------------|
| 1 | Money fields: Gear tab HTML + CSS | BP 0.1 | HTML: after `sheet-tab-panel-gear` open, before Armor. CSS: Section 13b |
| 2 | Remove 20 Questions: Bio tab HTML + scalarFields | BP 0.2 | HTML: delete lines 1214–1254 (20 Q&A pairs). Worker: delete `bio_q01`–`bio_q20` from scalarFields (subsumed by step 5) |
| 3 | Karma Ledger: Bio tab HTML + CSS | BP 0.3 | HTML: after Notes textarea, before closing `</div>`. CSS: end of Section 14 |
| 4 | Milestones: Bio tab HTML + CSS | BP 0.4 | HTML: after `</fieldset>` of `repeating_karma`. CSS: after karma block |
| 5 | Sync handler: wholesale replacement (lines 423–507) | BP 0.5 | Worker `<script type="text/worker">` block — complete rewrite |

### Key Patterns

**HTML fields (BP 0.1):**
- 3 number inputs: `attr_money_gold`, `attr_money_silver`, `attr_money_copper`
- Container: `.sheet-money-row` (flex, gap 8px, 70px inputs) — same pattern as `.sheet-karma-row`

**HTML fields (BP 0.3):**
- `<fieldset class="repeating_karma">` with `attr_karma_event` (text) + `attr_karma_amount` (number)
- Header: `.sheet-karma-log-header` (flex, event grows, amount 70px fixed)
- Shared rule: `.sheet-tab-panel-bio .repitem` (flex row for bio repeating sections)

**HTML fields (BP 0.4):**
- `<fieldset class="repeating_milestones">` with `attr_milestone_trial` (text), `attr_milestone_tier1`–`tier3` (text), `attr_milestone_current` (number, min=0 max=3)
- 5-column grid: trial grows, tiers 160px each, current 50px

**Sync handler (BP 0.5) — counter/latch rewrite:**
- `var remaining = 11` (10 sections + 1 scalar `getAttrs`)
- `proceed()` decrements; fires `fetch()` when `remaining === 0`
- `SECTIONS` lookup table maps section keys → field arrays (10 entries)
- `scalarFields`: remove `bio_q01`–`bio_q20`, add `money_gold/silver/copper`
- Each repeating row includes `roll20_row_id` (from `getSectionIDs` hash)
- `Object.keys(SECTIONS).forEach(function(key) { ... })` — Roll20 has no `for...of`
- Default `|| ''` for all row field values (consistent strings)

### 10 Repeating Sections — Field Reference

| Section key | Roll20 fieldset | Fields |
|---|---|---|
| `skills` | `repeating_skills` | `skill_name`, `skill_linked_attr`, `skill_general`, `skill_spec`, `skill_base`, `skill_foci`, `skill_misc`, `skill_total` |
| `mutations` | `repeating_mutations` | `mutation_name`, `mutation_level`, `mutation_essence`, `mutation_bp_cost`, `mutation_effect` |
| `adept_powers` | `repeating_adept_powers` | `power_name`, `power_level`, `power_pp_cost`, `power_pp_cost_value`, `power_effect` |
| `spells` | `repeating_spells` | `spell_name`, `spell_force`, `spell_drain` |
| `foci` | `repeating_foci` | `focus_name`, `focus_type`, `focus_force`, `focus_bonded`, `focus_notes` |
| `weapons` | `repeating_weapons` | `weapon_name`, `weapon_type`, `weapon_modifiers`, `weapon_power`, `weapon_damage`, `weapon_conceal`, `weapon_reach`, `weapon_ep`, `weapon_range_short`, `weapon_range_medium`, `weapon_range_long`, `weapon_range_extreme` |
| `equipment` | `repeating_equipment` | `equip_name`, `equip_description`, `equip_ep` |
| `contacts` | `repeating_contacts` | `contact_name`, `contact_info`, `contact_level` |
| `karma` | `repeating_karma` | `karma_event`, `karma_amount` |
| `milestones` | `repeating_milestones` | `milestone_trial`, `milestone_tier1`, `milestone_tier2`, `milestone_tier3`, `milestone_current` |

### Bio Tab Final Structure (post-changes)

```
Bio Tab
├── Description (textarea — existing)
├── Notes (textarea — existing)
├── Karma Ledger (NEW — repeating_karma)
└── Milestones (NEW — repeating_milestones)
```

20 Questions: removed from UI, removed from sync, data preserved in Roll20 attribute store.

### Acceptance Criteria

- [ ] 3 money inputs visible at top of Gear tab; values persist
- [ ] 20 Questions removed from Bio tab; Description/Notes remain
- [ ] Karma Ledger section on Bio tab: add/delete works, headers align
- [ ] Milestones section on Bio tab: 5-column layout, `milestone_current` accepts 0–3 only
- [ ] `payload.scalars` includes `money_gold/silver/copper`, excludes `bio_q01`–`bio_q20`
- [ ] `payload.repeating` has exactly 10 keys; empty sections produce `[]`
- [ ] Every repeating row object includes `roll20_row_id`
- [ ] Sync button shows "Syncing…" immediately, updates on completion

---

## Phase 1 — Project Scaffold + Database Schema + Seed Utility

**Goal:** Standing SvelteKit project with Turso connected, all 24 tables created, reference data seeded.

### Files to Create

| File | Blueprint | Purpose |
|------|-----------|---------|
| `companion/package.json` | BP 1.1 | SvelteKit project; scripts: `dev`, `build`, `migrate`, `seed` |
| `companion/svelte.config.js` | BP 1.1 | `adapter-cloudflare`, `vitePreprocess()` |
| `companion/wrangler.toml` | BP 1.1 | `nodejs_compat` flag, `pages_build_output_dir: ".svelte-kit/cloudflare"` |
| `companion/.dev.vars` | BP 1.1 | Local secrets (GITIGNORED): `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`, `CAMPAIGN_SECRET`, `AUTH_SECRET`, `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET` |
| `companion/.gitignore` | BP 1.1 | `.dev.vars` |
| `companion/db/schema.sql` | BP 1.3 | Authoritative DDL — 24 tables + 17 indices |
| `companion/src/app.d.ts` | BP 1.4 | `App.Platform['env']` typing (6 env vars) |
| `companion/src/lib/db.ts` | BP 1.4 | `getDb(env)` — async, `@libsql/client/web`, `PRAGMA foreign_keys = ON` |
| `companion/scripts/migrate.ts` | BP 1.4 | Execute `schema.sql` via `@libsql/client/node`; requires `--force` flag |
| `companion/scripts/seed.ts` | BP 1.5 | Parse 5 Excel workbooks → upsert 11 `ref_*` tables |

### Implementation Order

| Step | Blueprint | Action |
|------|-----------|--------|
| 1 | BP 1.1 | `npm create svelte@latest companion` (skeleton, TS, ESLint, Prettier) |
| 2 | BP 1.1 | Install deps: `@sveltejs/adapter-cloudflare`, `@libsql/client`, `tsx` (dev), `xlsx` (dev) |
| 3 | BP 1.1 | Create `wrangler.toml`, `.dev.vars`, `.gitignore`, `svelte.config.js` |
| 4 | BP 1.2 | Turso CLI: `turso db create companion-app`, generate token, populate `.dev.vars` |
| 5 | BP 1.3 | Write `db/schema.sql` (full DDL below) |
| 6 | BP 1.4 | Create `src/app.d.ts`, `src/lib/db.ts`, `scripts/migrate.ts` |
| 7 | Execute | `npm run migrate -- --force` → 24 tables live |
| 8 | BP 1.5 | Create `scripts/seed.ts` |
| 9 | Execute | `npm run seed` → 11 ref tables populated |
| 10 | BP 1.6 | Verify: `npm run dev` starts, Turso shell `.tables` shows 24, spot-check rows |

### Database Schema — 24 Tables

**Table creation order** (FK dependency-safe):

1. `campaigns` — no FK
2. `players` — no FK
3. `characters` — FK → `players(id)`, `campaigns(id)`. Backbone: `id` TEXT PK, `player_id` TEXT (nullable — backfilled in Phase 3), `campaign_id` TEXT NOT NULL, `roll20_character_id` TEXT UNIQUE (nullable), `sync_version` INTEGER DEFAULT 0, `synced_at`, `created_at`, `updated_at` + **129 scalar game-data columns** (mapped 1:1 from Roll20 `scalarFields` array; see BP 1.3 for complete column list)
4–13. `rep_skills`, `rep_mutations`, `rep_adept_powers`, `rep_spells`, `rep_foci`, `rep_weapons`, `rep_equipment`, `rep_contacts`, `rep_karma`, `rep_milestones` — all FK → `characters(id) ON DELETE CASCADE`, backbone: `id` TEXT PK, `character_id` TEXT NOT NULL, `roll20_row_id` TEXT NOT NULL, UNIQUE(`character_id`, `roll20_row_id`)
14–24. `ref_spells`, `ref_weapons`, `ref_armor`, `ref_equipment`, `ref_skills`, `ref_adept_powers`, `ref_mutations`, `ref_totems`, `ref_spirits`, `ref_spirit_powers`, `ref_elemental_services` — all: `id` INTEGER PK AUTOINCREMENT, `name` TEXT UNIQUE NOT NULL, `created_at`/`updated_at` TEXT defaults

**Key column design decisions:**
- `characters.player_id` nullable: sync payload has no Discord context; backfilled via GM assignment (Phase 3)
- `characters.roll20_character_id` nullable: Roll20 Sheet Workers cannot access platform character ID
- `essence_total` and `mutation_essence` use REAL; all other numerics use INTEGER
- All ref tables use `UNIQUE(name)` as the conflict target for idempotent seed upserts

**Indices (17 total):** `idx_characters_player`, `idx_characters_campaign`, `idx_rep_{section}_char` × 10, `idx_ref_spells_category`, `idx_ref_spells_type`, `idx_ref_weapons_type`, `idx_ref_totems_type`, `idx_ref_spirits_category`

### `getDb()` Pattern (BP 1.4)

```typescript
// companion/src/lib/db.ts
import { createClient } from '@libsql/client/web';  // Fetch API — CF Workers compatible
import type { Client } from '@libsql/client';

export async function getDb(env: App.Platform['env']): Promise<Client> {
  const client = createClient({ url: env.TURSO_DATABASE_URL, authToken: env.TURSO_AUTH_TOKEN });
  await client.execute('PRAGMA foreign_keys = ON');
  return client;
}
```

**CRITICAL:** This function is `async`. Every call site MUST `await` it. Phase 4 blueprints originally omitted `await` — this was caught in L4 audit (C3).

### Seed Utility Pattern (BP 1.5)

- Uses `@libsql/client/node` (NOT `/web` — seed runs in Node.js)
- 5 workbook files in `elements/` directory at repo root
- 11 parser functions (one per source sheet → row interface)
- 11 seeder functions using `INSERT INTO ... ON CONFLICT(name) DO UPDATE SET ...`
- Batch size: 50 rows per `db.batch()` call
- Reports: `upserted=N  errors=0` per table
- Idempotent: second run produces same counts, no duplicates
- Script: `"seed": "tsx --env-file=.dev.vars scripts/seed.ts"`

**Expected row counts:**

| Table | Expected |
|---|---|
| `ref_spells` | 60–80 |
| `ref_weapons` | ~20 |
| `ref_armor` | ~15 |
| `ref_equipment` | ~100 |
| `ref_skills` | ~40 |
| `ref_adept_powers` | ~20 |
| `ref_mutations` | ~20 |
| `ref_totems` | 43 |
| `ref_spirits` | 19 |
| `ref_spirit_powers` | 18 |
| `ref_elemental_services` | 4 |

### Acceptance Criteria

- [ ] `companion/` contains valid SvelteKit + TypeScript project
- [ ] `npm run dev` starts without errors
- [ ] `wrangler.toml`: `nodejs_compat` flag, correct `pages_build_output_dir`
- [ ] `svelte.config.js` uses `adapter-cloudflare`
- [ ] `.dev.vars` exists and is gitignored
- [ ] Turso DB reachable; `turso db shell` connects
- [ ] `npm run migrate -- --force` creates all 24 tables
- [ ] `npm run seed` populates 11 ref tables with expected row counts
- [ ] Second `npm run seed` run: no row count increase (idempotency)

---

## Phase 2 — Sync Endpoint + Roll20 Wiring

**Goal:** Click "Sync to DB" in Roll20 and data lands in Turso.

### Files to Create

| File | Blueprint | Purpose |
|------|-----------|---------|
| `companion/src/routes/api/sync/+server.ts` | BP 2.1 | POST validation pipeline + timing-safe secret verify |
| `companion/src/lib/sync-write.ts` | BP 2.2 | Atomic Turso batch: upsert character + delete/reinsert repeating |
| `companion/scripts/seed-campaign.ts` | BP 2.4 | Seed `campaigns` row with SHA-256 hashed secret |

### Files to Modify

| File | Blueprint | Changes |
|------|-----------|---------|
| `sheet.html` (worker block) | BP 2.3 | Add `CAMPAIGN_SECRET` constant + `X-Campaign-Secret` header to fetch |
| `companion/package.json` | BP 2.4 | Add `"seed-campaign"` script |

### Implementation Order

| Step | Blueprint | Action |
|------|-----------|--------|
| 1 | BP 2.2 | Create `src/lib/sync-write.ts` — types, allowlists, `syncWrite()` |
| 2 | BP 2.1 | Create `src/routes/api/sync/+server.ts` — validation + secret verify |
| 3 | BP 2.3 | Add `CAMPAIGN_SECRET` + `X-Campaign-Secret` header to sheet worker |
| 4 | BP 2.4 | Create `scripts/seed-campaign.ts` + add script to package.json |
| 5 | Execute | `npm run seed-campaign -- --name "Campaign" --secret "mysecret"` |
| 6 | Execute | `npm run build` — verify zero errors |
| 7 | Test | 9 cURL test cases (see test matrix below) |
| 8 | Deploy | `wrangler pages deploy` + set CF Pages env vars |
| 9 | BP 2.3 | Fill `SYNC_PROXY_URL` with CF Pages URL, upload sheet to Roll20 |
| 10 | Test | Live Roll20 E2E: first sync → verify row → second sync → version increments |

### `/api/sync` Validation Pipeline (BP 2.1)

Order of checks (first failure wins):
1. Body size > 1MB → 413
2. Content-Type not `application/json` → 415
3. JSON parse failure → 400
4. Missing/invalid fields (campaign_db_id, char_db_id, sync_version_from, scalars, repeating, 10 repeating keys) → 400
5. Missing `X-Campaign-Secret` header → 401
6. Campaign lookup fails (no row) → 401 (NOT 404 — prevents enumeration)
7. Timing-safe SHA-256 comparison fails → 401
8. All pass → call `syncWrite(db, body, campaignId)`

**Timing-safe comparison:** Hash incoming plaintext with `crypto.subtle.digest('SHA-256', ...)`, hex-encode, XOR every byte of both 64-char hex strings. Loop always runs to completion.

**Response contract:** `{ ok: true, char_db_id: string, sync_version: number }` on 200. Keys `char_db_id` and `sync_version` are binding — Roll20 handler reads these exact names.

### `syncWrite()` Logic (BP 2.2)

**Security boundary:** `ALLOWED_SCALAR_COLUMNS` (129 entries) and `ALLOWED_{SECTION}_COLUMNS` (10 section-specific arrays). Column names come ONLY from these allowlists — payload keys are never used as SQL identifiers. Unrecognized keys are silently ignored.

**First sync** (`char_db_id === null`):
- Generate `charId = crypto.randomUUID()`
- `INSERT INTO characters (id, campaign_id, player_id=NULL, ..., 129 scalar cols)`
- `sync_version = 1`

**Subsequent sync** (`char_db_id !== null`):
- `SELECT id, sync_version FROM characters WHERE id = ? AND campaign_id = ?`
- Not found → `SyncError(404)`
- Version mismatch (`sync_version !== body.sync_version_from`) → `SyncError(409)`
- `UPDATE characters SET sync_version = ?, ..., 129 scalar cols WHERE id = ? AND campaign_id = ?`

**Batch structure** (atomic via `db.batch(statements, 'write')`):

| Index | Statement |
|---|---|
| 0 | `PRAGMA foreign_keys = ON` |
| 1 | Characters INSERT or UPDATE |
| 2–11 | `DELETE FROM rep_{section} WHERE character_id = ?` × 10 |
| 12+ | `INSERT INTO rep_{section} (id, character_id, roll20_row_id, ...) VALUES (...)` per payload row |

Explicit DELETEs required because we UPDATE (not replace) the parent row, so `ON DELETE CASCADE` doesn't fire.

### Roll20 Wiring (BP 2.3)

Two additions to the worker block produced by BP 0.5:
1. `var CAMPAIGN_SECRET = '';` — after `SYNC_PROXY_URL`
2. `'X-Campaign-Secret': CAMPAIGN_SECRET` in fetch headers

`SYNC_PROXY_URL` stays empty until CF Pages URL is known (step 9).

### `seed-campaign.ts` (BP 2.4)

- Args: `--name "Campaign Name" --secret "plaintext_secret"`
- Computes `crypto.createHash('sha256').update(secret).digest('hex')`
- Generates UUID v4 for campaign ID
- Inserts into `campaigns` table
- Prints campaign ID (set as `attr_campaign_db_id` in Roll20)

### Test Matrix

| # | Test | Expected |
|---|---|---|
| 1 | First sync, valid | 200, `char_db_id` = new UUID, `sync_version` = 1 |
| 2 | Second sync, valid | 200, same UUID, `sync_version` = 2 |
| 3 | Stale version | 409 |
| 4 | Wrong secret | 401 |
| 5 | Missing header | 401 |
| 6 | Unknown campaign | 401 (not 404) |
| 7 | Missing `char_db_id` key | 400 |
| 8 | Missing repeating key | 400 |
| 9 | Oversized payload | 413 |

### Acceptance Criteria

- [ ] All 9 cURL test cases pass with correct status codes
- [ ] First sync creates `characters` row with `sync_version = 1`
- [ ] Second sync updates to `sync_version = 2`
- [ ] Rep tables match payload arrays exactly (not additive)
- [ ] Payload keys not in allowlists do not appear in SQL
- [ ] DB batch failure rolls back all statements
- [ ] Live Roll20 sync: status shows "Synced ✓", `char_db_id` populated, version increments

---

## Phase 3 — Auth + Character Viewer

**Goal:** Log in with Discord, see your characters, view full read-only sheet.

### Files to Create

| File | Blueprint | Purpose |
|------|-----------|---------|
| `companion/src/auth.ts` | BP 3.1 | `SvelteKitAuth` + Discord provider + player upsert in `jwt` callback |
| `companion/src/hooks.server.ts` | BP 3.1 | `sequence(authHandle, appHandle)` |
| `companion/src/lib/types.ts` | BP 3.6 | `CharacterRow`, `RepData`, 10 rep row interfaces |
| `companion/src/lib/computed.ts` | BP 3.7 | `computeCharacter()` — pure, sync, no side effects |
| `companion/src/lib/server/auth.ts` | **DRY C1** | `requireGm(locals, platform)` → `{ db, userId }` |
| `companion/src/routes/+layout.server.ts` | BP 3.3 | Root auth guard: redirect if no session, `SELECT id, is_gm FROM players` |
| `companion/src/routes/+layout.svelte` | BP 3.4 | Nav bar + `{@render children()}` |
| `companion/src/routes/+page.server.ts` | BP 3.4 | Home: redirect to `/characters` if player has characters |
| `companion/src/routes/+page.svelte` | BP 3.4 | "No characters assigned" message |
| `companion/src/routes/admin/+layout.server.ts` | BP 3.3 | GM gate: `parent()` → check `is_gm` |
| `companion/src/routes/admin/assign/+page.server.ts` | BP 3.2 | Load unclaimed chars + players; `actions.assign` |
| `companion/src/routes/admin/assign/+page.svelte` | BP 3.2 | One form per unclaimed character |
| `companion/src/routes/characters/+page.server.ts` | BP 3.5 | Character list (GM sees all, player sees own) |
| `companion/src/routes/characters/+page.svelte` | BP 3.5 | Card list with sync timestamp |
| `companion/src/routes/characters/[id]/+page.server.ts` | BP 3.6 | Detail load: access check + 10 rep queries in parallel + compute |
| `companion/src/routes/characters/[id]/+page.svelte` | BP 3.6 | 5-tab viewer (Overview, Skills, Magic, Gear, Bio) |
| `companion/src/routes/library/+page.svelte` | BP 3.4 | Stub: "Coming in Phase 4" |

### Files to Modify

| File | Blueprint | Changes |
|------|-----------|---------|
| `companion/src/app.d.ts` | BP 3.1 | Add `@auth/sveltekit` Session type augmentation |
| `companion/src/routes/api/sync/+server.ts` | BP 3.8 | Add `OPTIONS` handler + CORS headers |

### Implementation Order

| Step | Blueprint | Action |
|------|-----------|--------|
| 1 | BP 3.1 | Install `@auth/sveltekit @auth/core`; create `src/auth.ts` |
| 2 | BP 3.1 | Create `src/hooks.server.ts` |
| 3 | **DRY C1** | Create `src/lib/server/auth.ts` with `requireGm()` |
| 4 | BP 3.3 | Create root `+layout.server.ts` (auth guard + player SELECT) |
| 5 | BP 3.3 | Create `admin/+layout.server.ts` (GM gate via `parent()`) |
| 6 | BP 3.4 | Create `+layout.svelte` (nav + `{@render children()}`) — **C4 applied: Svelte 5 runes** |
| 7 | BP 3.4 | Create `+page.server.ts` (home redirect) + `+page.svelte` + `library/+page.svelte` stub |
| 8 | BP 3.2 | Create `admin/assign/+page.server.ts` + `.svelte` — **C1 applied: `requireGm()` in form action** |
| 9 | BP 3.6 | Create `src/lib/types.ts` |
| 10 | BP 3.7 | Create `src/lib/computed.ts` |
| 11 | BP 3.5 | Create `characters/+page.server.ts` + `+page.svelte` — **C4 applied: `$props()` not `export let`** |
| 12 | BP 3.6 | Create `characters/[id]/+page.server.ts` + `+page.svelte` — **C4 applied: `$props()`, `$state`, `onclick`** |
| 13 | BP 3.8 | Amend `api/sync/+server.ts` with CORS headers |

### DRY Audit Amendments Applied

**C1 — `requireGm()` extraction** (create in step 3, use in step 8):

```typescript
// companion/src/lib/server/auth.ts
import { error } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import type { Client } from '@libsql/client';

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

Use in form actions (replaces 8-line boilerplate with 1 line): `const { db } = await requireGm(locals, platform);`

**C4 — Svelte 5 runes** (applied in steps 6, 11, 12):
- `export let data: PageData;` → `let { data }: { data: PageData } = $props();`
- `let activeTab: TabId = 'overview';` → `let activeTab: TabId = $state('overview');`
- `on:click={handler}` → `onclick={handler}`

### Auth Model (BP 3.1)

- `SvelteKitAuth(async (event) => { ... })` — lazy config, reads `event.platform?.env` for Discord credentials + `AUTH_SECRET`
- `callbacks.jwt`: on sign-in (`account` present), upsert `players` row with Discord snowflake as PK, pin `token.sub = account.providerAccountId`
- `callbacks.session`: surface `token.sub` as `session.user.id`
- Player upsert: `INSERT INTO players ... ON CONFLICT(id) DO UPDATE SET username, display_name, avatar, updated_at`; `is_gm` never modified (set directly in DB by GM)

**[DEV DECISION]:** Verify Auth.js v4 vs v5 import paths and `(event) => config` form at implementation time.

### Root Layout Auth Guard (BP 3.3)

- `locals.auth()` → if no session, `redirect(302, '/auth/signin')`
- `SELECT id, is_gm FROM players WHERE id = ?` (Discord snowflake = PK lookup)
- Returns `{ session, player: { id, is_gm } }` — consumed by all children via `parent()`
- One DB query per request — never repeated per child route
- `/auth/*` routes intercepted by `authHandle` before layout load runs (no redirect loop)

### Character List (BP 3.5 + C4)

- GM: `SELECT ... FROM characters c JOIN campaigns ca ... ORDER BY char_name ASC` (all)
- Player: same with `WHERE c.player_id = ?`
- Returns `CharacterSummary[]` — card links to `/characters/{id}`

### Character Detail (BP 3.6 + C4)

- Access check: owner OR GM
- 10 rep table queries via `Promise.all` (parallel Turso HTTP)
- `computeCharacter(character, repData)` returns `ComputedFields`
- 5 tabs: Overview (attrs, CM boxes, dice pools), Skills, Magic (spells, foci, adept powers, mutations), Gear (weapons, equipment, money), Bio (identity, karma ledger with running totals, milestones, contacts)
- Empty rep sections: "No {items}" message — never an error

### `computeCharacter()` (BP 3.7)

Pure, sync function. Returns:
- `totalKarma`: sum of all `karma_amount` values
- `conditionMonitorBoxes`: `{ mental: ceil(wil/2)+8, stun: ceil(wil/2)+8, physical: ceil(body/2)+8 }`
- `formattedMoney`: `{ gold, silver, copper }` raw scalars
- `karmaLedgerRunningTotals`: sorted by `id ASC`, each entry accumulates running sum

**[DEV DECISION]:** Stun CM from `wil` (standard SR3) — verify with GM if campaign uses `body`.

### CORS (BP 3.8)

- Add `OPTIONS` handler to `api/sync/+server.ts`
- `Access-Control-Allow-Origin`: exact CF Pages deployment domain (NOT `*`)
- `Access-Control-Allow-Methods: POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, X-Campaign-Secret`
- CORS headers on 2xx and 4xx responses; omit from 5xx

### Acceptance Criteria

- [ ] Discord OAuth flow: `/auth/signin` → Discord → session cookie → redirect
- [ ] First login creates `players` row; subsequent logins update profile fields
- [ ] `is_gm` never modified by sign-in callback
- [ ] All routes redirect unauthenticated users to `/auth/signin`
- [ ] `/admin/*` returns 403 for non-GM
- [ ] Nav renders on all pages with correct links; GM-only "Assign Characters" visible only to GM
- [ ] `/` redirects to `/characters` for players with characters; shows "No characters" otherwise
- [ ] Character list: player sees own, GM sees all
- [ ] Character detail: 404 for unknown UUID, 403 for non-owner non-GM
- [ ] All 5 tabs render; empty rep sections show empty state
- [ ] `OPTIONS /api/sync` returns correct preflight headers
- [ ] All Svelte components use `$props()`, `$state`, `$derived`, `onclick` — no Svelte 4 syntax

---

## Phase 4 — Game Library

**Goal:** Browse curated catalog of all 11 ref_* tables. GM CRUD. Player browse + search + filter.

### Files to Create

| File | Blueprint | Purpose |
|------|-----------|---------|
| `companion/src/lib/catalog-config.ts` | BP 4.2a + 4.3a | `CATALOG_CONFIG` — 11 entries with `table`, `label`, `listColumns`, `filterFields`, `detailFields`, `formFields` |
| `companion/src/lib/server/catalog-utils.ts` | **DRY C5** | Optional `processFormFields()` utility |
| `companion/src/lib/components/CatalogForm.svelte` | BP 4.3c | Shared create/edit form component |
| `companion/src/routes/library/+layout.svelte` | BP 4.4 | Sub-nav bar (11 section links + "All Catalogs") |
| `companion/src/routes/library/+page.server.ts` | BP 4.1 | 11 parallel COUNT queries |
| `companion/src/routes/library/+page.svelte` | BP 4.1 | Card grid with counts + "Add entry" for GM |
| `companion/src/routes/library/[catalog]/+page.server.ts` | BP 4.2b | Load all rows + filter distinct values + delete action |
| `companion/src/routes/library/[catalog]/+page.svelte` | BP 4.2c | Search + filter + expandable detail + spirit stat block |
| `companion/src/routes/library/[catalog]/new/+page.server.ts` | BP 4.3b | GM guard + `actions.create` |
| `companion/src/routes/library/[catalog]/new/+page.svelte` | BP 4.3d | Uses CatalogForm |
| `companion/src/routes/library/[catalog]/[id]/edit/+page.server.ts` | BP 4.3e | GM guard + `actions.update` + `actions.delete` |
| `companion/src/routes/library/[catalog]/[id]/edit/+page.svelte` | BP 4.3f | Uses CatalogForm + inline delete confirmation |

### Implementation Order

| Step | Blueprint | Action | DRY Amendments |
|------|-----------|--------|----------------|
| 1 | BP 4.2a | Create `catalog-config.ts` (list/filter/detail config, no formFields yet) | — |
| 2 | BP 4.1 | Create `library/+page.server.ts` + `+page.svelte` (landing) | **C3: `await getDb()`** |
| 3 | BP 4.2b | Create `[catalog]/+page.server.ts` (list + delete action) | **C1: `requireGm()` in delete action; C3: `await getDb()` in load** |
| 4 | BP 4.2c | Create `[catalog]/+page.svelte` (search/filter/expand) | — |
| 5 | BP 4.3a | Amend `catalog-config.ts` — add `FormFieldDef` + `formFields` per entry | — |
| 6 | BP 4.3c | Create `CatalogForm.svelte` shared component | — |
| 7 | BP 4.3b | Create `[catalog]/new/+page.server.ts` + `+page.svelte` | **C1: `requireGm()` in create action; C2: parent() for load GM check; C3: `await getDb()` in load; C5: optional `processFormFields()`** |
| 8 | BP 4.3e | Create `[catalog]/[id]/edit/+page.server.ts` + `+page.svelte` | **C1: `requireGm()` in update + delete actions; C2: parent() for load GM check; C3: `await getDb()` in load; C5: optional `processFormFields()`** |
| 9 | BP 4.4 | Create `library/+layout.svelte` (sub-nav) | — |

### DRY Audit Amendments Applied

**C1 — `requireGm()` in all form actions:**
Replace 8-line GM re-validation pattern with: `const { db } = await requireGm(locals, platform);`
Applies to: `[catalog]/+page.server.ts` delete action, `new/+page.server.ts` create action, `[id]/edit/+page.server.ts` update + delete actions (5 sites total including Phase 3's admin assign).

**C2 — Load functions use `parent()` for GM check:**
Load functions in `new/+page.server.ts` and `[id]/edit/+page.server.ts` use the simplified pattern (no DB re-query):
```typescript
const { player } = await parent();
if (player.is_gm !== 1) throw error(403, 'Forbidden');
```
NOT form actions — form actions cannot access `parent()` and MUST use `requireGm()`.

**C3 — `await getDb()` everywhere:**
All Phase 4 load functions that call `getDb()` must `await` it:
- `library/+page.server.ts` load
- `[catalog]/+page.server.ts` load
- `[id]/edit/+page.server.ts` load (for entry fetch)
Form actions that use `requireGm()` get `db` from the helper (which handles `await` internally).

**C5 — Optional `processFormFields()`:**
Developer's discretion. If extracted:
```typescript
// companion/src/lib/server/catalog-utils.ts
export function processFormFields(config: CatalogEntry, formData: FormData): {
  values: Record<string, unknown>;
  errors: Record<string, string>;
}
```
Used in create + update actions. Eliminates risk of field-processing loops diverging.

### Catalog Config Structure

11 entries keyed by URL slug. Each entry defines:
- `table`: SQL table name (trusted constant — safe to interpolate)
- `label`: Human-readable heading
- `listColumns`: `{ key, label }[]` — columns in list table
- `filterFields`: `string[]` — drives `SELECT DISTINCT` queries + `<select>` dropdowns
- `detailFields`: `{ key, label }[]` — shown in expanded row panel
- `formFields`: `{ key, label, type: 'text'|'number'|'textarea'|'select', options?: string[] }[]`

| Slug | Table | Filter Fields | Detail Fields Present | Form Field Count |
|---|---|---|---|---|
| `spells` | `ref_spells` | `category`, `type` | Yes (description) | 7 |
| `weapons` | `ref_weapons` | `type` | No | 7 |
| `armor` | `ref_armor` | `location` | No | 8 |
| `equipment` | `ref_equipment` | None | No | 5 |
| `skills` | `ref_skills` | `linked_attr`, `category` | No | 4 |
| `adept-powers` | `ref_adept_powers` | None | Yes (description, game_effect) | 4 |
| `mutations` | `ref_mutations` | None | Yes (description, game_effect) | 5 |
| `totems` | `ref_totems` | `type` | Yes (description, advantages, disadvantages) | 6 |
| `spirits` | `ref_spirits` | `category` | Yes (12 detail fields: 9 formulas + attack + powers + weaknesses) | 14 |
| `spirit-powers` | `ref_spirit_powers` | `type` | Yes (description) | 6 |
| `elemental-services` | `ref_elemental_services` | None | Yes (description) | 2 |

### List Page Client-Side Filtering (BP 4.2c)

Full dataset loaded in server request (~370 rows max). Filtering in browser:
- Text search: `row.name.toLowerCase().includes(searchTerm.toLowerCase())`
- Filter selects: `activeFilters[field] === 'all' || row[field] === filterValue`
- Counter: "Showing N of M entries" — reactive
- Row click toggles expanded detail panel; spirits render `formula_*` as horizontal stat block

### Form Actions Security Pattern

All SQL column identifiers come from `config.formFields[].key` (trusted constant) or `config.table` (trusted constant). **No user-supplied values** ever appear as SQL identifiers. Values are always bound as `?` parameters.

UNIQUE constraint violation on `name`: caught via `err.message.includes('UNIQUE constraint failed')` → return form error (no crash, no redirect).

### Sub-Nav Layout (BP 4.4)

- `$derived` active slug from `page.url.pathname.split('/').filter(Boolean)[1]`
- Correctly highlights section for `/library/spells`, `/library/spells/new`, `/library/spells/42/edit`
- Uses `{@render children()}` — not `<slot />`
- No `+layout.server.ts` — inherits `player` from root layout

### Acceptance Criteria

- [ ] `/library` renders 11 cards with live entry counts
- [ ] All 11 `/library/{slug}` routes render; unknown slug → 404
- [ ] Search filters visible rows in real time (no reload)
- [ ] Filter dropdowns contain only DB-present values
- [ ] Row click expands detail panel; spirit stat block renders formulas
- [ ] GM sees Edit + Delete controls; non-GM does not
- [ ] Create form: adds row, redirects; duplicate name → inline error
- [ ] Edit form: updates row, redirects; duplicate name → inline error
- [ ] Delete: removes row; inline "Are you sure?" confirmation (no `window.confirm()`)
- [ ] Sub-nav renders on all `/library/*` routes; correct section highlighted
- [ ] All `getDb()` calls use `await`
- [ ] All form actions use `requireGm()` from `$lib/server/auth.ts`
- [ ] Load functions use `parent()` + `player.is_gm` check (not DB re-query)

---

## Cross-Cutting Concerns

### Auth Model

| Context | Auth Check Method | Rationale |
|---|---|---|
| Layout load functions | `parent()` → `player.is_gm` | Fresh DB data from root layout, same request |
| Page load functions | `parent()` → `player.is_gm` | Inherits from layout chain |
| Form actions | `requireGm(locals, platform)` | `parent()` unavailable; must re-query DB |
| API routes (`/api/sync`) | `X-Campaign-Secret` header + SHA-256 | No Discord session (Roll20 → server) |

### DB Access Pattern

- **Runtime (CF Workers):** `@libsql/client/web` — Fetch API only
- **Scripts (Node.js):** `@libsql/client/node` — net/tls
- **Per-request client:** No module-level singleton. `getDb(platform!.env)` per request. Lightweight for HTTP clients.
- **FK enforcement:** `PRAGMA foreign_keys = ON` issued by `getDb()` on every client creation
- **`getDb()` is async:** MUST `await` at every call site

### Error Handling

- Auth failures: `error(401)` or `error(403)` via SvelteKit's error helper
- Not found: `error(404)` — never 404 for campaigns (use 401 to prevent enumeration)
- DB errors in sync: catch, `console.error` server-side, return opaque 500
- Form validation: return `{ errors }` object for inline display (no redirect on validation failure)
- UNIQUE constraint violations: catch by message string match, return form error

### Svelte 5 Conventions

| Pattern | Use | Do NOT Use |
|---|---|---|
| Props | `let { data }: { data: PageData } = $props();` | `export let data` |
| Reactive state | `let x = $state(initialValue);` | `let x = initialValue;` (for reactive) |
| Derived | `const y = $derived(expression);` | `$: y = expression;` |
| Event handlers | `onclick={handler}` | `on:click={handler}` |
| Children | `{@render children()}` | `<slot />` |

### New Files from DRY Audit

| File | Purpose | Source |
|---|---|---|
| `companion/src/lib/server/auth.ts` | `requireGm(locals, platform)` → `{ db, userId }` | C1 — mandatory |
| `companion/src/lib/server/catalog-utils.ts` | `processFormFields(config, formData)` → `{ values, errors }` | C5 — optional, developer's discretion |

---

## Open [DEV DECISION] Items

These are deferred implementation-time decisions documented across L2/L3. The developer resolves each during the relevant phase.

### Phase 0
1. None — all decisions resolved in planning

### Phase 1
2. **Characters column enumeration:** Map 1:1 from Roll20 `scalarFields` array → DDL columns using type rules (BP 1.3)
3. **Armor rating columns:** Verify P/S/I headers in Equipment.xlsx (BP 1.3 ref_armor)
4. **Skill specializations:** TEXT comma-list vs. join table — TEXT recommended for V1 (BP 1.3)
5. **Spirit powers storage:** Comma-separated TEXT vs. join table — TEXT for V1 (BP 1.3)
6. **Spirit power sub-variants:** One row per variant vs. parent row with variants in description (BP 1.3)
7. **DDL execution method:** CLI pipe vs. migration script — script recommended (BP 1.3)
8. **Seed upserted vs. updated counts:** `SELECT COUNT(*)` before/after for precise counts — optional (BP 1.5)
9. **Workbook sheet names:** Verify actual names with `workbook.SheetNames` before implementing parsers (BP 1.5)
10. **`platform.env` access pattern:** Verify SvelteKit version's exact access for `event.platform?.env` (BP 1.4)

### Phase 2
11. **Turso batch size limits:** Monitor but don't pre-optimize — 42 statements typical (BP 2.2)
12. **`roll20_character_id`:** NULL on INSERT; future PATCH endpoint if needed (BP 2.2)
13. **CAMPAIGN_SECRET in sheet source:** Visible to Roll20 editor (GM only); acceptable for closed group (BP 2.3)

### Phase 3
14. **Auth.js import paths:** Verify v4 vs v5 paths at implementation time (BP 3.1)
15. **Discord profile fields:** Verify `global_name` availability; fall back to `profile.name` (BP 3.1)
16. **Discord avatar storage:** Hash vs. full CDN URL — hash preferred (BP 3.1)
17. **Sign-out method:** GET link vs. POST form depending on Auth.js version (BP 3.4)
18. **`/auth/*` interception:** Verify layout load doesn't run for auth routes (BP 3.3)
19. **`platform.env` in local dev:** Use `wrangler pages dev` to ensure `platform.env` is populated (BP 3.3)
20. **Promise.all for 10 rep queries:** Fall back to sequential if Turso 429 errors occur (BP 3.6)
21. **CharacterRow index signature:** Replace with full 129-column explicit listing if strict access preferred (BP 3.6)
22. **CM formula (stun track):** Verify `wil` vs `body` with GM (BP 3.7)
23. **Karma ledger sort order:** `id ASC` may not be chronological if Roll20 UUIDs are non-monotonic (BP 3.7)
24. **CORS origin:** Hardcode production domain; whitelist only if custom domain configured (BP 3.8)

### Phase 4
25. **Client-side filtering:** Add server-side query params only if page load becomes slow (BP 4.2)
26. **Delete on list page:** Co-located inline delete vs. navigate to edit page first — co-located recommended (BP 4.2b)
27. **Spell categories in formFields select:** Verify exact categories against Spells.xlsx (BP 4.3a)
28. **CatalogForm extraction:** Extract if >30% duplication reduction — yes, extracted (BP 4.3c)
29. **Sub-nav layout:** If 11 links too crowded, group into rows or collapsible drawer (BP 4.4)

---

## Complete File Manifest

Every file the companion app will contain when all phases are complete.

### `companion/` — Root

```
companion/
├── .dev.vars                                          # Local secrets (GITIGNORED)
├── .gitignore                                         # .dev.vars
├── package.json                                       # scripts: dev, build, migrate, seed, seed-campaign
├── svelte.config.js                                   # adapter-cloudflare, vitePreprocess()
├── tsconfig.json                                      # SvelteKit default
├── vite.config.ts                                     # SvelteKit default
└── wrangler.toml                                      # nodejs_compat, pages_build_output_dir
```

### `companion/db/`

```
companion/db/
└── schema.sql                                         # Authoritative DDL — 24 tables + 17 indices
```

### `companion/scripts/`

```
companion/scripts/
├── migrate.ts                                         # Execute schema.sql (--force flag)
├── seed.ts                                            # Parse 5 Excel workbooks → upsert 11 ref_* tables
└── seed-campaign.ts                                   # Seed campaigns row with hashed secret
```

### `companion/src/`

```
companion/src/
├── app.d.ts                                           # App.Platform['env'] + Session type augmentation
├── app.html                                           # SvelteKit shell
├── auth.ts                                            # SvelteKitAuth + Discord + player upsert
├── hooks.server.ts                                    # sequence(authHandle, appHandle)
└── lib/
    ├── catalog-config.ts                              # CATALOG_CONFIG — 11 entries (table, columns, formFields)
    ├── computed.ts                                    # computeCharacter() — pure sync function
    ├── db.ts                                          # getDb(env) — async, @libsql/client/web, PRAGMA FK ON
    ├── sync-write.ts                                  # syncWrite() — allowlists, batch builder
    ├── types.ts                                       # CharacterRow, RepData, 10 rep row interfaces
    ├── components/
    │   └── CatalogForm.svelte                         # Shared create/edit form component
    └── server/
        ├── auth.ts                                    # requireGm(locals, platform) — DRY C1
        └── catalog-utils.ts                           # processFormFields() — DRY C5 (optional)
```

### `companion/src/routes/`

```
companion/src/routes/
├── +layout.server.ts                                  # Root auth guard + player SELECT
├── +layout.svelte                                     # Nav bar + {@render children()}
├── +page.server.ts                                    # Home redirect to /characters
├── +page.svelte                                       # "No characters assigned" fallback
├── admin/
│   ├── +layout.server.ts                              # GM gate via parent()
│   └── assign/
│       ├── +page.server.ts                            # Load unclaimed + players; actions.assign
│       └── +page.svelte                               # One form per unclaimed character
├── api/
│   └── sync/
│       └── +server.ts                                 # POST validation + OPTIONS CORS handler
├── characters/
│   ├── +page.server.ts                                # Character list (GM=all, player=own)
│   ├── +page.svelte                                   # Card list
│   └── [id]/
│       ├── +page.server.ts                            # Detail: access check + 10 rep queries + compute
│       └── +page.svelte                               # 5-tab viewer
└── library/
    ├── +layout.svelte                                 # Sub-nav bar (11 sections)
    ├── +page.server.ts                                # 11 parallel COUNT queries
    ├── +page.svelte                                   # Card grid with counts
    └── [catalog]/
        ├── +page.server.ts                            # SELECT * + DISTINCT filters + delete action
        ├── +page.svelte                               # Search/filter/expand/spirit stat block
        ├── new/
        │   ├── +page.server.ts                        # GM guard + actions.create
        │   └── +page.svelte                           # CatalogForm (create mode)
        └── [id]/
            └── edit/
                ├── +page.server.ts                    # GM guard + actions.update + actions.delete
                └── +page.svelte                       # CatalogForm (edit mode) + inline delete
```

### Roll20 Sheet Files (Phase 0)

```
sheet.html                                             # HTML + CSS + Sheet Worker (modified)
sheet.css                                              # Styles (modified — money row, karma, milestones)
```

### Total File Count

| Category | Count |
|---|---|
| Config/build files | 7 |
| Database | 1 |
| Scripts | 3 |
| Source lib | 8 |
| Source routes | 22 |
| Roll20 sheet | 2 |
| **Total** | **43** |
