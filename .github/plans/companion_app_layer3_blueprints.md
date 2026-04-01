# Layer 3 — Phase 0: Roll20 Sheet Updates — Technical Blueprints

**Files touched:** `sheet.html` (HTML + Sheet Worker), `sheet.css`

---

## Blueprint 0.1 — Money Fields: Gear Tab HTML + CSS

### sheet.html — Insertion

**Anchor:** Line 1057 `<div class="sheet-tab-panel sheet-tab-panel-gear">`, before line 1058 `<!-- Region: Armor Panel -->`

Insert immediately after line 1057:

```html
    <!-- Region: Money -->
    <h3 class="sheet-section-title">Money</h3>
    <div class="sheet-money-row">
      <label>Gold:</label>
      <input type="number" name="attr_money_gold" value="0">
      <label>Silver:</label>
      <input type="number" name="attr_money_silver" value="0">
      <label>Copper:</label>
      <input type="number" name="attr_money_copper" value="0">
    </div>
```

**Field name table:**

| HTML `name`         | scalarFields entry   |
|---------------------|----------------------|
| `attr_money_gold`   | `'money_gold'`       |
| `attr_money_silver` | `'money_silver'`     |
| `attr_money_copper` | `'money_copper'`     |

### sheet.css — Insertion

**Anchor:** After closing `}` of `.sheet-tab-panel-gear .repitem .sheet-btn-attack` block (~line 1687), before `/* === SECTION 14: BIO TAB ===*/` (~line 1689).

```css
/* ===================================================
 * SECTION 13b: GEAR TAB — MONEY ROW
 * =================================================== */

.sheet-money-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 2px solid #5f5f5f;
  background-color: #f9f9f9;
  margin-bottom: 20px;
  flex-wrap: nowrap;
  overflow-x: auto;
}

.sheet-money-row label {
  font-size: 12px;
  font-weight: bold;
  color: #555555;
  white-space: nowrap;
}

.sheet-money-row input[type="number"] {
  width: 70px;
  text-align: center;
  font-size: 13px;
}
```

Pattern source: identical structure to `.sheet-karma-row` (SECTION 8, ~line 544); only `width: 70px` differs (vs karma's 50px — three fields need slightly more room).

---

## Blueprint 0.2 — Remove 20 Questions: Bio Tab HTML + scalarFields

### sheet.html — Deletion

**Delete lines 1214–1254** (blank separator + all 20 label+textarea pairs).

Anchor check:
- Line 1213: `      <textarea name="attr_char_notes" rows="6"></textarea>` — keep
- Line 1214: blank line — delete (first line of range)
- Line 1215: `      <label>Q1: Who is your biggest rival and why?</label>` — delete
- Line 1254: `      <textarea name="attr_bio_q20" rows="3"></textarea>` — delete (last line of range)
- Line 1255: `    </div>` (closing `.sheet-bio-section`) — keep

After deletion, line 1213 is directly followed by `    </div>`. Blueprints 0.3 and 0.4 insert between them.

**No CSS changes.** Dead `.sheet-session0-block` rules in SECTION 14 do not affect layout; leave in place.

### sheet.html Sheet Worker — scalarFields Deletion

**Delete lines 456–458** (3 lines):

```js
    'bio_q01', 'bio_q02', 'bio_q03', 'bio_q04', 'bio_q05', 'bio_q06', 'bio_q07', 'bio_q08',
    'bio_q09', 'bio_q10', 'bio_q11', 'bio_q12', 'bio_q13', 'bio_q14', 'bio_q15', 'bio_q16',
    'bio_q17', 'bio_q18', 'bio_q19', 'bio_q20',
```

**Note:** Blueprint 0.5 replaces the entire sync handler, which subsumes both this deletion and the money-field addition. Apply 0.2 and 0.5 together — do not do a partial scalarFields edit and then a full handler replacement separately; just do the full replacement in Blueprint 0.5 with the correct final scalarFields.

---

## Blueprint 0.3 — Karma Ledger: Bio Tab HTML + CSS

### sheet.html — Insertion

**Anchor:** After line 1213 (`<textarea name="attr_char_notes" rows="6"></textarea>`) once Blueprint 0.2 deletions are applied (i.e., the 20Q block is gone). Insert before the `    </div>` that closes `.sheet-bio-section`.

```html
      <h3 class="sheet-section-title">Karma Ledger</h3>
      <div class="sheet-karma-log-header">
        <span class="sheet-hdr-karma-event">Event</span>
        <span class="sheet-hdr-karma-amount">Amount</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
      <fieldset class="repeating_karma">
        <input type="text" name="attr_karma_event" placeholder="Event" class="sheet-karma-log-event">
        <input type="number" name="attr_karma_amount" value="0" class="sheet-karma-log-amount">
      </fieldset>
```

**Note on `.sheet-hdr-spacer`:** Already defined globally in at least the mutations and contacts section headers. Do not redefine — reuse the existing rule.

### sheet.css — Insertion

**Anchor:** End of SECTION 14, after closing `}` of `.sheet-tab-panel-bio .sheet-session0-block textarea` block (~line 1745), before `/* === SECTION 20: SHEET ROOT ===*/` (~line 1747).

```css
/* --- Bio Tab: Karma Ledger repeating section --- */
.sheet-karma-log-header {
  display: flex;
  align-items: center;
  padding: 2px 6px;
  gap: 6px;
  background-color: #f2f2f2;
  border-bottom: 2px solid #5f5f5f;
  font-size: 12px;
  font-weight: bold;
}

.sheet-hdr-karma-event  { flex: 1 1 auto; }
.sheet-hdr-karma-amount { flex: 0 0 70px; text-align: center; }

/* Bio repeating row base — shared by karma and milestones rows */
.sheet-tab-panel-bio .repitem {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 2px 6px;
}

.sheet-karma-log-event  { flex: 1 1 auto; min-width: 0; }
.sheet-karma-log-amount { flex: 0 0 70px; text-align: center; }
```

---

## Blueprint 0.4 — Milestones: Bio Tab HTML + CSS

### sheet.html — Insertion

**Anchor:** Directly after the closing `</fieldset>` of `repeating_karma` (end of Blueprint 0.3 insertion block), before the `    </div>` closing `.sheet-bio-section`.

```html
      <h3 class="sheet-section-title">Milestones</h3>
      <div class="sheet-milestones-header">
        <span class="sheet-hdr-milestone-trial">Trial</span>
        <span class="sheet-hdr-milestone-tier1">Tier 1</span>
        <span class="sheet-hdr-milestone-tier2">Tier 2</span>
        <span class="sheet-hdr-milestone-tier3">Tier 3</span>
        <span class="sheet-hdr-milestone-current">Cur</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
      <fieldset class="repeating_milestones">
        <input type="text" name="attr_milestone_trial" placeholder="Trial Name" class="sheet-milestone-trial">
        <input type="text" name="attr_milestone_tier1" placeholder="Tier 1" class="sheet-milestone-tier1">
        <input type="text" name="attr_milestone_tier2" placeholder="Tier 2" class="sheet-milestone-tier2">
        <input type="text" name="attr_milestone_tier3" placeholder="Tier 3" class="sheet-milestone-tier3">
        <input type="number" name="attr_milestone_current" value="0" min="0" max="3" class="sheet-milestone-current">
      </fieldset>
```

### sheet.css — Insertion

**Anchor:** Immediately after the karma ledger CSS block from Blueprint 0.3 (before `/* === SECTION 20 ===*/`).

```css
/* --- Bio Tab: Milestones repeating section --- */
.sheet-milestones-header {
  display: flex;
  align-items: center;
  padding: 2px 6px;
  gap: 6px;
  background-color: #f2f2f2;
  border-bottom: 2px solid #5f5f5f;
  font-size: 12px;
  font-weight: bold;
  margin-top: 12px;
}

/* Five-column layout: trial grows, tiers fixed, current narrow */
.sheet-hdr-milestone-trial   { flex: 1 1 auto; }
.sheet-hdr-milestone-tier1,
.sheet-hdr-milestone-tier2,
.sheet-hdr-milestone-tier3   { flex: 0 0 160px; }
.sheet-hdr-milestone-current { flex: 0 0 50px; text-align: center; }

.sheet-milestone-trial   { flex: 1 1 auto; min-width: 0; }
.sheet-milestone-tier1,
.sheet-milestone-tier2,
.sheet-milestone-tier3   { flex: 0 0 160px; min-width: 0; }
.sheet-milestone-current { flex: 0 0 50px; text-align: center; }
```

**Field name table:**

| HTML `name`               | scalarFields | repeating_milestones row field |
|---------------------------|--------------|-------------------------------|
| `attr_milestone_trial`    | —            | `milestone_trial`              |
| `attr_milestone_tier1`    | —            | `milestone_tier1`              |
| `attr_milestone_tier2`    | —            | `milestone_tier2`              |
| `attr_milestone_tier3`    | —            | `milestone_tier3`              |
| `attr_milestone_current`  | —            | `milestone_current`            |

---

## Blueprint 0.5 — Sync Handler: Counter/Latch Rewrite

**File:** `sheet.html` — Sheet Worker block (`<script type="text/worker">`)

**Scope:** Replace lines 423–507 in their entirety (entire `on('clicked:btn_sync_db', ...)` handler). Full replacement is cleaner than patching the nested callback structure.

---

### Updated `scalarFields` — Final Complete List

Current lines 428–459, with two changes:
1. **Remove** lines 456–458 (`bio_q01`–`bio_q20`)
2. **Add** after `'essence_total'` (last entry before `];` once bio_q lines are removed):

```js
    'money_gold', 'money_silver', 'money_copper',
```

All other entries remain identical.

---

### SECTIONS Lookup Table

```js
var SECTIONS = {
  skills:       ['skill_name', 'skill_linked_attr', 'skill_general', 'skill_spec',
                 'skill_base', 'skill_foci', 'skill_misc', 'skill_total'],
  mutations:    ['mutation_name', 'mutation_level', 'mutation_essence',
                 'mutation_bp_cost', 'mutation_effect'],
  adept_powers: ['power_name', 'power_level', 'power_pp_cost',
                 'power_pp_cost_value', 'power_effect'],
  spells:       ['spell_name', 'spell_force', 'spell_drain'],
  foci:         ['focus_name', 'focus_type', 'focus_force', 'focus_bonded', 'focus_notes'],
  weapons:      ['weapon_name', 'weapon_type', 'weapon_modifiers', 'weapon_power',
                 'weapon_damage', 'weapon_conceal', 'weapon_reach', 'weapon_ep',
                 'weapon_range_short', 'weapon_range_medium',
                 'weapon_range_long', 'weapon_range_extreme'],
  equipment:    ['equip_name', 'equip_description', 'equip_ep'],
  contacts:     ['contact_name', 'contact_info', 'contact_level'],
  karma:        ['karma_event', 'karma_amount'],
  milestones:   ['milestone_trial', 'milestone_tier1', 'milestone_tier2',
                 'milestone_tier3', 'milestone_current'],
};
```

SECTIONS key = `payload.repeating` key = Roll20 section name suffix.
e.g., key `'adept_powers'` → section `'repeating_adept_powers'` → `payload.repeating.adept_powers`

---

### Counter/Latch Pattern — Complete Pseudocode

```
on('clicked:btn_sync_db', function() {

  setAttrs({ sync_status: 'Syncing…' })

  // ── Shared state (closed over by all 11 callbacks) ──────────────────────
  var payload = {
    campaign_db_id:    null,
    char_db_id:        null,
    sync_version_from: 0,
    scalars:           {},
    repeating:         {},
  }
  var remaining = 11   // 10 sections + 1 scalar getAttrs

  // ── Completion latch ─────────────────────────────────────────────────────
  function proceed() {
    remaining -= 1
    if (remaining > 0) { return }

    // All 11 callbacks resolved — safety checks then fire
    if (!payload.campaign_db_id) {
      setAttrs({ sync_status: 'Sync failed — no campaign ID set' })
      return
    }
    if (!SYNC_PROXY_URL) {
      setAttrs({ sync_status: 'Sync skipped — no proxy URL configured' })
      return
    }

    fetch(SYNC_PROXY_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    })
    .then(function(res) { return res.json() })
    .then(function(response) {
      setAttrs({
        char_db_id:        payload.char_db_id || response.char_db_id,
        char_sync_version: response.sync_version.toString(),
        sync_status:       'Synced ✓ — ' + new Date().toLocaleString(),
      })
    })
    .catch(function(err) {
      console.error('Sync failed:', err)
      setAttrs({ sync_status: 'Sync failed — check console' })
    })
  }

  // ── Callback 1/11: Scalar getAttrs ───────────────────────────────────────
  getAttrs(scalarFields, function(attrs) {
    payload.campaign_db_id    = attrs['campaign_db_id']
    payload.char_db_id        = attrs['char_db_id'] || null
    payload.sync_version_from = parseInt(attrs['char_sync_version'], 10) || 0

    scalarFields.forEach(function(f) {
      if (f === 'campaign_db_id' || f === 'char_db_id' || f === 'char_sync_version') { return }
      payload.scalars[f] = attrs[f]
    })

    proceed()
  })

  // ── Callbacks 2–11: 10 repeating sections (all launched in parallel) ─────
  Object.keys(SECTIONS).forEach(function(key) {
    var sectionName = 'repeating_' + key
    var fields      = SECTIONS[key]

    getSectionIDs(sectionName, function(ids) {

      if (ids.length === 0) {
        payload.repeating[key] = []
        proceed()
        return
      }

      // Build flat attr key list: "repeating_{section}_{rowId}_{field}" × every (id, field)
      var flatKeys = []
      ids.forEach(function(id) {
        fields.forEach(function(f) {
          flatKeys.push(sectionName + '_' + id + '_' + f)
        })
      })

      getAttrs(flatKeys, function(rowAttrs) {
        payload.repeating[key] = ids.map(function(id) {
          var row = { roll20_row_id: id }
          fields.forEach(function(f) {
            row[f] = rowAttrs[sectionName + '_' + id + '_' + f] || ''
          })
          return row
        })
        proceed()
      })

    })
  })

})  // end on('clicked:btn_sync_db')
```

---

### Implementation Notes

| # | Note |
|---|------|
| 1 | **Closure safety:** `remaining` and `payload` live in the outer handler scope. All 11 callbacks share the same references. |
| 2 | **Roll20 attr key format:** `"repeating_skills_-NxYz123_skill_name"` — build with `sectionName + '_' + id + '_' + f`. |
| 3 | **`roll20_row_id`:** Always include in every row object. It's the raw Roll20 hash (e.g., `"-NxYz123abc"`); the companion app uses it for repeating-row upsert deduplication. |
| 4 | **Empty string default:** Use `|| ''` for all row field values. Do not use `null` or `undefined` — consistent string types simplify companion app ingestion. |
| 5 | **`char_db_id` in then-handler:** Use `payload.char_db_id || response.char_db_id` (not `attrs.char_db_id` — `attrs` is out of scope in the refactored closure). |
| 6 | **`Object.keys` + `forEach`:** Roll20 Sheet Workers do not support `for...of`. Use `Object.keys(SECTIONS).forEach(function(key) { ... })`. |
| 7 | **`remaining` initial value:** Must equal number of `getSectionIDs` calls + 1 for scalar `getAttrs`. Currently 11. If a section is added later, increment `remaining`. |

---

## Bio Tab Final HTML Structure (post all changes)

> **Note:** All line numbers throughout this document reference the original `sheet.html` and `sheet.css` before any blueprint changes are applied. Use the content-based anchors (quoted surrounding lines) during execution, not raw line numbers.

```
<div class="sheet-tab-panel sheet-tab-panel-bio">
  <div class="sheet-bio-section">
    <label>Description</label>
    <textarea name="attr_char_description" rows="6"></textarea>
    <label>Notes</label>
    <textarea name="attr_char_notes" rows="6"></textarea>

    <h3 class="sheet-section-title">Karma Ledger</h3>
    <div class="sheet-karma-log-header">...</div>
    <fieldset class="repeating_karma">...</fieldset>

    <h3 class="sheet-section-title">Milestones</h3>
    <div class="sheet-milestones-header">...</div>
    <fieldset class="repeating_milestones">...</fieldset>
  </div>
</div>
```

## Implementation Order

| Step | Blueprint | File(s) | Action |
|------|-----------|---------|--------|
| 1 | 0.1 | sheet.html, sheet.css | Insert money row in Gear tab |
| 2 | 0.2 | sheet.html | Delete bio 20Q HTML (lines 1214–1254) |
| 3 | 0.3 | sheet.html, sheet.css | Insert karma ledger section + CSS |
| 4 | 0.4 | sheet.html, sheet.css | Insert milestones section + CSS |
| 5 | 0.5 | sheet.html (worker) | Replace sync handler lines 423–507 wholesale |

Steps 1–4 are HTML/CSS only. Step 5 is always last — it includes the final scalarFields with money added and bio_q removed.

---


---

# Layer 3 — Phase 1: Scaffold + Schema + Seed Utility — Technical Blueprints

---

## Blueprint 1.1 — Project Scaffold

### Directory Tree (post Task 1 + Task 3 + Task 5)

```
companion/
├── .dev.vars                        # CF Pages local secrets — GITIGNORED
├── .gitignore                       # companion-local (add .dev.vars)
├── package.json
├── svelte.config.js
├── tsconfig.json
├── vite.config.ts
├── wrangler.toml
├── db/
│   ├── .gitkeep
│   └── schema.sql                   # Task 3 — DDL source of truth
├── scripts/
│   ├── .gitkeep
│   ├── migrate.ts                   # Task 3.6 — execute schema.sql
│   └── seed.ts                      # Task 5 — parse Excel + upsert ref_*
└── src/
    ├── app.d.ts                     # Task 4 — App.Platform typing
    ├── app.html
    ├── error.svelte
    ├── lib/
    │   └── db.ts                    # Task 4 — Turso client singleton
    └── routes/
        ├── +layout.svelte
        └── +page.svelte
```

### `companion/wrangler.toml`

```toml
name = "companion-app"
compatibility_date = "2025-04-01"
compatibility_flags = ["nodejs_compat"]
pages_build_output_dir = ".svelte-kit/cloudflare"
```

> [DEV DECISION]: Update `compatibility_date` to the latest recommended date at time of implementation. Check https://developers.cloudflare.com/workers/configuration/compatibility-dates/ for current guidance.

### `companion/svelte.config.js`

```js
import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter()
  }
};

export default config;
```

### `companion/.dev.vars` (template — fill after Task 2)

```
TURSO_DATABASE_URL=
TURSO_AUTH_TOKEN=
CAMPAIGN_SECRET=
AUTH_SECRET=
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
```

### `companion/.gitignore` (create if not auto-created by scaffold)

```
.dev.vars
```

Also confirm `.dev.vars` is ignored in the root `.gitignore`; add if absent.

### `companion/package.json` — scripts additions

Merge into the `"scripts"` block generated by scaffold. Add:

```json
"migrate": "tsx --env-file=.dev.vars scripts/migrate.ts",
"seed":    "tsx --env-file=.dev.vars scripts/seed.ts"
```

### `companion/db/.gitkeep` and `companion/scripts/.gitkeep`

Empty files. Purpose: track otherwise-empty directories in git.

---

## Blueprint 1.2 — Turso DB Provisioning

CLI sequence (no code files produced):

```sh
# Install CLI (if absent)
npm install -g @turso/cli

# Authenticate
turso auth login

# Create database — record the libsql:// URL from output
turso db create companion-app

# Generate read-write token — record value immediately
turso db tokens create companion-app

# Verify connectivity (expect empty .tables output)
turso db shell companion-app
.tables
.quit
```

After Step 4, populate `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` in `companion/.dev.vars`.

---

## Blueprint 1.3 — `companion/db/schema.sql` (complete DDL)

Copy-pasteable. Execute via `npm run migrate` or `turso db shell companion-app < db/schema.sql`.

Tables in dependency order: no-FK tables first, then FK-dependent, then repeating (FK → characters).

```sql
-- ============================================================
-- companion_app/db/schema.sql
-- Authoritative DDL. Execute in full; foreign_keys enforcement
-- requires PRAGMA foreign_keys = ON at runtime (see db.ts).
-- ============================================================

-- ── 1. campaigns ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS campaigns (
  id                   TEXT PRIMARY KEY,
  name                 TEXT NOT NULL,
  campaign_secret_hash TEXT NOT NULL,
  created_at           TEXT DEFAULT (datetime('now'))
);

-- ── 2. players ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS players (
  id           TEXT PRIMARY KEY,
  username     TEXT NOT NULL,
  display_name TEXT,
  avatar       TEXT,
  is_gm        INTEGER NOT NULL DEFAULT 0,
  created_at   TEXT DEFAULT (datetime('now')),
  updated_at   TEXT DEFAULT (datetime('now'))
);

-- ── 3. characters ───────────────────────────────────────────
-- Backbone + all scalar game-data columns (1:1 with scalarFields post-Phase-0)
-- campaign_db_id/char_db_id/char_sync_version from Roll20 map to
-- campaign_id / id / sync_version in backbone — not duplicated here.
CREATE TABLE IF NOT EXISTS characters (
  -- Backbone
  id                    TEXT PRIMARY KEY,
  player_id             TEXT REFERENCES players(id),
  campaign_id           TEXT NOT NULL REFERENCES campaigns(id),
  roll20_character_id   TEXT UNIQUE,
  sync_version          INTEGER NOT NULL DEFAULT 0,
  synced_at             TEXT DEFAULT (datetime('now')),
  created_at            TEXT DEFAULT (datetime('now')),
  updated_at            TEXT DEFAULT (datetime('now')),

  -- Attributes: base
  body_base  INTEGER, dex_base  INTEGER, str_base  INTEGER, cha_base  INTEGER,
  int_base   INTEGER, wil_base  INTEGER, hum_base  INTEGER, mag_base  INTEGER,

  -- Attributes: mutation modifiers
  body_mutations INTEGER, dex_mutations INTEGER, str_mutations INTEGER, cha_mutations INTEGER,
  int_mutations  INTEGER, wil_mutations  INTEGER, hum_mutations  INTEGER,

  -- Attributes: magic modifiers
  body_magic INTEGER, dex_magic INTEGER, str_magic INTEGER, cha_magic INTEGER,
  int_magic  INTEGER, wil_magic  INTEGER, hum_magic  INTEGER,

  -- Attributes: misc modifiers
  body_misc INTEGER, dex_misc INTEGER, str_misc INTEGER, cha_misc INTEGER,
  int_misc  INTEGER, wil_misc  INTEGER, hum_misc  INTEGER, mag_misc  INTEGER,

  -- Attributes: totals
  body INTEGER, dex INTEGER, str INTEGER, cha INTEGER,
  int  INTEGER, wil INTEGER, hum INTEGER, mag INTEGER,

  -- Reaction
  reaction_base INTEGER, reaction_misc INTEGER, reaction INTEGER,

  -- Dice pools
  pool_spell_base   INTEGER, pool_spell_misc   INTEGER, pool_spell   INTEGER,
  pool_combat_base  INTEGER, pool_combat_misc  INTEGER, pool_combat  INTEGER,
  pool_control_base INTEGER, pool_control_misc INTEGER, pool_control INTEGER,
  pool_astral_base  INTEGER, pool_astral_misc  INTEGER, pool_astral  INTEGER,

  -- Initiative
  init_dice INTEGER, init_reaction_mod INTEGER, init_misc_mod INTEGER, init_score INTEGER,

  -- Condition monitor derived
  cm_physical_overflow INTEGER, cm_tn_mod INTEGER, cm_init_mod INTEGER,

  -- Condition monitor: mental boxes (0/1 checkboxes)
  cm_mental_l1 INTEGER, cm_mental_l2 INTEGER,
  cm_mental_m1 INTEGER, cm_mental_m2 INTEGER, cm_mental_m3 INTEGER,
  cm_mental_s1 INTEGER, cm_mental_s2 INTEGER, cm_mental_s3 INTEGER, cm_mental_s4 INTEGER,
  cm_mental_d  INTEGER,

  -- Condition monitor: stun boxes (0/1 checkboxes)
  cm_stun_l1 INTEGER, cm_stun_l2 INTEGER,
  cm_stun_m1 INTEGER, cm_stun_m2 INTEGER, cm_stun_m3 INTEGER,
  cm_stun_s1 INTEGER, cm_stun_s2 INTEGER, cm_stun_s3 INTEGER, cm_stun_s4 INTEGER,
  cm_stun_d  INTEGER, cm_stun_u  INTEGER,

  -- Condition monitor: physical boxes (0/1 checkboxes)
  cm_physical_l1 INTEGER, cm_physical_l2 INTEGER,
  cm_physical_m1 INTEGER, cm_physical_m2 INTEGER, cm_physical_m3 INTEGER,
  cm_physical_s1 INTEGER, cm_physical_s2 INTEGER, cm_physical_s3 INTEGER, cm_physical_s4 INTEGER,
  cm_physical_d  INTEGER, cm_physical_u  INTEGER,

  -- Identity
  char_name TEXT, char_race_station TEXT, char_sex TEXT, char_age TEXT,
  char_description TEXT, char_notes TEXT,

  -- Karma
  karma_good INTEGER, karma_used INTEGER, karma_total INTEGER, karma_pool INTEGER,

  -- Encumberment
  ep_total INTEGER, ep_max INTEGER,

  -- Armor (worn)
  armor_torso_name TEXT, armor_torso_piercing INTEGER, armor_torso_slashing INTEGER, armor_torso_impact INTEGER,
  armor_legs_name  TEXT, armor_legs_piercing  INTEGER, armor_legs_slashing  INTEGER, armor_legs_impact  INTEGER,
  armor_head_name  TEXT, armor_head_piercing  INTEGER, armor_head_slashing  INTEGER, armor_head_impact  INTEGER,
  armor_total_piercing INTEGER, armor_total_slashing INTEGER, armor_total_impact INTEGER,

  -- Adept power points (fractional)
  power_points_max REAL, power_points_used REAL, power_points_remaining REAL,

  -- Spellcasting
  spells_sustained INTEGER, sustained_tn_mod INTEGER, tn_warning_level INTEGER,

  -- Essence (fractional)
  essence_total REAL,

  -- Money (Phase 0 additions)
  money_gold INTEGER, money_silver INTEGER, money_copper INTEGER
);

-- ── 4. rep_skills ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_skills (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  skill_name       TEXT,
  skill_linked_attr TEXT,
  skill_general    TEXT,
  skill_spec       INTEGER,
  skill_base       INTEGER,
  skill_foci       INTEGER,
  skill_misc       INTEGER,
  skill_total      INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 5. rep_mutations ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_mutations (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  mutation_name    TEXT,
  mutation_level   INTEGER,
  mutation_essence REAL,
  mutation_bp_cost INTEGER,
  mutation_effect  TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 6. rep_adept_powers ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_adept_powers (
  id                  TEXT PRIMARY KEY,
  character_id        TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id       TEXT NOT NULL,
  power_name          TEXT,
  power_level         INTEGER,
  power_pp_cost       TEXT,
  power_pp_cost_value REAL,
  power_effect        TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 7. rep_spells ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_spells (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  spell_name    TEXT,
  spell_force   INTEGER,
  spell_drain   TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 8. rep_foci ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_foci (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  focus_name    TEXT,
  focus_type    TEXT,
  focus_force   INTEGER,
  focus_bonded  INTEGER,
  focus_notes   TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 9. rep_weapons ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_weapons (
  id                  TEXT PRIMARY KEY,
  character_id        TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id       TEXT NOT NULL,
  weapon_name         TEXT,
  weapon_type         TEXT,
  weapon_modifiers    TEXT,
  weapon_power        INTEGER,
  weapon_damage       TEXT,
  weapon_conceal      INTEGER,
  weapon_reach        INTEGER,
  weapon_ep           INTEGER,
  weapon_range_short  TEXT,
  weapon_range_medium TEXT,
  weapon_range_long   TEXT,
  weapon_range_extreme TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 10. rep_equipment ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_equipment (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  equip_name       TEXT,
  equip_description TEXT,
  equip_ep         INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 11. rep_contacts ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_contacts (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  contact_name  TEXT,
  contact_info  TEXT,
  contact_level TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 12. rep_karma ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_karma (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  karma_event   TEXT,
  karma_amount  INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 13. rep_milestones ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_milestones (
  id                TEXT PRIMARY KEY,
  character_id      TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id     TEXT NOT NULL,
  milestone_trial   TEXT,
  milestone_tier1   TEXT,
  milestone_tier2   TEXT,
  milestone_tier3   TEXT,
  milestone_current INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 14. ref_spells ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spells (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  category    TEXT NOT NULL,
  type        TEXT,
  target      TEXT,
  duration    TEXT,
  drain       TEXT,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 15. ref_weapons ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_weapons (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  type       TEXT,
  conceal    INTEGER,
  reach      INTEGER,
  damage     TEXT,
  ep         INTEGER,
  cost       INTEGER,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 16. ref_armor ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_armor (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  location   TEXT,
  conceal    INTEGER,
  rating_p   INTEGER,
  rating_s   INTEGER,
  rating_i   INTEGER,
  ep         INTEGER,
  cost       INTEGER,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 17. ref_equipment ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_equipment (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  conceal    INTEGER,
  ep         INTEGER,
  cost       INTEGER,
  notes      TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 18. ref_skills ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_skills (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT NOT NULL,
  linked_attr     TEXT,
  category        TEXT,
  specializations TEXT,
  created_at      TEXT DEFAULT (datetime('now')),
  updated_at      TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 19. ref_adept_powers ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_adept_powers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  pp_cost     TEXT,
  description TEXT,
  game_effect TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 20. ref_mutations ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_mutations (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  essence     TEXT,
  bp_cost     INTEGER,
  description TEXT,
  game_effect TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 21. ref_totems ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_totems (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  name          TEXT NOT NULL,
  type          TEXT NOT NULL,
  environment   TEXT,
  description   TEXT,
  advantages    TEXT,
  disadvantages TEXT,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 22. ref_spirits ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spirits (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  name               TEXT NOT NULL,
  category           TEXT NOT NULL,
  formula_b          TEXT,
  formula_q          TEXT,
  formula_s          TEXT,
  formula_c          TEXT,
  formula_i          TEXT,
  formula_w          TEXT,
  formula_e          TEXT,
  formula_r          TEXT,
  formula_initiative TEXT,
  attack             TEXT,
  powers             TEXT,
  weaknesses         TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  updated_at         TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 23. ref_spirit_powers ────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spirit_powers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  type        TEXT,
  action      TEXT,
  range       TEXT,
  duration    TEXT,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 24. ref_elemental_services ───────────────────────────────
CREATE TABLE IF NOT EXISTS ref_elemental_services (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── Indices ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_characters_player    ON characters (player_id);
CREATE INDEX IF NOT EXISTS idx_characters_campaign  ON characters (campaign_id);
CREATE INDEX IF NOT EXISTS idx_rep_skills_char      ON rep_skills (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_mutations_char   ON rep_mutations (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_adept_powers_char ON rep_adept_powers (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_spells_char      ON rep_spells (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_foci_char        ON rep_foci (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_weapons_char     ON rep_weapons (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_equipment_char   ON rep_equipment (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_contacts_char    ON rep_contacts (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_karma_char       ON rep_karma (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_milestones_char  ON rep_milestones (character_id);
CREATE INDEX IF NOT EXISTS idx_ref_spells_category  ON ref_spells (category);
CREATE INDEX IF NOT EXISTS idx_ref_spells_type      ON ref_spells (type);
CREATE INDEX IF NOT EXISTS idx_ref_weapons_type     ON ref_weapons (type);
CREATE INDEX IF NOT EXISTS idx_ref_totems_type      ON ref_totems (type);
CREATE INDEX IF NOT EXISTS idx_ref_spirits_category ON ref_spirits (category);
```

---

## Blueprint 1.4 — Turso Client Singleton

### `companion/src/app.d.ts`

```typescript
// See https://kit.svelte.dev/docs/types#app
declare global {
  namespace App {
    interface Platform {
      env: {
        TURSO_DATABASE_URL: string;
        TURSO_AUTH_TOKEN: string;
        CAMPAIGN_SECRET: string;
        AUTH_SECRET: string;
        DISCORD_CLIENT_ID: string;
        DISCORD_CLIENT_SECRET: string;
      };
    }
  }
}
export {};
```

### `companion/src/lib/db.ts`

```typescript
import { createClient } from '@libsql/client/web';
import type { Client } from '@libsql/client';

/**
 * Creates a fresh libSQL client for each request.
 * Issues PRAGMA foreign_keys = ON before returning.
 *
 * @param env - CF Pages platform env (event.platform.env in +server.ts)
 * @returns Client with FK enforcement active
 *
 * IMPORTANT: Use @libsql/client/web (Fetch API) — NOT /node.
 * CF Workers have no Node.js net/tls module; /web uses fetch only.
 */
export async function getDb(env: App.Platform['env']): Promise<Client> {
  const client = createClient({
    url: env.TURSO_DATABASE_URL,
    authToken: env.TURSO_AUTH_TOKEN,
  });
  await client.execute('PRAGMA foreign_keys = ON');
  return client;
}
```

> [DEV DECISION]: In SvelteKit with `adapter-cloudflare`, `platform.env` is exposed on `event.platform?.env` inside `+server.ts` handlers and `hooks.server.ts`. It is NOT in `+page.server.ts` `load()` without `event.platform`. Verify the SvelteKit version's exact access pattern and confirm `platform` is non-null before passing to `getDb`.

### `companion/scripts/migrate.ts` (structure)

```typescript
import { createClient } from '@libsql/client/node';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

async function main(): Promise<void> {
  // Guard: require explicit --force flag to prevent accidental re-run
  // on a populated database.
  //   Usage: npm run migrate -- --force
  const force = process.argv.includes('--force');
  if (!force) {
    console.error('Pass --force to execute migration.');
    process.exit(1);
  }

  const url       = process.env.TURSO_DATABASE_URL!;
  const authToken = process.env.TURSO_AUTH_TOKEN!;
  const schemaPath = resolve(__dirname, '../db/schema.sql');
  const sql = readFileSync(schemaPath, 'utf-8');

  const db = createClient({ url, authToken });

  // Split on statement boundaries and execute sequentially
  const statements = sql.split(';').map(s => s.trim()).filter(Boolean);
  for (const stmt of statements) {
    await db.execute(stmt);
  }

  console.log(`Migration complete — ${statements.length} statements executed.`);
  db.close();
}

main().catch(e => { console.error(e); process.exit(1); });
```

> Note: `@libsql/client/node` is correct here — migrate.ts runs in Node.js, not CF Workers.

---

## Blueprint 1.5 — Seed Utility

### File: `companion/scripts/seed.ts`

#### Section A — Imports and Configuration

```typescript
import { createClient } from '@libsql/client/node';
import * as XLSX from 'xlsx';
import { resolve } from 'node:path';

// Workbook directory: elements/ at repo root (contains .xlsx game-data files).
// [BLOCKING PRE-IMPLEMENTATION CHECK]: Confirm .xlsx workbooks exist in
// elements/ before first seed run. If they live elsewhere, update this path.
const WORKBOOKS_DIR = resolve(__dirname, '../../elements');

const WORKBOOK_FILES = {
  spells:               'Spells.xlsx',
  equipment:            'Equipment.xlsx',
  skills:               'Skills.xlsx',
  adeptPowersMutations: 'Adept Powers and Mutations.xlsx',
  totemsSpirits:        'Totems and Spirits.xlsx',
} as const;
```

#### Section B — Row Interfaces

```typescript
interface SpellRow {
  name: string;
  category: string;       // derived from Excel sheet name
  type: string | null;    // "M" or "P"
  target: string | null;
  duration: string | null;
  drain: string | null;
  description: string | null;
}

interface WeaponRow {
  name: string;
  type: string | null;    // Edged, Clubs, Projectile, etc.
  conceal: number | null;
  reach: number | null;
  damage: string | null;
  ep: number | null;
  cost: number | null;
}

interface ArmorRow {
  name: string;
  location: string | null;
  conceal: number | null;
  rating_p: number | null;
  rating_s: number | null;
  rating_i: number | null;
  ep: number | null;
  cost: number | null;
}

interface EquipmentRow {
  name: string;
  conceal: number | null;
  ep: number | null;
  cost: number | null;
  notes: string | null;
}

interface SkillRow {
  name: string;
  linked_attr: string | null;
  category: string | null;
  specializations: string | null;  // comma-separated
}

interface AdeptPowerRow {
  name: string;
  pp_cost: string | null;
  description: string | null;
  game_effect: string | null;
}

interface MutationRow {
  name: string;
  essence: string | null;   // stored as text; may be "0.1 per level"
  bp_cost: number | null;
  description: string | null;
  game_effect: string | null;
}

interface TotemRow {
  name: string;
  type: string;             // "Animal" or "Nature" — from sheet name
  environment: string | null;
  description: string | null;
  advantages: string | null;
  disadvantages: string | null;
}

interface SpiritRow {
  name: string;
  category: string;         // "Elemental" or "Nature" — from sheet name
  formula_b: string | null;
  formula_q: string | null;
  formula_s: string | null;
  formula_c: string | null;
  formula_i: string | null;
  formula_w: string | null;
  formula_e: string | null;
  formula_r: string | null;
  formula_initiative: string | null;
  attack: string | null;
  powers: string | null;    // comma-separated power names
  weaknesses: string | null;
}

interface SpiritPowerRow {
  name: string;
  type: string | null;      // "P" or "M"
  action: string | null;
  range: string | null;
  duration: string | null;
  description: string | null;
}

interface ElementalServiceRow {
  name: string;
  description: string | null;
}

interface SeedStats {
  table: string;
  upserted: number;
  errors: number;
}
```

#### Section C — Parser Signatures + Column Mapping

Each parser: skip blank-name rows, trim strings, map missing cells to `null`.

```typescript
/**
 * Iterates all 9 category sheets in Spells.xlsx.
 * Sheet name → row.category value.
 * Expected columns: Name, Type, Target, Duration, Drain, Description
 */
function parseSpells(wb: XLSX.WorkBook): SpellRow[]

/**
 * Equipment.xlsx → "Weapons" sheet.
 * Expected columns: Name, Type, Conceal, Reach, Damage, EP, Cost
 */
function parseWeapons(wb: XLSX.WorkBook): WeaponRow[]

/**
 * Equipment.xlsx → "Armor" sheet.
 * Expected columns: Name, Location, Conceal, P, S, I, EP, Cost
 * [DEV DECISION]: Verify actual column headers P/S/I in workbook;
 * if different (e.g., "Piercing"/"Slashing"/"Impact"), update mapping here.
 */
function parseArmor(wb: XLSX.WorkBook): ArmorRow[]

/**
 * Equipment.xlsx → "Equipment" sheet.
 * Expected columns: Name, Conceal, EP, Cost, Notes
 */
function parseEquipment(wb: XLSX.WorkBook): EquipmentRow[]

/**
 * Skills.xlsx → first sheet (or sheet named "Skills").
 * Expected columns: Name, Linked Attribute, Category, Specializations
 */
function parseSkills(wb: XLSX.WorkBook): SkillRow[]

/**
 * Adept Powers and Mutations.xlsx → "Powers" sheet.
 * Expected columns: Name, PP Cost, Description, Game Effect
 */
function parseAdeptPowers(wb: XLSX.WorkBook): AdeptPowerRow[]

/**
 * Adept Powers and Mutations.xlsx → "Mutations" sheet.
 * Expected columns: Name, Essence, BP Cost, Description, Game Effect
 */
function parseMutations(wb: XLSX.WorkBook): MutationRow[]

/**
 * Totems and Spirits.xlsx → totem sheet(s).
 * [DEV DECISION]: May be 1 sheet (all totems) or 2 sheets (Animal/Nature split).
 * Check wb.SheetNames for actual names. Derive row.type from sheet name:
 * if sheet name contains "Animal" → type="Animal"; "Nature" → type="Nature".
 * Expected columns: Name, Environment, Description, Advantages, Disadvantages
 */
function parseTotems(wb: XLSX.WorkBook): TotemRow[]

/**
 * Totems and Spirits.xlsx → "Spirits" sheet (or equivalent).
 * Derive category from sheet name: "Elemental" or "Nature".
 * Expected columns: Name, B, Q, S, C, I, W, E, R, Initiative, Attack, Powers, Weaknesses
 */
function parseSpirits(wb: XLSX.WorkBook): SpiritRow[]

/**
 * Totems and Spirits.xlsx → "Spirit Powers" sheet (or equivalent).
 * Expected columns: Name, Type, Action, Range, Duration, Description
 */
function parseSpiritPowers(wb: XLSX.WorkBook): SpiritPowerRow[]

/**
 * Totems and Spirits.xlsx → "Elemental Services" sheet (or equivalent).
 * Expected columns: Name, Description
 */
function parseElementalServices(wb: XLSX.WorkBook): ElementalServiceRow[]
```

#### Section D — Seeder Signatures

All seeders follow identical contract:

```typescript
/** Upsert pattern for all seeders:
 *
 * INSERT INTO {table} (col1, col2, ...) VALUES (?, ?, ...)
 * ON CONFLICT(name) DO UPDATE SET col1=excluded.col1, ..., updated_at=datetime('now')
 *
 * Batch size: 50 rows per execute() call.
 * Returns: SeedStats { table, upserted (total rows processed), errors }
 */

function seedSpells(db: Client, rows: SpellRow[]): Promise<SeedStats>
function seedWeapons(db: Client, rows: WeaponRow[]): Promise<SeedStats>
function seedArmor(db: Client, rows: ArmorRow[]): Promise<SeedStats>
function seedEquipment(db: Client, rows: EquipmentRow[]): Promise<SeedStats>
function seedSkills(db: Client, rows: SkillRow[]): Promise<SeedStats>
function seedAdeptPowers(db: Client, rows: AdeptPowerRow[]): Promise<SeedStats>
function seedMutations(db: Client, rows: MutationRow[]): Promise<SeedStats>
function seedTotems(db: Client, rows: TotemRow[]): Promise<SeedStats>
function seedSpirits(db: Client, rows: SpiritRow[]): Promise<SeedStats>
function seedSpiritPowers(db: Client, rows: SpiritPowerRow[]): Promise<SeedStats>
function seedElementalServices(db: Client, rows: ElementalServiceRow[]): Promise<SeedStats>
```

**Upsert template (use for each seeder, substitute table/columns):**

```typescript
// Example: seedSpells — replicate structure for all 11 seeders
async function seedSpells(db: Client, rows: SpellRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_spells (name, category, type, target, duration, drain, description)
              VALUES (?, ?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                category=excluded.category, type=excluded.type,
                target=excluded.target, duration=excluded.duration,
                drain=excluded.drain, description=excluded.description,
                updated_at=datetime('now')`,
        args: [r.name, r.category, r.type, r.target, r.duration, r.drain, r.description],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedSpells batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_spells', upserted, errors };
}
```

#### Section E — Orchestrator (main)

```typescript
// Main entry — executed by `npm run seed` via tsx --env-file=.dev.vars
async function main(): Promise<void> {
  // 1. Create Node client (seed runs in Node.js — NOT @libsql/client/web)
  const db = createClient({
    url: process.env.TURSO_DATABASE_URL!,
    authToken: process.env.TURSO_AUTH_TOKEN!,
  });

  // 2. Load workbooks
  const wbs = {
    spells:               XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.spells)),
    equipment:            XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.equipment)),
    skills:               XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.skills)),
    adeptPowersMutations: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.adeptPowersMutations)),
    totemsSpirits:        XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.totemsSpirits)),
  };

  // 3. Parse all workbooks → row arrays; log counts
  const spells      = parseSpells(wbs.spells);
  const weapons     = parseWeapons(wbs.equipment);
  const armor       = parseArmor(wbs.equipment);
  const equipment   = parseEquipment(wbs.equipment);
  const skills      = parseSkills(wbs.skills);
  const powers      = parseAdeptPowers(wbs.adeptPowersMutations);
  const mutations   = parseMutations(wbs.adeptPowersMutations);
  const totems      = parseTotems(wbs.totemsSpirits);
  const spirits     = parseSpirits(wbs.totemsSpirits);
  const spiritPowers = parseSpiritPowers(wbs.totemsSpirits);
  const services    = parseElementalServices(wbs.totemsSpirits);

  // 4. Seed sequentially — avoids Turso HTTP rate limits, deterministic output
  console.log('Seeding companion_app reference tables...');
  const seeders: [string, () => Promise<SeedStats>][] = [
    ['ref_spells',             () => seedSpells(db, spells)],
    ['ref_weapons',            () => seedWeapons(db, weapons)],
    ['ref_armor',              () => seedArmor(db, armor)],
    ['ref_equipment',          () => seedEquipment(db, equipment)],
    ['ref_skills',             () => seedSkills(db, skills)],
    ['ref_adept_powers',       () => seedAdeptPowers(db, powers)],
    ['ref_mutations',          () => seedMutations(db, mutations)],
    ['ref_totems',             () => seedTotems(db, totems)],
    ['ref_spirits',            () => seedSpirits(db, spirits)],
    ['ref_spirit_powers',      () => seedSpiritPowers(db, spiritPowers)],
    ['ref_elemental_services', () => seedElementalServices(db, services)],
  ];
  const results: SeedStats[] = [];
  for (const [, fn] of seeders) {
    results.push(await fn());
  }

  // 5. Print stats + exit
  let total = 0;
  for (const r of results) {
    console.log(`  ${r.table.padEnd(24)} upserted=${r.upserted}   errors=${r.errors}`);
    total += r.upserted;
  }
  console.log(`Done. ${total} total records processed.`);

  db.close();
  process.exit(results.some(r => r.errors > 0) ? 1 : 0);
}

main().catch(e => {
  console.error(e);
  db?.close();
  process.exit(1);
});
```

> Note: `db` must be declared as `let db: Client` in outer scope of `main()` so the catch handler can access it for cleanup.

---

## Blueprint 1.6 — Verification Checkpoint

Command sequence (run from `companion/`):

```sh
# 6a — SvelteKit dev server
npm run dev
# Expected: server starts on http://localhost:5173, no TypeScript errors

# 6b — Migrate (first time needs --force)
npm run migrate -- --force
# Expected: "Migration complete — N statements executed."

# 6c — Seed
npm run seed
# Expected: all 11 tables show upserted > 0, errors = 0, exit code 0

# 6d — Turso shell spot-check
turso db shell companion-app
.tables
SELECT COUNT(*) FROM ref_spells;          -- expect 60–80
SELECT COUNT(*) FROM ref_totems;          -- expect 43
SELECT COUNT(*) FROM ref_spirits;         -- expect 19
SELECT COUNT(*) FROM ref_spirit_powers;   -- expect 18
SELECT COUNT(*) FROM ref_elemental_services; -- expect 4
SELECT * FROM ref_spells LIMIT 1;         -- visual spot-check
.quit

# 6e — Idempotency check (second seed run must not grow any table)
npm run seed
# Expected: same upserted counts, no new rows in .tables COUNT(*) queries
```

**Expected row counts (acceptance gate):**

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

---

## Implementation Order

| Step | Blueprint | Produces |
|------|-----------|----------|
| 1 | 1.1 | `companion/` scaffold — SvelteKit + wrangler.toml + .dev.vars template |
| 2 | 1.2 | Turso DB provisioned, .dev.vars populated |
| 3 | 1.3 (write) | `companion/db/schema.sql` |
| 4 | 1.4 (migrate.ts) | `companion/scripts/migrate.ts` |
| 5 | 1.3 (execute) | `npm run migrate -- --force` → 24 tables live |
| 6 | 1.4 (db.ts + app.d.ts) | `companion/src/lib/db.ts`, `src/app.d.ts` |
| 7 | 1.5 | `companion/scripts/seed.ts` |
| 8 | 1.6 | All verification commands pass |

---


# Layer 3 — Phase 2: Sync Endpoint + Roll20 Wiring — Technical Blueprints

---

## Blueprint 2.1 — `companion/src/routes/api/sync/+server.ts`

**Component:** POST `/api/sync` — HTTP-layer validation pipeline  
**New file:** `companion/src/routes/api/sync/+server.ts`

### Complete Implementation

```typescript
// companion/src/routes/api/sync/+server.ts
import type { RequestEvent } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import { syncWrite, SyncError } from '$lib/sync-write';
import type { SyncPayload } from '$lib/sync-write';

const REQUIRED_REPEATING_KEYS = [
  'skills', 'mutations', 'adept_powers', 'spells',
  'foci', 'weapons', 'equipment', 'contacts', 'karma', 'milestones',
] as const;

function jsonResp(body: unknown, status: number): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

/**
 * Timing-safe comparison: SHA-256 hash the incoming plaintext, then XOR every
 * byte of both 64-char hex strings. Loop always runs to completion — no
 * short-circuit regardless of first mismatch (prevents timing oracle).
 */
async function timingSafeHexCompare(incoming: string, storedHex: string): Promise<boolean> {
  const hashBuffer = await crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(incoming),
  );
  const incomingHex = Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  // Both are always 64-char hex strings — length mismatch = corrupted stored hash
  if (incomingHex.length !== storedHex.length) return false;

  const a = new TextEncoder().encode(incomingHex);
  const b = new TextEncoder().encode(storedHex);
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a[i] ^ b[i];
  }
  return diff === 0;
}

export async function POST({ request, platform }: RequestEvent): Promise<Response> {
  // 1b. Body size guard — application-level 1 MB ceiling
  const contentLength = request.headers.get('content-length');
  if (contentLength !== null && parseInt(contentLength, 10) > 1_048_576) {
    return jsonResp({ ok: false, error: 'Payload too large' }, 413);
  }

  // 1c. Content-Type guard
  if (!request.headers.get('content-type')?.includes('application/json')) {
    return jsonResp({ ok: false, error: 'Unsupported Media Type' }, 415);
  }

  // 1d. Body parse
  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return jsonResp({ ok: false, error: 'Invalid JSON' }, 400);
  }

  // 1e. Required-field validation — checked in spec order, first failure wins
  if (!body.campaign_db_id || typeof body.campaign_db_id !== 'string') {
    return jsonResp({ ok: false, error: 'campaign_db_id required' }, 400);
  }
  if (!('char_db_id' in body)) {
    return jsonResp({ ok: false, error: 'char_db_id required' }, 400);
  }
  if (
    typeof body.sync_version_from !== 'number' ||
    !Number.isInteger(body.sync_version_from) ||
    body.sync_version_from < 0 ||
    !Number.isSafeInteger(body.sync_version_from)
  ) {
    return jsonResp({ ok: false, error: 'sync_version_from must be a non-negative integer' }, 400);
  }
  if (!body.scalars || typeof body.scalars !== 'object' || Array.isArray(body.scalars)) {
    return jsonResp({ ok: false, error: 'scalars required' }, 400);
  }
  if (!body.repeating || typeof body.repeating !== 'object' || Array.isArray(body.repeating)) {
    return jsonResp({ ok: false, error: 'repeating required' }, 400);
  }

  const rep = body.repeating as Record<string, unknown>;
  for (const key of REQUIRED_REPEATING_KEYS) {
    if (!(key in rep)) {
      return jsonResp({ ok: false, error: `repeating.${key} required` }, 400);
    }
    if (!Array.isArray(rep[key])) {
      return jsonResp({ ok: false, error: `repeating.${key} must be an array` }, 400);
    }
  }

  // 1f. Secret header presence check
  // Same 401 body for all unauthorized states — never distinguish missing vs wrong
  const incomingSecret = request.headers.get('X-Campaign-Secret');
  if (!incomingSecret) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1g. Campaign lookup
  let db: Awaited<ReturnType<typeof getDb>>;
  try {
    db = await getDb(platform!.env);
  } catch (err) {
    console.error('[sync] db init error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }

  let campaignRow: { campaign_secret_hash: string } | undefined;
  try {
    const result = await db.execute({
      sql: 'SELECT campaign_secret_hash FROM campaigns WHERE id = ?',
      args: [body.campaign_db_id as string],
    });
    campaignRow = result.rows[0] as unknown as { campaign_secret_hash: string } | undefined;
  } catch (err) {
    console.error('[sync] campaign lookup error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }

  // Return 401 (not 404) — never disclose whether a campaign ID is valid (prevents enumeration)
  if (!campaignRow) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1h. Timing-safe secret verification
  const secretValid = await timingSafeHexCompare(incomingSecret, campaignRow.campaign_secret_hash);
  if (!secretValid) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1i. Invoke sync write logic
  try {
    const result = await syncWrite(
      db,
      body as unknown as SyncPayload,
      body.campaign_db_id as string,
    );
    // Response contract: { ok: true, char_db_id, sync_version }
    // Roll20 handler reads response.char_db_id and response.sync_version — key names are binding
    return jsonResp({ ok: true, char_db_id: result.char_db_id, sync_version: result.sync_version }, 200);
  } catch (err) {
    if (err instanceof SyncError) {
      return jsonResp({ ok: false, error: err.message }, err.status);
    }
    console.error('[sync] error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }
}
```

### Notes

| Check | Detail |
|---|---|
| `'char_db_id' in body` | `in` check (not truthiness) — null is valid (first sync) |
| Campaign → 401 not 404 | Non-existent campaign returns same 401 as wrong secret — no enumeration |
| SyncError routing | status 404 = character not found; status 409 = version conflict |
| `platform!.env` | Non-null assertion valid — CF Pages always injects `platform.env` in production |

[DEV DECISION]: `platform!.env` non-null assertion is safe in CF Pages production. During `wrangler pages dev`, platform is also populated. In Vitest unit tests, platform must be mocked or the db call bypassed.

---

## Blueprint 2.2 — `companion/src/lib/sync-write.ts`

**Component:** Sync write logic — types, allowlists, transaction builder  
**New file:** `companion/src/lib/sync-write.ts`

### Complete Implementation

```typescript
// companion/src/lib/sync-write.ts
import type { Client, InValue } from '@libsql/client';

// ── Exported types ───────────────────────────────────────────────────────────

export interface SyncPayload {
  campaign_db_id: string;
  char_db_id: string | null;
  sync_version_from: number;
  scalars: Record<string, unknown>;
  repeating: Record<RepSection, RepRow[]>;
}

interface RepRow {
  roll20_row_id: string;
  [key: string]: unknown;
}

export interface SyncResult {
  char_db_id: string;
  sync_version: number;
}

export class SyncError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = 'SyncError';
  }
}

type RepSection =
  | 'skills' | 'mutations' | 'adept_powers' | 'spells' | 'foci'
  | 'weapons' | 'equipment' | 'contacts' | 'karma' | 'milestones';

// ── Security allowlists ──────────────────────────────────────────────────────
// Source: companion/db/schema.sql Blueprint 1.3 — characters CREATE TABLE.
// Backbone columns excluded: id, player_id, campaign_id, roll20_character_id,
//   sync_version, synced_at, created_at, updated_at.
// Column names come ONLY from this list — payload keys are never used as SQL identifiers.
// [REVIEWER NOTE]: L2 specifies Set<string>, but ReadonlyArray is the better fit here —
// we iterate the allowlist (not the payload) to build SQL, so array ordering is needed.
// This is a deliberate, safer divergence from L2's collection type.

const ALLOWED_SCALAR_COLUMNS: ReadonlyArray<string> = [
  // Attributes: base
  'body_base',  'dex_base',  'str_base',  'cha_base',
  'int_base',   'wil_base',  'hum_base',  'mag_base',
  // Attributes: mutation modifiers
  'body_mutations', 'dex_mutations', 'str_mutations', 'cha_mutations',
  'int_mutations',  'wil_mutations', 'hum_mutations',
  // Attributes: magic modifiers
  'body_magic', 'dex_magic', 'str_magic', 'cha_magic',
  'int_magic',  'wil_magic', 'hum_magic',
  // Attributes: misc modifiers
  'body_misc',  'dex_misc',  'str_misc',  'cha_misc',
  'int_misc',   'wil_misc',  'hum_misc',  'mag_misc',
  // Attributes: totals
  'body', 'dex', 'str', 'cha', 'int', 'wil', 'hum', 'mag',
  // Reaction
  'reaction_base', 'reaction_misc', 'reaction',
  // Dice pools
  'pool_spell_base',   'pool_spell_misc',   'pool_spell',
  'pool_combat_base',  'pool_combat_misc',  'pool_combat',
  'pool_control_base', 'pool_control_misc', 'pool_control',
  'pool_astral_base',  'pool_astral_misc',  'pool_astral',
  // Initiative
  'init_dice', 'init_reaction_mod', 'init_misc_mod', 'init_score',
  // Condition monitor: derived
  'cm_physical_overflow', 'cm_tn_mod', 'cm_init_mod',
  // Condition monitor: mental boxes
  'cm_mental_l1', 'cm_mental_l2',
  'cm_mental_m1', 'cm_mental_m2', 'cm_mental_m3',
  'cm_mental_s1', 'cm_mental_s2', 'cm_mental_s3', 'cm_mental_s4',
  'cm_mental_d',
  // Condition monitor: stun boxes
  'cm_stun_l1', 'cm_stun_l2',
  'cm_stun_m1', 'cm_stun_m2', 'cm_stun_m3',
  'cm_stun_s1', 'cm_stun_s2', 'cm_stun_s3', 'cm_stun_s4',
  'cm_stun_d', 'cm_stun_u',
  // Condition monitor: physical boxes
  'cm_physical_l1', 'cm_physical_l2',
  'cm_physical_m1', 'cm_physical_m2', 'cm_physical_m3',
  'cm_physical_s1', 'cm_physical_s2', 'cm_physical_s3', 'cm_physical_s4',
  'cm_physical_d', 'cm_physical_u',
  // Identity
  'char_name', 'char_race_station', 'char_sex', 'char_age',
  'char_description', 'char_notes',
  // Karma
  'karma_good', 'karma_used', 'karma_total', 'karma_pool',
  // Encumberment
  'ep_total', 'ep_max',
  // Armor (worn)
  'armor_torso_name', 'armor_torso_piercing', 'armor_torso_slashing', 'armor_torso_impact',
  'armor_legs_name',  'armor_legs_piercing',  'armor_legs_slashing',  'armor_legs_impact',
  'armor_head_name',  'armor_head_piercing',  'armor_head_slashing',  'armor_head_impact',
  'armor_total_piercing', 'armor_total_slashing', 'armor_total_impact',
  // Adept power points (fractional)
  'power_points_max', 'power_points_used', 'power_points_remaining',
  // Spellcasting
  'spells_sustained', 'sustained_tn_mod', 'tn_warning_level',
  // Essence (fractional)
  'essence_total',
  // Money (Phase 0 additions)
  'money_gold', 'money_silver', 'money_copper',
];
// Total: 129 scalar columns

// Repeating-section allowlists — one per rep_* table.
// Backbone excluded for each: id, character_id, roll20_row_id.
const ALLOWED_SECTION_COLUMNS: Record<RepSection, ReadonlyArray<string>> = {
  skills: [
    'skill_name', 'skill_linked_attr', 'skill_general', 'skill_spec',
    'skill_base', 'skill_foci', 'skill_misc', 'skill_total',
  ],
  mutations: [
    'mutation_name', 'mutation_level', 'mutation_essence',
    'mutation_bp_cost', 'mutation_effect',
  ],
  adept_powers: [
    'power_name', 'power_level', 'power_pp_cost',
    'power_pp_cost_value', 'power_effect',
  ],
  spells: [
    'spell_name', 'spell_force', 'spell_drain',
  ],
  foci: [
    'focus_name', 'focus_type', 'focus_force', 'focus_bonded', 'focus_notes',
  ],
  weapons: [
    'weapon_name', 'weapon_type', 'weapon_modifiers', 'weapon_power',
    'weapon_damage', 'weapon_conceal', 'weapon_reach', 'weapon_ep',
    'weapon_range_short', 'weapon_range_medium',
    'weapon_range_long', 'weapon_range_extreme',
  ],
  equipment: [
    'equip_name', 'equip_description', 'equip_ep',
  ],
  contacts: [
    'contact_name', 'contact_info', 'contact_level',
  ],
  karma: [
    'karma_event', 'karma_amount',
  ],
  milestones: [
    'milestone_trial', 'milestone_tier1', 'milestone_tier2',
    'milestone_tier3', 'milestone_current',
  ],
};

const REP_SECTIONS: ReadonlyArray<RepSection> = [
  'skills', 'mutations', 'adept_powers', 'spells', 'foci',
  'weapons', 'equipment', 'contacts', 'karma', 'milestones',
];

// ── Main export ──────────────────────────────────────────────────────────────

export async function syncWrite(
  db: Client,
  body: SyncPayload,
  campaignId: string,
): Promise<SyncResult> {
  // ── 2c. First-sync vs subsequent-sync branching ──────────────────────────
  const isFirstSync = body.char_db_id === null;
  let charId: string;
  let newSyncVersion: number;

  if (isFirstSync) {
    charId = crypto.randomUUID();
    newSyncVersion = 1;
  } else {
    const charResult = await db.execute({
      sql: 'SELECT id, sync_version FROM characters WHERE id = ? AND campaign_id = ?',
      args: [body.char_db_id as string, campaignId],
    });
    if (charResult.rows.length === 0) {
      throw new SyncError('Character not found', 404);
    }
    const existingVersion = charResult.rows[0].sync_version as number;
    // 2d. Stale sync detection
    if (existingVersion !== body.sync_version_from) {
      throw new SyncError(
        'Sync conflict: version mismatch. Reload character and retry.',
        409,
      );
    }
    charId = body.char_db_id as string;
    newSyncVersion = existingVersion + 1;
  }

  // ── 2e. Build Turso batch ────────────────────────────────────────────────
  // Batch order: PRAGMA → characters write → 10× DELETE → N× INSERT per section
  const statements: { sql: string; args: InValue[] }[] = [];

  // [0] PRAGMA — enforce FK constraints within the batch transaction
  statements.push({ sql: 'PRAGMA foreign_keys = ON', args: [] });

  // [1] characters INSERT (first sync) or UPDATE (subsequent sync)
  const scalarValues: InValue[] = ALLOWED_SCALAR_COLUMNS.map((col) => {
    const v = body.scalars[col];
    return v === undefined || v === null ? null : String(v);
  });

  if (isFirstSync) {
    // 2f. First sync: INSERT
    const colList  = ALLOWED_SCALAR_COLUMNS.join(', ');
    const phList   = ALLOWED_SCALAR_COLUMNS.map(() => '?').join(', ');
    statements.push({
      sql: `INSERT INTO characters (id, campaign_id, player_id, roll20_character_id, sync_version, synced_at, created_at, updated_at, ${colList}) VALUES (?, ?, NULL, NULL, 1, datetime('now'), datetime('now'), datetime('now'), ${phList})`,
      args: [charId, campaignId, ...scalarValues],
    });
  } else {
    // 2f. Subsequent sync: UPDATE
    const setClause = ALLOWED_SCALAR_COLUMNS.map((col) => `${col} = ?`).join(', ');
    statements.push({
      sql: `UPDATE characters SET sync_version = ?, synced_at = datetime('now'), updated_at = datetime('now'), ${setClause} WHERE id = ? AND campaign_id = ?`,
      args: [newSyncVersion, ...scalarValues, charId, campaignId],
    });
  }

  // [2–11] DELETE all repeating rows for this character — clears before re-insert
  // Explicit DELETE required because we UPDATE (not replace) the parent characters row,
  // so ON DELETE CASCADE does not fire.
  for (const section of REP_SECTIONS) {
    statements.push({
      sql: `DELETE FROM rep_${section} WHERE character_id = ?`,
      args: [charId],
    });
  }

  // [12+] INSERT repeating rows
  // 2g: For each section, for each payload row, build a fresh UUID and insert allowed cols only.
  for (const section of REP_SECTIONS) {
    const rows = body.repeating[section] ?? [];
    const allowedCols = ALLOWED_SECTION_COLUMNS[section];
    for (const row of rows) {
      const rowId      = crypto.randomUUID();
      const roll20RowId = String(row.roll20_row_id ?? '');
      const colList    = allowedCols.join(', ');
      const phList     = allowedCols.map(() => '?').join(', ');
      const rowValues: InValue[] = allowedCols.map((col) => {
        const v = row[col];
        return v === undefined || v === null ? null : String(v);
      });
      statements.push({
        sql: `INSERT INTO rep_${section} (id, character_id, roll20_row_id, ${colList}) VALUES (?, ?, ?, ${phList})`,
        args: [rowId, charId, roll20RowId, ...rowValues],
      });
    }
  }

  // ── Execute batch (atomic — all succeed or all roll back) ────────────────
  try {
    await db.batch(statements, 'write');
  } catch (err) {
    console.error('[sync-write] batch error:', err);
    throw new Error('[sync] DB batch failed');
  }

  // 2h. Return
  return { char_db_id: charId, sync_version: newSyncVersion };
}
```

### Allowlist Column Counts (for verification)

| Table | Allowed columns | Count |
|---|---|---|
| characters (scalars) | body_base … money_copper | 129 |
| rep_skills | skill_name … skill_total | 8 |
| rep_mutations | mutation_name … mutation_effect | 5 |
| rep_adept_powers | power_name … power_effect | 5 |
| rep_spells | spell_name, spell_force, spell_drain | 3 |
| rep_foci | focus_name … focus_notes | 5 |
| rep_weapons | weapon_name … weapon_range_extreme | 12 |
| rep_equipment | equip_name, equip_description, equip_ep | 3 |
| rep_contacts | contact_name, contact_info, contact_level | 3 |
| rep_karma | karma_event, karma_amount | 2 |
| rep_milestones | milestone_trial … milestone_current | 5 |

### Batch Statement Index Map

| Index | Statement | Args |
|---|---|---|
| 0 | `PRAGMA foreign_keys = ON` | _(none)_ |
| 1 | `INSERT INTO characters …` (first sync) **or** `UPDATE characters …` (subsequent) | charId, campaignId, 129× scalar values / newSyncVersion, 129× scalars, charId, campaignId |
| 2 | `DELETE FROM rep_skills WHERE character_id = ?` | charId |
| 3 | `DELETE FROM rep_mutations WHERE character_id = ?` | charId |
| 4 | `DELETE FROM rep_adept_powers WHERE character_id = ?` | charId |
| 5 | `DELETE FROM rep_spells WHERE character_id = ?` | charId |
| 6 | `DELETE FROM rep_foci WHERE character_id = ?` | charId |
| 7 | `DELETE FROM rep_weapons WHERE character_id = ?` | charId |
| 8 | `DELETE FROM rep_equipment WHERE character_id = ?` | charId |
| 9 | `DELETE FROM rep_contacts WHERE character_id = ?` | charId |
| 10 | `DELETE FROM rep_karma WHERE character_id = ?` | charId |
| 11 | `DELETE FROM rep_milestones WHERE character_id = ?` | charId |
| 12+ | `INSERT INTO rep_{section} (id, character_id, roll20_row_id, {allowedCols}) VALUES (…)` | rowId, charId, roll20_row_id, N× values |

[DEV DECISION]: Turso HTTP batch has documented limits on total payload size. A character with ~30 total repeating rows yields ~42 statements — well within limits. If edge-case characters exceed limits (e.g., hundreds of weapons), the batch may need splitting per section. Monitor via Turso dashboard; do not pre-optimize.

[DEV DECISION]: `roll20_character_id` is set to NULL on INSERT (Phase 2 has no Roll20 API access to retrieve it). If future phases need to map back from Roll20's character ID to a DB row, a PATCH endpoint can populate this column post-sync.

---

## Blueprint 2.3 — Roll20 Sheet Worker: Phase 2 Wiring

**File modified:** `sheet.html` — Sheet Worker `<script type="text/worker">` block only  
**Scope:** Two surgical additions to the handler produced by Blueprint 0.5. No HTML or CSS changes.

### Pre-check

Verify Blueprint 0.5 is complete before applying these changes:
- `var remaining = 11` counter/latch pattern implemented
- `SYNC_PROXY_URL` constant declared (empty string)
- All 10 `getSectionIDs()` calls present with `roll20_row_id` in each row object
- fetch call targets `SYNC_PROXY_URL` with `Content-Type: application/json`
- `.then()` handler reads `response.sync_version` and `response.char_db_id`

### Change 1 — Add `CAMPAIGN_SECRET` constant

**Anchor:** Immediately after the `var SYNC_PROXY_URL = '';` line.

**Before:**
```javascript
var SYNC_PROXY_URL = '';
```

**After:**
```javascript
var SYNC_PROXY_URL = '';           // Fill after CF Pages deploy (Task 4d)
var CAMPAIGN_SECRET = '';          // Fill with plaintext campaign secret before going live
```

`CAMPAIGN_SECRET` is the plaintext value. `seed-campaign.ts` hashes it for storage; this is the original value sent with each sync request.

**[DEV DECISION] — Secret in source:** Visible to anyone with Roll20 sheet edit access (GM only for V1). This controls write access to the sync endpoint; it does not protect read access. Acceptable for a closed 6-player group. If the secret is rotated, update both this constant and `campaigns.campaign_secret_hash` in Turso (re-run `seed-campaign.ts` or issue a direct UPDATE).

### Change 2 — Add `X-Campaign-Secret` header to fetch

**Anchor:** The `fetch(SYNC_PROXY_URL, { ... })` call's `headers` object.

**Before:**
```javascript
fetch(SYNC_PROXY_URL, {
  method:  'POST',
  headers: { 'Content-Type': 'application/json' },
  body:    JSON.stringify(payload),
})
```

**After:**
```javascript
fetch(SYNC_PROXY_URL, {
  method:  'POST',
  headers: {
    'Content-Type':    'application/json',
    'X-Campaign-Secret': CAMPAIGN_SECRET,
  },
  body:    JSON.stringify(payload),
})
```

### Change 3 — Response handler verification (no code change if 0.5 was applied correctly)

Confirm the `.then()` handler uses these exact key names (matching the server response contract):

```javascript
.then(function(response) {
  setAttrs({
    char_db_id:        payload.char_db_id || response.char_db_id,
    char_sync_version: response.sync_version.toString(),
    sync_status:       'Synced ✓ — ' + new Date().toLocaleString(),
  })
})
```

- `response.char_db_id` — used on first sync (when `payload.char_db_id` is null)
- `response.sync_version` — server returns integer; `.toString()` converts for Roll20 attr storage

If these key names already match Blueprint 0.5, no change is required.

### Change 4 — Early-exit guard verification (no code change)

Confirm the guard is still present and unchanged:

```javascript
if (!SYNC_PROXY_URL) {
  setAttrs({ sync_status: 'Sync skipped \u2014 no proxy URL configured' })
  return
}
```

`SYNC_PROXY_URL` remains empty string until CF Pages deployment URL is known (Task 4d). This guard keeps the button functional in development without triggering network errors.

### Acceptance Criteria

- `var CAMPAIGN_SECRET = '';` declared after `SYNC_PROXY_URL`
- `'X-Campaign-Secret': CAMPAIGN_SECRET` in fetch headers object
- Response handler reads `response.sync_version` and `response.char_db_id` (no `_v2` suffix or other variation)
- `SYNC_PROXY_URL` remains empty string until Step 4d

---

## Blueprint 2.4 — Deployment, `seed-campaign.ts`, and E2E Verification

**New file:** `companion/scripts/seed-campaign.ts`  
**Modified file:** `companion/package.json` (scripts block only)

### `companion/scripts/seed-campaign.ts` — Complete Implementation

```typescript
// companion/scripts/seed-campaign.ts
// Usage: npm run seed-campaign -- --name "Campaign Name" --secret "plaintext_secret"

import crypto from 'node:crypto';
import { createClient } from '@libsql/client/node';

// Uses @libsql/client/node (NOT /web) — this script runs in Node.js (tsx),
// not a CF Worker. /node uses net/tls; /web requires Fetch API.

function parseArgs(): { name: string; secret: string } {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : undefined;
  };
  const name   = get('--name');
  const secret = get('--secret');
  if (!name || !secret) {
    console.error('Usage: npm run seed-campaign -- --name "Campaign Name" --secret "plaintext_secret"');
    process.exit(1);
  }
  return { name, secret };
}

async function main(): Promise<void> {
  const { name, secret } = parseArgs();

  const hash = crypto.createHash('sha256').update(secret).digest('hex');
  const id   = crypto.randomUUID();

  if (!process.env.TURSO_DATABASE_URL) {
    console.error('TURSO_DATABASE_URL not set. Run with --env-file=.dev.vars or set env vars.');
    process.exit(1);
  }

  const db = createClient({
    url:       process.env.TURSO_DATABASE_URL,
    authToken: process.env.TURSO_AUTH_TOKEN,
  });

  try {
    await db.execute({
      sql:  `INSERT INTO campaigns (id, name, campaign_secret_hash, created_at) VALUES (?, ?, ?, datetime('now'))`,
      args: [id, name, hash],
    });
  } finally {
    db.close();
  }

  console.log(`Campaign seeded. ID: ${id}`);
  console.log('');
  console.log('Next steps:');
  console.log(`  1. Set attr_campaign_db_id in Roll20 to: ${id}`);
  console.log(`  2. Ensure CAMPAIGN_SECRET in .dev.vars (and CF Pages env) equals: ${secret}`);
}

main().catch((err: unknown) => {
  console.error('Seed failed:', err);
  process.exit(1);
});
```

### `companion/package.json` — Scripts Addition

Merge into `"scripts"` block (alongside existing `migrate`, `seed`):

```json
"seed-campaign": "tsx --env-file=.dev.vars scripts/seed-campaign.ts"
```

### Deployment Sequence

**4b. Build:**
```sh
cd companion && npm run build
# Expect: zero TypeScript errors, exit 0
```

**4c. Deploy to CF Pages:**
```sh
# CLI deploy (Method A)
wrangler pages deploy .svelte-kit/cloudflare --project-name=companion-app

# Or push to tracked branch (Method B) — CF Pages CI deploys automatically
```

In CF Pages dashboard → Settings → Environment Variables, set:

| Variable | Value |
|---|---|
| `TURSO_DATABASE_URL` | libsql:// URL from Phase 1 Task 2 |
| `TURSO_AUTH_TOKEN` | token from Phase 1 Task 2 |

> [REVIEWER NOTE]: Omit `CAMPAIGN_SECRET` from CF Pages env vars — the server never reads it at runtime. It only compares the incoming `X-Campaign-Secret` header against the hash stored in the `campaigns` table. The plaintext secret is only needed locally by `seed-campaign.ts` (via `.dev.vars`).

**4d. Update `SYNC_PROXY_URL` in `sheet.html`:**

```javascript
var SYNC_PROXY_URL = 'https://{deployment-name}.pages.dev/api/sync';
```

Upload updated sheet via Roll20 Custom Sheet Editor → Save.

### cURL E2E Test Cases

Run against `npm run dev` (local) or the CF Pages deployment URL.

Seed a campaign row first:
```sh
npm run seed-campaign -- --name "Test Campaign" --secret "mysecret"
# Note the Campaign ID printed to stdout
```

**Test payload template:**
```json
{
  "campaign_db_id": "{uuid-from-seed}",
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

**Test matrix:**

| # | Test | Variation | Expected status | Expected body |
|---|---|---|---|---|
| 1 | First sync, valid | `char_db_id: null`, correct secret | 200 | `{ ok: true, char_db_id: "{new-uuid}", sync_version: 1 }` |
| 2 | Second sync, valid | `char_db_id: "{uuid-from-1}"`, `sync_version_from: 1`, correct secret | 200 | `{ ok: true, char_db_id: "{same-uuid}", sync_version: 2 }` |
| 3 | Stale version | Same char_db_id, `sync_version_from: 0` (stale) | 409 | `{ ok: false, error: "Sync conflict: version mismatch. Reload character and retry." }` |
| 4 | Wrong secret | Correct campaign_db_id, wrong `X-Campaign-Secret` | 401 | `{ ok: false, error: "Unauthorized" }` |
| 5 | Missing header | No `X-Campaign-Secret` header | 401 | `{ ok: false, error: "Unauthorized" }` |
| 6 | Unknown campaign | Valid-format UUID, non-existent `campaign_db_id` | 401 | `{ ok: false, error: "Unauthorized" }` (not 404) |
| 7 | Missing key | `char_db_id` field entirely absent (not null) | 400 | `{ ok: false, error: "char_db_id required" }` |
| 8 | Missing repeating key | `repeating.karma` absent from body | 400 | `{ ok: false, error: "repeating.karma required" }` |
| 9 | Oversized payload | `Content-Length: 1048577` header | 413 | `{ ok: false, error: "Payload too large" }` |

**Turso verification queries (run via `turso db shell companion-app`):**

```sql
-- After Test 1: confirm row created
SELECT char_name, sync_version, synced_at FROM characters ORDER BY created_at DESC LIMIT 1;
-- Expect: char_name='Caellum Test', sync_version=1

-- After Test 2: confirm version incremented
SELECT sync_version FROM characters WHERE id = '{uuid-from-test-1}';
-- Expect: 2

-- For a character with repeating rows (populate skills array in Test 1):
SELECT COUNT(*) FROM rep_skills WHERE character_id = '{uuid}';
-- Expect: row count matching skills array length
```

### Live Roll20 E2E Sequence (4f)

1. Open Roll20 character. Confirm `attr_campaign_db_id` is set (UUID from seed step). Clear `attr_char_db_id` to force first-sync path.
2. Click "Sync to DB". Verify status field updates to `Synced ✓ — {timestamp}`.
3. Verify `attr_char_db_id` is populated with a UUID.
4. In Turso shell: `SELECT char_name, sync_version, synced_at FROM characters ORDER BY created_at DESC LIMIT 1;` — confirm full row with `sync_version = 1`.
5. For a character with non-empty repeating sections: `SELECT COUNT(*) FROM rep_skills WHERE character_id = '{uuid}';` — confirm non-zero.
6. Click "Sync to DB" a second time. Confirm `attr_char_sync_version` updates and `sync_version = 2` in Turso.

---

## Implementation Order — Phase 2

| Step | Blueprint | File | Action | Hard depends on |
|---|---|---|---|---|
| 1 | 2.2 | `companion/src/lib/sync-write.ts` | Create — types, allowlists, transaction builder | BP 1.3 (schema), BP 1.4 (getDb) |
| 2 | 2.1 | `companion/src/routes/api/sync/+server.ts` | Create — validation pipeline, secret verify, syncWrite call | BP 2.2 (SyncError import) |
| 3 | 2.3 | `sheet.html` (worker block) | Add CAMPAIGN_SECRET constant + X-Campaign-Secret header | BP 0.5 complete |
| 4 | 2.4a | `companion/scripts/seed-campaign.ts` | Create seed script | BP 1.3 (campaigns table exists) |
| 5 | 2.4b | `companion/package.json` | Add seed-campaign script | Step 4 |
| 6 | 2.4 | Terminal | `npm run build` — verify zero errors | Steps 1–3 complete |
| 7 | 2.4 | Terminal | `npm run seed-campaign` — seed campaigns row | Step 4, Turso DB live |
| 8 | 2.4 | Terminal / curl | Local E2E test (9 test cases) | Steps 1–7 complete |
| 9 | 2.4 | CF Pages | Deploy, set env vars | Step 6 |
| 10 | 2.3 | `sheet.html` | Fill `SYNC_PROXY_URL` with CF Pages URL | Step 9 |
| 11 | 2.4 | Roll20 / Turso | Live E2E test | Steps 3, 9, 10 complete |

---


# Layer 3 — Phase 3: Auth + Character Viewer — Technical Blueprints

**Files touched:** `companion/src/app.d.ts` (type augmentation), `companion/src/auth.ts`, `companion/src/hooks.server.ts`, `companion/src/lib/types.ts`, `companion/src/lib/computed.ts`, `companion/src/routes/+layout.server.ts`, `companion/src/routes/+layout.svelte`, `companion/src/routes/+page.server.ts`, `companion/src/routes/+page.svelte`, `companion/src/routes/admin/+layout.server.ts`, `companion/src/routes/admin/assign/+page.server.ts`, `companion/src/routes/admin/assign/+page.svelte`, `companion/src/routes/library/+page.svelte`, `companion/src/routes/characters/+page.server.ts`, `companion/src/routes/characters/+page.svelte`, `companion/src/routes/characters/[id]/+page.server.ts`, `companion/src/routes/characters/[id]/+page.svelte`, `companion/src/routes/api/sync/+server.ts` (CORS amendment)

---

## Blueprint 3.1 — Discord OAuth setup + player upsert

**Files:** `companion/src/auth.ts`, `companion/src/hooks.server.ts`, `companion/src/app.d.ts` (type augmentation)

### `companion/src/auth.ts`

```typescript
import { SvelteKitAuth } from '@auth/sveltekit';
import Discord from '@auth/sveltekit/providers/discord';
import { getDb } from '$lib/db';

// CRITICAL: SvelteKitAuth must be called as async (event) => ({...}) — NOT with a
// static config object. CF Pages bindings are in event.platform.env; they are NOT
// in process.env or SvelteKit's $env modules.
export const { handle, signIn, signOut } = SvelteKitAuth(async (event) => {
  const env = event.platform?.env;

  return {
    providers: [
      Discord({
        clientId:     env!.DISCORD_CLIENT_ID,
        clientSecret: env!.DISCORD_CLIENT_SECRET,
      }),
    ],
    secret: env!.AUTH_SECRET,

    callbacks: {
      // jwt() runs on sign-in (account + profile present) AND on every
      // session read (account undefined). The account guard ensures the
      // upsert and snowflake-binding logic runs ONLY on the initial sign-in.
      async jwt({ token, account, profile }) {
        if (account?.providerAccountId && profile) {
          const dp = profile as {
            id:           string;
            username:     string;
            global_name?: string | null;
            avatar?:      string | null;
          };

          // Upsert player row — env captured from outer SvelteKitAuth closure.
          // players.id IS the Discord snowflake PK (Blueprint 1.3).
          // is_gm is never touched here — set directly in DB by GM.
          const db = await getDb(env!);
          await db.execute({
            sql: `
              INSERT INTO players
                (id, username, display_name, avatar, is_gm, created_at, updated_at)
              VALUES
                (?, ?, ?, ?, 0, datetime('now'), datetime('now'))
              ON CONFLICT(id) DO UPDATE SET
                username     = excluded.username,
                display_name = excluded.display_name,
                avatar       = excluded.avatar,
                updated_at   = datetime('now')
            `,
            args: [
              account.providerAccountId,    // Discord snowflake — IS players.id PK
              dp.username,
              dp.global_name ?? null,
              dp.avatar      ?? null,       // raw avatar hash, not full CDN URL
            ],
          });

          // Pin Discord snowflake as JWT subject for session resolution.
          token.sub = account.providerAccountId;
        }
        return token;
      },

      // Surface token.sub (Discord snowflake) as session.user.id.
      // Without this, session.user.id is undefined from the default JWT shape.
      async session({ session, token }) {
        session.user.id = token.sub!;
        return session;
      },
    },
  };
});
```

> **[DEV DECISION]:** `@auth/sveltekit` import paths differ across v4 / v5 beta releases. At implementation time verify: (a) the correct import for the Discord provider — may be `@auth/sveltekit/providers/discord`, `@auth/core/providers/discord`, or `next-auth/providers/discord`; (b) whether the `(event) => config` function form is supported at the installed version. Auth.js v5 supports this form natively. If using v4, the lazy env pattern requires wrapping `SvelteKitAuth` calls differently — check the @auth/sveltekit CF Pages migration guide.

> **[DEV DECISION]:** `profile.global_name` is the Discord "display name" (new as of 2023). `profile.username` is the discriminator-free handle. If the installed Discord provider version does not expose `global_name` on the profile object, fall back to `profile.name` (the default Auth.js normalized field). Log the raw `profile` object on first run to confirm available fields.

> **[DEV DECISION]:** `profile.avatar` is the raw hash string (e.g., `"a_123abc"`). The full CDN URL is `https://cdn.discordapp.com/avatars/{profile.id}/{profile.avatar}.png`. Decide at implementation time whether to store the hash or the full URL. Storing the hash is preferred — it doesn't embed the server's CDN assumption, and the URL can be constructed client-side.

> **Type augmentation:** `session.user.id` is typed as `string | undefined` in the default Auth.js types. Add to `companion/src/app.d.ts`:
> ```typescript
> declare module '@auth/sveltekit' {
>   interface Session {
>     user: DefaultSession['user'] & { id: string };
>   }
> }
> ```
> Or use the `next-auth` augmentation pattern appropriate to the installed version.

### `companion/src/hooks.server.ts`

```typescript
import { sequence } from '@sveltejs/kit/hooks';
import type { Handle } from '@sveltejs/kit';
import { handle as authHandle } from './auth';

// authHandle: Auth.js session cookie management + /auth/* route interception.
//   Auth.js short-circuits /auth/* requests before layout load functions run —
//   no redirect loop risk on /auth/signin.
// appHandle: passthrough placeholder for future request-scoped middleware.
//   Route-level auth enforcement lives in layout load functions (Blueprint 3.3).
const appHandle: Handle = ({ event, resolve }) => resolve(event);

export const handle = sequence(authHandle, appHandle);
```

### Acceptance criteria (Task 1)

- `GET /auth/signin` renders the Discord OAuth button (provided by Auth.js)
- Completing the OAuth flow sets an authenticated session cookie
- First login creates a `players` row; subsequent logins update `username`, `display_name`, `avatar`
- `is_gm` remains `0` for new players; sign-in callback never writes to `is_gm`
- `session.user.id` equals the Discord snowflake (not Auth.js-generated UUID)
- `AUTH_SECRET`, `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET` documented in `.dev.vars.example`

---

## Blueprint 3.2 — GM character assignment page (`/admin/assign`)

**Files:** `companion/src/routes/admin/assign/+page.server.ts`, `companion/src/routes/admin/assign/+page.svelte`

### `companion/src/routes/admin/assign/+page.server.ts`

```typescript
import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getDb } from '$lib/db';

export const load: PageServerLoad = async ({ parent, platform }) => {
  // admin +layout.server.ts (Blueprint 3.3) enforces is_gm before this load runs.
  // The check below is a defensive fallback for direct invocation without the layout.
  const { player } = await parent();
  if (player.is_gm !== 1) throw error(403, 'Forbidden');

  const db = await getDb(platform!.env);

  const [unclaimedResult, playersResult] = await Promise.all([
    db.execute('SELECT id, char_name FROM characters WHERE player_id IS NULL ORDER BY char_name ASC'),
    db.execute('SELECT id, username FROM players ORDER BY username ASC'),
  ]);

  return {
    unclaimedCharacters: unclaimedResult.rows as Array<{ id: string; char_name: string }>,
    players:             playersResult.rows  as Array<{ id: string; username: string }>,
  };
};

export const actions: Actions = {
  assign: async ({ request, locals, platform }) => {
    // OWASP A01: Re-verify authorization server-side on every action.
    // Form actions do NOT re-run layout load functions — parent() data is
    // unavailable here. Query DB directly.
    const session = await locals.auth();
    if (!session?.user?.id) throw error(401, 'Unauthorized');

    const db = await getDb(platform!.env);

    const gmCheck = await db.execute({
      sql:  'SELECT is_gm FROM players WHERE id = ?',
      args: [session.user.id],
    });
    if ((gmCheck.rows[0]?.is_gm as number) !== 1) throw error(403, 'Forbidden');

    const formData    = await request.formData();
    const characterId = formData.get('characterId');
    const playerId    = formData.get('playerId');

    // Validate both fields are non-empty strings
    if (
      typeof characterId !== 'string' || characterId.length === 0 ||
      typeof playerId    !== 'string' || playerId.length    === 0
    ) {
      throw error(400, 'Missing required fields');
    }

    // AND player_id IS NULL guard: idempotent — double-assign silently no-ops
    // rather than throwing a DB error.
    await db.execute({
      sql:  `UPDATE characters SET player_id = ?, updated_at = datetime('now') WHERE id = ? AND player_id IS NULL`,
      args: [playerId, characterId],
    });

    // POST-Redirect-GET: prevents form resubmission on browser refresh
    throw redirect(303, '/admin/assign');
  },
};
```

> **[DEV DECISION]:** Form actions do not run layout load functions, so `parent()` is unavailable in `actions.assign`. The GM re-verification DB query is required — this is not redundant. Do not remove it.

> **[DEV DECISION]:** Assigning a character to a player who does not exist in the `players` table will succeed at the SQL level (FK is on `characters.player_id REFERENCES players(id)` — check if FK enforcement is on). At implementation time, consider whether a `SELECT id FROM players WHERE id = ?` pre-check is needed, or whether FK rejection is an acceptable error response. For V1 with controlled GM usage, FK rejection is acceptable.

### `companion/src/routes/admin/assign/+page.svelte`

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>Assign Characters</h1>

{#if data.unclaimedCharacters.length === 0}
  <p>All characters have been assigned.</p>
{:else}
  {#each data.unclaimedCharacters as character}
    <!-- One <form> per character row — simplest PRG implementation -->
    <form method="POST" action="?/assign" class="assign-row">
      <input type="hidden" name="characterId" value={character.id} />
      <span class="char-name">{character.char_name}</span>
      <select name="playerId" required>
        <option value="" disabled selected>Select player…</option>
        {#each data.players as player}
          <option value={player.id}>{player.username}</option>
        {/each}
      </select>
      <button type="submit">Assign</button>
    </form>
  {/each}
{/if}
```

> **Note:** Each form is a flat `div`-level element, not a `<tr>`. Avoid wrapping `<form>` inside `<tr>` — that is invalid HTML and browsers will hoist the form element out, breaking value binding.

### Acceptance criteria (Task 2)

- `/admin/assign` returns 403 for non-GM authenticated users
- `/admin/assign` redirects to `/auth/signin` for unauthenticated users (via root layout guard)
- Page lists only characters where `player_id IS NULL`
- Submitting a row's form sets `player_id` to the selected player's `id`
- Assigning an already-assigned character (race condition) does not throw a DB error
- After successful assignment, character no longer appears on page reload

---

## Blueprint 3.3 — Route auth guards (layout load functions)

**Files:** `companion/src/routes/+layout.server.ts`, `companion/src/routes/admin/+layout.server.ts`

### `companion/src/routes/+layout.server.ts`

```typescript
import { redirect, error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { getDb } from '$lib/db';

// Single point of auth enforcement for all routes under /.
// Result is consumed via await parent() in all child +page.server.ts files —
// no per-route DB call for player identity (one SELECT per request).
export const load: LayoutServerLoad = async ({ locals, platform }) => {
  // locals.auth() is populated by authHandle (Blueprint 3.1 hooks.server.ts).
  // Returns null if no valid session cookie is present.
  const session = await locals.auth();
  if (!session?.user?.id) throw redirect(302, '/auth/signin');

  // players.id IS the Discord snowflake — direct PK lookup, no secondary index needed.
  const db = await getDb(platform!.env);
  const result = await db.execute({
    sql:  'SELECT id, is_gm FROM players WHERE id = ?',
    args: [session.user.id],
  });

  const row = result.rows[0];
  // Edge case: OAuth succeeded but upsert in jwt() callback failed (DB error at sign-in).
  // Return 500 rather than 403 — this indicates an infrastructure problem, not auth failure.
  if (!row) throw error(500, 'Player record missing');

  return {
    session,
    player: {
      id:    row.id    as string,
      is_gm: row.is_gm as number,
    },
  };
};
```

> **[DEV DECISION]:** `/auth/*` routes served by Auth.js are intercepted by `authHandle` before SvelteKit's routing resolves. The root layout load function does NOT run for `/auth/signin`, `/auth/callback/*`, or `/auth/signout`. Verify this behavior at implementation time with a quick test (log in the load function; confirm no log entry during the OAuth callback). If using an `@auth/sveltekit` version where this interception is not guaranteed, add a URL prefix guard:
> ```typescript
> if (url.pathname.startsWith('/auth')) return {};
> ```

> **[DEV DECISION]:** `platform!.env` non-null assertion — same caveat as Blueprint 1.4 note. `event.platform` is typed optional. If `platform` is null (e.g., running in `vite dev` without wrangler), `getDb` will throw. For local dev, start the app via `wrangler pages dev` to ensure `platform.env` is populated.

### `companion/src/routes/admin/+layout.server.ts`

```typescript
import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

// Fast gate: player record is already loaded by the root layout.
// This load runs only for /admin/* routes.
export const load: LayoutServerLoad = async ({ parent }) => {
  const { player } = await parent();
  if (player.is_gm !== 1) throw error(403, 'Forbidden');
  return {};
};
```

### Acceptance criteria (Task 3)

- All routes under `/` (excluding `/auth/*`) redirect unauthenticated users to `/auth/signin`
- `/admin/*` routes return 403 for authenticated non-GM users
- `data.player.is_gm` resolves correctly for both player (`0`) and GM (`1`) accounts
- Root layout DB query is one `SELECT` per request, not repeated per child route

---

## Blueprint 3.4 — App shell (layout component + home redirect)

**Files:** `companion/src/routes/+layout.svelte`, `companion/src/routes/+page.server.ts`, `companion/src/routes/+page.svelte`, `companion/src/routes/library/+page.svelte`

### `companion/src/routes/+layout.svelte`

```svelte
<script lang="ts">
  import type { LayoutData } from './$types';
  export let data: LayoutData;
</script>

<nav>
  <a href="/">Home</a>
  <a href="/characters">Characters</a>
  <a href="/library">Game Library</a>
  {#if data.player?.is_gm === 1}
    <a href="/admin/assign">Assign Characters</a>
  {/if}
  <span class="nav-user">
    <!-- session.user.name = Discord username (set by Auth.js Discord provider default mapping) -->
    {data.session.user?.name ?? data.session.user?.id}
  </span>
  <a href="/auth/signout">Sign Out</a>
</nav>

<main>
  <slot />
</main>
```

> **Note:** `data.player` and `data.session` are provided by `+layout.server.ts` (Blueprint 3.3). They are always defined for authenticated routes — the layout guard throws a redirect before this renders for unauthenticated users.

> **[DEV DECISION]:** The "Sign Out" link points to `/auth/signout` (GET). Auth.js v5 changed sign-out to require a POST for CSRF protection. If the installed version requires POST, replace the `<a>` with a `<form method="POST" action="/auth/signout">` button. Check the @auth/sveltekit changelog at implementation time.

### `companion/src/routes/+page.server.ts`

```typescript
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';

// Home page: redirect to /characters if player has at least one assigned character.
// If not, fall through and render the "No characters assigned" message in +page.svelte.
export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();

  const db = await getDb(platform!.env);
  const result = await db.execute({
    sql:  'SELECT id FROM characters WHERE player_id = ? LIMIT 1',
    args: [player.id],
  });

  if (result.rows.length > 0) throw redirect(302, '/characters');

  return {};
};
```

### `companion/src/routes/+page.svelte`

```svelte
<!-- Rendered only when player has no assigned characters (no redirect from +page.server.ts) -->
<h1>Welcome</h1>
<p>No characters have been assigned to your account yet. Check back after your GM assigns one.</p>
```

### `companion/src/routes/library/+page.svelte`

```svelte
<h1>Game Library</h1>
<p>Coming in Phase 4.</p>
```

### Acceptance criteria (Task 4)

- Nav renders on all authenticated pages with correct links
- GM-only "Assign Characters" nav link is visible only when `player.is_gm === 1`
- `/` redirects to `/characters` for players with at least one assigned character
- `/` renders the "No characters assigned" message for players with zero assigned characters (not an error or redirect loop)
- `/library` renders the stub without a runtime error

---

## Implementation Order — Phase 3 (Blueprints 3.1–3.4)

| Step | Blueprint | File | Action | Hard depends on |
|---|---|---|---|---|
| 1 | 3.1 | `auth.ts` | Implement SvelteKitAuth + jwt + session callbacks + player upsert | Phase 2 deployed; `players` table exists (BP 1.3) |
| 2 | 3.1 | `hooks.server.ts` | Wire `authHandle` via `sequence()` | Step 1 |
| 3 | 3.3 | `routes/+layout.server.ts` | Root auth guard + player SELECT | Step 2 (`locals.auth()` available) |
| 4 | 3.3 | `routes/admin/+layout.server.ts` | GM gate via `parent()` | Step 3 |
| 5 | 3.4 | `routes/+layout.svelte` | Nav + slot | Step 3 (session/player shape known) |
| 6 | 3.4 | `routes/+page.server.ts` | Home redirect load | Step 3 |
| 7 | 3.4 | `routes/+page.svelte` + `library/+page.svelte` | Static stubs | Step 5 |
| 8 | 3.2 | `admin/assign/+page.server.ts` | Load + actions.assign | Steps 3 + 4 complete |
| 9 | 3.2 | `admin/assign/+page.svelte` | Form view | Step 8 |

---

*Blueprints 3.5–3.8 continue in Part B.*

---


---

## Blueprint 3.5 — Character List Page (`/characters`)

**Files:** `companion/src/routes/characters/+page.server.ts`, `companion/src/routes/characters/+page.svelte`

### TypeScript interface

```typescript
// companion/src/routes/characters/+page.server.ts (local, or promote to $lib/types.ts)
interface CharacterSummary {
  id:            string;
  char_name:     string | null;
  campaign_name: string;
  synced_at:     string | null;
}
```

### `+page.server.ts`

```typescript
import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';

export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();
  const db = await getDb(platform!.env);

  const sql = player.is_gm === 1
    ? `SELECT c.id, c.char_name, c.synced_at, ca.name AS campaign_name
         FROM characters c
         JOIN campaigns ca ON c.campaign_id = ca.id
        ORDER BY c.char_name ASC`
    : `SELECT c.id, c.char_name, c.synced_at, ca.name AS campaign_name
         FROM characters c
         JOIN campaigns ca ON c.campaign_id = ca.id
        WHERE c.player_id = ?
        ORDER BY c.char_name ASC`;

  const args = player.is_gm === 1 ? [] : [player.id];
  const result = await db.execute({ sql, args });

  const characters: CharacterSummary[] = result.rows.map(row => ({
    id:            row.id            as string,
    char_name:     row.char_name     as string | null,
    campaign_name: row.campaign_name as string,
    synced_at:     row.synced_at     as string | null,
  }));

  return { characters };
};
```

### `+page.svelte`

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;

  // SQLite datetime('now') stores 'YYYY-MM-DD HH:MM:SS' UTC — render as-is with suffix.
  function formatSyncedAt(raw: string | null): string {
    if (!raw) return 'Never';
    return raw.replace('T', ' ').slice(0, 16) + ' UTC';
  }
</script>

<h1>Characters</h1>

{#if data.characters.length === 0}
  <p>No characters assigned.</p>
{:else}
  <ul class="character-list">
    {#each data.characters as char}
      <li>
        <a href="/characters/{char.id}" class="character-card">
          <strong>{char.char_name ?? '(Unnamed)'}</strong>
          <span>{char.campaign_name}</span>
          <span>Last synced: {formatSyncedAt(char.synced_at)}</span>
        </a>
      </li>
    {/each}
  </ul>
{/if}
```

### Acceptance criteria

- Player sees only characters where `player_id = player.id`
- GM sees all characters regardless of `player_id`
- Each card links to `/characters/{id}`
- `synced_at` renders as `YYYY-MM-DD HH:mm UTC`; null renders as "Never"
- `characters.length === 0` renders "No characters assigned" — not an error or redirect

---

## Blueprint 3.6 — Character Detail Page (`/characters/[id]`)

**Files:** `companion/src/lib/types.ts`, `companion/src/routes/characters/[id]/+page.server.ts`, `companion/src/routes/characters/[id]/+page.svelte`

### TypeScript interfaces — `companion/src/lib/types.ts`

```typescript
// Single source of truth for character + rep row shapes.
// Imported by +page.server.ts, computed.ts, and the Svelte component.

// ── CharacterRow ─────────────────────────────────────────────
// Backbone (8 columns) + key scalar columns typed explicitly.
// All 129 scalar columns are present at runtime via SELECT *;
// the index signature [key: string]: unknown captures the remainder.
export interface CharacterRow {
  // Backbone
  id:                  string;
  player_id:           string | null;
  campaign_id:         string;
  roll20_character_id: string | null;
  sync_version:        number;
  synced_at:           string | null;
  created_at:          string | null;
  updated_at:          string | null;

  // Attribute totals (used in Overview tab + CM formulas in computed.ts)
  body: number | null;
  dex:  number | null;
  str:  number | null;
  cha:  number | null;
  int:  number | null;
  wil:  number | null;
  hum:  number | null;
  mag:  number | null;
  essence_total: number | null;

  // Dice pool totals (Overview tab)
  pool_spell:   number | null;
  pool_combat:  number | null;
  pool_control: number | null;
  pool_astral:  number | null;

  // Condition monitor — current checkbox state (0/null = empty, 1 = filled)
  cm_mental_l1:  number | null;  cm_mental_l2:  number | null;
  cm_mental_m1:  number | null;  cm_mental_m2:  number | null;  cm_mental_m3:  number | null;
  cm_mental_s1:  number | null;  cm_mental_s2:  number | null;  cm_mental_s3:  number | null;  cm_mental_s4: number | null;
  cm_mental_d:   number | null;
  cm_stun_l1:    number | null;  cm_stun_l2:    number | null;
  cm_stun_m1:    number | null;  cm_stun_m2:    number | null;  cm_stun_m3:    number | null;
  cm_stun_s1:    number | null;  cm_stun_s2:    number | null;  cm_stun_s3:    number | null;  cm_stun_s4:   number | null;
  cm_stun_d:     number | null;  cm_stun_u:     number | null;
  cm_physical_l1: number | null; cm_physical_l2: number | null;
  cm_physical_m1: number | null; cm_physical_m2: number | null; cm_physical_m3: number | null;
  cm_physical_s1: number | null; cm_physical_s2: number | null; cm_physical_s3: number | null; cm_physical_s4: number | null;
  cm_physical_d:  number | null; cm_physical_u:  number | null;
  cm_physical_overflow: number | null;
  cm_tn_mod:   number | null;
  cm_init_mod: number | null;

  // Money (computed.ts formattedMoney)
  money_gold:   number | null;
  money_silver: number | null;
  money_copper: number | null;

  // Identity (Bio tab)
  char_name:         string | null;
  char_race_station: string | null;
  char_sex:          string | null;
  char_age:          string | null;
  char_description:  string | null;
  char_notes:        string | null;

  // Karma scalars (Bio tab header)
  karma_good:  number | null;
  karma_used:  number | null;
  karma_total: number | null;
  karma_pool:  number | null;

  // ... all remaining scalar columns from characters DDL present at runtime via SELECT *
  [key: string]: unknown;
}

// ── Rep-table row interfaces ─────────────────────────────────
// Column names match Phase 1 DDL exactly.

export interface RepSkillRow {
  id: string; character_id: string; roll20_row_id: string;
  skill_name:        string | null;
  skill_linked_attr: string | null;
  skill_general:     string | null;
  skill_spec:        number | null;
  skill_base:        number | null;
  skill_foci:        number | null;
  skill_misc:        number | null;
  skill_total:       number | null;
}

export interface RepMutationRow {
  id: string; character_id: string; roll20_row_id: string;
  mutation_name:    string | null;
  mutation_level:   number | null;
  mutation_essence: number | null;
  mutation_bp_cost: number | null;
  mutation_effect:  string | null;
}

export interface RepAdeptPowerRow {
  id: string; character_id: string; roll20_row_id: string;
  power_name:          string | null;
  power_level:         number | null;
  power_pp_cost:       string | null;
  power_pp_cost_value: number | null;
  power_effect:        string | null;
}

export interface RepSpellRow {
  id: string; character_id: string; roll20_row_id: string;
  spell_name:  string | null;
  spell_force: number | null;
  spell_drain: string | null;
}

export interface RepFocusRow {
  id: string; character_id: string; roll20_row_id: string;
  focus_name:   string | null;
  focus_type:   string | null;
  focus_force:  number | null;
  focus_bonded: number | null;
  focus_notes:  string | null;
}

export interface RepWeaponRow {
  id: string; character_id: string; roll20_row_id: string;
  weapon_name:          string | null;
  weapon_type:          string | null;
  weapon_modifiers:     string | null;
  weapon_power:         number | null;
  weapon_damage:        string | null;
  weapon_conceal:       number | null;
  weapon_reach:         number | null;
  weapon_ep:            number | null;
  weapon_range_short:   string | null;
  weapon_range_medium:  string | null;
  weapon_range_long:    string | null;
  weapon_range_extreme: string | null;
}

export interface RepEquipmentRow {
  id: string; character_id: string; roll20_row_id: string;
  equip_name:        string | null;
  equip_description: string | null;
  equip_ep:          number | null;
}

export interface RepContactRow {
  id: string; character_id: string; roll20_row_id: string;
  contact_name:  string | null;
  contact_info:  string | null;
  contact_level: string | null;
}

export interface RepKarmaRow {
  id: string; character_id: string; roll20_row_id: string;
  karma_event:  string | null;
  karma_amount: number | null;
}

export interface RepMilestoneRow {
  id: string; character_id: string; roll20_row_id: string;
  milestone_trial:   string | null;
  milestone_tier1:   string | null;
  milestone_tier2:   string | null;
  milestone_tier3:   string | null;
  milestone_current: number | null;
}

export interface RepData {
  skills:       RepSkillRow[];
  mutations:    RepMutationRow[];
  adept_powers: RepAdeptPowerRow[];
  spells:       RepSpellRow[];
  foci:         RepFocusRow[];
  weapons:      RepWeaponRow[];
  equipment:    RepEquipmentRow[];
  contacts:     RepContactRow[];
  karma:        RepKarmaRow[];
  milestones:   RepMilestoneRow[];
}
```

> **[DEV DECISION]:** `CharacterRow` uses an index signature `[key: string]: unknown` to cover the remaining ~80 scalar columns not explicitly listed. TypeScript will require explicit casts when accessing unlisted columns. If strict column access is preferred, replace the index signature with the full 129-column explicit listing at implementation time.

### `+page.server.ts`

```typescript
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { computeCharacter } from '$lib/computed';
import type { CharacterRow, RepData } from '$lib/types';

export const load: PageServerLoad = async ({ parent, params, platform }) => {
  const { player } = await parent();
  const db = await getDb(platform!.env);

  // 1. Fetch character scalar row
  const charResult = await db.execute({
    sql:  'SELECT * FROM characters WHERE id = ?',
    args: [params.id],
  });
  if (charResult.rows.length === 0) throw error(404, 'Character not found');

  const character = charResult.rows[0] as unknown as CharacterRow;

  // 2. Access control: owner OR GM
  if (player.is_gm !== 1 && character.player_id !== player.id) {
    throw error(403, 'Forbidden');
  }

  // 3. All 10 rep tables in parallel — one HTTP round-trip each over Turso HTTP transport
  const [
    skills, mutations, adept_powers, spells, foci,
    weapons, equipment, contacts, karma, milestones,
  ] = await Promise.all([
    db.execute({ sql: 'SELECT * FROM rep_skills        WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_mutations      WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_adept_powers   WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_spells         WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_foci           WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_weapons        WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_equipment      WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_contacts       WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_karma          WHERE character_id = ?', args: [params.id] }),
    db.execute({ sql: 'SELECT * FROM rep_milestones     WHERE character_id = ?', args: [params.id] }),
  ]);

  const repData: RepData = {
    skills:       skills.rows       as unknown as RepData['skills'],
    mutations:    mutations.rows    as unknown as RepData['mutations'],
    adept_powers: adept_powers.rows as unknown as RepData['adept_powers'],
    spells:       spells.rows       as unknown as RepData['spells'],
    foci:         foci.rows         as unknown as RepData['foci'],
    weapons:      weapons.rows      as unknown as RepData['weapons'],
    equipment:    equipment.rows    as unknown as RepData['equipment'],
    contacts:     contacts.rows     as unknown as RepData['contacts'],
    karma:        karma.rows        as unknown as RepData['karma'],
    milestones:   milestones.rows   as unknown as RepData['milestones'],
  };

  // 4. Pure computation — no side effects, no DB calls
  const computed = computeCharacter(character, repData);

  return { character, repData, computed };
};
```

> **[DEV DECISION]:** `Promise.all` for 10 parallel Turso HTTP requests is the recommended path. If connection limits cause 429 errors or socket hangs in production, fall back to sequential execution via Promise chaining.

### `+page.svelte` — tabbed viewer

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;

  type TabId = 'overview' | 'skills' | 'magic' | 'gear' | 'bio';
  let activeTab: TabId = 'overview';
</script>

<header>
  <h1>{data.character.char_name ?? '(Unnamed)'}</h1>
  <p class="sync-meta">
    Sync version {data.character.sync_version} ·
    Last synced: {data.character.synced_at ?? 'never'}
  </p>
</header>

<nav class="tab-bar">
  {#each (['overview', 'skills', 'magic', 'gear', 'bio'] as TabId[]) as tab}
    <button class:active={activeTab === tab} on:click={() => (activeTab = tab)}>
      {tab.charAt(0).toUpperCase() + tab.slice(1)}
    </button>
  {/each}
</nav>

<!-- ── Overview ─────────────────────────────────────────────── -->
{#if activeTab === 'overview'}
  <section>
    <h2>Attributes</h2>
    <dl>
      <dt>Body</dt>    <dd>{data.character.body ?? '—'}</dd>
      <dt>Dex</dt>     <dd>{data.character.dex ?? '—'}</dd>
      <dt>Str</dt>     <dd>{data.character.str ?? '—'}</dd>
      <dt>Cha</dt>     <dd>{data.character.cha ?? '—'}</dd>
      <dt>Int</dt>     <dd>{data.character.int ?? '—'}</dd>
      <dt>Wil</dt>     <dd>{data.character.wil ?? '—'}</dd>
      <dt>Hum</dt>     <dd>{data.character.hum ?? '—'}</dd>
      <dt>Essence</dt> <dd>{data.character.essence_total ?? '—'}</dd>
    </dl>
  </section>

  <section>
    <h2>Condition Monitor</h2>
    <dl>
      <dt>Mental boxes</dt>   <dd>{data.computed.conditionMonitorBoxes.mental}</dd>
      <dt>Stun boxes</dt>     <dd>{data.computed.conditionMonitorBoxes.stun}</dd>
      <dt>Physical boxes</dt> <dd>{data.computed.conditionMonitorBoxes.physical}</dd>
    </dl>
    <!-- [DEV DECISION]: Render cm_mental_*, cm_stun_*, cm_physical_* as a box grid.
         Each null/0 = empty, 1 = filled. Column order follows DDL: l1, l2, m1–m3, s1–s4, d (+ u for stun/physical). -->
  </section>

  <section>
    <h2>Dice Pools</h2>
    <dl>
      <dt>Combat</dt>  <dd>{data.character.pool_combat ?? '—'}</dd>
      <dt>Spell</dt>   <dd>{data.character.pool_spell ?? '—'}</dd>
      <dt>Control</dt> <dd>{data.character.pool_control ?? '—'}</dd>
      <dt>Astral</dt>  <dd>{data.character.pool_astral ?? '—'}</dd>
    </dl>
  </section>

<!-- ── Skills ──────────────────────────────────────────────── -->
{:else if activeTab === 'skills'}
  <section>
    <h2>Skills</h2>
    {#if data.repData.skills.length === 0}
      <p>No skills.</p>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Skill</th><th>Linked Attr</th><th>Base</th>
            <th>Foci</th><th>Misc</th><th>Total</th>
          </tr>
        </thead>
        <tbody>
          {#each data.repData.skills as s}
            <tr>
              <td>{s.skill_name ?? '—'}</td>
              <td>{s.skill_linked_attr ?? '—'}</td>
              <td>{s.skill_base ?? '—'}</td>
              <td>{s.skill_foci ?? '—'}</td>
              <td>{s.skill_misc ?? '—'}</td>
              <td>{s.skill_total ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

<!-- ── Magic ───────────────────────────────────────────────── -->
{:else if activeTab === 'magic'}
  <section>
    <h2>Spells</h2>
    {#if data.repData.spells.length === 0}
      <p>No spells.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Force</th><th>Drain</th></tr></thead>
        <tbody>
          {#each data.repData.spells as s}
            <tr>
              <td>{s.spell_name ?? '—'}</td>
              <td>{s.spell_force ?? '—'}</td>
              <td>{s.spell_drain ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Foci</h2>
    {#if data.repData.foci.length === 0}
      <p>No foci.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Type</th><th>Force</th><th>Bonded</th><th>Notes</th></tr></thead>
        <tbody>
          {#each data.repData.foci as f}
            <tr>
              <td>{f.focus_name ?? '—'}</td>
              <td>{f.focus_type ?? '—'}</td>
              <td>{f.focus_force ?? '—'}</td>
              <td>{f.focus_bonded === 1 ? 'Yes' : 'No'}</td>
              <td>{f.focus_notes ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Adept Powers</h2>
    {#if data.repData.adept_powers.length === 0}
      <p>No adept powers.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Level</th><th>PP Cost</th><th>Effect</th></tr></thead>
        <tbody>
          {#each data.repData.adept_powers as p}
            <tr>
              <td>{p.power_name ?? '—'}</td>
              <td>{p.power_level ?? '—'}</td>
              <td>{p.power_pp_cost ?? '—'}</td>
              <td>{p.power_effect ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Mutations</h2>
    {#if data.repData.mutations.length === 0}
      <p>No mutations.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Level</th><th>Essence</th><th>BP Cost</th><th>Effect</th></tr></thead>
        <tbody>
          {#each data.repData.mutations as m}
            <tr>
              <td>{m.mutation_name ?? '—'}</td>
              <td>{m.mutation_level ?? '—'}</td>
              <td>{m.mutation_essence ?? '—'}</td>
              <td>{m.mutation_bp_cost ?? '—'}</td>
              <td>{m.mutation_effect ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

<!-- ── Gear ────────────────────────────────────────────────── -->
{:else if activeTab === 'gear'}
  <section>
    <h2>Weapons</h2>
    {#if data.repData.weapons.length === 0}
      <p>No weapons.</p>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Name</th><th>Type</th><th>Power</th><th>Damage</th>
            <th>Conceal</th><th>Reach</th><th>EP</th>
          </tr>
        </thead>
        <tbody>
          {#each data.repData.weapons as w}
            <tr>
              <td>{w.weapon_name ?? '—'}</td>
              <td>{w.weapon_type ?? '—'}</td>
              <td>{w.weapon_power ?? '—'}</td>
              <td>{w.weapon_damage ?? '—'}</td>
              <td>{w.weapon_conceal ?? '—'}</td>
              <td>{w.weapon_reach ?? '—'}</td>
              <td>{w.weapon_ep ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Equipment</h2>
    {#if data.repData.equipment.length === 0}
      <p>No equipment.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Description</th><th>EP</th></tr></thead>
        <tbody>
          {#each data.repData.equipment as e}
            <tr>
              <td>{e.equip_name ?? '—'}</td>
              <td>{e.equip_description ?? '—'}</td>
              <td>{e.equip_ep ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Money</h2>
    <dl>
      <dt>Gold</dt>   <dd>{data.computed.formattedMoney.gold ?? 0}</dd>
      <dt>Silver</dt> <dd>{data.computed.formattedMoney.silver ?? 0}</dd>
      <dt>Copper</dt> <dd>{data.computed.formattedMoney.copper ?? 0}</dd>
    </dl>
  </section>

<!-- ── Bio ─────────────────────────────────────────────────── -->
{:else if activeTab === 'bio'}
  <section>
    <h2>Identity</h2>
    <dl>
      <dt>Name</dt>         <dd>{data.character.char_name ?? '—'}</dd>
      <dt>Race/Station</dt> <dd>{data.character.char_race_station ?? '—'}</dd>
      <dt>Sex</dt>          <dd>{data.character.char_sex ?? '—'}</dd>
      <dt>Age</dt>          <dd>{data.character.char_age ?? '—'}</dd>
    </dl>
    {#if data.character.char_description}
      <h3>Description</h3>
      <p>{data.character.char_description}</p>
    {/if}
    {#if data.character.char_notes}
      <h3>Notes</h3>
      <p>{data.character.char_notes}</p>
    {/if}
  </section>

  <section>
    <h2>Karma</h2>
    <dl>
      <dt>Total earned</dt> <dd>{data.character.karma_total ?? 0}</dd>
      <dt>Used</dt>         <dd>{data.character.karma_used ?? 0}</dd>
      <dt>Good karma</dt>   <dd>{data.character.karma_good ?? 0}</dd>
      <dt>Ledger total</dt> <dd>{data.computed.totalKarma}</dd>
    </dl>
    {#if data.repData.karma.length > 0}
      <h3>Karma Ledger</h3>
      <table>
        <thead><tr><th>Event</th><th>Amount</th><th>Running Total</th></tr></thead>
        <tbody>
          {#each data.computed.karmaLedgerRunningTotals as entry}
            <tr>
              <td>{entry.karma_event ?? '—'}</td>
              <td>{entry.karma_amount}</td>
              <td>{entry.runningTotal}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Milestones</h2>
    {#if data.repData.milestones.length === 0}
      <p>No milestones.</p>
    {:else}
      <table>
        <thead>
          <tr><th>Trial</th><th>Tier 1</th><th>Tier 2</th><th>Tier 3</th><th>Current</th></tr>
        </thead>
        <tbody>
          {#each data.repData.milestones as m}
            <tr>
              <td>{m.milestone_trial ?? '—'}</td>
              <td>{m.milestone_tier1 ?? '—'}</td>
              <td>{m.milestone_tier2 ?? '—'}</td>
              <td>{m.milestone_tier3 ?? '—'}</td>
              <td>{m.milestone_current ?? 0}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>

  <section>
    <h2>Contacts</h2>
    {#if data.repData.contacts.length === 0}
      <p>No contacts.</p>
    {:else}
      <table>
        <thead><tr><th>Name</th><th>Info</th><th>Level</th></tr></thead>
        <tbody>
          {#each data.repData.contacts as c}
            <tr>
              <td>{c.contact_name ?? '—'}</td>
              <td>{c.contact_info ?? '—'}</td>
              <td>{c.contact_level ?? '—'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </section>
{/if}
```

### Acceptance criteria

- `/characters/{id}` returns 404 for unknown UUID
- `/characters/{id}` returns 403 for authenticated non-owner non-GM
- GM can view any character's detail page regardless of `player_id`
- All 5 tabs render; zero-row rep sections show empty-state text — not an error
- `sync_version` and `synced_at` visible in the page header
- `RepData` and `CharacterRow` column names match Phase 1 DDL exactly

---

## Blueprint 3.7 — Computed Fields Module (`computed.ts`)

**File:** `companion/src/lib/computed.ts`

```typescript
import type { CharacterRow, RepData } from '$lib/types';

export interface ComputedFields {
  totalKarma: number;
  conditionMonitorBoxes: {
    mental:   number; // Math.ceil(wil / 2) + 8  — SR3 Mental CM track
    stun:     number; // Math.ceil(wil / 2) + 8  — SR3 Stun CM track [DEV DECISION: see note]
    physical: number; // Math.ceil(body / 2) + 8 — SR3 Physical CM track
  };
  formattedMoney: {
    gold:   number | null;
    silver: number | null;
    copper: number | null;
  };
  karmaLedgerRunningTotals: Array<{
    karma_event:  string | null;
    karma_amount: number;
    runningTotal: number;
  }>;
}

export function computeCharacter(character: CharacterRow, repData: RepData): ComputedFields {
  // ── totalKarma ────────────────────────────────────────────
  const totalKarma = repData.karma.reduce(
    (sum, row) => sum + (row.karma_amount ?? 0),
    0
  );

  // ── conditionMonitorBoxes ─────────────────────────────────
  const wil  = character.wil  ?? 0;
  const body = character.body ?? 0;
  const conditionMonitorBoxes = {
    mental:   Math.ceil(wil  / 2) + 8,
    stun:     Math.ceil(wil  / 2) + 8,
    physical: Math.ceil(body / 2) + 8,
  };

  // ── formattedMoney ────────────────────────────────────────
  // Raw scalars only — no currency conversion.
  const formattedMoney = {
    gold:   character.money_gold,
    silver: character.money_silver,
    copper: character.money_copper,
  };

  // ── karmaLedgerRunningTotals ──────────────────────────────
  // Sort by id ASC (TEXT collation). UUIDs from rep_karma are expected to be
  // insertion-ordered by Roll20 row creation. See DEV DECISION note below.
  const sorted = [...repData.karma].sort((a, b) => a.id.localeCompare(b.id));
  let running = 0;
  const karmaLedgerRunningTotals = sorted.map(row => {
    running += row.karma_amount ?? 0;
    return {
      karma_event:  row.karma_event,
      karma_amount: row.karma_amount ?? 0,
      runningTotal: running,
    };
  });

  return { totalKarma, conditionMonitorBoxes, formattedMoney, karmaLedgerRunningTotals };
}
```

> **[DEV DECISION]:** `conditionMonitorBoxes.stun` uses `wil` per standard SR3 rules. If the campaign's 3-track system derives Stun from `body`, change to `Math.ceil(body / 2) + 8`. Verify with GM before final implementation.

> **[DEV DECISION]:** `karmaLedgerRunningTotals` sorts by `id ASC` (TEXT/UUID collation). If Roll20 assigns random (non-monotonic) UUIDs to rep rows, the chronological order will be incorrect. Verify with real Roll20 sync data during integration testing. Safe fix if needed: add a `sequence` INTEGER column to `rep_karma` during a Phase 1 schema amendment, or sort by `roll20_row_id` if Roll20 encodes insertion order in that value.

### Acceptance criteria

- `computeCharacter` is synchronous and has zero side effects
- `totalKarma` sums positive and negative `karma_amount` values; treats `null` as 0
- Last entry in `karmaLedgerRunningTotals` has `runningTotal === totalKarma`
- CM formula sanity: `wil=4` → `mental=stun=10`; `body=6` → `physical=11`
- Module imports only `$lib/types` — no DB, no `fetch`, no async

---

## Blueprint 3.8 — CORS Headers on `/api/sync`

**File:** `companion/src/routes/api/sync/+server.ts` (amend existing file from Blueprint 2.2)

### Module-level additions

```typescript
// Add near the top of the file, after imports.
//
// [DEV DECISION]: For single-deployment V1, hardcode the production domain.
// For multi-environment support, use:
//   import { PUBLIC_APP_ORIGIN } from '$env/static/public';
// and set PUBLIC_APP_ORIGIN in the CF Pages environment dashboard.

const APP_ORIGIN = 'https://your-app.pages.dev'; // replace at implementation time

const CORS_HEADERS = {
  'Access-Control-Allow-Origin':  APP_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Campaign-Secret',
} as const;
```

### OPTIONS handler (new export)

```typescript
import type { RequestHandler } from './$types';

// Handles CORS preflight requests from the Roll20 client.
export const OPTIONS: RequestHandler = () => {
  return new Response(null, {
    status: 200,
    headers: CORS_HEADERS,
  });
};
```

### POST handler — CORS injection pattern

```typescript
// In every `return new Response(...)` inside the POST handler, spread CORS_HEADERS:
//
//   return new Response(JSON.stringify(body), {
//     status: 200,
//     headers: {
//       ...CORS_HEADERS,
//       'Content-Type': 'application/json',
//     },
//   });
//
// Apply to: success (200), validation errors (400), auth errors (403), size errors (413).
// Do NOT add CORS headers inside catch blocks that return 500 — infrastructure failures
// should not declare themselves CORS-accessible to untrusted origins.
```

> **[DEV DECISION]:** CORS headers on 4xx error responses are optional for preflight correctness, but they allow the Roll20 client to read error body text cross-origin — useful for debugging sync failures in production. Recommended: add to all 2xx and 4xx responses. Omit from 5xx.

> **[DEV DECISION]:** `APP_ORIGIN` must be the exact origin of the CF Pages deployment (including protocol, no trailing slash). If a custom domain is configured, use the custom domain, not the `.pages.dev` subdomain — both work, but the browser sends the Origin header matching the page's domain. If the app is accessed via both, a whitelist check (`ALLOWED_ORIGINS.includes(request.headers.get('Origin'))`) is the correct pattern, but is unnecessary for a single-domain solo-maintainer V1.

### Acceptance criteria

- `OPTIONS /api/sync` returns 200 with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`
- `POST /api/sync` success and 4xx responses include `Access-Control-Allow-Origin` scoped to the deployment domain
- `Access-Control-Allow-Origin` value is never `*`
- Existing POST handler validation logic is unchanged — only CORS header injection is added

---

## Implementation Order — Phase 3 (Blueprints 3.1–3.8)

| Step | Blueprint | File | Action | Hard depends on |
|---|---|---|---|---|
| 1 | 3.1 | `src/auth.ts` | SvelteKitAuth + jwt + session callbacks + player upsert | Phase 2 deployed; `players` table (BP 1.3) |
| 2 | 3.1 | `src/hooks.server.ts` | Wire `authHandle` via `sequence()` | Step 1 |
| 3 | 3.3 | `routes/+layout.server.ts` | Root auth guard + `player` SELECT | Step 2 (`locals.auth()` available) |
| 4 | 3.3 | `routes/admin/+layout.server.ts` | GM gate via `parent()` | Step 3 |
| 5 | 3.4 | `routes/+layout.svelte` | Nav + slot | Step 3 (session/player shape known) |
| 6 | 3.4 | `routes/+page.server.ts` | Home redirect load | Step 3 |
| 7 | 3.4 | `routes/+page.svelte` + `library/+page.svelte` | Static stubs | Step 5 |
| 8 | 3.2 | `routes/admin/assign/+page.server.ts` | Character list load + `actions.assign` | Steps 3 + 4 |
| 9 | 3.2 | `routes/admin/assign/+page.svelte` | Assignment form view | Step 8 |
| 10 | 3.7 | `src/lib/types.ts` | `CharacterRow`, `RepData`, all 10 rep row interfaces | Step 3 (data shape known) |
| 11 | 3.7 | `src/lib/computed.ts` | `computeCharacter` pure function + `ComputedFields` | Step 10 |
| 12 | 3.5 | `routes/characters/+page.server.ts` | Character list load (GM/player branch) | Steps 3 + 8 |
| 13 | 3.5 | `routes/characters/+page.svelte` | Character card list + empty state | Step 12 |
| 14 | 3.6 | `routes/characters/[id]/+page.server.ts` | Detail load + access check + 10 rep queries + compute | Steps 10 + 11 + 12 |
| 15 | 3.6 | `routes/characters/[id]/+page.svelte` | 5-tab viewer | Steps 11 + 14 |
| 16 | 3.8 | `routes/api/sync/+server.ts` | Add `OPTIONS` handler + CORS headers to POST | Independent; complete before E2E browser testing |

---

*Phase 3 blueprints complete (3.1–3.8). Continuing to Phase 4.*

---

# Layer 3 — Phase 4: Game Library

**Files touched in this phase (Blueprints 4.1–4.4):**
- `companion/src/lib/catalog-config.ts` (new)
- `companion/src/lib/components/CatalogForm.svelte` (new, Blueprint 4.3c)
- `companion/src/routes/library/+layout.svelte` (new)
- `companion/src/routes/library/+page.server.ts` (new)
- `companion/src/routes/library/+page.svelte` (replace Phase 3 stub)
- `companion/src/routes/library/[catalog]/+page.server.ts` (new)
- `companion/src/routes/library/[catalog]/+page.svelte` (new)
- `companion/src/routes/library/[catalog]/new/+page.server.ts` (new)
- `companion/src/routes/library/[catalog]/new/+page.svelte` (new)
- `companion/src/routes/library/[catalog]/[id]/edit/+page.server.ts` (new)
- `companion/src/routes/library/[catalog]/[id]/edit/+page.svelte` (new)

---

## Blueprint 4.1 — Library Landing Page

**Files:** `companion/src/routes/library/+page.server.ts`, `companion/src/routes/library/+page.svelte`

### `+page.server.ts`

```typescript
import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { CATALOG_CONFIG } from '$lib/catalog-config';

export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();
  const db = getDb(platform!.env);

  const entries = Object.entries(CATALOG_CONFIG);

  // 11 parallel COUNT queries — table names from trusted constant only
  const countResults = await Promise.all(
    entries.map(([, cfg]) =>
      db.execute({ sql: `SELECT COUNT(*) AS count FROM ${cfg.table}`, args: [] })
    )
  );

  const counts: Record<string, number> = {};
  for (let i = 0; i < entries.length; i++) {
    const [slug] = entries[i];
    // libSQL may return INTEGER as bigint — Number() normalises both
    counts[slug] = Number(
      (countResults[i].rows[0] as { count: number | bigint }).count
    );
  }

  return { counts, isGm: player.is_gm === 1 };
};
```

### `+page.svelte`

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  import { CATALOG_CONFIG } from '$lib/catalog-config';

  let { data }: { data: PageData } = $props();
  const catalogEntries = Object.entries(CATALOG_CONFIG);
</script>

<h1>Game Library</h1>

<div class="library-grid">
  {#each catalogEntries as [slug, cfg]}
    <div class="library-card">
      <h2>{cfg.label}</h2>
      <p class="entry-count">{data.counts[slug] ?? 0} entries</p>
      <a href="/library/{slug}">Browse →</a>
      {#if data.isGm}
        <a href="/library/{slug}/new">+ Add entry</a>
      {/if}
    </div>
  {/each}
</div>

<style>
  .library-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  /* DEV DECISION: match app card styles */
</style>
```

Landing page imports `CATALOG_CONFIG` both server-side (drives COUNT query table names) and client-side (drives card rendering) — no catalog metadata is duplicated. `Object.entries()` insertion order is stable, so server-side count indices map back to slugs correctly.

### Acceptance criteria

- `/library` renders 11 category cards with live entry counts from the DB
- All 11 card links navigate to the correct sub-routes without 404
- "Add entry" links are visible only to GM users

---

## Blueprint 4.2 — Catalog Config + Dynamic List Pages

### Blueprint 4.2a — `catalog-config.ts`

**File:** `companion/src/lib/catalog-config.ts`

```typescript
export interface ColumnDef { key: string; label: string; }

export interface CatalogEntry {
  table: string;          // trusted SQL constant — interpolated, never from user input
  label: string;
  listColumns: ColumnDef[];
  filterFields: string[]; // drives server DISTINCT queries + client <select> dropdowns
  detailFields: ColumnDef[]; // [] means no expand panel for this catalog
}

export const CATALOG_CONFIG: Record<string, CatalogEntry> = {
  spells:              { table: 'ref_spells',             label: 'Spells',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'category', label: 'Category' },
      { key: 'type', label: 'Type' }, { key: 'target', label: 'Target' },
      { key: 'duration', label: 'Duration' }, { key: 'drain', label: 'Drain' },
    ],
    filterFields: ['category', 'type'],
    detailFields: [{ key: 'description', label: 'Description' }],
  },
  weapons:             { table: 'ref_weapons',            label: 'Weapons',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'type', label: 'Type' },
      { key: 'damage', label: 'Damage' }, { key: 'reach', label: 'Reach' },
      { key: 'conceal', label: 'Conceal' }, { key: 'ep', label: 'EP' },
      { key: 'cost', label: 'Cost' },
    ],
    filterFields: ['type'], detailFields: [],
  },
  armor:               { table: 'ref_armor',              label: 'Armor',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'location', label: 'Location' },
      { key: 'rating_p', label: 'Rating (P)' }, { key: 'rating_s', label: 'Rating (S)' },
      { key: 'rating_i', label: 'Rating (I)' }, { key: 'conceal', label: 'Conceal' },
      { key: 'ep', label: 'EP' }, { key: 'cost', label: 'Cost' },
    ],
    filterFields: ['location'], detailFields: [],
  },
  equipment:           { table: 'ref_equipment',          label: 'Equipment',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'conceal', label: 'Conceal' },
      { key: 'ep', label: 'EP' }, { key: 'cost', label: 'Cost' },
      { key: 'notes', label: 'Notes' },
    ],
    filterFields: [], detailFields: [],
  },
  skills:              { table: 'ref_skills',             label: 'Skills',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'linked_attr', label: 'Linked Attr' },
      { key: 'category', label: 'Category' }, { key: 'specializations', label: 'Specializations' },
    ],
    filterFields: ['linked_attr', 'category'], detailFields: [],
  },
  'adept-powers':      { table: 'ref_adept_powers',       label: 'Adept Powers',
    listColumns: [{ key: 'name', label: 'Name' }, { key: 'pp_cost', label: 'PP Cost' }],
    filterFields: [],
    detailFields: [{ key: 'description', label: 'Description' }, { key: 'game_effect', label: 'Game Effect' }],
  },
  mutations:           { table: 'ref_mutations',          label: 'Mutations',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'bp_cost', label: 'BP Cost' },
      { key: 'essence', label: 'Essence' },
    ],
    filterFields: [],
    detailFields: [{ key: 'description', label: 'Description' }, { key: 'game_effect', label: 'Game Effect' }],
  },
  totems:              { table: 'ref_totems',             label: 'Totems',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'type', label: 'Type' },
      { key: 'environment', label: 'Environment' },
    ],
    filterFields: ['type'],
    detailFields: [
      { key: 'description', label: 'Description' },
      { key: 'advantages', label: 'Advantages' },
      { key: 'disadvantages', label: 'Disadvantages' },
    ],
  },
  spirits:             { table: 'ref_spirits',            label: 'Spirits',
    listColumns: [{ key: 'name', label: 'Name' }, { key: 'category', label: 'Category' }],
    filterFields: ['category'],
    detailFields: [
      { key: 'formula_b', label: 'Body' }, { key: 'formula_q', label: 'Quickness' },
      { key: 'formula_s', label: 'Strength' }, { key: 'formula_c', label: 'Charisma' },
      { key: 'formula_i', label: 'Intelligence' }, { key: 'formula_w', label: 'Willpower' },
      { key: 'formula_e', label: 'Essence' }, { key: 'formula_r', label: 'Reaction' },
      { key: 'formula_initiative', label: 'Initiative' },
      { key: 'attack', label: 'Attack' }, { key: 'powers', label: 'Powers' },
      { key: 'weaknesses', label: 'Weaknesses' },
    ],
  },
  'spirit-powers':     { table: 'ref_spirit_powers',      label: 'Spirit Powers',
    listColumns: [
      { key: 'name', label: 'Name' }, { key: 'type', label: 'Type' },
      { key: 'action', label: 'Action' }, { key: 'range', label: 'Range' },
      { key: 'duration', label: 'Duration' },
    ],
    filterFields: ['type'],
    detailFields: [{ key: 'description', label: 'Description' }],
  },
  'elemental-services': { table: 'ref_elemental_services', label: 'Elemental Services',
    listColumns: [{ key: 'name', label: 'Name' }],
    filterFields: [],
    detailFields: [{ key: 'description', label: 'Description' }],
  },
};
```

---

### Blueprint 4.2b — `[catalog]/+page.server.ts`

**File:** `companion/src/routes/library/[catalog]/+page.server.ts`

```typescript
import { error, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { CATALOG_CONFIG } from '$lib/catalog-config';

export const load: PageServerLoad = async ({ params, parent, platform }) => {
  const config = CATALOG_CONFIG[params.catalog];
  if (!config) throw error(404, 'Unknown catalog section');

  const { player } = await parent();
  const db = getDb(platform!.env);

  // config.table = trusted constant, never user-derived — safe to interpolate
  const [rowsResult, ...filterResults] = await Promise.all([
    db.execute({ sql: `SELECT * FROM ${config.table} ORDER BY name ASC`, args: [] }),
    ...config.filterFields.map((field) =>
      db.execute({
        sql:  `SELECT DISTINCT ${field} FROM ${config.table} WHERE ${field} IS NOT NULL ORDER BY ${field} ASC`,
        args: [],
      })
    ),
  ]);

  const rows = rowsResult.rows as Record<string, unknown>[];
  const filterOptions: Record<string, string[]> = {};
  for (let i = 0; i < config.filterFields.length; i++) {
    const field = config.filterFields[i];
    filterOptions[field] = filterResults[i].rows.map((r) => String(r[field]));
  }

  return { config, rows, filterOptions, isGm: player.is_gm === 1, slug: params.catalog };
};

export const actions: Actions = {
  delete: async ({ request, locals, params, platform }) => {
    // Fresh GM re-validation — do not trust layout session
    const session = await locals.auth();
    if (!session?.user?.id) throw error(401, 'Unauthorized');

    const config = CATALOG_CONFIG[params.catalog];
    if (!config) throw error(404, 'Unknown catalog section');

    const db = getDb(platform!.env);
    const playerRow = await db.execute({
      sql: 'SELECT is_gm FROM players WHERE id = ?', args: [session.user.id],
    });
    if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
      throw error(403, 'Forbidden');
    }

    const formData = await request.formData();
    const id = formData.get('id');
    if (!id || typeof id !== 'string' || id.trim() === '') {
      throw error(400, 'Missing or invalid entry id');
    }

    // id bound as parameter — not interpolated — no injection risk
    await db.execute({ sql: `DELETE FROM ${config.table} WHERE id = ?`, args: [id] });
    throw redirect(303, `/library/${params.catalog}`);
  },
};
```

---

### Blueprint 4.2c — `[catalog]/+page.svelte`

**File:** `companion/src/routes/library/[catalog]/+page.svelte`

Spirit stat block detection: `data.config.table === 'ref_spirits'` renders `formula_*` as a horizontal `B | Q | S | C | I | W | E | R | Init` block; non-formula `detailFields` (`attack`, `powers`, `weaknesses`) render as standard label:value pairs below.

Delete confirmation: `onclick` sets `deletingRowId`; reveals inline "Are you sure?" with a `<form method="POST" action="?/delete">` + hidden `id` input and a cancel button — **no** `window.confirm()`.

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  let { data }: { data: PageData } = $props();

  let searchTerm = $state('');
  let activeFilters = $state<Record<string, string>>(
    Object.fromEntries(data.config.filterFields.map((f) => [f, 'all']))
  );
  let expandedRowId = $state<number | null>(null);
  let deletingRowId = $state<number | null>(null);

  const filteredRows = $derived(
    (data.rows as Record<string, unknown>[]).filter((row) => {
      if (searchTerm && !String(row.name ?? '').toLowerCase().includes(searchTerm.toLowerCase()))
        return false;
      for (const field of data.config.filterFields) {
        const active = activeFilters[field];
        if (active && active !== 'all' && row[field] !== active) return false;
      }
      return true;
    })
  );

  const SPIRIT_FORMULA_KEYS = [
    'formula_b','formula_q','formula_s','formula_c',
    'formula_i','formula_w','formula_e','formula_r','formula_initiative',
  ] as const;
  const FORMULA_ABBREV: Record<string, string> = {
    formula_b:'B', formula_q:'Q', formula_s:'S', formula_c:'C',
    formula_i:'I', formula_w:'W', formula_e:'E', formula_r:'R', formula_initiative:'Init',
  };
  const isSpirits = data.config.table === 'ref_spirits';
  const spiritNonFormulaFields = isSpirits
    ? data.config.detailFields.filter((f) => !f.key.startsWith('formula_'))
    : [];

  const detailColspan = $derived(
    data.config.listColumns.length +
    (data.config.detailFields.length > 0 ? 1 : 0) +
    (data.isGm ? 1 : 0)
  );

  function toggleRow(id: number): void {
    expandedRowId = expandedRowId === id ? null : id;
    if (expandedRowId !== id) deletingRowId = null;
  }
</script>

<nav><a href="/library">← Game Library</a></nav>
<h1>{data.config.label}</h1>

<div class="controls">
  <input type="search" placeholder="Search by name…" bind:value={searchTerm} />
  {#each data.config.filterFields as field}
    <select bind:value={activeFilters[field]}>
      <option value="all">All {field}</option>
      {#each data.filterOptions[field] ?? [] as opt}
        <option value={opt}>{opt}</option>
      {/each}
    </select>
  {/each}
  {#if data.isGm}<a href="/library/{data.slug}/new">+ Add entry</a>{/if}
</div>

<p>Showing {filteredRows.length} of {data.rows.length} entries</p>

{#if filteredRows.length === 0}
  <p>No entries match your filters.</p>
{:else}
  <table>
    <thead><tr>
      {#each data.config.listColumns as col}<th>{col.label}</th>{/each}
      {#if data.config.detailFields.length > 0}<th></th>{/if}
      {#if data.isGm}<th>Actions</th>{/if}
    </tr></thead>
    <tbody>
      {#each filteredRows as row}
        {@const rowId = row.id as number}
        {@const isExpanded = expandedRowId === rowId}
        {@const canExpand = data.config.detailFields.length > 0}
        <tr
          class:expanded={isExpanded}
          onclick={canExpand ? () => toggleRow(rowId) : undefined}
          style={canExpand ? 'cursor:pointer' : ''}
        >
          {#each data.config.listColumns as col}<td>{row[col.key] ?? '—'}</td>{/each}
          {#if canExpand}<td>{isExpanded ? '▲' : '▼'}</td>{/if}
          {#if data.isGm}
            <td onclick={(e) => e.stopPropagation()}>
              <a href="/library/{data.slug}/{rowId}/edit">Edit</a>
              {#if deletingRowId === rowId}
                Are you sure?
                <form method="POST" action="?/delete" style="display:inline">
                  <input type="hidden" name="id" value={rowId} />
                  <button type="submit">Yes</button>
                </form>
                <button type="button" onclick={() => (deletingRowId = null)}>No</button>
              {:else}
                <button type="button" onclick={() => (deletingRowId = rowId)}>Delete</button>
              {/if}
            </td>
          {/if}
        </tr>

        {#if isExpanded && canExpand}
          <tr><td colspan={detailColspan}>
            {#if isSpirits}
              <div class="stat-block">
                {#each SPIRIT_FORMULA_KEYS as key}
                  <div class="stat">
                    <small>{FORMULA_ABBREV[key]}</small>
                    <strong>{row[key] ?? '—'}</strong>
                  </div>
                {/each}
              </div>
              {#each spiritNonFormulaFields as f}
                <p><strong>{f.label}:</strong> {row[f.key] ?? '—'}</p>
              {/each}
            {:else}
              {#each data.config.detailFields as f}
                <p><strong>{f.label}:</strong> {row[f.key] ?? '—'}</p>
              {/each}
            {/if}
          </td></tr>
        {/if}
      {/each}
    </tbody>
  </table>
{/if}

<style>
  .controls { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
  .stat-block { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
  .stat { display: flex; flex-direction: column; align-items: center; }
  /* DEV DECISION: match app theme */
</style>
```

### Acceptance criteria (Blueprint 4.2)

- All 11 `/library/{slug}` routes render without error
- An unknown slug (e.g., `/library/foobar`) returns 404
- Rows display correct column data; empty tables show an empty state — not an error
- Search filters visible rows in real time (no page reload)
- Filter dropdowns contain only values present in the DB
- Search and filter can be active simultaneously
- Expanded row panel renders `detailFields` values (visible via row click)
- Spirit detail panel renders `formula_*` as compact stat block
- Edit and Delete controls appear only for GM users
- Co-located delete action re-validates GM server-side and validates `id` from form data

---

## Blueprint 4.3 — GM Create & Edit Forms

### Blueprint 4.3a — `catalog-config.ts` Amendment: `formFields`

**File:** `companion/src/lib/catalog-config.ts` (amendment to 4.2a)

Add `FormFieldDef` interface and `formFields: FormFieldDef[]` to `CatalogEntry`.

**Typing rules:**
- `textarea` — description, game_effect, advantages, disadvantages, powers, weaknesses, attack, notes, specializations
- `select` with hardcoded `options` — spell `type` (M, P), spell `category`, totem `type` (Animal, Nature), spirit `category` (Elemental, Nature), spirit power `type` (P, M)
- `number` — all columns typed `INTEGER` or `REAL` in the DDL
- `text` — everything else, **including `formula_*` columns** (they store formula strings like `"F+4"`, not raw integers)

```typescript
export interface FormFieldDef {
  key: string;
  label: string;
  type: 'text' | 'number' | 'textarea' | 'select';
  options?: string[];
}

// Add to CatalogEntry interface:
// formFields: FormFieldDef[];
```

Complete `formFields` per catalog entry:

```typescript
// spells
formFields: [
  { key: 'name',        label: 'Name',        type: 'text' },
  {
    key: 'category', label: 'Category', type: 'select',
    // [DEV DECISION]: verify exact categories against Spells.xlsx before deploy
    options: ['Combat', 'Detection', 'Health', 'Illusion', 'Manipulation',
              'Elemental Combat', 'Elemental Manipulation', 'Exclusive', 'Ritual'],
  },
  { key: 'type',        label: 'Type',        type: 'select', options: ['M', 'P'] },
  { key: 'target',      label: 'Target',      type: 'text' },
  { key: 'duration',    label: 'Duration',    type: 'text' },
  { key: 'drain',       label: 'Drain',       type: 'text' },
  { key: 'description', label: 'Description', type: 'textarea' },
],

// weapons
formFields: [
  { key: 'name',    label: 'Name',    type: 'text' },
  { key: 'type',    label: 'Type',    type: 'text' },
  { key: 'conceal', label: 'Conceal', type: 'number' },
  { key: 'reach',   label: 'Reach',   type: 'number' },
  { key: 'damage',  label: 'Damage',  type: 'text' },
  { key: 'ep',      label: 'EP',      type: 'number' },
  { key: 'cost',    label: 'Cost',    type: 'number' },
],

// armor
formFields: [
  { key: 'name',     label: 'Name',       type: 'text' },
  { key: 'location', label: 'Location',   type: 'text' },
  { key: 'conceal',  label: 'Conceal',    type: 'number' },
  { key: 'rating_p', label: 'Rating (P)', type: 'number' },
  { key: 'rating_s', label: 'Rating (S)', type: 'number' },
  { key: 'rating_i', label: 'Rating (I)', type: 'number' },
  { key: 'ep',       label: 'EP',         type: 'number' },
  { key: 'cost',     label: 'Cost',       type: 'number' },
],

// equipment
formFields: [
  { key: 'name',    label: 'Name',    type: 'text' },
  { key: 'conceal', label: 'Conceal', type: 'number' },
  { key: 'ep',      label: 'EP',      type: 'number' },
  { key: 'cost',    label: 'Cost',    type: 'number' },
  { key: 'notes',   label: 'Notes',   type: 'textarea' },
],

// skills
formFields: [
  { key: 'name',            label: 'Name',             type: 'text' },
  { key: 'linked_attr',     label: 'Linked Attribute', type: 'text' },
  { key: 'category',        label: 'Category',         type: 'text' },
  { key: 'specializations', label: 'Specializations',  type: 'textarea' },
],

// adept-powers
formFields: [
  { key: 'name',        label: 'Name',        type: 'text' },
  { key: 'pp_cost',     label: 'PP Cost',     type: 'text' },
  // pp_cost is TEXT in DDL — stores values like "0.25", "1.5", or "varies"
  // text input matches DDL type; no parseFloat coercion
  { key: 'description', label: 'Description', type: 'textarea' },
  { key: 'game_effect', label: 'Game Effect', type: 'textarea' },
],

// mutations
formFields: [
  { key: 'name',        label: 'Name',        type: 'text' },
  { key: 'essence',     label: 'Essence',     type: 'text' },
  // essence is TEXT in DDL — stores values like "0.5", "1"; text matches DDL type
  { key: 'bp_cost',     label: 'BP Cost',     type: 'number' },
  { key: 'description', label: 'Description', type: 'textarea' },
  { key: 'game_effect', label: 'Game Effect', type: 'textarea' },
],

// totems
formFields: [
  { key: 'name',          label: 'Name',          type: 'text' },
  { key: 'type',          label: 'Type',          type: 'select', options: ['Animal', 'Nature'] },
  { key: 'environment',   label: 'Environment',   type: 'text' },
  { key: 'description',   label: 'Description',   type: 'textarea' },
  { key: 'advantages',    label: 'Advantages',    type: 'textarea' },
  { key: 'disadvantages', label: 'Disadvantages', type: 'textarea' },
],

// spirits
formFields: [
  { key: 'name',               label: 'Name',               type: 'text' },
  { key: 'category',           label: 'Category',           type: 'select', options: ['Elemental', 'Nature'] },
  // formula_* are TEXT columns — store expressions like "F+4", not raw numbers
  { key: 'formula_b',          label: 'Body Formula',          type: 'text' },
  { key: 'formula_q',          label: 'Quickness Formula',     type: 'text' },
  { key: 'formula_s',          label: 'Strength Formula',      type: 'text' },
  { key: 'formula_c',          label: 'Charisma Formula',      type: 'text' },
  { key: 'formula_i',          label: 'Intelligence Formula',  type: 'text' },
  { key: 'formula_w',          label: 'Willpower Formula',     type: 'text' },
  { key: 'formula_e',          label: 'Essence Formula',       type: 'text' },
  { key: 'formula_r',          label: 'Reaction Formula',      type: 'text' },
  { key: 'formula_initiative', label: 'Initiative Formula',    type: 'text' },
  { key: 'attack',             label: 'Attack',             type: 'textarea' },
  { key: 'powers',             label: 'Powers',             type: 'textarea' },
  { key: 'weaknesses',         label: 'Weaknesses',         type: 'textarea' },
],

// spirit-powers
formFields: [
  { key: 'name',        label: 'Name',        type: 'text' },
  { key: 'type',        label: 'Type',        type: 'select', options: ['P', 'M'] },
  { key: 'action',      label: 'Action',      type: 'text' },
  { key: 'range',       label: 'Range',       type: 'text' },
  { key: 'duration',    label: 'Duration',    type: 'text' },
  { key: 'description', label: 'Description', type: 'textarea' },
],

// elemental-services
formFields: [
  { key: 'name',        label: 'Name',        type: 'text' },
  { key: 'description', label: 'Description', type: 'textarea' },
],
```

---

### Blueprint 4.3b — Create Form: `new/+page.server.ts`

**File:** `companion/src/routes/library/[catalog]/new/+page.server.ts`

```typescript
import { error, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { CATALOG_CONFIG } from '$lib/catalog-config';

export const load: PageServerLoad = async ({ params, parent, platform }) => {
  const config = CATALOG_CONFIG[params.catalog];
  if (!config) throw error(404, 'Unknown catalog section');

  const { player } = await parent();
  const db = getDb(platform!.env);

  const playerRow = await db.execute({
    sql:  'SELECT is_gm FROM players WHERE id = ?',
    args: [player.id],
  });
  if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  return { config, slug: params.catalog };
};

export const actions: Actions = {
  create: async ({ request, locals, params, platform }) => {
    const config = CATALOG_CONFIG[params.catalog];
    if (!config) throw error(404, 'Unknown catalog section');

    const session = await locals.auth();
    if (!session?.user?.id) throw error(401, 'Unauthorized');

    const db = getDb(platform!.env);
    const playerRow = await db.execute({
      sql:  'SELECT is_gm FROM players WHERE id = ?',
      args: [session.user.id],
    });
    if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
      throw error(403, 'Forbidden');
    }

    const formData = await request.formData();
    const errors: Record<string, string> = {};
    const columns: string[] = [];
    const values: unknown[] = [];

    // Column names from config.formFields[].key — never from formData keys.
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
      columns.push(field.key);
      values.push(value);
    }

    if (Object.keys(errors).length > 0) return { errors };

    try {
      await db.execute({
        sql:  `INSERT INTO ${config.table} (${columns.join(', ')}) VALUES (${columns.map(() => '?').join(', ')})`,
        args: values,
      });
    } catch (err) {
      if (err instanceof Error && err.message.includes('UNIQUE constraint failed')) {
        return { errors: { name: 'An entry with this name already exists' } };
      }
      throw err;
    }

    throw redirect(303, `/library/${params.catalog}`);
  },
};
```

---

### Blueprint 4.3c — Shared Component: `CatalogForm.svelte`

**File:** `companion/src/lib/components/CatalogForm.svelte`

**[DEV DECISION] resolved — extract.** Create and edit pages are structurally identical (same `formFields` iteration, same per-field error display, same Save/Cancel). The only differences are entry pre-population and the delete section — both handled through props. Extraction eliminates >30% duplication.

| Prop | Type | Required | Purpose |
|---|---|---|---|
| `config` | `CatalogEntry` | Yes | Drives `formFields` iteration |
| `entry` | `Record<string, unknown>` | No | Pre-populates values (edit mode); omit for create |
| `form` | `{ errors?: Record<string, string> } \| null` | No | SvelteKit action return for per-field error messages |
| `action` | `string` | Yes | Named action target: `"?/create"` or `"?/update"` |
| `cancelHref` | `string` | Yes | Cancel link destination |

```svelte
<script lang="ts">
  import type { CatalogEntry } from '$lib/catalog-config';

  interface Props {
    config: CatalogEntry;
    entry?: Record<string, unknown>;
    form?: { errors?: Record<string, string> } | null;
    action: string;
    cancelHref: string;
  }
  let { config, entry = undefined, form = null, action, cancelHref }: Props = $props();
</script>

<form method="POST" {action} class="catalog-form">
  {#each config.formFields as field}
    <div class="field-group">
      <label for={field.key}>{field.label}</label>

      {#if field.type === 'textarea'}
        <textarea id={field.key} name={field.key} rows="4"
          value={String(entry?.[field.key] ?? '')}></textarea>

      {:else if field.type === 'select'}
        <select id={field.key} name={field.key}>
          <option value="">— select —</option>
          {#each field.options ?? [] as opt}
            <option value={opt} selected={entry?.[field.key] === opt}>{opt}</option>
          {/each}
        </select>

      {:else if field.type === 'number'}
        <!-- step="any" supports pp_cost/essence fractional values -->
        <input type="number" id={field.key} name={field.key}
          step="any" value={entry?.[field.key] ?? ''} />

      {:else}
        <input type="text" id={field.key} name={field.key}
          value={String(entry?.[field.key] ?? '')} />
      {/if}

      {#if form?.errors?.[field.key]}
        <p class="field-error" role="alert">{form.errors[field.key]}</p>
      {/if}
    </div>
  {/each}

  <div class="form-actions">
    <button type="submit" class="btn-primary">Save</button>
    <a href={cancelHref} class="btn-secondary">Cancel</a>
  </div>
</form>

<style>
  /* DEV DECISION: integrate with app-level CSS variables/theme */
  .catalog-form  { max-width: 640px; }
  .field-group   { display: flex; flex-direction: column; gap: 0.25rem; margin-bottom: 1rem; }
  label          { font-weight: bold; font-size: 0.9rem; }
  input, select,
  textarea       { width: 100%; padding: 0.4rem 0.5rem; font-size: 0.95rem; box-sizing: border-box; }
  textarea       { resize: vertical; }
  .field-error   { color: var(--error, #c00); font-size: 0.85rem; margin: 0; }
  .form-actions  { display: flex; gap: 1rem; align-items: center; margin-top: 1.5rem; }
</style>
```

---

### Blueprint 4.3d — Create Form: `new/+page.svelte`

**File:** `companion/src/routes/library/[catalog]/new/+page.svelte`

```svelte
<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import CatalogForm from '$lib/components/CatalogForm.svelte';

  let { data, form }: { data: PageData; form: ActionData } = $props();
  const cancelHref = `/library/${data.slug}`;
</script>

<nav class="breadcrumb">
  <a href={cancelHref}>← {data.config.label}</a>
</nav>

<h1>Add {data.config.label} Entry</h1>

<CatalogForm config={data.config} {form} action="?/create" cancelHref={cancelHref} />
```

---

### Blueprint 4.3e — Edit Form: `[id]/edit/+page.server.ts`

**File:** `companion/src/routes/library/[catalog]/[id]/edit/+page.server.ts`

```typescript
import { error, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { CATALOG_CONFIG } from '$lib/catalog-config';

export const load: PageServerLoad = async ({ params, parent, platform }) => {
  const config = CATALOG_CONFIG[params.catalog];
  if (!config) throw error(404, 'Unknown catalog section');

  const { player } = await parent();
  const db = getDb(platform!.env);

  const playerRow = await db.execute({
    sql:  'SELECT is_gm FROM players WHERE id = ?',
    args: [player.id],
  });
  if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  const result = await db.execute({
    sql:  `SELECT * FROM ${config.table} WHERE id = ?`,
    args: [params.id],
  });
  const entry = result.rows[0] as Record<string, unknown> | undefined;
  if (!entry) throw error(404, 'Entry not found');

  return { config, entry, slug: params.catalog };
};

export const actions: Actions = {
  update: async ({ request, locals, params, platform }) => {
    const config = CATALOG_CONFIG[params.catalog];
    if (!config) throw error(404, 'Unknown catalog section');

    const session = await locals.auth();
    if (!session?.user?.id) throw error(401, 'Unauthorized');

    const db = getDb(platform!.env);
    const playerRow = await db.execute({
      sql:  'SELECT is_gm FROM players WHERE id = ?',
      args: [session.user.id],
    });
    if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
      throw error(403, 'Forbidden');
    }

    // Verify entry still exists — guard against concurrent delete
    const existsRow = await db.execute({
      sql:  `SELECT id FROM ${config.table} WHERE id = ?`,
      args: [params.id],
    });
    if (existsRow.rows.length === 0) throw error(404, 'Entry not found');

    const formData = await request.formData();
    const errors: Record<string, string> = {};
    const setClauses: string[] = [];
    const values: unknown[] = [];

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
      // Trusted config key in SET clause — no user-supplied column names
      setClauses.push(`${field.key} = ?`);
      values.push(value);
    }

    if (Object.keys(errors).length > 0) return { errors };

    const setClause = [...setClauses, "updated_at = datetime('now')"].join(', ');
    values.push(params.id);

    try {
      await db.execute({
        sql:  `UPDATE ${config.table} SET ${setClause} WHERE id = ?`,
        args: values,
      });
    } catch (err) {
      if (err instanceof Error && err.message.includes('UNIQUE constraint failed')) {
        return { errors: { name: 'An entry with this name already exists' } };
      }
      throw err;
    }

    throw redirect(303, `/library/${params.catalog}`);
  },

  delete: async ({ locals, params, platform }) => {
    const config = CATALOG_CONFIG[params.catalog];
    if (!config) throw error(404, 'Unknown catalog section');

    const session = await locals.auth();
    if (!session?.user?.id) throw error(401, 'Unauthorized');

    const db = getDb(platform!.env);
    const playerRow = await db.execute({
      sql:  'SELECT is_gm FROM players WHERE id = ?',
      args: [session.user.id],
    });
    if ((playerRow.rows[0] as { is_gm: number } | undefined)?.is_gm !== 1) {
      throw error(403, 'Forbidden');
    }

    await db.execute({
      sql:  `DELETE FROM ${config.table} WHERE id = ?`,
      args: [params.id],
    });

    throw redirect(303, `/library/${params.catalog}`);
  },
};
```

---

### Blueprint 4.3f — Edit Form: `[id]/edit/+page.svelte`

**File:** `companion/src/routes/library/[catalog]/[id]/edit/+page.svelte`

```svelte
<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import CatalogForm from '$lib/components/CatalogForm.svelte';

  let { data, form }: { data: PageData; form: ActionData } = $props();

  const listHref = `/library/${data.slug}`;
  let confirming = $state(false);
</script>

<nav class="breadcrumb">
  <a href={listHref}>← {data.config.label}</a>
</nav>

<h1>Edit {data.config.label} — {data.entry.name as string}</h1>

<CatalogForm
  config={data.config}
  entry={data.entry}
  {form}
  action="?/update"
  cancelHref={listHref}
/>

<!-- Delete section — separate action, visually isolated -->
<section class="delete-section">
  <h2>Delete Entry</h2>

  {#if confirming}
    <p>
      Are you sure you want to delete
      <strong>{data.entry.name as string}</strong>?
      This cannot be undone.
    </p>
    <form method="POST" action="?/delete"
      style="display: inline-flex; gap: 0.5rem; align-items: center;">
      <button type="submit" class="btn-danger">Yes, delete</button>
      <button type="button" class="btn-secondary"
        onclick={() => (confirming = false)}>Cancel</button>
    </form>
  {:else}
    <button type="button" class="btn-danger-outline"
      onclick={() => (confirming = true)}>Delete entry</button>
  {/if}
</section>

<style>
  .delete-section {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border, #e0e0e0);
  }
  .delete-section h2 { font-size: 1rem; color: var(--text-muted, #666); margin-bottom: 0.75rem; }
</style>
```

### Acceptance criteria (Blueprint 4.3)

- `/library/{catalog}/new` returns 403 for non-GM users; 404 for unknown catalog slug
- Submitting a valid create form adds a row and redirects to the catalog list
- Submitting with a duplicate name returns an inline form error — no crash, no redirect
- Submitting a valid edit form updates the row and redirects
- Delete action removes the row; catalog list confirms removal on reload
- All SQL column identifiers come from `config.formFields[].key` (trusted constant) — no user-supplied column names appear anywhere in SQL
- `CatalogForm.svelte` shared component renders correctly for both create (empty) and edit (pre-populated) modes

---

## Blueprint 4.4 — Library Sub-Navigation Layout

**File:** `companion/src/routes/library/+layout.svelte`

No `+layout.server.ts` — inherits `player` from root layout via `$page.data`. Zero additional server load.

Active slug detection isolates path segment `[1]` so `/library/spells/new` and `/library/spells/42/edit` both correctly highlight the **Spells** nav item.

```svelte
<script lang="ts">
  import { page } from '$app/state';
  import { CATALOG_CONFIG } from '$lib/catalog-config';

  let { children } = $props();

  // /library          → activeSlug = null (only "All Catalogs" is active)
  // /library/spells   → activeSlug = 'spells'
  // /library/spells/new  → activeSlug = 'spells'  ✓ correct active item
  // /library/spells/42/edit → activeSlug = 'spells'  ✓ correct active item
  const activeSlug = $derived(
    page.url.pathname.split('/').filter(Boolean)[1] ?? null
  );
</script>

<nav class="library-subnav" aria-label="Game Library sections">
  <a href="/library" class="subnav-link"
    class:active={page.url.pathname === '/library'}
    aria-current={page.url.pathname === '/library' ? 'page' : undefined}>
    All Catalogs
  </a>

  {#each Object.entries(CATALOG_CONFIG) as [slug, entry]}
    <a href="/library/{slug}" class="subnav-link"
      class:active={activeSlug === slug}
      aria-current={activeSlug === slug ? 'page' : undefined}>
      {entry.label}
    </a>
  {/each}
</nav>

{@render children()}

<style>
  /* DEV DECISION: integrate with app-level CSS variables/theme */
  .library-subnav {
    display: flex; flex-wrap: wrap; gap: 0.25rem;
    padding: 0.5rem 0 0.75rem;
    border-bottom: 2px solid var(--border, #e0e0e0);
    margin-bottom: 1.5rem;
  }
  .subnav-link {
    padding: 0.3rem 0.8rem; border-radius: 0.25rem;
    font-size: 0.875rem; text-decoration: none;
    color: var(--text, #333); transition: background 0.1s;
  }
  .subnav-link:hover { background: var(--surface-2, #f0f0f0); }
  .subnav-link.active {
    background: var(--accent, #005eff);
    color: var(--accent-text, #fff); font-weight: bold;
  }
</style>
```

### Acceptance criteria (Blueprint 4.4)

- Sub-nav renders on all `/library/*` routes (landing, list, new, edit)
- "All Catalogs" active only on `/library` exactly; each catalog link active on that slug and all its sub-routes
- `aria-current="page"` set on the active link for accessibility
- Uses `{@render children()}` (Svelte 5 snippet API) — not `<slot />`
- Zero server data load added — no `+layout.server.ts`

---

## Implementation Order — Phase 4 (Blueprints 4.1–4.4)

| Step | Blueprint | File | Action | Hard depends on |
|---|---|---|---|---|
| 1 | 4.2a | `src/lib/catalog-config.ts` | Create — types + full config (no `formFields` yet) | Phase 1 schema (BP 1.3) |
| 2 | 4.1 | `routes/library/+page.server.ts` | Create — parallel COUNT queries | Step 1 |
| 3 | 4.1 | `routes/library/+page.svelte` | Replace Phase 3 stub — card grid | Steps 1 + 2 |
| 4 | 4.2b | `routes/library/[catalog]/+page.server.ts` | Create — SELECT + filters + delete action | Step 1 |
| 5 | 4.2c | `routes/library/[catalog]/+page.svelte` | Create — search/filter/detail/spirit stat block | Steps 1 + 4 |
| 6 | 4.3a | `src/lib/catalog-config.ts` | Amend — add `FormFieldDef` + `formFields` to all 11 entries | Step 1; verify spell categories vs. Excel |
| 7 | 4.3c | `src/lib/components/CatalogForm.svelte` | Create — shared field-rendering component | Step 6 |
| 8 | 4.3b | `routes/library/[catalog]/new/+page.server.ts` | Create — GM guard + INSERT action | Step 6 |
| 9 | 4.3d | `routes/library/[catalog]/new/+page.svelte` | Create — uses CatalogForm | Steps 7 + 8 |
| 10 | 4.3e | `routes/library/[catalog]/[id]/edit/+page.server.ts` | Create — GM guard + UPDATE + DELETE actions | Step 6 |
| 11 | 4.3f | `routes/library/[catalog]/[id]/edit/+page.svelte` | Create — uses CatalogForm + inline delete | Steps 7 + 10 |
| 12 | 4.4 | `routes/library/+layout.svelte` | Create — sub-nav bar | Step 1 (independent of 6–11) |

---

*Phase 4 blueprints complete (4.1–4.4). All Layer 3 phases done. Hand off to Layer 4 DRY audit.*
