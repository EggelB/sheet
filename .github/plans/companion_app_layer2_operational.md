# Layer 2 — Phase 0: Roll20 Sheet Updates

**Goal:** Add `money_gold/silver/copper` scalar fields, `repeating_karma` ledger section, `repeating_milestones` section, remove 20 Questions from the sheet (companion app owns that data), and complete the sync handler to collect all 10 repeating sections.

---

## Task 1 — Add Money scalar fields to top of Gear tab (HTML + CSS)

**Steps:**

1a. In `sheet.html`, locate the Gear tab panel opening (`<div class="sheet-tab-panel sheet-tab-panel-gear">`, line 1057). Immediately after the panel div (before the existing `<!-- Region: Armor Panel -->` comment), insert:
- `<h3 class="sheet-section-title">Money</h3>`
- `<div class="sheet-money-row">` containing three labeled number inputs:
  - Label "Gold:" + `<input type="number" name="attr_money_gold" value="0">`
  - Label "Silver:" + `<input type="number" name="attr_money_silver" value="0">`
  - Label "Copper:" + `<input type="number" name="attr_money_copper" value="0">`

1b. In `sheet.css`, add a `.sheet-money-row` rule using the same flexbox/gap pattern as `.sheet-karma-row` (horizontal flex, centered items, gap between label/input pairs, inputs ~70px wide).

**Acceptance Criteria:** Three labeled number inputs are visible at the very top of the Gear tab (above Armor); values persist when typed; the row visually matches the karma row styling on Core tab.

---

## Task 2 — Remove 20 Questions from Bio tab (HTML + CSS)

**Steps:**

2a. In `sheet.html`, locate the Bio tab panel (`<div class="sheet-tab-panel sheet-tab-panel-bio">`, line 1208). Remove all 20 Q&A label+textarea pairs (Q1 through Q20, `attr_bio_q01` through `attr_bio_q20`). Keep "Description" and "Notes" textareas — those remain.

2b. In the sync handler's `scalarFields` array, remove all `bio_q01` through `bio_q20` entries. These fields still exist in Roll20's attribute store (data isn't deleted), but they no longer need to sync. The companion app will own the 20 Questions data going forward.

2c. No CSS changes needed — the bio question styling inherits from the generic label+textarea rules already in the bio section.

**Acceptance Criteria:** Bio tab shows only Description and Notes (plus whatever new sections we add in Tasks 3-4). The 20 questions no longer appear. Existing bio_q data in Roll20 is unaffected (just hidden from UI).

---

## Task 3 — Add `repeating_karma` ledger section to Bio tab (HTML + CSS)

**Steps:**

3a. In `sheet.html`, inside the Bio tab panel, after the Notes textarea, add:
- `<h3 class="sheet-section-title">Karma Ledger</h3>`
- A column-header row `<div class="sheet-karma-log-header">` with two `<span>` elements: "Event" (class `sheet-hdr-karma-event`) and "Amount" (class `sheet-hdr-karma-amount`). Plus an empty spacer span for Roll20's auto-generated delete button column.

3b. Add `<fieldset class="repeating_karma">` containing:
- `<input type="text" name="attr_karma_event" placeholder="Event">` with class `sheet-karma-log-event`
- `<input type="number" name="attr_karma_amount" value="0">` with class `sheet-karma-log-amount`

3c. In `sheet.css`, add layout rules for `.sheet-karma-log-header` and `.repeating_karma` rows. Two-column grid: Event takes remaining width (flex-grow), Amount is fixed ~70px. Column headers visually align with the input fields below.

**Acceptance Criteria:** Karma Ledger section appears on Bio tab below Description/Notes; Roll20 "Add" button works; entries show text + number fields; headers align with fields; entries persist across reloads.

---

## Task 4 — Add `repeating_milestones` section to Bio tab (HTML + CSS)

**Steps:**

4a. In `sheet.html`, directly after the closing `</fieldset>` of `repeating_karma`, add:
- `<h3 class="sheet-section-title">Milestones</h3>`
- A column-header row `<div class="sheet-milestones-header">` with spans: "Trial" (class `sheet-hdr-milestone-trial`), "Tier 1" (`sheet-hdr-milestone-tier1`), "Tier 2" (`sheet-hdr-milestone-tier2`), "Tier 3" (`sheet-hdr-milestone-tier3`), "Cur" (`sheet-hdr-milestone-current`), and empty spacer.

4b. Add `<fieldset class="repeating_milestones">` containing:
- `<input type="text" name="attr_milestone_trial" placeholder="Trial Name">` — class `sheet-milestone-trial`
- `<input type="text" name="attr_milestone_tier1" placeholder="Tier 1">` — class `sheet-milestone-tier1`
- `<input type="text" name="attr_milestone_tier2" placeholder="Tier 2">` — class `sheet-milestone-tier2`
- `<input type="text" name="attr_milestone_tier3" placeholder="Tier 3">` — class `sheet-milestone-tier3`
- `<input type="number" name="attr_milestone_current" value="0" min="0" max="3">` — class `sheet-milestone-current`

All tier fields use `<input type="text">` (single-line). These hold short mechanical phrases like "Leechskin: Consider Decrease Attribute as 1 less force when sustaining" — punchy enough for single-line inputs.

4c. In `sheet.css`, add a 5-column grid layout for `.sheet-milestones-header` and `.repeating_milestones` rows:
- Trial: flex-grow (widest)
- Tier 1/2/3: equal width, ~150-180px each
- Current: narrow fixed ~50px
- Align header spans with their corresponding input columns

**Design note:** Milestones are a fixed 3-tier progression system. Characters "level up" through them — always exactly 3 tiers per trial path, no more. The `milestone_current` field (0/1/2/3) tracks which tier has been achieved. Each character has unique trials with their own flavor.

**Acceptance Criteria:** Milestones section appears on Bio tab below Karma Ledger; "Add" button works; each row shows all five fields; `milestone_current` only accepts 0-3; column headers align with fields.

---

## Task 5 — Complete the sync handler for all 10 repeating sections

This task modifies only the Sheet Worker `<script type="text/worker">` block. No HTML or CSS changes.

**Steps:**

5a. In the `on('clicked:btn_sync_db', ...)` handler, locate the `scalarFields` array. Add `'money_gold'`, `'money_silver'`, `'money_copper'` to the array. Remove `'bio_q01'` through `'bio_q20'` (already done in Task 2b — listed here for completeness).

5b. Reference: complete field list for each of the 10 repeating sections:

| Section | Fields to collect |
|---|---|
| `repeating_skills` | `skill_name`, `skill_linked_attr`, `skill_general`, `skill_spec`, `skill_base`, `skill_foci`, `skill_misc`, `skill_total` |
| `repeating_mutations` | `mutation_name`, `mutation_level`, `mutation_essence`, `mutation_bp_cost`, `mutation_effect` |
| `repeating_adept_powers` | `power_name`, `power_level`, `power_pp_cost`, `power_pp_cost_value`, `power_effect` |
| `repeating_spells` | `spell_name`, `spell_force`, `spell_drain` |
| `repeating_foci` | `focus_name`, `focus_type`, `focus_force`, `focus_bonded`, `focus_notes` |
| `repeating_weapons` | `weapon_name`, `weapon_type`, `weapon_modifiers`, `weapon_power`, `weapon_damage`, `weapon_conceal`, `weapon_reach`, `weapon_ep`, `weapon_range_short`, `weapon_range_medium`, `weapon_range_long`, `weapon_range_extreme` |
| `repeating_equipment` | `equip_name`, `equip_description`, `equip_ep` |
| `repeating_contacts` | `contact_name`, `contact_info`, `contact_level` |
| `repeating_karma` | `karma_event`, `karma_amount` |
| `repeating_milestones` | `milestone_trial`, `milestone_tier1`, `milestone_tier2`, `milestone_tier3`, `milestone_current` |

5c. Replace `repeating: {}` in the payload construction with a populated `repeating` object. Implementation approach:

- **Counter/latch pattern** (recommended over nested callbacks): Declare `var remaining = 11;` (10 sections + 1 for scalar getAttrs). Each callback decrements `remaining` and calls a `proceed()` function when `remaining === 0`.
- Launch all 10 `getSectionIDs()` calls in parallel with scalar `getAttrs()`
- For each section, inner `getAttrs()` grabs all fields for all row IDs
- Accumulate into `payload.repeating` keyed by section name (e.g. `repeating.skills = [{...}, ...]`)
- Empty sections produce `[]`, not `undefined` or `null`
- `fetch(SYNC_PROXY_URL, ...)` fires only after all 11 callbacks have resolved

5d. The existing `getAttrs(scalarFields, function(attrs) { ... })` block becomes one of the 11 parallel callbacks. It sets `payload.scalars` and decrements `remaining`. The `fetch` call moves into the shared `proceed()` function.

**Acceptance Criteria:**
- `money_gold`, `money_silver`, `money_copper` appear in `payload.scalars`
- `bio_q01`–`bio_q20` are NOT in `payload.scalars`
- `payload.repeating` has exactly 10 keys (one per section)
- Each key's value is an array of row objects with all field names from the table above
- Sections with zero rows produce `[]`
- Sync button still shows "Syncing…" immediately and updates on completion

---

## Ordering and Dependencies

| Order | Task | Depends on | Tab affected |
|---|---|---|---|
| 1st | Task 1 — Money HTML + CSS | none | Gear |
| 2nd | Task 2 — Remove 20 Questions | none | Bio |
| 3rd | Task 3 — Karma ledger HTML + CSS | none (recommended after Task 2 for clean diff) | Bio |
| 4th | Task 4 — Milestones HTML + CSS | none (recommended after Task 3 for page order) | Bio |
| 5th | Task 5 — Sync handler completion | Tasks 1-4 (all fields must exist) | Script block |

Tasks 1, 2, 3, and 4 are all structurally independent — they touch different parts of the file. Recommended order is 1→2→3→4 for clean diffs (Task 2 frees Bio space before 3/4 add to it), but not a hard dependency. Task 5 must follow all four.

---

## Bio Tab Final Layout (post-changes)

```
Bio Tab
├── Description (textarea, existing)
├── Notes (textarea, existing)
├── Karma Ledger (NEW repeating — event + amount)
└── Milestones (NEW repeating — trial + 3 tiers + current)
```

20 Questions removed. Data preserved in Roll20 attribute store but no longer rendered or synced. Companion app will own that data going forward.

---

## Companion App Impact

These changes also affect the companion app plan (to be captured in later layers):
- **20 Questions:** ~~Companion app Phase 3 (Character Viewer) should include a "Bio" view that displays the 20 questions. This data will need a one-time migration from Roll20 → Turso, or manual re-entry.~~ **[Resolved — Phase 3 L2]:** 20 Questions display confirmed out of scope for V1. Bio question fields are removed from sync; no migration required. Not a Phase 0 concern.
- **Money:** Will render in companion character viewer alongside gear.
- **Karma Ledger + Milestones:** Will render in companion character viewer with dedicated views (running total for karma, tier progression cards for milestones).

---


---

# Layer 2 — Phase 1: Project Scaffold + Database Schema + Seed Utility

**Goal:** Standing SvelteKit project with Turso connected, all 24 tables created, reference data seeded. Seed utility is a proper CI/CD-ready CLI tool that can be re-run idempotently.

---

## Task 1 — Scaffold SvelteKit project in `companion/`

**Steps:**

1a. From `c:\Users\bryce\source\sheet`, initialize a new SvelteKit project into `companion/` using `npm create svelte@latest companion`. Selections: Skeleton project, TypeScript syntax, ESLint, Prettier. Do NOT select Vitest or Playwright at scaffold time.

1b. `cd companion && npm install`

1c. Install additional dependencies:
- `@sveltejs/adapter-cloudflare` (replaces `adapter-auto`)
- `@libsql/client` (installs both `/web` and `/node` subpath exports)
- `tsx` (TypeScript script runner for local CLI tools — devDependency)
- `xlsx` (SheetJS for Excel parsing — devDependency; needed by seed script but install now to keep package management clean)

1d. Update `svelte.config.js`: import from `@sveltejs/adapter-cloudflare` and replace any existing adapter usage with it.

1e. Create `companion/wrangler.toml` with these fields:
- `name` = deployment name (e.g., `"companion-app"`)
- `compatibility_date` = latest recommended date at time of implementation
- `compatibility_flags = ["nodejs_compat"]` — required for `@libsql/client` usage in CF Workers
- `pages_build_output_dir = ".svelte-kit/cloudflare"`

1f. Create `companion/.dev.vars` (CF Pages local secrets equivalent). Populate with placeholder keys — values filled in Task 2:
```
TURSO_DATABASE_URL=
TURSO_AUTH_TOKEN=
CAMPAIGN_SECRET=
AUTH_SECRET=
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
```

1g. Add `companion/.dev.vars` to `.gitignore` (root or a `companion/.gitignore`). This file must never be committed.

1h. Create two empty directories: `companion/db/` (for schema artifacts) and `companion/scripts/` (for CLI tools). Add `.gitkeep` files so directories are tracked.

1i. Verify: `npm run dev` starts on localhost without errors. A skeleton page is sufficient.

**Acceptance Criteria:**
- `companion/` contains a valid SvelteKit + TypeScript project
- `npm run dev` starts without errors from `companion/`
- `wrangler.toml` present with `nodejs_compat` flag and correct `pages_build_output_dir`
- `svelte.config.js` uses `adapter-cloudflare`
- `.dev.vars` exists and is gitignored

---

## Task 2 — Create Turso database and generate auth token

**Steps:**

2a. Install Turso CLI if not present: `npm install -g @turso/cli` (or via platform package manager).

2b. Authenticate: `turso auth login`

2c. Create the database: `turso db create companion-app` (or chosen name). Record the returned database URL (format: `libsql://companion-app-{user}.turso.io`).

2d. Generate one read-write auth token: `turso db tokens create companion-app`. This single token is used for all three contexts:
- Local seed utility (`.dev.vars`)
- CF Pages production (stored as a Cloudflare Pages environment secret — NOT in `wrangler.toml`)
- Local dev server (`.dev.vars`)

2e. Populate `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` in `companion/.dev.vars` with the values from steps 2c–2d.

2f. Verify connectivity: `turso db shell companion-app`. Run `.tables` — should return empty (no tables yet).

**Acceptance Criteria:**
- Turso database exists and is reachable
- `turso db shell companion-app` connects without errors
- `.dev.vars` has non-empty `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`

---

## Task 3 — Write and execute DDL: all 24 tables + indices

This task produces `companion/db/schema.sql` — the authoritative DDL file. Tables defined in dependency order (FKs reference already-created tables). All FK constraints are declared; enforcement requires `PRAGMA foreign_keys = ON` at runtime (Turso does not enable this by default — see Task 4).

### 3.1 — Auth/meta tables (2 tables)

**`campaigns`** (no FK dependencies — create first)

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID (v4), generated at campaign creation |
| `name` | TEXT | NOT NULL | Campaign display name |
| `campaign_secret_hash` | TEXT | NOT NULL | Hash of shared sync secret; plaintext never stored |
| `created_at` | TEXT | DEFAULT (datetime('now')) | ISO-8601 text |

**`players`** (no FK dependencies)

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | Discord user ID (snowflake string) |
| `username` | TEXT | NOT NULL | Discord username at time of last login |
| `display_name` | TEXT | | Discord display name (nullable for some accounts) |
| `avatar` | TEXT | | Full Discord avatar URL |
| `is_gm` | INTEGER | NOT NULL DEFAULT 0 | 0=player, 1=GM; only set directly in DB, never self-assignable |
| `created_at` | TEXT | DEFAULT (datetime('now')) | |
| `updated_at` | TEXT | DEFAULT (datetime('now')) | Refreshed on each login |

### 3.2 — Character scalar table (1 table)

**`characters`** (FK → players, campaigns)

Backbone columns (definitive):

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID generated by companion on first sync |
| `player_id` | TEXT | FK → players(id) | Nullable by design — sync payload has no Discord context. Phase 3 backfills on first Discord login via player-claims-character flow. |
| `campaign_id` | TEXT | NOT NULL, FK → campaigns(id) | |
| `roll20_character_id` | TEXT | UNIQUE | Nullable by design — Roll20 Sheet Workers cannot access the platform's internal character entity ID via `getAttrs`. May add manual GM population (hidden attr) in V1.1 if cross-reference proves necessary. |
| `sync_version` | INTEGER | NOT NULL DEFAULT 0 | Incremented on each successful sync |
| `synced_at` | TEXT | DEFAULT (datetime('now')) | Timestamp of last successful sync |
| `created_at` | TEXT | DEFAULT (datetime('now')) | |
| `updated_at` | TEXT | DEFAULT (datetime('now')) | |

**[DEV DECISION] — Full `characters` column enumeration:** The remaining game-data columns correspond 1:1 to the Roll20 `scalarFields` array in `sheet.html`'s sync handler (Phase 0, Task 5a). Developer must:

1. Open `sheet.html`, locate the `scalarFields` array in the `clicked:btn_sync_db` handler
2. Create one column per field, using this type mapping:
   - `type="number"` inputs → `INTEGER` (use `REAL` for `essence_total` and any field that may be fractional)
   - `type="checkbox"` inputs (value="1") → `INTEGER` (stores 1 or 0; includes all `cm_*` boxes and `skill_spec`)
   - `<select>` elements → `TEXT` (stores the selected option's value string)
   - All other fields (`type="text"`, `<textarea>`, `type="hidden"`) → `TEXT`
3. Include Phase 0 additions explicitly: `money_gold INTEGER`, `money_silver INTEGER`, `money_copper INTEGER`

**Confirmed columns (sample — names must match scalarFields exactly):**

| Column | Type | scalarField |
|---|---|---|
| `money_gold` | INTEGER | `money_gold` |
| `money_silver` | INTEGER | `money_silver` |
| `money_copper` | INTEGER | `money_copper` |
| `karma_good` | INTEGER | `karma_good` |
| `karma_used` | INTEGER | `karma_used` |
| `karma_total` | INTEGER | `karma_total` |
| `karma_pool` | INTEGER | `karma_pool` |
| `body` | INTEGER | `body` |
| `dex` | INTEGER | `dex` |
| `str` | INTEGER | `str` |
| `cha` | INTEGER | `cha` |
| `int` | INTEGER | `int` |
| `wil` | INTEGER | `wil` |
| `hum` | INTEGER | `hum` |
| `essence_total` | REAL | `essence_total` |
| `mag` | INTEGER | `mag` |

**CRITICAL:** Column names in `characters` table **must** match the scalarField keys exactly (those keys become the payload property names). Do NOT prefix with `attr_` — the scalarFields array already strips that prefix.

### 3.3 — Character repeating section tables (10 tables)

All 10 sharing this backbone:

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID generated by companion |
| `character_id` | TEXT | NOT NULL, FK → characters(id) ON DELETE CASCADE | |
| `roll20_row_id` | TEXT | NOT NULL | Roll20's internal row ID within the section |
| — | — | UNIQUE (character_id, roll20_row_id) | Composite unique constraint |

Plus table-specific columns from Phase 0 L2 field definitions:

**`rep_skills`**

| Column | Type |
|---|---|
| `skill_name` | TEXT |
| `skill_linked_attr` | TEXT |
| `skill_general` | TEXT |
| `skill_spec` | INTEGER |
| `skill_base` | INTEGER |
| `skill_foci` | INTEGER |
| `skill_misc` | INTEGER |
| `skill_total` | INTEGER |

**`rep_mutations`**

| Column | Type | Notes |
|---|---|---|
| `mutation_name` | TEXT | |
| `mutation_level` | INTEGER | |
| `mutation_essence` | REAL | Fractional value (HTML uses `type="number"`) |
| `mutation_bp_cost` | INTEGER | |
| `mutation_effect` | TEXT | |

**`rep_adept_powers`**

| Column | Type | Notes |
|---|---|---|
| `power_name` | TEXT | |
| `power_level` | INTEGER | |
| `power_pp_cost` | TEXT | Display string (e.g., "0.5 per level") |
| `power_pp_cost_value` | REAL | Numeric value for pool calculations |
| `power_effect` | TEXT | |

**`rep_spells`**

| Column | Type |
|---|---|
| `spell_name` | TEXT |
| `spell_force` | INTEGER |
| `spell_drain` | TEXT |

**`rep_foci`**

| Column | Type | Notes |
|---|---|---|
| `focus_name` | TEXT | |
| `focus_type` | TEXT | |
| `focus_force` | INTEGER | |
| `focus_bonded` | INTEGER | 0/1 boolean |
| `focus_notes` | TEXT | |

**`rep_weapons`**

| Column | Type |
|---|---|
| `weapon_name` | TEXT |
| `weapon_type` | TEXT |
| `weapon_modifiers` | TEXT |
| `weapon_power` | INTEGER |
| `weapon_damage` | TEXT |
| `weapon_conceal` | INTEGER |
| `weapon_reach` | INTEGER |
| `weapon_ep` | INTEGER |
| `weapon_range_short` | TEXT |
| `weapon_range_medium` | TEXT |
| `weapon_range_long` | TEXT |
| `weapon_range_extreme` | TEXT |

**`rep_equipment`**

| Column | Type |
|---|---|
| `equip_name` | TEXT |
| `equip_description` | TEXT |
| `equip_ep` | INTEGER |

**`rep_contacts`**

| Column | Type |
|---|---|
| `contact_name` | TEXT |
| `contact_info` | TEXT |
| `contact_level` | TEXT |

**`rep_karma`**

| Column | Type | Notes |
|---|---|---|
| `karma_event` | TEXT | Event description |
| `karma_amount` | INTEGER | Positive = grant, negative = expenditure |

**`rep_milestones`**

| Column | Type | Notes |
|---|---|---|
| `milestone_trial` | TEXT | Trial name |
| `milestone_tier1` | TEXT | Tier 1 description |
| `milestone_tier2` | TEXT | Tier 2 description |
| `milestone_tier3` | TEXT | Tier 3 description |
| `milestone_current` | INTEGER | Current tier achieved (0–3) |

### 3.4 — Reference catalog tables (11 tables)

All 11 catalog tables share these backbone columns:

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `created_at` | TEXT | DEFAULT (datetime('now')) |
| `updated_at` | TEXT | DEFAULT (datetime('now')) |

All have a `UNIQUE (name)` constraint — this is the conflict target for idempotent seed upserts.

---

**`ref_spells`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `category` | TEXT | NOT NULL — equals the sheet name from Spells.xlsx (e.g., "Combat", "Detection", "Health") |
| `type` | TEXT | "M" (mana) or "P" (physical) |
| `target` | TEXT | Targeting mechanic |
| `duration` | TEXT | Duration code (e.g., "I", "S", "P") |
| `drain` | TEXT | Drain code (e.g., "(F÷2)−2") |
| `description` | TEXT | Full rules text |

---

**`ref_weapons`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `type` | TEXT | Weapon category (Edged, Clubs, Projectile, etc.) |
| `conceal` | INTEGER | Concealment rating |
| `reach` | INTEGER | Reach modifier |
| `damage` | TEXT | Damage code (e.g., "9S") |
| `ep` | INTEGER | Encumberment Points |
| `cost` | INTEGER | Cost in gold/silver equivalent |

---

**`ref_armor`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `location` | TEXT | Body location (Full Body, Partial Body, etc.) |
| `conceal` | INTEGER | |
| `rating_p` | INTEGER | Physical/power protection rating |
| `rating_s` | INTEGER | Stopping power rating |
| `rating_i` | INTEGER | Impact rating |
| `ep` | INTEGER | Encumberment Points |
| `cost` | INTEGER | |

**[DEV DECISION]:** Open Equipment.xlsx > Armor tab and verify protection rating column headers are "P", "S", "I" as expected. If headers differ, rename `rating_p/s/i` before executing DDL.

---

**`ref_equipment`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `conceal` | INTEGER | |
| `ep` | INTEGER | |
| `cost` | INTEGER | |
| `notes` | TEXT | |

---

**`ref_skills`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `linked_attr` | TEXT | e.g., "Body", "Quickness", "Intelligence" |
| `category` | TEXT | Skill category grouping |
| `specializations` | TEXT | Comma-separated list of valid specializations |

**[DEV DECISION]:** If specializations exceed ~5 per skill, comma-list TEXT becomes unwieldy in library UI. Decide at implementation time: keep as TEXT (simple, V1-appropriate) or extract to a `ref_skill_specializations` join table (enables future filtering by specialization).

---

**`ref_adept_powers`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `pp_cost` | TEXT | Power Point cost string (may include "per level") |
| `description` | TEXT | |
| `game_effect` | TEXT | Mechanical rules text |

---

**`ref_mutations`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `essence` | TEXT | Essence cost as text (may be "0.2", "0.1 per level") |
| `bp_cost` | INTEGER | Build Point cost |
| `description` | TEXT | |
| `game_effect` | TEXT | Mechanical rules text |

---

**`ref_totems`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `type` | TEXT | NOT NULL — "Animal" or "Nature" |
| `environment` | TEXT | Primary environment (e.g., "Forest", "Urban", "Mountain") |
| `description` | TEXT | Lore/flavor paragraph |
| `advantages` | TEXT | Mechanical bonuses (e.g., "+2 dice for combat spells") |
| `disadvantages` | TEXT | Behavioral restrictions |

---

**`ref_spirits`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `category` | TEXT | NOT NULL — "Elemental" or "Nature" |
| `formula_b` | TEXT | Body stat formula (e.g., "F+4") |
| `formula_q` | TEXT | Quickness formula |
| `formula_s` | TEXT | Strength formula |
| `formula_c` | TEXT | Charisma formula |
| `formula_i` | TEXT | Intelligence formula |
| `formula_w` | TEXT | Willpower formula |
| `formula_e` | TEXT | Essence formula |
| `formula_r` | TEXT | Reaction formula |
| `formula_initiative` | TEXT | Initiative dice formula |
| `attack` | TEXT | Attack code formula |
| `powers` | TEXT | Comma-separated power names from ref_spirit_powers |
| `weaknesses` | TEXT | |

**[DEV DECISION]:** `powers` stored as comma-separated TEXT (no FK enforcement) vs. a `ref_spirit_powers_map` join table. V1 read-only display makes comma-list acceptable — this call is deferred to implementation.

---

**`ref_spirit_powers`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `type` | TEXT | "P" (physical) or "M" (magical) |
| `action` | TEXT | Action type to use (Complex, Simple, Free, etc.) |
| `range` | TEXT | Range indicator (Self, LOS, etc.) |
| `duration` | TEXT | Duration type |
| `description` | TEXT | Full rules text including any elemental variants |

**[DEV DECISION]:** Some powers have elemental sub-variants (e.g., Fire/Water/Air/Earth Engulf). Decide: one row per variant (cleaner queries, more rows) vs. parent row with variants described in `description` text (simpler seeding). Separate rows are preferred for Phase 4 library display clarity.

---

**`ref_elemental_services`**

| Column | Type | Notes |
|---|---|---|
| `name` | TEXT | UNIQUE NOT NULL |
| `description` | TEXT | Full rules text for this service type |

---

### 3.5 — Indices

Declared in `schema.sql` after all CREATE TABLE statements:

| Index name | Table | Columns | Rationale |
|---|---|---|---|
| `idx_characters_player` | `characters` | `(player_id)` | Character list page |
| `idx_characters_campaign` | `characters` | `(campaign_id)` | Sync validation |
| `idx_rep_skills_char` | `rep_skills` | `(character_id)` | Character detail page joins |
| `idx_rep_mutations_char` | `rep_mutations` | `(character_id)` | |
| `idx_rep_adept_powers_char` | `rep_adept_powers` | `(character_id)` | |
| `idx_rep_spells_char` | `rep_spells` | `(character_id)` | |
| `idx_rep_foci_char` | `rep_foci` | `(character_id)` | |
| `idx_rep_weapons_char` | `rep_weapons` | `(character_id)` | |
| `idx_rep_equipment_char` | `rep_equipment` | `(character_id)` | |
| `idx_rep_contacts_char` | `rep_contacts` | `(character_id)` | |
| `idx_rep_karma_char` | `rep_karma` | `(character_id)` | Karma ledger by character |
| `idx_rep_milestones_char` | `rep_milestones` | `(character_id)` | |
| `idx_ref_spells_category` | `ref_spells` | `(category)` | Library spell browser filter |
| `idx_ref_spells_type` | `ref_spells` | `(type)` | M/P filter |
| `idx_ref_weapons_type` | `ref_weapons` | `(type)` | Library weapon browser filter |
| `idx_ref_totems_type` | `ref_totems` | `(type)` | Animal vs Nature filter |
| `idx_ref_spirits_category` | `ref_spirits` | `(category)` | Elemental vs Nature filter |

### 3.6 — Execute DDL

After `companion/db/schema.sql` is finalized, execute it against the Turso database:
- CLI method: `turso db shell companion-app < companion/db/schema.sql`
- Scripted method: a `companion/scripts/migrate.ts` file that reads and executes `schema.sql` via the libSQL Node client (add `"migrate": "tsx --env-file=.dev.vars scripts/migrate.ts"` to package.json)
- Verify: `.tables` in Turso shell shows all 24 tables

**[DEV DECISION]:** CLI pipe vs. migration script. A migration script is recommended — enables CI/CD re-execution and version consistency. If choosing the script path, also gate it with a `-- force` flag to prevent accidental re-execution against a populated database.

**Acceptance Criteria:**
- `companion/db/schema.sql` file exists and is the source of truth for all table definitions
- All 24 tables visible in Turso shell after execution
- No FK violation errors during execution (dependency order is correct)

---

## Task 4 — Turso client singleton

**Steps:**

4a. Create `companion/src/lib/db.ts` with these requirements:
- Import from `@libsql/client/web` (NOT `/node` — this variant uses the Fetch API, the only HTTP client available in CF Workers)
- Export a `getDb(env: App.Platform['env'])` function that creates and returns a libSQL `Client` instance using `env.TURSO_DATABASE_URL` and `env.TURSO_AUTH_TOKEN`
- Do NOT create a module-level singleton — CF Workers may share module state across isolation contexts; per-request client creation is safe and lightweight for HTTP clients
- After creating the client, issue `PRAGMA foreign_keys = ON` as the first statement (Turso does not enable FK enforcement by default)

4b. Update `companion/src/app.d.ts` — add `env` to `App.Platform`:

Minimum type shape for `App.Platform['env']`:

| Key | Type |
|---|---|
| `TURSO_DATABASE_URL` | `string` |
| `TURSO_AUTH_TOKEN` | `string` |
| `CAMPAIGN_SECRET` | `string` |
| `AUTH_SECRET` | `string` |
| `DISCORD_CLIENT_ID` | `string` |
| `DISCORD_CLIENT_SECRET` | `string` |

4c. Create a minimal `companion/src/routes/+page.server.ts` that calls `getDb(platform?.env)` and performs `SELECT 1` to confirm the connection resolves. Remove this file after verification (or replace with real content in Phase 3).

**[DEV DECISION]:** In CF Pages, `platform.env` is available in `+server.ts` routes and `hooks.server.ts` but NOT in `+page.server.ts` unless using SvelteKit's `event.platform`. Verify the correct access pattern for the chosen SvelteKit version at implementation time.

**Acceptance Criteria:**
- `companion/src/lib/db.ts` exports `getDb(env)` using `@libsql/client/web`
- `App.Platform['env']` is correctly typed in `app.d.ts`
- `PRAGMA foreign_keys = ON` issued on each created client
- A test `SELECT 1` successfully rounds-trips to Turso in `npm run dev`

---

## Task 5 — Seed utility (CLI tool)

**Scope:** `companion/scripts/seed.ts` — a standalone TypeScript script that reads all Excel workbooks from `plans/` and populates all 11 `ref_*` tables via idempotent upsert.

**Steps:**

5a. `xlsx` is already installed (Task 1c). No further installs needed.

5b. Create `companion/scripts/seed.ts` with the following structural modules:

---

**Module: Configuration**

- `WORKBOOKS_DIR`: absolute path to `elements/` directory at workspace root (resolve relative to `__dirname`)
- `WORKBOOK_FILES`: named map of logical key → filename:

| Key | Filename |
|---|---|
| `spells` | `Spells.xlsx` |
| `equipment` | `Equipment.xlsx` |
| `skills` | `Skills.xlsx` |
| `adeptPowersMutations` | `Adept Powers and Mutations.xlsx` |
| `totemsSpirits` | `Totems and Spirits.xlsx` |

---

**Module: WorkbookParsers** — one function per source/sheet combination:

| Function | Workbook | Sheet | Returns | Notes |
|---|---|---|---|---|
| `parseSpells(wb)` | Spells.xlsx | All 9 category sheets | `SpellRow[]` | Sheet name used as `category` value on each row |
| `parseWeapons(wb)` | Equipment.xlsx | Weapons sheet | `WeaponRow[]` | |
| `parseArmor(wb)` | Equipment.xlsx | Armor sheet | `ArmorRow[]` | |
| `parseEquipment(wb)` | Equipment.xlsx | Equipment sheet | `EquipmentRow[]` | |
| `parseSkills(wb)` | Skills.xlsx | First (or named) sheet | `SkillRow[]` | |
| `parseAdeptPowers(wb)` | Adept Powers and Mutations.xlsx | Powers sheet | `AdeptPowerRow[]` | |
| `parseMutations(wb)` | Adept Powers and Mutations.xlsx | Mutations sheet | `MutationRow[]` | |
| `parseTotems(wb)` | Totems and Spirits.xlsx | Animal/Nature totem sheet(s) | `TotemRow[]` | May be 1 or 2 sheets; `type` column derived from sheet name |
| `parseSpirits(wb)` | Totems and Spirits.xlsx | Spirits sheet | `SpiritRow[]` | |
| `parseSpiritPowers(wb)` | Totems and Spirits.xlsx | Spirit Powers sheet | `SpiritPowerRow[]` | |
| `parseElementalServices(wb)` | Totems and Spirits.xlsx | Elemental Services sheet | `ElementalServiceRow[]` | |

Each parser must:
- Skip header rows (row 1 or detected by checking for expected column headers in the first row)
- Skip rows where the `Name` column is blank or undefined
- Trim whitespace from all string values
- Map null/undefined cells to `null` (not crash)
- Return empty array `[]` if sheet is empty or not found (log a warning)

**[DEV DECISION]:** Verify actual sheet names in each workbook with `workbook.SheetNames` before implementing. Excel sheet names may not match the logical names in this plan. Build a validation step at the top of each parser that throws an informative error if the expected sheet is not found.

---

**Module: Seeders** — one function per ref table:

| Function | Table | Upsert conflict target |
|---|---|---|
| `seedSpells(db, rows)` | `ref_spells` | `name` |
| `seedWeapons(db, rows)` | `ref_weapons` | `name` |
| `seedArmor(db, rows)` | `ref_armor` | `name` |
| `seedEquipment(db, rows)` | `ref_equipment` | `name` |
| `seedSkills(db, rows)` | `ref_skills` | `name` |
| `seedAdeptPowers(db, rows)` | `ref_adept_powers` | `name` |
| `seedMutations(db, rows)` | `ref_mutations` | `name` |
| `seedTotems(db, rows)` | `ref_totems` | `name` |
| `seedSpirits(db, rows)` | `ref_spirits` | `name` |
| `seedSpiritPowers(db, rows)` | `ref_spirit_powers` | `name` |
| `seedElementalServices(db, rows)` | `ref_elemental_services` | `name` |

Each seeder:
- Uses `INSERT INTO {table} (...) VALUES (?) ON CONFLICT(name) DO UPDATE SET col1=excluded.col1, ..., updated_at=datetime('now')`
- Issues inserts in batches of 50 rows (safe default for Turso HTTP API)
- Returns `SeedStats { table: string, upserted: number, errors: number }`

Return type is `upserted` (not insert/update split) — Turso HTTP does not return per-row change metadata that cleanly distinguishes new inserts from updates. Log this as a known limitation in seed output.

**[DEV DECISION]:** If distinguishing "inserted vs updated" counts is important for operator feedback, an alternative is to `SELECT COUNT(*) FROM {table}` before and after the batch and diff the totals. This trades two round-trips for precise counts — worth it only if the operator experience requires it.

---

**Module: Orchestrator** (main entry point):

Execution order:
1. Load env from `.dev.vars` using `tsx --env-file` flag (no `dotenv` import needed)
2. Create Turso client using `@libsql/client/node` (NOT `/web` — seed script runs in Node.js, not CF Workers)
3. Load all 5 workbooks: `xlsx.readFile(path.join(WORKBOOKS_DIR, filename))`
4. Call all 11 parsers; log row counts per parser
5. Call all 11 seeder functions in sequence
6. Print stats table to stdout in this format:

```
Seeding companion_app reference tables...
  ref_spells              upserted=62   errors=0
  ref_weapons             upserted=18   errors=0
  ref_armor               upserted=15   errors=0
  ref_equipment           upserted=107  errors=0
  ref_skills              upserted=41   errors=0
  ref_adept_powers        upserted=22   errors=0
  ref_mutations           upserted=21   errors=0
  ref_totems              upserted=43   errors=0
  ref_spirits             upserted=19   errors=0
  ref_spirit_powers       upserted=18   errors=0
  ref_elemental_services  upserted=4    errors=0
Done. 370 total records processed.
```

7. Exit process with code 0 on success, code 1 if any table had errors > 0

---

5c. Add scripts to `companion/package.json`:

| Script key | Command |
|---|---|
| `"seed"` | `tsx --env-file=.dev.vars scripts/seed.ts` |
| `"migrate"` | `tsx --env-file=.dev.vars scripts/migrate.ts` (if Task 3.6 uses script path) |

**Acceptance Criteria:**
- `npm run seed` executes from `companion/` without errors
- All 11 ref tables populated with non-zero row counts
- `npm run seed` run a second time produces no duplicate rows (idempotent upsert confirmed)
- Exit code 0 on success, 1 on any seeder error

---

## Task 6 — Verification checkpoint

**Steps:**

6a. From `companion/`, run `npm run dev`. Confirm SvelteKit dev server starts, no import or type errors, reaches localhost.

6b. From `companion/`, run `npm run seed`. Confirm non-zero upserted counts for all 11 tables.

6c. Open Turso CLI: `turso db shell companion-app`. Run:
- `.tables` — all 24 tables visible
- `SELECT COUNT(*) FROM ref_spells;` — expect 60-80
- `SELECT COUNT(*) FROM ref_totems;` — expect 43
- `SELECT COUNT(*) FROM ref_spirits;` — expect 19
- `SELECT COUNT(*) FROM ref_spirit_powers;` — expect 18
- `SELECT COUNT(*) FROM ref_elemental_services;` — expect 4

6d. Run `npm run seed` a second time. Confirm no row count increase (idempotency verified).

6e. Spot-check sample rows: select 1 row from at least 3 ref tables and visually verify column values against source Excel.

**Acceptance Criteria:**
- `npm run dev` starts without errors
- All 24 tables visible in Turso shell
- All 11 ref tables populated; row counts within expected ranges:

| Table | Expected rows |
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

- Second seed run: no new rows inserted (idempotent)

---

## Ordering and Dependencies

| Order | Task | Hard depends on | Parallelizable with |
|---|---|---|---|
| 1 | Task 1 — Scaffold | none | Task 2 (if Turso CLI already installed) |
| 2 | Task 2 — Turso DB | Task 1 (for .dev.vars location) | — |
| 3 | Task 3 — Write schema.sql | Task 1 (project/directory structure) | Task 2 execution; Task 3 writing can precede DB creation |
| 4 | Task 3 — Execute DDL | Tasks 2 + 3 writing | — |
| 5 | Task 4 — Client singleton | Tasks 1, 2, 3 done | Task 5 writing (not execution) |
| 6 | Task 5 — Seed utility | Task 3 executed (tables must exist) | Task 4 writing |
| 7 | Task 6 — Verification | Tasks 1–5 all complete | — |

## Companion App Impact (carry forward)

- **companion_app Phase 2 (Sync Endpoint):** The `characters` column list finalized in Task 3.2a is the authoritative column set for the sync upsert in Phase 2. Developer should cross-reference when writing the sync handler.
- **companion_app Phase 4 (Game Library):** ref_* table structures defined here drive the library UI. Seeder column names must match exactly or Phase 4 queries will fail.
- **[Flagged from Phase 0]:** 20 Questions removal from Roll20 means companion app Phase 3 Character Viewer needs a data migration decision: one-time manual re-entry of bio data, OR a one-time Roll20 attribute extract. This is a Phase 3 concern, not Phase 1.

---


---

# Layer 2 — Phase 2: Sync Endpoint + Roll20 Wiring

**Goal:** Click "Sync to DB" in Roll20 and data lands in Turso.

---

## Task 1 — `/api/sync` route: validation pipeline

**File:** `companion/src/routes/api/sync/+server.ts`

This file handles HTTP-layer concerns only: request parsing, validation, secret verification, and response formatting. Business logic lives in Task 2.

**Steps:**

1a. Create directory `companion/src/routes/api/sync/` and file `+server.ts`. Export a single `POST` async function with signature `POST({ request, platform }: RequestEvent): Promise<Response>`.

1b. **Body size guard:** Check `request.headers.get('content-length')`. If present and exceeds 1,048,576 (1 MB), return 413 `{ ok: false, error: 'Payload too large' }`. This prevents pathological payloads (e.g., thousands of repeating rows) from consuming Turso batch resources. CF Workers has a platform-level 100 MB limit, but our 1 MB ceiling is the application-level defense.

1c. **Content-Type guard:** `request.headers.get('content-type')`. If value does not include `application/json`, return `Response(JSON.stringify({ ok: false, error: 'Unsupported Media Type' }), { status: 415 })`.

1d. **Body parse:** `await request.json()` inside a try/catch. On parse failure (SyntaxError), return 400 `{ ok: false, error: 'Invalid JSON' }`.

1e. **Required-field validation** — check the following conditions in order and return 400 `{ ok: false, error: '{message}' }` on first failure:

| Condition | Error message |
|---|---|
| `body.campaign_db_id` missing or not a non-empty string | `'campaign_db_id required'` |
| `body.char_db_id` key not present (undefined — null is valid for first sync) | `'char_db_id required'` |
| `body.sync_version_from` not a non-negative safe integer | `'sync_version_from must be a non-negative integer'` |
| `body.scalars` missing or not a plain object | `'scalars required'` |
| `body.repeating` missing or not a plain object | `'repeating required'` |
| Any of the 10 repeating keys missing from `body.repeating`: `skills`, `mutations`, `adept_powers`, `spells`, `foci`, `weapons`, `equipment`, `contacts`, `karma`, `milestones` | `'repeating.{first missing key} required'` |

Each value in `body.repeating.{key}` must be an array; if not an array, return 400 `'repeating.{key} must be an array'`.

1f. **Secret header presence check:** `request.headers.get('X-Campaign-Secret')`. If absent or empty string, return 401 `{ ok: false, error: 'Unauthorized' }`. Use the same 401 body for all unauthorized states — never distinguish "missing header" from "wrong secret" in the response (prevents information leakage).

1g. **Campaign lookup:** Call `getDb(platform?.env)` and execute `SELECT campaign_secret_hash FROM campaigns WHERE id = ?` binding `body.campaign_db_id`. If no row returned, return 401 (same body as 1e — do not return 404; returning 404 would disclose whether the campaign ID is valid, enabling enumeration).

1h. **Secret verification:** Compare the incoming secret against `row.campaign_secret_hash`.

**[DEV DECISION] — Hash algorithm and timing-safe comparison:**

CF Workers has access to `crypto.subtle` (Web Crypto API). Recommended approach:

- Store `campaign_secret_hash` as: `hex( SHA-256(plaintext_secret) )` — computed by `seed-campaign.ts` (Task 5a) using Node.js `crypto.createHash('sha256')`.
- At verify time in CF Workers: compute `hex( await crypto.subtle.digest('SHA-256', new TextEncoder().encode(incoming_secret)) )` and compare.
- Timing-safe comparison: **do NOT use `===` string comparison** (short-circuits, creating a timing oracle). Instead, implement a constant-time XOR loop over the two hex strings encoded as `Uint8Array`. Both strings are always the same length (64 hex chars), so the loop runs to completion regardless of where they differ.

Alternative (more robust): use HMAC-SHA256. Store `HMAC-SHA256(secret, campaign_id)` and verify via `crypto.subtle.verify('HMAC', key, sig, data)`, which is inherently timing-safe. The extra complexity is only warranted if the threat model requires it.

If mismatch, return 401 (same body as 1e).

1i. On successful validation: call `syncWrite(db, body, body.campaign_db_id)` (imported from Task 2). Wrap in try/catch:
- On success: return `Response(JSON.stringify({ ok: true, char_db_id: result.char_db_id, sync_version: result.sync_version }), { status: 200, headers: { 'Content-Type': 'application/json' } })`.
- On caught error: `console.error('[sync] error:', err)` then return 500 `{ ok: false, error: 'Internal server error' }`. Never include error stack or DB details in the response body.

**Response field naming contract:** The response key is `sync_version` (not `new_sync_version`). The Roll20 sheet worker reads `response.sync_version` in its `.then()` handler (confirmed in current `sheet.html` code). This key name must match exactly.

**Acceptance Criteria:**
- Body >1 MB → 413
- Wrong Content-Type → 415
- Malformed JSON → 400
- Missing required field → 400 with field-specific message
- Missing/wrong `X-Campaign-Secret` → 401 (same body regardless of reason)
- Unknown `campaign_db_id` → 401 (not 404 — no enumeration)
- Valid request proceeds to sync logic and returns 200 `{ ok: true, char_db_id, sync_version }`
- DB errors return 500 with opaque error message; no DB internals in response body

---

## Task 2 — Sync write logic: `src/lib/sync-write.ts`

**File:** `companion/src/lib/sync-write.ts`

Isolated from the route handler to enable independent testing. Contains all Turso write logic.

**Steps:**

2a. Define exported types:
- `SyncPayload` — shape of the validated body from Task 1
- `SyncResult` — `{ char_db_id: string; sync_version: number }`

Export function signature: `syncWrite(db: Client, body: SyncPayload, campaignId: string): Promise<SyncResult>`

2b. **Security boundary — `ALLOWED_SCALAR_COLUMNS`:** Declare a module-level `const ALLOWED_SCALAR_COLUMNS: Set<string>` containing only the column names that exist in the `characters` table (sourced from Phase 1 Task 3.2 schema — all scalar columns except `id`, `player_id`, `campaign_id`, `roll20_character_id`, `sync_version`, `synced_at`, `created_at`, `updated_at`). These are the columns that correspond 1:1 to Roll20 `scalarFields` minus routing metadata.

**Critical:** When building SQL statements, column names come ONLY from `ALLOWED_SCALAR_COLUMNS`, never from raw `body.scalars` keys. Any payload key not in the set is silently ignored. This prevents SQL injection through crafted key names in the sync payload.

Similarly, declare `ALLOWED_{SECTION}_COLUMNS` sets for each of the 10 repeating sections (one set per rep table, sourced from Phase 1 Task 3.3 column definitions), excluding backbone columns (`id`, `character_id`, `roll20_row_id`).

2c. **First-sync vs. subsequent-sync branching:**

- If `body.char_db_id === null` → **first-sync path**: `const charId = crypto.randomUUID()` (CF Workers runtime has `crypto.randomUUID()` natively — no library needed).
- If `body.char_db_id` is a non-null string → **subsequent-sync path**: query `SELECT id, sync_version FROM characters WHERE id = ? AND campaign_id = ?` binding `body.char_db_id` and `campaignId`.
  - If no row: throw an error that the route maps to 404 `{ ok: false, error: 'Character not found' }`.
  - If row found: read `existing_sync_version`.

2d. **Stale sync detection (recommended — [DEV DECISION] Option B):**

On subsequent sync, compare `existing_sync_version` with `body.sync_version_from`:
- If mismatch: throw an error that the route maps to 409 `{ ok: false, error: 'Sync conflict: version mismatch. Reload character and retry.' }`. This prevents an older Roll20 session from overwriting a newer sync.
- If match: proceed. Use `existing_sync_version + 1` as the new `sync_version` value for the UPDATE.

On first sync: `newSyncVersion = 1`.

2e. **Build the Turso batch:**

Construct an array of `{ sql: string, args: InValue[] }` objects in this order:

| Index | Statement | Notes |
|---|---|---|
| 0 | `PRAGMA foreign_keys = ON` | No args |
| 1 | Characters INSERT or UPDATE (see 2f) | Scalar values as positional bindings |
| 2–11 | 10× `DELETE FROM rep_{section} WHERE character_id = ?` | Clears existing repeating rows; explicit DELETEs because we UPDATE (not replace) the parent `characters` row, so ON DELETE CASCADE does not trigger |
| 12+ | INSERT rows for each rep section (see 2g) | One INSERT statement per payload row |

Send the complete array via `await db.batch(statements, 'write')`. This executes all statements in an implicit transaction — all succeed or all roll back.

2f. **Characters statement:**

*First sync:*
`INSERT INTO characters (id, campaign_id, player_id, roll20_character_id, sync_version, synced_at, created_at, updated_at, {allowed_scalar_cols}) VALUES (?, ?, NULL, NULL, 1, datetime('now'), datetime('now'), datetime('now'), {scalar_values_bindings})`

Build `{allowed_scalar_cols}` by iterating `ALLOWED_SCALAR_COLUMNS` in stable order; for each key, read `body.scalars[key] ?? null` as the bound value. All scalar values are strings from Roll20; SQLite coerces to column type at storage.

*Subsequent sync:*
`UPDATE characters SET sync_version = ?, synced_at = datetime('now'), updated_at = datetime('now'), {scalar_col} = ?, ... WHERE id = ? AND campaign_id = ?`

Same column-building approach. Append `newSyncVersion`, then all scalar values, then `charId`, then `campaignId` as positional bindings.

2g. **Repeating section INSERTs:**

For each of the 10 keys in `body.repeating`:
- If the array is empty: no INSERT statements added (zero-row sections are valid).
- For each row object in the array:
  - `roll20_row_id` is read from `row.roll20_row_id` (see Phase 0 ↔ Phase 2 interface contract below).
  - Generate a new UUID: `crypto.randomUUID()` for the `id` column.
  - Build allowed column list from the section's `ALLOWED_{SECTION}_COLUMNS` set.
  - Construct: `INSERT INTO rep_{section} (id, character_id, roll20_row_id, {allowed_cols}) VALUES (?, ?, ?, {value_bindings})`

2h. **Return:** After successful batch, return `{ char_db_id: charId, sync_version: newSyncVersion }`.

2i. **Error propagation:** Wrap the batch call in try/catch. On DB error, `console.error` the raw error server-side, then rethrow with a tag so the route handler can return 500. DB error details must not reach the response body.

**[DEV DECISION] — Turso batch size limits:** Turso's HTTP API has documented limits on total batch size (statements and payload). For a typical character with ~30 total repeating rows across 10 sections, the batch will have roughly 12 + 30 = 42 statements — well within limits. If a pathological character exceeds limits, the batch may need to be split into one transaction per rep section. Monitor but do not pre-optimize.

**Acceptance Criteria:**
- `char_db_id: null` creates a new `characters` row and returns the generated UUID
- Same UUID on second sync updates the existing row, `sync_version` increments to 2
- All 10 DELETE statements execute before any INSERT
- Rep table rows after sync match payload row count for each section exactly (not additive)
- Payload keys not in `ALLOWED_SCALAR_COLUMNS` do not appear in any SQL column position
- DB transaction failure rolls back all statements (no partial writes)

---

## Task 3 — Roll20 sheet worker: Phase 2 wiring

Modifications to the Sheet Worker `<script type="text/worker">` block in `sheet.html` only. No HTML or CSS changes.

**Phase 0 pre-check (do first):**

Verify that Phase 0 Task 5 is complete before starting these steps:
- `var remaining = 11` counter/latch pattern is implemented
- All 10 `getSectionIDs()` + inner `getAttrs()` calls are present
- `payload.repeating` is populated with all 10 keys
- Each row object in every repeating array includes a `roll20_row_id` property (see Interface Contract section below)
- `bio_q01`–`bio_q20` are removed from `scalarFields`
- `money_gold`, `money_silver`, `money_copper` are present in `scalarFields`

If Phase 0 Task 5 is not yet complete, complete it before continuing.

**Steps:**

3a. At the top of the sheet worker block, declare two constants (add after `SYNC_PROXY_URL` if not already present):

```
var SYNC_PROXY_URL = '';           // Fill after CF Pages deploy (Task 4c)
var CAMPAIGN_SECRET = '';          // Fill with plaintext campaign secret
```

`CAMPAIGN_SECRET` is the plaintext value of the campaign secret. The `seed-campaign.ts` script (Task 4a) hashes it for storage in DB; this is the original value.

**[DEV DECISION] — CAMPAIGN_SECRET in sheet.html source:** This secret is visible to anyone with Roll20 sheet edit access. Security posture for V1: Roll20 edit access is restricted to GM only; the secret prevents unauthorized third parties from writing to the sync endpoint. Acceptable for a closed 6-player group. If the secret must be rotated, update both the constant in `sheet.html` and the hash stored in `campaigns.campaign_secret_hash`.

3b. In the `fetch(SYNC_PROXY_URL, { ... })` call, add `'X-Campaign-Secret': CAMPAIGN_SECRET` to the `headers` object alongside the existing `Content-Type` header.

3c. Verify the response handler's key names match the API response contract from Task 1h:
- `response.char_db_id` — set `char_db_id` attribute on first sync (existing logic: `attrs.char_db_id || response.char_db_id` is correct)
- `response.sync_version` — the existing code uses `.toString()` to set `char_sync_version` (correct — this key name matches the server response)
- Do NOT change these lines if they already match

3d. Confirm the early-exit guard for empty `SYNC_PROXY_URL` is still present and unchanged:
```javascript
if (!SYNC_PROXY_URL) {
  setAttrs({ sync_status: 'Sync skipped \u2014 no proxy URL configured' });
  return;
}
```
This guard remains during development. `SYNC_PROXY_URL` stays as empty string until Step 4d.

**Acceptance Criteria:**
- `CAMPAIGN_SECRET` constant declared in sheet worker block
- `X-Campaign-Secret` header present in fetch call
- `SYNC_PROXY_URL` remains empty until deployment URL is known (Task 4d)
- Response handler key names match server response contract (`sync_version`, `char_db_id`)

---

## Task 4 — Deployment and end-to-end verification

**Steps:**

4a. **Seed the `campaigns` row:**

Create `companion/scripts/seed-campaign.ts`:
- Accept two CLI arguments: `--name` (campaign display name) and `--secret` (plaintext secret)
- Compute `SHA-256(plaintext_secret)` as lowercase hex using Node.js: `crypto.createHash('sha256').update(secret).digest('hex')`
- Generate a UUID v4 for the campaign `id` using Node.js `crypto.randomUUID()`
- Execute: `INSERT INTO campaigns (id, name, campaign_secret_hash, created_at) VALUES (?, ?, ?, datetime('now'))` — using `@libsql/client/node` (not `/web`)
- Print to stdout: `Campaign seeded. ID: {uuid}` — this UUID becomes `attr_campaign_db_id` in Roll20 and the basis for all sync payloads.
- Add to `companion/package.json` scripts: `"seed-campaign": "tsx --env-file=.dev.vars scripts/seed-campaign.ts"`

Set `attr_campaign_db_id` in Roll20 (the hidden field at the bottom of `sheet.html`) to the printed UUID. This can be done by opening the Raw Attributes in Roll20 campaign settings or by using Roll20's API console.

4b. **Build the companion app:** `cd companion && npm run build`. Confirm `npm run build` exits 0 with no TypeScript errors.

4c. **Deploy to CF Pages:**

- Method A (CLI): `wrangler pages deploy .svelte-kit/cloudflare --project-name={project-name}`
- Method B (Git): Push to the tracked branch; CF Pages CI builds and deploys automatically

In CF Pages dashboard (or via Wrangler secrets command), set the following encrypted environment variables:
- `TURSO_DATABASE_URL` — from Phase 1 Task 2
- `TURSO_AUTH_TOKEN` — from Phase 1 Task 2
- `CAMPAIGN_SECRET` — plaintext value used in `seed-campaign.ts` (used for server-side hash computation at verify time)

Note the deployed URL: `https://{deployment-name}.pages.dev`

4d. **Update `SYNC_PROXY_URL` in `sheet.html`:**

Set `var SYNC_PROXY_URL = 'https://{deployment-name}.pages.dev/api/sync'` in the sheet worker block. Upload the updated sheet to Roll20 via the Custom Sheet Editor.

4e. **Local cURL tests** (run against `wrangler pages dev .svelte-kit/cloudflare` or `npm run dev`):

Construct a valid minimal test payload:
```json
{
  "campaign_db_id": "{uuid-from-4a}",
  "char_db_id": null,
  "sync_version_from": 0,
  "scalars": { "char_name": "Caellum Test", "body": "5" },
  "repeating": {
    "skills": [], "mutations": [], "adept_powers": [], "spells": [],
    "foci": [], "weapons": [], "equipment": [], "contacts": [],
    "karma": [], "milestones": []
  }
}
```

Execute these test cases and confirm expected outcomes:

| Test | Variation | Expected status | Expected body |
|---|---|---|---|
| First sync, valid | `char_db_id: null`, correct secret | 200 | `{ ok: true, char_db_id: "{new-uuid}", sync_version: 1 }` |
| Second sync, valid | `char_db_id: "{uuid-from-first}"`, `sync_version_from: 1` | 200 | `{ ok: true, char_db_id: "{same-uuid}", sync_version: 2 }` |
| Stale version | `char_db_id` valid, `sync_version_from: 0` (stale) | 409 | `{ ok: false, error: "Sync conflict..." }` |
| Wrong secret | Correct campaign ID, wrong `X-Campaign-Secret` | 401 | `{ ok: false, error: "Unauthorized" }` |
| Missing header | No `X-Campaign-Secret` header | 401 | `{ ok: false, error: "Unauthorized" }` |
| Unknown campaign | Valid format but non-existent `campaign_db_id` | 401 | `{ ok: false, error: "Unauthorized" }` (not 404) |
| Missing `char_db_id` key | Field entirely absent (not null) | 400 | `{ ok: false, error: "char_db_id required" }` |
| Missing repeating key | `repeating.karma` absent | 400 | `{ ok: false, error: "repeating.karma required" }` |
| Oversized payload | Content-Length >1 MB | 413 | `{ ok: false, error: "Payload too large" }` |

After first-sync test: `SELECT char_name, sync_version FROM characters LIMIT 1;` in Turso shell — confirms row exists.
After second-sync test: `SELECT sync_version FROM characters WHERE id = '{uuid}';` — expect `2`.

4f. **Live Roll20 test:**

- Open a Roll20 character. Verify `attr_campaign_db_id` is set (the UUID from 4a). Clear `attr_char_db_id` (so this is treated as first sync).
- Click "Sync to DB".
- Verify Roll20 status field updates to `Synced ✓ — {timestamp}`.
- Verify `attr_char_db_id` is populated with a UUID.
- In Turso shell: `SELECT char_name, sync_version, synced_at FROM characters ORDER BY created_at DESC LIMIT 1;` — confirm full row.
- For a character with non-empty repeating sections (e.g., has skills): `SELECT COUNT(*) FROM rep_skills WHERE character_id = '{uuid}';` — confirm non-zero.
- Click "Sync to DB" a second time. Confirm `sync_version` increments to 2 in Turso.

**Acceptance Criteria:**
- `campaigns` row seeded before testing begins
- All 8 cURL test cases pass with correct status codes and response bodies
- After first sync: `characters` row in Turso with correct `char_name` and `sync_version = 1`
- After second sync: `sync_version = 2` in Turso
- rep_* tables contain rows matching payload section arrays (empty arrays → zero rows for that table)
- Live Roll20 sync shows success status; `attr_char_db_id` populated after first sync; `attr_char_sync_version` updates on each sync

---

## Phase 0 ↔ Phase 2 Interface Contract (repeating row format)

This is a binding contract between the Phase 0 sync handler implementation and Phase 2 server logic.

Each element in `payload.repeating.{section}` **must** include `roll20_row_id` (the Roll20 section row hash key returned by `getSectionIDs()`), alongside the section's field values.

Example element in `payload.repeating.skills`:
```
{
  "roll20_row_id": "-MFj2xyz_abc123",
  "skill_name": "Armed Combat",
  "skill_linked_attr": "Quickness",
  "skill_general": "1",
  "skill_spec": "0",
  "skill_base": "4",
  "skill_foci": "1",
  "skill_misc": "0",
  "skill_total": "5"
}
```

If Phase 0 Task 5 implementation did not include `roll20_row_id` in each row object, it **must be amended before Phase 2 can be completed.** This is a **blocking dependency** — without `roll20_row_id`, the server cannot populate the `rep_*` table backbone column.

---

## Ordering and Dependencies

| Order | Task | Hard depends on | Parallelize with |
|---|---|---|---|
| 1 | Task 1 — `/api/sync` route (writing) | Phase 1 schema finalized | Task 2 writing |
| 1 | Task 2 — `sync-write.ts` (writing) | Phase 1 Task 4 (`getDb` factory) | Task 1 writing |
| 2 | Task 3 — Roll20 wiring (partial) | Phase 0 Task 5 complete; `CAMPAIGN_SECRET` known | Tasks 1+2 writing |
| 3 | Task 4a — Seed campaigns row | Phase 1 Task 2 (Turso DB), Phase 1 Task 3 (tables exist) | None |
| 4 | Task 4b — npm run build | Tasks 1+2+3 complete | None |
| 5 | Task 4e — Local cURL tests | Tasks 1+2+3+4a complete; local server running | None |
| 6 | Task 4c — CF Pages deploy | Task 4b succeeds | None |
| 7 | Task 4d — Update Roll20 SYNC_PROXY_URL | Task 4c (URL is known) | None |
| 8 | Task 4f — Live Roll20 test | Tasks 3+4c+4d complete | None |

**Note:** Task 3 (`CAMPAIGN_SECRET` + header) can be added before deployment; only `SYNC_PROXY_URL` filling requires the CF Pages URL from Task 4c.

---

## Companion App Impact (carry forward)

- **Phase 3 (Auth + Character Viewer):** Must populate `characters.player_id` for all rows created in Phase 2 (currently NULL). A matching step on first Discord login — query characters by Roll20 session or by GM confirmation — is required before per-player character visibility works correctly.
- **Phase 3 (Auth + Character Viewer — CORS):** Phase 2's `/api/sync` is called from Roll20's sandboxed sheet worker (not a browser origin), so CORS headers are not needed yet. Phase 3 introduces browser-based requests from the companion app's own pages to its API — at that point, add appropriate `Access-Control-Allow-Origin` headers scoped to the deployment domain.
- **Phase 3 (Character Viewer):** `sync_version` and `synced_at` can surface in the character viewer as "Last synced: {time}, version #{n}" to confirm freshness.
- **Phase 4 (Game Library):** No changes from Phase 2.

---



---

# Layer 2 — Phase 3: Auth + Character Viewer

**Goal:** Players log in via Discord, see their characters, and browse full read-only character details.

---

## Task 1 — Discord OAuth setup + player upsert

**Files:** `companion/src/auth.ts`, `companion/src/hooks.server.ts`

**Steps:**

1a. Install `@auth/sveltekit` and `@auth/core` via `npm install @auth/sveltekit @auth/core` from `companion/`.

1b. Create `companion/src/auth.ts`:
- Import `SvelteKitAuth` from `@auth/sveltekit` and `Discord` from `@auth/sveltekit/providers/discord`
- Call `SvelteKitAuth({ ... })` with `providers: [Discord({ clientId, clientSecret })]` and `secret: AUTH_SECRET`
- Implement the `events.signIn` callback for player upsert (Step 1e)
- Export the resulting `{ handle, signIn, signOut }` destructured tuple

1c. Create or update `companion/src/hooks.server.ts`:
- Use SvelteKit's `sequence()` utility: `export const handle = sequence(authHandle, appHandle)`
- `authHandle` = the `handle` export from `src/auth.ts`
- `appHandle` = passthrough for now (route-level auth checks live in layout load functions)

1d. **Env vars:** Confirm `AUTH_SECRET`, `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET` are present in:
- `companion/.dev.vars` (local — fill real values before running)
- `companion/src/app.d.ts` `App.Platform['env']` interface (added in Phase 1 Task 4b — verify)
- CF Pages dashboard encrypted env vars (at deployment time)

1e. **Player upsert** in `events.signIn` callback:
- Extract from the Discord OAuth response: `id` from `account.providerAccountId` (Discord snowflake — this IS the `players.id` PK per Phase 1 schema), `username` from `profile.username`, `display_name` from `profile.global_name` (nullable), `avatar` from `profile.avatar` (nullable)
- Execute against Turso (`getDb(event.platform?.env)`):
  `INSERT INTO players (id, username, display_name, avatar, is_gm, created_at, updated_at) VALUES (?, ?, ?, ?, 0, datetime('now'), datetime('now')) ON CONFLICT(id) DO UPDATE SET username=excluded.username, display_name=excluded.display_name, avatar=excluded.avatar, updated_at=datetime('now')`
  — First `?` binds `account.providerAccountId` (Discord snowflake string). The PK IS the Discord user ID — no separate `discord_id` column exists.
- `is_gm` defaults to `0` on insert; never modified by sign-in logic (set directly in DB by GM)

1f. **Discord redirect URI registration** — in the Discord Developer Portal, add OAuth2 redirect URIs:
- Local: `http://localhost:5173/auth/callback/discord`
- Production: `https://{deployment-name}.pages.dev/auth/callback/discord`

**[DEV DECISION]:** `@auth/sveltekit` env access pattern in CF Pages — `platform.env` bindings are not in SvelteKit's standard env module. Verify the correct method for passing `DISCORD_CLIENT_ID` / `DISCORD_CLIENT_SECRET` to the provider at the installed version (may require `SvelteKitAuth` to be called inside a lazy wrapper receiving `event`). Check the `@auth/sveltekit` CF adapter docs at implementation time.

**[DEV DECISION]:** `events.signIn` vs `callbacks.jwt` for profile extraction. If `events.signIn` does not expose full Discord profile fields (`username`, `avatar`), use `callbacks.jwt` with the `profile` parameter — it receives the raw Discord profile on first sign-in.

**Acceptance Criteria:**
- `GET /auth/signin` renders Discord OAuth button
- Completing OAuth flow sets an authenticated session cookie
- First login creates a `players` row; subsequent logins update `username`, `display_name`, and `avatar`
- `is_gm` is `0` for new players and is never modified by the sign-in callback
- `AUTH_SECRET`, `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET` documented in `.dev.vars.example` or README

---

## Task 2 — GM character assignment page (`/admin/assign`)

**Files:** `companion/src/routes/admin/assign/+page.server.ts`, `companion/src/routes/admin/assign/+page.svelte`

**Steps:**

2a. **`+page.server.ts` load function:**
- Read `player` from `await parent()` (provided by root layout, Task 3)
- If `player.is_gm !== 1`: throw `error(403, 'Forbidden')`
- Query unclaimed characters: `SELECT id, char_name FROM characters WHERE player_id IS NULL ORDER BY char_name ASC`
- Query all players: `SELECT id, username FROM players ORDER BY username ASC`
- Return `{ unclaimedCharacters, players }`

2b. **`+page.svelte` view:**
- For each unclaimed character: render character name + `<select>` dropdown (player options) + "Assign" submit button
- Each character row is its own `<form method="POST" action="?/assign">` — one form per row, simplest to implement

2c. **`+page.server.ts` form action (`actions.assign`):**
- Extract `characterId` and `playerId` from `formData`
- Validate both are non-empty strings; return 400 otherwise
- Re-verify GM status server-side: `SELECT is_gm FROM players WHERE id = ?` — do not trust parent data alone
- Execute: `UPDATE characters SET player_id = ?, updated_at = datetime('now') WHERE id = ? AND player_id IS NULL`
- The `AND player_id IS NULL` guard prevents double-assignment without throwing — idempotent by design
- On success: `throw redirect(303, '/admin/assign')` (POST-redirect-GET)

**[DEV DECISION]:** One form per character row is the MVP approach. A single bulk-save form with all `<select>` elements is a minor UX improvement — defer unless the per-row forms feel cumbersome during testing.

**Acceptance Criteria:**
- `/admin/assign` returns 403 for non-GM authenticated users
- `/admin/assign` returns 403 (or login redirect) for unauthenticated users
- Page lists only characters where `player_id IS NULL`
- Submitting a row's form sets `player_id` to the selected player's `id`
- Assigning an already-assigned character does not throw a DB error
- After assignment, character no longer appears on page reload

---

## Task 3 — Route auth guards: layout load functions

**Files:** `companion/src/routes/+layout.server.ts`, `companion/src/routes/admin/+layout.server.ts`

**Steps:**

3a. Create `companion/src/routes/+layout.server.ts`:
- Call `locals.auth()` to get the current session
- If no session: `throw redirect(302, '/auth/signin')`
- Query: `SELECT id, is_gm FROM players WHERE id = ?` binding the Discord user ID from the session (`session.user.id` or `providerAccountId` — whichever holds the Discord snowflake; verify against Task 1e). Since `players.id` IS the Discord snowflake (Phase 1 schema), this is a direct PK lookup.
- If no player row found (edge case: OAuth succeeded but upsert failed): throw `error(500, 'Player record missing')`
- Return `{ player: { id: string, is_gm: number }, session }`

3b. Create `companion/src/routes/admin/+layout.server.ts`:
- `const { player } = await parent()`
- If `player.is_gm !== 1`: throw `error(403, 'Forbidden')`
- Return `{}` — no additional data needed

3c. **Consistent session shape:** `data.player` from 3a is resolved once at the root layout level. All child `+page.server.ts` files access it via `await parent()` — no per-page DB call for player identity.

**Acceptance Criteria:**
- All routes under `/` except `/auth/*` redirect unauthenticated users to `/auth/signin`
- `/admin/*` routes return 403 for authenticated non-GM users
- `data.player.is_gm` resolves correctly for both player and GM accounts
- Root layout DB query is one `SELECT` per request — not repeated per child route

---

## Task 4 — App shell: layout component + home redirect

**Files:** `companion/src/routes/+layout.svelte`, `companion/src/routes/+page.server.ts`, `companion/src/routes/library/+page.svelte`

**Steps:**

4a. Create `companion/src/routes/+layout.svelte`:
- Top nav bar with links: "Home" (`/`), "Characters" (`/characters`), "Game Library" (`/library`)
- Display `data.session.user.name` (Discord username) in the nav
- "Sign Out" link: `href="/auth/signout"`
- `<slot />` for page content

4b. Create `companion/src/routes/+page.server.ts` (home):
- Query: `SELECT id FROM characters WHERE player_id = ? LIMIT 1` binding `data.player.id`
- If row found: `throw redirect(302, '/characters')`
- If no row: return `{}` — page component renders "No characters assigned yet" message

4c. Create `companion/src/routes/library/+page.svelte` — static stub:
- Single heading: "Game Library" + body text: "Coming in Phase 4."

**Acceptance Criteria:**
- Nav renders on all authenticated pages with correct links
- `/` redirects to `/characters` for players with at least one assigned character
- `/` shows a pending message for players with no assigned characters (not an error state)
- `/library` renders the stub without error

---

## Task 5 — Character list page (`/characters`)

**Files:** `companion/src/routes/characters/+page.server.ts`, `companion/src/routes/characters/+page.svelte`

**Steps:**

5a. **`+page.server.ts` load:**
- Read `player` from `await parent()`
- If `player.is_gm = 1`: `SELECT c.id, c.char_name, c.synced_at, ca.name AS campaign_name FROM characters c JOIN campaigns ca ON c.campaign_id = ca.id ORDER BY c.char_name ASC`
- If `player.is_gm = 0`: same query with `WHERE c.player_id = ?` binding `player.id`
- Return `{ characters: CharacterSummary[] }`

5b. **`+page.svelte` view:**
- One card per character: `char_name` (heading), `campaign_name`, "Last synced: {synced_at formatted as `YYYY-MM-DD HH:mm` UTC}"
- Each card is a link to `/characters/{id}`
- `characters.length === 0`: render "No characters assigned" — not an error

**Acceptance Criteria:**
- Player sees only characters where `player_id = player.id`
- GM sees all characters regardless of `player_id`
- Each card links to the correct detail route
- `synced_at` renders as a human-readable UTC timestamp

---

## Task 6 — Character detail page (`/characters/[id]`)

**Files:** `companion/src/routes/characters/[id]/+page.server.ts`, `companion/src/routes/characters/[id]/+page.svelte`

**Steps:**

6a. **`+page.server.ts` load:**
- Read `player` from `await parent()`; read `params.id` (character UUID)
- Query: `SELECT * FROM characters WHERE id = ?` — if no row: throw `error(404, 'Character not found')`
- **Access check:** if `player.is_gm !== 1 AND character.player_id !== player.id`: throw `error(403, 'Forbidden')`
- Query all 10 rep tables in parallel (`Promise.all`):
  `SELECT * FROM rep_{section} WHERE character_id = ?` for each of: `skills`, `mutations`, `adept_powers`, `spells`, `foci`, `weapons`, `equipment`, `contacts`, `karma`, `milestones`
- Call `computeCharacter(character, repData)` from Task 7
- Return `{ character, repData, computed }`

**[DEV DECISION]:** `Promise.all` for 10 parallel Turso HTTP requests is recommended — reduces latency from 10 serial round-trips to ~1. If Turso's connection limits cause issues, fall back to sequential with Promise chaining.

6b. **`+page.svelte` tabbed view:**

Tab state managed with a Svelte reactive `let activeTab` variable — no URL routing per tab.

| Tab label | Content rendered |
|---|---|
| Overview | Core attrs (body, dex, str, cha, int, wil, hum, essence), CM box counts from `computed`, current conditions (cm_* scalar checkboxes), computed pool summaries |
| Skills | `repData.skills` table: `skill_name`, `skill_linked_attr`, `skill_base`, `skill_foci`, `skill_misc`, `skill_total` |
| Magic | `repData.spells`, `repData.foci`, `repData.adept_powers`, `repData.mutations` — each as a labeled section |
| Gear | `repData.weapons`, `repData.equipment`; money display from `computed.formattedMoney` |
| Bio | `repData.karma` with `computed.karmaLedgerRunningTotals`; `repData.milestones`; `repData.contacts`; `char_name`, description, notes scalars |

Each empty rep section renders an empty-state message (e.g., "No spells") — never an error.

**Acceptance Criteria:**
- `/characters/{id}` returns 404 for unknown UUID
- `/characters/{id}` returns 403 if character is not owned by the requesting player (and player is not GM)
- GM can access any character's detail page
- All 5 tabs render; zero-row rep sections show empty state
- `synced_at` and `sync_version` visible on the page (e.g., in a footer or Overview tab)

---

## Task 7 — Computed fields module

**File:** `companion/src/lib/computed.ts`

**Steps:**

7a. Export a single entry point: `computeCharacter(character: CharacterRow, repData: RepData): ComputedFields`

7b. **`ComputedFields` shape:**

| Field | Derivation rule |
|---|---|
| `totalKarma` | Sum of all `karma_amount` integers in `repData.karma` |
| `conditionMonitorBoxes.mental` | `Math.ceil(character.wil / 2) + 8` |
| `conditionMonitorBoxes.stun` | `Math.ceil(character.wil / 2) + 8` — **[DEV DECISION]:** Standard SR3 derives Stun from Willpower. Verify with GM — if the campaign's 3-track system uses Body for both Stun and Physical, change back to `body`. |
| `conditionMonitorBoxes.physical` | `Math.ceil(character.body / 2) + 8` |
| `formattedMoney` | `{ gold: character.money_gold, silver: character.money_silver, copper: character.money_copper }` — raw scalars, no conversion |
| `karmaLedgerRunningTotals` | Array of `{ karma_event, karma_amount, runningTotal }` built from `repData.karma` sorted by `id ASC`; each entry accumulates a running sum |

7c. All functions are **pure** — no DB calls, no `fetch`, no side effects. Inputs are plain objects from the server load; output is a plain object.

**[DEV DECISION]:** Condition monitor formulas above follow standard SR3 rules. If the campaign uses house-ruled CM formulas, verify with the GM before implementing. The formulas are the most likely point of divergence from core rules.

**Acceptance Criteria:**
- `computeCharacter` is synchronous and pure (no async, no side effects)
- `totalKarma` correctly sums positive and negative entries
- `karmaLedgerRunningTotals` accumulates in chronological order (by `id ASC`)
- CM box counts match expected SR3 formula for known attribute values
- Module imports nothing outside the project's own type definitions

---

## Task 8 — CORS headers on API routes (carry-forward from Phase 2)

**File:** `companion/src/routes/api/sync/+server.ts`

**Steps:**

8a. Add `Access-Control-Allow-Origin: https://{deployment-domain}` to all non-error `POST` responses. Scope to the exact CF Pages deployment domain — do not use `*`.

8b. Export an `OPTIONS` handler in the same file:
- Returns `200` with headers: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods: POST, OPTIONS`, `Access-Control-Allow-Headers: Content-Type, X-Campaign-Secret`

8c. **[DEV DECISION]:** If the deployment domain is stable, hardcode it as a module constant. If env-variable-driven multi-environment deployment is desired, read it from a `PUBLIC_APP_ORIGIN` SvelteKit public env var. For a single-deployment solo-maintainer app, hardcoding the production domain is acceptable V1 practice.

**Acceptance Criteria:**
- `OPTIONS /api/sync` returns 200 with correct preflight headers
- `POST /api/sync` responses include `Access-Control-Allow-Origin` scoped to the deployment domain
- Origin is not `*` — wildcard CORS is explicitly rejected

---

## Ordering and Dependencies

| Order | Task | Hard depends on | Parallelize with |
|---|---|---|---|
| 1st | Task 1 — Discord OAuth + player upsert | Phase 2 deployed; `players` table exists | Task 8 (no auth dependency) |
| 2nd | Task 3 — Root layout auth guard | Task 1 (`locals.auth()` available) | Task 4 writing |
| 2nd | Task 4 — App shell + nav | Task 1 (session data shape known) | Task 3 writing |
| 3rd | Task 2 — Admin assign page | Tasks 1 + 3 complete | Task 5 writing |
| 3rd | Task 5 — Character list | Tasks 1 + 3 complete | Task 2 writing |
| 4th | Task 7 — Computed fields module | Task 6 data shape known | Task 6 structure writing |
| 4th | Task 6 — Character detail | Tasks 3 + 5 complete; Task 7 API defined | Task 7 writing |
| 5th | Task 6 — Wire computed into detail view | Task 7 complete | — |

Task 8 (CORS) is independent of auth and viewer work — apply at any point during Phase 3, before end-to-end browser testing.

---

## Carry-Forward Notes (Phase 3 → Phase 4)

- **`/library` stub (Task 4c):** Becomes the Phase 4 entry point; no routing changes needed.
- **`player_id` backfill:** All characters synced in Phase 2 have `player_id = NULL`. Players will see an empty list until the GM uses `/admin/assign`. Document this as expected onboarding behavior — not a bug.
- **20 Questions:** Bio question fields were removed from sync in Phase 0. Companion app does not display them. No migration required — confirmed out of scope.
- **Verification path for Phase 3 sign-off:** Discord sign-in → character list → character detail (all 5 tabs) → GM views another player's character → non-GM blocked from `/admin/assign`. All must pass before Phase 4 begins.

---



---

# Layer 2 — Phase 4: Game Library

**Goal:** Replace the `/library` stub with a browsable catalog of all 11 ref_* tables. All authenticated players can search and browse; GM can create, edit, and delete catalog entries.

---

## Task 1 — Library landing page (`/library`)

**Files:** `companion/src/routes/library/+page.server.ts`, `companion/src/routes/library/+page.svelte`

**Steps:**

1a. Replace the Phase 3 stub `+page.svelte` (which contained only "Coming in Phase 4."). Keep the file path unchanged — no routing changes needed.

1b. Create `companion/src/routes/library/+page.server.ts`:
- Read `player` from `await parent()`
- Execute 11 parallel count queries via `Promise.all`:
  `SELECT COUNT(*) AS count FROM {ref_table}` for each of: `ref_spells`, `ref_weapons`, `ref_armor`, `ref_equipment`, `ref_skills`, `ref_adept_powers`, `ref_mutations`, `ref_totems`, `ref_spirits`, `ref_spirit_powers`, `ref_elemental_services`
- Return `{ counts: Record<string, number>, isGm: player.is_gm === 1 }`

1c. `+page.svelte` view:
- Heading: "Game Library"
- 11 category cards arranged in a responsive grid
- Each card: human-readable label, entry count (e.g. "62 entries"), and a link to the section's list route

Cards, labels, and target routes:

| Card label | Route |
|---|---|
| Spells | `/library/spells` |
| Weapons | `/library/weapons` |
| Armor | `/library/armor` |
| Equipment | `/library/equipment` |
| Skills | `/library/skills` |
| Adept Powers | `/library/adept-powers` |
| Mutations | `/library/mutations` |
| Totems | `/library/totems` |
| Spirits | `/library/spirits` |
| Spirit Powers | `/library/spirit-powers` |
| Elemental Services | `/library/elemental-services` |

- GM users (`isGm === true`) see an "Add entry" link per card (links to `/library/{slug}/new`)

**Acceptance Criteria:**
- `/library` renders 11 category cards with live entry counts from the DB
- All 11 card links navigate to the correct sub-routes without 404
- "Add entry" links are visible only to GM users

---

## Task 2 — Catalog list pages (dynamic `[catalog]` route)

**Files:** `companion/src/lib/catalog-config.ts`, `companion/src/routes/library/[catalog]/+page.server.ts`, `companion/src/routes/library/[catalog]/+page.svelte`

**Steps:**

2a. Create `companion/src/lib/catalog-config.ts` — a configuration map keyed by URL slug. For each entry, define:
- `table`: SQL table name (e.g., `"ref_spells"`)
- `label`: Human-readable page heading (e.g., `"Spells"`)
- `listColumns`: Ordered array of `{ key: string, label: string }` — columns rendered in the list table
- `filterFields`: Array of column key strings that support filter `<select>` dropdowns (load distinct values at request time)
- `detailFields`: Array of `{ key: string, label: string }` shown only in the expanded detail panel (not in the list table); empty `[]` if no detail-only fields

Config entries:

| Slug | Table | listColumns | filterFields | detailFields (keys) |
|---|---|---|---|---|
| `spells` | `ref_spells` | `name`, `category`, `type`, `target`, `duration`, `drain` | `category`, `type` | `description` |
| `weapons` | `ref_weapons` | `name`, `type`, `damage`, `reach`, `conceal`, `ep`, `cost` | `type` | — |
| `armor` | `ref_armor` | `name`, `location`, `rating_p`, `rating_s`, `rating_i`, `conceal`, `ep`, `cost` | `location` | — |
| `equipment` | `ref_equipment` | `name`, `conceal`, `ep`, `cost`, `notes` | — | — |
| `skills` | `ref_skills` | `name`, `linked_attr`, `category`, `specializations` | `linked_attr`, `category` | — |
| `adept-powers` | `ref_adept_powers` | `name`, `pp_cost` | — | `description`, `game_effect` |
| `mutations` | `ref_mutations` | `name`, `bp_cost`, `essence` | — | `description`, `game_effect` |
| `totems` | `ref_totems` | `name`, `type`, `environment` | `type` | `description`, `advantages`, `disadvantages` |
| `spirits` | `ref_spirits` | `name`, `category` | `category` | `formula_b`, `formula_q`, `formula_s`, `formula_c`, `formula_i`, `formula_w`, `formula_e`, `formula_r`, `formula_initiative`, `attack`, `powers`, `weaknesses` |
| `spirit-powers` | `ref_spirit_powers` | `name`, `type`, `action`, `range`, `duration` | `type` | `description` |
| `elemental-services` | `ref_elemental_services` | `name` | — | `description` |

2b. Create `companion/src/routes/library/[catalog]/+page.server.ts`:
- Look up `CATALOG_CONFIG[params.catalog]`. If not found: `throw error(404, 'Unknown catalog section')`. This validates the slug against the trusted config map before any SQL executes.
- Execute in parallel via `Promise.all`:
  - Main query: `SELECT * FROM {config.table} ORDER BY name ASC`
  - One distinct-values query per filter field: `SELECT DISTINCT {field} FROM {config.table} WHERE {field} IS NOT NULL ORDER BY {field} ASC`
- `config.table` comes from the trusted `CATALOG_CONFIG` constant (not from user input) — safe to interpolate directly into SQL.
- Return `{ config, rows, filterOptions: Record<string, string[]>, isGm: player.is_gm === 1 }`

2c. Create `companion/src/routes/library/[catalog]/+page.svelte`:
- Heading from `config.label`; breadcrumb: "← Game Library" linking `/library`
- Search input: text field bound to reactive `let searchTerm = ''`
- One `<select>` filter per `config.filterFields` entry, each bound to a reactive variable; options populated from `filterOptions[field]`, plus an "All" option
- Reactive statement (`$:`) filters `rows` client-side:
  - `row.name.toLowerCase().includes(searchTerm.toLowerCase())`
  - Each active filter: `filterValue === 'all' || row[field] === filterValue`
- Results table with `config.listColumns` rendered in order
- Row click toggles an expanded detail panel below that row showing `config.detailFields` label+value pairs; spirit rows render the `formula_*` columns as a compact stat block
- Entry counter: "Showing N of M entries" — updates reactively
- Zero filtered results: "No entries match your filters" — not an error
- GM users see "Edit" (`href="/library/{catalog}/{row.id}/edit"`) and "Delete" (`action="?/delete"`) controls per row

**[DEV DECISION]:** Client-side filtering is used because the full dataset (~370 rows, largest table ~107 rows) is small enough to load entirely in the server request and filter in the browser. Add server-side query params only if page load becomes measurably slow.

**[DEV DECISION]:** The delete control on the list page requires a `<form method="POST" action="?/delete">` with a hidden `id` field. This means the list `+page.server.ts` must also export a `delete` form action (same logic as Task 3d below). Decide at implementation time whether to co-locate delete on the list page or require navigating to the edit page first. Co-locating is the lower-friction path. If delete is co-located on the list page: (1) the same inline "Are you sure?" confirmation toggle from Task 3e MUST be applied to each row's delete form, (2) the delete action binds `id` from `formData.get('id')` (not `params.id`, which does not exist on the list route) and must validate it as a non-empty string before use, and (3) the co-located delete action MUST re-validate GM status server-side (same as Task 3d) before executing the DELETE.

**Acceptance Criteria:**
- All 11 `/library/{slug}` routes render without error
- An unknown slug (e.g., `/library/foobar`) returns 404
- Rows display correct column data; empty tables show an empty state — not an error
- Search filters visible rows in real time (no page reload)
- Filter dropdowns contain only values present in the DB
- Search and filter can be active simultaneously
- Expanded row panel renders `detailFields` values (visible via row click)
- Edit and Delete controls appear only for GM users

---

## Task 3 — GM create and edit forms

**Files:**
- `companion/src/routes/library/[catalog]/new/+page.server.ts` + `+page.svelte`
- `companion/src/routes/library/[catalog]/[id]/edit/+page.server.ts` + `+page.svelte`

**Steps:**

3a. Extend `catalog-config.ts` with a `formFields` array per catalog entry:
- Each element: `{ key: string, label: string, type: 'text' | 'number' | 'textarea' | 'select', options?: string[] }`
- Covers all writable columns for that table (all columns except `id`, `created_at`, `updated_at`)
- `textarea` type for description/long-text fields; `select` type supplies a hardcoded `options` array (e.g., `["M", "P"]` for spell type, `["Animal", "Nature"]` for totem type, `["Elemental", "Nature"]` for spirit category, `["P", "M"]` for spirit power type)

3b. **Create form — `+page.server.ts`:**
- Load: GM check (`if (player.is_gm !== 1) throw error(403, 'Forbidden')`); catalog slug validation; return `{ config }`
- Form action `create`:
  - Re-validate GM status server-side from a fresh `players` query (do not trust layout data alone)
  - Collect fields: `formData.get(key)` for each `config.formFields[].key`
  - Validate: `name` must be non-empty string; `number` type fields must parse as finite number or be set to `null`; return `{ errors }` on validation failure (do NOT redirect — return errors for inline display)
  - Column names for the INSERT come from `config.formFields[].key` (trusted constant) — never from `formData` keys directly
  - Execute: `INSERT INTO {config.table} ({columns}) VALUES ({bindings})`
  - On UNIQUE constraint violation (`name` column): return form error "An entry with this name already exists"
  - On success: `throw redirect(303, '/library/{catalog}')`

3c. **Create form — `+page.svelte`:**
- Heading: "Add {config.label} Entry"; breadcrumb to `/library/{catalog}`
- `<form method="POST" action="?/create">` with one input per `config.formFields` entry (type driven by field's `type` value)
- Per-field error messages rendered adjacent to inputs when present in server response
- "Save" submit button; "Cancel" link to `/library/{catalog}`

3d. **Edit form — `+page.server.ts`:**
- Load: GM check + slug validation; `SELECT * FROM {config.table} WHERE id = ?` binding `params.id`; throw `error(404)` if not found; return `{ config, entry }`
- Form action `update`:
  - Re-validate GM status server-side
  - Verify entry exists before writing: `SELECT id FROM {config.table} WHERE id = ?`; throw 404 if gone
  - Build SET clause from `config.formFields[].key` (trusted constant) + `formData` values as bindings
  - Execute: `UPDATE {config.table} SET {set_clause}, updated_at = datetime('now') WHERE id = ?`
  - On UNIQUE violation: return form error "An entry with this name already exists"
  - On success: `throw redirect(303, '/library/{catalog}')`
- Form action `delete`:
  - Re-validate GM status server-side
  - Execute: `DELETE FROM {config.table} WHERE id = ?` binding `params.id`
  - On success: `throw redirect(303, '/library/{catalog}')`

3e. **Edit form — `+page.svelte`:**
- Heading: "Edit {config.label} — {entry.name}"; breadcrumb to list
- Same form structure as create page, pre-populated with `entry` values
- Delete section at the bottom: a separate `<form method="POST" action="?/delete">` with a visible "Delete entry" button; on click, reveal an inline "Are you sure?" confirmation before the submit fires (Svelte `let confirming = false` toggle — no browser `confirm()` dialogs)

**[DEV DECISION]:** Shared `CatalogForm.svelte` component. The new and edit pages render identical field structures. If extracting a shared component reduces duplication by more than 30% of markup, extract it. Otherwise inline form markup per page is acceptable for V1.

**Acceptance Criteria:**
- `/library/{catalog}/new` returns 403 for non-GM users; 404 for unknown catalog slug
- Submitting a valid create form adds a row and redirects to the catalog list
- Submitting with a duplicate name returns an inline form error — no crash, no redirect
- Submitting a valid edit form updates the row and redirects
- Delete action removes the row; catalog list confirms removal on reload
- All SQL column identifiers come from `config.formFields[].key` (trusted constant) — no user-supplied column names appear anywhere in SQL

---

## Task 4 — Sub-navigation within library

**File:** `companion/src/routes/library/+layout.svelte`

**Steps:**

4a. Create `companion/src/routes/library/+layout.svelte`:
- Renders a sub-nav bar (horizontal or sidebar) with links to all 11 catalog sections, using the same label/slug pairs from Task 1c
- Active section highlighted by comparing each link's `href` against `$page.url.pathname`
- `<slot />` for page content below the sub-nav

4b. No changes to the top-level app nav from Phase 3 Task 4a — it already has "Game Library" → `/library`.

4c. The sub-nav layout automatically wraps all routes under `/library/**`, including new and edit pages. This provides consistent navigation context without adding breadcrumb code to every page.

**[DEV DECISION]:** If the 11-link sub-nav bar is visually crowded, group into two rows or use a collapsible drawer — defer this to implementation-time judgment.

**Acceptance Criteria:**
- Sub-nav renders on all `/library/*` routes (landing, list, new, edit)
- Active section link is visually differentiated from inactive links
- Sub-nav does not require its own `+layout.server.ts` — inherits `player` data from root layout via `$page.data`

---

## Ordering and Dependencies

| Order | Task | Hard depends on | Parallelize with |
|---|---|---|---|
| 1st | Task 2a — `catalog-config.ts` (listColumns + filterFields) | Phase 1 schema finalized (column names locked) | Task 1 server |
| 1st | Task 1 — Landing page | Phase 3 complete (auth guard + stub route) | Task 2a |
| 2nd | Task 2b/2c — List pages | Task 2a (config drives queries) | Task 4 layout writing |
| 2nd | Task 4 — Sub-nav layout | Task 2a (config slug/label pairs exist) | Task 2b/2c writing |
| 3rd | Task 3a — `formFields` extension to config | Task 2a (extends same file) | Task 4 implementation |
| 4th | Task 3b/3c — Create forms | Tasks 2 + 3a | Task 3d/3e writing |
| 4th | Task 3d/3e — Edit forms | Tasks 2 + 3a | Task 3b/3c writing |

---

## Carry-Forward Notes (Phase 4 → V2)

- **Character viewer enrichment (V2):** Phase 3's character detail page renders `repData.spells` as plain Roll20 text. A V2 pass could cross-reference against `ref_spells` by name to surface spell descriptions inline. Not a V1 concern.
- **Bookmarkable detail URLs (V2):** `/library/{catalog}/{id}` is currently used only for edit routes. A read-only detail page per entry (shareable link) is a natural extension — expandable rows cover the V1 need.
- **Seed re-run:** GM can update catalog data by editing source Excels and re-running `npm run seed`. Phase 1 Task 5's idempotent upsert handles this correctly — no Phase 4 changes needed.
- **Phase 4 sign-off criteria:** All 11 catalog sections render with live data; name search and category filters work; GM can create, edit, and delete entries in all 11 catalogs; non-GM users cannot access create, edit, or delete routes (403); sub-nav renders on all library pages.
