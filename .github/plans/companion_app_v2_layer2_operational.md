
# Layer 2 — Operational Granularity
## Phase 1 — Data Foundation: Schema & Migrations

**Goal:** Extend the DB schema with 6 new tables and 2 column additions, run the migration against Turso, and seed all static campaign data (groups, group assignments, karma events, karma allocations, milestones) so every downstream phase has a populated, queryable foundation.

---

### Task 1 — Extend `schema.sql`: add `groups` table

**Inputs:** `companion/db/schema.sql` (existing), Phase 1 design specs  
**Outputs:** `groups` table DDL appended to `schema.sql`; indices defined

**Steps:**
1. Open `companion/db/schema.sql`.
2. After table 24 (`ref_elemental_services`) and before the Indices block, insert the new table block numbered 25.
3. `groups` columns: `id TEXT PK`, `campaign_id TEXT NOT NULL FK → campaigns(id)`, `group_name TEXT NOT NULL`, `created_at TEXT DEFAULT datetime('now')`.
4. Add `UNIQUE (campaign_id, group_name)` constraint.
5. Add index `idx_groups_campaign ON groups (campaign_id)` to the Indices block.

**Acceptance Criteria:** `schema.sql` parses without error; `groups` is table 25; FK to `campaigns` is declared; unique constraint is present.

---

### Task 2 — Extend `schema.sql`: add `group_id` FK to `characters`

**Inputs:** `schema.sql` with Task 1 complete  
**Outputs:** `characters` table DDL updated with nullable `group_id` FK column

**Steps:**
1. Locate the `characters` table DDL.
2. Add `group_id TEXT REFERENCES groups(id)` as a nullable column (no `NOT NULL` — existing rows will be NULL until seeded).
3. Add index `idx_characters_group ON characters (group_id)` to the Indices block.

**Acceptance Criteria:** `characters` table includes `group_id`; column is nullable; index exists.

---

### Task 3 — Extend `schema.sql`: add `sessions` table

**Inputs:** `schema.sql` with Task 2 complete  
**Outputs:** `sessions` table DDL appended

**Steps:**
1. Add table 26: `sessions` — columns: `id TEXT PK`, `campaign_id TEXT NOT NULL FK → campaigns(id)`, `session_number INTEGER`, `session_date TEXT`, `notes TEXT`, `created_at TEXT DEFAULT datetime('now')`.
2. Add `UNIQUE (campaign_id, session_number)` constraint.
3. Add index `idx_sessions_campaign ON sessions (campaign_id)`.

**Acceptance Criteria:** `sessions` table present; FK to `campaigns`; unique constraint on (campaign_id, session_number).

---

### Task 4 — Extend `schema.sql`: add `session_characters` join table

**Inputs:** `schema.sql` with Task 3 complete  
**Outputs:** M:N join table DDL appended

**Steps:**
1. Add table 27: `session_characters` — columns: `session_id TEXT NOT NULL FK → sessions(id) ON DELETE CASCADE`, `character_id TEXT NOT NULL FK → characters(id) ON DELETE CASCADE`.
2. Add `PRIMARY KEY (session_id, character_id)`.
3. Add index `idx_session_characters_char ON session_characters (character_id)`.

**Acceptance Criteria:** Composite PK; both FKs cascade on delete; index on character_id exists.

---

### Task 5 — Extend `schema.sql`: add `group_treasure` table

**Inputs:** `schema.sql` with Task 4 complete  
**Outputs:** `group_treasure` table DDL appended

**Steps:**
1. Add table 28: `group_treasure` — columns: `id TEXT PK`, `group_id TEXT NOT NULL FK → groups(id)`, `item_name TEXT NOT NULL`, `quantity INTEGER NOT NULL DEFAULT 1`, `owner_character_id TEXT REFERENCES characters(id)` (nullable — party items have no owner), `description TEXT`, `created_at TEXT DEFAULT datetime('now')`, `updated_at TEXT DEFAULT datetime('now')`.
2. [RESOLVED]: Currency uses a separate `group_currency` table — Option A confirmed. Columns: `gold INTEGER NOT NULL DEFAULT 0` (gold crowns), `silver INTEGER NOT NULL DEFAULT 0` (silver stags), `copper INTEGER NOT NULL DEFAULT 0` (copper pennies).
3. Add table 29 `group_currency` — `id TEXT PK`, `group_id TEXT NOT NULL UNIQUE FK → groups(id)`, `gold INTEGER NOT NULL DEFAULT 0`, `silver INTEGER NOT NULL DEFAULT 0`, `copper INTEGER NOT NULL DEFAULT 0`, `updated_at TEXT DEFAULT datetime('now')`.
4. Add index `idx_group_treasure_group ON group_treasure (group_id)`.

**Acceptance Criteria:** `group_treasure` table present; nullable owner FK; currency approach resolved and DDL matches decision.

---

### Task 6 — Extend `schema.sql`: add `karma_events` table

**Inputs:** `schema.sql` with Task 5 complete  
**Outputs:** `karma_events` table DDL appended

**Steps:**
1. Add table 30 (or 29/30 depending on Task 5 decision): `karma_events` — columns: `id TEXT PK`, `campaign_id TEXT NOT NULL FK → campaigns(id)`, `event_name TEXT NOT NULL`, `karma_amount INTEGER NOT NULL`, `date_awarded TEXT`, `created_at TEXT DEFAULT datetime('now')`.
2. Add index `idx_karma_events_campaign ON karma_events (campaign_id)`.

**Acceptance Criteria:** `karma_events` table present; FK to `campaigns`; no enforcement of `UNIQUE (campaign_id, event_name)` (same event name could recur in a campaign).

---

### Task 7 — Extend `schema.sql`: add `character_milestones` table

**Inputs:** `schema.sql` with Task 6 complete  
**Outputs:** `character_milestones` table DDL appended

**Steps:**
1. Add next table: `character_milestones` — columns: `id TEXT PK`, `character_id TEXT NOT NULL FK → characters(id) ON DELETE CASCADE`, `progression_name TEXT NOT NULL`, `milestone_1 TEXT`, `milestone_2 TEXT`, `milestone_3 TEXT`, `active_tier INTEGER NOT NULL DEFAULT 0`.
2. Add `CHECK (active_tier BETWEEN 0 AND 3)` constraint.
3. Add index `idx_character_milestones_char ON character_milestones (character_id)`.

**Acceptance Criteria:** Table present; CHECK constraint; FK with cascade delete; index exists.

---

### Task 8 — Extend `schema.sql`: alter `rep_karma` columns

**Inputs:** `schema.sql` with Task 7 complete, existing `rep_karma` DDL  
**Outputs:** `rep_karma` CREATE TABLE updated with two new columns

**Steps:**
1. Locate the `rep_karma` CREATE TABLE block (table 12).
2. Add column `source TEXT NOT NULL DEFAULT 'roll20'` — values will be `'roll20'`, `'companion'`, or `'seed'`.
3. Add column `karma_event_id TEXT REFERENCES karma_events(id)` (nullable — `roll20` rows won't reference a karma_event).
4. Remove the `NOT NULL` from `roll20_row_id` — companion-originated and seed rows will not have a Roll20 row ID.

[DEV DECISION]: `roll20_row_id` currently has `NOT NULL` and `UNIQUE (character_id, roll20_row_id)`. Making it nullable requires either (a) dropping the unique constraint, or (b) keeping the constraint but using a sentinel value for non-roll20 rows. Recommended approach: make `roll20_row_id` nullable, drop the `UNIQUE` constraint, and add a partial unique index `CREATE UNIQUE INDEX IF NOT EXISTS uq_rep_karma_roll20 ON rep_karma (character_id, roll20_row_id) WHERE roll20_row_id IS NOT NULL`.

**Acceptance Criteria:** `rep_karma` has `source` and `karma_event_id` columns; `roll20_row_id` is nullable; partial unique index is defined; no existing Roll20 rows will violate constraints.

---

### Task 9 — Verify `schema.sql` parses end-to-end

**Inputs:** Completed `schema.sql` from Tasks 1–8  
**Outputs:** Confirmation that all DDL is valid before migration runs

**Steps:**
1. Parse the full `schema.sql` locally using the existing `migrate.ts` statement splitter (strip line comments, split on `;`, filter empty) and count statements.
2. Verify no statement is blank or malformed.
3. Verify FK references are self-consistent (e.g., `karma_events` table is defined before `rep_karma` references it).
4. [DEV DECISION]: Table ordering in `schema.sql` matters because `migrate.ts` executes statements sequentially. Ensure `groups` is defined before `characters` uses `group_id`; `karma_events` before `rep_karma` uses `karma_event_id`.

**Acceptance Criteria:** Statement count is deterministic and non-zero; no FK is referenced before its parent table is created; dry-run parse exits cleanly.

---

### Task 10 — Run migration against Turso remote DB

**Inputs:** Verified `schema.sql`; `.dev.vars` with `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`  
**Outputs:** New tables and columns live in the remote Turso database

**Steps:**
1. Run `npm run migrate -- --force` from the `companion/` directory.
2. Confirm output: "Migration complete — N statements executed."
3. Spot-check via Turso CLI or libsql client: `SELECT name FROM sqlite_master WHERE type='table' ORDER BY name` — verify all new table names appear.
4. Verify `rep_karma` columns: `PRAGMA table_info(rep_karma)` — confirm `source` and `karma_event_id` are present.

**Risk:** `CREATE TABLE IF NOT EXISTS` is idempotent for new tables, but the `rep_karma` ALTER (removing `NOT NULL`, adding columns) is a structural change. Turso/SQLite does not support `ALTER TABLE DROP NOT NULL` — the column modification must be expressed as a new `CREATE TABLE` definition in `schema.sql`, not a standalone `ALTER TABLE`. Confirm that `migrate.ts` replaces the entire table definition (which it does — it runs the full DDL).

**Risk:** If the Turso DB already has rows in `rep_karma`, adding a `NOT NULL DEFAULT 'roll20'` column is safe — existing rows get the default. Making `roll20_row_id` nullable is also safe for existing rows.

**Acceptance Criteria:** All new tables visible in `sqlite_master`; `rep_karma` has 6 columns including `source` and `karma_event_id`; no migration errors.

---

### Task 11 — Create `seed-phase1.ts` script: seed groups

**Inputs:** Campaign ID `9ef60c48-6e85-4363-ac45-6efbbb4d9a5f`; groups A, B, C  
**Outputs:** 3 rows in `groups` table; group IDs captured for downstream use

**Steps:**
1. Create `companion/scripts/seed-phase1.ts` following the pattern of `seed-campaign.ts` (`.dev.vars` loader, `@libsql/client/node`, `--force` guard).
2. Hard-code the known campaign ID as `CAMPAIGN_ID` constant at top of file.
3. Insert 3 rows: group_name `'A'`, `'B'`, `'C'` with `crypto.randomUUID()` for each `id`.
4. Use `INSERT OR IGNORE` so the script is safe to re-run without duplicating groups.
5. Log the 3 group UUIDs to stdout after insert — they are needed for Task 12.

**Acceptance Criteria:** 3 rows in `groups` for the known campaign ID; script is idempotent; UUIDs are logged and captured.

---

### Task 12 — Seed `characters.group_id` assignments

**Inputs:** 4 active character names; 3 group IDs from Task 11; group assignment decisions  
**Outputs:** `group_id` set on all 4 active characters

**Steps:**
1. [DEV DECISION]: Assign each of the 4 characters (Breit the Wide, Rohan Drake, Caellum, Obon Unoekre) to a group (A, B, or C). This is campaign-world data the GM must confirm.
2. Once assignments are confirmed, add to `seed-phase1.ts`: for each character, `UPDATE characters SET group_id = ? WHERE name = ? AND campaign_id = ?`.
3. Log the update count after each statement; error if count is 0 (character not found).
4. Use character `name` field for lookup since Roll20 character IDs may differ from the internal `id`.

**Acceptance Criteria:** All 4 active characters have a non-NULL `group_id`; group IDs correspond to groups seeded in Task 11; script logs each assignment.

---

### Task 13 — Seed `karma_events` (16 campaign events)

**Inputs:** 16 karma events with names and amounts (from Karma Tracker workbook — see Phase 1 spec); campaign ID  
**Outputs:** 16 rows in `karma_events`; total karma_amount sums to 36

**Steps:**
1. Add a `seedKarmaEvents()` function to `seed-phase1.ts`.
2. Hard-code the 16 event tuples as a `const` array: `[event_name, karma_amount][]`.
3. For each event, insert a row with `crypto.randomUUID()` id, the known campaign ID, event_name, karma_amount, and `date_awarded = NULL` (no date data available from workbook).
4. Use `INSERT OR IGNORE` on `(campaign_id, event_name)` if a unique index exists; otherwise check for existing rows before insert to preserve idempotency.
5. After all inserts, run `SELECT SUM(karma_amount) FROM karma_events WHERE campaign_id = ?` — assert result equals 36.
6. Log each event name + amount + generated ID.

**Risk:** Karma event count discrepancy — the spec states "17 events" in the header but lists 16 events totaling 36. Clarify with GM before seeding: is there a 17th event missing from the list, or was the header count wrong?

**Acceptance Criteria:** 16 rows in `karma_events` (or 17 if GM confirms the 17th); SUM of karma_amount = 36; script logs the total and errors if assertion fails.

---

### Task 14 — Seed character-level karma spend entries (`rep_karma`)

**Inputs:** Character-level karma data from Excel pg3 (6 entries for Rohan Drake, 6 for Caellum); character IDs; karma_event IDs from Task 13  
**Outputs:** `rep_karma` rows with `source='seed'`; spend entries with negative amounts and `source='companion'`

**Steps:**
1. Add a `seedCharacterKarma()` function to `seed-phase1.ts`.
2. For each character, map their earned-karma entries (positive amounts) to the corresponding `karma_events` row ID by event name. Insert `rep_karma` rows with `source='seed'`, `karma_event_id = <matched ID>`, `roll20_row_id = NULL`, `karma_event = <event_name>`, `karma_amount = <positive amount>`.
3. Insert spend entries (negative amounts: "Level Body to 4" → -8, "Added Pick locks skill" → -2 for Rohan) with `source='companion'`, `karma_event_id = NULL`, `roll20_row_id = NULL`.
4. [RESOLVED]: The Excel pg3 data is for Rohan and Caellum only. Breit has no pg3 in the workbook — seed only if karma allocations surface later. Obon is a test character and excluded from seeding entirely.
5. Use `INSERT OR IGNORE` keyed on `(character_id, karma_event_id)` for earned entries to prevent duplicates on re-run.

**Acceptance Criteria:** Each seeded character has rep_karma rows matching their Excel pg3 data; spend entries have negative amounts; `source` column is set correctly on every row; no NULL violations.

---

### Task 15 — Add npm script for `seed-phase1.ts`

**Inputs:** `companion/package.json`; completed `seed-phase1.ts`  
**Outputs:** New npm script entry `"seed-phase1": "tsx scripts/seed-phase1.ts"`

**Steps:**
1. Open `companion/package.json`.
2. Add `"seed-phase1": "tsx scripts/seed-phase1.ts"` alongside the existing `"migrate"` and `"seed"` scripts.
3. Verify `tsx` is available as a dev dependency (it already is, given `migrate.ts` uses it).

**Acceptance Criteria:** `npm run seed-phase1 -- --force` resolves and runs without "script not found" error.

---

### Task 16 — End-to-end verification

**Inputs:** Populated Turso DB after Tasks 10–14  
**Outputs:** Spot-check query results confirming all seeded data

**Steps:**
1. Query `SELECT g.group_name, c.char_name FROM groups g LEFT JOIN characters c ON c.group_id = g.id WHERE g.campaign_id = ?` — confirm 3 groups and 4 characters distributed.
2. Query `SELECT COUNT(*), SUM(karma_amount) FROM karma_events WHERE campaign_id = ?` — confirm 16 rows and SUM = 36.
3. Query `SELECT source, COUNT(*) FROM rep_karma GROUP BY source` — confirm `'roll20'` rows exist (from prior sync), `'seed'` rows exist (earned karma), `'companion'` rows exist (spend entries).
4. Query `SELECT COUNT(*) FROM character_milestones` — confirm 0 rows (no milestone data in Phase 1; will be seeded in a later phase).
5. Confirm `group_treasure` and `sessions` / `session_characters` tables exist and are empty (correct for Phase 1).

**Acceptance Criteria:** All 5 verification queries return expected values; no FK violation errors; Phase 1 is releasable as a standalone DB state.

---

### Dependency Order

```
Task 1  →  Task 2  →  Task 9
Task 3  →  Task 4        ↓
Task 5 (DEV DECISION: currency)   Task 10 (migration)
Task 6  ←── depends on Task 5 table numbering         ↓
Task 7                            Task 11 (seed groups)
Task 8  →  Task 9                        ↓
                             Task 12 (assign characters)
                             Task 13 (karma events)
                                         ↓
                             Task 14 (char karma entries)
                             Task 15 (npm script — can run anytime after seed-phase1.ts created)
                             Task 16 (verification — last)
```

### Risks & Open Questions

| # | Risk / Ambiguity | Owner | Blocking? |
|---|---|---|---|
| R1 | Karma event count: 16 listed totaling 36, assumed 17 total — one event missing from workbook. Seed the 16 known; add 17th later. | GM | ~~Yes~~ RESOLVED — seed 16 now |
| R2 | Group assignments: Rohan → A, Caellum → B, Breit → C. Obon = test character, skip. | GM | ~~Yes~~ RESOLVED |
| R3 | `roll20_row_id NOT NULL` change on `rep_karma` — verify no app-layer code does a blanket INSERT that omits `roll20_row_id` | Developer | Yes — before Task 10 |
| R4 | `group_currency` as separate table vs. flag in `group_treasure` | Developer/GM | ~~Yes~~ RESOLVED — Option A: separate `group_currency` table (gold crowns, silver stags, copper pennies) |
| R5 | Breit historical karma data: none found in Excel pg3 — if he has karma allocations, they're missing from seed. Obon is a test character and excluded from seeding. | GM | No — can add later |
| R6 | `karma_events` unique constraint: can the same event name recur? (e.g., "Barbarians Attack!" twice) | GM | No — low risk, no unique index proposed |

---

## Phase 1 — Data Foundation: Schema & Migrations (REVISED)
*Revision addresses Reviewer FAIL findings 1–7. This replaces the previously rejected Phase 1 plan.*

**Goal:** Establish the full relational backbone — add 6 new tables to schema.sql, produce an idempotent ALTER TABLE migration for 3 existing tables, and seed reference data (groups, karma events). Character-to-group assignment is a blocking sub-task contingent on user confirmation of group assignments.

**Features:** U1 (schema), U1b (schema), U16 (karma schema), U18 (milestone schema — reuses rep_milestones)

---

### Task 1 — Update schema.sql: New Table DDL
**Scope:** schema.sql structural changes only — new table definitions, no changes to existing ones

**Steps:**
a. Insert `groups` table DDL immediately **before** the `characters` table definition in schema.sql
b. Insert `karma_events` table DDL immediately **before** the `rep_karma` table definition in schema.sql
c. Insert `sessions` table DDL after the `groups` definition
d. Insert `session_characters` M:N join table DDL after both the `sessions` and `characters` definitions
e. Insert `group_treasure` table DDL after the `groups` definition
f. Insert `group_currency` table DDL after `group_treasure` (confirmed Option A — separate table for party funds: gold crowns, silver stags, copper pennies)

**Notes:**
- SQLite does not validate FK references at CREATE TABLE time — enforcement only occurs at DML time when `PRAGMA foreign_keys=ON`. Positioning new tables before their dependents is logical convention only, not a hard runtime requirement. [Addresses FINDING-2]
- All new table DDL uses `CREATE TABLE IF NOT EXISTS` — safe for idempotent fresh-DB execution via the existing migrate.ts splitter
- Column definitions for all 6 new tables are specified in Layer 3 blueprints
- [DEV DECISION — from BD-2]: `sessions` table must include `name TEXT` and `status TEXT NOT NULL DEFAULT 'active'` columns in addition to the columns specified in the original Phase 1 Task 3. Developer adds these when authoring the DDL.

**Acceptance Criteria:**
- schema.sql contains all 6 new table definitions: `groups`, `sessions`, `session_characters`, `group_treasure`, `group_currency`, `karma_events`
- Each new table definition appears in schema.sql before the first dependent table that references it
- schema.sql is parseable by the existing migrate.ts (split-on-`;` approach) without error on a fresh DB

**Dependencies:** None — first task

---

### Task 2 — Produce ALTER TABLE migration script
**Scope:** New file `companion/scripts/migrate-add-columns.ts`

**Steps:**
a. For each target table, query `PRAGMA table_info({table_name})` and parse the resulting column list into a Set of existing column names
b. For each column to be added: skip the ADD COLUMN statement if the column name is already present in the PRAGMA output (idempotency guard — SQLite has no native `ADD COLUMN IF NOT EXISTS`)
c. Execute the following ADD COLUMN operations in order:
   - `characters`: ADD COLUMN `group_id` (TEXT, nullable, foreign key references groups(id)) [Addresses FINDING-1]
   - `rep_karma`: ADD COLUMN `source` (TEXT NOT NULL DEFAULT 'roll20') [Addresses FINDING-1]
   - `rep_karma`: ADD COLUMN `karma_event_id` (TEXT, nullable, foreign key references karma_events(id)) [Addresses FINDING-1]
   - `rep_milestones`: ADD COLUMN `source` (TEXT NOT NULL DEFAULT 'roll20') [Addresses FINDING-5]
d. Do NOT alter `roll20_row_id` on any table — it remains NOT NULL on both `rep_karma` and `rep_milestones`. Companion-originated entries will use a `comp-{uuid}` format value to satisfy the existing UNIQUE(character_id, roll20_row_id) constraint without nulls or constraint modification. [Addresses FINDING-1, FINDING-6]
e. Log each operation: emit "SKIPPED (column exists): {table}.{column}" or "APPLIED: ALTER TABLE {table} ADD COLUMN {column} ..." for each step

**Acceptance Criteria:**
- Script runs to completion on a DB that already has all 4 new columns — all 4 operations logged as SKIPPED, exit 0
- Script runs to completion on a fresh DB (after migrate.ts) — all 4 operations logged as APPLIED, exit 0
- After a fresh run: `PRAGMA table_info(characters)` includes `group_id`; `PRAGMA table_info(rep_karma)` includes `source` and `karma_event_id`; `PRAGMA table_info(rep_milestones)` includes `source`
- No table recreation performed — all changes are ADD COLUMN only

**Dependencies:** Task 1 must be committed before this script is run (groups and karma_events tables must exist for FK references to resolve at DML time)
**Can be authored in parallel with:** Tasks 3, 4, and the Task 5 stub

---

### Task 3 — Seed script: groups
**Scope:** New file `companion/scripts/seed-groups.ts`

**Steps:**
a. Read DB connection config from `.dev.vars` (same pattern as existing seed scripts)
b. Apply `--force` guard — abort with logged error if flag is absent in non-dev environment
c. **Idempotency pattern:** DELETE all rows WHERE `campaign_id = '9ef60c48-6e85-4363-ac45-6efbbb4d9a5f'`, then INSERT 3 new rows. [Addresses FINDING-4 — DELETE-then-INSERT, no INSERT OR IGNORE]
d. Insert groups: names "A", "B", "C"; campaign_id = `9ef60c48-6e85-4363-ac45-6efbbb4d9a5f`; id = freshly generated UUID per group
e. Log the inserted row UUIDs to stdout so they can be used as input for Task 5

**Acceptance Criteria:**
- After first run: `groups` table has exactly 3 rows for the campaign
- After second run (re-run): `groups` table still has exactly 3 rows — no duplicates
- Script exits non-zero and logs an error message if `--force` is absent in non-dev environment

**Dependencies:** None — authoring independent
**Can be authored in parallel with:** Tasks 2, 4, 5 stub

---

### Task 4 — Seed script: karma_events
**Scope:** New file `companion/scripts/seed-karma-events.ts`

**Steps:**
a. Read DB connection config from `.dev.vars`
b. Apply `--force` guard
c. **Idempotency pattern:** DELETE WHERE `campaign_id = '9ef60c48-6e85-4363-ac45-6efbbb4d9a5f'` AND `source = 'seed'`, then INSERT all 16 events. [Addresses FINDING-4]
d. Insert 16 known karma events verbatim — preserve source spelling exactly, no normalization. Note: total count is assumed to be 17 (one event may be missing from the source workbook). Insert the 16 known events; the 17th can be added later when identified:
   1. "Barbarians Attack!" — karma_amount: 2
   2. "Rancid Cellar cleansing" — karma_amount: 3
   3. "Troubled Crypt" — karma_amount: 3
   4. "Rexton's boxing match against Big Joe" — karma_amount: 1
   5. "Dead Oak Dungeon rescue" — karma_amount: 3
   6. "Scales of Justice" — karma_amount: 4
   7. "Finding sewer exit and entrance to Dead Oak" — karma_amount: 1
   8. "Rosa's Tower" — karma_amount: 3
   9. "Rexton's boxing match against Big Gram Tolb" — karma_amount: 1
   10. "Gathering materials for healing potions" — karma_amount: 2
   11. "Whistle and Rohans notebook retrival" — karma_amount: 4
   12. "Rexton vs Kraven" — karma_amount: 1
   13. "gather silver" — karma_amount: 1
   14. "gather bowstring (Tunnel Troll)" — karma_amount: 1
   15. "Gambiling Den" — karma_amount: 2
   16. "Fey Adventure for bow wood" — karma_amount: 4
e. Each row: id = UUID, campaign_id = `9ef60c48-6e85-4363-ac45-6efbbb4d9a5f`, name, karma_amount, source = 'seed'

**Note:** Event name spellings ("Gambiling Den", "retrival") are preserved as-is from the source workbook. Corrections are a future editorial decision, not a schema concern.

**Acceptance Criteria:**
- After first run: `karma_events` table has exactly 16 rows for the campaign with `source = 'seed'` (17th event TBD — will be added when identified)
- After second run (re-run): exactly 16 rows — no duplicates
- Sum check: `SELECT SUM(karma_amount) FROM karma_events WHERE campaign_id = ? AND source = 'seed'` returns **36** (will increase when 17th event is added)

**Dependencies:** None — authoring independent
**Can be authored in parallel with:** Tasks 2, 3, 5 stub

---

### Task 5 — Data migration: assign existing characters to groups
**Scope:** New file `companion/scripts/migrate-character-groups.ts`

**[RESOLVED]: Group assignments confirmed by GM — Rohan Drake → A, Caellum → B, Breit the Wide → C. Obon Unoekre is a test character and should be skipped.**

**Steps (authoring the stub now; populating values after user confirms assignments):**
a. For each of the 4 characters, look up the character's `id` using `WHERE char_name = ? AND campaign_id = ?` [Addresses FINDING-3 — column is `char_name`, not `name`]
b. Execute: `UPDATE characters SET group_id = ? WHERE char_name = ? AND campaign_id = ?`
c. Target characters and confirmed group assignments:
   - Rohan Drake → Group A
   - Caellum → Group B
   - Breit the Wide → Group C
   - Obon Unoekre → SKIP (dummy character used for player testing — not a real PC)
d. Default mode: dry-run — log the SQL that would execute, do not commit; require explicit `--confirm` flag to execute
e. After `--confirm` run: log count of rows updated (expect 3)

**Acceptance Criteria:**
- Dry-run mode logs 4 UPDATE statements with correct `char_name` values — no writes to DB
- After `--confirm` run: `SELECT char_name, group_id FROM characters WHERE campaign_id = ?` shows a non-null `group_id` for Rohan Drake, Caellum, and Breit the Wide
- Obon Unoekre retains NULL `group_id` (test character — excluded from assignment)
- 3 rows updated, 0 errors

**Dependencies (execution):** Task 2 (group_id column must exist on characters), Task 3 (groups must be seeded so FK references resolve)
**Authoring dependency:** None — stub can be written in parallel with Tasks 2–4

---

### Task 6 — Verification: confirm migration pipeline is end-to-end correct
**Scope:** Smoke test — no new files required

**Steps:**
a. Run `migrate.ts` against a fresh test database
b. Query `SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name` on the result
c. Confirm all 5 new table names are present: `groups`, `sessions`, `session_characters`, `group_treasure`, `karma_events`
d. Confirm existing tables are unaffected: `characters`, `rep_karma`, `rep_milestones`, and any others present before
e. Run `migrate-add-columns.ts` against the same test DB — confirm all 4 operations logged as APPLIED
f. Run `migrate-add-columns.ts` a second time against the same DB — confirm all 4 operations logged as SKIPPED

**Acceptance Criteria:**
- All 5 new tables present after migrate.ts run; no existing tables dropped or modified
- First run of migrate-add-columns.ts: 4 APPLIED entries, 0 SKIPPED, exit 0
- Second run of migrate-add-columns.ts: 4 SKIPPED entries, 0 APPLIED, exit 0
- No parse failures, no FK errors, no constraint violations

**Dependencies:** Tasks 1 and 2 complete and committed

---

### Dependency & Execution Map

**Authoring parallelism (all can be written simultaneously after Task 1 is underway):**
- Tasks 2, 3, 4, and the Task 5 stub are fully independent at authoring time

**Execution order (strict):**
1. Task 1 — commit schema.sql changes (prerequisite for everything else)
2. Task 2 run — migrate-add-columns.ts (new columns on existing tables)
3. Tasks 3 & 4 runs — seed-groups.ts and seed-karma-events.ts (order between them is irrelevant)
4. Task 5 run — BLOCKED until group assignments confirmed by user
5. Task 6 — verification pass (can run alongside or after Steps 2–3)

**RESOLVED:** Group assignments confirmed:
- Rohan Drake → Group A
- Caellum → Group B
- Breit the Wide → Group C
- Obon Unoekre → SKIP (test character)

---

## Phase 2 — GM Command Center: Dashboard, Roster & Character Management

**Goal:** Build the GM's home base — role-based landing routing, enriched character list, campaign overview dashboard, player roster with group/player reassignment, GM karma award action, and player-facing character upload portal.

**Features:** U3 (GM dashboard), U4 (player roster), U5 (reassign/un-assign), U6 (character enrichment), U15 (character upload), U16 (GM karma award)

**Phase dependency:** Phase 1 must be fully executed (schema migrated, columns added, seeds applied) before any route in this phase goes live. Karma award (Task 5) requires `karma_events` and `rep_karma` columns from Phase 1.

---

### Task 1 — Route Scaffolding + Role-Based Landing Routing
**Scope:** Create `/dashboard` and `/roster` route stubs, apply GM auth guards, and modify the root landing page to redirect authenticated users by role.

**Steps:**
a. Create `/dashboard/+page.server.ts` stub: call `requireGm(locals, platform)` at the top of `load()`. Return empty placeholder data; full queries added in Task 3.
b. Create `/dashboard/+page.svelte` stub: render "GM Dashboard" heading with loading placeholder.
c. Create `/roster/+page.server.ts` stub: call `requireGm(locals, platform)`. Return empty placeholder data; queries added in Task 4.
d. Create `/roster/+page.svelte` stub: render "Player Roster" heading.
e. Modify `/+page.server.ts` (root landing `load()`): call `locals.auth()`. Branch — if `is_gm = 1`: `redirect(302, '/dashboard')`; if `is_gm = 0`: `redirect(302, '/characters')`; if unauthenticated: return no redirect (existing welcome page).

[RESOLVED]: Route placement — **both top-level**: `/dashboard` and `/roster`. These are primary GM surfaces, not admin utilities. The existing `/admin/assign` is the oddball and may eventually fold into `/roster`.

**Acceptance Criteria:**
- GET `/dashboard` with a non-GM authenticated session returns 403 or redirects to login (existing `requireGm` behavior).
- GET `/roster` (or `/admin/roster`) with a non-GM session is similarly guarded.
- An authenticated GM hitting `/` is redirected to `/dashboard`.
- An authenticated non-GM player hitting `/` is redirected to `/characters`.
- Unauthenticated user hitting `/` sees the existing welcome page — no regression.

**Dependencies:** None. Stub files are fully independent. `requireGm()` already exists — no changes needed to the guard itself.

---

### Task 2 — Character List Enrichment (U6)
**Scope:** Extend the `/characters` page query with owner, group, and combat stat columns; add client-side sorting and filtering.

**Steps:**
a. Inspect the live DB: run `PRAGMA table_info(characters)` to identify exact column names for initiative (base score), physical condition monitor max and filled, and stun condition monitor max and filled. Record these names — they are required inputs for all subsequent steps.
b. Update `/characters/+page.server.ts` `load()` query:
   - JOIN `players ON characters.player_id = players.id` → bring in `discord_name` as the owner display name.
   - LEFT JOIN `groups ON characters.group_id = groups.id` → bring in `group_name`.
   - Include the initiative and condition monitor columns identified in step (a).
   - Include `synced_at` with a computed staleness flag: character is stale if `synced_at < datetime('now', '-N days')` where N is a named constant at the top of the file (not a magic number).
c. Preserve existing row-level visibility: GM receives all rows; player receives only rows where `characters.player_id = current_user.id`. Confirm this gate is still in place after the query rewrite.
d. Update `/characters/+page.svelte`:
   - Add columns: Owner (GM session only), Group (all), Physical CM as `filled/max`, Stun CM as `filled/max`, Stale badge (all).
   - GM-only columns are conditionally rendered based on a `isGm` value passed from the server — not derived client-side from role inference.
   - Implement column sorting via Svelte 5 `$state` (`sortKey`, `sortDir`) + `$derived` for the sorted rows array. Clicking a header sets/toggles the sort; the derived array re-sorts reactively.
   - Add filter controls: Group dropdown (values from groups in the data), Owner dropdown (GM only, values from distinct owners in the data), Stale checkbox (show stale only). Filters compose — a Group + Stale selection both apply simultaneously. Implement filters via a single `$derived` filtered-then-sorted rows array.

[RESOLVED]: Staleness threshold — **7 days**. Defined as a named constant `STALE_THRESHOLD_DAYS = 7`. Shared between Tasks 2 and 3.

[DEV DECISION]: Condition monitor display — does the `characters` table store the *current filled* value (damage taken at last sync) or only the *maximum* value? If only max, display as "— / max" and note that current damage is not tracked until Roll20 sync is enhanced. Confirm by inspecting the schema column names found in step (a).

[DEV DECISION]: Filter and sort scope — all filtering and sorting should be client-side (small data set, ≤20 characters, no page navigation needed). If this assumption is wrong (large campaigns in future), server-side pagination is a separate future task. Confirm client-side is acceptable.

**Acceptance Criteria:**
- Owner column visible in GM session; absent in player session.
- Group column shows group name or "—" for unassigned characters.
- CM columns show values as fractions; Stale badge appears on characters beyond the configured threshold.
- Clicking any column header sorts the list; clicking again reverses direction.
- Group dropdown, Owner dropdown (GM), and Stale checkbox all filter independently and compose correctly.
- Existing columns (character name link, Campaign, Last Synced) are still present — no regression.
- Player session: own characters only, no Owner column.

**Dependencies:** Phase 1 Task 2 (`group_id` column on `characters` must exist for the GROUP JOIN to return data). Task 1 of this phase not required — `/characters` route already exists.

---

### Task 3 — GM Dashboard Page (U3)
**Scope:** Implement the `/dashboard` load function and page with campaign overview stats, stale alert panel, quick links, and karma event history table.

**Steps:**
a. Implement `/dashboard/+page.server.ts` `load()` — run 5 queries in parallel via `Promise.all()`:
   1. Player count: `SELECT COUNT(DISTINCT player_id) AS player_count FROM characters WHERE campaign_id = ?` (GM has no characters — this naturally excludes the GM).
   2. Character counts by group: `SELECT g.group_name, COUNT(c.id) AS char_count FROM groups g LEFT JOIN characters c ON c.group_id = g.id WHERE g.campaign_id = ? GROUP BY g.id ORDER BY g.group_name`.
   3. Total active character count: characters with `group_id IS NOT NULL` and `campaign_id = ?` (used for the "N active characters" karma form label in Task 5).
   4. Stale characters: `SELECT c.char_name, p.discord_name, c.synced_at FROM characters c JOIN players p ON c.player_id = p.id WHERE c.campaign_id = ? AND c.synced_at < datetime('now', '-N days')` — use the same `N` constant as Task 2.
   5. Karma event history: `SELECT event_name, karma_amount, source, date_awarded FROM karma_events WHERE campaign_id = ? ORDER BY date_awarded DESC, id DESC LIMIT 50`.
b. Implement `/dashboard/+page.svelte` with 4 named sections:
   1. **Overview**: player count, per-group character counts (one stat box per group), total active PC count.
   2. **Stale Alerts**: list of stale characters with player name and last-synced timestamp. If none, show "All characters up to date."
   3. **Karma Award** (U16 form, authored in Task 5 but rendered here): placeholder slot in this task; wired in Task 5.
   4. **Karma Event History**: table — Event Name | Karma Amount | Source badge | Date Awarded. Source badge: `source = 'seed'` → "Imported"; `source = 'companion'` → "In-app".
c. Quick links section: navigation links to `/roster`, `/characters`, `/library`. Future `/sessions` link rendered as visually distinct "Coming soon" placeholder — not a dead `<a>` tag.

[DEV DECISION]: Dashboard layout — single-column vs. 2-column grid (stats + karma history side by side). Recommendation: 2-column — stat cards left, karma history right — maximises information density for a GM-facing overview page.

[DEV DECISION]: Should the karma award action form live inline on the dashboard (recommended — avoids a separate route for a 2-field form) or on a dedicated `/admin/karma` route? Inline is simpler and consistent with the "command center" mental model. Confirm before starting Task 5.

**Acceptance Criteria:**
- Player count displays correctly for current campaign.
- Group breakdown shows A: 1, B: 1, C: 1 (Obon excluded; `group_id IS NULL`).
- Stale alerts correctly identify characters not synced within the threshold; a freshly-synced character does not appear.
- Karma event history lists all 16 seeded events plus any companion-created events, most recent first.
- Source badge correctly distinguishes "Imported" (seed) from "In-app" (companion).
- Quick links navigate to valid routes without 404.
- Non-GM users cannot access this page (Task 1 guard).

**Dependencies:** Task 1 stubs and guard. Phase 1 data (seeded groups, karma events) must be present for history and stats to populate. Task 5 authored to complete the karma form section.

---

### Task 4 — Player Roster + Character Reassignment (U4, U5)
**Scope:** Implement the `/roster` page with a full players → characters → groups mapping and form actions for group reassignment and group un-assignment.

**Steps:**
a. Implement `/roster/+page.server.ts` `load()`:
   - Main query: `SELECT p.id AS player_id, p.discord_name, c.id AS char_id, c.char_name, g.id AS group_id, g.group_name FROM players p LEFT JOIN characters c ON c.player_id = p.id AND c.campaign_id = ? LEFT JOIN groups g ON c.group_id = g.id WHERE p.is_gm = 0 ORDER BY p.discord_name, c.char_name`.
   - Groups dropdown query: `SELECT id, group_name FROM groups WHERE campaign_id = ? ORDER BY group_name`.
b. Implement `/roster/+page.svelte`:
   - Table columns: Player | Character | Group | Actions.
   - Per character row: group dropdown + "Assign" button; "Unassign" button.
   - Players who own no characters appear with empty character/group cells — not omitted from the list.
c. Implement form actions in `/roster/+page.server.ts` — each action first verifies the target character belongs to the campaign before executing any write:
   - `assignGroup`: read `char_id`, `group_id` from form data. Validate both present. Verify: `SELECT id FROM characters WHERE id = ? AND campaign_id = ?`. On verified: `UPDATE characters SET group_id = ? WHERE id = ?`. Redirect.
   - `unassignGroup`: read `char_id`. Verify character belongs to campaign. `UPDATE characters SET group_id = NULL WHERE id = ?`. Redirect.

*Player-to-player reassignment (`assignPlayer`) deferred — no value-add now. U5 scope is group assignment/un-assignment only.*

[DEV DECISION]: Campaign ID guard — each action validates the character's `campaign_id` against a known campaign constant. For now, the campaign ID is the known constant (`9ef60c48-...`). Future multi-campaign support will require storing the active campaign on the session. Flag this as known debt — do not implement multi-campaign logic now.

**Acceptance Criteria:**
- Roster shows all non-GM players; each appears with their character(s) and current group assignment.
- A player with no characters shows a row with empty character/group cells.
- "Unassign" sets `group_id = NULL`; reload of `/roster` confirms the change.
- "Assign group" updates `group_id`; reload confirms.
- Each action rejects a `char_id` that does not belong to the campaign — returns error, no DB write.
- Non-GM users cannot access this page (Task 1 guard).

**Dependencies:** Task 1 stubs and guard. Phase 1 Task 3 (groups seeded), Phase 1 Task 5 (character assignments applied, so initial state is populated).

---

### Task 5 — GM Karma Award (U16)
**Scope:** Inline karma award form on the GM Dashboard — inserts a `karma_events` row and a `rep_karma` row for every active PC (characters with `group_id IS NOT NULL`).

**Steps:**
a. Add karma award form to `/dashboard/+page.svelte` above the karma event history table:
   - Field: `event_name` (text, required).
   - Field: `karma_amount` (positive integer, required, min=1).
   - Informational note derived from load data: "Will be awarded to {awardedCount} active characters."
   - Submit button: "Award Karma to All PCs".
b. Modify `/dashboard/+page.server.ts` `load()` (from Task 3) to include the active PC count query from Task 3 step a.3 — pass result as `awardedCount` in page data.
c. Implement form action `awardKarma` in `/dashboard/+page.server.ts`:
   1. Read `event_name` (string) and `karma_amount` (integer) from form data. Validate: `event_name` non-empty, `karma_amount` is an integer ≥ 1. On failure: `return fail(400, { error: '<message>' })` — no DB writes.
   2. Generate UUIDs: one for the `karma_events` row, one companion sentinel per PC.
   3. Insert `karma_events`: id, campaign_id, event_name, karma_amount, source = `'companion'`, date_awarded = current UTC datetime string.
   4. Query active PCs: `SELECT id FROM characters WHERE campaign_id = ? AND group_id IS NOT NULL`.
   5. For each PC id: insert `rep_karma` row — character_id, roll20_row_id = `'comp-{uuid}'` (unique per row, never NULL), karma_event = event_name, karma_amount, source = `'companion'`, karma_event_id = the new `karma_events` id.
   6. On success: redirect back to `/dashboard` (reloads the karma history table with the new event at top).

[DEV DECISION]: "All PCs" predicate is `group_id IS NOT NULL`. This naturally excludes Obon (test character, no group assignment). Confirm this is the correct exclusion mechanism.

[DEV DECISION]: `karma_amount` type — integer only, or allow positive fractions (e.g., 0.5 for partial-session participation)? Spec says integer. Confirm with GM.

**Acceptance Criteria:**
- Valid submission creates exactly 1 `karma_events` row (`source='companion'`) and N `rep_karma` rows (one per character with non-null `group_id`).
- `rep_karma` rows: `roll20_row_id = 'comp-{uuid}'` (distinct UUID per row, never NULL), `source = 'companion'`, `karma_event_id` points to the new event row.
- After redirect, the new event appears at the top of the karma history table on the dashboard.
- Empty `event_name` or `karma_amount < 1` → 400 error returned to form, no DB writes.
- Characters with `group_id IS NULL` receive no `rep_karma` row.
- The "Will be awarded to N" count matches the count of rows inserted.

**Dependencies:** Task 3 (same `+page.server.ts` file). Phase 1 Task 1 (`karma_events` table), Phase 1 Task 2 (rep_karma `source` and `karma_event_id` columns must exist).

---

### Task 6 — Character Upload Portal (U15)
**Scope:** Player-facing `/upload` route for importing a character from a `.xlsx` workbook into the companion app.

**RESOLVED: Excel parsing uses Option A — SheetJS client-side.** Cell-by-position reads (`worksheet['B2']?.v`) fully cover the use case. Zero new infrastructure, Cloudflare-native.

**Steps:**
a. Install `xlsx` npm package as a dependency in `companion/`.

b. Create `/upload/+page.server.ts` and `/upload/+page.svelte`. Require authentication (any player, including GM). Redirect unauthenticated users to login.

c. Implement the 2-step upload flow on `/upload/+page.svelte`:
   - **Step 1 (client-side, no round-trip)**: Player selects a `.xlsx` file using a file input. An `onchange` handler (or `$effect`) uses SheetJS (Option A) to read the workbook and extract the list of sheet names. Sheet names are rendered as a dropdown/radio list.
   - **Step 2 (form submit)**: Player selects the pg1 sheet name (identity/attributes/condition monitors). A separate pg2 sheet selector appears for the gear/weapons/money sheet (pg2 naming conventions vary per player). Player submits the form.

d. Implement form action `uploadCharacter` in `/upload/+page.server.ts`:
   1. Validate: file present, extension `.xlsx`, file size ≤ configured maximum (e.g., 5 MB). Return 400 with error message on failure.
   2. Parse pg1 by cell position: character name, metatype/race, all attributes, condition monitor max values. Cell positions are defined in a separate `excel-cell-map.ts` config file — not hardcoded in the action.
   3. Parse pg2 by row iteration: weapon rows, gear rows, nuyen. Map to the appropriate rep table column names.
   4. Duplicate check: `SELECT id FROM characters WHERE char_name = ? AND player_id = ?`. If a match exists, apply the conflict resolution strategy confirmed in the DEV DECISION below.
   5. On new character: insert into `characters` with `player_id = current_user.id`, `campaign_id = known_campaign_id`, all scalar field values from pg1, `synced_at = now()`, `group_id = NULL` (GM assigns after import). Insert rep table rows for gear and weapons — all companion-originated rep rows use `roll20_row_id = 'comp-{uuid}'` and `source = 'companion'`.
   6. On success: redirect to `/characters` or the new character's detail page with a success flash message.

[RESOLVED]: Duplicate character handling — **reject** with "Character already exists" error message. No overwrite, no confirmation screen.

[DEV DECISION]: pg2 rep tables — identify which rep tables and column names receive weapon rows, gear rows, and nuyen. Recommendation: implement and validate pg1 first; add pg2 support in a follow-on sub-task once pg1 round-trips correctly.

[DEV DECISION]: GM upload on behalf of a player — should the GM be able to upload a character and assign it to a specific player from a dropdown? If yes, add an optional `target_player_id` field that GMs can set.

**Acceptance Criteria:**
- GET `/upload` renders the upload form for authenticated users; unauthenticated users are redirected to login.
- Selecting a `.xlsx` file populates the sheet picker with the workbook's sheet names — no server round-trip required.
- Submitting with valid sheet selections and a non-duplicate character name creates a new `characters` row: correct `char_name`, `player_id`, `campaign_id`, `synced_at`, `group_id = NULL`.
- The new character appears in the player's `/characters` list after redirect.
- Non-`.xlsx` file types are rejected before any parsing with a descriptive error message.
- Files over the size limit are rejected with a descriptive error message.
- Duplicate character name triggers the confirmed conflict resolution path.
- All companion-originated rep table rows have `roll20_row_id = 'comp-{uuid}'` — never NULL.

**Dependencies:** Phase 1 schema (all character and rep table columns in final form). No dependency on Tasks 1–5 of this phase, except that the authenticated session is required.

---

### Feature-to-Task Coverage

| Feature | Task(s) |
|---|---|
| U3 — GM Dashboard | Tasks 1 (route), 3 (implementation) |
| U4 — Player Roster | Tasks 1 (route), 4 (implementation) |
| U5 — Character Reassignment | Task 4 |
| U6 — Character List Enrichment | Task 2 |
| U15 — Character Upload | Task 6 |
| U16 — GM Karma Award | Tasks 3 (dashboard host page), 5 (form + action) |

---

### Dependency & Execution Map

**Authoring parallelism** (all can be written simultaneously after Task 1 stubs exist):
- Task 2 — isolated to `/characters` route.
- Task 4 — isolated to `/roster` route.
- Task 6 — isolated to `/upload` route.
- Tasks 3 + 5 — co-authored in the same `/dashboard/+page.server.ts`.

**Execution order (strict):**
1. Phase 1 fully committed (schema migrated, columns added, seeds applied).
2. Task 1 — route stubs + landing redirect.
3. Tasks 2, 4, 6 — parallel (independent routes).
4. Tasks 3 + 5 — together (same dashboard file); Task 5 adds the form action to the file Task 3 creates.

---

### Blocking Items

| # | Item | Owner | Resolution |
|---|---|---|---|
| B1 | Route placement | User | ~~Blocking~~ RESOLVED — both top-level: `/dashboard`, `/roster` |
| B2 | Excel parsing runtime | User | ~~Blocking~~ RESOLVED — SheetJS client-side (Option A) |
| B3 | Staleness threshold | GM | ~~Blocking~~ RESOLVED — 7 days |
| B4 | Player-to-player reassignment | User | ~~Blocking~~ RESOLVED — deferred, no value-add now |
| B5 | Duplicate upload handling | User | ~~Blocking~~ RESOLVED — reject with error message |

---

## Phase 3 — Session & Party Management: The Crown Jewel

**Goal:** Deliver the full in-session GM workflow and the between-session PC management loop: session entity CRUD with continuation model, roster add/remove from any group, need-to-know combat stat view, group-level party treasure, player karma allocation ledger, and milestone progression CRUD.

**Features:** U2 (session roster / party view), U1b (treasure UI), U17 (player karma allocation), U18 (milestone progressions)

**Phase dependency:** Phase 1 schema fully migrated and seeded (all new tables live, `rep_karma.source`/`karma_event_id` columns added, `rep_milestones.source` column added). Phase 2 Task 2 character enrichment complete (stat column names identified — same columns power the session stat view).

---

### Task 1 — Session & Group Treasure Route Scaffolding

**Scope:** Create stub route files for `/sessions`, `/sessions/[id]`, and `/groups/[id]/treasure` with auth guards. No query logic — stubs only.

**Steps:**
a. Create `/sessions/+page.server.ts` stub: call `requireGm(locals, platform)` at the top of `load()`. Return `{ sessions: [] }`.
b. Create `/sessions/+page.svelte` stub: render "Sessions" heading.
c. Create `/sessions/[id]/+page.server.ts` stub: call `requireGm(locals, platform)`. Return `{ session: null, roster: [], available: [] }`.
d. Create `/sessions/[id]/+page.svelte` stub: render "Session Detail" heading.
e. Create `/groups/[id]/treasure/+page.server.ts` stub: call `locals.auth()`. If user is not GM (`is_gm = 0`): query `SELECT id FROM characters WHERE player_id = ? AND group_id = ? AND campaign_id = '9ef60c48-6e85-4363-ac45-6efbbb4d9a5f'` — if 0 rows returned, throw error with status 403. Return `{ group: null, items: [], currency: { gold: 0, silver: 0, copper: 0 } }`.
f. Create `/groups/[id]/treasure/+page.svelte` stub: render "Party Treasure" heading.

**Acceptance Criteria:**
- GET `/sessions` returns 200 for GM; returns auth redirect or 403 for non-GM.
- GET `/sessions/{valid-id}` returns 200 for GM; 403 for non-GM.
- GET `/groups/{group-a-id}/treasure` returns 200 for a player whose character has `group_id = group-a-id`; returns 403 for a player whose characters are all assigned to a different group; returns 403 for unauthenticated.
- No existing routes regress.

**Dependencies:** None — stubs only.

---

### Task 2 — Session CRUD: List, Create, Archive

**Scope:** Implement the `/sessions` list page with create form and archive action. Session entity management only — roster wired in Task 3.

**Steps:**
a. Implement `/sessions/+page.server.ts` `load()`:
   1. Session list query: `SELECT s.id, s.session_number, s.session_date, s.name, s.status, COUNT(sc.character_id) AS roster_count FROM sessions s LEFT JOIN session_characters sc ON sc.session_id = s.id WHERE s.campaign_id = '9ef60c48-6e85-4363-ac45-6efbbb4d9a5f' GROUP BY s.id ORDER BY s.session_number DESC`.
   2. Return `{ sessions }`.

b. Implement `/sessions/+page.svelte`:
   - Session list table: Session # | Name | Date | Roster | Status | Actions (View link → `/sessions/{id}`, Archive button).
   - Inline create form above the table: fields `session_date` (date input, required), `session_name` (text, optional). Submit "Create Session" calls `createSession` action.
   - Archived sessions rendered with a visual distinction (muted opacity or "archived" badge) — still visible, not hidden.

c. Implement form action `createSession` in `/sessions/+page.server.ts`:
   1. Read `session_date` (string, required), `session_name` (string, optional, default empty string).
   2. Validate `session_date` matches `YYYY-MM-DD` format — return `fail(400, { error: 'Invalid date format' })` if not.
   3. Resolve next session number: `SELECT COALESCE(MAX(session_number), 0) + 1 AS next_num FROM sessions WHERE campaign_id = '9ef60c48-...'`. Store as `nextNum`.
   4. Insert new session: `INSERT INTO sessions (id, campaign_id, session_number, session_date, name, notes, status) VALUES (uuid(), '9ef60c48-...', ?, ?, ?, '', 'active')`.
   5. Store `newSessionId` and `nextNum` — used for Task 3 continuation logic executed in the same action body.
   6. Continuation roster copy — see Task 3 step a.
   7. Redirect to `/sessions/{newSessionId}`.

d. Implement form action `archiveSession` in `/sessions/+page.server.ts`:
   1. Read `session_id` from form data. Validate non-empty.
   2. Ownership check: `SELECT id FROM sessions WHERE id = ? AND campaign_id = '9ef60c48-...'`. Return `fail(404, ...)` if not found.
   3. `UPDATE sessions SET status = 'archived' WHERE id = ?`. Redirect to `/sessions`.

[DEV DECISION]: Verify exact column names via `PRAGMA table_info(sessions)` before writing any queries — the schema context states `date TEXT, name TEXT, status TEXT` but Phase 1 DDL may have used `session_date TEXT` and may not have included `name` or `status`. Use `PRAGMA` output as ground truth; update all query references accordingly.

[DEV DECISION]: Session status lifecycle — confirm the complete set of valid `status` values. Recommendation: `'active'` | `'archived'` only. Define as a named constant array at the top of the server file.

**Acceptance Criteria:**
- Session list renders with correct session_number, session_date, name, roster count, and status for all rows.
- Creating a session with a valid date inserts one row with `status = 'active'` and auto-incremented `session_number`; redirects to the new session's detail page.
- `session_date` in an invalid format returns 400 with a descriptive error message — no DB write.
- Archiving a session sets `status = 'archived'`; session remains in the list with visual archived indicator.
- Form action rejects a `session_id` from a different campaign — no DB write.

**Dependencies:** Task 1 stubs. Phase 1 schema fully migrated (`sessions` table exists).

---

### Task 3 — Session Roster Management + Continuation Model

**Scope:** Character picker on `/sessions/[id]` — add/remove characters via `session_characters`; pre-populate new session roster from the prior session's character list.

**Steps:**
a. Continuation model — extend `createSession` action from Task 2 step c, executed after step c.4's `INSERT INTO sessions`:
   1. Query prior session characters: `SELECT sc.character_id FROM session_characters sc WHERE sc.session_id = (SELECT id FROM sessions WHERE campaign_id = '9ef60c48-...' AND session_number = ?)` where `?` = `nextNum - 1`. If `nextNum = 1` (first session ever created), this subquery returns no rows — skip bulk insert.
   2. For each returned `character_id`: `INSERT OR IGNORE INTO session_characters (session_id, character_id) VALUES (?, ?)` using `newSessionId`.
   3. Log count of copied characters to server console.

b. Implement `/sessions/[id]/+page.server.ts` `load()` (replacing Task 1 stub):
   1. Session lookup: `SELECT id, session_number, session_date, name, notes, status FROM sessions WHERE id = ? AND campaign_id = '9ef60c48-...'`. Throw 404 if not found.
   2. Current roster: `SELECT c.id, c.char_name, g.group_name, p.discord_name FROM characters c JOIN session_characters sc ON sc.character_id = c.id LEFT JOIN groups g ON c.group_id = g.id JOIN players p ON c.player_id = p.id WHERE sc.session_id = ? ORDER BY g.group_name, c.char_name`.
   3. Available characters: `SELECT c.id, c.char_name, g.group_name FROM characters c LEFT JOIN groups g ON c.group_id = g.id WHERE c.campaign_id = '9ef60c48-...' AND c.id NOT IN (SELECT character_id FROM session_characters WHERE session_id = ?) ORDER BY g.group_name, c.char_name`.
   4. Return `{ session, roster, available }`.

c. Implement `/sessions/[id]/+page.svelte`:
   - Current roster section: table with `char_name`, `group_name`, `discord_name` (owner), and a "Remove" button per row.
   - Add character section: `<select>` of available characters grouped by `group_name` via `<optgroup>` + "Add to Session" submit button.
   - Stat columns (Task 4) are added in the next task — leave as empty placeholders.

d. Implement form action `addCharacter` in `/sessions/[id]/+page.server.ts`:
   1. Read `character_id` from form data.
   2. Validate campaign membership: `SELECT id FROM characters WHERE id = ? AND campaign_id = '9ef60c48-...'`. Return `fail(400, ...)` if 0 rows.
   3. `INSERT OR IGNORE INTO session_characters (session_id, character_id) VALUES (?, ?)`. Redirect. *(Requires `UNIQUE(session_id, character_id)` constraint on `session_characters` — confirm when Phase 1 DDL is authored.)*

e. Implement form action `removeCharacter` in `/sessions/[id]/+page.server.ts`:
   1. Read `character_id`.
   2. Validate row exists: `SELECT session_id FROM session_characters WHERE session_id = ? AND character_id = ?`. Return `fail(404, ...)` if not found.
   3. `DELETE FROM session_characters WHERE session_id = ? AND character_id = ?`. Redirect.

[DEV DECISION]: Continuation ordering key — prior session resolved by `session_number = nextNum - 1`. Confirm `session_number` (not `session_date`) is the canonical ordering key.

[DEV DECISION]: Archived session immutability — should `addCharacter` and `removeCharacter` be blocked when `session.status = 'archived'`? Recommendation: yes — validate `status = 'active'`; return `fail(400, { error: 'Cannot modify an archived session' })` if not. Confirm before implementing.

**Acceptance Criteria:**
- Creating session N when session N-1 exists: new session's `session_characters` count equals the prior session's count. Verify: `SELECT COUNT(*) FROM session_characters WHERE session_id = {new_id}`.
- Creating session 1 (no prior): roster starts empty — `SELECT COUNT(*) FROM session_characters WHERE session_id = {new_id}` returns 0.
- Adding a character not in the campaign returns 400 — no DB write.
- Adding a character already in the session is idempotent (`INSERT OR IGNORE`) — no error, no duplicate row.
- Removing a character deletes exactly one `session_characters` row; character reappears in the available dropdown on redirect.

**Dependencies:** Task 1 stubs. Task 2 `createSession` action (Task 3 step a extends it). Phase 1 `session_characters` table present.

---

### Task 4 — Party Stat View: Need-to-Know Combat Table

**Scope:** Extend `/sessions/[id]` roster to display initiative, physical CM, and stun CM per rostered character. Schema inspection confirms column names below.

**Steps:**
a. Schema reference (confirmed from `schema.sql`):
   - Initiative: `init_score` (INTEGER). Related: `init_dice`, `init_reaction_mod`, `init_misc_mod`.
   - Physical CM boxes (11 columns, INTEGER 0/1): `cm_physical_l1`, `cm_physical_l2`, `cm_physical_m1`, `cm_physical_m2`, `cm_physical_m3`, `cm_physical_s1`, `cm_physical_s2`, `cm_physical_s3`, `cm_physical_s4`, `cm_physical_d`, `cm_physical_u`. Define `CM_PHYSICAL_COLS` as this list.
   - Stun CM boxes (11 columns, INTEGER 0/1): `cm_stun_l1`, `cm_stun_l2`, `cm_stun_m1`, `cm_stun_m2`, `cm_stun_m3`, `cm_stun_s1`, `cm_stun_s2`, `cm_stun_s3`, `cm_stun_s4`, `cm_stun_d`, `cm_stun_u`. Define `CM_STUN_COLS` as this list.
   - Edge does not exist in this game system — no column in schema.
   - Mental CM (`cm_mental_*`, 10 columns) exists in the schema but is intentionally excluded from the session stat view — mental damage cannot reduce a character's condition in this system.

b. Extend roster query in `/sessions/[id]/+page.server.ts` `load()` (from Task 3 step b.2) to include all `cm_physical_*` columns, all `cm_stun_*` columns, `init_score`, and `c.synced_at`. Select explicitly by name — no `SELECT *`.

c. Compute derived stat values server-side before returning page data:
   - `cm_physical_filled`: count of `CM_PHYSICAL_COLS` columns equal to `1`.
   - `cm_physical_max`: count of `CM_PHYSICAL_COLS` columns that are NOT NULL.
   - `cm_stun_filled` and `cm_stun_max`: same for `CM_STUN_COLS`.
   - `initiative_display`: direct value of `init_score`. NULL renders as `null` — handled in template.
   - `is_stale`: `Date.parse(synced_at) < Date.now() - STALE_THRESHOLD_DAYS * 86_400_000` — reuse `STALE_THRESHOLD_DAYS = 7` constant from Phase 2 Task 2.

d. Update `/sessions/[id]/+page.svelte` roster table:
   - Columns: Character | Group | Owner | Initiative | CM Phys | CM Stun | Last Sync.
   - CM cell format: `{filled}/{max}`. Apply CSS utility classes: 0–33% filled → `cm-safe`; 34–66% → `cm-warn`; 67–100% → `cm-critical`.
   - NULL stat cell renders as "—" — guard with `{value ?? '—'}`.
   - "Last Sync" cell: inline relative-time calculation using `Date.now() - Date.parse(synced_at)`. Leave `// TODO: replace with shared relative-time helper in Phase 5` comment.

[DEV DECISION]: If `init_score` is NULL for all characters (e.g., initiative is only derived at roll time in Roll20 and never synced), display initiative as "—" and add a code comment noting the limitation.

**Acceptance Criteria:**
- Stat table renders for all rostered characters.
- CM fractions are computed correctly from the 0/1 box columns — a character with 3 of 10 physical CM boxes filled shows `3/10`.
- CSS class `cm-critical` is applied when `filled / max >= 0.67`.
- NULL stat values render "—" — no runtime template error.
- The roster stat table does not break when the session has zero characters.

**Dependencies:** Task 3 roster query (Task 4 extends, not replaces, it). Phase 2 Task 2 `PRAGMA table_info(characters)` output (reuse column discovery from that task).

---

### Task 5 — Party Treasure UI: Group Treasure View & Edit (U1b)

**RESOLVED (BD-1):** Option A — separate `group_currency` table. `group_treasure` stores named items. `group_currency` stores party funds per group: `id TEXT PK`, `group_id TEXT NOT NULL UNIQUE REFERENCES groups(id)`, `gold INTEGER NOT NULL DEFAULT 0` (gold crowns), `silver INTEGER NOT NULL DEFAULT 0` (silver stags), `copper INTEGER NOT NULL DEFAULT 0` (copper pennies), `updated_at TEXT DEFAULT datetime('now')`. DDL added to Phase 1 Task 5 schema.sql.

**Scope:** Implement `/groups/[id]/treasure` — group treasure items and party currency (gold crowns, silver stags, copper pennies), view and edit. Accessible to group members and GM.

**Steps:**
a. Implement `/groups/[id]/treasure/+page.server.ts` `load()` (replacing Task 1 stub):
   1. Group validation: `SELECT id, group_name FROM groups WHERE id = ? AND campaign_id = '9ef60c48-...'`. Throw 404 if not found.
   2. Re-apply auth: if `is_gm = 0`, verify `SELECT id FROM characters WHERE player_id = ? AND group_id = ? AND campaign_id = '9ef60c48-...'` — throw 403 if 0 rows.
   3. Treasure items: `SELECT id, item_name, quantity, owner_character_id, description FROM group_treasure WHERE group_id = ? ORDER BY item_name ASC`.
   4. Owner name lookup: `SELECT id, char_name FROM characters WHERE group_id = ?` — build in-memory map `{ [char_id]: char_name }` for owner cell rendering.
   5. Currency: `SELECT COALESCE(gold, 0) AS gold, COALESCE(silver, 0) AS silver, COALESCE(copper, 0) AS copper FROM group_currency WHERE group_id = ?`. Return `{ gold: 0, silver: 0, copper: 0 }` if no row.
   6. Return `{ group, items, ownerMap, currency }`.

b. Implement `/groups/[id]/treasure/+page.svelte`:
   - Currency section: display gold crowns (GC), silver stags (SS), copper pennies (CP) as three labeled values. Inline edit: three number inputs (`gold`, `silver`, `copper`) + "Update Currency" submit → `updateCurrency` action.
   - Item table: Item Name | Qty | Owner | Description | Actions (Remove button per row).
   - Add item form below table: `item_name` (text, required), `quantity` (integer, min 1, default 1), `owner` `<select>` (options: "Party" → empty string → NULL on server; then each `char_name` by id), `description` (textarea, optional). Submit "Add Item" → `addItem` action.

c. Implement form actions in `/groups/[id]/treasure/+page.server.ts`:
   - `addItem`:
     1. Auth re-check (same as `load()`).
     2. Validate `item_name` non-empty; `quantity` is integer ≥ 1.
     3. Resolve `owner_character_id`: if form value is empty → NULL. If non-empty → validate: `SELECT id FROM characters WHERE id = ? AND group_id = ?` — return `fail(400, ...)` if 0 rows.
     4. `INSERT INTO group_treasure (id, group_id, item_name, quantity, owner_character_id, description, created_at, updated_at) VALUES (uuid(), ?, ?, ?, ?, ?, datetime('now'), datetime('now'))`. Redirect.
   - `removeItem`:
     1. Auth re-check.
     2. Read `item_id`. Validate: `SELECT id FROM group_treasure WHERE id = ? AND group_id = ?`. Return `fail(404, ...)` if not found.
     3. `DELETE FROM group_treasure WHERE id = ?`. Redirect.
   - `updateCurrency`:
     1. Auth re-check.
     2. Read `gold`, `silver`, `copper` (integers, required, each ≥ 0). Return `fail(400, ...)` if any is negative or non-integer.
     3. `INSERT OR REPLACE INTO group_currency (id, group_id, gold, silver, copper, updated_at) VALUES (COALESCE((SELECT id FROM group_currency WHERE group_id = ?), uuid()), ?, ?, ?, ?, datetime('now'))`. Redirect.

[DEV DECISION]: Item edit (update quantity/description) — implement `editItem` form action with hidden `item_id` per row now, or defer to Phase 5. Recommendation: implement `editItem` in this task (a 2-field form per row is trivial and avoids a Phase 5 revisit).

[DEV DECISION]: Remove item permissions — all group members can add and remove, or GM-only for removes? Spec says "accessible to all group members." Recommendation: all group members can add and remove. Confirm before implementing the `removeItem` auth check.

**Acceptance Criteria:**
- Page renders group name, currency balances (gold crowns, silver stags, copper pennies), and item list for authenticated group member.
- `addItem` creates a `group_treasure` row with correct `group_id`. Item appears in list on redirect.
- `owner_character_id` is NULL when "Party" is selected; is the selected character's id when an owner is chosen.
- `addItem` rejects an `owner_character_id` not belonging to this group — 400, no DB write.
- `removeItem` deletes the correct row; attempting to delete an item from a different group returns 404.
- `updateCurrency` stores the new gold/silver/copper values; the page displays the updated balances after redirect. All-zero values are accepted.
- A player with no character in this group receives 403.

**Dependencies:** Task 1 stubs. Phase 1 Task 5 (`group_treasure` and `group_currency` tables). Phase 1 Task 3 (groups seeded).

---

### Task 6 — Character Detail: Player Karma Allocation Ledger (U17)

**Scope:** Extend `/characters/[id]` with a Karma section — balance summary, `rep_karma` ledger with source badges, campaign event reference panel, and spend form.

**Steps:**
a. Extend `/characters/[id]/+page.server.ts` `load()` with karma queries scoped to character `id`:
   1. Auth gate: if `is_gm = 0`, validate `SELECT player_id FROM characters WHERE id = ?` returns `player_id = current_user.id`. Throw 403 if character belongs to another player.
   2. Karma ledger: `SELECT rk.id, rk.karma_event, rk.karma_amount, rk.source, ke.event_name, ke.date_awarded FROM rep_karma rk LEFT JOIN karma_events ke ON ke.id = rk.karma_event_id WHERE rk.character_id = ? ORDER BY ke.date_awarded ASC NULLS LAST, rk.id ASC`.
   3. Balance aggregates (parallel via `Promise.all()`):
      - `SELECT COALESCE(SUM(karma_amount), 0) AS earned FROM rep_karma WHERE character_id = ? AND karma_amount > 0`
      - `SELECT COALESCE(SUM(karma_amount), 0) AS spent FROM rep_karma WHERE character_id = ? AND karma_amount < 0`
   4. Campaign event reference: `SELECT event_name, karma_amount FROM karma_events WHERE campaign_id = '9ef60c48-...' ORDER BY date_awarded ASC NULLS LAST`.
   5. Return `{ ...(existing data), karmaLedger, earned, spent, balance: earned + spent, campaignEvents }`.

b. Add Karma section to `/characters/[id]/+page.svelte`:
   - Balance summary bar: "Earned: {earned} | Spent: {Math.abs(spent)} | Balance: {balance}".
   - Karma ledger table: Event | Amount | Source badge | Date. Source badges: `'roll20'` → "Roll20"; `'seed'` → "Imported"; `'companion'` → "In-app". Amount: positive values styled in green `+{n}`, negative in red `{n}`.
   - Campaign events reference panel (collapsed by default using `<details>`): table of `event_name` and `karma_amount` for all campaign events — no interactive elements.
   - Spend form (conditionally rendered `{#if balance > 0}`): text input `description` (label "Description", required), number input `amount` (label "Amount to Spend", positive integer, min 1, max `balance`). Submit "Spend Karma" → `spendKarma` action.

c. Implement form action `spendKarma` in `/characters/[id]/+page.server.ts`:
   1. Auth gate: allow if `player_id = current_user.id` OR `is_gm = 1`. Return `fail(403, ...)` otherwise.
   2. Read `description` (string, required, non-empty), `amount` (integer, required, ≥ 1). User enters a positive number — action negates it.
   3. Balance check: `SELECT COALESCE(SUM(karma_amount), 0) AS balance FROM rep_karma WHERE character_id = ?`. If `amount > balance`, return `fail(400, { error: 'Insufficient karma balance' })` — no DB write.
   4. Generate `roll20_row_id = 'comp-' + crypto.randomUUID()`.
   5. `INSERT INTO rep_karma (id, character_id, roll20_row_id, karma_event, karma_amount, source, karma_event_id) VALUES (uuid(), ?, ?, ?, ?, 'companion', NULL)` — `karma_amount` = `-amount`.
   6. Redirect to `/characters/{id}`.

[DEV DECISION]: `characters` table has `karma_good`, `karma_used`, `karma_total`, `karma_pool` columns from Roll20 sync. These are not used for the companion karma balance — `rep_karma` SUM is the source of truth. Confirm whether to show Roll20 karma fields as a read-only reference aside or hide them entirely.

[DEV DECISION]: Karma section placement on `/characters/[id]` — tab, `<details>` accordion, or full-page `<section id="karma">`. Recommendation: `<section id="karma">` (visible on scroll, no JS tab state). Confirm, as this decision also applies to Task 7 (milestones section).

**Acceptance Criteria:**
- Balance = `SUM(karma_amount)` from `rep_karma` — not from `karma_good` / `karma_total`.
- Ledger lists all `rep_karma` rows for the character with correct Source badges.
- `spendKarma` with valid amount creates one `rep_karma` row: `karma_amount = -amount`, `source = 'companion'`, `roll20_row_id = 'comp-{uuid}'` (never NULL), `karma_event_id = NULL`.
- `spendKarma` with `amount > balance` returns 400 — no DB write.
- `spendKarma` called with another player's character ID returns 403 — no DB write.
- Spend form is not rendered when `balance = 0`.

**Dependencies:** Phase 2 character detail page exists and is extensible. Phase 1 `karma_events` table and `rep_karma.source`, `rep_karma.karma_event_id` columns present. Phase 2 Task 5 (karma events seeded or created via GM award form — ledger will be empty otherwise but page should still render).

---

### Task 7 — Character Detail: Milestone Progression CRUD (U18)

**Scope:** Extend `/characters/[id]` with a Milestones section — add, edit, and delete `rep_milestones` rows with `source = 'companion'`. Roll20-synced rows display read-only.

**Steps:**
a. Extend `/characters/[id]/+page.server.ts` `load()` with milestones query:
   1. `SELECT id, milestone_trial, milestone_tier1, milestone_tier2, milestone_tier3, milestone_current, source FROM rep_milestones WHERE character_id = ? ORDER BY id ASC`.
   2. Auth gate: reuse the same check as Task 6 step a.1. Return companion and Roll20 rows; template segregates by `source`.
   3. Return `{ ...(existing data), milestones }`.

b. Add Milestones section to `/characters/[id]/+page.svelte`:
   - Milestones table: Progression Name (`milestone_trial`) | Tier 1 | Tier 2 | Tier 3 | Active Tier | Actions.
   - `milestone_current` mapping: 0 → "None", 1 → "Tier 1", 2 → "Tier 2", 3 → "Tier 3".
   - `source = 'roll20'` rows: plain text for all 5 data cells; no action buttons; muted "Synced from Roll20" label.
   - `source = 'companion'` rows: "Edit" and "Delete" buttons. "Edit" sets per-row `$state isEditing = true`, rendering 5 inline inputs + `milestone_current` `<select>` (options 0–3 with display labels) + "Save" (submits `editMilestone`) + "Cancel" (resets state).
   - Add row form at section bottom: same 5 fields. Submit "Add Progression" → `addMilestone` action.

c. Implement form action `addMilestone` in `/characters/[id]/+page.server.ts`:
   1. Auth gate: `player_id = current_user.id` OR `is_gm = 1`. Return `fail(403, ...)` otherwise.
   2. Read `milestone_trial` (required, non-empty), `milestone_tier1`, `milestone_tier2`, `milestone_tier3` (optional strings), `milestone_current` (integer, default 0).
   3. Validate `milestone_current` ∈ `[0, 1, 2, 3]` — return `fail(400, { error: 'Active tier must be 0–3' })` if not.
   4. Generate `roll20_row_id = 'comp-' + crypto.randomUUID()`.
   5. `INSERT INTO rep_milestones (id, character_id, roll20_row_id, milestone_trial, milestone_tier1, milestone_tier2, milestone_tier3, milestone_current, source) VALUES (uuid(), ?, ?, ?, ?, ?, ?, ?, 'companion')`. Redirect.

d. Implement form action `editMilestone` in `/characters/[id]/+page.server.ts`:
   1. Auth gate: same as `addMilestone`.
   2. Read `milestone_id` (hidden form field — the `rep_milestones.id`).
   3. Ownership + source check: `SELECT id, source FROM rep_milestones WHERE id = ? AND character_id = ?`. Return `fail(404, ...)` if not found. Return `fail(400, { error: 'Cannot edit Roll20-synced milestones' })` if `source = 'roll20'`.
   4. Read and validate 5 fields (same as `addMilestone`).
   5. `UPDATE rep_milestones SET milestone_trial = ?, milestone_tier1 = ?, milestone_tier2 = ?, milestone_tier3 = ?, milestone_current = ? WHERE id = ?`. Redirect.

e. Implement form action `deleteMilestone` in `/characters/[id]/+page.server.ts`:
   1. Auth gate: same as `addMilestone`.
   2. Read `milestone_id`.
   3. Ownership + source check: `SELECT id, source FROM rep_milestones WHERE id = ? AND character_id = ?`. Return `fail(404, ...)` if not found. Return `fail(400, { error: 'Cannot delete Roll20-synced milestones' })` if `source = 'roll20'`.
   4. `DELETE FROM rep_milestones WHERE id = ?`. Redirect.

[DEV DECISION]: Active tier column name is `milestone_current` (confirmed from schema context — `rep_milestones` has this column). Do NOT use `active_tier` — that was a draft name in a superseded Phase 1 spec for a separate `character_milestones` table. Verify via `PRAGMA table_info(rep_milestones)` before implementation.

[DEV DECISION]: Player-managed = players can delete their own milestone rows. Confirm this is intentional. Recommendation: add a JS confirmation dialog on the Delete button (`onclick="return confirm('Delete this progression? This cannot be undone.')"`) to prevent accidental loss.

**Acceptance Criteria:**
- Milestones section renders all `rep_milestones` rows for the character; `source = 'companion'` rows show Edit/Delete; `source = 'roll20'` rows show "Synced from Roll20" label, no action buttons.
- `addMilestone` inserts a new row: `source = 'companion'`, `roll20_row_id = 'comp-{uuid}'` (never NULL), correct `character_id`.
- `editMilestone` updates the correct row; editing a row belonging to a different character returns 404; editing a `source = 'roll20'` row returns 400.
- `deleteMilestone` deletes the correct companion row; deleting another character's row returns 404; deleting a Roll20 row returns 400.
- `milestone_current` values outside `[0, 1, 2, 3]` rejected with 400 — no DB write.
- Players cannot modify milestones for characters they don't own (403).

**Dependencies:** Phase 2 character detail page exists and is extensible. Phase 1 Task 2 (`rep_milestones.source` column added via `migrate-add-columns.ts` must be present). Co-authored with Task 6 in the same `/characters/[id]/+page.server.ts` file.

---

### Feature-to-Task Coverage

| Feature | Task(s) |
|---|---|
| U2 — Session Roster / Party View | Task 1 (scaffolding), Task 2 (session CRUD), Task 3 (roster + continuation), Task 4 (stat view) |
| U1b — Treasure UI | Task 1 (group treasure route scaffolding), Task 5 (implementation) |
| U17 — Player Karma Allocation | Task 6 |
| U18 — Milestone Progressions | Task 7 |

---

### Dependency & Execution Map

**Authoring parallelism** (after Task 1 stubs exist):
- Tasks 2 → 3 → 4: tightly coupled sequential chain — all target `/sessions` and `/sessions/[id]`.
- Task 5: isolated to `/groups/[id]/treasure` — fully independent of Tasks 2–4.
- Tasks 6 → 7: co-authored in `/characters/[id]/+page.server.ts` and `/characters/[id]/+page.svelte` — sequential within same files, independent of Tasks 2–5.

**Execution order (strict):**
1. Task 1 — route stubs (unblocks all other tasks)
2. Tasks 2 → 3 → 4 — sequential session chain
3. Task 5 — independent
4. Tasks 6 → 7 — sequential; independent of session tasks

---

### Blocking Items

| ID | Decision | Owner | Blocking Task |
|---|---|---|---|
| BD-1 | Treasure schema | GM | ~~Blocking~~ RESOLVED — Option A: separate `group_currency` table. Columns: `gold INTEGER NOT NULL DEFAULT 0` (gold crowns), `silver INTEGER NOT NULL DEFAULT 0` (silver stags), `copper INTEGER NOT NULL DEFAULT 0` (copper pennies). DDL added to Phase 1 Task 5. |
| BD-2 | `sessions` column names | Dev | ~~Blocking~~ DOWNGRADED to DEV DECISION — developer adds `name TEXT` and `status TEXT NOT NULL DEFAULT 'active'` to Phase 1 `sessions` DDL. No user input needed. |

