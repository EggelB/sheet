# Layer 2 — Operational Granularity: Phase 1

## Data Architecture & Roll20 Attribute Naming Contract

**Deliverable:** Naming contract document + `sheet.json` K-scaffold attribute definition file.
**No HTML, CSS, or Sheet Worker logic produced in this phase.**
**Status: FORMULA CONFIRMED ✅ — awaiting Bryce sign-off to produce sheet.json**

---

## ✅ RESOLVED: Dice Pool Formulas (confirmed by Bryce 2026-03-28)

| Pool             | Formula                | Used For                         |
| ---------------- | ---------------------- | -------------------------------- |
| `pool_spell`   | floor((CHA+INT+WIL)/2) | Spell casting, summoning spirits |
| `pool_combat`  | floor((DEX+INT+WIL)/2) | All combat actions               |
| `pool_control` | = REACTION total       | Vehicle & mount control          |
| `pool_astral`  | floor((INT+WIL+MAG)/3) | Astral activities (Phase 5+)     |

---

## Task 1.1 — Naming Convention

- All attribute names: lowercase snake_case
- 8 core attribute abbreviations: `body`, `dex`, `str`, `cha`, `int`, `wil`, `hum`, `mag`
- Sub-field suffixes: `_base` (player-entered), `_mutations`, `_magic`, `_misc`, bare name = total (Sheet Worker computed)
- REACTION exception: `reaction_base` = computed floor((int+dex)/2), `reaction_misc`, `reaction` = total
- MAGIC exception: no `_mutations` or `_magic` sub-fields — just `mag_base`, `mag_misc`, `mag`
- Dice pools: `pool_{name}_base` (computed), `pool_{name}_misc`, `pool_{name}` (total)
- Condition monitors: `cm_{track}` (stores integer damage level)
- Repeating sections: `repeating_{section}`
- Roll buttons: prefix `btn_`, plain snake_case

---

## Task 1.2 — Core Attribute Fields (45 fields)

| Attribute | _base | _mutations | _magic | _misc | total (computed) |
| --------- | ----- | ---------- | ------ | ----- | ---------------- |
| body      | ✓    | ✓         | ✓     | ✓    | ✓               |
| dex       | ✓    | ✓         | ✓     | ✓    | ✓               |
| str       | ✓    | ✓         | ✓     | ✓    | ✓               |
| cha       | ✓    | ✓         | ✓     | ✓    | ✓               |
| int       | ✓    | ✓         | ✓     | ✓    | ✓               |
| wil       | ✓    | ✓         | ✓     | ✓    | ✓               |
| hum       | ✓    | ✓         | ✓     | ✓    | ✓               |
| mag       | ✓    | —         | —     | ✓    | ✓               |

Total per attribute = base + mutations + magic + misc (Sheet Worker computed).

**Reaction (derived):**

- `reaction_base` = Sheet Worker: floor((int + dex) / 2)
- `reaction_misc` — manual modifier
- `reaction` — total: reaction_base + reaction_misc

---

## Task 1.3 — Dice Pool Fields (12 fields)

| Pool                  | _base formula                | _misc                 | total            |
| --------------------- | ---------------------------- | --------------------- | ---------------- |
| `pool_spell_base`   | floor((cha + int + wil) / 2) | `pool_spell_misc`   | `pool_spell`   |
| `pool_combat_base`  | floor((dex + int + wil) / 2) | `pool_combat_misc`  | `pool_combat`  |
| `pool_control_base` | =`reaction` total          | `pool_control_misc` | `pool_control` |
| `pool_astral_base`  | floor((int + wil + mag) / 3) | `pool_astral_misc`  | `pool_astral`  |

---

## Task 1.4 — Initiative Fields (4 fields)

| Field                 | Purpose                                                    | Computed? |
| --------------------- | ---------------------------------------------------------- | --------- |
| `init_dice`         | Number of d6s to roll (default 1; mutations may increase)  | No        |
| `init_reaction_mod` | Reaction modifier to add to initiative                     | No        |
| `init_misc_mod`     | Miscellaneous Initiative modifier                          | No        |
| `init_score`        | Sheet Worker: reaction + init_reaction_mod + init_misc_mod | Yes       |

**Roll formula:** `@{init_dice}d6 + @{init_score}`

---

## Task 1.5 — Condition Monitor Fields (6 fields)

| Field                    | Type    | Values                                                           |
| ------------------------ | ------- | ---------------------------------------------------------------- |
| `cm_mental`            | integer | 0=clean, 1=Light, 2=Moderate, 3=Serious, 4=Deadly                |
| `cm_stun`              | integer | 0=clean, 1=L, 2=M, 3=S, 4=D, 5=Unconscious                       |
| `cm_physical`          | integer | 0=clean, 1=L, 2=M, 3=S, 4=D, 5=Unconscious                       |
| `cm_physical_overflow` | integer | Overflow damage boxes beyond Deadly                              |
| `cm_tn_mod`            | integer | Computed: max TN penalty across all active tracks (+0/+1/+2/+3)  |
| `cm_init_mod`          | integer | Computed: max Init penalty across all active tracks (0/-1/-2/-3) |

Penalty tiers: Light=+1TN/-1Init, Moderate=+2TN/-2Init, Serious=+3TN/-3Init, Deadly=incapacitated.

---

## Task 1.6 — Character Info and Karma Fields (10 fields)

**Character Identity:** `char_name`, `char_race_station`, `char_sex`, `char_age`, `char_description`, `char_notes`

**Karma:** `karma_good`, `karma_used`, `karma_total` (computed: good + used), `karma_pool`

**Encumbrance:**

- `ep_total` — Sheet Worker: sum of repeating_weapons + repeating_equipment EP values
- `ep_max` — Sheet Worker: max(str, body) × 4 + floor(min(str, body) / 2)

---

## Task 1.7 — Armor Fields (Fixed-Location Model, 15 + 3 computed = 18 fields)

**Per location × 4 fields:** `armor_{torso|legs|head}_{name|piercing|slashing|impact}`
**Computed totals:** `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact`

---

## Task 1.8 — repeating_ Section Schemas

### repeating_skills (9 fields per row)

`skill_name`, `skill_linked_attr`, `skill_general`, `skill_spec`, `skill_base`, `skill_foci`, `skill_misc`, `skill_total` (computed), `btn_skill_roll`

### repeating_spells (8 fields per row)

`spell_name`, `spell_type`, `spell_duration`, `spell_target`, `spell_force`, `spell_drain`, `btn_cast_spell`, `btn_drain_resist`

### repeating_mutations (5 fields per row)

`mutation_name`, `mutation_level`, `mutation_essence`, `mutation_bp_cost`, `mutation_effect`

### repeating_adept_powers (6 fields per row)

`power_name`, `power_level`, `power_pp_cost` (text display — human-readable cost string, e.g. "0.25/level"), `power_pp_cost_value` (number — numeric cost for Sheet Worker sum), `power_effect`

+ Sheet-level: `power_points_max` (= mag), `power_points_used` (computed sum of all `power_pp_cost_value`), `power_points_remaining` (computed)

### repeating_weapons (14 fields per row)

`weapon_name`, `weapon_type`, `weapon_modifiers`, `weapon_power`, `weapon_damage`, `weapon_conceal`, `weapon_reach`, `weapon_ep`, `weapon_range_short`, `weapon_range_medium`, `weapon_range_long`, `weapon_range_extreme`, `btn_attack_ranged`, `btn_attack_melee`

### repeating_equipment (3 fields per row)

`equip_name`, `equip_description`, `equip_ep`

### repeating_contacts (3 fields per row)

`contact_name`, `contact_info`, `contact_level`

---

## Task 1.9 — K-scaffold sheet.json Attribute Definition File

Steps:

1. Map all fields from Tasks 1.1–1.8 to K-scaffold attribute syntax
2. Integers → 0; strings → ""; computed fields → worker_only: true
3. Tag all Sheet Worker computed fields
4. Validate against K-scaffold docs
5. Commit `sheet.json` as sole code artifact of Phase 1

**Computed fields (worker_only: true):**
All 8 attribute totals + reaction + reaction_base, all 4 pool_*_base + pool_* totals, init_score, cm_tn_mod, cm_init_mod, karma_total, ep_total, ep_max, all armor_total_*, skill_total, power_points_max/used/remaining

---

## Task 1.10 — Roll Button Reference Table

| Button                     | Location          | Test dice                          | Default TN      |
| -------------------------- | ----------------- | ---------------------------------- | --------------- |
| `btn_init_roll`          | Sheet header      | @{init_dice}d6 + @{init_score}     | —              |
| `btn_skill_roll`         | repeating_skills  | @{skill_total}                     | ?{TN} prompt    |
| `btn_attack_ranged`      | repeating_weapons | Skill total + ?{Pool dice}         | Range table     |
| `btn_attack_melee`       | repeating_weapons | Skill total + ?{Pool dice}         | 4 (base)        |
| `btn_cast_spell`         | repeating_spells  | Sorcery skill + ?{Spell Pool dice} | TN + mods       |
| `btn_drain_resist`       | repeating_spells  | @{wil} + ?{remaining Spell Pool}   | Force/2 + drain |
| `btn_dodge`              | Combat panel      | ?{Combat Pool dice}                | 4               |
| `btn_damage_resist_body` | Combat panel      | @{body} + ?{Combat Pool dice}      | Power - armor   |

---

## Phase 1 Deliverables

1. ✅ Naming contract (this document)
2. ✅ Formula confirmed (Spell = (CHA+INT+WIL)/2 for casting/summoning)
3. ⬜ Bryce sign-off → produce `sheet.json`

## Phase 1 Success Criteria

- [X] Spell pool formula confirmed
- [ ] Naming contract reviewed and approved by Bryce
- [ ] `sheet.json` passes K-scaffold syntax validation
- [ ] Zero Sheet Worker computation logic implemented in HTML

---

*Character Creation reference (Priority System):*

| Priority | Station                          | Magic         | Attributes  | Skills | Resources |
| -------- | -------------------------------- | ------------- | ----------- | ------ | --------- |
| A        | Nobility/Merchant (+5 pts)       | Full Magician | 20 (cap 10) | 33     | 5000gp    |
| B        | Shop owner/Professional (+4 pts) | Adept         | 18 (cap 9)  | 27     | 2000gp    |
| C        | Military/Freeman (+3 pts)        | —            | 16 (cap 8)  | 23     | 450gp     |
| D        | Serf/Peasant (+2 pts)            | —            | 14 (cap 7)  | 20     | 100gp     |
| E        | Beggar/Pauper (+1 pt)            | —            | 12 (cap 6)  | 18     | 25gp      |

Starting pools: Knowledge Skills = INT×5pts; Language Skills = INT pts; Spells = 17pts (125 RP for additional).

---

# Layer 2 — Operational Granularity: Phase 2

## HTML Structure & Tab Layout

**Input:** Layer 2 Phase 1 naming contract (approved 2026-03-28)
**Output:** Annotated HTML skeleton — semantic structure, all attributes wired, zero CSS/Sheet Worker logic. One file: `sheet.html`
**Gate:** Bryce review + sign-off before Phase 3

---

## Phase 1 Amendment — Attribute Roll Buttons (9 new fields added to sheet.json)

From Bryce sign-off: attributes must be directly rollable (e.g. Perception = roll INT vs TN).

| Button                | Location            | Roll          | Default TN      |
| --------------------- | ------------------- | ------------- | --------------- |
| `btn_roll_body`     | Tab 1, BODY row     | @{body}d6     | ?{TN\|4} prompt |
| `btn_roll_dex`      | Tab 1, DEX row      | @{dex}d6      | ?{TN\|4}        |
| `btn_roll_str`      | Tab 1, STR row      | @{str}d6      | ?{TN\|4}        |
| `btn_roll_cha`      | Tab 1, CHA row      | @{cha}d6      | ?{TN\|4}        |
| `btn_roll_int`      | Tab 1, INT row      | @{int}d6      | ?{TN\|4}        |
| `btn_roll_wil`      | Tab 1, WIL row      | @{wil}d6      | ?{TN\|4}        |
| `btn_roll_hum`      | Tab 1, HUM row      | @{hum}d6      | ?{TN\|4}        |
| `btn_roll_mag`      | Tab 1, MAG row      | @{mag}d6      | ?{TN\|4}        |
| `btn_roll_reaction` | Tab 1, REACTION row | @{reaction}d6 | ?{TN\|4}        |

Example use: Perception test → click btn_roll_int → enter TN → count successes (dice result ≥ TN).
Success threshold (die result ≥ TN) is a Phase 3 roll template decision; Phase 2 stubs only.

---

## New Fields Added (Phase 2 discoveries)

These fields were not in Phase 1 but are required by the HTML structure:

| Field                    | Type            | Purpose                                                   | Tab    |
| ------------------------ | --------------- | --------------------------------------------------------- | ------ |
| `essence_total`        | computed        | Sum of all mutation_essence values                        | Skills |
| `spells_sustained`     | integer (0–10) | Player-tracked sustained spell count; drives +2TN display | Magic  |
| `sustained_tn_mod`     | computed        | = spells_sustained × 2                                   | Magic  |
| `bio_q01`–`bio_q20` | text            | Session 0 roleplay questions                              | Bio    |

---

## Task 2.1 — Tab Architecture

5 tabs. Roll20 implementation: radio-button/label pattern (`<input type="radio">` + `<label>` controlling `<div>` visibility via CSS sibling selector — standard Roll20 pattern).

| Tab slug       | Display Label | Primary Content                                                                       |
| -------------- | ------------- | ------------------------------------------------------------------------------------- |
| `tab-core`   | Core          | Identity · Attributes · Condition Monitors · Pools · Initiative · Karma · Armor |
| `tab-skills` | Skills        | Skill list · Mutations · Adept Powers                                               |
| `tab-magic`  | Magic         | Spell list · Sustained tracker · Spell pool reference                               |
| `tab-gear`   | Gear          | Weapons · Equipment · Contacts · EP tracker                                        |
| `tab-bio`    | Bio           | Description · Notes · Session 0 questions                                           |

Default active tab: `tab-core`.

---

## Task 2.2 — Tab: Core (layout, top → bottom)

1. **Identity Row** — char_name (wide), char_race_station, char_sex, char_age — single inline row
2. **Condition Monitors Region** — 3 tracks side-by-side:

   - Each track: label (Mental / Stun / Physical) + 4 tier columns (Light / Moderate / Serious / Deadly)
   - Each tier cell: TN modifier label (+1/+2/+3 TN) + Initiative penalty label (-1/-2/-3 Init) + checkbox
   - Stun + Physical only: 5th column "Uncon" checkbox
   - Physical only: Overflow input field below track
   - cm_tn_mod and cm_init_mod display fields (computed totals, read-only, shown in header)
3. **Attributes Region** — table layout:

   - Header row: Name | Base | Mutations | Magic | Misc | **Total** | **[Roll]**
   - 8 attribute rows (body → hum): Base input | Mutations input | Magic input | Misc input | Total (read-only computed) | Roll button
   - Reaction row: label "(INT+DEX)/2" | read-only Base | — | — | Misc input | Total (read-only) | Roll button
   - Magic row: Base input | — | — | Misc input | Total (read-only) | Roll button
4. **Initiative Row** — "#d6" input (init_dice) | "Reaction Mod" input | "Misc" input | Score (read-only, init_score) | [Roll Initiative] button (btn_init_roll) — all inline
5. **Dice Pools Region** — 4-row table:

   - Columns: Pool Name | Formula (static label) | Base (read-only computed) | Misc input | Total (read-only)
   - Rows: Spell "(CHA+INT+WIL)/2" | Combat "(DEX+INT+WIL)/2" | Control "REACTION" | Astral "(INT+WIL+MAG)/3"
   - No roll buttons on pools (dice spent during actions, not rolled as a pool directly)
6. **Karma Row** — Good Karma input | Used Karma input | Total (read-only) | Pool input — inline
7. **Armor Region** — 3-column table (Torso · Legs · Head):

   - Each column: Name text input + Piercing / Slashing / Impact number inputs
   - Totals row at bottom: armor_total_piercing / armor_total_slashing / armor_total_impact (read-only computed)
8. **Combat Panel** — positioned below the Armor Region:

   - `btn_dodge` button — label "Dodge" (Roll: `?{Combat Pool dice for dodge|0}d6cs>=4 cf<=1`)
   - `btn_damage_resist_body` button — label "Resist Damage (Body)" (Roll: `(@{body} + ?{Combat Pool dice|0})d6cs>=?{TN (Power-Armor)|0} cf<=1`)
   - Both are static sheet-level buttons — not inside any repeating section

---

## Task 2.3 — Tab: Skills (layout, top → bottom)

1. **Skills Section**

   - Header: column labels — Name | Linked Attr | Category | Spec | Base | Foci | Misc | Total | [Roll]
   - `<fieldset data-groupname="repeating_skills">` — K-scaffold repeating section
   - Each row: skill_name text | skill_linked_attr select (body/dex/str/cha/int/wil/hum/mag/reaction) | skill_general text | skill_spec text | skill_base number | skill_foci number | skill_misc number | skill_total (read-only) | btn_skill_roll button
   - K-scaffold add/remove row controls
2. **Mutations Section**

   - Header: "Mutations" label + Essence Used: `essence_total` (read-only computed) display
   - `<fieldset data-groupname="repeating_mutations">`
   - Each row: mutation_name text | mutation_level number | mutation_essence number | mutation_bp_cost number | mutation_effect text (wider)
3. **Adept Powers Section**

   - Header: "Adept Powers" label + "PP: `power_points_used` / `power_points_max` remaining: `power_points_remaining`" display
   - `<fieldset data-groupname="repeating_adept_powers">`
   - Each row: power_name text | power_level number | power_pp_cost text (display) | power_pp_cost_value number (small numeric input — feeds PP sum worker) | power_effect text (wider)

---

## Task 2.4 — Tab: Magic (layout, top → bottom)

1. **Magic Summary Row** — Magic rating display (read-only `mag`) | Spell Pool display (read-only `pool_spell`) | Sustained: [spells_sustained number input] spells → [sustained_tn_mod read-only] TN modifier active
2. **Spells Section**

   - Header: "Spells" label
   - Column labels: Name | Type (M/P) | Duration (I/S/P) | Target | Force | Drain | [Cast] | [Drain]
   - `<fieldset data-groupname="repeating_spells">`
   - Each row: spell_name text | spell_type select (M/P) | spell_duration select (I/S/P) | spell_target text | spell_force number | spell_drain text | btn_cast_spell button | btn_drain_resist button
3. **Casting Reference** — static collapsed reference text:

   - "+2 TN per sustained spell (currently: sustained_tn_mod)"
   - "Spell resistance: target rolls WIL/BOD/INT vs Force"
   - "Drain test: WIL + remaining Spell Pool vs Force/2 + drain modifier"

---

## Task 2.5 — Tab: Gear (layout, top → bottom)

1. **EP Tracker Row** — EP Used: `ep_total` (read-only computed) | EP Max: `ep_max` (read-only computed) | formula hint "max(STR,BOD)×4 + ½min(STR,BOD)" — inline
2. **Weapons Section**

   - Header: column labels — Name | Type | Mods | Power | Dmg | Conceal | Reach | EP | Short | Med | Long | Ext | [Rng] | [Mel]
   - `<fieldset data-groupname="repeating_weapons">`
   - Each row: weapon_name | weapon_type select (Edged/Club/Polearm/Unarmed/Projectile/Thrown) | weapon_modifiers text | weapon_power number | weapon_damage text | weapon_conceal number | weapon_reach number | weapon_ep number | weapon_range_short text | weapon_range_medium text | weapon_range_long text | weapon_range_extreme text | btn_attack_ranged | btn_attack_melee
3. **Equipment Section**

   - Header: column labels — Name | Description | EP
   - `<fieldset data-groupname="repeating_equipment">`
   - Each row: equip_name | equip_description | equip_ep number
4. **Contacts Section**

   - Header: column labels — Name | Info | Level
   - `<fieldset data-groupname="repeating_contacts">`
   - Each row: contact_name | contact_info | contact_level select (1-Contact / 2-Buddy / 3-Friend)
   - Level 2 note: "+1 Etiquette die"; Level 3 note: "+2 Etiquette die"

---

## Task 2.6 — Tab: Bio (layout, top → bottom)

1. **Description** — label + char_description `<textarea>` (large, ~6 rows)
2. **Notes** — label + char_notes `<textarea>` (large, ~6 rows)
3. **Session 0 Questions** — 20 question blocks, each: static read-only label (question text) + bio_q01…bio_q20 `<textarea>` (~3 rows each)

Questions (pre-populated labels from Character Creation.xlsx):
Q1 Who is your biggest rival and why? Q2 Who/what do you despise? Q3 Who looks up to you and why? Q4 Most prized possession? Q5 How have you gained success or suffered failure? Q6 What drives you? Q7 Closest friends? Q8 Who trained you and in what? Q9 Close to family? Q10 Family relationship state? Q11 Current love interest? Q12 In a relationship? Q13 Greatest love? Q14 Bathing habits? Q15 Have you killed anyone? Q16 Jailed/imprisoned? Q17 How do you look and dress? Q18 Noticeable mannerisms? Q19 Greatest virtues? Q20 Greatest flaws?

---

## Task 2.7 — Attribute Roll Button Placement

- Position: rightmost column of each row in the Attributes Region (Tab: Core)
- One `<button type="roll">` per attribute row + reaction row = 9 buttons
- Button label: die icon or abbreviated attribute name
- Roll formula stub (Phase 2): `attribute_name_placeholder` — final formulas wired in Phase 3

---

## Task 2.8 — Conditional Visibility Strategy

**Decision: No Sheet Worker conditional show/hide.**

- Magic fields always present; zero-magic characters simply have mag=0 and empty repeating_spells
- Adept Powers section always present; non-adepts leave it empty
- Simplifies Sheet Worker scope and avoids attribute-watching overhead
- Exception if Bryce requests it during Phase 3 review

---

## Task 2.9 — HTML Skeleton Deliverable: `sheet.html`

Structure requirements:

- `<script type="text/worker">` placeholder tag (K-scaffold hook — content empty until Phase 3)
- 5 tab radio/label navigation pattern
- All `<input>` elements: `name="attr_{attribute_name}"` per Phase 1 contract
- All `<button type="roll">` stubs: `name="roll_placeholder"` value `placeholder` (formulas Phase 3)
- All `<fieldset data-groupname="repeating_{section}">` containers with inner template div
- `<select>` elements for skill_linked_attr, spell_type, spell_duration, weapon_type, contact_level
- No `<style>` blocks; no `onclick`; no inline styles; no JavaScript

File: workspace root `sheet.html`

---

## Phase 2 Deliverables

1. ⬜ `sheet.html` — HTML skeleton (Task 2.9), including:
   - 9 attribute roll button stubs in Attributes Region (HTML `<button type="roll">` elements only — roll buttons have no sheet.json schema entry in K-scaffold)
   - `btn_dodge` and `btn_damage_resist_body` stubs in Combat Panel (Task 2.2 item 8)
2. ⬜ Updated `sheet.json` — add 5 new fields discovered in Phase 2/3 planning:
   - `essence_total` (computed), `spells_sustained` (integer, default 0), `sustained_tn_mod` (computed)
   - `bio_q01`–`bio_q20` (text strings, default "")
   - `power_pp_cost_value` (number, default 0) in repeating_adept_powers

## Phase 2 Success Criteria

- [ ] All Phase 1 attribute names wired as `name="attr_{name}"` inputs in sheet.html
- [ ] 5-tab navigation structure renders (structural test)
- [ ] All 7 repeating sections have `data-groupname` containers
- [ ] All roll buttons stubbed with `type="roll"` (formulas = placeholder text)
- [ ] K-scaffold worker script tag present
- [ ] Zero inline styles, zero `<style>` blocks, zero JS in HTML
- [ ] sheet.json updated with 5 new fields (essence_total, spells_sustained, sustained_tn_mod, bio_q01–q20, power_pp_cost_value)
- [ ] Combat Panel present in Tab: Core with btn_dodge and btn_damage_resist_body stubs

---

# Layer 2 — Operational Granularity: Phase 3

## Sheet Workers & Roll Templates

**Input:** Phase 1 naming contract + Phase 2 HTML skeleton
**Output:** Complete Sheet Worker specification (no production code — task-level roadmap with exact formulas, watch patterns, and roll template schemas)
**Gate:** Bryce review + sign-off before Phase 4

---

## Task 3.1 — K-scaffold Worker Initialization

> **Layer boundary note:** Tasks 3.2–3.13 include concrete JS method calls (`Math.floor`, `k.cascadeUpdate`, etc.) as part of the formula specifications. This is an intentional Layer 2/3 boundary blur — for Sheet Workers, the runtime method *is* the formula definition. Layer 3 Technical Blueprints should reference these specs directly rather than re-specifying the same logic.

**Steps:**

1. Import K-scaffold via CDN or local copy into `sheet.html` worker script tag
2. Define `k.version` registration block (required by K-scaffold)
3. Register all `worker_only` attributes in `sheet.json` with `defaultValue: 0`
4. Confirm K-scaffold event routing: `k.registerFuncs({...})` pattern used throughout
5. Add `k.sheetOpens` handler → triggers all computed field recalculations on sheet open

**K-scaffold watcher pattern (used for all computed fields):**

```
k.cascadeUpdate([list of trigger attributes], function(attrs) {
  attrs.computed_field = formula;
});
```

---

## Task 3.2 — Core Attribute Totals (8 workers)

**Trigger pattern per attribute:** watch `{attr}_base`, `{attr}_mutations`, `{attr}_magic`, `{attr}_misc`
**Formula:** `total = (base + mutations + magic + misc)` (integer, no rounding)
**Output field:** bare attribute name (e.g., `body`)

**8 workers:** body, dex, str, cha, int, wil, hum, mag

**mag worker exception:** watch only `mag_base`, `mag_misc` (no mutations/magic sub-fields)

---

## Task 3.3 — Reaction Worker (derived attribute)

**Trigger:** `int`, `dex`, `reaction_misc` (fires after attribute total workers resolve)
**Formula:**

```
reaction_base = Math.floor((int + dex) / 2)
reaction = reaction_base + reaction_misc
```

**Note:** reaction_base is also a worker_only field (no user input for it).
**Dependency order:** Reaction MUST fire AFTER int and dex totals are computed.
K-scaffold cascade handles this via registered dependency order.
**Floor behavior:** `reaction` is the source value for `pool_control_base` and `@{reaction}d6` roll buttons. Apply `Math.max(1, reaction)` as a floor in the reaction worker output to prevent Roll20 `0d6` errors if int+dex totals to zero.

---

## Task 3.4 — Dice Pool Workers (4 workers)

**Trigger/Formula table:**

| Pool                  | Trigger Attributes        | Formula                               |
| --------------------- | ------------------------- | ------------------------------------- |
| `pool_spell_base`   | `cha`, `int`, `wil` | `Math.floor((cha + int + wil) / 2)` |
| `pool_combat_base`  | `dex`, `int`, `wil` | `Math.floor((dex + int + wil) / 2)` |
| `pool_control_base` | `reaction`              | `reaction` (direct copy)            |
| `pool_astral_base`  | `int`, `wil`, `mag` | `Math.floor((int + wil + mag) / 3)` |

**Pool total workers (4 additional):**

| Pool Total       | Trigger                                      | Formula         |
| ---------------- | -------------------------------------------- | --------------- |
| `pool_spell`   | `pool_spell_base`, `pool_spell_misc`     | `base + misc` |
| `pool_combat`  | `pool_combat_base`, `pool_combat_misc`   | `base + misc` |
| `pool_control` | `pool_control_base`, `pool_control_misc` | `base + misc` |
| `pool_astral`  | `pool_astral_base`, `pool_astral_misc`   | `base + misc` |

**Dependency order:** Pool base workers fire AFTER all attribute total workers AND after reaction worker.
**Floor behavior:** All four pool base values apply `Math.max(0, computed)`. Pool totals (base + misc) apply `Math.max(0, total)`. A pool of 0 is valid (player has no dice to spend); a negative total should not propagate. Roll20 `0d6` is technically valid but produces no dice — acceptable for a depleted pool.

---

## Task 3.5 — Initiative Worker

**Trigger:** `reaction`, `init_reaction_mod`, `init_misc_mod`
**Formula:** `init_score = reaction + init_reaction_mod + init_misc_mod`
**Dependency order:** Fires after reaction worker.

---

## Task 3.6 — Condition Monitor Workers (2 computed fields)

**Purpose:** `cm_tn_mod` and `cm_init_mod` show the worst active penalty from any track.

**Penalty value mapping** (used by both workers):

```
0 = clean (no penalty)
1 = Light   → +1 TN / -1 Init
2 = Moderate → +2 TN / -2 Init
3 = Serious  → +3 TN / -3 Init
4+ = Deadly  → treat as 3 (incapacitated is a narrative state, not an additional modifier)
```

**cm_tn_mod trigger:** `cm_mental`, `cm_stun`, `cm_physical`
**cm_tn_mod formula:**

```
penaltyOf = (level) => Math.min(level, 3)
cm_tn_mod = Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))
```

**cm_init_mod trigger:** same fields
**cm_init_mod formula:**

```
cm_init_mod = -1 * Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))
```

**Note:** Both workers can share one event handler since they fire on the same triggers.

---

## Task 3.7 — Karma Total Worker

**Trigger:** `karma_good`, `karma_used`
**Formula:** `karma_total = karma_good + karma_used`
Simple sum — no flooring needed.

---

## Task 3.8 — Encumbrance Workers (2 fields)

**ep_max trigger:** `str`, `body`
**ep_max formula:**

```
ep_max = Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)
```

**ep_total trigger:** repeating_weapons:weapon_ep + repeating_equipment:equip_ep (all rows)
**ep_total formula:** Sum all `weapon_ep` values across repeating_weapons + all `equip_ep` across repeating_equipment.
**K-scaffold pattern:** Use `k.getAllAttrs` or `k.getAttrs` with repeating section iteration.

---

## Task 3.9 — Armor Total Workers (3 fields)

**Trigger:** Any change to `armor_{torso|legs|head}_{piercing|slashing|impact}`
**Formulas:**

```
armor_total_piercing = armor_torso_piercing + armor_legs_piercing + armor_head_piercing
armor_total_slashing = armor_torso_slashing + armor_legs_slashing + armor_head_slashing
armor_total_impact   = armor_torso_impact   + armor_legs_impact   + armor_head_impact
```

---

## Task 3.10 — Skill Total Worker (repeating)

**Trigger:** Any change to `skill_base`, `skill_foci`, `skill_misc` in any repeating_skills row
**Formula:** `skill_total = skill_base + skill_foci + skill_misc`
**K-scaffold pattern:** Register within repeating section update handler.
**Defaulting rule note (comment in code, not logic):** If total = 0, rolls use linked attribute at +4 TN — this is a roll-time player responsibility, not sheet-enforced.

---

## Task 3.11 — Adept Powers Workers (3 computed fields)

**power_points_max trigger:** `mag`
**power_points_max formula:** `power_points_max = mag`

**power_points_used trigger:** Any change to `power_pp_cost_value` in any repeating_adept_powers row
**power_points_used formula:** Sum all `power_pp_cost_value` (numeric field) values across all repeating_adept_powers rows using `parseFloat`. The display field `power_pp_cost` (text) has no worker watching it — it is player-reference only and must NOT be used as the trigger or sum source. **`power_pp_cost_value` is already added to the repeating_adept_powers schema in Task 1.8 (Phase 3 amendment, confirmed).**

**power_points_remaining trigger:** `power_points_max`, `power_points_used`
**formula:** `power_points_remaining = power_points_max - power_points_used`

---

## Task 3.12 — Essence Total Worker

**Trigger:** Any change to `mutation_essence` in any repeating_mutations row
**Formula:** Sum all `mutation_essence` values across all repeating_mutations rows (decimal arithmetic).
**Note:** Essence costs are decimals (e.g., 0.2, 1.15). Use `parseFloat` not `parseInt`.

---

## Task 3.13 — Sustained Spell TN Worker

**Trigger:** `spells_sustained`
**Formula:** `sustained_tn_mod = spells_sustained * 2`
Simple — no flooring (multiples of 2 always integer).

---

## Task 3.14 — Roll Templates (3 templates)

Roll20 roll templates are HTML snippets defined in `sheet.html` inside `<rolltemplate>` tags.

### Template 1: `rolltemplate-skill`

**Used by:** btn_skill_roll (repeating_skills), btn_roll_{attr} (attribute rolls)
**Fields:**

- `charname` — auto from Roll20
- `rollname` — label passed from button (skill name or attribute name)
- `linked_attr` — reference label for the roll
- `tn` — target number used
- `successes` — inline roll `[[Nd6cs>=TN cf<=1]]`; result = success count; ones rendered red
- `{{^successes}}` — warning block shown when hits = 0

*(See Phase 3 Amendment for complete revised field specification)*

### Template 2: `rolltemplate-attack`

**Used by:** btn_attack_ranged, btn_attack_melee
**Fields:**

- `charname`, `rollname`, `weapon_name`
- `tn`, `successes` — inline roll with `cs>=TN cf<=1`
- `damage_code` — weapon damage string (e.g., "4M", "(STR)L") displayed for GM reference
- `power` — weapon Power value
- `reach` — reach value (melee only; empty string for ranged)
- `range_band` — range band (ranged only; empty string for melee)
- `{{^successes}}` — warning block

*(See Phase 3 Amendment for complete revised field specification)*

### Template 3: `rolltemplate-spell`

**Used by:** btn_cast_spell, btn_drain_resist
**Fields:**

- `charname`, `rollname`, `spell_name`
- `spell_type` — M or P
- `spell_duration` — I, S, or P
- `force` — Force used
- `tn`, `successes` — inline roll with `cs>=TN cf<=1`
- `drain_code` — drain string for GM reference (shown on drain resist roll)
- `sustained_penalty` — sustained_tn_mod value at time of roll (informational)
- `{{^successes}}` — warning block

*(See Phase 3 Amendment for complete revised field specification)*

---

## Task 3.15 — Roll Button Final Formulas

All `type="roll"` buttons from Phase 2 stubs get their production `value` attributes here.

### Attribute Roll Buttons (9 buttons)

```
value="&{template:skill} {{rollname=Body}} {{tn=?{Target Number|4}}} {{successes=[[@{body}d6cs>=?{Target Number|4} cf<=1]]}}"
```

Same pattern for all 9: dex, str, cha, int, wil, hum, mag, reaction.
**TN:** `?{Target Number|4}` — player queried at roll time, default 4.
**Success counting:** Roll20 `cs>=TN cf<=1` built into the single inline roll expression — no separate `{{dice_rolled=...}}` parameter. Omitting `dice_rolled` prevents a ghost inline roll appearing in chat outside the template.

### Initiative Roll Button

```
value="/roll @{init_dice}d6 + @{init_score}  &{template:skill} {{rollname=Initiative}} {{result=[[...]]}}"
```

Initiative is a sum roll, not a success-counting roll — result displayed directly.

### Skill Roll Button (repeating_skills)

```
value="&{template:skill} {{rollname=@{skill_name}}} {{linked=@{skill_linked_attr}}} {{successes=[[@{skill_total}d6cs>=?{Target Number|4}]]}} {{tn=?{Target Number|4}}}"
```

Pool dice: second ask-query `?{Pool dice to add|0}` for player to commit Combat/Spell Pool dice.
Full formula: `[[ (@{skill_total} + ?{Pool dice to add|0})d6cs>=?{Target Number|4} ]]`

### Ranged Attack Roll Button

```
Full formula: [[ (@{skill_total_of_weapon_skill} + ?{Combat Pool dice|0})d6cs>=?{Range TN|4} ]]
&{template:attack} {{rollname=Ranged Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{range_band=?{Range Band|Short}}} {{successes=...}}
```

**Note:** weapon skill total is not stored per weapon row — player selects dice via `?{Skill dice|0}` first query. Two queries at roll time: skill dice, range TN.

### Melee Attack Roll Button

```
Two queries: ?{Skill dice|0}, ?{TN|4}
[[ (?{Skill dice|0} + ?{Combat Pool dice|0})d6cs>=?{TN|4} ]]
&{template:attack} {{rollname=Melee Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{reach=@{weapon_reach}}}
```

### Cast Spell Button

```
Queries: ?{Sorcery dice|0}, ?{Spell Pool dice|0}, ?{Target Number|@{sustained_tn_mod}+4}
[[ (?{Sorcery dice|0} + ?{Spell Pool dice|0})d6cs>=?{Target Number|...} ]]
&{template:spell} {{rollname=Cast Spell}} {{spell_name=@{spell_name}}} {{spell_type=@{spell_type}}} {{duration=@{spell_duration}}} {{force=@{spell_force}}} {{drain_code=@{spell_drain}}} {{sustained_penalty=@{sustained_tn_mod}}}
```

**TN default:** pre-fills `?{Target Number|4}` — GM applies sustained modifier separately or player factors in manually. A display reminder on the tab shows "Active TN modifier: +@{sustained_tn_mod}".

### Drain Resist Button

```
Queries: ?{Remaining Spell Pool dice|0}
[[ (@{wil} + ?{Remaining Spell Pool dice|0})d6cs>=?{Drain TN|auto} ]]
```

Drain TN = Force/2 + drain modifier. Since drain modifier is a string (not a number), player reads the drain code and enters TN manually. Two queries: remaining pool dice + drain TN.

### Dodge Button (Combat panel, static, not in repeating)

```
[[ ?{Combat Pool dice for dodge|0}d6cs>=4 ]]
&{template:skill} {{rollname=Dodge}} {{tn=4}} {{successes=...}}
```

### Damage Resist (Body) Button

```
Queries: ?{Power of attack|0}, ?{Combat Pool dice|0}
TN = Power - armor (player calculates and enters)
[[ (@{body} + ?{Combat Pool dice|0})d6cs>=?{TN (Power-Armor)|0} ]]
```

---

## Task 3.16 — Worker Sequencing & Dependency Map

Computation must resolve in this order (Sheet Worker cascade):

```
Layer 1 (raw inputs): all _base, _mutations, _magic, _misc fields
Layer 2 (attribute totals): body, dex, str, cha, int, wil, hum, mag  ← Task 3.2
Layer 3 (derived from attrs): reaction_base, reaction               ← Task 3.3
Layer 4 (pools + init):
  pool_spell_base, pool_combat_base, pool_control_base, pool_astral_base  ← Task 3.4
  pool_spell, pool_combat, pool_control, pool_astral (+ misc)             ← Task 3.4
  init_score                                                               ← Task 3.5
Layer 5 (aggregates): ep_total, ep_max, armor totals, skill_total, power_points_*, essence_total  ← Tasks 3.8–3.13
Layer 6 (modifiers): cm_tn_mod, cm_init_mod, sustained_tn_mod, karma_total  ← Tasks 3.6, 3.7, 3.13
```

K-scaffold handles sequencing via its cascade mechanism if dependencies are declared correctly.
**Implementation note:** Use `k.registerFuncs` with explicit dependency arrays, not bare `on()` calls.

---

## Task 3.17 — Phase 1 Schema Amendments (carry into sheet.json update)

Two fields added as a result of Phase 3 planning:

1. `power_pp_cost_value` (number, default 0) added to `repeating_adept_powers` — numeric cost for sum computation. Separate from text display field `power_pp_cost`.
2. `spells_sustained` already added in Phase 2. Confirm default = 0.

---

## Phase 3 Deliverables

1. ⬜ `sheet.html` — roll template blocks added (`<rolltemplate>` tags), roll button `value` attributes finalized
2. ⬜ `sheet.html` — `<script type="text/worker">` block fully implemented (all tasks 3.2–3.13)
3. ⬜ `sheet.json` — final amendment: `power_pp_cost_value` added to repeating_adept_powers

## Phase 3 Success Criteria

- [ ] All attribute totals recompute on any sub-field change (test: change body_mutations → body updates)
- [ ] Reaction recomputes after int or dex changes
- [ ] All 4 pool bases recompute after constituent attribute changes
- [ ] pool_control_base tracks reaction total correctly
- [ ] cm_tn_mod shows 0 at clean, 3 at Deadly across all 3 tracks
- [ ] ep_total sums both repeating sections; ep_max formula correct
- [ ] Initiative roll uses @{init_dice}d6 + @{init_score} (sum, not cs)
- [ ] Skill rolls prompt for Pool dice and TN; count successes via cs>=
- [ ] Spell rolls prompt for Sorcery dice, Pool dice, TN; show drain code in template
- [ ] Drain resist prompts for remaining pool dice and TN; rolls Willpower + pool
- [ ] All 3 roll templates render charname, rollname, successes correctly
- [ ] sheet.html validates via Roll20 custom sheet sandbox (no JS errors on load)

---

---

## Phase 3 Amendment — Critical Failure Mechanic (confirmed 2026-03-28)

### Confirmed Rule

If **ALL** dice in a pool roll show a 1, the result is a **Critical Failure** (catastrophic outcome). This is the SR3 rule — **not** the SR4 ">half dice are 1s" glitch variant. One non-1 die anywhere in the roll prevents it. Zero-successes alone is NOT a critical failure.

---

### Roll20 Implementation Technique

**Core expression pattern for ALL success-counting rolls:**

```
[[ Nd6cs>=TN cf<=1 ]]
```

- `cs>=TN` — dice meeting or exceeding TN rendered **green** (successes contribute to result value)
- `cf<=1` — dice showing exactly 1 rendered **red** (critical failure indicators)
- The roll result value = success count (unchanged — `cf` does not alter the number)

**Critical failure condition is met when:** every die in the tray appears red and successes = 0. Roll20 renders this visually — all dice highlighted red with a zero result. Players and GM see this instantly in the dice tray; no additional computation is required.

**Why no separate ones-count roll:** A second `[[ Nd6cs<=1 ]]` expression would roll a fresh, independent set of dice (different physical results from the main roll). It cannot reference the same dice already rolled. Therefore `cf<=1` visual coloring on the **same roll expression** is the correct and only Roll20-native technique.

---

### Amendment to Task 3.14 — Roll Template Field Updates

**Remove:** `glitch` field with "discuss with Bryce" flag from all three templates.

**Replace with:** a zero-successes warning block using Roll20's inverted Mustache syntax `{{^successes}}`.

**Updated field additions apply to rolltemplate-skill, rolltemplate-attack, rolltemplate-spell:**

| Field / Block            | Purpose                                    | Implementation                                                           |
| ------------------------ | ------------------------------------------ | ------------------------------------------------------------------------ |
| `successes` (updated)  | Inline roll counting hits + marking 1s red | `[[ Nd6cs>=TN cf<=1 ]]`                                                |
| `{{^successes}}` block | Shows warning text when successes = 0      | `⚠ No successes — check dice tray. All red dice = Critical Failure.` |

**Note on zero-successes warning:** The `{{^successes}}` block triggers on ANY zero-hit roll, not only critical failures. It is an advisory hint; the dice tray is the definitive source of truth. A roll showing 0 successes with dice in multiple colors is simply a miss — critical failure requires every die to be red.

**Revised complete field list for each template:**

**rolltemplate-skill:**

- `charname`, `rollname`, `linked_attr`
- `successes` — `[[ Nd6cs>=TN cf<=1 ]]`
- `tn` — target number
- `{{^successes}}` warning block

**rolltemplate-attack:**

- `charname`, `rollname`, `weapon_name`
- `successes` — `[[ Nd6cs>=TN cf<=1 ]]`
- `tn`, `damage_code`, `power`
- `reach` (melee) / `range_band` (ranged) — empty string when not applicable
- `{{^successes}}` warning block

**rolltemplate-spell:**

- `charname`, `rollname`, `spell_name`
- `spell_type` (M/P), `spell_duration` (I/S/P), `force`
- `successes` — `[[ Nd6cs>=TN cf<=1 ]]`
- `tn`, `drain_code`, `sustained_penalty`
- `{{^successes}}` warning block

---

### Amendment to Task 3.15 — Add `cf<=1` to All Success-Counting Roll Expressions

Every success-counting roll button `value` must use `cs>=TN cf<=1`. Plain `cs>=TN` without `cf` is not permitted in production.

| Button                                        | Expression change                                          |
| --------------------------------------------- | ---------------------------------------------------------- |
| `btn_roll_{attr}` (all 9 attribute buttons) | `@{attr}d6cs>=?{TN\|4}` → `@{attr}d6cs>=?{TN\|4} cf<=1` |
| `btn_skill_roll`                            | pool roll → append `cf<=1`                              |
| `btn_attack_ranged`                         | pool roll → append `cf<=1`                              |
| `btn_attack_melee`                          | pool roll → append `cf<=1`                              |
| `btn_cast_spell`                            | sorcery+pool roll → append `cf<=1`                      |
| `btn_drain_resist`                          | wil+pool roll → append `cf<=1`                          |
| `btn_dodge`                                 | pool roll → append `cf<=1`                              |
| `btn_damage_resist_body`                    | body+pool roll → append `cf<=1`                         |

**Exempt (no cf modifier):**

- `btn_init_roll` — Sum roll (`@{init_dice}d6 + @{init_score}`). Initiative is not a success-counting roll; the critical failure mechanic does not apply.

---

### Phase 3 Success Criteria Additions

- [ ] All success-counting rolls use `cs>=TN cf<=1` — dice showing 1 render red in Roll20 tray
- [ ] `{{^successes}}` warning block present in all 3 roll templates
- [ ] Initiative roll confirmed as plain sum — no `cs` or `cf` modifiers applied
- [ ] Phase 3 plan has no unresolved "discuss with Bryce" flags

---

**Phase 3 Status: SPEC COMPLETE ✅ — Pending Bryce sign-off before Phase 4**

---

## Phase 4: CSS & Visual Design

### Phase Header

**Input:**

- Approved Phase 2 HTML skeleton (5-tab layout, 7 repeating sections, all inputs/buttons stubbed)
- Approved Phase 3 Sheet Worker specification (roll buttons with `cs>=TN cf<=1`, 3 roll templates)
- Extracted design system from `archive/Test_ver3.html` (canonical visual reference)

**Output:**

- Complete `<style>` block specification for `sheet.html`
- All selectors, layout models, colors, and Roll20 constraints documented per component
- Roll template stylesheet sections fully specified

**Gate:** Developer can implement the entire `<style>` block from this document alone, without referencing the archive files or making any aesthetic judgment calls. All hex values, selector names, and layout models are specified here.

---

### Extracted Design System Reference

*Source: `archive/Test_ver3.html`. All values below are direct hex — no CSS custom properties (`var()`) anywhere in the sheet.*

**Color Palette (comment-block constants — label these as comments at the top of the `<style>` block):**

| Comment Token                 | Hex         | Source in Archive                                         | Usage                                 |
| ----------------------------- | ----------- | --------------------------------------------------------- | ------------------------------------- |
| `COLOR_TEXT_PRIMARY`        | `#000000` | `.box-init` background, `color` on `.box-attribute` | Body text, primary labels             |
| `COLOR_TEXT_ON_DARK`        | `#ffffff` | `.box-init` text                                        | Text on dark backgrounds              |
| `COLOR_SURFACE_HEADER`      | `#f2f2f2` | `.header` background-color                              | Sheet header region background        |
| `COLOR_BORDER_STRONG`       | `#5f5f5f` | `.box-attribute`, `.box-skills` border                | Attribute/skills section borders      |
| `COLOR_BORDER_LIGHT`        | `#cccccc` | `.box`, `.box-condition`, `.box-dice-pool` border   | General section borders               |
| `COLOR_BORDER_FOCUS`        | `#888888` | `.damage-checkbox:focus` border                         | Input focus ring                      |
| `COLOR_CHECKBOX_BORDER`     | `#555555` | `.damage-checkbox:checked` border                       | Unchecked damage checkbox border      |
| `COLOR_DAMAGE_X`            | `#b81a1a` | `.damage-checkbox:checked::before` color                | ✘ glyph on checked damage checkboxes |
| `COLOR_TAB_NAV`             | `#dddddd` | `.tab-navigation` background-color                      | Tab navigation bar background         |
| `COLOR_SURFACE_INIT`        | `#000000` | `.box-init` background-color                            | Initiative box background             |
| `COLOR_WARN_AMBER`          | `#e6a817` | Not in archive — new addition                            | Magic TN warning: +2 sustained        |
| `COLOR_WARN_ORANGE`         | `#e06c00` | Not in archive — new addition                            | Magic TN warning: +4 sustained        |
| `COLOR_WARN_RED`            | `#cc2200` | Not in archive — new addition                            | Magic TN warning: +6+ sustained       |
| `COLOR_SUCCESS_HIGHLIGHT`   | `#1a7a1a` | Not in archive — new addition                            | Roll template success count badge     |
| `COLOR_ROLLTEMPLATE_SKILL`  | `#1a1a2e` | Not in archive — new addition                            | Skill roll template header bar        |
| `COLOR_ROLLTEMPLATE_ATTACK` | `#3a1c1c` | Not in archive — new addition                            | Attack roll template header bar       |
| `COLOR_ROLLTEMPLATE_SPELL`  | `#1c3a5e` | Not in archive — new addition                            | Spell roll template header bar        |
| `COLOR_ROW_ALT`             | `#f9f9f9` | Not in archive — derived from archive pattern            | Alternating even-row background       |

[DEV DECISION]: The roll template colors (`#1a1a2e`, `#3a1c1c`, `#1c3a5e`), magic warning ramp colors, and success highlight color are not in the archive. The above hex values are recommendations consistent with the dark aesthetic of the init box. Confirm with system owner before implementing.

**Typography (from archive):**

- `h3, h4`: `margin: 0; font-size: 15px` (explicit in archive)
- No `font-family` declared in archive — browser default sans-serif used
- Input/label font size: implied 14px (browser default in archive context)

**Core Layout Patterns (from archive):**

- Sections: `border: 1px solid [color]; padding: 10px; margin-bottom: 20px`
- Flex containers: `display: inline-flex; align-items: center; justify-content: space-between`
- Checkbox grid: `display: flex; flex-wrap: wrap; justify-content: space-between; gap: 3px`
- Tier columns: `flex: 0 0 calc(12% - 10px); margin-bottom: 10px`
- Tab navigation bar: `background-color: #dddddd; padding: 10px`
- Active tab panel: `display: block; overflow: hidden` (inactive: `display: none`)

---

### Task 4.1 — Global Reset & Base Typography

**Component:** `<style>` block preamble — universal reset, font stack, color palette comment block, base input/label/heading styles, table base

**What is being styled:** All elements globally, establishing the visual baseline before component-specific rules

**Selectors involved:**

- Universal reset: `*, *::before, *::after`
- Sheet body text: widest-scope selector available in Roll20's iframe context
- `input[type="text"]`, `input[type="number"]`, `textarea`
- `label`
- `h1, h2, h3, h4`
- `table`, `th`, `td`
- `button[type="roll"]` (base, before component-specific overrides)

**Key CSS properties and approach:**

- Apply `box-sizing: border-box` universally on `*, *::before, *::after` — prevents Roll20 padding/border conflicts on width calculations
- Set `font-family: sans-serif` at widest scope
- Font sizes by heading level: `h1` → `22px`, `h2` → `18px`, `h3` → `15px` (matching archive), `h4` → `15px` (matching archive)
- `margin: 0` on all headings (matching archive)
- `color: #000000` as default text color
- `input[type="text"]`, `input[type="number"]`: normalize with `border`, `padding: 2px 4px`, `font-size: 14px`, `font-family: inherit` — Roll20 injects `height` and `border-radius` on inputs that must be explicitly reset
- `label`: `font-size: 14px; font-weight: normal; display: inline-block` — Roll20 can render labels as block or add bold; explicitly normalize
- `table`: `border-collapse: collapse; width: 100%`
- `th`: `text-align: left; font-size: 13px; font-weight: bold; padding: 2px 4px`
- `td`: `padding: 2px 4px; vertical-align: middle`
- Color palette comment block at the very top of `<style>`: insert all color token comments using the table above as the source, one per line, format: `/* COLOR_TOKEN: #hexvalue — description */`

**Roll20-specific constraints:**

- Roll20 injects global `input` styles (large `height`, `border-radius`, `padding`) that inflate inputs — explicit small-value overrides are mandatory here, not optional
- `font-family` from Roll20's parent frame bleeds through the iframe boundary — set it explicitly
- Do NOT use `:root` for any values; `:root` is in the parent frame scope and not reliably accessible

**Acceptance Criteria:**

- All inputs on the sheet render at consistent compact size; no Roll20 default inflation visible
- Heading sizes follow h1 > h2 > h3 = h4 hierarchy
- Color palette comment block is the first content in the `<style>` block
- Zero `var(--)` occurrences in the `<style>` block

---

### Task 4.2 — Tab Navigation

**Component:** The 5-tab radio/label switcher — tab bar container, tab labels, active indicator, hidden/visible panel logic

**What is being styled:** The navigation system that shows/hides the 5 tab content panels using CSS-only sibling selectors

**HTML structure dependency (Phase 2):** Each tab is `input[type="radio"]` + `<label>` pairs with content panel `<div>` siblings. All radios, labels, and panels are children of the same parent. CSS general sibling combinator (`~`) drives visibility.

**Selectors involved:**

- `.sheet-tab-nav` — the tab bar container
- `input.sheet-tab-radio` — the hidden radio inputs (one per tab)
- `label.sheet-tab-label` — the visible clickable tab labels
- `input.sheet-tab-radio:checked + label.sheet-tab-label` — active label state
- `.sheet-tab-panel` — base class on all 5 content panel wrappers (hidden by default)
- Individual panel show rules: `input#tab-core:checked ~ .sheet-tab-panel-core`, repeated for `tab-skills`, `tab-magic`, `tab-gear`, `tab-bio`

**Key CSS properties and approach:**

- Tab bar `.sheet-tab-nav`: `display: flex; flex-direction: row; flex-wrap: wrap; background-color: #dddddd; padding: 6px 10px; gap: 4px; margin-bottom: 0`
- Radio inputs `input.sheet-tab-radio`: `display: none` — visually hidden, still functional
- Tab labels `.sheet-tab-label`: `padding: 5px 12px; cursor: pointer; background-color: #f2f2f2; border: 1px solid #5f5f5f; font-size: 13px; user-select: none; white-space: nowrap`
- Active label `input:checked + .sheet-tab-label`: `background-color: #5f5f5f; color: #ffffff; font-weight: bold; border-color: #5f5f5f`
- All content panels `.sheet-tab-panel`: `display: none` — hidden by default
- Active panel (per tab): use `input#tab-{slug}:checked ~ .sheet-tab-panel-{slug}` → `display: block`
- Tab order in DOM must be: Core → Skills → Magic → Gear → Bio (slugs: `tab-core`, `tab-skills`, `tab-magic`, `tab-gear`, `tab-bio`)

**Roll20-specific constraints:**

- Roll20 radio inputs receive injected styles — `display: none` on the radio must be explicit, not relying on inherited behavior
- Sibling combinator pattern requires radio inputs and panels to be strict DOM siblings within the same parent — confirm with Phase 2 HTML structure
- `flex-wrap: wrap` on the nav allows tab labels to wrap at narrow widths rather than overflow

**Acceptance Criteria:**

- Only one tab panel is visible at a time; all others have `display: none`
- Active tab label has `background-color: #5f5f5f` and `color: #ffffff`
- Inactive labels have `background-color: #f2f2f2`
- All 5 tab labels render in correct order (Core, Skills, Magic, Gear, Bio)
- Switching tabs requires no JavaScript
- Tab bar wraps correctly at narrow widths without horizontal overflow

---

### Task 4.3 — Attribute Table

**Component:** Core tab attribute region — the table with columns for Base/Mutations/Magic/Misc/Total, plus a roll button column

**What is being styled:** The outer container, the table internals, number input cells, the computed total cell, and the roll button column

**Archive reference:** `.box-attribute` — `display: inline-flex; align-items: center; justify-content: space-between; border: 1px solid #5f5f5f; padding: 10px; margin-bottom: 20px; max-width: 850px; flex-grow: 1; height: 100%`

**Selectors involved:**

- `.sheet-box-attribute` — outer container
- `.sheet-box-attribute table` — the attribute table
- `.sheet-box-attribute th` — column header cells
- `.sheet-box-attribute td` — data cells
- `.sheet-box-attribute tr:nth-child(even)` — alternating row shading
- `.sheet-box-attribute td input[type="number"]` — attribute number inputs
- `.sheet-box-attribute td.sheet-attr-total` — computed total cell (read-only display)
- `.sheet-box-attribute td.sheet-attr-roll` — roll button column cell
- `.sheet-box-attribute td.sheet-attr-roll button[type="roll"]` — the roll button per row

**Key CSS properties and approach:**

- Container `.sheet-box-attribute`: `display: inline-flex; align-items: flex-start; border: 1px solid #5f5f5f; padding: 10px; margin-bottom: 20px; max-width: 850px` (matching archive)
- Table column width allocation via `min-width` on `th`/`td`: Attribute name column ~140px; Base/Mutations/Magic/Misc numeric columns ~55px each; Total column ~55px; Roll button column ~50px
- Number inputs in attribute cells: `width: 45px; text-align: center; padding: 1px 2px`
- Attribute name cells (first column): `font-weight: bold; white-space: nowrap`
- Total cell `.sheet-attr-total`: `font-weight: bold; text-align: center; color: #000000` — no input box, display-only
- Column headers `.sheet-box-attribute th`: `background-color: #f2f2f2; border-bottom: 2px solid #5f5f5f; text-align: center`
- Even rows `tr:nth-child(even)`: `background-color: #f9f9f9`
- Odd rows `tr:nth-child(odd)`: `background-color: #ffffff`
- Roll button in `.sheet-attr-roll`: `padding: 2px 6px; font-size: 12px`

**Roll20-specific constraints:**

- `input[type="number"]` in Roll20 renders very wide without explicit `width` — always set width on number inputs
- Roll20's `button[type="roll"]` inherits Roll20's native button styles — pad and font-size overrides are required
- `max-width: 850px` is a guide — Roll20 panels can be narrower; compact fallback is defined in Task 4.12

**Acceptance Criteria:**

- All attribute rows render without horizontal overflow at standard Roll20 panel width (~700px)
- Total column is visually distinct: bold, no input border
- Roll button column is compact — does not inflate row height
- Alternating row shading is visible and consistent
- Column headers are centered with a bottom border

---

### Task 4.4 — Condition Monitor Track Styling

**Component:** The three damage tracks (Mental, Stun, Physical) — checkbox grid layout, ✘ red X checked state, tier column headers, TN penalty labels, overflow input

**What is being styled:** The entire condition monitor region including all three tracks and their sub-elements

**Archive reference — damage checkbox pattern (extracted verbatim from `Test_ver3.html`):**

- Unchecked state: `width: 16px; height: 16px; border: 1px solid #555555; border-radius: 3px; cursor: pointer`; `appearance: none` applied (removes browser default checkmark)
- Checked state `::before`: `content: "\2718"` (✘ Unicode), `position: absolute; top: -1px; left: 2px; font-size: 12px; line-height: 1; width: 16px; height: 16px; text-align: center; color: #b81a1a`
- Checked wrapper needs `position: relative` on the checkbox element itself
- Focus state: `outline: 0; border: 2px solid #888888`

**Selectors involved:**

- `.sheet-box-condition` — outer container
- `.sheet-condition-track` — wrapper for each of the 3 damage tracks
- `.sheet-condition-track h3` — track name labels ("Mental Damage", "Stun Damage", "Physical Damage")
- `.sheet-condition-grid` — the flex grid of tier columns within each track (equivalent to archive `.checkbox`)
- `.sheet-condition-tier` — each tier column (`flex` child)
- `.sheet-condition-tier h4` — tier header ("No Damage", "Light", "Moderate", "Serious", "Deadly", "Uncon")
- `input[type="checkbox"].sheet-damage-checkbox` — individual damage checkboxes
- `input[type="checkbox"].sheet-damage-checkbox:checked` — checked state (applies `appearance: none`, `position: relative`, base dimensions)
- `input[type="checkbox"].sheet-damage-checkbox:checked::before` — the ✘ glyph pseudo-element
- `input[type="checkbox"].sheet-damage-checkbox:focus` — focus ring
- `.sheet-condition-penalty` — TN penalty label beneath each tier header
- `.sheet-condition-tier-uncon h4` — "Uncon" tier header specifically (distinct color)
- `.sheet-condition-overflow` — Physical track only: overflow damage input after "Uncon" column

**Key CSS properties and approach:**

- Container `.sheet-box-condition`: `border: 1px solid #cccccc; padding: 10px; margin-bottom: 20px`
- Track wrapper `.sheet-condition-track`: `margin-bottom: 12px`
- Track name `h3`: `margin: 0; font-size: 15px; font-weight: bold; margin-bottom: 4px` (matching archive)
- Checkbox grid `.sheet-condition-grid`: `display: flex; flex-wrap: wrap; justify-content: flex-start; gap: 3px` (matching archive `.checkbox`)
- Tier column `.sheet-condition-tier`: `flex: 0 0 calc(12% - 6px); min-width: 36px; margin-bottom: 10px`
- Tier header `h4`: `margin: 0; font-size: 13px; margin-bottom: 2px` (adapted from archive)
- Penalty label `.sheet-condition-penalty`: `font-size: 11px; color: #555555; display: block; margin-top: 2px`
- Checkbox base (both checked and unchecked): `-webkit-appearance: none; -moz-appearance: none; appearance: none; position: relative; width: 16px; height: 16px; border: 1px solid #555555; border-radius: 3px; cursor: pointer; display: inline-block; vertical-align: middle`
- Checked `::before` pseudo-element: `content: "\2718"; display: block; position: absolute; top: -1px; left: 2px; font-size: 12px; line-height: 1; color: #b81a1a; width: 16px; height: 16px; text-align: center`
- Focus ring: `outline: 0; border: 2px solid #888888`
- "Uncon" header `.sheet-condition-tier-uncon h4`: `color: #b81a1a` — distinct red color to indicate severity
- Overflow input `.sheet-condition-overflow`: `width: 40px; font-size: 12px; text-align: center; border: 1px solid #5f5f5f; padding: 1px 2px`

**Roll20-specific constraints:**

- **CRITICAL:** Roll20's sandboxed iframe may not fully support `appearance: none` on checkboxes across all browsers that access Roll20 (Chrome, Firefox, Edge, Safari on various platforms). The archive's approach of applying `::before` directly on the `input[type="checkbox"]` element requires `appearance: none` to suppress the browser's native checkbox rendering.
- [DEV DECISION]: Test the `appearance: none; position: relative; ::before` approach directly on `input[type="checkbox"]` elements in Roll20's live sandbox before finalizing. If the browser does not support this pattern (e.g., browser ignores `appearance: none` on native inputs), the fallback is: visually hide the checkbox with `opacity: 0; position: absolute` and add a `<label>` immediately adjacent to each checkbox; use `input[type="checkbox"].sheet-damage-checkbox + label::before` for the unchecked styling and `input[type="checkbox"].sheet-damage-checkbox:checked + label::before` for the ✘ glyph. This requires HTML changes to Phase 2's condition monitor structure.
- Stun and Physical tracks include an "Uncon" 5th tier — style identically to other tiers except with `color: #b81a1a` on the header
- Physical track "Uncon" column is followed by the overflow damage input — position it as an additional `<div>` or `<td>` after the last tier column

**Acceptance Criteria:**

- Checked damage checkboxes display ✘ glyph in `#b81a1a` with no browser-default checkmark visible
- Unchecked damage checkboxes display as 16×16 bordered boxes
- Focus ring is `#888888` with `outline: 0`
- Tier headers ("No Damage", "Light", "Moderate", "Serious", "Deadly") align above their checkbox groups
- "Uncon" tier header renders in `#b81a1a`
- TN penalty labels (`+0 TN`, `+1 TN`, `+2 TN`, `+3 TN`, `+4 TN`) appear beneath each tier header
- Three tracks are visually separated with `margin-bottom: 12px` between them
- Overflow input on Physical track is visible and compact

---

### Task 4.5 — Dice Pools & Initiative Region

**Component:** The dice pool summary table and the initiative "black box" component

**What is being styled:** The horizontal layout of the init box and pool table

**Archive reference:** `.box-dice-pool` — `display: inline-flex; max-width: 600px`; `.box-init` — `background-color: #000000; color: #ffffff; text-align: center; max-width: 250px`

**Selectors involved:**

- `.sheet-box-dice-pool` — outer flex container for the entire region
- `.sheet-box-init` — the initiative black box sub-component
- `.sheet-box-init h4` — "Initiative:" label inside init box
- `.sheet-box-init button[type="roll"]` — the INIT roll button
- `.sheet-dice-pool-table` — the pools summary table
- `.sheet-dice-pool-table th, .sheet-dice-pool-table td` — table cells
- `.sheet-dice-pool-table td.sheet-pool-formula` — formula display column (read-only)
- `.sheet-dice-pool-table td.sheet-pool-base` — base rating column
- `.sheet-dice-pool-table td.sheet-pool-misc input` — misc modifier input
- `.sheet-dice-pool-table td.sheet-pool-total` — final computed total column

**Key CSS properties and approach:**

- Container `.sheet-box-dice-pool`: `display: inline-flex; align-items: flex-start; border: 1px solid #cccccc; padding: 10px; margin-bottom: 20px; max-width: 600px` (matching archive)
- Init box `.sheet-box-init`: `background-color: #000000; color: #ffffff; padding: 10px; margin-right: 10px; text-align: center; min-width: 80px; max-width: 120px; flex-shrink: 0` (adapted from archive's `max-width: 250px` — tighter for sharing row with table)
- Init label `h4`: `color: #ffffff; font-size: 15px; margin: 0 0 6px 0`
- Init roll button: `background-color: #333333; color: #ffffff; border: 1px solid #888888; padding: 4px 10px; cursor: pointer; font-size: 12px`
- Pool table column headers `th`: `background-color: #f2f2f2; border-bottom: 1px solid #5f5f5f; font-size: 12px; white-space: nowrap`
- Formula column `.sheet-pool-formula`: `font-size: 12px; color: #555555; font-style: italic` — decorative, not interactive
- Base and Total columns: `text-align: center; font-weight: bold`
- Misc input column: `width: 45px; text-align: center`

**Roll20-specific constraints:**

- Roll20 roll buttons inside dark-background containers do NOT inherit `color: #ffffff` by default — explicitly set on the init button
- `flex-shrink: 0` on the init box prevents it from collapsing when the table is wider

**Acceptance Criteria:**

- Init box renders as a black block with white text and white-styled roll button
- Init box and pool table are side-by-side when panel width permits
- All 4 pool rows (Combat, Spell, Control, Astral) are visible
- Formula column text is smaller and italicized (decorative differentiation)
- Misc column has a compact number input per pool row

---

### Task 4.6 — Repeating Section Rows

**Component:** All 7 K-scaffold repeating sections — consistent row layout, alternating colors, add/delete controls

**What is being styled:** The K-scaffold repeating container, row items, and Roll20-injected control buttons

**Selectors involved:**

- `.sheet-repcontainer` — K-scaffold outer repeating container (or Roll20's `.repcontainer` depending on K-scaffold version — [DEV DECISION] below)
- `.repitem` — each individual row (Roll20-injected class; do NOT rename)
- `.repitem:nth-child(even)` — alternating even row
- `.repitem:nth-child(odd)` — alternating odd row
- `.repitem input[type="text"]` — text inputs within rows
- `.repitem input[type="number"]` — number inputs within rows
- `.repitem button[type="roll"]` — roll buttons within rows
- `.repcontrol_add` — Roll20-injected "Add" button (below last row)
- `.repcontrol_del` — Roll20-injected per-row "Delete" button

**Key CSS properties and approach:**

- Container `.sheet-repcontainer` (or `.repcontainer`): `width: 100%; margin-bottom: 12px`
- Row `.repitem`: `display: flex; align-items: center; padding: 3px 6px; border-bottom: 1px solid #cccccc; gap: 6px`
- Even rows: `background-color: #f9f9f9`
- Odd rows: `background-color: #ffffff`
- Delete control `.repcontrol_del`: `margin-left: auto; font-size: 11px; color: #b81a1a; cursor: pointer; border: none; background: none; padding: 1px 4px` — right-aligned, red, minimal
- Add control `.repcontrol_add`: `display: block; margin-top: 4px; font-size: 12px; padding: 2px 8px; cursor: pointer`
- Text/number inputs inside `.repitem`: `flex-shrink: 0` with explicit per-section `width` values — each section's widths are defined in Tasks 4.10 (Gear) and the skill/spell/contacts sections below
- Roll buttons inside `.repitem`: `padding: 2px 6px; font-size: 12px; flex-shrink: 0`

**Section-specific button column notes:**

- `repeating_skills`: skill name (flex-grow), skill level (50px), TN (50px), roll button
- `repeating_spells`: spell name (flex-grow), drain TN (50px), force (50px), roll button
- `repeating_mutations`: mutation name (flex-grow), description (flex-grow), no roll button
- `repeating_adept_powers`: power name (flex-grow), PP cost (50px), no roll button
- `repeating_weapons`: handled in Task 4.10
- `repeating_equipment`: item name (flex-grow), qty (40px), weight (50px), no roll button
- `repeating_contacts`: contact name (flex-grow), loyalty (50px), connection (50px), no roll button

**Roll20-specific constraints:**

- `.repcontrol_add` and `.repcontrol_del` are Roll20-injected — selectors must match Roll20's generated names exactly. K-scaffold may wrap these differently.
- [DEV DECISION]: Verify K-scaffold's exact outer container class name (may be `.repcontainer` not `.sheet-repcontainer`) and control button class names (`.repcontrol_add`, `.repcontrol_del` are Roll20 native; K-scaffold may use variants). Adjust selectors post sandbox test.
- `.repitem` is Roll20-injected and cannot be renamed — style it as-is

**Acceptance Criteria:**

- All 7 repeating sections display consistent alternating row shading
- Delete control is right-aligned (via `margin-left: auto`) and red (`#b81a1a`)
- Add button is visible and labeled below the last row
- Text/number inputs inside rows don't overflow their row container
- Each row has a subtle bottom border (`#cccccc`) separating it from the next

---

### Task 4.7 — Roll Template CSS

**Component:** The 3 roll templates — `rolltemplate-skill`, `rolltemplate-attack`, `rolltemplate-spell` — chat card appearance

**What is being styled:** The Roll20 chat card output for all roll buttons on the sheet

**Selectors involved (replicate for all 3 templates; only `-skill` prefix shown, apply identically to `-attack` and `-spell`):**

- `.sheet-rolltemplate-skill` — outer wrapper
- `.sheet-rolltemplate-skill .sheet-template-header` — header bar
- `.sheet-rolltemplate-skill .sheet-template-body` — body region
- `.sheet-rolltemplate-skill .sheet-template-row` — each data row in the body
- `.sheet-rolltemplate-skill .sheet-template-label` — left-side row label
- `.sheet-rolltemplate-skill .sheet-template-value` — right-side row value
- `.sheet-rolltemplate-skill .sheet-template-successes` — success count badge
- `.sheet-rolltemplate-skill .sheet-template-nosuccess` — no-success / glitch warning (shown via `{{^successes}}`)
- `.sheet-rolltemplate-skill .sheet-template-critfail` — critical failure note (cf<=1 threshold reached)
- Repeat pattern for `.sheet-rolltemplate-attack.*` and `.sheet-rolltemplate-spell.*`

**Header bar color differentiation:**

- Skill rolls: `background-color: #1a1a2e` (dark navy)
- Attack rolls: `background-color: #3a1c1c` (dark maroon)
- Spell rolls: `background-color: #1c3a5e` (dark blue)

**Key CSS properties and approach:**

- Outer wrapper (all 3): `display: block; border: 1px solid [header color]; font-family: sans-serif; font-size: 13px; width: 100%; box-sizing: border-box; min-width: 200px`
- Header bar `.sheet-template-header`: `[per-template background-color]; color: #ffffff; padding: 6px 10px; font-weight: bold; font-size: 14px`
- Body `.sheet-template-body`: `padding: 2px 0`
- Row `.sheet-template-row`: `display: flex; align-items: baseline; padding: 3px 10px; border-bottom: 1px solid #cccccc`
- Row label `.sheet-template-label`: `font-weight: bold; color: #555555; min-width: 80px; flex-shrink: 0; font-size: 12px`
- Row value `.sheet-template-value`: `flex: 1; font-size: 13px`
- Success count badge `.sheet-template-successes`: `display: inline-block; background-color: #1a7a1a; color: #ffffff; font-weight: bold; padding: 2px 10px; font-size: 16px; border-radius: 2px`
- No-success warning `.sheet-template-nosuccess`: `color: #b81a1a; font-weight: bold; font-style: italic; font-size: 13px; padding: 4px 10px`
- Critical fail note `.sheet-template-critfail`: `color: #b81a1a; font-weight: bold; background-color: #fce8e8; padding: 3px 10px; font-size: 12px`
- All color values are direct hex — `var(--)` is not used

**Roll20-specific constraints:**

- Roll template selectors MUST use the `.sheet-rolltemplate-{name}` prefix — this is Roll20's mandatory naming convention
- Roll template CSS lives in the same `<style>` block as all other sheet CSS — Roll20 applies it to chat output
- Roll20's native `cf` coloring (making dice results red in the dice roller) is handled automatically by Roll20 when `cf<=1` is set; the `.sheet-template-critfail` element adds a text-based warning in the card, not dice coloring
- The `{{^successes}}` Handlebars inverse block renders a DOM element only when `successes` is falsy (0 or absent) — the `.sheet-template-nosuccess` selector targets the HTML wrapper of this block, not the Handlebars expression itself

**Acceptance Criteria:**

- All 3 roll template types render with a visually distinct header bar color per type
- Success count badge renders as a green (`#1a7a1a`) block with white text
- No-success state renders `#b81a1a` red italicized text
- Critical fail note renders with `#fce8e8` light-red background and `#b81a1a` text
- Template body rows show label and value in two columns
- No `var(--)` in any selector within roll template CSS

---

### Task 4.8 — Combat Panel Styling

**Component:** Core tab combat panel — Dodge and Resist Damage roll buttons, Armor region display

**What is being styled:** The dedicated combat section below the condition monitor on the Core tab

**Selectors involved:**

- `.sheet-combat-panel` — outer container for the combat section
- `.sheet-armor-region` — armor value display sub-region
- `.sheet-armor-region label` — "Armor:" label
- `.sheet-armor-region input[type="number"]` — armor value input
- `.sheet-combat-buttons` — the two-button row
- `.sheet-combat-buttons button[type="roll"]` — Dodge and Resist Damage buttons

**Key CSS properties and approach:**

- Combat panel `.sheet-combat-panel`: `border: 1px solid #5f5f5f; padding: 10px; margin-top: 8px; margin-bottom: 20px`
- Armor region `.sheet-armor-region`: `display: flex; align-items: center; gap: 8px; margin-bottom: 8px`
- Armor label: `font-weight: bold; font-size: 14px`
- Armor input: `width: 50px; text-align: center`
- Button row `.sheet-combat-buttons`: `display: flex; gap: 8px`
- Roll buttons in combat row: `flex: 1 1 auto; padding: 6px 10px; font-size: 13px; font-weight: bold; cursor: pointer` — `flex: 1 1 auto` makes both buttons share the row equally regardless of label length

**Roll20-specific constraints:**

- Roll20's default button styles add substantial padding — explicit overrides via `padding: 6px 10px` are required
- `flex: 1 1 auto` prevents one button from dominating if label lengths differ

**Acceptance Criteria:**

- Dodge and Resist Damage buttons appear side-by-side at equal width
- Armor value label and input appear above the button row
- Combat panel is visually bounded by `border: 1px solid #5f5f5f`
- Combat panel is positioned below the Armor Region within the Core tab

---

### Task 4.9 — Magic Tab Specifics

**Component:** Magic tab — sustained spell count badge, TN modifier warning color ramp, magic section region headers

**What is being styled:** The visual feedback elements unique to the Magic tab

**CSS class scheme for warning states:** The Sheet Worker (Phase 3) must set a class on the `.sheet-tn-warning` element. Three class variants drive three visual states. Class names used here must be coordinated with Phase 3 Sheet Worker implementation.

**Selectors involved:**

- `.sheet-tab-magic .sheet-sustained-count` — the sustained count badge
- `.sheet-tab-magic .sheet-tn-warning` — base TN warning container (hidden by default)
- `.sheet-tab-magic .sheet-tn-warning.sheet-warn-amber` — TN +2 state
- `.sheet-tab-magic .sheet-tn-warning.sheet-warn-orange` — TN +4 state
- `.sheet-tab-magic .sheet-tn-warning.sheet-warn-red` — TN +6+ state
- `.sheet-tab-magic .sheet-magic-region-header` — section headers within the Magic tab

**Key CSS properties and approach:**

- Sustained badge `.sheet-sustained-count`: `display: inline-block; background-color: #dddddd; border: 1px solid #5f5f5f; border-radius: 3px; padding: 1px 6px; font-size: 12px; font-weight: bold; min-width: 24px; text-align: center`
- Warning base `.sheet-tn-warning`: `font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 2px; display: none` — invisible unless a warning class is added
- Amber state `.sheet-warn-amber`: `display: inline-block; background-color: #e6a817; color: #000000` — dark text on amber for contrast
- Orange state `.sheet-warn-orange`: `display: inline-block; background-color: #e06c00; color: #ffffff`
- Red state `.sheet-warn-red`: `display: inline-block; background-color: #cc2200; color: #ffffff`
- Magic section headers `.sheet-magic-region-header`: inherit global `h2` / `h3` styles; `border-bottom: 1px solid #5f5f5f; margin-bottom: 8px; padding-bottom: 4px`

**Roll20-specific constraints:**

- Warning states must be CSS class-driven — Roll20 Sheet Workers can call `setAttrs()` but cannot directly manipulate DOM class lists. The typical Roll20 pattern for visual warnings is to use hidden inputs or computed attributes whose values trigger `:checked` sibling styles, or to use a `data-` attribute approach. [DEV DECISION]: Coordinate with Phase 3 Sheet Worker to determine whether the warning color ramp is best implemented via a `select` attribute with values 0/1/2/3 that the Sheet Worker sets, with CSS `[value="1"]`, `[value="2"]`, `[value="3"]` attribute selectors driving the warning states — this is the Roll20-compatible approach if direct class manipulation is not supported.
- Amber/orange/red colors were not in the archive — confirm with system owner before finalizing

**Acceptance Criteria:**

- Sustained count badge is compact and visible next to the "Sustained Spells:" label
- Warning element is invisible at 0 sustained spells
- Amber state appears at TN +2 modifier
- Orange state appears at TN +4 modifier
- Red state appears at TN +6+ modifier
- All three warning states have sufficient contrast (WCAG AA minimum: 4.5:1 for text)

---

### Task 4.10 — Gear Tab

**Component:** Gear tab — weapon rows in `repeating_weapons`, range band column layout, EP tracker

**What is being styled:** The weapon row layout within the repeating section and the standalone EP tracker

**Selectors involved:**

- `.sheet-tab-gear .repitem` — weapon rows (extends base `.repitem` from Task 4.6)
- `.sheet-tab-gear .sheet-weapon-name` — weapon name cell
- `.sheet-tab-gear .sheet-weapon-damage` — damage code cell
- `.sheet-tab-gear .sheet-weapon-mode` — fire mode / type cell
- `.sheet-tab-gear .sheet-range-bands` — flex wrapper for the 4 range band TN cells
- `.sheet-tab-gear .sheet-range-short` — Short range TN input
- `.sheet-tab-gear .sheet-range-medium` — Medium range TN input
- `.sheet-tab-gear .sheet-range-long` — Long range TN input
- `.sheet-tab-gear .sheet-range-extreme` — Extreme range TN input
- `.sheet-tab-gear .sheet-weapons-header` — static header row above the repeating section showing column labels
- `.sheet-tab-gear .sheet-ep-tracker` — EP tracker container
- `.sheet-tab-gear .sheet-ep-current` — current EP value input
- `.sheet-tab-gear .sheet-ep-max` — max EP value input
- `.sheet-tab-gear .sheet-ep-label` — "EP:" label

**Key CSS properties and approach:**

- Weapon row (scoped override of `.repitem`): `flex-wrap: nowrap` — keeps range columns on one line at normal width
- Weapon name `.sheet-weapon-name` input: `flex: 2 1 120px; min-width: 80px`
- Damage code `.sheet-weapon-damage` input: `flex: 0 0 60px; text-align: center`
- Fire mode `.sheet-weapon-mode` input: `flex: 0 0 50px; text-align: center`
- Range band wrapper `.sheet-range-bands`: `display: flex; gap: 3px; flex-shrink: 0`
- Each range input (`.sheet-range-short`, `.sheet-range-medium`, `.sheet-range-long`, `.sheet-range-extreme`): `width: 38px; text-align: center; font-size: 12px`
- Weapons header row `.sheet-weapons-header`: `display: flex; align-items: center; padding: 2px 6px; gap: 6px; background-color: #f2f2f2; border-bottom: 2px solid #5f5f5f; font-size: 12px; font-weight: bold` — must match `.repitem` column widths exactly for alignment
- EP tracker `.sheet-ep-tracker`: `display: flex; align-items: center; gap: 8px; padding: 6px 10px; border: 1px solid #5f5f5f; margin-bottom: 12px; margin-top: 8px`
- EP label `.sheet-ep-label`: `font-weight: bold; font-size: 14px`
- Current and max inputs: `width: 45px; text-align: center; font-size: 14px`
- EP separator between current/max: a `/` character styled with `font-size: 16px; color: #555555`

**Roll20-specific constraints:**

- `flex-wrap: nowrap` on weapon rows may cause overflow at very narrow panel widths — compact fallback in Task 4.12 adds `flex-wrap: wrap` override
- Weapons header row is a static `<div>` above the repeating section and must manually match the column widths of `.repitem` — a table-based approach is not possible with Roll20 repeating sections

**Acceptance Criteria:**

- Weapon name, damage code, fire mode, and 4 range band columns are horizontally aligned in each row
- Weapons header row column labels align with their corresponding input columns
- Range TN inputs are compact (38px wide)
- EP tracker shows current/max with a `/` separator
- Weapon rows inherit alternating row shading from Task 4.6

---

### Task 4.11 — Bio Tab

**Component:** Bio tab — character info fields, textarea styling, Session 0 question blocks

**What is being styled:** The biographical/narrative tab with free-text fields and structured question blocks

**Selectors involved:**

- `.sheet-tab-bio .sheet-bio-region` — outer wrapper for the bio tab
- `.sheet-tab-bio textarea` — all bio tab textareas
- `.sheet-tab-bio .sheet-bio-field-label` — labels above bio text inputs
- `.sheet-tab-bio input[type="text"]` — character info text inputs (name, race, station, etc.)
- `.sheet-tab-bio .sheet-session0-block` — each Session 0 question wrapper
- `.sheet-tab-bio .sheet-session0-block h4` — the question heading text
- `.sheet-tab-bio .sheet-session0-block textarea` — the answer textarea per question

**Key CSS properties and approach:**

- Bio region wrapper `.sheet-bio-region`: `padding: 10px`
- Textarea base: `width: 100%; min-height: 80px; border: 1px solid #cccccc; padding: 6px; font-family: sans-serif; font-size: 13px; resize: vertical; box-sizing: border-box`
- Field label `.sheet-bio-field-label`: `display: block; font-weight: bold; font-size: 13px; margin-bottom: 2px; margin-top: 10px`
- Character info inputs `input[type="text"]`: `width: 100%; border: 1px solid #cccccc; padding: 4px 6px; font-size: 13px; box-sizing: border-box`
- Session 0 block `.sheet-session0-block`: `border: 1px solid #dddddd; border-left: 3px solid #5f5f5f; padding: 8px; margin-bottom: 10px; background-color: #fafafa`
- Session 0 heading `h4`: `margin: 0 0 6px 0; font-size: 14px; font-weight: bold; color: #000000`
- Session 0 textarea (within block): same base textarea style with `min-height: 60px`

**Roll20-specific constraints:**

- Roll20's default `textarea` styling may override `resize` — set `resize: vertical` explicitly
- `box-sizing: border-box` is critical for `width: 100%` textareas inside padded containers to prevent overflow
- `font-family: sans-serif` on textareas must be explicit — Roll20 can inject monospace or serif in textareas

**Acceptance Criteria:**

- All textareas are full-width and vertically resizable
- Session 0 question blocks have a visible left-border accent in `#5f5f5f`
- Field labels are bold and appear directly above their associated input
- Character info inputs (name, race, station, height, weight, age) are full-width
- Bio tab layout is uncluttered and readable at standard Roll20 panel width

---

### Task 4.12 — Responsive / Compact Fallback

**Component:** Minimum width declarations and compact layout mode for narrow Roll20 panel widths

**What is being styled:** Layout degradation for Roll20's panel at widths below standard (~500px)

**Context:** Roll20 character sheet panels can display at widths as narrow as ~350px in portrait mode, side-by-side sheet+map view, or compact character sheet mode. Components with `flex-wrap: nowrap`, `inline-flex`, or fixed `max-width` values may overflow at these widths.

**Selectors involved:**

- `@media (max-width: 500px)` — if supported in Roll20's browser context (test required)
- Sheet root container: `min-width: 340px` — defines the minimum acceptable width before horizontal scroll
- `.sheet-box-attribute` in compact context: override to `display: block; max-width: 100%`
- `.sheet-box-attribute table th:nth-child(3), .sheet-box-attribute table td:nth-child(3)` — hide "Mutations" column in compact (nth-child(3))
- `.sheet-box-attribute table th:nth-child(4), .sheet-box-attribute table td:nth-child(4)` — hide "Magic" column in compact (nth-child(4))
- `.sheet-box-dice-pool` in compact context: override to `display: block; max-width: 100%` — init box stacks above pool table
- `.sheet-tab-gear .repitem` in compact context: `flex-wrap: wrap` — range bands wrap to second line
- Manual compact toggle: `input#sheet-compact-mode[type="checkbox"]:checked ~ .sheet-compact-target`

**Key CSS properties and approach:**

- Set `min-width: 340px` on the outermost sheet container to establish a minimum; below this, horizontal scrolling is acceptable
- Within `@media (max-width: 500px)` (if supported): override `display: inline-flex` to `display: block` on `.sheet-box-attribute` and `.sheet-box-dice-pool`; apply `display: none` to the Mutations (3rd) and Magic (4th) attribute table columns
- Manual fallback: a `input[type="checkbox"]#sheet-compact-mode` + `<label>` toggle in the sheet header region. When checked: general sibling `~` selector targets all `.sheet-compact-target` wrappers. Within `.sheet-compact-target`, apply the same `display: block` and column-hiding rules described above. Class `.sheet-compact-target` is applied to `.sheet-box-attribute`, `.sheet-box-dice-pool`, and `.sheet-tab-gear .sheet-repcontainer`
- All compact-mode rules use only CSS selectors — no JavaScript

**Roll20-specific constraints:**

- [DEV DECISION]: Roll20's CSS environment does NOT guarantee `@media` query support across all browsers that access Roll20. Test `@media (max-width: 500px)` in Roll20's live sandbox. If media queries fail to apply in Roll20's iframe, the manual toggle (`#sheet-compact-mode:checked ~ .sheet-compact-target`) is the production approach.
- The manual toggle checkbox must be a Roll20 `input[type="checkbox"]` with a proper `name` attribute so its state persists per-character

**Acceptance Criteria:**

- Sheet renders without critical horizontal overflow at 500px width regardless of method used
- At 350px, the attribute table degrades gracefully — either via media query or manual compact mode checkbox
- Compact mode hides the Mutations and Magic bonus columns in the attribute table
- Compact mode causes the init box to stack above the dice pool table (not side-by-side)
- Gear tab weapon rows wrap range band cells to a second line in compact mode
- All 5 tab panels remain functional in compact mode

---

### Phase Deliverables

1. **Color palette comment block** — all 18 color tokens documented at the top of the `<style>` block; no `var(--)` anywhere in the sheet
2. **Global reset** — `box-sizing`, font normalization, input/label/table base styles
3. **Tab navigation CSS** — pure CSS radio/label/sibling-selector tab system; 5 tabs; active state defined
4. **Attribute table CSS** — container, column widths, total cell styling, roll button column, alternating rows
5. **Condition monitor CSS** — all 3 tracks; ✘ (`\2718`) glyph in `#b81a1a` on checked checkboxes; tier columns; penalty labels; overflow input on Physical
6. **Dice pools & initiative CSS** — init black box; pool table; formula/base/misc/total column styles
7. **Repeating section row CSS** — base `.repitem` row style; alternating colors; delete (red, right-aligned) and add controls; 7 per-section column width specs
8. **Roll template CSS** — `.sheet-rolltemplate-skill`, `.sheet-rolltemplate-attack`, `.sheet-rolltemplate-spell`; per-template header color; success badge in `#1a7a1a`; no-success in `#b81a1a`; critfail on `#fce8e8` background
9. **Combat panel CSS** — armor region; Dodge + Resist Damage equal-width button row
10. **Magic tab CSS** — sustained count badge; 3-state TN warning ramp (amber/orange/red); magic section headers
11. **Gear tab CSS** — weapon row column layout; range band column alignment; weapons header row; EP tracker
12. **Bio tab CSS** — full-width textareas; Session 0 question block left-border accent; bio field labels
13. **Compact fallback CSS** — minimum width; compact mode attribute table (column-hiding); dice pool stacking; gear tab wrap fallback; manual toggle pattern

---

### Phase Success Criteria

- [ ] Zero `var(--)` CSS custom property references anywhere in the `<style>` block
- [ ] Zero `@import` rules in the `<style>` block
- [ ] All 18 color tokens present as comments at the top of `<style>`; all values trace to archive or are flagged [DEV DECISION]
- [ ] Tab navigation switches panels using only CSS radio/label/sibling patterns; no JavaScript
- [ ] Condition monitor checkboxes display ✘ in `#b81a1a` on checked state, confirmed functional in Roll20 sandbox
- [ ] All 3 roll template types render in Roll20 chat with distinct header bar colors
- [ ] Success count badge renders prominently in `#1a7a1a` green
- [ ] No-success and critical fail states are visually distinct from normal output
- [ ] Alternating row shading applies to all 7 repeating sections
- [ ] Delete controls are red (`#b81a1a`) and right-aligned in all repeating rows
- [ ] Magic TN warning ramp has 3 distinguishable states (amber → orange → red)
- [ ] EP tracker is visible and compact in the Gear tab
- [ ] Session 0 question blocks have a visible left-border accent (`#5f5f5f`, 3px)
- [ ] Sheet renders without horizontal overflow at 500px panel width
- [ ] Compact mode collapses attribute table to Name/Base/Misc/Total/Roll columns
- [ ] All [DEV DECISION] items confirmed with system owner before `<style>` block is finalized

---


---

## Phase 4 Amendment — Reviewer Corrections (2026-03-28)

*Reviewer verdict: FAIL → revised to PASS WITH NOTES after applying the following corrections.*
*Each section below supersedes the named task in the Phase 4 plan above.*

---

### Amendment 4-A — CRITICAL: Task 4.9 Magic TN Warning (supersedes Task 4.9 warning section)

**Root cause:** The primary spec described calling `classList.add()` from the Sheet Worker — architecturally impossible. Roll20 Sheet Workers only call `setAttrs()`. The [DEV DECISION] alternative is promoted here to the sole implementation spec.

**New implementation — attribute selector approach:**

Add a new integer attribute `tn_warning_level` (values: 0 = no warning, 1 = amber, 2 = orange, 3 = red) to:
- `sheet.json` Phase 1 schema: `{ "defaultValue": 0 }` (worker_only: true)
- Phase 3 Task 3.13 amendment: the `spells_sustained` watcher must also `setAttrs({ tn_warning_level: ... })` based on `sustained_tn_mod` thresholds:
  - `sustained_tn_mod >= 2 && < 4` → level 1 (amber)
  - `sustained_tn_mod >= 4 && < 6` → level 2 (orange)
  - `sustained_tn_mod >= 6` → level 3 (red)
  - `0` → level 0 (hidden)

**HTML dependency:** Add `<input type="hidden" name="attr_tn_warning_level" value="0">` as a sibling element immediately preceding `.sheet-tn-warning` in the Magic tab HTML. This is a Phase 2 amendment.

**Revised CSS selectors for Task 4.9 warning states:**
```
- `input[name="attr_tn_warning_level"]` — hidden input carrying the computed warning level
- `.sheet-tab-panel-magic .sheet-tn-warning` — warning container (hidden base state: `display: none`)
- `input[name="attr_tn_warning_level"][value="1"] ~ .sheet-tn-warning` — amber state
- `input[name="attr_tn_warning_level"][value="2"] ~ .sheet-tn-warning` — orange state
- `input[name="attr_tn_warning_level"][value="3"] ~ .sheet-tn-warning` — red state
```

**Revised CSS key properties for warning states:**
```
.sheet-tn-warning                         { display: none; font-size: 12px; font-weight: bold; padding: 3px 8px; border-radius: 2px; }
[value="1"] ~ .sheet-tn-warning          { display: inline-block; background-color: #e6a817; color: #000000; }
[value="2"] ~ .sheet-tn-warning          { display: inline-block; background-color: #e06c00; color: #ffffff; }
[value="3"] ~ .sheet-tn-warning          { display: inline-block; background-color: #cc2200; color: #ffffff; }
```

**Drop from Task 4.9:** Remove all references to `.sheet-warn-amber`, `.sheet-warn-orange`, `.sheet-warn-red` class variants. Remove "CSS class scheme for warning states" introductory paragraph. The compound class selectors in the original Task 4.9 are VOID — do not implement them.

**[DEV DECISION]:** The `input[name="attr_..."][value="..."] ~` sibling selector requires the hidden input to be a DOM sibling *immediately preceding* `.sheet-tn-warning`. Confirm this placement in sandbox — if the hidden input is inside a different container this selector fires against nothing.

---

### Amendment 4-B — CRITICAL: Task 4.8 Armor Region (supersedes Task 4.8 armor section)

**Root cause:** Task 4.8 was written as if armor was a single number field. Phase 2 Task 2.2 defines a 3-column × 4-row table (15 editable inputs + 3 computed totals = 18 fields).

**Full armor table CSS specification:**

**Selectors to add:**
```
- `.sheet-armor-region` — outer wrapper for the full armor table
- `.sheet-armor-region table` — the 3-column armor table
- `.sheet-armor-region thead tr` — header row (location names: Torso / Legs / Head)
- `.sheet-armor-region thead th` — per-column header cell
- `.sheet-armor-region tbody tr th` — row label cells (Name / Piercing / Slashing / Impact row labels, leftmost column)
- `.sheet-armor-region tbody td input[type="text"]` — armor name text inputs (one per location)
- `.sheet-armor-region tbody td input[type="number"]` — armor value number inputs (Piercing/Slashing/Impact per location = 9 inputs)
- `.sheet-armor-region tfoot tr` — totals row
- `.sheet-armor-region tfoot td` — computed total cells (armor_total_piercing / armor_total_slashing / armor_total_impact)
- `.sheet-armor-region tfoot th` — "Totals" row label cell
```

**Key CSS properties:**
- Outer wrapper `.sheet-armor-region`: `margin-bottom: 20px`
- Table: `border-collapse: collapse; width: 100%; max-width: 500px`
- Column headers `thead th`: `background-color: #f2f2f2; border: 1px solid #5f5f5f; text-align: center; padding: 3px 6px; font-size: 13px; min-width: 120px`
- Row label cells `tbody tr th`: `text-align: right; padding: 3px 8px; font-size: 13px; font-weight: bold; white-space: nowrap; border-right: 2px solid #5f5f5f; color: #555555`
- Name input cells: `width: 100%; font-size: 13px; border: 1px solid #cccccc; padding: 2px 4px`
- Numeric input cells `tbody td input[type="number"]`: `width: 48px; text-align: center; font-size: 13px; border: 1px solid #cccccc; padding: 2px 4px`
- All `tbody td`: `border: 1px solid #cccccc; padding: 2px 4px; text-align: center`
- Totals row `tfoot tr`: `background-color: #f2f2f2; border-top: 2px solid #5f5f5f`
- Totals cells `tfoot td`: `font-weight: bold; text-align: center; border: 1px solid #5f5f5f; padding: 3px 6px; font-size: 13px` — no input, read-only display value
- Totals label `tfoot th`: same style as `tbody tr th` with "Totals" label

**Acceptance criteria (replaces single input criterion):**
- 3 location columns (Torso / Legs / Head) with distinct column headers
- 4 rows: Name (text), Piercing (number), Slashing (number), Impact (number)
- Totals row shows computed `armor_total_{type}` values in bold with no input border
- Table max-width 500px, cell borders `#cccccc`, header borders `#5f5f5f`
- Armor region sits above the Combat Buttons region within Task 4.8's `.sheet-combat-panel`

---

### Amendment 4-C — MAJOR: Tasks 4.9, 4.10, 4.11 Scoping Selectors (supersedes all tab-scoped selectors in those tasks)

**Root cause:** Tasks 4.9, 4.10, 4.11 scope with `.sheet-tab-magic`, `.sheet-tab-gear`, `.sheet-tab-bio`. Task 4.2 defines panels as `.sheet-tab-panel-magic`, `.sheet-tab-panel-gear`, `.sheet-tab-panel-bio`. The mismatched class names will result in dead CSS selectors.

**Correction (apply globally across all Task 4.9/4.10/4.11 selectors):**

| Old (broken) prefix | Correct prefix |
|---|---|
| `.sheet-tab-magic ` | `.sheet-tab-panel-magic ` |
| `.sheet-tab-gear ` | `.sheet-tab-panel-gear ` |
| `.sheet-tab-bio ` | `.sheet-tab-panel-bio ` |

This affects every selector entry in those three tasks. Apply the substitution uniformly before implementing.

---

### Amendment 4-D — MAJOR: Task 4.10 Weapon Columns (supersedes Task 4.10 selector block + phase 4.6 weapon note)

**Root cause:** Task 4.10 specified only 5 columns for a 12-field row. Seven fields unspecified; wrong class name for weapon type; second roll button missing.

**Full weapon row column specification:**

| Field | Selector class | CSS width | Notes |
|---|---|---|---|
| `weapon_name` | `.sheet-weapon-name` | `flex: 2 1 100px` | flex-grow, min 100px |
| `weapon_type` (select) | `.sheet-weapon-type` | `flex: 0 0 80px` | **Renamed from `.sheet-weapon-mode`** — this is a category select (Edged/Club/etc.), not fire mode |
| `weapon_modifiers` | `.sheet-weapon-modifiers` | `flex: 1 1 60px` | text, condensed |
| `weapon_power` | `.sheet-weapon-power` | `flex: 0 0 40px; text-align: center` | number |
| `weapon_damage` | `.sheet-weapon-damage` | `flex: 0 0 55px; text-align: center` | text (e.g. "4M") |
| `weapon_conceal` | `.sheet-weapon-conceal` | `flex: 0 0 36px; text-align: center` | number |
| `weapon_reach` | `.sheet-weapon-reach` | `flex: 0 0 36px; text-align: center` | number |
| `weapon_ep` | `.sheet-weapon-ep` | `flex: 0 0 36px; text-align: center` | number |
| Range bands (4 inputs) | `.sheet-range-bands` wrapper | — | container for the 4×38px range inputs |
| `weapon_range_short` | `.sheet-range-short` | `width: 36px; text-align: center; font-size: 11px` | text TN |
| `weapon_range_medium` | `.sheet-range-medium` | same | — |
| `weapon_range_long` | `.sheet-range-long` | same | — |
| `weapon_range_extreme` | `.sheet-range-extreme` | same | — |
| `btn_attack_ranged` | within `.repitem` | `flex: 0 0 auto; padding: 2px 4px; font-size: 11px` | Ranged roll button |
| `btn_attack_melee` | within `.repitem` | same | Melee roll button |

**Range band wrapper `.sheet-range-bands`:** `display: flex; gap: 2px; flex-shrink: 0`

**Drop `.sheet-weapon-mode`** — this class name is void; use `.sheet-weapon-type` per Phase 2 field name.

**Weapons header row:** Update the static header row to include all 13 column labels above. Column labels: Name | Type | Mods | PWR | DMG | Conc | Rch | EP | Short | Med | Long | Ext | Ranged | Melee

**[DEV DECISION]:** At narrow Roll20 panel widths, this 15-column row will overflow. Task 4.12's compact fallback (flex-wrap on gear repitems) is the mitigation. Verify weapon row horizontal overflow threshold in sandbox.

---

### Amendment 4-E — MAJOR: Task 4.6 Skills Column Spec (supersedes skills entry in Task 4.6 section-specific notes)

**Root cause:** "skill level (50px), TN (50px)" do not correspond to any Phase 2 field names. Five fields had no width.

**Corrected skill row column specification:**

| Field | CSS width/flex | Notes |
|---|---|---|
| `skill_name` | `flex: 2 1 100px` | Widest column |
| `skill_linked_attr` (select) | `flex: 0 0 70px` | Dropdown: body/dex/str/etc. |
| `skill_general` | `flex: 1 1 55px` | Category text, condensed |
| `skill_spec` | `flex: 1 1 55px` | Specialization text, condensed |
| `skill_base` | `flex: 0 0 38px; text-align: center` | Number |
| `skill_foci` | `flex: 0 0 38px; text-align: center` | Number |
| `skill_misc` | `flex: 0 0 38px; text-align: center` | Number |
| `skill_total` (read-only) | `flex: 0 0 42px; text-align: center; font-weight: bold; border: none; background: #f2f2f2` | Computed — visually distinct from editable inputs |
| `btn_skill_roll` | `flex: 0 0 auto; padding: 2px 4px; font-size: 11px` | Compact roll button |

---

### Amendment 4-F — MAJOR: Missing Karma Row (new Task 4.5a, insert after Task 4.5)

**Root cause:** The Karma Row (Phase 2 Task 2.2 item 6) had no CSS specification.

**Task 4.5a — Karma Row**

**Component:** Core tab karma row — karma_good, karma_used, karma_total (computed), karma_pool — compact inline row

**Selectors:**
- `.sheet-karma-row` — outer flex container
- `.sheet-karma-row label` — labels ("Good:", "Used:", "Total:", "Pool:")
- `.sheet-karma-row input[type="number"]` — editable karma inputs
- `.sheet-karma-row .sheet-karma-total` — read-only computed karma_total display

**Key CSS properties:**
- `.sheet-karma-row`: `display: flex; align-items: center; gap: 12px; padding: 6px 10px; border: 1px solid #cccccc; margin-bottom: 20px; flex-wrap: wrap`
- Labels: `font-weight: bold; font-size: 13px; white-space: nowrap`
- Editable inputs (karma_good, karma_used, karma_pool): `width: 55px; text-align: center; font-size: 14px`
- Computed total `.sheet-karma-total`: `width: 55px; text-align: center; font-size: 14px; font-weight: bold; border: 1px solid #5f5f5f; background-color: #f2f2f2; padding: 2px 4px` — differentiated from editable inputs

**Add to Phase Deliverables:** "Karma Row CSS — compact inline layout with read-only total differentiated from editable inputs"
**Add to Phase Success Criteria:** `[ ] Karma total cell is visually distinct (gray background, bold) from good/used/pool inputs`

---

### Amendment 4-G — MAJOR: Missing Skills Tab Computed Display Badges (extend Task 4.6)

**Root cause:** Phase 2 Task 2.3 defines `essence_total` and `power_points_*` as header-level display badges in repeating section headers. No CSS was specified for them.

**Additional selectors for Task 4.6 (append to selector block):**
```
- `.sheet-skills-section-header` — wrapper for each section header on the Skills tab (Mutations, Adept Powers)
- `.sheet-skills-section-header h2` — section title ("Mutations", "Adept Powers")
- `.sheet-computed-badge` — shared class: read-only computed value display element used in section headers
- `.sheet-essence-display` — Mutations header: "Essence Used: {essence_total}"
- `.sheet-pp-display` — Adept Powers header: "PP: {used} / {max} remaining: {remaining}"
```

**Key CSS properties (append to Task 4.6 key properties):**
- Section header `.sheet-skills-section-header`: `display: flex; align-items: center; justify-content: space-between; padding: 4px 0; border-bottom: 2px solid #5f5f5f; margin-bottom: 6px`
- Section title `h2` within header: `margin: 0; font-size: 16px`
- Computed badge `.sheet-computed-badge`: `display: inline-block; background-color: #f2f2f2; border: 1px solid #5f5f5f; border-radius: 2px; padding: 1px 8px; font-size: 12px; font-weight: bold`
- `.sheet-essence-display` and `.sheet-pp-display`: extend `.sheet-computed-badge`; no additional rules needed

**Acceptance criteria (append):**
- Essence Used badge renders in `#f2f2f2` box with `#5f5f5f` border next to "Mutations" section header
- PP tracker badge (used/max/remaining) renders in same style next to "Adept Powers" section header
- Section headers have a bottom border `2px solid #5f5f5f`

---

### Amendment 4-H — MAJOR: Task 4.5 Initiative Row Inputs (append to Task 4.5)

**Root cause:** Task 4.5 styled the "init black box" component but omitted the 4-field Initiative Row (Phase 2 Task 2.2 item 4) which is a separate inline row of inputs.

**Additional selectors to append to Task 4.5:**
```
- `.sheet-initiative-row` — inline flex container for the 4 init fields
- `.sheet-initiative-row label` — "d6", "Reaction Mod", "Misc", "Score" labels
- `.sheet-initiative-row input[type="number"]` — init_dice, init_reaction_mod, init_misc_mod inputs
- `.sheet-initiative-row .sheet-init-score` — read-only init_score display
```

**Key CSS properties (append to Task 4.5):**
- `.sheet-initiative-row`: `display: flex; align-items: center; gap: 8px; padding: 4px 0; margin-bottom: 12px; flex-wrap: wrap`
- Labels: `font-size: 12px; color: #555555; white-space: nowrap`
- Editable inputs (init_dice, init_reaction_mod, init_misc_mod): `width: 42px; text-align: center; font-size: 13px`
- Read-only score `.sheet-init-score`: `width: 42px; text-align: center; font-size: 14px; font-weight: bold; border: 1px solid #5f5f5f; background-color: #000000; color: #ffffff; padding: 2px 4px` — visual echo of the init black box aesthetic

---

### Amendment 4-I — Task 4.12 Compact Toggle DOM Constraint (append to Task 4.12)

**Root cause:** The `~` general sibling combinator requires the compact-mode checkbox and all `.sheet-compact-target` elements to be siblings at the same DOM level. This structural requirement was undocumented.

**Append to Task 4.12 Roll20-specific constraints:**
"**DOM Co-location Constraint [DEV DECISION]:** The CSS general sibling combinator `~` in `#sheet-compact-mode:checked ~ .sheet-compact-target` requires the compact-mode `<input>` and ALL `.sheet-compact-target` elements to be **direct children of the same parent container** — the `~` selector cannot cross block containment boundaries. The compact-mode checkbox must be placed at the same DOM level as the tab panel wrappers (`.sheet-tab-panel-core`, `.sheet-tab-panel-gear`), not inside a header sub-div. Verify sibling co-location in Phase 2 HTML before implementing. If the compact checkbox is inside a header container, either restructure Phase 2 HTML to hoist it, or replace with a per-tab compact radio pattern."

**Also append cross-reference for repcontainer selector:**
"**Cross-reference Task 4.6 [DEV DECISION]:** If sandbox testing confirms K-scaffold uses `.repcontainer` (without `sheet-` prefix), update the compact fallback selector from `.sheet-tab-gear .sheet-repcontainer` to `.sheet-tab-panel-gear .repcontainer` — both the prefix AND the repcontainer class name must be consistent with Task 4.6's sandbox-verified value."

---

### Amendment 4-J — Minor Fixes (targeted corrections, no task rewrites needed)

**FINDING-15 — Task 4.2 active label key CSS property:**
Change:
- Active label `input:checked + .sheet-tab-label`: ...
To:
- Active label `input.sheet-tab-radio:checked + label.sheet-tab-label`: `background-color: #5f5f5f; color: #ffffff; font-weight: bold; border-color: #5f5f5f`

**FINDING-10 — Task 4.4 checkbox base rule:**
Add as the first entry in the selector list for checkbox styling:
```
- `input[type="checkbox"].sheet-damage-checkbox` — base (unchecked) state: sets `-webkit-appearance: none; -moz-appearance: none; appearance: none`, 16×16 dimensions, `border: 1px solid #555555`, `border-radius: 3px`, `cursor: pointer`, `position: relative`, `display: inline-block`, `vertical-align: middle`
```
Move ALL mention of `appearance: none` and base dimensions OUT of the `:checked` rule description and into this base rule. The `:checked` rule description becomes: "checked state — no additional dimensions or normalization needed; inherits base rule."

**FINDING-11 — Task 4.4 initiative penalty label:**
Add to selector list:
```
- `.sheet-condition-init-penalty` — Initiative penalty label (-1/-2/-3 Init) below each TN penalty label
```
Add to key CSS properties:
```
- Init penalty label `.sheet-condition-init-penalty`: `font-size: 10px; color: #888888; display: block; margin-top: 1px; font-style: italic`
```
Add to acceptance criteria: "Initiative penalty labels (-1 Init, -2 Init, -3 Init) appear in italicized muted gray below the TN penalty labels."

**FINDING-12 — Task 4.4 "No Damage" tier:**
Add to Task 4.4 key CSS properties:
"[DEV DECISION] Phase 2 defines 4 tier columns only (Light/Moderate/Serious/Deadly). 'No Damage' listed in acceptance criteria is not a Phase 2 HTML element — it has no checkboxes. If implemented as a visual-only label in a leftmost tier-header position, specify it as an empty non-data column. Confirm with system owner whether this is a Phase 2 scope amendment before adding HTML and CSS for it."

**FINDING-13 — Color palette DEV DECISION block:**
Add to the [DEV DECISION] confirmation block (the block that already lists roll template colors, magic warning ramp, and success highlight):
"`COLOR_ROW_ALT: #f9f9f9` — derived from archive gray scale; no direct archive reference. Confirm with system owner."

---

### Phase 4 Post-Amendment Status: PASS WITH NOTES ✅

All FAIL and MAJOR findings resolved above. MINOR findings resolved in Amendment 4-J.

**Remaining open [DEV DECISION] items requiring system owner confirmation before style block is finalized:**
1. Roll template header bar colors (#1a1a2e / #3a1c1c / #1c3a5e)
2. Magic TN warning ramp colors (#e6a817 / #e06c00 / #cc2200)
3. Success count badge green (#1a7a1a)
4. `COLOR_ROW_ALT` (#f9f9f9)
5. "No Damage" tier column — Phase 2 scope amendment vs. visual-only label
6. `@media` query support in Roll20 sandbox (vs. manual compact toggle)
7. K-scaffold class name for repeating container (`.repcontainer` vs `.sheet-repcontainer`)
8. `appearance: none` on checkboxes — sandbox cross-browser verification
9. Magic TN warning hidden input sibling placement verification
10. Compact-mode checkbox DOM co-location verification

**New data model additions required (Phase 1/3 carry-forward):**
- `tn_warning_level` field added to `sheet.json` (worker_only: true, integer 0–3)
- Phase 3 Task 3.13 (`spells_sustained` watcher) extended to also `setAttrs({ tn_warning_level: ... })`
- Magic tab Phase 2 HTML: `<input type="hidden" name="attr_tn_warning_level" value="0">` added as sibling of `.sheet-tn-warning`

---


---

## Phase 4 Amendment — DEV DECISION Resolutions (2026-03-28)

### D1–D4: Colors CONFIRMED ✅

All proposed color values approved by system owner. These are now locked — no further confirmation needed.

| Token | Hex | Usage | Status |
|---|---|---|---|
| `COLOR_ROLLTEMPLATE_SKILL` | `#1a1a2e` | Skill roll template header bar | **LOCKED** |
| `COLOR_ROLLTEMPLATE_ATTACK` | `#3a1c1c` | Attack roll template header bar | **LOCKED** |
| `COLOR_ROLLTEMPLATE_SPELL` | `#1c3a5e` | Spell roll template header bar | **LOCKED** |
| `COLOR_WARN_AMBER` | `#e6a817` | Magic TN warning: sustained_tn_mod = +2 (dark text) | **LOCKED** |
| `COLOR_WARN_ORANGE` | `#e06c00` | Magic TN warning: sustained_tn_mod = +4 (white text) | **LOCKED** |
| `COLOR_WARN_RED` | `#cc2200` | Magic TN warning: sustained_tn_mod = +6+ (white text) | **LOCKED** |
| `COLOR_SUCCESS_HIGHLIGHT` | `#1a7a1a` | Roll template success count badge | **LOCKED** |
| `COLOR_ROW_ALT` | `#f9f9f9` | Alternating even-row background in repeating sections | **LOCKED** |

---

### D5: "No Damage" Column — Option A CONFIRMED ✅

**Decision:** Add a 5th leftmost "No Damage" column to all 3 condition monitor tracks. This is a visual-only label column — no checkboxes, just the state name and a clean baseline indicator.

**Phase 2 HTML amendment required:**
Each `.sheet-condition-track` div gains a first `.sheet-condition-tier` child:
```html
<div class="sheet-condition-tier sheet-condition-tier-nodamage">
  <h4>No Damage</h4>
  <!-- no checkboxes — visual baseline state only -->
</div>
```

**Phase 4 CSS addition (append to Task 4.4 selector list):**
```
- `.sheet-condition-tier-nodamage` — the leftmost baseline column on all 3 tracks
- `.sheet-condition-tier-nodamage h4` — "No Damage" column header
```

**Key CSS for No Damage tier:**
```
.sheet-condition-tier-nodamage {
  flex: 0 0 calc(12% - 6px);
  min-width: 36px;
  margin-bottom: 10px;
}
.sheet-condition-tier-nodamage h4 {
  margin: 0;
  font-size: 13px;
  color: #555555;
  font-style: italic;
}
```

**Updated acceptance criteria for Task 4.4:**
Replace: "Tier headers ('No Damage', 'Light', 'Moderate', 'Serious', 'Deadly') align above their checkbox groups"
With: "5 tier columns per track: 'No Damage' (label-only, no checkboxes) | Light | Moderate | Serious | Deadly — Stun and Physical tracks additionally have a 6th 'Uncon' column"

---

### D6–D10: Sandbox Verification Tests — Implementation Sprint Checklist

These 5 items are unresolvable before implementation. The developer must run these tests **first**, before writing any CSS, and update Task selectors based on the results.

**Pre-implementation checklist (print and test in order):**

| # | Test | If YES | If NO |
|---|---|---|---|
| D6 | Does `@media (max-width: 500px)` apply inside Roll20's iframe? | Use media queries as specified | Use only the manual `#sheet-compact-mode:checked ~` toggle pattern |
| D7 | Does K-scaffold generate `.sheet-repcontainer` as the outer wrapper? | Keep `.sheet-repcontainer` in Tasks 4.6 + 4.12 | Replace with `.repcontainer` everywhere |
| D8 | Does `appearance: none` suppress native checkbox rendering in Chrome + Firefox on Roll20? | Use `input[type="checkbox"]::before` pattern | Restructure Phase 2 HTML to use hidden checkbox + adjacent label; use `label::before` pattern |
| D9 | Is `input[name="attr_tn_warning_level"]` a direct DOM sibling of `.sheet-tn-warning` in the rendered sheet? | Attribute selector `~` will fire correctly | Reposition hidden input in Phase 2 HTML to be a true sibling |
| D10 | Is the compact-mode `<input>` a direct DOM sibling of all `.sheet-tab-panel-*` elements? | `#sheet-compact-mode:checked ~ .sheet-compact-target` will fire | Move compact-mode checkbox in Phase 2 HTML to be at tab-panel level, or switch to per-panel compact toggles |

---

### Phase 4 Final Status: ALL DEV DECISIONS RESOLVED ✅

**Colors:** 8 tokens locked  
**Structure:** "No Damage" column confirmed as Phase 2 amendment  
**Sandbox tests:** 5 items documented as pre-implementation checklist  

**Phase 4 is approved and ready for Phase 5 planning.**

---


---

# Layer 2 — Operational Granularity: Phase 5

## Companion App Architecture & Data Sync

### Phase Header

**Input:**
- Approved Phase 1–4 Roll20 sheet specification: naming contract (~150 scalar fields + 7 repeating section schemas), K-scaffold `sheet.json`, HTML skeleton, Sheet Worker spec, CSS spec
- Confirmed tech stack: Turso (libSQL/SQLite-compatible) as the edge database; Roll20 K-scaffold Sheet Workers as the sync trigger surface
- Campaign context: 6 players, multiple characters each, 1 GM; private group, not a public product

**Output:**
- Turso schema specification (table names, column names, column types, relationships, indices — no DDL)
- Roll20 ↔ Turso sync contract: outbound payload structure, inbound pull strategy, trigger model
- Companion app routing plan: routes, auth gates, read/write operations per route
- Security posture definition: token storage, access control, blast-radius analysis
- Conflict resolution protocol: sync_version model, conflict behavior
- `sheet.json` amendment: three new sync infrastructure fields (`char_db_id`, `char_sync_version`, `campaign_db_id`)
- All 16 [DECISION] items (DECISION-01 through DECISION-16) surfaced for system owner resolution in one pass

**Gate:** All 16 [DECISION] items in Tasks 5.1–5.6 answered by system owner before companion app implementation begins. Companion app development is a **separate TEMPO workflow** — this phase is a planning handoff document only.

---

### Task 5.1 — Turso Schema Design

**Component:** The relational data model in Turso that persists all campaign character data and supports the companion app's query patterns

**Context:** Roll20 stores all character data as a flat key-value map (attribute names → string/number values). The Turso schema must translate this flat model into a structured, queryable form. The three query patterns the schema must support without full-table scans:
1. All characters owned by player X
2. Full character sheet for character Y (all scalar fields + all repeating rows)
3. Summary of all characters in campaign Z (for GM dashboard — a subset of scalar fields per character)

**Tier 1 — Top-level entity tables (always normalized relational):**

| Table | Columns | Notes |
|---|---|---|
| `campaigns` | `id` (TEXT PK), `name` (TEXT), `created_at` (TEXT ISO 8601), `updated_at` (TEXT ISO 8601) | One row per campaign; this project has one campaign |
| `players` | `id` (TEXT PK), `campaign_id` (TEXT FK → campaigns.id), `display_name` (TEXT), `is_gm` (INTEGER 0/1), `auth_credential` (TEXT — hashed; content depends on auth model selected in Task 5.4), `created_at` (TEXT) | One row per player; auth credential column type depends on Task 5.4 [DECISION] |
| `characters` | `id` (TEXT PK — UUID assigned on first sync), `player_id` (TEXT FK → players.id), `campaign_id` (TEXT FK → campaigns.id), `char_name` (TEXT — denormalized from scalar blob for fast lookups), `is_active` (INTEGER 0/1), `created_at` (TEXT), `updated_at` (TEXT), `sync_version` (INTEGER default 0) | `char_name` is the only scalar field stored outside the blob — enables campaign dashboard query without parsing JSON; `sync_version` is the conflict resolution counter (see Task 5.6) |

**Tier 2 — Scalar character attributes (~150 fields per character):**

Three viable approaches exist. They are mutually exclusive — the schema choice drives both the sync payload format (Task 5.2) and the companion app read path (Task 5.4).

**Option A — Key/value table:**
One table `character_attributes` with columns: `character_id` (FK), `attr_name` (TEXT), `attr_value` (TEXT). One row per attribute per character → ~150 rows per character. Reads require 150-row fetch + application-side pivot to reconstruct a character. Writes can be targeted (send only changed attr).

**Option B — Wide typed table:**
One table `character_scalars` with one column per attribute (~150 columns). One row per character. Full-sheet read is one row. Schema requires ALTER TABLE if the attribute contract grows. Column types can be accurate (INTEGER for numbers, TEXT for strings, REAL for decimals like essence costs). Partial sync requires constructing a targeted UPDATE for only changed columns.

**Option C — JSON blob (hybrid, recommended):**
One table `character_scalars` with columns: `character_id` (TEXT PK, FK → characters.id) and `data` (TEXT — stores all ~150 scalar attributes serialized as a JSON string). Full-sheet read is one row + JSON.parse in application code. Schema never changes as the attribute contract evolves. SQLite's `json_extract()` function can query specific fields from the blob without deserializing in application code. Sync always sends the full scalar blob (no partial update needed — blob is <10KB at ~150 fields). Computed fields (attribute totals, pool bases, reaction, init_score, etc.) are excluded from the blob — they are recalculated in the companion app from their source fields, same as the Roll20 Sheet Worker does.

**Option D — Per-section tables for repeating sections (applies regardless of Tier 2 choice):**
One table per repeating section, each with: the Roll20-generated row ID as the primary key (TEXT — Roll20 assigns unique string tokens per row, e.g. `-M7X9hqxZ...`), `character_id` (FK → characters.id), section-specific columns per the Phase 1 schema, and `row_order` (INTEGER — preserves display order since Roll20 does not guarantee ordering). Tables: `rep_skills`, `rep_spells`, `rep_mutations`, `rep_adept_powers`, `rep_weapons`, `rep_equipment`, `rep_contacts`.

**Recommended schema approach:**
- Tier 1: normalized relational (campaigns, players, characters) — always
- Tier 2 scalars: Option C (JSON blob) — best balance of simplicity, schema stability, and read performance at this scale (≤~20 characters total)
- Repeating sections: Option D (per-section tables, Roll20 row ID as PK) — preserves sync identity without a separate ID mapping layer

**Why not Option B?** The Phase 1 attribute contract is finalized, but future campaign expansions (new mutation subtypes, new equipment fields, house rule additions) would require ALTER TABLE on a 150-column table. The JSON blob eliminates this friction entirely. At 6 players and ~20 characters, there is no performance case for column-level indexing on scalar attributes.

**Why not Option A?** Full-sheet reads (the companion app's primary use case) require 150+ row fetches and a pivot. The blob approach is one query.

**Indices required (named, not DDL):**

| Index name | Table | Column(s) | Purpose |
|---|---|---|---|
| `idx_characters_player` | characters | player_id | Lookup all characters for player X |
| `idx_characters_campaign` | characters | campaign_id | Lookup all characters in campaign Z |
| `idx_rep_skills_char` | rep_skills | character_id | Lookup skill rows for character Y |
| `idx_rep_spells_char` | rep_spells | character_id | Lookup spell rows for character Y |
| `idx_rep_mutations_char` | rep_mutations | character_id | Lookup mutation rows for character Y |
| `idx_rep_adept_powers_char` | rep_adept_powers | character_id | Lookup adept power rows for character Y |
| `idx_rep_weapons_char` | rep_weapons | character_id | Lookup weapon rows for character Y |
| `idx_rep_equipment_char` | rep_equipment | character_id | Lookup equipment rows for character Y |
| `idx_rep_contacts_char` | rep_contacts | character_id | Lookup contact rows for character Y |
| `idx_scalars_char` | character_scalars | character_id (UNIQUE) | Enforces one scalar blob per character; fast lookup |

[DECISION-01]: Confirm the hybrid schema approach (Option C for scalars + Option D for repeating sections), or select an alternative. The rest of the sync payload design (Task 5.2) and companion app read paths (Task 5.4) are specified based on this hybrid model — a different selection requires revising those sections.

[DECISION-02]: The `players` table includes an `auth_credential` column whose content (hashed passphrase, OAuth token, magic link seed, etc.) depends on the authentication model selected in Task 5.4. Confirm auth approach there first; this column's content is specified once the auth decision is made.

---

### Task 5.2 — Roll20 → Turso Sync (Outbound)

**Component:** The mechanism by which character data changed in Roll20 propagates to Turso

**Critical constraint:** Roll20's Sheet Worker `fetch()` support is available on Roll20 Pro game plans as of 2022 updates. Roll20 Plus and Free plan games may not have `fetch()` available in Sheet Workers. If the campaign is not on Roll20 Pro, outbound sync from the Sheet Worker is not possible and the entire outbound sync strategy must use a different approach (e.g., player manually exports a JSON file).

[DECISION-03]: Confirm the Roll20 campaign plan (Pro / Plus / Free). If not Pro, outbound sync via Sheet Worker fetch() is unavailable and Phase 5's sync architecture must be redesigned. All subsequent outbound sync design assumes Roll20 Pro.

**Trigger model options:**

| Option | Trigger | Sync frequency | Roll20 fetch() calls per session |
|---|---|---|---|
| A — Per-field onChange | Every attribute change event via K-scaffold watcher | Near-real-time | ~Hundreds (one per user edit) |
| B — Tab-switch | On `sheet:tabChange` or equivalent | Per tab switch | ~5–15 per session |
| C — Manual "Sync to DB" button | Player presses a dedicated sync button | Player-controlled | 1–5 per session |
| D — Debounced idle batch | N-second timer after last change fires a batched sync | Near-real-time, batched | ~10–20 per session |

**Recommended trigger:** Option C (manual sync button) as primary; Option D as a stretch goal.
- Rationale: This is a private tabletop group. Manual sync at natural pause points (end of combat, end of session, before consulting the companion app) is explicitly acceptable. Option A's call volume risks hitting rate limits and creates noise in the Sheet Worker event loop. Option D requires verifying that Roll20's Sheet Worker sandbox supports persistent `setTimeout` across tab switches — this is not guaranteed and must be tested (flag as Sandbox Verification Test D11 in the Phase 4 pre-implementation checklist).

[DECISION-04]: Confirm acceptable sync latency. If the GM needs live condition monitor state during combat (e.g., companion app shows real-time HP), Option A or D is required and the architecture must account for significantly higher Turso write volume. If manual/end-of-session sync is acceptable, confirm Option C.

**Sync payload structure (Roll20 → Turso):**
The payload is a JSON document sent to the Turso HTTP pipeline API (or to the proxy function — see Task 5.5). Specify what the top-level payload document contains; exact field names are confirmed in Layer 3:

- `character_id` — the Turso UUID stored in the `char_db_id` sheet attribute; identifies the record being written
- `campaign_id` — the Turso campaign UUID; stored as a sheet attribute `campaign_db_id` (new field to add to `sheet.json`)
- `sync_version_from` — the current `char_sync_version` value on the sheet at the time of sync; used for conflict detection in Turso (the write is rejected if Turso's current version > this value — see Task 5.6)
- `synced_at` — ISO 8601 timestamp of the sync event (client clock)
- `scalars` — the full JSON object of all ~150 scalar attribute values (key: attribute name per Phase 1 contract, value: current attribute value); excludes worker-only computed fields (see field exclusion list below)
- `repeating` — an object with 7 keys (one per section); each key maps to an array of row objects; each row object contains the Roll20 row ID and all section-specific field values per the Phase 1 repeating section schemas

**Always a full sync, never a delta patch.** The complete scalar object and all repeating section arrays are sent on every sync trigger. Reasons: (1) K-scaffold does not expose a dirty-field registry; (2) at ~150 scalar fields, the compressed payload is well under 50KB; (3) full sync eliminates partial-write logic complexity; (4) conflict resolution (Task 5.6) operates on whole-character snapshots, not field-level diffs.

**Fields excluded from sync payload:**

| Field category | Excluded? | Reason |
|---|---|---|
| Worker-only computed fields (all attribute totals, pool bases, pool totals, reaction_base, init_score, cm_tn_mod, cm_init_mod, sustained_tn_mod, skill_total, power_points_*, essence_total, karma_total, ep_total, ep_max, armor_total_*) | Yes — exclude | Fully derivable from source fields; companion app recomputes them; avoids double-truth problem |
| Roll button fields (btn_*) | Yes — exclude | No data value; Roll20 internal UI only |
| `char_db_id`, `char_sync_version`, `campaign_db_id` | Yes — exclude from scalars block; send as top-level payload fields | These are sync infrastructure, not character data |
| `init_dice` | Recommended: include | Low-cost; player may set this at character creation based on mutations; excluding it loses that state in the companion app |
| `bio_q01`–`bio_q20` | Recommended: include | 20 answers at ~100 chars each ≈ 2KB addition; complete character record in companion app; include |

[DECISION-05]: Confirm exclusion list. Any field excluded from the sync payload will not be visible in the companion app. If init_dice or bio questions should be read-only reference data in the companion app, they must be included.

**Auth token placement for the Sheet Worker HTTP call:**

| Option | Who can see the token | Recommendation |
|---|---|---|
| Hardcoded in Sheet Worker JS | Any player who views sheet source | Never acceptable |
| Sheet attribute (`turso_auth_token`) | All players in the session | Acceptable only with a write-only, single-DB-scoped token (see Task 5.5) |
| GM-only Roll20 hidden field | GM only (Roll20 enforces this at the data layer) | Better; sufficient for a trusted group |
| Proxy function (Cloudflare Worker / Vercel Edge) | Sheet Worker sees only the proxy URL + a lightweight shared secret (not the real Turso token) | Best security posture; adds one infrastructure component |

[DECISION-06]: Select token placement. Full security analysis is in Task 5.5. Decision here drives whether a proxy function needs to be built as part of Phase 5 implementation.

**New sheet attributes required (add to sheet.json as Phase 5 amendment):**

| Attribute name | Type | Default | Purpose |
|---|---|---|---|
| `char_db_id` | TEXT | `""` | Turso character UUID; set on first sync, read-only thereafter |
| `char_sync_version` | INTEGER | `0` | Last-known Turso sync_version; updated after successful push and pull |
| `campaign_db_id` | TEXT | `""` | Turso campaign UUID; set once by GM during campaign setup |

**Error handling on failed sync:**
Roll20 Sheet Workers cannot display native browser alerts. Three feedback options:
- Option A: Write a `sync_status` sheet attribute (TEXT: "Synced ✓", "Sync failed", "Never synced"); display as a small read-only label on the Core tab next to the sync button
- Option B: Sheet Worker posts a Roll20 chat message on sync success or failure (zero additional HTML; leverages existing Roll20 output channel; visible to all session participants)
- Option C: Silent failure (no player-facing feedback)

Recommended: Option B for error cases + Option A for persistent last-sync status display. Chat messages are appropriate for errors; a persistent status label avoids re-opening Roll20 just to check sync state.

[DECISION-07]: Confirm error feedback approach. Note that Option B (chat messages) are visible to all players in the session — some GMs prefer quiet sync. Confirm whether sync events should post to chat.

---

### Task 5.3 — Turso → Roll20 Sync (Inbound)

**Component:** The mechanism by which companion app writes (stored in Turso) propagate back into the Roll20 sheet

**Core constraint:** Roll20 Sheet Workers cannot receive external events, webhooks, or server-push messages. There is no mechanism to push data into Roll20 from outside. All inbound sync is pull-only, initiated from within the sheet. Persistent polling (setInterval) is not viable — Roll20's Sheet Worker sandbox does not support interval-based background tasks reliably across tab switches, and a polling timer firing in all open Roll20 windows simultaneously would generate unacceptable fetch() volume.

**Inbound sync strategy options:**

| Option | Mechanism | When it fires | Viability |
|---|---|---|---|
| A — Manual "Pull from DB" button | Player clicks a pull button; Sheet Worker fetches Turso, calls setAttrs() | On player demand | Fully viable; symmetric with outbound sync button |
| B — Auto-pull on sheet open | K-scaffold `on('sheet:opened', ...)` handler fetches Turso on every sheet open; calls setAttrs() to overwrite | On Roll20 sheet tab open | Fully viable; transparent to player; requires Turso to be reachable at sheet-open time |
| C — Read-only companion app | Companion app never writes to Turso; Roll20 is the only edit surface; companion app is display/reference only | N/A — no inbound sync needed | Viable; eliminates all inbound sync complexity; trades the "edit from companion app" feature |
| D — Periodic polling | Sheet Worker uses setInterval to call Turso every N seconds | Continuous | Not viable — Roll20 sandbox timer behavior is unreliable for persistent cross-tab-switch intervals; would generate excessive fetch() calls |

**Recommended strategy:** Option A (manual pull button) as the primary inbound mechanism, plus Option B (auto-pull on sheet open) for session start consistency.

- Auto-pull on sheet open (Option B) ensures the sheet always starts with the latest Turso state. Covers the case where a player edited via companion app between sessions. Auto-pull is guarded: if `char_db_id === ""` (sheet not yet linked to a Turso record), pull is skipped silently.
- Manual pull button (Option A) covers mid-session re-sync if the companion app was consulted and edited during a break.
- If the companion app is scoped as read-only (Option C), both pull mechanisms become unnecessary and this entire task collapses to "not applicable." Option C is a valid scope reduction.

[DECISION-08]: Is bidirectional sync required — meaning, can players edit character data in the companion app and have those edits reflected in Roll20? Or is the companion app a read-only reference tool, with Roll20 as the exclusive edit surface? This is the single most architecturally significant decision in Phase 5. Read-only companion app (Option C) eliminates Task 5.3 entirely, simplifies Task 5.6 to a trivial last-write-wins, and removes the need for inbound Sheet Worker logic.

**Inbound pull payload structure:**
The Turso read response contains the same top-level structure as the outbound sync payload: character scalars as a JSON object + 7 repeating section arrays. The Sheet Worker receives this payload and calls Roll20's `setAttrs()` to overwrite all fields.

**Scalar inbound apply:** All scalar fields in the payload are passed directly into a single `setAttrs()` call with `{silent: true}` to suppress cascaded Sheet Worker recalculations during the batch write. K-scaffold's cascade is triggered once after `setAttrs()` completes, recomputing all derived fields from the newly-written source values.

**Repeating section inbound apply — "clear then re-insert" strategy:**
Roll20 repeating section rows are identified by their Roll20-assigned row ID. Setting attributes for a row that does not exist creates the row; setting attributes for an existing row updates it; rows in Roll20 that are not in the payload need to be explicitly removed. The safe approach:
1. Read all current row IDs from Roll20 for each section
2. For each row ID not in the Turso payload: call Roll20's `removeRepeatingRow()`
3. For each row in the Turso payload: call `setAttrs()` using `repeating_{section}_{rowid}_{field}` syntax to set all column values
4. This process runs sequentially for all 7 sections — it is not a single atomic operation in Roll20

"Clear then re-insert" (remove all existing rows, then insert all Turso rows) is the simplest variant of step 1–3 above. It is fully deterministic. The cost is that it triggers Roll20's repeating section DOM refresh for all rows, which may produce a brief visual flash in the sheet — acceptable for a sync operation.

[DECISION-09]: Confirm "clear and re-insert all rows" for repeating sections on inbound pull, OR confirm "diff by row ID and apply minimal changes." Clear-and-reinsert is simpler to implement and verify. Diff-based sync is less visually disruptive but significantly more complex.

---

### Task 5.4 — Companion App Architecture

**Component:** The web-based character management tool running outside Roll20

**Minimum viable scope:**
1. Character list: shows all characters the authenticated player owns (name, race/station, active status)
2. Full character sheet view: displays all tabs of data (Core attributes, Skills, Magic, Gear, Bio) in read-only format
3. Full character sheet editor: form-based editing of all character fields (same data as Roll20 sheet); saves to Turso
4. GM dashboard: read-only summary of all characters in the campaign (name, player, condition monitors, pools, karma)
5. GM detail view: any character's full sheet in read-only form

Out of MVP scope (deferred, not planned here): dice roller, chat log, real-time live updates between companion app sessions, encounter tracker, mobile-native app.

**Routing plan:**

| Route | Purpose | Auth gate | Turso operations |
|---|---|---|---|
| `/` | Landing page; redirect authenticated users to `/characters` | None (public) | None |
| `/login` | Authentication entry point (form depends on auth model selected) | None | Read players for credential check |
| `/characters` | List all characters owned by the authenticated player | Any authenticated player | Read characters WHERE player_id = auth.player_id |
| `/characters/[id]` | Full character sheet — view and edit form | Owner of character, OR GM | Read character_scalars + all 7 rep tables for character [id] |
| `/characters/new` | Create a new blank character record in Turso; not yet linked to Roll20 | Any authenticated player | Insert into characters, character_scalars |
| `/gm` | GM dashboard: summary card for every character in the campaign | GM role only | Read characters JOIN players for campaign; read selective scalar fields per character |
| `/gm/[id]` | GM full-sheet view for any character | GM role only | Read same as `/characters/[id]` |
| `/logout` | Clear session | Any authenticated player | None |

**Frontend framework options:**

| Option | Stack | Turso integration | DX notes |
|---|---|---|---|
| A — SvelteKit + @libsql/client | SvelteKit server-side form actions + Turso's official JS client | First-class; Turso publishes a SvelteKit guide | Low boilerplate; form actions are clean for character editing; deploys to Cloudflare Pages, Vercel, Netlify |
| B — Next.js App Router + @libsql/client | Next.js 14 React Server Components + @libsql/client in server components | Fully supported; no official guide but well-documented community | Larger ecosystem; RSC ensures DB credentials stay server-side; more setup for form handling |
| C — Astro + @libsql/client | Astro SSR with server endpoints + @libsql/client | Fully supported | Minimal JS to browser; best for read-heavy content; form handling requires more manual setup vs. SvelteKit actions |

[DECISION-10]: Select frontend framework. Recommended: Option A (SvelteKit) for the best balance of form-handling ergonomics and deployment simplicity at this scale. If the developer is more familiar with Next.js, Option B is equally valid and no re-planning is required. All routing and auth patterns described here apply to all three options.

**Companion app write path (companion app → Turso):**
All writes originate from server-side code only — never from browser JavaScript. The `@libsql/client` library and Turso credentials live exclusively in the server-side runtime (not in any client bundle).

Scalar field edit write path:
1. Player submits the character edit form
2. Server-side form handler (action / API route / server endpoint) receives the form data
3. Handler reads the current `sync_version` from the `characters` table for this character
4. Handler serializes all scalar fields from the form into a JSON string
5. Handler writes the updated scalar blob to `character_scalars` and increments `sync_version` + updates `updated_at` on `characters` — both in a single transaction
6. Response confirms success; page re-renders with saved values

Repeating section row write path (add/edit/delete a skill row, weapon row, etc.):
1. Same server-side handling
2. Handler targets the specific per-section table (`rep_skills`, `rep_weapons`, etc.) with an INSERT, UPDATE, or DELETE
3. Handler updates `characters.updated_at` and increments `sync_version` in the same transaction as the section write

[DECISION-11]: Should the companion app use auto-save (save each field on blur, without explicit submit) or form-level save (explicit "Save Changes" button per tab or per section)? Auto-save per field risks partial writes when forms are not fully filled. Form-level submit is safer for a character sheet with many interdependent fields. Recommended: form-level submit per tab or per section, with a visible "unsaved changes" indicator.

**Authentication model:**

| Option | Description | External service needed | Complexity |
|---|---|---|---|
| A — Passphrase per player | GM assigns each player a unique passphrase; stored hashed (bcrypt or Argon2) in the `players.auth_credential` column; session token issued on successful login | None | Lowest; no external dependency; entirely self-contained |
| B — Magic link (email) | Player enters email address; server sends a one-time login link; session established on link click | Email sending service (Resend, Postmark — both have generous free tiers) | Low; stateless on the companion app side; requires email delivery reliability |
| C — Discord OAuth | OAuth 2.0 flow via a Discord application; player authorizes with their Discord account | Discord developer app registration (free) | Medium; requires each player to have a Discord account (high probability for a TTRPG group); Auth.js/NextAuth integrations available for all three framework options; zero password management |
| D — Shared player token in URL | Each player receives a unique URL token (e.g., `/access?token=abc123`); token validates in server middleware | None | Trivial; no login flow; token can be forwarded/shared accidentally; no true session management |

[DECISION-12]: Select authentication approach. Recommended: Option C (Discord OAuth) if all 6 players have Discord accounts — zero password management, strong identity, Auth.js integration available for all three framework options. If Discord is not universal, Option A (passphrase per player) is the simplest self-contained alternative. Option D is convenient but has meaningful sharing risk.

**Offline / PWA considerations:**
Players at a physical table may have intermittent connectivity. The companion app's primary in-session use case is character reference (reading stats, checking resource pools) rather than editing. Editing is primarily a between-session activity.

[DECISION-13]: Is offline read access to character sheets required during sessions? If yes: implement a service worker that caches the last-fetched character sheet JSON response; no database replication needed; sheets render from cache when offline; writes are queued and sent when connectivity returns (requires service worker background sync). If no: companion app is online-only; players without connectivity consult Roll20 directly. Offline support adds meaningful implementation complexity — scope it as a Phase 2 iteration of the companion app, not MVP, unless the primary use case requires it.

---

### Task 5.5 — Security Model

**Component:** The security posture governing token storage, access control, and data protection for the full Roll20 ↔ Turso ↔ companion app system

**Threat model assessment for this specific use case:**
- Data sensitivity: character stat blocks are neither financial data nor personally identifiable information beyond a display name. The damage of a full data exposure is: someone sees fictional character stats for a TTRPG campaign. This is low-sensitivity.
- Actor profile: 6 known, trusted players + 1 GM. Not a public product; not accessible to anonymous internet users unless the Turso database is misconfigured.
- Primary threat: accidental misuse — a player inadvertently overwrites another player's character data, or a leaked Roll20 sync token enables a player to send malformed writes to Turso. Adversarial attacks are out of scope for this threat model.
- Secondary concern: Turso database exposure — if the auth token is broadly accessible, an external party could write to the database. Mitigated by Turso token scoping (write-only, single-database).

**Roll20 sync token security:**

The Roll20 Sheet Worker requires an auth credential to write to Turso (or to a proxy). The placement options and their implications:

| Placement | Visibility | Blast radius | Viability |
|---|---|---|---|
| Hardcoded in Sheet Worker JavaScript | Any player viewing page source in browser dev tools | Full write access to the entire Turso database | Unacceptable — never use |
| Sheet attribute (`turso_auth_token`) | All players with the Roll20 sheet open can read sheet attributes | Write access scoped to whatever permissions the token has | Acceptable only with a strictly scoped token (write-only to one database); still visible to all 6 players |
| GM-only Roll20 hidden field | GM only; Roll20 does not render GM-only fields to non-GM players | Same as above; smaller audience | Better posture for a trusted group; depends on Roll20's GM-only field implementation being consistent |
| Proxy function (Cloudflare Worker / Vercel Edge Function) | Sheet Worker sees only the proxy URL + a lightweight shared secret (`campaign_secret` header); the real Turso token lives in the proxy's environment variables and is never transmitted to the browser | Proxy can enforce: (a) only known campaign_id values are accepted, (b) payload structure is validated before forwarding to Turso | Best security posture; adds one infrastructure component to maintain |

**Recommended security posture for this use case:**
Primary recommendation: proxy function (Cloudflare Worker free tier is sufficient — 100,000 requests/day; a 6-player game will never approach this limit). The proxy holds the Turso write token in environment variables. The Sheet Worker sends the sync payload to the proxy endpoint with a `campaign_secret` value (a random string, not cryptographic strength — sufficient to prevent casual misuse from outside the group). The proxy validates that `campaign_id` matches the known campaign and that the `character_id` is a valid member of that campaign before forwarding the write to Turso.

Acceptable minimum (if proxy infra is unacceptable): GM-only hidden Roll20 field storing a Turso token with strictly scoped permissions. This token must be write-only (`INSERT` / `UPDATE` only), scoped to the campaign's single Turso database. A player who obtains this token could overwrite character data — accepted risk for a 6-person trusted group where the GM controls Roll20 access. At no point can this token be used to read data (separate read token lives only in the companion app's server-side runtime).

The distinction matters: two separate Turso tokens are required:
- **Sync token** (for Roll20 Sheet Worker / proxy): write-only, scoped to the campaign database
- **App token** (for companion app server-side): read+write, scoped to the campaign database; lives in companion app environment variables only; never transmitted to the browser

**Companion app access control:**
All write paths in the companion app enforce ownership at the server-side handler level before any Turso write executes:
- Scalar field edits: verify `characters.player_id === auth.player_id` before writing; reject if mismatch
- Repeating section row edits: same ownership check (the row belongs to a character that belongs to the authenticated player)
- GM routes (`/gm`, `/gm/[id]`): verify `players.is_gm === 1` for the authenticated player; reject if not GM
- The `is_gm` flag on the `players` table is set by the GM directly in Turso during campaign setup; it is not self-assignable via any app route

[DECISION-14]: Confirm proxy function vs. GM-only hidden field for Roll20 sync token storage. If proxy function is selected, confirm which serverless platform (Cloudflare Workers recommended for zero-cost tier; Vercel Edge Functions as alternative).

[DECISION-15]: Should the GM have write access to any character through the companion app? The current access control model restricts writes to character owners only. If the GM needs the ability to adjust damage, karma, or other fields during a session recap via the companion app, the model expands to "owner OR is_gm can write." Define which fields (if any) the GM can write; or permit full write access to all characters for the GM role.

---

### Task 5.6 — Sync State & Conflict Resolution

**Component:** The strategy for detecting and resolving state divergence between Roll20 and Turso

**Divergence scenarios for this system:**

1. **Offline edit → late sync:** Player edits character in Roll20 during a session with no internet. Regains connectivity after session. Pushes sync. Companion app had been showing the old pre-session state. After sync, Turso reflects the post-session state. No conflict — this is sequential.

2. **Companion app edit + Roll20 not pulled:** Player edits a field in the companion app between sessions. Opens Roll20 for the next session. Has not pulled from Turso. Rolls using stale attribute values.

3. **Simultaneous edits:** Player has Roll20 open. GM opens the companion app and edits the same character (if GM write access is enabled — see Task 5.5 [DECISION]). Both make changes. One pushes first; the other's push is a conflict.

4. **Multiple Roll20 windows:** A player opens their character sheet in two browser tabs. Both are the same Roll20 sheet — Roll20's own sync handles this. This is not a Turso conflict scenario.

**Conflict resolution strategy options:**

| Strategy | Description | Implementation complexity | Appropriateness |
|---|---|---|---|
| Last-write-wins (wall clock) | The write with the later `updated_at` timestamp wins; earlier write is silently overwritten | Low | Risk: client clocks across Roll20 browser + companion app browser may differ by seconds or minutes; non-deterministic |
| Last-write-wins (sync_version) | Monotonic integer incremented on every write; higher version wins regardless of clock | Low | Deterministic; no clock skew; recommended |
| Roll20-always-authoritative | Turso is always overwritten by Roll20 sync; Turso is never the authoritative source | Trivial (no conflict logic needed) | Only valid if companion app is read-only (see Task 5.3 [DECISION]) |
| Manual merge on conflict | Surface a diff to the player on conflict detection; player resolves field-by-field | High | Not appropriate for a casual group; overengineered for this scale |

**Recommended strategy: `sync_version` last-write-wins.**
- On every Roll20 push: payload includes `sync_version_from` (the sheet's current `char_sync_version`). The write succeeds if Turso's current `sync_version` matches or is lower. (The "or is lower" case covers Turso rollback or failed-increment scenarios — it is defensive and expected to be rare in practice.) After a successful write, Turso's `sync_version` is incremented by 1. The sheet updates its `char_sync_version` to match.
- On every companion app write: same logic — server-side handler reads current `sync_version`, writes with incremented value.
- On Roll20 pull: the sheet updates `char_sync_version` to the value received from Turso.

**Conflict behavior on Roll20 push (when Turso's version is ahead of the sheet's version):**

| Option | Behavior | Recommended |
|---|---|---|
| A — Roll20 overwrites unconditionally | Ignore the conflict; write proceeds; Turso version is incremented | Simplest; Roll20 is the primary edit surface; companion app edits during an active session are overwritten |
| B — Sync fails with notification | Push is rejected if Turso version > payload version; Sheet Worker emits a chat message: "Sync conflict — pull from DB first, then re-sync" | Safer for bidirectional sync; player is informed of lost companion app edits |

[DECISION-16]: On sync_version conflict (Turso is newer than the sheet's last-known version), should Roll20 overwrite Turso unconditionally (Option A), or should the sync fail and require a pull-then-resync cycle (Option B)? Recommended: Option B if bidirectional sync is confirmed; Option A if Roll20 is the authoritative source and companion app edits are secondary.

**`sync_version` lifecycle summary:**

| Event | sync_version change |
|---|---|
| Character creation in Turso | Set to 0 |
| Successful Roll20 push | Turso: incremented by 1; Roll20 sheet `char_sync_version`: set to new Turso value |
| Successful companion app write | Turso: incremented by 1 |
| Successful Roll20 pull | Roll20 sheet `char_sync_version`: updated to Turso's current value |
| Conflicted Roll20 push (Option B behavior) | No change to either; push rejected |

**`char_sync_version` sheet attribute:** Stores the last-known Turso `sync_version` value on the Roll20 sheet side. Updated after every successful push and pull. Used as `sync_version_from` in outbound sync payload. Added to `sheet.json` as a Phase 5 amendment (non-computed INTEGER field, default 0, not displayed in the sheet UI — sync infrastructure only).

---

### Task 5.7 — Phase 5 Deliverables & Out-of-Scope Boundary

**Component:** Explicit scope contract — what this planning phase produces, what is deferred to implementation

**What Phase 5 planning produces:**

1. **Turso schema specification** — all table names, column names, column types (SQLite: INTEGER / TEXT / REAL / BLOB), primary keys, foreign keys, and index names for all campaign/player/character/repeating tables. Sufficient for a developer to write DDL independently without making structural decisions.

2. **Sync API contract** — the exact top-level JSON key structure of the outbound sync payload (Roll20 → Turso) and the inbound pull payload (Turso → Roll20), including key names, value types, and which Roll20 attribute names map to which payload keys. No code — a field mapping table is sufficient.

3. **Companion app routing plan** — the complete routes table: URL pattern, page/component purpose, authentication gate, Turso read operations, Turso write operations. Sufficient for a developer to scaffold the app structure and wire routes to the database.

4. **Security posture decision** — confirmed token storage approach (proxy vs. GM-only field), token permission scoping (write-only sync token, read+write app token), and companion app access control rules (ownership check on all write paths; GM role verification on GM routes).

5. **Conflict resolution protocol** — confirmed sync_version strategy, confirmed Roll20 conflict behavior (overwrite vs. reject), and confirmed pull-on-open guard condition.

6. **`sheet.json` Phase 5 amendment** — three new fields to add to the Phase 1 naming contract: `char_db_id` (TEXT, default ""), `char_sync_version` (INTEGER, default 0), `campaign_db_id` (TEXT, default ""). These are sync infrastructure fields; not displayed in the sheet UI; not computed by Sheet Workers.

7. **All [DECISION] items resolved** — the 16 decision points (DECISION-01 through DECISION-16) flagged in Tasks 5.1–5.6 are answered by the system owner and recorded in the plan before implementation authorization is given.

**What is explicitly deferred (not in Phase 5 planning scope):**

- Turso database creation, configuration, and credential management
- Writing DDL (CREATE TABLE statements) for the schema
- Roll20 Sheet Worker sync code (fetch calls, payload construction, setAttrs logic, error handling)
- Proxy/serverless function implementation
- Companion app scaffolding, folder structure, component code, form components
- Authentication provider setup (Discord OAuth app, email service configuration, etc.)
- Deployment pipeline and hosting configuration for the companion app
- Testing, QA, and end-to-end sync validation
- Companion app implementation is a **separate TEMPO workflow** triggered after Layer 5 of this Roll20 sheet workflow is complete

**Gate criterion — what must be confirmed before implementation begins:**

| Gate | Item |
|---|---|
| G1 | Roll20 campaign plan confirmed as Pro (fetch() available in Sheet Workers) |
| G2 | All 16 [DECISION] items (DECISION-01 through DECISION-16) in Tasks 5.1–5.6 answered and recorded |
| G3 | Sync directionality confirmed: bidirectional OR Roll20-only-outbound (companion read-only) |
| G4 | Frontend framework selected: SvelteKit / Next.js / Astro |
| G5 | Auth model selected: Discord OAuth / passphrase / magic link |
| G6 | Token storage confirmed: proxy function OR GM-only hidden field |
| G7 | Turso database created and both credentials (sync token, app token) available |
| G8 | `sheet.json` amended with `char_db_id`, `char_sync_version`, `campaign_db_id` (Phase 5 amendment carried into Phase 1) |

---

## Phase 5 Deliverables

1. ⬜ Turso schema specification: all table names, column names, column types, primary/foreign keys, and index names — companion app data model complete
2. ⬜ Sync API contract: outbound payload field mapping (Roll20 attribute names → Turso JSON keys) + inbound pull payload field mapping
3. ⬜ Companion app routing plan: full route table with auth gates and Turso operations per route
4. ⬜ Security posture decision: confirmed token storage approach, token scope definitions (sync-write-only, app-read+write), companion app access control rules
5. ⬜ Conflict resolution protocol: confirmed sync_version model + Roll20 conflict behavior (overwrite vs. reject)
6. ⬜ sheet.json Phase 5 amendment: `char_db_id`, `char_sync_version`, `campaign_db_id` added to Phase 1 field contract
7. ⬜ All [DECISION] items answered and recorded; zero unresolved planning decisions

## Phase 5 Success Criteria

- [ ] Turso schema supports all 3 query patterns: by player, by character, by campaign — without full-table scans
- [ ] Schema uses only SQLite-compatible types (INTEGER, TEXT, REAL, BLOB) — no PostgreSQL-isms
- [ ] Sync payload field list covers all ~150 scalar attributes; computed fields explicitly excluded with rationale
- [ ] All 7 repeating sections covered in sync payload structure
- [ ] Outbound sync trigger model confirmed; rationale documented
- [ ] Inbound sync strategy confirmed: bidirectional or read-only companion app
- [ ] Roll20 fetch() availability confirmed (Pro plan gate: G1)
- [ ] Auth model selected; player identity and GM identity model described
- [ ] Security posture confirmed: no hardcoded tokens in Sheet Worker JS under any circumstance
- [ ] Conflict resolution strategy confirmed: sync_version model or Roll20-authoritative fallback
- [ ] GM role defined: view-only or write-enabled for character edits in companion app
- [ ] All 16 [DECISION] items (DECISION-01 through DECISION-16) resolved before implementation authorization
- [ ] `char_db_id`, `char_sync_version`, `campaign_db_id` added to sheet.json Phase 5 amendment
- [ ] Companion app implementation scope clearly delineated as a separate TEMPO workflow

---

*Phase 5 planning complete — 16 [DECISION] items (DECISION-01 through DECISION-16) flagged for system owner resolution before implementation begins. Companion app implementation is a separate TEMPO workflow, gated on all decisions above being resolved.*


---

## Phase 5 Amendments (Post-Review — 2026-03-28)

*Applied corrections from Tempo Reviewer PASS WITH NOTES verdict. FINDINGS 1, 2, and 8 resolved via inline edits above. The following amendments address FINDINGS 3–7, 9–10.*

---

### Amendment 5-A — Turso Write Semantics for Repeating Sections (FINDING-3)

**Finding:** The outbound sync contract specified "full sync, never a delta patch" but never defined what the Turso write handler must do with repeating section rows that exist in Turso but are absent from the new payload. An UPSERT-only implementation would accumulate ghost rows (deleted Roll20 skills, weapons, etc.) in Turso indefinitely; the next inbound pull would re-inject them into Roll20.

**Resolution — Outbound Turso write contract for repeating sections:**

For each of the 7 `rep_*` tables (`rep_skills`, `rep_spells`, `rep_mutations`, `rep_adept_powers`, `rep_weapons`, `rep_equipment`, `rep_contacts`), the Turso write handler MUST use a truncate-and-reload strategy:

1. DELETE all existing rows WHERE `character_id` = payload `character_id` for that section table
2. INSERT all rows from the payload array for that section

This mirrors the inbound "clear then re-insert" strategy in Task 5.3 and ensures Turso's `rep_*` tables never accumulate deleted rows.

**Atomicity requirement (see Amendment 5-E):** All DELETE + INSERT statements across all 7 section tables, plus the scalar UPSERT on `character_scalars`, must execute within a single Turso pipeline transaction. If any statement fails, all statements roll back.

---

### Amendment 5-B — Cross-Phase Amendment Declarations (FINDING-4)

**Finding:** Phase 5 introduces new HTML elements (Sync button, Pull button, sync status label) and new Sheet Worker handlers (clicked:btn_sync_db, clicked:btn_pull_db, sheetOpens auto-pull guard), but no corresponding Phase 2 or Phase 3 amendment was declared. The existing Phase 2 and Phase 3 deliverables are incomplete without these additions.

**Resolution — Phase 2 HTML Amendment (Phase 5 carry-forward):**

Add a sync infrastructure row to the Core tab HTML (Task 2.2), positioned below the Combat Panel and before the tab footer:

- `btn_sync_db` — Roll20 roll button (`<button type="action">`) labelled "Sync to DB"; triggers the outbound Sheet Worker handler; confirmation that this fires `clicked:btn_sync_db` without initiating a dice roll must be verified (Sandbox Verification item 5-SV1)
- `btn_pull_db` — Roll20 roll button (`<button type="action">`) labelled "Pull from DB"; triggers the inbound pull handler
- `sync_status` (conditional on DECISION-07 error feedback option) — read-only text display of last sync state (e.g., "Synced ✓ — 2025-03-28 18:42"); rendered via a `<span>` or `<input type="text" readonly>` bound to `attr_sync_status`
- `char_db_id`, `char_sync_version`, `campaign_db_id` — `<input type="hidden">` elements; not displayed in the sheet UI; required for Sheet Workers to read and write via `getAttrs()`/`setAttrs()`

**Resolution — Phase 3 Sheet Worker Amendment (Phase 5 carry-forward):**

Add to the Sheet Worker implementation spec (Task 3.x) the following new handlers:

1. **`on('clicked:btn_sync_db', ...)`** — Outbound sync handler: calls `getAttrs()` for all ~150 scalar fields + all 7 repeating sections, constructs the full sync payload (see Task 5.2 payload structure), calls `fetch()` to the proxy or Turso HTTP API, updates `char_sync_version` on success, writes `sync_status` feedback attribute.

2. **`on('clicked:btn_pull_db', ...)`** — Inbound pull handler: fetches full character payload from Turso using `char_db_id`, runs the "clear then re-insert" strategy across all 7 repeating sections (see Task 5.3), calls `setAttrs({silent: true})` for scalar fields, triggers K-scaffold cascade update for computed fields, updates `char_sync_version` to Turso's current value.

3. **Extend `k.sheetOpens` handler** — Add auto-pull guard: if `char_db_id !== ""`, run the inbound pull handler on sheet open. If `char_db_id === ""`, skip silently. This guard extends the existing `k.sheetOpens` registration in the Phase 3 worker; it does not replace it.

---

### Amendment 5-C — Sandbox Verification Items (FINDING-5)

**Finding:** `removeRepeatingRow()` availability via K-scaffold and the row-creation-by-setAttrs behavior are both critical inbound sync assumptions. Neither was flagged as a sandbox verification item, unlike the other 11 sandbox tests documented in Phase 4.

**Resolution — Add to Phase 4 Pre-Implementation Sandbox Verification Checklist:**

| ID | Test | Expected Result |
|---|---|---|
| 5-SV1 | Fire `clicked:btn_sync_db` from a `<button type="action">` element; confirm the Sheet Worker `on('clicked:btn_sync_db', ...)` handler fires WITHOUT triggering a dice roll in chat | Handler fires; no roll output; action button confirmed viable for non-roll triggers |
| 5-SV2 | Call K-scaffold's `removeRepeatingRow(rowId)` for a known repeating section row; confirm the row is removed from the Roll20 sheet DOM and that no error is thrown in the Sheet Worker console | Row removed; K-scaffold wrapper confirmed to expose this function |
| 5-SV3 | Call `setAttrs({ 'repeating_skills_-NEWTESTID_skill_name': 'TestSkill' })` where `-NEWTESTID` is a row ID that does not currently exist in the sheet; confirm a new row is created with that exact row ID | New row created; setAttrs-based row creation confirmed in K-scaffold context |

---

### Amendment 5-D — Conditional Attributes in sheet.json Table (FINDING-6)

**Finding:** Two conditionally-required attributes (`turso_auth_token` and `sync_status`) were absent from the new attributes table in Task 5.2, even though they are required fields depending on DECISION-06 and DECISION-07 outcomes respectively.

**Resolution — Extend the new attributes table in Task 5.2:**

| Attribute name | Type | Default | Purpose | Condition |
|---|---|---|---|---|
| `char_db_id` | TEXT | `""` | Turso character UUID | Always required |
| `char_sync_version` | INTEGER | `0` | Last-known Turso sync_version | Always required |
| `campaign_db_id` | TEXT | `""` | Turso campaign UUID | Always required |
| `turso_auth_token` | TEXT | `""` | Turso write-only sync token or shared proxy secret | Required only if **DECISION-06** selects "sheet attribute" or "GM-only hidden field" token placement. Not needed if proxy function stores the token server-side. |
| `sync_status` | TEXT | `"Never synced"` | Last sync result displayed on Core tab | Required only if **DECISION-07** selects Option A (persistent label). Not needed if Option B (chat-only) or Option C (silent) is selected. |

---

### Amendment 5-E — Atomic Transaction Mandate for Outbound Writes (FINDING-9)

**Finding:** The outbound sync writes up to 15+ SQL statements (scalar UPSERT + 7 × DELETE + 7 × INSERT for repeating sections). If any statement fails after earlier statements have committed, Turso is left in a partially-written inconsistent state. A subsequent inbound pull would re-populate Roll20 with a half-updated dataset.

**Resolution — Add to Task 5.2 outbound sync contract:**

> **Atomicity requirement:** All SQL statements for a single payload write — the scalar `character_scalars` UPSERT plus all 7 section DELETE-then-INSERT sequences — MUST execute within a **single Turso pipeline transaction**. If any statement fails, all statements roll back. Turso's HTTP pipeline API (`POST /pipeline`) supports batched transactions; the proxy or direct-Turso write handler must use this mechanism. A partial write (e.g., scalar blob updated but `rep_weapons` rows not inserted) must never be committed as a valid state.

This requirement applies to the companion app's scalar+repeating write path (Task 5.4) identically — all section writes for a single character save must execute in a single transaction.

---

### Amendment 5-F — Parameterized Query Mandate (FINDING-10, OWASP A03)

**Finding:** The security model (Task 5.5) documented token storage and access control but did not state the SQL injection baseline. Companion app form inputs (character names, bio answers Q01–Q20) are user-controlled strings that flow into Turso writes. String-interpolated SQL with these values is an injection vector.

**Resolution — Add to Task 5.5 security model:**

> **SQL injection prevention (OWASP A03):** All Turso read and write operations in the companion app MUST use the `@libsql/client` parameterized query interface. No SQL string concatenation with user-supplied values is permitted under any circumstance. This applies to: character name lookups, scalar blob writes (JSON.stringify output passed as a parameter), all `rep_*` table row inserts/updates/deletes, and all WHERE clause values derived from route parameters (character ID, player ID). The `@libsql/client` library's `.execute({ sql: '...?...', args: [...] })` syntax is the required pattern. The proxy function (Amendment 5-A) enforces the same constraint on any SQL statement it constructs.

---

### Amendment 5-G — Proxy Secret Transparency Note (FINDING-7)

**Finding:** The Task 5.5 proxy security analysis described the Cloudflare Worker as ensuring "the real Turso token lives in the proxy's environment variables and is never transmitted to the browser," but did not state that the `campaign_secret` sent by the Sheet Worker is itself stored as a Roll20 sheet attribute — readable by all 6 players. The proxy's security benefit is specifically that the Turso write token is not transmitted, not that the shared proxy credential is private.

**Resolution — Add clarifying note to Task 5.5 proxy analysis:**

> **Proxy security scope clarification:** The `campaign_secret` value sent by the Sheet Worker to the proxy is stored as a Roll20 sheet attribute (`attr_turso_auth_token` or a dedicated `attr_campaign_secret`). This value is readable by all players with the sheet open, in the same way the Turso token would be if stored directly. The proxy's security benefit is **specifically** that the real Turso write token is never transmitted to the browser — not that the proxy credential is private from the 6 players. A player with knowledge of the `campaign_secret` and the proxy URL could craft write requests for any character in the campaign. Under the stated threat model (6 known trusted players, no adversarial actors), this is an accepted residual risk. Document this clearly in the companion app's technical README.

---

*Phase 5 amendments complete. All 10 Reviewer findings addressed: FINDINGS 1–2 resolved via inline edits; FINDINGS 3–10 resolved via Amendments 5-A through 5-G above.*


---

## Phase 5 DECISION Resolutions — 2026-03-28

### Resolved by system owner

---

**[DECISION-08] RESOLVED — Read-only companion app (V1)**
Companion app is read-only in V1. Roll20 is the exclusive edit surface. The companion app displays character data fetched from Turso but has no write path. Bidirectional sync (Tasks 5.3, 5.6 inbound strategy) is deferred to the companion app V2 TEMPO workflow.

*Cascades:*
- **DECISION-09** (clear-and-reinsert on inbound pull): **N/A — no inbound sync in V1**
- **DECISION-11** (auto-save vs form-level submit): **N/A — no edit forms in V1**
- **DECISION-16** (conflict behavior on sync conflict): **N/A — companion app cannot write; no conflict possible in V1**
- Task 5.3 (Turso → Roll20 inbound sync): deferred to V2; no Pull button, no sheetOpens auto-pull in V1
- Amendment 5-B Phase 3 Sheet Worker additions: `on('clicked:btn_pull_db', ...)` and `k.sheetOpens` auto-pull guard deferred to V2
- Conflict resolution model (Task 5.6): `sync_version` still maintained on outbound push for V2 readiness; Turso stores it, Roll20 updates `char_sync_version` after each successful push; no conflict detection logic required in V1

---

**[DECISION-10] RESOLVED — SvelteKit**
Frontend framework: SvelteKit with `@libsql/client`. Server-side form actions (read-only in V1: server load functions only), deploys to Cloudflare Pages (co-located with the Cloudflare Worker proxy from DECISION-14).

---

**[DECISION-12] RESOLVED — Discord OAuth**
Authentication model: Discord OAuth (Option C). The campaign has an active Discord server — all 6 players have Discord accounts. Auth.js (formerly NextAuth) SvelteKit adapter handles the OAuth flow. Player identity in Turso is linked to Discord user ID stored in `players.auth_credential`.

*Cascades:*
- **DECISION-02** (`auth_credential` column): TEXT column stores Discord user ID (stable, unique per Discord account). No hashing required — Discord user IDs are non-secret public identifiers. Session token issued by Auth.js after OAuth flow; never stored in Turso.

---

**[DECISION-14] RESOLVED — Proxy function (Cloudflare Workers)**
Roll20 sync token storage: Cloudflare Worker proxy (free tier: 100,000 requests/day, well above game volume). The Turso write-only sync token lives exclusively in Cloudflare Worker environment variables. The Sheet Worker sends the sync payload to the proxy URL with a `campaign_secret` shared value (see Amendment 5-G for scope clarification).

*Cascades:*
- **DECISION-06** (token placement): Resolved — proxy function. No `turso_auth_token` sheet attribute required. Companion app retains its own read+write app token in server-side SvelteKit environment only (Cloudflare Pages env vars).
- Conditional attribute `turso_auth_token` from Amendment 5-D: **not needed** — proxy holds the token. Remove from conditional attributes table.

---

**[DECISION-15] RESOLVED — No GM-only functionality in V1**
The companion app does not implement a separate GM role or GM dashboard in V1. All authenticated players see their own characters only. The `/gm` and `/gm/[id]` routes are removed from the V1 routing plan. The `players.is_gm` column is retained in the schema for V2 extensibility but not used for access control in V1.

*Revised routing plan (V1):*

| Route | Purpose | Auth gate | Turso operations |
|---|---|---|---|
| `/` | Landing page; redirect authenticated users to `/characters` | None (public) | None |
| `/login` | Discord OAuth entry point | None | None (Auth.js handles) |
| `/auth/callback` | Discord OAuth callback handler | None | Upsert into players on first login |
| `/characters` | List all characters owned by authenticated player | Authenticated | Read characters WHERE player_id = auth.player_id |
| `/characters/[id]` | Full character sheet — read-only view | Owner of character | Read character_scalars + all 7 rep tables for character [id] |
| `/logout` | Clear session | Authenticated | None |

Routes removed from V1 (deferred): `/characters/new` (no Roll20-independent character creation), `/characters/[id]/edit` (no write path), `/gm`, `/gm/[id]`.

---

### Group B defaults confirmed (remaining decisions)

The following decisions default to the recommended values as specified in the plan. System owner has reviewed and no objection has been raised:

| Decision | Resolution |
|---|---|
| DECISION-01 | Hybrid schema confirmed: Option C (JSON blob scalars) + Option D (per-section rep tables) |
| DECISION-03 | Roll20 Pro confirmed — `fetch()` available in Sheet Workers |
| DECISION-04 | Manual sync trigger (Option C: "Sync to DB" button) confirmed; Option D (debounced idle batch) deferred to V2 |
| DECISION-05 | Exclusion list confirmed: all computed/worker-only fields excluded; `init_dice` and `bio_q01`–`bio_q20` included in sync payload |
| DECISION-07 | Error feedback confirmed: Option B (Roll20 chat message on failure) + Option A (persistent `sync_status` label on Core tab) |
| DECISION-13 | Offline/PWA: post-MVP; companion app V1 is online-only |

---

### Updated gate checklist (post-resolution)

| Gate | Item | Status |
|---|---|---|
| G1 | Roll20 Pro confirmed (fetch() available) | ✅ RESOLVED |
| G2 | All 16 DECISION items answered | ✅ RESOLVED — see resolutions above |
| G3 | Sync directionality: Roll20-outbound only (read-only companion app V1) | ✅ RESOLVED |
| G4 | Frontend framework: SvelteKit | ✅ RESOLVED |
| G5 | Auth model: Discord OAuth via Auth.js | ✅ RESOLVED |
| G6 | Token storage: Cloudflare Worker proxy | ✅ RESOLVED |
| G7 | Turso database created; Cloudflare Worker deployed; both tokens available | ⏳ Implementation-time |
| G8 | `sheet.json` amended with `char_db_id`, `char_sync_version`, `campaign_db_id` | ⏳ Implementation-time |

**Phase 5 planning complete. Layer 2 operational planning complete. All phases approved and all decisions resolved. Ready for Layer 3.**
