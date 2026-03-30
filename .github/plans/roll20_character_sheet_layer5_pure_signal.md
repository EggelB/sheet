# Roll20 Character Sheet — Layer 5: Pure Signal Implementation

**Goal:** Build a custom Roll20 Shadowrun 3e character sheet template (K-scaffold) for 6 players (~18 characters) with a companion read-only web app (SvelteKit + Turso + Cloudflare).

**Phases:**
1. Data Architecture & Naming Contract
2. HTML Structure & Tab System
3. Sheet Worker Cascade & Roll Templates
4. CSS Design System
5. Companion App Architecture & Data Sync

**Architecture:** Two-layer system — (A) Roll20 native sheet (K-scaffold HTML+CSS+Sheet Workers, all in-session play) + (B) companion SvelteKit web app (Turso DB, Cloudflare Pages, Discord OAuth). Layer B is additive and decoupled; players can use the sheet without it.

---

## Phase 1: Data Architecture & Naming Contract

**Context:** Attribute name renames in Roll20 break ALL player macros retroactively. Locking the complete 122-field data contract + 7 repeating section schemas before any UI work is the highest-leverage planning task.

**Implementation:**

### sheet.json Top-Level Skeleton

```json
{
  "html": "sheet.html",
  "css": "sheet.css",
  "authors": "[roll20_character_sheet project]",
  "roll20_authors": "",
  "preview": "preview.png",
  "instructions": "Custom TTRPG character sheet — Shadowrun-hybrid system with K-scaffold Sheet Worker automation.",
  "legacy": false,
  "tabs": [
    { "name": "tab-core", "label": "Core" },
    { "name": "tab-skills", "label": "Skills" },
    { "name": "tab-magic", "label": "Magic" },
    { "name": "tab-gear", "label": "Gear" },
    { "name": "tab-bio", "label": "Bio" }
  ],
  "templates": ["skill", "attack", "spell"],
  "attributes": [ "..." ]
}
```

- `tabs` and `templates` keys are K-scaffold extensions — verify against installed K-scaffold version; standard Roll20 sheet.json only requires `html`, `css`, `authors`, `roll20_authors`, `preview`, `instructions`, `legacy`
- `legacy: false` required for K-scaffold
- Tab names are CSS slug identifiers matching `.sheet-tab-panel-{name}` classes

### Scalar Field Registry (122 fields, 19 groups)

**Conventions:** `name` = bare attribute name (no `attr_` prefix in this registry). `type` = Roll20 input type. `worker_only: true` = set exclusively by Sheet Workers, requires hidden/readonly HTML input. All number fields default `0`; all text fields default `""` unless noted.

- [DEV DECISION] Verify K-scaffold `attr_` prefix convention: bare names in sheet.json (Option A) vs `attr_`-prefixed (Option B). Tables below use bare names — mechanically prefix all names if K-scaffold requires it.

#### Groups 1–5: Core Attributes (38 fields)

8 attributes: `body` | `dex` | `str` | `cha` | `int` | `wil` | `hum` | `mag`

| Group | Pattern | Fields | worker_only | Count |
|---|---|---|---|---|
| 1 — Base Values | `{attr}_base` | All 8 | false | 8 |
| 2 — Mutations | `{attr}_mutations` | 7 (mag excluded) | false | 7 |
| 3 — Magic | `{attr}_magic` | 7 (mag excluded) | false | 7 |
| 4 — Misc | `{attr}_misc` | All 8 (including mag) | false | 8 |
| 5 — Totals | `{attr}` | All 8 | true | 8 |

- Total formula (7 standard attrs): `base + mutations + magic + misc`
- `mag` exception: `mag_base + mag_misc` only — no `_mutations` or `_magic` sub-fields (magic rating cannot modify itself)
- `int` is a valid JS property name and Roll20 attribute name — no rename needed

#### Group 6: Reaction (3 fields)

| Field | worker_only | Formula |
|---|---|---|
| `reaction_base` | true | `Math.floor((int + dex) / 2)` |
| `reaction_misc` | false | Player-editable modifier |
| `reaction` | true | `Math.max(1, reaction_base + reaction_misc)` — floor at 1 prevents 0d6 roll errors |

#### Group 7: Dice Pools (12 fields)

4 pools × 3 fields each: `pool_{name}_base` (worker_only) | `pool_{name}_misc` (player-editable) | `pool_{name}` (worker_only)

| Pool | Base Formula | Total Formula |
|---|---|---|
| `pool_spell` | `Math.floor((cha + int + wil) / 2)` | `Math.max(0, base + misc)` |
| `pool_combat` | `Math.floor((dex + int + wil) / 2)` | `Math.max(0, base + misc)` |
| `pool_control` | `= reaction` (direct copy) | `Math.max(0, base + misc)` |
| `pool_astral` | `Math.floor((int + wil + mag) / 3)` | `Math.max(0, base + misc)` |

#### Group 8: Initiative (4 fields)

| Field | worker_only | Notes |
|---|---|---|
| `init_dice` | false | Number d6s for initiative; default `1` |
| `init_reaction_mod` | false | Reaction-specific initiative bonus |
| `init_misc_mod` | false | Miscellaneous initiative modifier |
| `init_score` | true | `reaction + init_reaction_mod + init_misc_mod` — no floor (negative is valid) |

- Roll formula: `@{init_dice}d6 + @{init_score}` — plain sum, NOT success-counting, no cs/cf, no template

#### Group 9: Condition Monitors (6 fields)

| Field | worker_only | Notes |
|---|---|---|
| `cm_mental` | false | Damage level 0–4 (no Unconscious on mental) |
| `cm_stun` | false | Damage level 0–5 (5 = Unconscious) |
| `cm_physical` | false | Damage level 0–5 (5 = Overflow threshold) |
| `cm_physical_overflow` | false | Overflow boxes beyond Deadly |
| `cm_tn_mod` | true | `Math.max(penaltyOf(mental), penaltyOf(stun), penaltyOf(physical))` where `penaltyOf = lvl => Math.min(lvl, 3)` — range 0–3 |
| `cm_init_mod` | true | `= -1 * cm_tn_mod` — range 0 to −3 |

- Penalty tiers: 0=Clean, 1=Light(+1TN/−1Init), 2=Moderate(+2), 3=Serious(+3), 4=Deadly(capped at 3), 5=Unconscious(capped at 3)

#### Group 10: Character Identity (6 text fields)

`char_name` | `char_race_station` | `char_sex` | `char_age` | `char_description` | `char_notes` — all player-editable text, default `""`

#### Group 11: Karma (4 fields)

| Field | worker_only | Notes |
|---|---|---|
| `karma_good` | false | Good karma accumulated |
| `karma_used` | false | Karma spent |
| `karma_total` | true | `karma_good + karma_used` — no flooring |
| `karma_pool` | false | Player-tracked pool (separate resource, not computed) |

#### Group 12: Encumbrance (2 fields, both worker_only)

| Field | Formula |
|---|---|
| `ep_total` | `parseFloat` sum of `weapon_ep` (rep_weapons) + `equip_ep` (rep_equipment) |
| `ep_max` | `Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)` |

#### Group 13: Armor Inputs (12 fields)

3 locations (torso | legs | head) × 4 sub-fields: `armor_{loc}_name` (text) | `armor_{loc}_piercing` | `armor_{loc}_slashing` | `armor_{loc}_impact` (all number, player-editable)

#### Group 14: Armor Totals (3 fields, all worker_only)

`armor_total_piercing` | `armor_total_slashing` | `armor_total_impact` — sum of 3 locations per type

#### Group 15: Magic / Adept Power Scalars (6 fields)

| Field | worker_only | Formula |
|---|---|---|
| `power_points_max` | true | `= mag` |
| `power_points_used` | true | `parseFloat` sum of `power_pp_cost_value` across rep_adept_powers — decimal arithmetic |
| `power_points_remaining` | true | `power_points_max - power_points_used` |
| `spells_sustained` | false | Player-tracked count of sustained spells (0–10 range) |
| `sustained_tn_mod` | true | `spells_sustained * 2` |
| `tn_warning_level` | true | 0–3: `sustained_tn_mod >= 6 → 3`, `>= 4 → 2`, `>= 2 → 1`, else `0` — CSS attribute selector drives warning colors |

- `power_points_remaining` canonical name (L2 used "remaining" not "available")
- `power_pp_cost_value` is the numeric sum source; `power_pp_cost` (text display) must NOT be used for arithmetic

#### Group 16: Essence (1 field, worker_only)

`essence_total` = `parseFloat` sum of `mutation_essence` across rep_mutations — decimal arithmetic. This is essence SPENT. To display remaining: render `6.0 - essence_total` at the view layer.

#### Group 17: Bio Questions (20 text fields)

`bio_q01` through `bio_q20` — all player-editable text, default `""`. Labels (question text) are static HTML.

#### Group 18: Sync Infrastructure (4 fields)

| Field | type | default | Notes |
|---|---|---|---|
| `char_db_id` | text | `""` | Turso character UUID; set on first sync; write-once |
| `char_sync_version` | number | `0` | Server-authoritative; updated after each successful outbound sync |
| `campaign_db_id` | text | `""` | Turso campaign UUID; GM sets once during setup |
| `sync_status` | text | `"Never synced"` | Human-readable sync feedback; displayed on Core tab |

- `turso_auth_token` NOT in sheet.json — Turso token lives in CF Worker proxy env vars only (DECISION-14)
- `btn_pull_db` deferred to V2 (DECISION-08) — no corresponding attribute needed

#### Group 19: UI State (1 field)

`sheet_compact_mode` — checkbox, default `0`, CSS-only effect via `#sheet-compact-mode:checked ~ .sheet-compact-target` rules. No Sheet Worker handler.

#### Registry Summary

| Group | Count | Notes |
|---|---|---|
| 1–5 Core Attributes | 38 | 30 editable + 8 computed |
| 6 Reaction | 3 | 1 editable + 2 computed |
| 7 Dice Pools | 12 | 4 editable + 8 computed |
| 8 Initiative | 4 | 3 editable + 1 computed |
| 9 Condition Monitors | 6 | 4 editable + 2 computed |
| 10 Identity | 6 | All editable text |
| 11 Karma | 4 | 3 editable + 1 computed |
| 12 Encumbrance | 2 | Both computed |
| 13 Armor Inputs | 12 | All editable |
| 14 Armor Totals | 3 | All computed |
| 15 Magic Scalars | 6 | 1 editable + 5 computed |
| 16 Essence | 1 | Computed |
| 17 Bio Questions | 20 | All editable text |
| 18 Sync Infrastructure | 4 | Sheet Worker writes; not cascade-computed |
| 19 UI State | 1 | Checkbox, CSS-only |
| **TOTAL** | **122** | **L2 estimate "~150" was stale** |

### Roll Buttons (NOT in attributes array)

Roll buttons are HTML elements, not stored character attributes. 18 total (17 roll + 1 action):

| Button | type | name= | V1/V2 |
|---|---|---|---|
| 9 × Attribute rolls | roll | `roll_btn_roll_{attr}` | V1 |
| Initiative | roll | `roll_btn_init_roll` | V1 |
| Dodge | roll | `roll_btn_dodge` | V1 |
| Resist Damage | roll | `roll_btn_damage_resist_body` | V1 |
| Skill Roll (per row) | roll | `roll_btn_skill_roll` | V1 |
| Cast Spell (per row) | roll | `roll_btn_cast_spell` | V1 |
| Drain Resist (per row) | roll | `roll_btn_drain_resist` | V1 |
| Ranged Attack (per row) | roll | `roll_btn_attack_ranged` | V1 |
| Melee Attack (per row) | roll | `roll_btn_attack_melee` | V1 |
| Sync to DB | action | `act_btn_sync_db` | V1 |
| Pull from DB | action | `act_btn_pull_db` | **V2 only** |

- K-scaffold roll button naming: `roll_btn_{name}` → event fires as `clicked:btn_{name}`
- K-scaffold action button naming: `act_btn_{name}` → event fires as `clicked:btn_{name}`
- [DEV DECISION] Confirm naming pattern matches installed K-scaffold version

### Repeating Section Schemas (7 sections, 42 data fields + 5 button rows)

#### repeating_skills (8 data + 1 button)

| Field | type | default | worker_only | Notes |
|---|---|---|---|---|
| `skill_name` | text | `""` | false | |
| `skill_linked_attr` | text | `"body"` | false | `<select>`: body/dex/str/cha/int/wil/hum/mag/reaction |
| `skill_general` | text | `""` | false | Category |
| `skill_spec` | text | `""` | false | Specialization |
| `skill_base` | number | 0 | false | |
| `skill_foci` | number | 0 | false | |
| `skill_misc` | number | 0 | false | |
| `skill_total` | number | 0 | true | `base + foci + misc` — per-row worker |
| `btn_skill_roll` | — | — | — | HTML button only |

#### repeating_spells (6 data + 2 buttons)

| Field | type | default | Notes |
|---|---|---|---|
| `spell_name` | text | `""` | |
| `spell_type` | text | `"M"` | `<select>`: M (Mana) / P (Physical) |
| `spell_duration` | text | `"I"` | `<select>`: I / S / P |
| `spell_target` | text | `""` | |
| `spell_force` | number | 0 | |
| `spell_drain` | text | `""` | Drain code string (e.g., "+2D", "F/2+2S") |
| `btn_cast_spell` | — | — | HTML button |
| `btn_drain_resist` | — | — | HTML button |

#### repeating_mutations (5 data)

| Field | type | default | Notes |
|---|---|---|---|
| `mutation_name` | text | `""` | |
| `mutation_level` | number | 0 | |
| `mutation_essence` | number | 0 | Decimal — `parseFloat` in workers |
| `mutation_bp_cost` | number | 0 | |
| `mutation_effect` | text | `""` | Wide display field |

#### repeating_adept_powers (5 data)

| Field | type | default | Notes |
|---|---|---|---|
| `power_name` | text | `""` | |
| `power_level` | number | 0 | |
| `power_pp_cost` | text | `""` | Display-only (e.g., "0.25/level") — NOT used for arithmetic |
| `power_pp_cost_value` | number | 0 | Numeric PP cost — decimal; `parseFloat` sum source |
| `power_effect` | text | `""` | Wide display field |

- L2 spec header says "6 fields per row" — actual verified count is 5
- `power_pp_cost` (text) and `power_pp_cost_value` (number) are intentionally separate fields

#### repeating_weapons (12 data + 2 buttons)

| Field | type | default | Notes |
|---|---|---|---|
| `weapon_name` | text | `""` | |
| `weapon_type` | text | `"Edged"` | `<select>`: Edged/Club/Polearm/Unarmed/Projectile/Thrown |
| `weapon_modifiers` | text | `""` | |
| `weapon_power` | number | 0 | |
| `weapon_damage` | text | `""` | Damage code string (e.g., "4M") |
| `weapon_conceal` | number | 0 | |
| `weapon_reach` | number | 0 | |
| `weapon_ep` | number | 0 | Feeds `ep_total` sum |
| `weapon_range_short` | text | `""` | May be number or "—" |
| `weapon_range_medium` | text | `""` | |
| `weapon_range_long` | text | `""` | |
| `weapon_range_extreme` | text | `""` | |
| `btn_attack_ranged` | — | — | HTML button |
| `btn_attack_melee` | — | — | HTML button |

#### repeating_equipment (3 data)

`equip_name` (text) | `equip_description` (text) | `equip_ep` (number, feeds `ep_total`)

#### repeating_contacts (3 data)

`contact_name` (text) | `contact_info` (text) | `contact_level` (number, default `1`, `<select>`: 1-Contact/2-Buddy/3-Friend)

**Repeating section fields do NOT appear in sheet.json `attributes` array** — they are defined in HTML `<fieldset data-groupname="repeating_{section}">` template divs. Roll20 infers schema from HTML inputs.

### Phase 1 Constraints

- All Roll20 attribute names: `lowercase_snake_case`, no spaces, no special chars
- Repeating attribute name format: `repeating_{section}_{rowId}_{fieldName}` (Roll20-assigned `rowId`)
- `worker_only` fields still require HTML input elements (hidden or readonly) — without them `setAttrs()` silently fails
- Roll20 `getAttrs()` returns ALL values as strings — `parseInt(v,10)||0` required for every addition-based formula; `parseFloat(v||0)` for decimal fields (`mutation_essence`, `power_pp_cost_value`)
- `parseInt(0.25)` returns `0` — using parseInt on decimal fields silently zeroes all fractional costs

**Verification:** Field count = 122 scalars + 42 repeating data fields + 5 button rows. Cross-reference every Phase 3 worker trigger/output against this registry.

---

## Phase 2: HTML Structure & Tab System

**Context:** Visual HTML shell can be tested locally and in Roll20's sheet sandbox before any JS. All element placements, CSS class names, and DOM ordering must be locked here.

**Implementation:**

### Document Structure

`sheet.html` has NO `<html>`, `<head>`, or `<body>` tags — Roll20 injects content into campaign page DOM. Top-level sibling ordering:

```
1. <script type="text/worker">       — K-scaffold hook (Phase 3 body)
2. <div class="sheet-hidden-infrastructure">  — 3 hidden sync fields
3. <input type="checkbox" id="sheet-compact-mode" name="attr_sheet_compact_mode">
   <label for="sheet-compact-mode">          — MUST precede all tab panels (~ selector dep)
4. 5 × <input type="radio"> + <label>        — Tab navigation
5. <div class="sheet-compact-target">         — SINGLE wrapper for all tab panels
   └─ 5 × <div class="sheet-tab-panel sheet-tab-{name}">
```

- Compact checkbox at position 3 is CRITICAL — CSS `#sheet-compact-mode:checked ~ .sheet-compact-target` requires it to precede all tab content
- `.sheet-compact-target` must be a SINGLE wrapper div, NOT a per-element class — `A ~ B C` requires C to be a descendant of B; an element cannot be its own descendant
- All tab radio inputs must precede all tab panel divs for `~` selector to work
- Default active tab: `tab-core` carries `checked` attribute

### Tab System (CSS-Only Radio Pattern)

```html
<input type="radio" name="sheet-tab-nav" id="sheet-tab-core" checked>
<label for="sheet-tab-core" class="sheet-tab-label">Core</label>
<!-- ...repeat for skills, magic, gear, bio... -->
```

CSS activation: `input#tab-core:checked ~ .sheet-tab-panel-core { display: block; }` (one rule per tab)

### Tab: Core — 9 Regions

**Region 1 — Header Strip:** `sync_status` (readonly text) | `btn_sync_db` (action button) | `cm_tn_mod` (readonly number) | `cm_init_mod` (readonly number)

**Region 2 — Identity Row:** `char_name` (wide text) | `char_race_station` | `char_sex` | `char_age` (text, not number — allows "Unknown")

**Region 3 — Condition Monitors:** 3 radio groups sharing `name="attr_cm_{track}"`. Selected radio `value` stores damage level integer (0–4 mental; 0–5 stun/physical). CSS `:checked` highlights active tier. DO NOT use separate boolean checkboxes — radio group is the only correct implementation. Plus `cm_physical_overflow` (editable number input).

**Region 4 — Attributes Table:** 7-column table (Name | Base | Mutations | Magic | Misc | Total | Roll). 9 rows: body through mag + reaction row. Reaction row: static formula label "(INT+DEX)/2" in Base cell, only misc is editable. Magic row: no mutations/magic inputs. Roll buttons: `type="roll"` with `name="roll_btn_roll_{attr}"`. DO NOT use `type="action"` for dice-rolling buttons.

**Region 5 — Initiative Row:** `init_dice` | `init_reaction_mod` | `init_misc_mod` (editable) | `init_score` (readonly) | Roll Init button

**Region 6 — Dice Pools Table:** 4-column table (Pool Name | Formula | Misc | Total). Pool base values are `type="hidden"` intermediates, not displayed.

**Region 7 — Karma Row:** `karma_good` | `karma_used` (editable) | `karma_total` (readonly) | `karma_pool` (editable)

**Region 8 — Armor Panel:** 3-column table (Torso | Legs | Head) × 4 rows (Name/Piercing/Slashing/Impact) + totals row in `<tfoot>` (readonly computed)

**Region 9 — Combat Panel:** `btn_dodge` | `btn_damage_resist_body` (roll buttons)

### Tab: Skills

- `repeating_skills` fieldset with 9-column row template
- Mutations section: `essence_total` (readonly) + `repeating_mutations` fieldset
- Adept Powers section: `power_points_used` | `power_points_max` | `power_points_remaining` (all readonly) + `repeating_adept_powers` fieldset

### Tab: Magic

- Magic summary row: `mag` (readonly) | `pool_spell` (readonly) | `spells_sustained` (editable) | `sustained_tn_mod` (readonly)
- `<input type="hidden" name="attr_tn_warning_level">` — MUST immediately precede `.sheet-tn-warning` div (CSS sibling selector dependency)
- `repeating_spells` fieldset with Cast/Drain buttons per row
- Casting reference card (static display-only block)

### Tab: Gear

- EP tracker: `ep_total` | `ep_max` (both readonly) + formula hint text
- `repeating_weapons` fieldset (14 columns including 2 buttons)
- `repeating_equipment` fieldset (3 columns)
- `repeating_contacts` fieldset (3 columns)

### Tab: Bio

- `char_description` textarea (~6 rows) | `char_notes` textarea (~6 rows)
- 20 × Session 0 question blocks: static question label + `bio_q{01-20}` textarea (~3 rows each)

### Hidden & Worker-Only Input Summary

**9 hidden inputs (type="hidden"):** `char_db_id` | `char_sync_version` | `campaign_db_id` | `reaction_base` | `pool_spell_base` | `pool_combat_base` | `pool_control_base` | `pool_astral_base` | `tn_warning_level`

**29 readonly visible inputs:** 8 attribute totals + `reaction` + 4 pool totals + `init_score` + `karma_total` + `ep_total` + `ep_max` + 3 armor totals + `cm_tn_mod` + `cm_init_mod` + `power_points_max` + `power_points_used` + `power_points_remaining` + `essence_total` + `sustained_tn_mod` + `sync_status` (text) + `skill_total` (per repeating row)

### Phase 2 Constraints

- DO NOT use `disabled` attribute on inputs — Roll20's `getAttrs()` cannot read disabled inputs in some configurations
- Checkboxes MUST include `value="1"` — without it Roll20 stores `"on"` instead of `1`, breaking Sheet Worker numeric comparisons
- All computed fields still require an HTML input element — Roll20 stores attributes server-side but only updates DOM if matching `name=` input exists
- `tn_warning_level` hidden input MUST be an immediate DOM sibling preceding `.sheet-tn-warning` — if ordering is violated, CSS warning states never activate (no error surfaces)
- K-scaffold repeating section row template: inner `<div>` is the template; K-scaffold handles add/remove controls automatically

**Verification:** 18 buttons match Phase 1 roll button registry. 9 hidden + 29 readonly = 38 worker-interface inputs verified against Phase 1 worker_only count.

---

## Phase 3: Sheet Worker Cascade & Roll Templates

**Context:** Sheet Workers are the heart of Roll20 automation. K-scaffold makes 30+ cascade workers maintainable via dependency graph resolution. All formulas, roll button values, and sync handler logic are fully specified here.

**Implementation:**

### Worker Script Structure (5 regions)

```
Region 1: K-scaffold initialization + version
Region 2: Constants (SYNC_PROXY_URL, REPEATING_SECTIONS array)
Region 3: k.registerFuncs({...}) — 30 cascade workers (order doesn't matter; K-scaffold resolves topologically)
Region 4: k.sheetOpens(() => { /* full cascade recalc */ })
Region 5: on('clicked:btn_sync_db', syncHandler) — event-driven, NOT cascade
```

### K-scaffold Registration Pattern

```javascript
k.registerFuncs({
  workerName: {
    name: 'workerName',
    trigger: ['field1', 'field2'],   // attribute changes that fire this worker
    affects: ['outputField'],        // cascade graph output declaration
    callback: function(attrs) {
      attrs.outputField = /* formula */;
      return attrs;
    }
  }
});
```

- ALL computed field workers MUST use `k.registerFuncs` — never bare `on()` calls
- Only `btn_sync_db` handler is bare `on()` (event-driven, no downstream dependencies)
- K-scaffold guarantees workers fire in topological order based on trigger/affects declarations

### Cascade Registration Table (30 workers)

| Function | Layer | Triggers | Affects | Formula |
|---|---|---|---|---|
| `calcBody` | L2 | `body_base`, `body_mutations`, `body_magic`, `body_misc` | `body` | `parseInt(base)+parseInt(mutations)+parseInt(magic)+parseInt(misc)` |
| `calcDex` | L2 | `dex_base`, `dex_mutations`, `dex_magic`, `dex_misc` | `dex` | same pattern |
| `calcStr` | L2 | `str_base`, `str_mutations`, `str_magic`, `str_misc` | `str` | same pattern |
| `calcCha` | L2 | `cha_base`, `cha_mutations`, `cha_magic`, `cha_misc` | `cha` | same pattern |
| `calcInt` | L2 | `int_base`, `int_mutations`, `int_magic`, `int_misc` | `int` | same pattern |
| `calcWil` | L2 | `wil_base`, `wil_mutations`, `wil_magic`, `wil_misc` | `wil` | same pattern |
| `calcHum` | L2 | `hum_base`, `hum_mutations`, `hum_magic`, `hum_misc` | `hum` | same pattern |
| `calcMag` | L2 | `mag_base`, `mag_misc` | `mag` | `parseInt(base)+parseInt(misc)` — no mutations/magic |
| `calcReactionBase` | L3 | `int`, `dex` | `reaction_base` | `Math.floor((parseInt(int)+parseInt(dex))/2)` |
| `calcReaction` | L3 | `reaction_base`, `reaction_misc` | `reaction` | `Math.max(1, parseInt(reaction_base)+parseInt(reaction_misc))` |
| `calcPoolSpellBase` | L4a | `cha`, `int`, `wil` | `pool_spell_base` | `Math.max(0, Math.floor((cha+int+wil)/2))` |
| `calcPoolCombatBase` | L4a | `dex`, `int`, `wil` | `pool_combat_base` | `Math.max(0, Math.floor((dex+int+wil)/2))` |
| `calcPoolControlBase` | L4a | `reaction` | `pool_control_base` | `= reaction` |
| `calcPoolAstralBase` | L4a | `int`, `wil`, `mag` | `pool_astral_base` | `Math.max(0, Math.floor((int+wil+mag)/3))` |
| `calcPoolSpell` | L4b | `pool_spell_base`, `pool_spell_misc` | `pool_spell` | `Math.max(0, parseInt(base)+parseInt(misc))` |
| `calcPoolCombat` | L4b | `pool_combat_base`, `pool_combat_misc` | `pool_combat` | same pattern |
| `calcPoolControl` | L4b | `pool_control_base`, `pool_control_misc` | `pool_control` | same pattern |
| `calcPoolAstral` | L4b | `pool_astral_base`, `pool_astral_misc` | `pool_astral` | same pattern |
| `calcInitScore` | L4c | `reaction`, `init_reaction_mod`, `init_misc_mod` | `init_score` | `parseInt(reaction)+parseInt(init_reaction_mod)+parseInt(init_misc_mod)` |
| `calcEpMax` | L5 | `str`, `body` | `ep_max` | `Math.max(str,body)*4+Math.floor(Math.min(str,body)/2)` |
| `calcEpTotal` | L5 | `repeating_weapons:weapon_ep`, `repeating_equipment:equip_ep` | `ep_total` | `parseFloat` sum across both sections (Pattern A) |
| `calcArmorTotals` | L5 | all 9 armor inputs | `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact` | Sum of 3 locations per type |
| `calcSkillTotal` | L5 | `skill_base`, `skill_foci`, `skill_misc` (per row) | `skill_total` (per row) | `parseInt(base)+parseInt(foci)+parseInt(misc)` (Pattern B) |
| `calcPowerPointsMax` | L5 | `mag` | `power_points_max` | `= mag` |
| `calcPowerPointsUsed` | L5 | `repeating_adept_powers:power_pp_cost_value` | `power_points_used` | `parseFloat` sum (Pattern A) |
| `calcPowerPointsRemaining` | L5 | `power_points_max`, `power_points_used` | `power_points_remaining` | `max - used` |
| `calcEssenceTotal` | L5 | `repeating_mutations:mutation_essence` | `essence_total` | `parseFloat` sum = essence SPENT |
| `calcKarmaTotal` | L6 | `karma_good`, `karma_used` | `karma_total` | `parseInt(good)+parseInt(used)` |
| `calcCmPenalties` | L6 | `cm_mental`, `cm_stun`, `cm_physical` | `cm_tn_mod`, `cm_init_mod` | `penaltyOf = lvl => Math.min(parseInt(lvl),3)`; `cm_tn_mod = Math.max(...)`, `cm_init_mod = -1 * cm_tn_mod` |
| `calcSustainedPenalty` | L6 | `spells_sustained` | `sustained_tn_mod`, `tn_warning_level` | `sustained_tn_mod = spells_sustained*2`; warning: `>=6->3, >=4->2, >=2->1, else 0` |

**Cascade layer summary:** L1->raw inputs -> L2->8 attr totals -> L3->reaction -> L4a->4 pool bases -> L4b->4 pool totals -> L4c->init_score -> L5->aggregates -> L6->modifiers

**Repeating section worker patterns:**
- Pattern A (full-section iteration): `calcEpTotal`, `calcPowerPointsUsed`, `calcEssenceTotal` — fires on any row change, callback receives all rows; guard empty sections with `|| []`
- Pattern B (per-row scope): `calcSkillTotal` — fires within changed row context, writes to that row only

**`k.sheetOpens` handler:** Must trigger full cascade recalculation. Preferred: K-scaffold built-in `k.recalcAll()` if available. Fallback: trigger root attrs for all independent chains (`body_base`, `str_base`, `cha_base`, `int_base`, `wil_base`, `hum_base`, `mag_base`, `karma_good`, `cm_mental`, `spells_sustained`, + repeating section changes). Triggering only `body_base` will miss independent chains like `calcKarmaTotal`.

### Roll Template HTML Skeletons

3 templates defined OUTSIDE tab structure, after all tab panel divs:

#### rolltemplate-skill

```html
<rolltemplate class="sheet-rolltemplate-skill">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-skill">
      {{charname}} -- {{rollname}}
    </div>
    <div class="sheet-template-body">
      <div class="sheet-template-row">
        <span class="sheet-label">TN:</span> <span>{{tn}}</span>
      </div>
      {{#linked_attr}}
      <div class="sheet-template-row">
        <span class="sheet-label">Linked:</span> <span>{{linked_attr}}</span>
      </div>
      {{/linked_attr}}
      <div class="sheet-template-row sheet-template-roll-result">
        <span class="sheet-label">Successes:</span> <span>{{successes}}</span>
      </div>
      {{^successes}}
      <div class="sheet-template-warning">
        Warning: No successes -- check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

Header bg: `#1a1a2e` (dark navy). Used by: 9 attr rolls, skill roll, dodge, damage resist.

- Parameter `linked_attr` (NOT `linked`) — L2 Task 3.15 incorrectly used `{{linked=...}}`, which causes silent failure
- `{{^successes}}` fires on any zero-success result (ordinary misses AND critical failures)

#### rolltemplate-attack

```html
<rolltemplate class="sheet-rolltemplate-attack">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-attack">
      {{charname}} -- {{rollname}}
    </div>
    <div class="sheet-template-body">
      <div class="sheet-template-row">
        <span class="sheet-label">Weapon:</span> <span>{{weapon_name}}</span>
      </div>
      <div class="sheet-template-row">
        <span class="sheet-label">TN:</span> <span>{{tn}}</span>
        <span class="sheet-label">Power:</span> <span>{{power}}</span>
        <span class="sheet-label">Dmg:</span> <span>{{damage_code}}</span>
      </div>
      {{#reach}}
      <div class="sheet-template-row">
        <span class="sheet-label">Reach:</span> <span>{{reach}}</span>
      </div>
      {{/reach}}
      {{#range_band}}
      <div class="sheet-template-row">
        <span class="sheet-label">Range:</span> <span>{{range_band}}</span>
      </div>
      {{/range_band}}
      <div class="sheet-template-row sheet-template-roll-result">
        <span class="sheet-label">Successes:</span> <span>{{successes}}</span>
      </div>
      {{^successes}}
      <div class="sheet-template-warning">
        Warning: No successes -- check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

Header bg: `#3a1c1c` (dark maroon). Used by: ranged/melee attacks. `reach` shown for melee only; `range_band` for ranged only (via Mustache conditionals).

#### rolltemplate-spell

```html
<rolltemplate class="sheet-rolltemplate-spell">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-spell">
      {{charname}} -- {{rollname}}
    </div>
    <div class="sheet-template-body">
      <div class="sheet-template-row">
        <span class="sheet-label">Spell:</span> <span>{{spell_name}}</span>
        <span class="sheet-label">Type:</span> <span>{{spell_type}}</span>
        <span class="sheet-label">Duration:</span> <span>{{spell_duration}}</span>
      </div>
      <div class="sheet-template-row">
        <span class="sheet-label">Force:</span> <span>{{force}}</span>
        <span class="sheet-label">TN:</span> <span>{{tn}}</span>
        <span class="sheet-label">Drain:</span> <span>{{drain_code}}</span>
      </div>
      <div class="sheet-template-row">
        <span class="sheet-label">Sustained TN Mod:</span> <span>{{sustained_penalty}}</span>
      </div>
      <div class="sheet-template-row sheet-template-roll-result">
        <span class="sheet-label">Successes:</span> <span>{{successes}}</span>
      </div>
      {{^successes}}
      <div class="sheet-template-warning">
        Warning: No successes -- check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

Header bg: `#1c3a5e` (dark blue). Used by: cast spell, drain resist.

### Production Roll Button Formula Registry (paste-ready)

All success-counting rolls use `cf<=1` (renders 1s red in dice tray — SR3 critical failure visual). `btn_init_roll` is the only exempt button (plain sum roll).

| Button `name=` | `value=` |
|---|---|
| `roll_btn_roll_body` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Body}} {{tn=?{Target Number\|4}}} {{successes=[[@{body}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_dex` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Dexterity}} {{tn=?{Target Number\|4}}} {{successes=[[@{dex}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_str` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Strength}} {{tn=?{Target Number\|4}}} {{successes=[[@{str}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_cha` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Charisma}} {{tn=?{Target Number\|4}}} {{successes=[[@{cha}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_int` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Intelligence}} {{tn=?{Target Number\|4}}} {{successes=[[@{int}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_wil` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Willpower}} {{tn=?{Target Number\|4}}} {{successes=[[@{wil}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_hum` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Humanity}} {{tn=?{Target Number\|4}}} {{successes=[[@{hum}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_reaction` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Reaction}} {{tn=?{Target Number\|4}}} {{successes=[[@{reaction}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_mag` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Magic}} {{tn=?{Target Number\|4}}} {{successes=[[@{mag}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_init_roll` | `@{init_dice}d6 + @{init_score}` |
| `roll_btn_dodge` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Dodge}} {{tn=4}} {{successes=[[?{Combat Pool dice for dodge\|0}d6cs>=4 cf<=1]]}}` |
| `roll_btn_damage_resist_body` | `&{template:skill} {{charname=@{char_name}}} {{rollname=Resist Damage (Body)}} {{tn=?{TN (Power - Armor)\|0}}} {{successes=[[(@{body} + ?{Combat Pool dice\|0})d6cs>=?{TN (Power - Armor)\|0} cf<=1]]}}` |
| `roll_btn_skill_roll` | `&{template:skill} {{charname=@{char_name}}} {{rollname=@{skill_name}}} {{linked_attr=@{skill_linked_attr}}} {{tn=?{Target Number\|4}}} {{successes=[[(@{skill_total} + ?{Pool dice to add\|0})d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_cast_spell` | `&{template:spell} {{charname=@{char_name}}} {{rollname=Cast Spell}} {{spell_name=@{spell_name}}} {{spell_type=@{spell_type}}} {{spell_duration=@{spell_duration}}} {{force=@{spell_force}}} {{drain_code=@{spell_drain}}} {{sustained_penalty=@{sustained_tn_mod}}} {{tn=?{Target Number\|4}}} {{successes=[[(?{Sorcery dice\|0} + ?{Spell Pool dice\|0})d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_drain_resist` | `&{template:spell} {{charname=@{char_name}}} {{rollname=Drain Resist}} {{spell_name=@{spell_name}}} {{spell_type=@{spell_type}}} {{spell_duration=@{spell_duration}}} {{force=@{spell_force}}} {{drain_code=@{spell_drain}}} {{sustained_penalty=@{sustained_tn_mod}}} {{tn=?{Drain TN\|0}}} {{successes=[[(@{wil} + ?{Remaining Spell Pool dice\|0})d6cs>=?{Drain TN\|0} cf<=1]]}}` |
| `roll_btn_attack_ranged` | `&{template:attack} {{charname=@{char_name}}} {{rollname=Ranged Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{range_band=?{Range Band\|Short}}} {{tn=?{Range TN\|4}}} {{successes=[[(?{Skill dice\|0} + ?{Combat Pool dice\|0})d6cs>=?{Range TN\|4} cf<=1]]}}` |
| `roll_btn_attack_melee` | `&{template:attack} {{charname=@{char_name}}} {{rollname=Melee Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{reach=@{weapon_reach}}} {{tn=?{TN\|4}}} {{successes=[[(?{Skill dice\|0} + ?{Combat Pool dice\|0})d6cs>=?{TN\|4} cf<=1]]}}` |
| `act_btn_sync_db` | N/A — action button, fires `clicked:btn_sync_db` only |

- L2 Task 3.15 initiative formula is invalid (`/roll` + `&{template}` cannot coexist in button value). Correct: plain sum `@{init_dice}d6 + @{init_score}`
- Skill roll uses `{{linked_attr=...}}` NOT `{{linked=...}}` — L2 Task 3.15 is wrong; this table is authoritative
- Dodge TN hardcoded `4` (SR3 rule). Drain resist default `0` is a safety placeholder — player must enter correct TN
- `cf<=1` on the same expression is the only correct Roll20-native technique for SR3 critical failure visual — a separate `[[Nd6cs<=1]]` expression rolls independent dice

### Sync Handler Architecture (btn_sync_db)

Event-driven handler. NOT in `k.registerFuncs`. Registered as bare `on('clicked:btn_sync_db', callback)` in Region 5.

**6-step execution flow:**

```
Step 1: setAttrs({ sync_status: 'Syncing...' }) — immediate visual feedback
Step 2: getAttrs(['char_db_id','campaign_db_id','char_sync_version']) -> control fields
        Guard: if !campaign_db_id -> set error status, return
Step 3: getAttrs(SCALAR_FIELDS_TO_SYNC) + collect 7 repeating sections -> build payload
        payload = {
          character_id: charDbId || null,
          campaign_id: campaignId,
          sync_version_from: parseInt(syncVersion) || 0,
          synced_at: ISO 8601 timestamp,
          scalars: { ...90 included fields... },
          repeating: { skills:[], spells:[], mutations:[], adept_powers:[], weapons:[], equipment:[], contacts:[] }
        }
Step 4: fetch(SYNC_PROXY_URL, { method:'POST', headers:{'Content-Type':'application/json','X-Campaign-Secret':...}, body:JSON.stringify(payload) })
Step 5a (success): setAttrs({
          char_db_id: attrs.char_db_id || response.char_db_id,  // preserve existing; set on first sync
          char_sync_version: response.sync_version.toString(),   // SERVER-authoritative, never local increment
          sync_status: 'Synced -- ' + new Date().toLocaleString()
        })
Step 5b (failure): setAttrs({ sync_status: 'Sync failed -- check console' })
                   DO NOT modify char_db_id or char_sync_version on failure
```

- `SYNC_PROXY_URL` = empty string `''` during dev; fill after CF Worker deployment
- V1 is outbound-only — no inbound pull handler, no `btn_pull_db` implementation
- Sync infra fields (`char_db_id`, `char_sync_version`, `campaign_db_id`, `sync_status`) are NOT in the `scalars` payload object — they are top-level sync metadata
- Total included scalar fields: 122 - 28 worker_only - 4 sync_infra = ~90

**Verification:** 30 registered cascade workers + 1 event handler = 31 total handlers. 18 buttons with production formulas. 3 roll templates.

---

## Phase 4: CSS Design System

**Context:** CSS defines the finished character sheet interface. Roll20 iframe constraints (no `var()`, no `:root`, no `@import`) require all styles to use inline hex values. Verified against 10 L2 amendments (4-A through 4-J).

**Implementation:**

### Color Token Reference (all locked — inline hex only)

```
TEXT_PRIMARY:        #000000    TEXT_ON_DARK:     #ffffff
SURFACE_HEADER:      #f2f2f2    BORDER_STRONG:    #5f5f5f
BORDER_LIGHT:        #cccccc    BORDER_FOCUS:     #888888
CHECKBOX_BORDER:     #555555    DAMAGE_X:         #b81a1a
TAB_NAV:             #dddddd    SURFACE_INIT:     #000000
WARN_AMBER:          #e6a817    WARN_ORANGE:      #e06c00
WARN_RED:            #cc2200    SUCCESS:          #1a7a1a
TEMPLATE_SKILL:      #1a1a2e    TEMPLATE_ATTACK:  #3a1c1c
TEMPLATE_SPELL:      #1c3a5e    ROW_ALT:          #f9f9f9
```

### CSS Section Ordering (20 sections, implement in this exact order)

1. **Color token comment block** — comments only, NOT custom properties
2. **Global reset** — `box-sizing: border-box`, normalize Roll20-inflated input styles (border-radius:0, height:auto), `select` reset, textarea resize:vertical, heading margins, button cursor. Roll20 injects `height`, `border-radius`, `padding` on inputs — must be explicitly overridden
3. **Tab navigation** — `.sheet-tab-nav` flex row, hidden radio inputs, label styling, active label (`input.sheet-tab-radio:checked + label.sheet-tab-label` with `#5f5f5f` bg + white text, fully qualified per Amendment 4-J FINDING-15), default panels `display:none`, 5 activation rules
4. **Attribute table** — `.sheet-box-attribute` inline-flex, 850px max-width, 7-column min-widths (140/55x5/50px), alternating row bg `#f9f9f9`, number inputs 45px centered, bold total cell, roll button column
5. **Condition monitor** — `.sheet-box-condition` border container, `.sheet-condition-track` per track, flex grid 12% tier cells, "No Damage" column (italic gray, no checkboxes per D5), TN/Init penalty labels, Uncon header red `#b81a1a`, overflow input 40px. Damage checkbox: `appearance:none` + 16x16px + `::before` content `\2718` red glyph. Base rule has ALL dimensions; `:checked` rule visual additions ONLY (Amendment 4-J FINDING-10)
6. **Dice pools + init black box** — `.sheet-box-dice-pool` inline-flex, init black box `#000000` bg white text, pool table with formula/misc/total columns
7. **Initiative row** — `.sheet-initiative-row` flex row, 42px inputs, init_score field: black bg white text bold (echoes init box)
8. **Karma row** — `.sheet-karma-row` flex row, 55px inputs, karma_total gray bg `#f2f2f2`
9. **Repeating section base** — `.sheet-repcontainer`/`.repcontainer` (dual selector per D7), `.repitem` flex row, alternating bg, `.repcontrol_del` red right-aligned, `.repcontrol_add` button, `.repitem button[type="roll"]` compact
10. **Skills tab columns** — `.sheet-skill-name` flex:2, linked 70px, general/spec flex:1, base/foci/misc 38px, total 42px bold `#f2f2f2` bg
11. **Magic tab columns** — spell name flex:2, drain/force 50px; mutation name flex:2, effect flex:3; power name flex:2, pp-cost 50px
12. **Gear tab weapon columns** — weapon name flex:2, type 80px, mods flex:1, power/damage/conceal/reach/ep compact columns, range bands 4x36px, attack buttons auto
13. **Gear/Bio tab columns** — equipment name flex:2, qty 40px, weight 50px; contact name flex:2, loyalty/connection 50px
14. **Computed badges** — `.sheet-computed-badge` inline-block gray bg, used for essence and power point displays
15. **Roll template CSS** — Structural pattern shared (wrapper, header, body, rows, labels). Per-type: skill `#1a1a2e` border+header, attack `#3a1c1c`, spell `#1c3a5e`. Success badge: `#1a7a1a` bg white bold 16px. No-success warning: `#b81a1a` italic. Critical fail: `#b81a1a` on `#fce8e8` bg
16. **Combat panel + armor table** — `.sheet-combat-panel` with `.sheet-armor-region` table (3-col x 4-row, tfoot totals), combat buttons flex equal-width
17. **Magic TN warning ramp** — Attribute selector pattern (NOT class-based): `input[name="attr_tn_warning_level"][value="1"] ~ .sheet-tn-warning { display:inline-block; background:#e6a817; color:#000 }`, value="2": `#e06c00`/white, value="3": `#cc2200`/white. Default `.sheet-tn-warning { display:none }`. Hidden input MUST be immediate preceding DOM sibling
18. **Gear tab EP tracker** — `.sheet-ep-tracker` flex row, 45px inputs, separator `/`
19. **Bio tab** — Full-width textareas (resize:vertical, box-sizing), Session 0 question blocks with left-border accent `#5f5f5f`
20. **Compact fallback** — `input#sheet-compact-mode` visually hidden (position:absolute, opacity:0, 1px — NO pointer-events:none per FINDING-2), label with cursor:pointer. Compact rules via `#sheet-compact-mode:checked ~ .sheet-compact-target`: attribute table -> block, hide Mutations/Magic columns (3rd/4th), dice pool -> block, weapon rows -> flex-wrap. `@media` block commented out pending D6

### Sandbox Verification Items (run BEFORE writing CSS)

| ID | Test | Pass Action | Fail Action |
|---|---|---|---|
| D8 (run first) | `appearance:none` suppresses native checkbox in Chrome+Firefox on Roll20 | Use `::before` pattern | Restructure Phase 2 HTML: hidden checkbox + adjacent `<label>` + `label::before` pattern |
| D7 | K-scaffold generates `.sheet-repcontainer` as outer wrapper | Keep `.sheet-repcontainer` | Replace with `.repcontainer` |
| D9 | `attr_tn_warning_level` and `.sheet-tn-warning` are direct DOM siblings | Section 17 `~` selectors work | Reposition hidden input in HTML |
| D10 | `input#sheet-compact-mode` is direct DOM sibling of all tab panels | Section 20 compact toggle works | Move checkbox to tab-panel sibling level |
| D6 | `@media (max-width:500px)` applies inside Roll20 iframe | Uncomment `@media` block | Leave commented — manual toggle only |

### Phase 4 Constraints

- FORBIDDEN: `var(--anything)` -> resolves to `unset` in iframe; `:root {}` -> targets parent frame; `@import` -> not supported
- Tab-scoped selectors use `.sheet-tab-panel-magic` (correct) NOT `.sheet-tab-magic` (dead selector)
- Active tab label selector must be fully qualified: `input.sheet-tab-radio:checked + label.sheet-tab-label`
- Weapon row static header `.sheet-weapons-header` must match `.repitem` flex column widths exactly
- Roll template CSS lives in same `<style>` block — Roll20 applies it to chat output automatically
- `.sheet-rolltemplate-{name}` prefix is Roll20's mandatory naming convention

**Verification:** 20 CSS sections in correct dependency order. 5 sandbox items (D6-D10). All 8+10 locked color tokens embedded as inline hex constants.

---

## Phase 5: Companion App Architecture & Data Sync

**Context:** Companion web app provides read-only character viewing between sessions. Uses Turso (free edge SQLite, no dormancy risk) + SvelteKit on Cloudflare Pages + Discord OAuth. V1 is READ-ONLY — zero write paths from companion app. Companion app is a separate TEMPO workflow; this blueprint is the handoff document.

**Implementation:**

### Turso Schema (12 tables, all SQLite-native types)

All columns use SQLite types only: `INTEGER` | `TEXT` | `REAL`. No SERIAL, BOOLEAN, UUID, DATETIME, JSON column types. UUIDs stored as TEXT. Timestamps as TEXT (ISO 8601). Booleans as INTEGER 0/1.

#### campaigns

```sql
CREATE TABLE campaigns (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

#### players

```sql
CREATE TABLE players (
  id TEXT PRIMARY KEY,
  campaign_id TEXT NOT NULL REFERENCES campaigns(id),
  display_name TEXT NOT NULL,
  discord_user_id TEXT NOT NULL UNIQUE,
  is_gm INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
```

- `discord_user_id`: stable Discord snowflake ID, stored as TEXT, NOT hashed (non-secret public identifier)
- `is_gm`: set directly in Turso by GM; not self-assignable; retained for V2 GM dashboard

#### characters

```sql
CREATE TABLE characters (
  id TEXT PRIMARY KEY,
  player_id TEXT NOT NULL REFERENCES players(id),
  campaign_id TEXT NOT NULL REFERENCES campaigns(id),
  char_name TEXT NOT NULL DEFAULT '',
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  sync_version INTEGER NOT NULL DEFAULT 0
);
```

- `char_name` denormalized from scalar blob for fast lookups; updated on every sync
- `sync_version`: monotonic counter incremented on each successful write; `sync_version_from` in payload must match (or be <=)
- `campaign_id` denormalized for campaign-wide dashboard queries (V2)

#### character_scalars

```sql
CREATE TABLE character_scalars (
  character_id TEXT PRIMARY KEY REFERENCES characters(id),
  data TEXT NOT NULL
);
```

- `data`: JSON blob of all included scalar fields (~2.5KB). `json_extract()` can query without full deserialize
- Schema evolution: new Roll20 fields absorbed without ALTER TABLE; companion app ignores unknown keys

#### rep_skills

```sql
CREATE TABLE rep_skills (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  skill_name TEXT,
  skill_linked_attr TEXT,
  skill_general TEXT,
  skill_spec TEXT,
  skill_base INTEGER,
  skill_foci INTEGER,
  skill_misc INTEGER
);
```

`skill_total` NOT stored — computed by companion app.

#### rep_spells

```sql
CREATE TABLE rep_spells (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  spell_name TEXT,
  spell_type TEXT,
  spell_duration TEXT,
  spell_target TEXT,
  spell_force INTEGER,
  spell_drain TEXT
);
```

#### rep_mutations

```sql
CREATE TABLE rep_mutations (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  mutation_name TEXT,
  mutation_level INTEGER,
  mutation_essence REAL,
  mutation_bp_cost INTEGER,
  mutation_effect TEXT
);
```

`essence_total` NOT stored — companion app sums `mutation_essence`.

#### rep_adept_powers

```sql
CREATE TABLE rep_adept_powers (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  power_name TEXT,
  power_level INTEGER,
  power_pp_cost TEXT,
  power_pp_cost_value REAL,
  power_effect TEXT
);
```

`power_points_used`/`power_points_remaining` NOT stored — computed from `SUM(power_pp_cost_value)`.

#### rep_weapons

```sql
CREATE TABLE rep_weapons (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  weapon_name TEXT,
  weapon_type TEXT,
  weapon_modifiers TEXT,
  weapon_power INTEGER,
  weapon_damage TEXT,
  weapon_conceal INTEGER,
  weapon_reach INTEGER,
  weapon_ep INTEGER,
  weapon_range_short TEXT,
  weapon_range_medium TEXT,
  weapon_range_long TEXT,
  weapon_range_extreme TEXT
);
```

#### rep_equipment

```sql
CREATE TABLE rep_equipment (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  equip_name TEXT,
  equip_description TEXT,
  equip_ep INTEGER
);
```

#### rep_contacts

```sql
CREATE TABLE rep_contacts (
  id TEXT PRIMARY KEY,
  character_id TEXT NOT NULL REFERENCES characters(id),
  row_order INTEGER,
  contact_name TEXT,
  contact_info TEXT,
  contact_level INTEGER
);
```

#### Indices (10 total)

```sql
CREATE INDEX idx_characters_player ON characters(player_id);
CREATE INDEX idx_characters_campaign ON characters(campaign_id);
-- character_scalars PK on character_id enforces uniqueness
CREATE INDEX idx_rep_skills_char ON rep_skills(character_id);
CREATE INDEX idx_rep_spells_char ON rep_spells(character_id);
CREATE INDEX idx_rep_mutations_char ON rep_mutations(character_id);
CREATE INDEX idx_rep_adept_powers_char ON rep_adept_powers(character_id);
CREATE INDEX idx_rep_weapons_char ON rep_weapons(character_id);
CREATE INDEX idx_rep_equipment_char ON rep_equipment(character_id);
CREATE INDEX idx_rep_contacts_char ON rep_contacts(character_id);
```

### Sync Payload Contract

**Outbound (Roll20 -> CF Worker proxy -> Turso):** Always full snapshot, no delta patches.

```json
{
  "character_id": "uuid or empty string on first sync",
  "campaign_id": "campaign uuid",
  "sync_version_from": 0,
  "synced_at": "ISO 8601",
  "scalars": { "body_base": 5, "dex_base": 3, "..." : "..." },
  "repeating": {
    "skills": [{ "_rowId": "-M7X9...", "_rowOrder": 0, "skill_name": "...", "..." : "..." }],
    "spells": [], "mutations": [], "adept_powers": [],
    "weapons": [], "equipment": [], "contacts": []
  }
}
```

**Excluded from `scalars`:**
- 28 worker_only computed fields (Group 5 totals, reaction_base, reaction, 4 pool bases, 4 pool totals, init_score, ep_max, ep_total, 3 armor totals, power_points_max/used/remaining, essence_total, karma_total, cm_tn_mod, cm_init_mod, sustained_tn_mod, tn_warning_level, skill_total per row)
- 4 sync infra fields (sent as top-level: `char_db_id`->`character_id`, `char_sync_version`->`sync_version_from`, `campaign_db_id`->`campaign_id`; `sync_status` excluded entirely)
- All roll buttons (HTML-only, not stored attributes)
- Total included: ~90 fields

### Cloudflare Worker Proxy

Standalone CF Worker (separate `wrangler.toml`, NOT part of SvelteKit Pages app).

**Request contract:**
```
POST {PROXY_URL}/sync
Content-Type: application/json
X-Campaign-Secret: {campaign_secret value}
Body: {full payload JSON}
```

**Validation pipeline:**
1. Reject non-POST -> 405
2. Validate `X-Campaign-Secret` against `env.CAMPAIGN_SECRET` -> 401
3. Parse JSON -> 400 if malformed
4. Validate: `campaign_id` non-empty + matches `env.KNOWN_CAMPAIGN_ID`; `character_id` is string; `scalars` is object; `repeating` has 7 keys -> 400 if invalid
5. First-sync path if `character_id === ""`: generate UUID, create character row IN SAME TRANSACTION
6. Forward to Turso pipeline API -> 200 `{ ok:true, char_db_id, new_sync_version }` | 502 on failure

**Turso pipeline API target:** `POST {TURSO_DB_URL}/v2/pipeline` with `Authorization: Bearer {TURSO_WRITE_TOKEN}`

**Pipeline transaction structure:**
```
BEGIN
  -- First-sync only: INSERT INTO characters (...)
  INSERT INTO character_scalars ... ON CONFLICT DO UPDATE SET data = excluded.data
  UPDATE characters SET char_name=?, updated_at=?, sync_version=sync_version+1 WHERE id=?
  -- For each of 7 rep tables: DELETE FROM rep_{x} WHERE character_id=?
  -- Then INSERT per row from payload.repeating.{x}
COMMIT
```

- ALL statements inside BEGIN/COMMIT — atomic; partial write is an invalid state
- First-sync INSERT INTO characters MUST be inside the transaction — never outside (orphaned row on pipeline failure)
- After COMMIT: `SELECT sync_version FROM characters WHERE id=?` -> return as `new_sync_version`

**Environment variables:**
- `CAMPAIGN_SECRET` — shared secret matched against header
- `KNOWN_CAMPAIGN_ID` — expected Turso campaign UUID
- `TURSO_DB_URL` — `https://{db-name}-{org}.turso.io` (HTTP scheme, not `libsql://`)
- `TURSO_WRITE_TOKEN` — write-only, never transmitted to client

**Security model:** `campaign_secret` is readable by all 6 players (accepted residual risk with trusted player base). Proxy's value is keeping the real Turso write token server-side. Document in README.

### Sheet Worker Sync Handler (SCALAR_FIELDS_TO_SYNC array)

```javascript
const SCALAR_FIELDS_TO_SYNC = [
  // Group 1: base values (8)
  'body_base','dex_base','str_base','cha_base','int_base','wil_base','hum_base','mag_base',
  // Group 2: mutations (7, mag excluded)
  'body_mutations','dex_mutations','str_mutations','cha_mutations','int_mutations','wil_mutations','hum_mutations',
  // Group 3: magic sub-values (7, mag excluded)
  'body_magic','dex_magic','str_magic','cha_magic','int_magic','wil_magic','hum_magic',
  // Group 4: misc (8, all including mag)
  'body_misc','dex_misc','str_misc','cha_misc','int_misc','wil_misc','hum_misc','mag_misc',
  // Group 6: reaction misc (1)
  'reaction_misc',
  // Group 7: pool misc (4)
  'pool_spell_misc','pool_combat_misc','pool_control_misc','pool_astral_misc',
  // Group 8: initiative (3, init_score excluded)
  'init_dice','init_reaction_mod','init_misc_mod',
  // Group 9: condition monitors (4)
  'cm_mental','cm_stun','cm_physical','cm_physical_overflow',
  // Group 10: identity (6)
  'char_name','char_race_station','char_sex','char_age','char_description','char_notes',
  // Group 11: karma (3, karma_total excluded)
  'karma_good','karma_used','karma_pool',
  // Group 13: armor inputs (12)
  'armor_torso_name','armor_torso_piercing','armor_torso_slashing','armor_torso_impact',
  'armor_legs_name','armor_legs_piercing','armor_legs_slashing','armor_legs_impact',
  'armor_head_name','armor_head_piercing','armor_head_slashing','armor_head_impact',
  // Group 15: spells_sustained (1)
  'spells_sustained',
  // Group 17: bio questions (20)
  'bio_q01','bio_q02','bio_q03','bio_q04','bio_q05','bio_q06','bio_q07','bio_q08','bio_q09','bio_q10',
  'bio_q11','bio_q12','bio_q13','bio_q14','bio_q15','bio_q16','bio_q17','bio_q18','bio_q19','bio_q20',
  // Group 19: UI state (1)
  'sheet_compact_mode'
];
```

### SvelteKit Project Structure

```
companion-app/
  src/
    app.html                          -- HTML shell
    app.d.ts                          -- Session augmentation (discord_user_id, player_id)
    hooks.server.ts                   -- Auth.js SvelteKitAuth handle
    lib/
      db.ts                           -- Turso @libsql/client singleton
      computed.ts                     -- DerivedFields interface + computeDerivedFields()
      types.ts                        -- Character, ScalarBlob, RepRow, Session interfaces
    routes/
      +layout.server.ts               -- Session guard -> redirect /login
      +layout.svelte                  -- Nav shell
      +page.svelte                    -- / -> redirect authenticated to /characters
      login/+page.svelte              -- Discord OAuth button
      auth/[...auth]/+server.ts       -- Auth.js catch-all route handler
      characters/
        +page.server.ts               -- load(): characters WHERE player_id=?
        +page.svelte                  -- Character list
        [id]/
          +page.server.ts             -- load(): full character + scalars + 7 rep tables + derived
          +page.svelte                -- Read-only character sheet (tabbed)
      logout/+server.ts               -- signOut -> redirect /
  svelte.config.js                    -- adapter-cloudflare
  package.json                        -- @auth/sveltekit, @libsql/client, adapter-cloudflare
  .env.local                          -- DISCORD_CLIENT_ID/SECRET, AUTH_SECRET, TURSO_APP_URL/TOKEN
  wrangler.toml                       -- CF Pages deployment
```

**Dependencies:** `@auth/sveltekit` + `@auth/core` | `@libsql/client` (import from `@libsql/client/web` for CF Workers runtime — NOT default export which uses Node.js native modules) | `@sveltejs/adapter-cloudflare`

**Environment variables (CF Pages env vars for production):**

| Variable | Used by |
|---|---|
| `DISCORD_CLIENT_ID` | Auth.js |
| `DISCORD_CLIENT_SECRET` | Auth.js |
| `AUTH_SECRET` | Auth.js JWT signing (32+ chars) |
| `TURSO_APP_URL` | SvelteKit server loads |
| `TURSO_APP_TOKEN` | SvelteKit server loads (read+write, separate from proxy write-only token) |

- Access pattern: `event.platform?.env.VARIABLE_NAME` (NOT `process.env` — Cloudflare runtime)

### Auth.js Discord OAuth

**hooks.server.ts skeleton:**

```typescript
import { SvelteKitAuth } from '@auth/sveltekit';
import Discord from '@auth/core/providers/discord';

export const { handle } = SvelteKitAuth(async (event) => ({
  providers: [Discord({
    clientId: event.platform?.env.DISCORD_CLIENT_ID,
    clientSecret: event.platform?.env.DISCORD_CLIENT_SECRET,
  })],
  secret: event.platform?.env.AUTH_SECRET,
  trustHost: true,
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account && profile) {
        token.discord_user_id = profile.id;
        const playerId = await upsertAndGetPlayerId(profile, event.platform?.env);
        token.player_id = playerId;
      }
      return token;
    },
    async session({ session, token }) {
      session.discord_user_id = token.discord_user_id as string;
      session.player_id = token.player_id as string;
      return session;
    },
  },
}));
```

**First-login player upsert:**
1. Extract `discord_user_id = profile.id` (stable Discord snowflake)
2. `SELECT id FROM players WHERE discord_user_id = ?`
3. If exists -> use existing player_id
4. If not -> generate UUID, `INSERT INTO players` with `is_gm=0`, `campaign_id=KNOWN_CAMPAIGN_ID`
5. Store player_id in JWT token

**Session shape (app.d.ts):**

```typescript
declare module '@auth/core/types' {
  interface Session {
    user: { name?: string | null; email?: string | null; image?: string | null; };
    discord_user_id: string;
    player_id: string;  // Turso players.id UUID — key for all ownership checks
  }
}
```

**Discord callback URL:** `{APP_URL}/auth/callback/discord` — register both localhost and production URLs in Discord developer app OAuth2 settings.

### Turso Client Singleton

```typescript
// src/lib/db.ts
import { createClient, type Client } from '@libsql/client/web';

let _client: Client | null = null;

export function getDb(env: { TURSO_APP_URL: string; TURSO_APP_TOKEN: string }): Client {
  if (!_client) {
    _client = createClient({ url: env.TURSO_APP_URL, authToken: env.TURSO_APP_TOKEN });
  }
  return _client;
}
```

- CF Workers may re-instantiate between requests — singleton avoids unnecessary overhead but don't rely on survival across all requests
- ALL queries MUST use parameterized syntax: `db.execute({ sql: '...WHERE id=?', args: [id] })` — NEVER string concatenation (OWASP A03)

### Route Load Functions

**`/characters` (+page.server.ts):**
```
session = await event.locals.auth() -> redirect /login if unauthenticated
SELECT id, char_name, char_race_station, is_active, updated_at
FROM characters WHERE player_id = ? AND is_active = 1
ORDER BY char_name ASC
```

**`/characters/[id]` (+page.server.ts):**
```
session = await event.locals.auth() -> redirect /login
Validate event.params.id format -> 400 if malformed
SELECT c.*, cs.data FROM characters c JOIN character_scalars cs
  ON cs.character_id = c.id WHERE c.id = ? AND c.player_id = ?
-> 404 if no rows (ownership guard: guessing UUID gets 404, not 403)
scalars = JSON.parse(scalar_data)
Parallel: 7 x SELECT * FROM rep_{x} WHERE character_id=? ORDER BY row_order
derived = computeDerivedFields(scalars, { skills, mutations, adept_powers, weapons, equipment })
return { character, scalars, repeating, derived }
```

### Computed Field Recalculation (computed.ts — paste-ready)

```typescript
export interface DerivedFields {
  body: number; dex: number; str: number; cha: number;
  int: number; wil: number; hum: number; mag: number;
  reaction_base: number; reaction: number;
  pool_spell_base: number; pool_spell: number;
  pool_combat_base: number; pool_combat: number;
  pool_control_base: number; pool_control: number;
  pool_astral_base: number; pool_astral: number;
  init_score: number;
  ep_max: number; ep_total: number;
  armor_total_piercing: number; armor_total_slashing: number; armor_total_impact: number;
  power_points_max: number; power_points_used: number; power_points_remaining: number;
  essence_total: number;
  karma_total: number;
  cm_tn_mod: number; cm_init_mod: number;
  sustained_tn_mod: number; tn_warning_level: number;
  skill_total: Record<string, number>;
}

export function computeDerivedFields(
  s: Record<string, unknown>,
  rep: {
    skills: Array<Record<string, unknown>>;
    mutations: Array<Record<string, unknown>>;
    adept_powers: Array<Record<string, unknown>>;
    weapons: Array<Record<string, unknown>>;
    equipment: Array<Record<string, unknown>>;
  }
): DerivedFields {
  const gi = (k: string, fb = 0) => parseInt(String(s[k] ?? fb), 10) || fb;

  // L2 — Attribute totals
  const body = gi('body_base') + gi('body_mutations') + gi('body_magic') + gi('body_misc');
  const dex  = gi('dex_base')  + gi('dex_mutations')  + gi('dex_magic')  + gi('dex_misc');
  const str  = gi('str_base')  + gi('str_mutations')  + gi('str_magic')  + gi('str_misc');
  const cha  = gi('cha_base')  + gi('cha_mutations')  + gi('cha_magic')  + gi('cha_misc');
  const int  = gi('int_base')  + gi('int_mutations')  + gi('int_magic')  + gi('int_misc');
  const wil  = gi('wil_base')  + gi('wil_mutations')  + gi('wil_magic')  + gi('wil_misc');
  const hum  = gi('hum_base')  + gi('hum_mutations')  + gi('hum_magic')  + gi('hum_misc');
  const mag  = gi('mag_base')  + gi('mag_misc');

  // L3 — Reaction
  const reaction_base = Math.floor((int + dex) / 2);
  const reaction      = Math.max(1, reaction_base + gi('reaction_misc'));

  // L4a — Pool bases
  const pool_spell_base   = Math.floor((cha + int + wil) / 2);
  const pool_combat_base  = Math.floor((dex + int + wil) / 2);
  const pool_control_base = reaction;
  const pool_astral_base  = Math.floor((int + wil + mag) / 3);

  // L4b — Pool totals
  const pool_spell   = Math.max(0, pool_spell_base   + gi('pool_spell_misc'));
  const pool_combat  = Math.max(0, pool_combat_base  + gi('pool_combat_misc'));
  const pool_control = Math.max(0, pool_control_base + gi('pool_control_misc'));
  const pool_astral  = Math.max(0, pool_astral_base  + gi('pool_astral_misc'));

  // L4c — Initiative
  const init_score = reaction + gi('init_reaction_mod') + gi('init_misc_mod');

  // L5 — Aggregates
  const ep_max   = Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2);
  const ep_total = rep.weapons.reduce((s, r) => s + (parseFloat(String(r.weapon_ep)) || 0), 0)
                 + rep.equipment.reduce((s, r) => s + (parseFloat(String(r.equip_ep)) || 0), 0);

  const armor_total_piercing = gi('armor_torso_piercing') + gi('armor_legs_piercing') + gi('armor_head_piercing');
  const armor_total_slashing = gi('armor_torso_slashing') + gi('armor_legs_slashing') + gi('armor_head_slashing');
  const armor_total_impact   = gi('armor_torso_impact')   + gi('armor_legs_impact')   + gi('armor_head_impact');

  const power_points_max       = mag;
  const power_points_used      = rep.adept_powers.reduce((s, r) => s + (parseFloat(String(r.power_pp_cost_value)) || 0), 0);
  const power_points_remaining = power_points_max - power_points_used;

  // essence_total = SUM(mutation_essence) = essence SPENT
  // Display remaining: render 6.0 - derived.essence_total at the view layer
  const essence_total = rep.mutations.reduce((s, r) => s + (parseFloat(String(r.mutation_essence)) || 0), 0);

  // L6 — Modifiers
  const karma_total = gi('karma_good') + gi('karma_used');

  const penaltyOf = (lvl: number) => Math.min(lvl, 3);
  const cm_tn_mod   = Math.max(penaltyOf(gi('cm_mental')), penaltyOf(gi('cm_stun')), penaltyOf(gi('cm_physical')));
  const cm_init_mod = -1 * cm_tn_mod;

  const sustained_tn_mod = gi('spells_sustained') * 2;
  const tn_warning_level = sustained_tn_mod >= 6 ? 3 : sustained_tn_mod >= 4 ? 2 : sustained_tn_mod >= 2 ? 1 : 0;

  const skill_total: Record<string, number> = {};
  rep.skills.forEach((row) => {
    skill_total[String(row.id)] = (parseInt(String(row.skill_base)) || 0)
                                + (parseInt(String(row.skill_foci)) || 0)
                                + (parseInt(String(row.skill_misc)) || 0);
  });

  return {
    body, dex, str, cha, int, wil, hum, mag,
    reaction_base, reaction,
    pool_spell_base, pool_spell, pool_combat_base, pool_combat,
    pool_control_base, pool_control, pool_astral_base, pool_astral,
    init_score, ep_max, ep_total,
    armor_total_piercing, armor_total_slashing, armor_total_impact,
    power_points_max, power_points_used, power_points_remaining,
    essence_total, karma_total, cm_tn_mod, cm_init_mod,
    sustained_tn_mod, tn_warning_level, skill_total,
  };
}
```

### Companion App Tab Structure

| Tab | Source | Visibility |
|---|---|---|
| Core | scalars (attrs, CM, pools, init, armor, karma) | Always |
| Skills | repeating.skills | Always |
| Magic | repeating.spells/mutations/adept_powers + magic scalars | Only if `derived.mag > 0` |
| Gear | repeating.weapons/equipment | Always |
| Bio | scalars.bio_q01-q20, char_description, char_notes, repeating.contacts | Always |

`sheet_compact_mode` is Roll20-only — ignored in companion app.

### Sandbox Verification (run BEFORE Sheet Worker sync code)

| ID | Test | Expected |
|---|---|---|
| 5-SV1 | `<button type="action" name="act_btn_sync_db">` fires `on('clicked:btn_sync_db')` WITHOUT triggering dice roll | Handler fires; no roll in chat |
| 5-SV2 | `removeRepeatingRow(rowId)` removes row from DOM without error | Row removed; K-scaffold wrapper confirmed |
| 5-SV3 | `setAttrs({ 'repeating_skills_-NEWTESTID_skill_name': 'Test' })` creates new row | New row created with exact row ID |

### Phase 5 Constraints

- V1 is READ-ONLY companion + outbound-only sync — zero write paths from companion app
- Two separate Turso tokens: proxy write-only token (CF Worker env) vs app read+write token (CF Pages env) — never mix
- `campaign_db_id` bootstrap: GM manually inserts campaign row in Turso + sets value on Roll20 sheet before first sync
- `char_db_id` is write-once from Roll20: empty on first sync -> proxy generates UUID -> Sheet Worker saves -> subsequent syncs use persisted UUID
- `@libsql/client/web` import REQUIRED for CF Workers runtime (not default `@libsql/client` which needs Node.js net/tls)
- Discord callback URL must be registered: `{APP_URL}/auth/callback/discord` (both localhost and production)

**Verification:** 12 Turso tables + 10 indices. Sync payload ~90 included scalar fields. Computed.ts mirrors all 30 cascade formulas. 3 sandbox items (5-SV1 through 5-SV3).

---

## Verification Matrix

| Phase | Verification | Success Criteria |
|---|---|---|
| 1 — Data Architecture | Count all fields in sheet.json attributes array; cross-reference every Phase 3 worker trigger/output | 122 scalar fields, 42 repeating data fields, 7 sections |
| 2 — HTML Structure | Open in Roll20 sandbox; verify all tabs activate, all inputs bind, all buttons appear | 5 tabs render, 18 buttons clickable, compact toggle works, no orphaned inputs |
| 3 — Sheet Workers | Change each base attribute and verify full cascade propagation; test all 18 roll buttons in chat | 30 workers fire in correct order; roll templates render with correct parameters; sync handler POSTs |
| 4 — CSS Design | Visual inspection across all 5 tabs; verify Roll20 iframe compatibility | No `var()` failures; all color tokens render; condition monitor checkboxes styled; compact mode toggling; TN warning ramp activates |
| 5 — Companion App | Create character in Roll20, sync, verify data appears in companion app | Login via Discord; character list shows synced character; full sheet view renders all fields + computed values match Roll20 |

### Sandbox Pre-Implementation Tests (run first)

| ID | Phase | Gate |
|---|---|---|
| D8 | 4 | `appearance:none` on checkboxes -> Phase 2 HTML structure decision |
| D7 | 4 | K-scaffold `.repcontainer` class name |
| D9 | 4 | `attr_tn_warning_level` sibling ordering |
| D10 | 4 | Compact checkbox sibling ordering |
| D6 | 4 | `@media` inside Roll20 iframe |
| 5-SV1 | 5 | Action button fires without dice roll |
| 5-SV2 | 5 | `removeRepeatingRow` works in K-scaffold |
| 5-SV3 | 5 | `setAttrs` creates new repeating row by ID |

---

## Execution Checklist

- [ ] Phase 1: Write sheet.json with 122 scalar attributes (19 groups)
- [ ] Phase 1: Define 7 repeating section HTML fieldsets with all data fields
- [ ] Phase 2: Build document skeleton (script + hidden infra + compact checkbox + tab radios + compact-target wrapper + 5 panels)
- [ ] Phase 2: Implement Core tab (9 regions: header strip, identity, condition monitors, attributes table, initiative, dice pools, karma, armor, combat)
- [ ] Phase 2: Implement Skills tab (repeating_skills + mutations + adept powers with computed badges)
- [ ] Phase 2: Implement Magic tab (summary row + tn_warning hidden input + repeating_spells)
- [ ] Phase 2: Implement Gear tab (EP tracker + repeating_weapons + repeating_equipment + repeating_contacts)
- [ ] Phase 2: Implement Bio tab (textareas + 20 Session 0 question blocks)
- [ ] Phase 2: Place all 9 hidden inputs + 29 readonly inputs + 18 buttons
- [ ] Phase 3: Implement 8 L2 attribute total workers with parseInt guards
- [ ] Phase 3: Implement L3 reaction workers (reaction_base + reaction with Math.max(1) floor)
- [ ] Phase 3: Implement 4 L4a pool base workers + 4 L4b pool total workers
- [ ] Phase 3: Implement L4c init_score worker
- [ ] Phase 3: Implement L5 aggregate workers (EP, armor, skill_total, power points, essence)
- [ ] Phase 3: Implement L6 modifier workers (karma, CM penalties, sustained TN + warning level)
- [ ] Phase 3: Wire 3 roll template HTML blocks
- [ ] Phase 3: Set all 18 roll button formula values (paste from registry)
- [ ] Phase 3: Implement btn_sync_db handler (6-step flow)
- [ ] Phase 3: Implement k.sheetOpens full cascade recalculation
- [ ] Phase 4: Run sandbox tests D6-D10 FIRST
- [ ] Phase 4: Write CSS in 20-section order (global reset -> compact fallback)
- [ ] Phase 4: Verify all 18 color tokens as inline hex (zero var())
- [ ] Phase 5: Deploy Turso schema (12 tables + 10 indices)
- [ ] Phase 5: Bootstrap campaign row + set campaign_db_id on Roll20 sheets
- [ ] Phase 5: Deploy CF Worker proxy with env vars
- [ ] Phase 5: Run sandbox tests 5-SV1 through 5-SV3
- [ ] Phase 5: Scaffold SvelteKit app with Auth.js Discord OAuth
- [ ] Phase 5: Implement Turso client singleton + computed.ts
- [ ] Phase 5: Implement /characters and /characters/[id] routes
- [ ] Phase 5: End-to-end test: Roll20 sync -> CF proxy -> Turso -> companion app display

---

## Cross-Cutting Constraints

### K-scaffold
- Roll20 Pro required for custom sheet upload and Sheet Worker `fetch()` calls
- Beacon SDK NOT available (publisher-gated) — all interaction via K-scaffold + standard Sheet Worker APIs
- Confirm installed K-scaffold version for: `attr_` prefix convention, `registerFuncs` API, repeating section pattern A vs B, `k.sheetOpens` or equivalent, action button `act_` vs `roll_` naming
- `k.registerFuncs` for ALL cascade workers; bare `on()` ONLY for event-driven sync handler

### Roll20
- Sheet Workers are single-script-tag, callback-only sandbox — ZERO external HTTP except `fetch()` on Pro tier
- `getAttrs()` returns ALL values as strings — `parseInt(v,10)||0` for integers, `parseFloat(v||0)` for decimals
- No `var()`, no `:root`, no `@import` in CSS — inline hex values only
- Roll templates defined in `sheet.html`, CSS in same `<style>` block, referenced as `&{template:name}`
- `disabled` inputs cannot be read by `getAttrs()` in some configurations — use `readonly` instead
- Condition monitors use radio groups (shared `name=`), NOT separate boolean checkboxes
- `tn_warning_level` CSS attribute selector requires hidden input as immediate preceding DOM sibling

### OWASP
- A03 (Injection): ALL Turso queries use parameterized `{ sql, args }` — zero string concatenation
- Ownership guard: `WHERE c.id = ? AND c.player_id = ?` on every character read — 404 on mismatch (not 403)
- Turso write token never transmitted to client; lives in CF Worker env vars only
- Auth.js JWT signing secret (AUTH_SECRET) in server env only

### Turso
- SQLite-native types only: INTEGER, TEXT, REAL
- Pipeline API with BEGIN/COMMIT for atomic sync writes — partial write is invalid state
- Full snapshot sync (no delta patches) — DELETE + INSERT per repeating section table per sync
- `sync_version` maintained in V1 for V2 bidirectional readiness
- JSON blob in `character_scalars.data` absorbs schema evolution without ALTER TABLE

### V2 Deferred (do NOT implement)
- `btn_pull_db` + inbound pull handler + `k.sheetOpens` auto-pull guard
- Companion app write paths / character edit forms
- Conflict resolution (sync_version semantics)
- Offline/PWA service worker caching
- GM dashboard routes
- Debounced idle-batch sync trigger
- `/characters/new` companion-side character creation

### Open [DEV DECISION] Items (resolve during implementation)
1. K-scaffold `attr_` prefix convention in sheet.json (bare vs prefixed)
2. K-scaffold action button naming pattern (`act_` vs `roll_`)
3. K-scaffold repeating section wrapper class (`.sheet-repcontainer` vs `.repcontainer`)
4. `k.sheetOpens` built-in recalcAll availability
5. `appearance:none` on checkboxes in Roll20 iframe (D8)
6. `@media` queries inside Roll20 iframe (D6)
7. player_id resolution in first-sync (Discord ID in payload vs manual GM insert)