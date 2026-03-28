# Layer 3 — Technical Blueprints: roll20_character_sheet

*Layer 3 produces structural blueprints and annotated skeletons. No production code. Sufficient for a Developer to implement without making architectural decisions.*

---

## Phase 1 — sheet.json + Naming Contract Blueprint

**Goal:** Produce the complete specification for `sheet.json` and the Roll20 attribute naming contract. After this phase a Developer has everything needed to produce the final `sheet.json` without making any structural or naming decisions.

**Input:** Layer 2 Phase 1–5 operational plan (all phases + all amendments), fully cross-referenced.

**Phase 1 does NOT cover:** HTML structure, Sheet Worker code, CSS, companion app. Those are Phases 2–5.

---

### Section 1: sheet.json Top-Level Metadata Skeleton

The `sheet.json` file is the K-scaffold configuration manifest. The complete top-level skeleton:

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
    { "name": "tab-core",   "label": "Core"   },
    { "name": "tab-skills", "label": "Skills" },
    { "name": "tab-magic",  "label": "Magic"  },
    { "name": "tab-gear",   "label": "Gear"   },
    { "name": "tab-bio",    "label": "Bio"    }
  ],
  "templates": [
    "skill",
    "attack",
    "spell"
  ],
  "attributes": [ ... ]
}
```

**Top-level field notes:**

| Field | Value | Notes |
|---|---|---|
| `html` | `"sheet.html"` | Must match the uploaded HTML file name exactly |
| `css` | `"sheet.css"` | Must match the uploaded CSS file name exactly |
| `authors` | project placeholder | Replace with real author name before publishing |
| `roll20_authors` | `""` | Roll20 marketplace username — leave blank for private game |
| `preview` | `"preview.png"` | Screenshot used in Roll20's sheet browser; create before upload |
| `instructions` | one-line string | Displayed in Roll20 sheet builder; brief description is sufficient |
| `legacy` | `false` | `true` disables beacon/new Roll20 features; set `false` for K-scaffold |
| `tabs` | 5 entries | Tab names are CSS slug identifiers matching `.sheet-tab-panel-{name}` classes |
| `templates` | 3 entries | Roll template suffix names — referenced in buttons as `&{template:skill}` etc. |
| `attributes` | full array | See Section 2 — this is the core of the file |

[CARRY-FORWARD NOTE — tabs key]: The `tabs` and `templates` keys are not part of standard Roll20's published `sheet.json` schema. Verify whether your version of K-scaffold expects these keys or ignores them. Standard Roll20 sheet.json only requires `html`, `css`, `authors`, `roll20_authors`, `preview`, `instructions`, and `legacy`. K-scaffold may extend this; consult K-scaffold version docs.

---

### Section 2: Full Attribute Registry

**Conventions:**
- `name`: bare attribute name — no `attr_` prefix in this table. See Section 6 (Developer Guidance) for the K-scaffold prefix convention decision.
- `type`: Roll20 input type — `"number"` | `"text"` | `"checkbox"` | `"hidden"`
- `default`: value Roll20 sets on new sheet creation. Integer fields → `0`; text fields → `""`; exceptions noted. Computed/worker_only fields default `0`.
- `worker_only: true` = field is set exclusively by Sheet Workers; never directly edited by the player; still requires an HTML input element (hidden or read-only)
- `max`: typically `""` (no maximum enforced) unless noted

---

#### Group 1 — Core Attribute Base Values (8 fields)

Player-entered raw scores before any modifiers.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `body_base` | number | 0 | false | Player-entered Body base score |
| `dex_base` | number | 0 | false | Player-entered Dexterity base score |
| `str_base` | number | 0 | false | Player-entered Strength base score |
| `cha_base` | number | 0 | false | Player-entered Charisma base score |
| `int_base` | number | 0 | false | Player-entered Intelligence base score |
| `wil_base` | number | 0 | false | Player-entered Willpower base score |
| `hum_base` | number | 0 | false | Player-entered Humanity base score |
| `mag_base` | number | 0 | false | Player-entered Magic rating base; 0 = non-magical character |

---

#### Group 2 — Core Attribute Mutation Sub-values (7 fields — `mag` excluded)

Bonuses to core attributes from mutations. `mag` has no `_mutations` sub-field per Phase 1 exception.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `body_mutations` | number | 0 | false | Body bonus from mutations |
| `dex_mutations` | number | 0 | false | Dexterity bonus from mutations |
| `str_mutations` | number | 0 | false | Strength bonus from mutations |
| `cha_mutations` | number | 0 | false | Charisma bonus from mutations |
| `int_mutations` | number | 0 | false | Intelligence bonus from mutations |
| `wil_mutations` | number | 0 | false | Willpower bonus from mutations |
| `hum_mutations` | number | 0 | false | Humanity bonus from mutations |

---

#### Group 3 — Core Attribute Magic Sub-values (7 fields — `mag` excluded)

Magic-granted bonuses to core attributes. `mag` has no `_magic` sub-field (would be circular).

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `body_magic` | number | 0 | false | Body bonus from magic |
| `dex_magic` | number | 0 | false | Dexterity bonus from magic |
| `str_magic` | number | 0 | false | Strength bonus from magic |
| `cha_magic` | number | 0 | false | Charisma bonus from magic |
| `int_magic` | number | 0 | false | Intelligence bonus from magic |
| `wil_magic` | number | 0 | false | Willpower bonus from magic |
| `hum_magic` | number | 0 | false | Humanity bonus from magic |

---

#### Group 4 — Core Attribute Misc Modifiers (8 fields — all attributes including `mag`)

Catch-all modifiers not covered by mutations or magic (equipment, conditions, temporary effects).

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `body_misc` | number | 0 | false | Miscellaneous Body modifier |
| `dex_misc` | number | 0 | false | Miscellaneous Dexterity modifier |
| `str_misc` | number | 0 | false | Miscellaneous Strength modifier |
| `cha_misc` | number | 0 | false | Miscellaneous Charisma modifier |
| `int_misc` | number | 0 | false | Miscellaneous Intelligence modifier |
| `wil_misc` | number | 0 | false | Miscellaneous Willpower modifier |
| `hum_misc` | number | 0 | false | Miscellaneous Humanity modifier |
| `mag_misc` | number | 0 | false | Miscellaneous Magic modifier |

---

#### Group 5 — Core Attribute Totals (8 fields — all `worker_only: true`)

Computed total for each attribute. These are the values referenced in roll formulas (`@{body}d6`, `@{int}`, etc.) and in downstream Sheet Worker calculations.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `body` | number | 0 | true | Worker (L2): `body_base + body_mutations + body_magic + body_misc` |
| `dex` | number | 0 | true | Worker (L2): `dex_base + dex_mutations + dex_magic + dex_misc` |
| `str` | number | 0 | true | Worker (L2): `str_base + str_mutations + str_magic + str_misc` |
| `cha` | number | 0 | true | Worker (L2): `cha_base + cha_mutations + cha_magic + cha_misc` |
| `int` | number | 0 | true | Worker (L2): `int_base + int_mutations + int_magic + int_misc` |
| `wil` | number | 0 | true | Worker (L2): `wil_base + wil_mutations + wil_magic + wil_misc` |
| `hum` | number | 0 | true | Worker (L2): `hum_base + hum_mutations + hum_magic + hum_misc` |
| `mag` | number | 0 | true | Worker (L2): `mag_base + mag_misc` (no mutations/magic sub-fields) |

---

#### Group 6 — Reaction (Derived Attribute, 3 fields)

Reaction is derived from INT + DEX totals. It feeds pool_control and initiative.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `reaction_base` | number | 0 | true | Worker (L3): `Math.floor((int + dex) / 2)`. No user input. |
| `reaction_misc` | number | 0 | false | Manual reaction modifier (equipment, talent, temporary) |
| `reaction` | number | 0 | true | Worker (L3): `reaction_base + reaction_misc`; apply `Math.max(1, result)` floor to prevent 0d6 roll errors |

---

#### Group 7 — Dice Pools (12 fields)

Four pools each with: computed base + manual misc + computed total.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `pool_spell_base` | number | 0 | true | Worker (L4a): `Math.floor((cha + int + wil) / 2)`. Spell casting and summoning. |
| `pool_spell_misc` | number | 0 | false | Manual spell pool modifier |
| `pool_spell` | number | 0 | true | Worker (L4b): `pool_spell_base + pool_spell_misc`; floor at 0 |
| `pool_combat_base` | number | 0 | true | Worker (L4a): `Math.floor((dex + int + wil) / 2)`. All combat actions. |
| `pool_combat_misc` | number | 0 | false | Manual combat pool modifier |
| `pool_combat` | number | 0 | true | Worker (L4b): `pool_combat_base + pool_combat_misc`; floor at 0 |
| `pool_control_base` | number | 0 | true | Worker (L4a): `= reaction` (direct copy). Vehicle and mount control. |
| `pool_control_misc` | number | 0 | false | Manual control pool modifier |
| `pool_control` | number | 0 | true | Worker (L4b): `pool_control_base + pool_control_misc`; floor at 0 |
| `pool_astral_base` | number | 0 | true | Worker (L4a): `Math.floor((int + wil + mag) / 3)`. Astral activities. |
| `pool_astral_misc` | number | 0 | false | Manual astral pool modifier |
| `pool_astral` | number | 0 | true | Worker (L4b): `pool_astral_base + pool_astral_misc`; floor at 0 |

---

#### Group 8 — Initiative (4 fields)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `init_dice` | number | 1 | false | Number of d6s rolled for initiative; default 1 (standard human); mutations may increase |
| `init_reaction_mod` | number | 0 | false | Reaction-specific initiative bonus (talent, equipment, trait) |
| `init_misc_mod` | number | 0 | false | Miscellaneous initiative modifier |
| `init_score` | number | 0 | true | Worker (L4c): `reaction + init_reaction_mod + init_misc_mod`. Roll: `@{init_dice}d6 + @{init_score}` (plain sum — NOT success-counting; no `cs`/`cf` modifiers on initiative) |

---

#### Group 9 — Condition Monitors (6 fields)

Damage level integers drive the computed TN/Init modifiers. Penalty tier: 0=clean, 1=Light(+1TN/-1Init), 2=Moderate(+2TN/-2Init), 3=Serious(+3TN/-3Init), 4=Deadly(treat as 3 for penalty; narratively incapacitated), 5=Unconscious (Stun/Physical tracks only).

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `cm_mental` | number | 0 | false | Mental damage level: 0–4 (no Unconscious on mental track) |
| `cm_stun` | number | 0 | false | Stun damage level: 0–5 (5 = Unconscious) |
| `cm_physical` | number | 0 | false | Physical damage level: 0–5 (5 = Unconscious; overflow in separate field) |
| `cm_physical_overflow` | number | 0 | false | Overflow damage boxes beyond Deadly on Physical track |
| `cm_tn_mod` | number | 0 | true | Worker (L6): `Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))` where `penaltyOf = lvl => Math.min(lvl, 3)`. Range: 0–3. |
| `cm_init_mod` | number | 0 | true | Worker (L6): `= -1 * cm_tn_mod`. Range: 0 to -3. (Both fire on same trigger set as cm_tn_mod.) |

---

#### Group 10 — Character Identity (6 fields)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `char_name` | text | `""` | false | Character display name; surfaced in roll template `{{charname=@{char_name}}}` |
| `char_race_station` | text | `""` | false | Race and social station (e.g., "Human / Serf") |
| `char_sex` | text | `""` | false | Character sex or gender |
| `char_age` | text | `""` | false | Character age |
| `char_description` | text | `""` | false | Physical description; bound to textarea in Bio tab |
| `char_notes` | text | `""` | false | General notes; bound to textarea in Bio tab |

---

#### Group 11 — Karma (4 fields)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `karma_good` | number | 0 | false | Good karma accumulated |
| `karma_used` | number | 0 | false | Karma spent |
| `karma_total` | number | 0 | true | Worker (L6): `karma_good + karma_used`. Simple sum — no flooring. |
| `karma_pool` | number | 0 | false | Player-tracked karma pool (separate resource; not computed) |

---

#### Group 12 — Encumbrance (2 fields)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `ep_total` | number | 0 | true | Worker (L5): sum of `weapon_ep` across all `repeating_weapons` rows + `equip_ep` across all `repeating_equipment` rows. Uses K-scaffold repeating section iteration. |
| `ep_max` | number | 0 | true | Worker (L5): `Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)`. Triggers on `str`, `body`. |

---

#### Group 13 — Armor Inputs (12 fields — 3 locations × 4 sub-fields each)

3 armor locations: Torso, Legs, Head. 4 sub-fields each: name (text), Piercing (number), Slashing (number), Impact (number).

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `armor_torso_name` | text | `""` | false | Name/description of torso armor piece |
| `armor_torso_piercing` | number | 0 | false | Torso armor rating vs. Piercing damage |
| `armor_torso_slashing` | number | 0 | false | Torso armor rating vs. Slashing damage |
| `armor_torso_impact` | number | 0 | false | Torso armor rating vs. Impact damage |
| `armor_legs_name` | text | `""` | false | Name/description of leg armor piece |
| `armor_legs_piercing` | number | 0 | false | Leg armor rating vs. Piercing damage |
| `armor_legs_slashing` | number | 0 | false | Leg armor rating vs. Slashing damage |
| `armor_legs_impact` | number | 0 | false | Leg armor rating vs. Impact damage |
| `armor_head_name` | text | `""` | false | Name/description of head armor piece |
| `armor_head_piercing` | number | 0 | false | Head armor rating vs. Piercing damage |
| `armor_head_slashing` | number | 0 | false | Head armor rating vs. Slashing damage |
| `armor_head_impact` | number | 0 | false | Head armor rating vs. Impact damage |

---

#### Group 14 — Armor Totals (3 fields — `worker_only: true`)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `armor_total_piercing` | number | 0 | true | Worker (L5): `armor_torso_piercing + armor_legs_piercing + armor_head_piercing` |
| `armor_total_slashing` | number | 0 | true | Worker (L5): `armor_torso_slashing + armor_legs_slashing + armor_head_slashing` |
| `armor_total_impact` | number | 0 | true | Worker (L5): `armor_torso_impact + armor_legs_impact + armor_head_impact` |

---

#### Group 15 — Magic / Adept Power Tab Scalars (6 fields)

Sheet-level fields for the Magic tab. Not per-row — the per-row field `power_pp_cost_value` lives in the `repeating_adept_powers` schema (Section 3).

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `power_points_max` | number | 0 | true | Worker (L5): `= mag`. Magic rating equals maximum Power Points. |
| `power_points_used` | number | 0 | true | Worker (L5): `parseFloat` sum of `power_pp_cost_value` across all `repeating_adept_powers` rows (decimal arithmetic — PP costs may be 0.25, 0.5, etc.) |
| `power_points_remaining` | number | 0 | true | Worker (L5): `power_points_max - power_points_used` |
| `spells_sustained` | number | 0 | false | Player-tracked count of currently sustained spells (0–10 range; no hard cap enforced) |
| `sustained_tn_mod` | number | 0 | true | Worker (L6): `spells_sustained * 2`. Every sustained spell adds +2 TN to all magical actions. |
| `tn_warning_level` | number | 0 | true | Worker (L6): integer 0–3. 0=no warning, 1=amber(sustained_tn_mod=+2), 2=orange(+4), 3=red(+6+). Set by the same `spells_sustained` watcher that sets `sustained_tn_mod`. CSS attribute selector drives warning colors — no DOM class manipulation. (Phase 4 Amendment 4-A) |

[CARRY-FORWARD NOTE — power_points_available vs power_points_remaining]: The Blueprint Requirement header uses `power_points_available`. Layer 2 consistently uses `power_points_remaining` throughout (Phase 2 Task 2.3, Phase 3 Task 3.11, Phase 5 DECISION-05). This blueprint uses `power_points_remaining` as the canonical name per Layer 2. Confirm with system owner if the name should be changed.

---

#### Group 16 — Essence (1 field)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `essence_total` | number | 0 | true | Worker (L5): `parseFloat` sum of `mutation_essence` across all `repeating_mutations` rows (decimal arithmetic: essence costs may be 0.2, 1.15, etc.) |

---

#### Group 17 — Bio Questions (20 fields)

Textual answers to the 20 Session 0 character creation questions. All text, all empty defaults, none computed. Labels (the question text) are static HTML — these attributes hold only the player's answer.

| `name` | `type` | `default` | `worker_only` | Question label (static HTML; not stored) |
|---|---|---|---|---|
| `bio_q01` | text | `""` | false | "Who is your biggest rival and why?" |
| `bio_q02` | text | `""` | false | "Who/what do you despise?" |
| `bio_q03` | text | `""` | false | "Who looks up to you and why?" |
| `bio_q04` | text | `""` | false | "Most prized possession?" |
| `bio_q05` | text | `""` | false | "How have you gained success or suffered failure?" |
| `bio_q06` | text | `""` | false | "What drives you?" |
| `bio_q07` | text | `""` | false | "Closest friends?" |
| `bio_q08` | text | `""` | false | "Who trained you and in what?" |
| `bio_q09` | text | `""` | false | "Close to family?" |
| `bio_q10` | text | `""` | false | "Family relationship state?" |
| `bio_q11` | text | `""` | false | "Current love interest?" |
| `bio_q12` | text | `""` | false | "In a relationship?" |
| `bio_q13` | text | `""` | false | "Greatest love?" |
| `bio_q14` | text | `""` | false | "Bathing habits?" |
| `bio_q15` | text | `""` | false | "Have you killed anyone?" |
| `bio_q16` | text | `""` | false | "Jailed/imprisoned?" |
| `bio_q17` | text | `""` | false | "How do you look and dress?" |
| `bio_q18` | text | `""` | false | "Noticeable mannerisms?" |
| `bio_q19` | text | `""` | false | "Greatest virtues?" |
| `bio_q20` | text | `""` | false | "Greatest flaws?" |

---

#### Group 18 — Sync Infrastructure (4 fields)

Phase 5 carry-forward fields. Not displayed in the player-facing sheet UI. No CSS styling. Require `<input type="hidden">` elements in the HTML so Sheet Workers can read/write them via K-scaffold.

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `char_db_id` | text | `""` | false | Turso character UUID. Set by the `btn_sync_db` handler on first successful outbound sync. Never user-edited. Read-only after initial assignment. |
| `char_sync_version` | number | 0 | false | Last-known Turso `sync_version` integer. Updated after every successful outbound push. Used as `sync_version_from` payload field. NOT `worker_only` — Sheet Worker writes it as side-effect of sync, not as part of attribute cascade. |
| `campaign_db_id` | text | `""` | false | Turso campaign UUID. Set once by GM during campaign setup. Included as top-level field in sync payload (not part of the `scalars` object). |
| `sync_status` | text | `"Never synced"` | false | Human-readable last sync result label (e.g., `"Synced ✓ — 2026-03-28 18:42"` or `"Sync failed — check console"`). Updated by the outbound sync Sheet Worker handler on success and failure. Displayed on Core tab next to `btn_sync_db`. (DECISION-07: Option A + B confirmed) |

[CARRY-FORWARD NOTE — turso_auth_token]: Phase 5 Amendment 5-D listed `turso_auth_token` as a conditional field. DECISION-14 resolved this as: Cloudflare Worker proxy stores the real Turso token; the Sheet Worker sends only to the proxy URL. **`turso_auth_token` is NOT required in sheet.json and must NOT be added.** If the architecture changes away from the proxy pattern this must be revisited.

[CARRY-FORWARD NOTE — btn_pull_db]: Phase 5 Amendment 5-B specifies a `btn_pull_db` action button and inbound pull Sheet Worker handler. DECISION-08 deferred bidirectional sync to V2. The `btn_pull_db` button and its handler are **V2 scope — do not implement in V1**. No corresponding attribute is needed in V1 sheet.json.

---

#### Group 19 — UI State (1 field)

| `name` | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `sheet_compact_mode` | checkbox | 0 | false | Manual compact layout toggle. Checked state triggers CSS `#sheet-compact-mode:checked ~ .sheet-compact-target` rules. Persists per character via Roll20 attribute storage. No Sheet Worker handler — CSS-only effect. (Phase 4 Task 4.12) |

---

#### Registry Total

| Group | Field count | Notes |
|---|---|---|
| 1 — Core Attribute Base Values | 8 | All player-editable |
| 2 — Core Attribute Mutation Sub-values | 7 | `mag` excluded |
| 3 — Core Attribute Magic Sub-values | 7 | `mag` excluded |
| 4 — Core Attribute Misc Modifiers | 8 | All 8 attributes including `mag` |
| 5 — Core Attribute Totals | 8 | All `worker_only: true` |
| 6 — Reaction | 3 | `reaction_base` and `reaction` are worker_only; `reaction_misc` is player-editable |
| 7 — Dice Pools | 12 | All base and total fields are `worker_only: true`; misc fields are player-editable |
| 8 — Initiative | 4 | `init_score` is worker_only; others player-editable |
| 9 — Condition Monitors | 6 | Damage level inputs player-editable; `cm_tn_mod` and `cm_init_mod` worker_only |
| 10 — Character Identity | 6 | All player-editable text |
| 11 — Karma | 4 | `karma_total` is worker_only; others player-editable |
| 12 — Encumbrance | 2 | Both `worker_only: true` |
| 13 — Armor Inputs | 12 | All player-editable (3 loc × 4 sub-fields) |
| 14 — Armor Totals | 3 | All `worker_only: true` |
| 15 — Magic / Adept Power Tab Scalars | 6 | `spells_sustained` is player-editable; 5 others worker_only |
| 16 — Essence | 1 | `worker_only: true` |
| 17 — Bio Questions | 20 | All player-editable text |
| 18 — Sync Infrastructure | 4 | All player-editable (Sheet Worker updates, not cascade-computed) |
| 19 — UI State | 1 | Player-editable (checkbox toggle) |
| **TOTAL** | **122** | **Verified against all Phase 1–5 amendments** |

[CARRY-FORWARD NOTE — field count vs. plan estimate]: Layer 2 memory and plan notes reference "~150 scalar attributes." This blueprint's verified count is **122 scalar attributes**. The "~150" was an early planning estimate written before all phases were complete. Use the 122-field table as the authoritative count.

[CARRY-FORWARD NOTE — Phase 1 Task 1.2 header discrepancy]: The Layer 2 Phase 1 spec header says "Core Attribute Fields (45 fields)" but the table mathematics yield 38 (7×5 + 3 for mag) + 3 (reaction) = 41 fields. The "(45)" annotation appears to be a plan-writing error. Verified count from this blueprint: 41 core + reaction fields (Groups 1–6).

---

#### Roll Buttons — Declaration Note

[CARRY-FORWARD NOTE — roll buttons not in attributes array]: Layer 2 Phase 2 deliverables explicitly state: "roll buttons have no sheet.json schema entry in K-scaffold." Roll buttons are HTML `<button type="roll">` and `<button type="action">` elements; they are not Roll20 stored character attributes. They do NOT appear in sheet.json's `attributes` array.

The following `btn_*` elements exist in the sheet HTML. They are listed here for completeness, cross-referenced against their K-scaffold handler names:

| HTML element | `name=` attribute in HTML | K-scaffold handler (Phase 3) | V1/V2 |
|---|---|---|---|
| Attribute roll (×9) | `roll_btn_roll_{attr}` | `on('clicked:btn_roll_{attr}', ...)` | V1 |
| Initiative roll | `roll_btn_init_roll` | `on('clicked:btn_init_roll', ...)` | V1 |
| Dodge | `roll_btn_dodge` | `on('clicked:btn_dodge', ...)` | V1 |
| Resist Damage (Body) | `roll_btn_damage_resist_body` | `on('clicked:btn_damage_resist_body', ...)` | V1 |
| Skill Roll | `roll_btn_skill_roll` (per repeating row) | `on('clicked:btn_skill_roll', ...)` | V1 |
| Cast Spell | `roll_btn_cast_spell` (per repeating row) | `on('clicked:btn_cast_spell', ...)` | V1 |
| Drain Resist | `roll_btn_drain_resist` (per repeating row) | `on('clicked:btn_drain_resist', ...)` | V1 |
| Ranged Attack | `roll_btn_attack_ranged` (per repeating row) | `on('clicked:btn_attack_ranged', ...)` | V1 |
| Melee Attack | `roll_btn_attack_melee` (per repeating row) | `on('clicked:btn_attack_melee', ...)` | V1 |
| Sync to DB | `act_btn_sync_db` (`<button type="action">`) | `on('clicked:btn_sync_db', ...)` | V1 |
| Pull from DB | `act_btn_pull_db` (`<button type="action">`) | `on('clicked:btn_pull_db', ...)` | **V2 only — do not implement in V1** |

[CARRY-FORWARD NOTE — K-scaffold action button naming]: K-scaffold action buttons use `<button type="action" name="act_btn_{name}">`. The event fires as `on('clicked:btn_{name}', ...)`. Confirm this naming pattern matches your K-scaffold version. Some versions use `roll_` prefix even for action buttons; others use `act_`.

---

### Section 3: Repeating Section Schema Reference

K-scaffold's `sheet.json` `attributes` array does **not** include repeating section row fields. Row fields are defined in the HTML `<fieldset data-groupname="repeating_{section}">` template div. This section serves as the authoritative per-row field reference for the Developer writing both the HTML template rows and the K-scaffold Sheet Worker repeating section handlers.

**K-scaffold repeating attribute name format:** `repeating_{section}_{rowId}_{fieldName}`
Example: `repeating_skills_-M7X9hqxZ_skill_base`

Roll20 assigns the `rowId` token automatically when a row is added. Sheet Workers use `k.getAllAttrs` or `k.getAttrs` with the repeating section identifier to iterate all rows.

---

#### repeating_skills

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `skill_name` | text | `""` | false | Custom skill name (any string) |
| `skill_linked_attr` | text | `"body"` | false | Linked core attribute. HTML `<select>` with options: body / dex / str / cha / int / wil / hum / mag / reaction |
| `skill_general` | text | `""` | false | General skill category (e.g., "Combat", "Social") |
| `skill_spec` | text | `""` | false | Specialization within the skill |
| `skill_base` | number | 0 | false | Base skill rating (player-purchased points) |
| `skill_foci` | number | 0 | false | Skill focus / foci bonus |
| `skill_misc` | number | 0 | false | Miscellaneous modifier |
| `skill_total` | number | 0 | true | Worker (L5): `skill_base + skill_foci + skill_misc`. If total = 0 at roll time: player rolls linked attribute at +4 TN — this is a roll-time player responsibility, not sheet-enforced logic. |
| `btn_skill_roll` | — | — | — | HTML `<button type="roll">` — NOT a stored attribute; not in sheet.json |

**Row total: 9 documented fields (8 data fields + 1 button row)**

---

#### repeating_spells

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `spell_name` | text | `""` | false | Spell name |
| `spell_type` | text | `"M"` | false | Mana (M) or Physical (P). HTML `<select>` with options: M / P |
| `spell_duration` | text | `"I"` | false | Instantaneous (I), Sustained (S), or Permanent (P). HTML `<select>` with options: I / S / P |
| `spell_target` | text | `""` | false | Target description (e.g., "WIL", "BOD", "No resistance") |
| `spell_force` | number | 0 | false | Spell Force rating |
| `spell_drain` | text | `""` | false | Drain code string (e.g., `"+2D"`, `"F/2+2S"`) — text because drain codes are not pure integers |
| `btn_cast_spell` | — | — | — | HTML `<button type="roll">` — NOT a stored attribute |
| `btn_drain_resist` | — | — | — | HTML `<button type="roll">` — NOT a stored attribute |

**Row total: 8 documented fields (6 data fields + 2 button rows)**

---

#### repeating_mutations

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `mutation_name` | text | `""` | false | Mutation name |
| `mutation_level` | number | 0 | false | Mutation level or rating |
| `mutation_essence` | number | 0 | false | Essence cost — **decimal arithmetic** (e.g., 0.2, 1.15). Use `parseFloat` in Sheet Worker sum. |
| `mutation_bp_cost` | number | 0 | false | Build Point cost at character creation |
| `mutation_effect` | text | `""` | false | Narrative and/or mechanical effect description (wide field in HTML) |

**Row total: 5 data fields**

---

#### repeating_adept_powers

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `power_name` | text | `""` | false | Adept power name |
| `power_level` | number | 0 | false | Power level |
| `power_pp_cost` | text | `""` | false | **Display-only** human-readable PP cost string (e.g., `"0.25/level"`, `"1 per level"`). Player reference only. Sheet Workers must NOT read this field for arithmetic. |
| `power_pp_cost_value` | number | 0 | false | **Numeric** PP cost for Sheet Worker sum. Separate from `power_pp_cost`. Phase 3 amendment confirmed: this is the only field used for `power_points_used` calculation. Use `parseFloat` in sum. |
| `power_effect` | text | `""` | false | Power effect description (wide field in HTML) |

**Row total: 5 data fields**

[CARRY-FORWARD NOTE — repeating_adept_powers field count header]: The Layer 2 Phase 1 spec header says "(6 fields per row)" but the explicit field list contains exactly 5 fields. The "(6)" annotation appears to be a plan-writing error. This blueprint documents 5 fields. Developer should confirm with system owner if a 6th unanticipated field was intended.

---

#### repeating_weapons

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `weapon_name` | text | `""` | false | Weapon name |
| `weapon_type` | text | `"Edged"` | false | Weapon category. HTML `<select>`: Edged / Club / Polearm / Unarmed / Projectile / Thrown |
| `weapon_modifiers` | text | `""` | false | Modifiers, accessories, or notes (e.g., smartgun link, silencer) |
| `weapon_power` | number | 0 | false | Weapon Power rating (used in damage resist TN calculation) |
| `weapon_damage` | text | `""` | false | Damage code string (e.g., `"4M"`, `"(STR)L"`) — text because damage codes are not pure integers |
| `weapon_conceal` | number | 0 | false | Concealability rating |
| `weapon_reach` | number | 0 | false | Reach (melee weapons; 0 for most ranged) |
| `weapon_ep` | number | 0 | false | Encumbrance Points; contributes to `ep_total` Sheet Worker sum |
| `weapon_range_short` | text | `""` | false | Short range band TN (text: may be a number or "—") |
| `weapon_range_medium` | text | `""` | false | Medium range band TN |
| `weapon_range_long` | text | `""` | false | Long range band TN |
| `weapon_range_extreme` | text | `""` | false | Extreme range band TN |
| `btn_attack_ranged` | — | — | — | HTML `<button type="roll">` — NOT a stored attribute |
| `btn_attack_melee` | — | — | — | HTML `<button type="roll">` — NOT a stored attribute |

**Row total: 14 documented fields (12 data fields + 2 button rows)**

---

#### repeating_equipment

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `equip_name` | text | `""` | false | Equipment item name |
| `equip_description` | text | `""` | false | Description, notes, or special properties |
| `equip_ep` | number | 0 | false | Encumbrance Points; contributes to `ep_total` Sheet Worker sum |

**Row total: 3 data fields**

---

#### repeating_contacts

| Field | `type` | `default` | `worker_only` | Notes |
|---|---|---|---|---|
| `contact_name` | text | `""` | false | Contact's name |
| `contact_info` | text | `""` | false | Background, job, location, or relationship notes |
| `contact_level` | number | 1 | false | Relationship depth. 1 = Contact (acquaintance); 2 = Buddy (+1 Etiquette die); 3 = Friend (+2 Etiquette die). HTML `<select>`: 1-Contact / 2-Buddy / 3-Friend |

**Row total: 3 data fields**

---

#### Repeating Section Totals

| Section | Data fields | Button rows | Total documented rows |
|---|---|---|---|
| `repeating_skills` | 8 | 1 | 9 |
| `repeating_spells` | 6 | 2 | 8 |
| `repeating_mutations` | 5 | 0 | 5 |
| `repeating_adept_powers` | 5 | 0 | 5 |
| `repeating_weapons` | 12 | 2 | 14 |
| `repeating_equipment` | 3 | 0 | 3 |
| `repeating_contacts` | 3 | 0 | 3 |
| **TOTALS** | **42 data fields** | **5 button rows** | **47 documented rows** |

---

### Section 4: Roll Template Declarations

Roll templates are defined in `sheet.html` inside `<rolltemplate class="sheet-rolltemplate-{name}">` blocks. They are referenced in roll button `value` attributes as `&{template:{name}}`. Template parameters are passed as `{{paramName=value}}` in the button formula.

[CARRY-FORWARD NOTE — sheet.json template declaration]: Standard Roll20 `sheet.json` does not have a `templates` key. Roll templates are self-contained HTML blocks; they do not require separate registration in sheet.json. The `"templates": ["skill","attack","spell"]` skeleton in Section 1 is K-scaffold metadata only — verify whether your K-scaffold version uses it.

---

#### Template: `rolltemplate-skill`

**Referenced as:** `&{template:skill}`
**Used by:** `btn_roll_{attr}` (all 9 attribute rolls), `btn_skill_roll` (repeating_skills), `btn_dodge`, and any future non-attack/non-spell success rolls.
**CSS class:** `.sheet-rolltemplate-skill` — dark navy header (`#1a1a2e`)

| Parameter | Required | Source | Purpose |
|---|---|---|---|
| `{{charname=...}}` | Required | `@{char_name}` | Character name in header bar |
| `{{rollname=...}}` | Required | Attribute name or skill name (e.g., `"Body"`, `@{skill_name}`) | Roll label in header |
| `{{linked_attr=...}}` | Optional | `@{skill_linked_attr}` (skill rolls only) | Displays linked attribute for reference; omit for raw attribute rolls |
| `{{tn=...}}` | Required | `?{Target Number\|4}` | Target number used; displayed in template body |

[CARRY-FORWARD NOTE — Layer 2 Task 3.15 skill button formula correction]: Layer 2 Task 3.15 (line 713) has the skill roll button formula as: `{{linked=@{skill_linked_attr}}}`. The parameter name `linked` does NOT match the template parameter `linked_attr` declared in this spec and in Layer 2 Task 3.14 (line 648). Roll20 Mustache templates silently receive no value for an unrecognised parameter — `linked_attr` will not render in chat if the button formula uses `{{linked=...}}`. **The correct button formula must use `{{linked_attr=@{skill_linked_attr}}}`**. Task 3.15's formula is wrong; this blueprint's parameter table is authoritative. The Developer must implement `{{linked_attr=...}}` and ignore the `{{linked=...}}` occurrence in Task 3.15.
| `{{successes=...}}` | Required | `[[ Nd6cs>=TN cf<=1 ]]` | Inline roll expression. Result = success count. `cs>=TN` renders successes green; `cf<=1` renders 1s red. |
| `{{^successes}}` block | Auto | — | Inverse Mustache — renders warning text when `successes = 0`. Text: `"⚠ No successes — check dice tray. All red dice = Critical Failure."` |

**Complete button formula pattern (attribute roll example):**
```
&{template:skill} {{charname=@{char_name}}} {{rollname=Body}} {{tn=?{Target Number|4}}} {{successes=[[@{body}d6cs>=?{Target Number|4} cf<=1]]}}
```

---

#### Template: `rolltemplate-attack`

**Referenced as:** `&{template:attack}`
**Used by:** `btn_attack_ranged`, `btn_attack_melee` (both in `repeating_weapons`)
**CSS class:** `.sheet-rolltemplate-attack` — dark maroon header (`#3a1c1c`)

| Parameter | Required | Source | Purpose |
|---|---|---|---|
| `{{charname=...}}` | Required | `@{char_name}` | Character name in header bar |
| `{{rollname=...}}` | Required | `"Ranged Attack"` or `"Melee Attack"` | Roll type label |
| `{{weapon_name=...}}` | Required | `@{weapon_name}` | Weapon name in template body |
| `{{tn=...}}` | Required | `?{Range TN\|4}` (ranged) or `?{TN\|4}` (melee) | Target number used |
| `{{successes=...}}` | Required | `[[ (pool_dice)d6cs>=TN cf<=1 ]]` | Inline success roll; `cf<=1` required |
| `{{damage_code=...}}` | Required | `@{weapon_damage}` | Damage code display for GM reference (e.g., `"4M"`) |
| `{{power=...}}` | Required | `@{weapon_power}` | Weapon Power for damage resist TN calculation reference |
| `{{reach=...}}` | Optional | `@{weapon_reach}` (melee only; `""` for ranged) | Reach value for melee; empty string suppresses display |
| `{{range_band=...}}` | Optional | `?{Range Band\|Short}` (ranged only; `""` for melee) | Range band for ranged; empty string suppresses display |
| `{{^successes}}` block | Auto | — | Zero-successes warning block (same text as skill template) |

**Notes on weapon roll queries:**
- Ranged: two queries at roll time — `?{Skill dice|0}` + `?{Combat Pool dice|0}`, then `?{Range TN|4}`
- Melee: two queries — `?{Skill dice|0}` + `?{Combat Pool dice|0}`, then `?{TN|4}`
- Weapon skill total is not stored per weapon row — player enters dice via query at roll time

---

#### Template: `rolltemplate-spell`

**Referenced as:** `&{template:spell}`
**Used by:** `btn_cast_spell`, `btn_drain_resist` (both in `repeating_spells`)
**CSS class:** `.sheet-rolltemplate-spell` — dark blue header (`#1c3a5e`)

| Parameter | Required | Source | Purpose |
|---|---|---|---|
| `{{charname=...}}` | Required | `@{char_name}` | Character name in header bar |
| `{{rollname=...}}` | Required | `"Cast Spell"` or `"Drain Resist"` | Roll type label |
| `{{spell_name=...}}` | Required | `@{spell_name}` | Spell name in template body |
| `{{spell_type=...}}` | Required | `@{spell_type}` | M or P |
| `{{spell_duration=...}}` | Required | `@{spell_duration}` | I / S / P |
| `{{force=...}}` | Required | `@{spell_force}` | Spell force used |
| `{{tn=...}}` | Required | `?{Target Number\|4}` | Target number for the roll |
| `{{successes=...}}` | Required | `[[ (dice)d6cs>=TN cf<=1 ]]` | Inline success roll; `cf<=1` required |
| `{{drain_code=...}}` | Required | `@{spell_drain}` | Drain code display for GM reference |
| `{{sustained_penalty=...}}` | Required | `@{sustained_tn_mod}` | Active TN penalty from sustained spells; informational reference for GM/player |
| `{{^successes}}` block | Auto | — | Zero-successes warning block |

**Cast Spell roll queries:** `?{Sorcery dice|0}` + `?{Spell Pool dice|0}` + `?{Target Number|4}`
**Drain Resist roll queries:** `?{Remaining Spell Pool dice|0}` + `?{Drain TN|0}` (player reads drain code and calculates TN manually as Force/2 + drain modifier)

**Initiative roll — not a roll template:** Initiative uses a plain `/roll` expression (sum roll, not success-counting). Template is NOT used for initiative: `@{init_dice}d6 + @{init_score}`. No `&{template:...}`. No `cs` or `cf` modifiers.

[CARRY-FORWARD NOTE — Layer 2 Task 3.15 initiative formula is invalid]: Layer 2 Task 3.15 (line 705) shows the initiative button value as: `value="/roll @{init_dice}d6 + @{init_score}  &{template:skill} {{rollname=Initiative}} {{result=[[...]]}}"`. This is syntactically invalid — `/roll` and `&{template:...}` cannot be combined in a single Roll20 button value; the `/roll` prefix is for chat commands and is not a button value prefix. **The correct button value is the plain-sum expression: `@{init_dice}d6 + @{init_score}`** (no `/roll`, no template, no `cs`/`cf`). The Developer must use this blueprint's guidance and ignore the Task 3.15 initiative formula.

---

### Section 5: K-scaffold Cascade Dependency Map

**Purpose:** Table-form dependency graph sufficient for a Developer to wire K-scaffold's `k.registerFuncs` and `k.cascadeUpdate` calls. Not code. Column definitions: Layer = computation order; Source Fields = K-scaffold `getAttrs` trigger set; Computed Output = `setAttrs` target; Worker Task = Layer 2 Phase 3 reference.

K-scaffold handles cascade sequencing when dependencies are declared via `k.registerFuncs` with explicit dependency arrays. **All workers must use `k.registerFuncs`, not bare `on()` calls.** One `k.sheetOpens` handler triggers full cascade recalculation on sheet open.

| Layer | Source Fields (triggers) | Computed Output | Worker Task | Notes |
|---|---|---|---|---|
| L1 — Raw inputs | `{attr}_base`, `{attr}_mutations`, `{attr}_magic`, `{attr}_misc` for each of the 8 attributes | *(no computation — leaf inputs)* | — | Changes here cascade to L2 workers |
| L2 — Attribute totals | `body_base`, `body_mutations`, `body_magic`, `body_misc` | `body` | Task 3.2 | Formula: `base + mutations + magic + misc` (no rounding) |
| L2 | `dex_base`, `dex_mutations`, `dex_magic`, `dex_misc` | `dex` | Task 3.2 | Same formula |
| L2 | `str_base`, `str_mutations`, `str_magic`, `str_misc` | `str` | Task 3.2 | Same formula |
| L2 | `cha_base`, `cha_mutations`, `cha_magic`, `cha_misc` | `cha` | Task 3.2 | Same formula |
| L2 | `int_base`, `int_mutations`, `int_magic`, `int_misc` | `int` | Task 3.2 | Same formula |
| L2 | `wil_base`, `wil_mutations`, `wil_magic`, `wil_misc` | `wil` | Task 3.2 | Same formula |
| L2 | `hum_base`, `hum_mutations`, `hum_magic`, `hum_misc` | `hum` | Task 3.2 | Same formula |
| L2 | `mag_base`, `mag_misc` | `mag` | Task 3.2 | Exception: no `_mutations` or `_magic` sub-fields |
| L3 — Reaction | `int`, `dex` | `reaction_base` | Task 3.3 | `Math.floor((int + dex) / 2)`. Must fire AFTER L2 workers. |
| L3 | `reaction_base`, `reaction_misc` | `reaction` | Task 3.3 | `reaction_base + reaction_misc`; apply `Math.max(1, result)` floor |
| L4a — Pool bases | `cha`, `int`, `wil` | `pool_spell_base` | Task 3.4 | `Math.floor((cha + int + wil) / 2)`. Must fire AFTER L2 and L3. |
| L4a | `dex`, `int`, `wil` | `pool_combat_base` | Task 3.4 | `Math.floor((dex + int + wil) / 2)` |
| L4a | `reaction` | `pool_control_base` | Task 3.4 | Direct copy: `= reaction` |
| L4a | `int`, `wil`, `mag` | `pool_astral_base` | Task 3.4 | `Math.floor((int + wil + mag) / 3)` |
| L4b — Pool totals | `pool_spell_base`, `pool_spell_misc` | `pool_spell` | Task 3.4 | `base + misc`; `Math.max(0, result)` floor |
| L4b | `pool_combat_base`, `pool_combat_misc` | `pool_combat` | Task 3.4 | Same pattern |
| L4b | `pool_control_base`, `pool_control_misc` | `pool_control` | Task 3.4 | Same pattern |
| L4b | `pool_astral_base`, `pool_astral_misc` | `pool_astral` | Task 3.4 | Same pattern |
| L4c — Initiative | `reaction`, `init_reaction_mod`, `init_misc_mod` | `init_score` | Task 3.5 | `reaction + init_reaction_mod + init_misc_mod`. Fires after L3. |
| L5 — Aggregates | `str`, `body` | `ep_max` | Task 3.8 | `Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)` |
| L5 | `repeating_weapons:weapon_ep`, `repeating_equipment:equip_ep` | `ep_total` | Task 3.8 | Full repeating-section iteration; `parseFloat` sum |
| L5 | 9 armor inputs (all `armor_{loc}_{type}`) | `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact` | Task 3.9 | Sum of 3 locations per type |
| L5 | `skill_base`, `skill_foci`, `skill_misc` (per repeating_skills row) | `skill_total` (per row) | Task 3.10 | Registered within repeating section handler |
| L5 | `mag` | `power_points_max` | Task 3.11 | Direct copy: `= mag` |
| L5 | `repeating_adept_powers:power_pp_cost_value` | `power_points_used` | Task 3.11 | `parseFloat` sum; decimal arithmetic |
| L5 | `power_points_max`, `power_points_used` | `power_points_remaining` | Task 3.11 | `max - used` |
| L5 | `repeating_mutations:mutation_essence` | `essence_total` | Task 3.12 | `parseFloat` sum; decimal arithmetic |
| L6 — Modifiers | `karma_good`, `karma_used` | `karma_total` | Task 3.7 | `good + used`; no flooring |
| L6 | `cm_mental`, `cm_stun`, `cm_physical` | `cm_tn_mod` | Task 3.6 | `Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))`; `penaltyOf = lvl => Math.min(lvl, 3)` |
| L6 | `cm_mental`, `cm_stun`, `cm_physical` | `cm_init_mod` | Task 3.6 | `-1 * cm_tn_mod`; can share one handler with `cm_tn_mod` |
| L6 | `spells_sustained` | `sustained_tn_mod` | Task 3.13 | `spells_sustained * 2`; no flooring needed |
| L6 | `spells_sustained` (via `sustained_tn_mod` threshold) | `tn_warning_level` | Phase 4 Amend. 4-A + Task 3.13 | Extend the `spells_sustained` watcher: `sustained_tn_mod >= 6 → 3`; `>= 4 → 2`; `>= 2 → 1`; else `0` |

**Cascade layers summary:**

```
L1 → raw inputs (leaf)
L2 → 8 attribute totals (require L1 complete)
L3 → reaction_base, reaction (require L2 complete; specifically int + dex)
L4a → 4 pool bases (require L2 + L3)
L4b → 4 pool totals (require L4a)
L4c → init_score (require L3)
L5 → ep_max, ep_total, armor totals, skill_total per row, power_points_*, essence_total
L6 → karma_total, cm_tn_mod, cm_init_mod, sustained_tn_mod, tn_warning_level
```

**Event-driven (not cascade):** Sheet Worker sync handlers (`on('clicked:btn_sync_db', ...)`) fire on button click, not on attribute change. They call `getAttrs` to collect all scalar fields and repeating section data, construct the Turso payload, and call `setAttrs` to write `char_sync_version`, `char_db_id`, and `sync_status` as side effects. These do not participate in the cascade.

---

### Section 6: Developer Guidance Notes

---

#### 6.1 K-scaffold `attr_` Prefix Convention in sheet.json

[CARRY-FORWARD NOTE]: The `name` field in the `attributes` array of K-scaffold's `sheet.json` format is ambiguous from the Layer 2 documents. Two conventions exist:

- **Option A — Bare name:** `"name": "body_base"`. K-scaffold's attribute registry uses bare names internally; `getAttrs()`/`setAttrs()` use bare names. This is consistent with how Sheet Workers reference attributes throughout Phase 3.
- **Option B — `attr_`-prefixed:** `"name": "attr_body_base"`. The Blueprint Requirement example shows this form, noting "K-scaffold strips this."

Both conventions have been seen in the wild. **Verify against K-scaffold's source documentation or an existing K-scaffold sheet.json example before writing the file.** The attribute tables in this blueprint use bare names as the canonical identifier. If K-scaffold requires `attr_` prefix in `sheet.json`, prefix all names in the `attributes` array mechanically — the names themselves are correct as documented here.

---

#### 6.2 `worker_only` Fields and HTML Input Requirements

Roll20 only persists attribute values that have a corresponding HTML input element on the sheet. Worker-only fields must still appear in the HTML as either:
- `<input type="hidden" name="attr_{fieldname}" value="0">` — the standard approach; invisible to the player; survives Roll20's DOM processing
- `<input type="text" name="attr_{fieldname}" readonly>` — if the value should be visibly displayed (e.g., in the attribute totals column, pool totals, computed badge fields)

Without an HTML input, Roll20 does not create the attribute record in the character's data store and `setAttrs()` calls targeting it will silently fail.

---

#### 6.3 The `int` Attribute Name

The attribute name `int` is used throughout this project for the Intelligence core attribute. Concerns:
- **Java/C#:** `int` is a reserved keyword. Irrelevant — this is not Java or C#.
- **JavaScript (ECMAScript 2015+):** `int` is NOT a reserved keyword in modern JavaScript. ECMAScript reserved words include `in`, `instanceof`, `new`, `return`, etc. but NOT `int`. K-scaffold attribute names are plain strings passed to `getAttrs(['int', 'dex', ...])` and `setAttrs({ int: value })` — this is valid JavaScript object property syntax.
- **Roll20 HTML:** `name="attr_int"` is a valid HTML attribute value per the HTML5 specification.

**Verdict: use `int` as specified in Layer 2. No rename needed.**

---

#### 6.4 How Roll20 Handles sheet.json Defaults

When a new character sheet is created in Roll20, the values in the `default` field of each attribute entry are written to the character's attribute store. If a character's attribute has never been set, Roll20 returns the `default` value when it is read. Changing a `default` in `sheet.json` after deployment affects only newly created characters — existing characters retain their previously stored values.

---

#### 6.5 Roll20 Version and K-scaffold Constraints

- **Roll20 Pro required:** Custom character sheet upload requires Roll20 Pro plan. K-scaffold's Sheet Worker `fetch()` calls (for Turso sync) also require Roll20 Pro.
- **K-scaffold version:** K-scaffold is an open-source library. Confirm the project's pinned version before referencing any K-scaffold API calls. API names and sheet.json extensions vary by version.
- **Beacon SDK:** Not available for this project (gated to commercial publishers). All Roll20 interaction is via K-scaffold + standard Sheet Worker APIs.
- **No CSS `var()` / `:root`:** Roll20's iframe context does not reliably expose `:root`. CSS custom properties are disallowed; all color values are inline hex constants. (Phase 4 constraint — affects CSS Phase 2 not this phase, documented here for completeness.)

---

#### 6.6 Repeating Section Row Fields vs. `sheet.json`

Repeating section per-row fields (e.g., `skill_name`, `weapon_ep`) do NOT appear in the `attributes` array of `sheet.json`. They are defined only in the HTML `<fieldset data-groupname="repeating_{section}">` template structure. Roll20 infers the schema from the HTML inputs inside the template div.

Roll20 assigns each row a unique token ID (e.g., `-M7X9hqxZ...`). Sheet Workers reference row fields via `repeating_{section}_{rowId}_{fieldName}` in `getAttrs`/`setAttrs`. K-scaffold provides helpers to iterate all rows without manually tracking row IDs.

**Exception for worker_only fields within repeating sections:** `skill_total` is `worker_only: true` within each `repeating_skills` row. It still requires a `<input type="hidden" name="attr_skill_total" value="0">` inside the repeating template div (using the bare field name without the section prefix — Roll20 handles the prefix injection for repeating sections automatically).

---

#### 6.7 Sync Infrastructure Fields — Placement in HTML

The 4 sync infrastructure attributes (`char_db_id`, `char_sync_version`, `campaign_db_id`, `sync_status`) require hidden inputs in the HTML. Placement in the Core tab, per Phase 5 Amendment 5-B:

```
<!-- Sync infrastructure (hidden; Sheet Worker read/write only) -->
<input type="hidden" name="attr_char_db_id">
<input type="hidden" name="attr_char_sync_version" value="0">
<input type="hidden" name="attr_campaign_db_id">
<!-- sync_status IS displayed in UI — see next line -->
<input type="text" name="attr_sync_status" readonly value="Never synced">
```

`sync_status` is a visible read-only display field on the Core tab next to `btn_sync_db`. The other three are fully hidden.

---

#### 6.8 Phase Carry-Forward Summary

The following fields were added as amendments to Phase 1 across Phases 2–5. All have been included in the Section 2 attribute registry above. This list serves as a quick reconciliation check:

| Field | Added in | Group |
|---|---|---|
| `essence_total` | Phase 2 (new field discovery) | Group 16 |
| `spells_sustained` | Phase 2 (new field discovery) | Group 15 |
| `sustained_tn_mod` | Phase 2 (new field discovery) | Group 15 |
| `bio_q01`–`bio_q20` | Phase 2 (new field discovery) | Group 17 |
| `tn_warning_level` | Phase 4 Amendment 4-A | Group 15 |
| `sheet_compact_mode` | Phase 4 (Task 4.12) | Group 19 |
| `char_db_id` | Phase 5 (sync infrastructure) | Group 18 |
| `char_sync_version` | Phase 5 (sync infrastructure) | Group 18 |
| `campaign_db_id` | Phase 5 (sync infrastructure) | Group 18 |
| `sync_status` | Phase 5 Amendment 5-D (DECISION-07) | Group 18 |

**Fields explicitly NOT added despite being mentioned in Phase 5:**
- `turso_auth_token` — excluded; DECISION-14 resolved as proxy-based architecture; token lives in Cloudflare Worker env vars only
- `btn_pull_db` / inbound pull handler — deferred to V2 per DECISION-08

---

*Phase 1 blueprint complete.*

---


---

## Phase 2: HTML Skeleton Blueprint
*(Part A of 3 — Document Structure + Tab: Core)*

**Goal:** Produce the structural blueprint for `sheet.html` — element inventory, nesting hierarchy, and attribute-name-to-HTML-element bindings. After Phase 2 a Developer can write the complete HTML file without making any structural decisions.

**Input:** Phase 1 Naming Contract (all 122 scalar fields + all repeating-section row fields). Phase 2 does NOT cover CSS selectors, Sheet Worker logic, or companion app integration — those are Phases 3–5.

---

### Section 1: Document Structure Skeleton

`sheet.html` has **no `<html>`, `<head>`, or `<body>` tags** — Roll20 injects this file's content directly into the campaign page DOM. The file is a flat sequence of sibling elements in this exact order:

**Top-level nesting order:**

1. `<script type="text/worker">` — K-scaffold hook. Empty at this layer; Sheet Worker body is authored in Phase 3.
2. `<div class="sheet-hidden-infrastructure">` — 4 hidden sync scalar fields as `<input type="hidden">`.
3. `<input type="checkbox" name="attr_sheet_compact_mode" id="sheet-compact-mode">` + its `<label>` — **must appear before all tab content `<div>`s** so the CSS `~` general sibling selector reaches them without re-ordering the DOM.
4. Tab navigation: 5 `<input type="radio" name="sheet-tab-nav">` inputs + 5 paired `<label>` elements (each radio immediately followed by its label, then the next radio/label pair). Radio `id`s match label `for` attributes.
5. 5 tab `<div class="sheet-tab-panel sheet-tab-{name}">` content panels. Each panel is activatable via the CSS sibling selector pattern: `#sheet-tab-{name}:checked ~ .sheet-tab-panel.sheet-tab-{name} { display: block; }`.

**Structural pseudocode skeleton:**

```html
<!-- ═══════════════════════════════════════════════════ -->
<!-- K-scaffold Sheet Worker hook                        -->
<!-- ═══════════════════════════════════════════════════ -->
<script type="text/worker">
  <!-- Sheet Worker body authored in Phase 3 -->
</script>

<!-- ═══════════════════════════════════════════════════ -->
<!-- Hidden infrastructure (sync scalars)                -->
<!-- ═══════════════════════════════════════════════════ -->
<div class="sheet-hidden-infrastructure">
  <input type="hidden" name="attr_char_db_id">
  <input type="hidden" name="attr_char_sync_version" value="0">
  <input type="hidden" name="attr_campaign_db_id">
  <!-- sync_status is a visible readonly text input in the Core tab header strip — NOT hidden here -->
</div>

<!-- ═══════════════════════════════════════════════════ -->
<!-- Compact mode toggle                                 -->
<!-- MUST precede all tab panel divs — ~ selector dep.  -->
<!-- ═══════════════════════════════════════════════════ -->
<input type="checkbox" name="attr_sheet_compact_mode" id="sheet-compact-mode" value="1">
<label for="sheet-compact-mode" class="sheet-compact-toggle">☰ Compact</label>

<!-- ═══════════════════════════════════════════════════ -->
<!-- Tab navigation radios + labels                      -->
<!-- ═══════════════════════════════════════════════════ -->
<input type="radio" name="sheet-tab-nav" id="sheet-tab-core" checked>
<label for="sheet-tab-core" class="sheet-tab-label">Core</label>

<input type="radio" name="sheet-tab-nav" id="sheet-tab-skills">
<label for="sheet-tab-skills" class="sheet-tab-label">Skills</label>

<input type="radio" name="sheet-tab-nav" id="sheet-tab-magic">
<label for="sheet-tab-magic" class="sheet-tab-label">Magic</label>

<input type="radio" name="sheet-tab-nav" id="sheet-tab-gear">
<label for="sheet-tab-gear" class="sheet-tab-label">Gear</label>

<input type="radio" name="sheet-tab-nav" id="sheet-tab-bio">
<label for="sheet-tab-bio" class="sheet-tab-label">Bio</label>

<!-- ═══════════════════════════════════════════════════ -->
<!-- Tab panels (all hidden by default; CSS activates)  -->
<!-- ═══════════════════════════════════════════════════ -->
<div class="sheet-tab-panel sheet-tab-core">
  <!-- Section 2 content — see below -->
</div>

<div class="sheet-tab-panel sheet-tab-skills">
  <!-- Skills tab content — see Tab: Skills element inventory above -->
</div>

<div class="sheet-tab-panel sheet-tab-magic">
  <!-- Magic tab content — see Tab: Magic element inventory above -->
</div>

<div class="sheet-tab-panel sheet-tab-gear">
  <!-- Gear tab content — see Tab: Gear element inventory above -->
</div>

<div class="sheet-tab-panel sheet-tab-bio">
  <!-- Bio tab content — see Tab: Bio element inventory above -->
</div>
```

> **Note:** Full production HTML is not written at Layer 3. This skeleton defines nesting order and class names only. All element details are in Sections 2–5.

---

### Section 2: Tab Element Inventories

#### Tab: Core

The Core tab is organized into 8 named regions rendered top-to-bottom. Each region maps to a `<div class="sheet-region-{name}">` wrapper.

---

##### Region 1: Core Tab Header Strip

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<input>` | text | `attr_sync_status` | — | `sheet-sync-status` | `readonly` attribute present; displays worker-written sync feedback string |
| `<button>` | action | `act_btn_sync_db` | "Sync to DB" | `sheet-btn-sync` | Roll20 action button; triggers Sheet Worker `btn_sync_db` handler |
| `<input>` | number | `attr_cm_tn_mod` | "TN Penalty" | `sheet-cm-tn-mod` | `readonly`; worker-computed compact-mode TN penalty display |
| `<input>` | number | `attr_cm_init_mod` | "Init Penalty" | `sheet-cm-init-mod` | `readonly`; worker-computed compact-mode Init penalty display |

---

##### Region 2: Identity Row

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<input>` | text | `attr_char_name` | "Name" | `sheet-char-name sheet-wide` | Wide input spanning ~3 columns |
| `<input>` | text | `attr_char_race_station` | "Race / Station" | `sheet-char-race-station` | Free text |
| `<input>` | text | `attr_char_sex` | "Sex" | `sheet-char-sex` | Free text |
| `<input>` | text | `attr_char_age` | "Age" | `sheet-char-age` | Free text per Phase 1 registry (allows non-numeric values like "Unknown") |

---

##### Region 3: Condition Monitors

**Implementation pattern:** Each damage track is a set of `<input type="radio">` elements sharing the same `name="attr_{track}"`. The selected radio's `value` attribute stores the integer damage level (0–4 for all tracks; 0–5 for stun and physical to include Unconscious/Overflow threshold). The CSS `:checked` pseudo-class highlights the active tier column. No separate per-box attributes are stored — only the one integer per track.

**TN penalty labels per tier:** +0 (No Damage) / +1 (Light) / +2 (Moderate) / +3 (Serious) / Incap (Deadly)  
**Initiative penalty labels per tier:** 0 / –1 / –2 / –3 / — (Incap)

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| Radio group | radio | `attr_cm_mental` | values: 0 (No Damage), 1 (Light), 2 (Moderate), 3 (Serious), 4 (Deadly) | `sheet-cm-track sheet-cm-mental` | 5 radio inputs; no Uncon column for Mental track |
| Radio group | radio | `attr_cm_stun` | values: 0 (No Damage), 1 (Light), 2 (Moderate), 3 (Serious), 4 (Deadly), 5 (Uncon) | `sheet-cm-track sheet-cm-stun` | 6 radio inputs; value=5 maps to Unconscious threshold |
| Radio group | radio | `attr_cm_physical` | values: 0 (No Damage), 1 (Light), 2 (Moderate), 3 (Serious), 4 (Deadly), 5 (Overflow threshold) | `sheet-cm-track sheet-cm-physical` | 6 radio inputs; value=5 triggers overflow display |
| `<input>` | number | `attr_cm_physical_overflow` | "Overflow" | `sheet-cm-overflow` | Editable; tracks damage beyond Deadly; appears below physical track row |

Each radio group is rendered as a row of 5 or 6 cells. Each cell contains:
- Static TN label (e.g., `+2`)  
- Static Init penalty label (e.g., `–2`)  
- `<input type="radio" name="attr_cm_{track}" value="{tier}">` with a visually-hidden label for accessibility

---

##### Region 4: Attributes Table

**Column headers (static text):** Name | Base | Mutations | Magic | Misc | Total | [Roll]

| Attribute | Base field (`name=`) | Mutations field | Magic field | Misc field | Total field | Roll button |
|---|---|---|---|---|---|---|
| Body | `attr_body_base` (number) | `attr_body_mutations` (number) | `attr_body_magic` (number) | `attr_body_misc` (number) | `attr_body` (number, readonly) | `roll_btn_roll_body` |
| Dexterity | `attr_dex_base` (number) | `attr_dex_mutations` (number) | `attr_dex_magic` (number) | `attr_dex_misc` (number) | `attr_dex` (number, readonly) | `roll_btn_roll_dex` |
| Strength | `attr_str_base` (number) | `attr_str_mutations` (number) | `attr_str_magic` (number) | `attr_str_misc` (number) | `attr_str` (number, readonly) | `roll_btn_roll_str` |
| Charisma | `attr_cha_base` (number) | `attr_cha_mutations` (number) | `attr_cha_magic` (number) | `attr_cha_misc` (number) | `attr_cha` (number, readonly) | `roll_btn_roll_cha` |
| Intelligence | `attr_int_base` (number) | `attr_int_mutations` (number) | `attr_int_magic` (number) | `attr_int_misc` (number) | `attr_int` (number, readonly) | `roll_btn_roll_int` |
| Willpower | `attr_wil_base` (number) | `attr_wil_mutations` (number) | `attr_wil_magic` (number) | `attr_wil_misc` (number) | `attr_wil` (number, readonly) | `roll_btn_roll_wil` |
| Humanity | `attr_hum_base` (number) | `attr_hum_mutations` (number) | `attr_hum_magic` (number) | `attr_hum_misc` (number) | `attr_hum` (number, readonly) | `roll_btn_roll_hum` |
| Reaction | static label "(INT+DEX)/2" | *(blank — no mutations input)* | *(blank — no magic input)* | `attr_reaction_misc` (number) | `attr_reaction` (number, readonly) | `roll_btn_roll_reaction` |
| Magic | `attr_mag_base` (number) | *(blank — no mutations input)* | *(blank — no magic input)* | `attr_mag_misc` (number) | `attr_mag` (number, readonly) | `roll_btn_roll_mag` |

**Notes:**
- `attr_body` through `attr_hum` totals are worker-computed: `{attr}_base + {attr}_mutations + {attr}_magic + {attr}_misc`.
- `attr_reaction` is worker-computed: `floor((INT + DEX) / 2) + reaction_misc`. The Base cell displays the `(INT+DEX)/2` formula as static text; `attr_reaction_base` is a readonly worker-output field, not shown as editable.
- `attr_mag` total: `mag_base + mag_misc`.
- Roll buttons are `type="roll"` with `name="roll_btn_roll_{attr}"`. **DO NOT** use `type="action"` for dice-rolling buttons — action buttons fire a Sheet Worker event but do NOT produce roll output in chat.

---

##### Region 5: Initiative Row

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<input>` | number | `attr_init_dice` | "#d6" | `sheet-init-dice` | Default value `1`; editable |
| `<input>` | number | `attr_init_reaction_mod` | "Reaction Mod" | `sheet-init-reaction-mod` | Editable modifier applied to reaction for init score |
| `<input>` | number | `attr_init_misc_mod` | "Misc Mod" | `sheet-init-misc-mod` | Editable catch-all modifier |
| `<input>` | number | `attr_init_score` | "Init Score" | `sheet-init-score` | `readonly`; worker-computed |
| `<button>` | roll | `roll_btn_init_roll` | "Roll Init" | `sheet-btn-init-roll` | Rolls `{init_dice}d6 + init_score` |

---

##### Region 6: Dice Pools Table

**Column headers (static text):** Pool Name | Formula | Misc | Total

| Pool | Formula (static display) | Misc field | Total field |
|---|---|---|---|
| Spell Pool | "floor((CHA+INT+WIL)/2)" | `attr_pool_spell_misc` (number) | `attr_pool_spell` (number, readonly) |
| Combat Pool | "floor((DEX+INT+WIL)/2)" | `attr_pool_combat_misc` (number) | `attr_pool_combat` (number, readonly) |
| Control Pool | "= reaction" | `attr_pool_control_misc` (number) | `attr_pool_control` (number, readonly) |
| Astral Pool | "floor((INT+WIL+MAG)/3)" | `attr_pool_astral_misc` (number) | `attr_pool_astral` (number, readonly) |

**Notes:**
- Pool base values (`attr_pool_*_base`) are `type="hidden"` worker-computed intermediates; see Table A. They are not displayed as a visible column — the Formula column provides the formula reference.
- Total fields are `readonly`; worker-computed: `pool_*_base + pool_*_misc`.
- Misc fields are editable player-entered modifiers.

---

##### Region 7: Karma Row

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<input>` | number | `attr_karma_good` | "Good Karma" | `sheet-karma-good` | Editable; earned but unspent karma |
| `<input>` | number | `attr_karma_used` | "Karma Used" | `sheet-karma-used` | Editable; total spent karma |
| `<input>` | number | `attr_karma_total` | "Total Karma" | `sheet-karma-total` | `readonly`; worker-computed: `karma_good + karma_used` |
| `<input>` | number | `attr_karma_pool` | "Karma Pool" | `sheet-karma-pool` | Editable; current session pool |

---

##### Region 8: Armor Panel

**Layout:** 3 columns (Torso | Legs | Head) with an identical set of inputs per location, plus a totals row spanning all columns.

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<input>` | text | `attr_armor_torso_name` | "Torso Armor Name" | `sheet-armor-name` | |
| `<input>` | number | `attr_armor_torso_piercing` | "Piercing" | `sheet-armor-piercing` | |
| `<input>` | number | `attr_armor_torso_slashing` | "Slashing" | `sheet-armor-slashing` | |
| `<input>` | number | `attr_armor_torso_impact` | "Impact" | `sheet-armor-impact` | |
| `<input>` | text | `attr_armor_legs_name` | "Legs Armor Name" | `sheet-armor-name` | |
| `<input>` | number | `attr_armor_legs_piercing` | "Piercing" | `sheet-armor-piercing` | |
| `<input>` | number | `attr_armor_legs_slashing` | "Slashing" | `sheet-armor-slashing` | |
| `<input>` | number | `attr_armor_legs_impact` | "Impact" | `sheet-armor-impact` | |
| `<input>` | text | `attr_armor_head_name` | "Head Armor Name" | `sheet-armor-name` | |
| `<input>` | number | `attr_armor_head_piercing` | "Piercing" | `sheet-armor-piercing` | |
| `<input>` | number | `attr_armor_head_slashing` | "Slashing" | `sheet-armor-slashing` | |
| `<input>` | number | `attr_armor_head_impact` | "Impact" | `sheet-armor-impact` | |
| `<input>` | number | `attr_armor_total_piercing` | "Total Piercing" | `sheet-armor-total` | `readonly`; worker-computed sum across all 3 locations |
| `<input>` | number | `attr_armor_total_slashing` | "Total Slashing" | `sheet-armor-total` | `readonly`; worker-computed sum across all 3 locations |
| `<input>` | number | `attr_armor_total_impact` | "Total Impact" | `sheet-armor-total` | `readonly`; worker-computed sum across all 3 locations |

---

##### Region 9: Combat Panel

| Element | Type | `name=` | Label / Options | CSS class hint | Notes |
|---|---|---|---|---|---|
| `<button>` | roll | `roll_btn_dodge` | "Dodge" | `sheet-btn-dodge` | Roll button; triggers dodge roll handler |
| `<button>` | roll | `roll_btn_damage_resist_body` | "Resist Damage (Body)" | `sheet-btn-damage-resist` | Roll button; triggers body damage resistance handler |

---

*(Part A complete — continues in Part B)*

---


---

#### Tab: Skills

**Region: Skills Section Header**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static row | — | — | Column labels: Skill Name / Linked Attr / Category / Spec / Base / Foci / Misc / Total / Roll |
| `<fieldset>` | — | `data-groupname="repeating_skills"` | Repeating section container |

**Within `repeating_skills` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_skill_name` | — | Skill name |
| `<select>` | select | `attr_skill_linked_attr` | body / dex / str / cha / int / wil / hum / mag / reaction | Linked attribute; `<select>` element |
| `<input>` | text | `attr_skill_general` | — | Category column |
| `<input>` | text | `attr_skill_spec` | — | Specialization |
| `<input>` | number | `attr_skill_base` | — | Base rating |
| `<input>` | number | `attr_skill_foci` | — | Foci bonus |
| `<input>` | number | `attr_skill_misc` | — | Misc modifier |
| `<input>` | number | `attr_skill_total` | — | `readonly`; worker computed: base + foci + misc |
| `<button>` | roll | `roll_btn_skill_roll` | — | Roll button |

---

**Region: Mutations Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static label | — | — | "Mutations" |
| `<input>` | number | `attr_essence_total` | `readonly`; worker-computed essence sum across all repeating_mutations rows |
| `<fieldset>` | — | `data-groupname="repeating_mutations"` | Repeating section container |

**Within `repeating_mutations` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_mutation_name` | — | Mutation name |
| `<input>` | number | `attr_mutation_level` | — | Mutation level |
| `<input>` | number | `attr_mutation_essence` | — | Essence cost; decimal values supported; parseFloat in worker |
| `<input>` | number | `attr_mutation_bp_cost` | — | BP cost |
| `<input>` | text | `attr_mutation_effect` | — | Wider display column |

---

**Region: Adept Powers Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static label | — | — | "Adept Powers" |
| `<input>` | number | `attr_power_points_used` | `readonly`; worker-computed sum of power_pp_cost_value across all rows |
| `<input>` | number | `attr_power_points_max` | `readonly`; worker-computed max PP |
| `<input>` | number | `attr_power_points_remaining` | `readonly`; worker computed: max − used; displayed as "PP: X / Y · Remaining: Z" |
| `<fieldset>` | — | `data-groupname="repeating_adept_powers"` | Repeating section container |

**Within `repeating_adept_powers` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_power_name` | — | Power name |
| `<input>` | number | `attr_power_level` | — | Power level |
| `<input>` | text | `attr_power_pp_cost` | — | Display field; drain codes are not pure integers |
| `<input>` | number | `attr_power_pp_cost_value` | — | CSS-hidden numeric field; worker sum target only; separate from display field |
| `<input>` | text | `attr_power_effect` | — | Wider display column |

---

#### Tab: Magic

**Region: Magic Summary Row**

| Element | Type | `name=` | Notes |
|---|---|---|---|
| `<input>` | number | `attr_mag` | `readonly`; worker-computed magic rating total |
| `<input>` | number | `attr_pool_spell` | `readonly`; worker-computed spell pool total |
| `<input>` | number | `attr_spells_sustained` | Player-tracked; directly editable |
| `<input>` | number | `attr_sustained_tn_mod` | `readonly`; worker computed: spells_sustained × 2 |
| `<input>` | hidden | `attr_tn_warning_level` | MUST appear immediately preceding `.sheet-tn-warning` div in DOM order; CSS sibling selector `input[name="attr_tn_warning_level"] ~ .sheet-tn-warning` drives warning color states; values 0 / 1 / 2 / 3 |
| `.sheet-tn-warning` | — | — | Static div / span; no input; CSS target only; displays warning text when tn_warning_level > 0 |

---

**Region: Spells Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static row | — | — | Column headers: Name / Type / Duration / Target / Force / Drain / [Cast] / [Drain] |
| `<fieldset>` | — | `data-groupname="repeating_spells"` | Repeating section container |

**Within `repeating_spells` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_spell_name` | — | Spell name |
| `<select>` | select | `attr_spell_type` | M (Mana) / P (Physical) | Spell type; `<select>` element |
| `<select>` | select | `attr_spell_duration` | I (Instant) / S (Sustained) / P (Permanent) | Spell duration; `<select>` element |
| `<input>` | text | `attr_spell_target` | — | Target |
| `<input>` | number | `attr_spell_force` | — | Force rating |
| `<input>` | text | `attr_spell_drain` | — | Drain code; not pure integers (e.g., "Drain (D/2)M") |
| `<button>` | roll | `roll_btn_cast_spell` | — | Roll button |
| `<button>` | roll | `roll_btn_drain_resist` | — | Roll button |

---

**Region: Casting Reference**

| Element | Type | `name=` | Notes |
|---|---|---|---|
| Static block | — | — | Collapsed display-only reference card; no inputs; no attributes |

---

#### Tab: Gear

**Region: EP Tracker Row**

| Element | Type | `name=` | Notes |
|---|---|---|---|
| `<input>` | number | `attr_ep_total` | `readonly`; worker computed: sum of weapon_ep + equip_ep across all rows |
| `<input>` | number | `attr_ep_max` | `readonly`; worker computed: max(STR,BOD)×4 + ½min(STR,BOD) |
| Static text | — | — | Formula hint: "EP Max = max(STR,BOD)×4 + ½min(STR,BOD)" |

---

**Region: Weapons Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static row | — | — | Column headers: Name / Type / Mods / Power / Dmg / Conceal / Reach / EP / Short / Med / Long / Ext / [Rng] / [Mel] |
| `<fieldset>` | — | `data-groupname="repeating_weapons"` | Repeating section container |

**Within `repeating_weapons` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_weapon_name` | — | Weapon name |
| `<select>` | select | `attr_weapon_type` | Edged / Club / Polearm / Unarmed / Projectile / Thrown | Weapon type; `<select>` element |
| `<input>` | text | `attr_weapon_modifiers` | — | Modifier text |
| `<input>` | number | `attr_weapon_power` | — | Power rating |
| `<input>` | text | `attr_weapon_damage` | — | Damage code; not pure integers |
| `<input>` | number | `attr_weapon_conceal` | — | Conceal rating |
| `<input>` | number | `attr_weapon_reach` | — | Reach rating |
| `<input>` | number | `attr_weapon_ep` | — | Encumbrance points; feeds ep_total sum |
| `<input>` | text | `attr_weapon_range_short` | — | Short range |
| `<input>` | text | `attr_weapon_range_medium` | — | Medium range |
| `<input>` | text | `attr_weapon_range_long` | — | Long range |
| `<input>` | text | `attr_weapon_range_extreme` | — | Extreme range |
| `<button>` | roll | `roll_btn_attack_ranged` | — | Roll button |
| `<button>` | roll | `roll_btn_attack_melee` | — | Roll button |

---

**Region: Equipment Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static row | — | — | Column headers: Name / Description / EP |
| `<fieldset>` | — | `data-groupname="repeating_equipment"` | Repeating section container |

**Within `repeating_equipment` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_equip_name` | — | Equipment name |
| `<input>` | text | `attr_equip_description` | — | Description |
| `<input>` | number | `attr_equip_ep` | — | Encumbrance points; feeds ep_total sum |

---

**Region: Contacts Section**

| Element | Type | `name=` | Options / Notes |
|---|---|---|---|
| Static row | — | — | Column headers: Name / Info / Level |
| `<fieldset>` | — | `data-groupname="repeating_contacts"` | Repeating section container |

**Within `repeating_contacts` row template:**

| Field | Input type | `name=` | Options | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_contact_name` | — | Contact name |
| `<input>` | text | `attr_contact_info` | — | Contact info |
| `<select>` | select | `attr_contact_level` | 1-Contact / 2-Buddy / 3-Friend | Contact level; `<select>` element |

---

#### Tab: Bio

| Element | Type | `name=` | Notes |
|---|---|---|---|
| Static label | — | — | "Description" |
| `<textarea>` | textarea | `attr_char_description` | ~6 rows |
| Static label | — | — | "Notes" |
| `<textarea>` | textarea | `attr_char_notes` | ~6 rows |
| Static label | — | — | Q1: "Who is your biggest rival and why?" |
| `<textarea>` | textarea | `attr_bio_q01` | ~3 rows |
| Static label | — | — | Q2: "Who or what do you despise?" |
| `<textarea>` | textarea | `attr_bio_q02` | ~3 rows |
| Static label | — | — | Q3: "Who looks up to you and why?" |
| `<textarea>` | textarea | `attr_bio_q03` | ~3 rows |
| Static label | — | — | Q4: "What is your most prized possession?" |
| `<textarea>` | textarea | `attr_bio_q04` | ~3 rows |
| Static label | — | — | Q5: "How have you gained success or suffered failure?" |
| `<textarea>` | textarea | `attr_bio_q05` | ~3 rows |
| Static label | — | — | Q6: "What drives you?" |
| `<textarea>` | textarea | `attr_bio_q06` | ~3 rows |
| Static label | — | — | Q7: "Who are your closest friends?" |
| `<textarea>` | textarea | `attr_bio_q07` | ~3 rows |
| Static label | — | — | Q8: "Who trained you and in what?" |
| `<textarea>` | textarea | `attr_bio_q08` | ~3 rows |
| Static label | — | — | Q9: "Are you close to family?" |
| `<textarea>` | textarea | `attr_bio_q09` | ~3 rows |
| Static label | — | — | Q10: "What is the current state of that relationship?" |
| `<textarea>` | textarea | `attr_bio_q10` | ~3 rows |
| Static label | — | — | Q11: "Current love interest?" |
| `<textarea>` | textarea | `attr_bio_q11` | ~3 rows |
| Static label | — | — | Q12: "Are you in a relationship?" |
| `<textarea>` | textarea | `attr_bio_q12` | ~3 rows |
| Static label | — | — | Q13: "What has been your greatest love?" |
| `<textarea>` | textarea | `attr_bio_q13` | ~3 rows |
| Static label | — | — | Q14: "What are your bathing habits?" |
| `<textarea>` | textarea | `attr_bio_q14` | ~3 rows |
| Static label | — | — | Q15: "Have you killed anyone?" |
| `<textarea>` | textarea | `attr_bio_q15` | ~3 rows |
| Static label | — | — | Q16: "Have you been jailed or imprisoned?" |
| `<textarea>` | textarea | `attr_bio_q16` | ~3 rows |
| Static label | — | — | Q17: "How do you look and dress?" |
| `<textarea>` | textarea | `attr_bio_q17` | ~3 rows |
| Static label | — | — | Q18: "What are your noticeable mannerisms?" |
| `<textarea>` | textarea | `attr_bio_q18` | ~3 rows |
| Static label | — | — | Q19: "What are your greatest virtues?" |
| `<textarea>` | textarea | `attr_bio_q19` | ~3 rows |
| Static label | — | — | Q20: "What are your greatest flaws?" |
| `<textarea>` | textarea | `attr_bio_q20` | ~3 rows |

---

### Section 3: Repeating Section Row Templates

Concise summary of all 7 repeating sections: groupname, field count, and per-row field inventory.

---

**`repeating_skills`**
`data-groupname="repeating_skills"` — 9 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_skill_name` | `""` | Skill name |
| `<select>` | select | `attr_skill_linked_attr` | `body` | `<select>` element |
| `<input>` | text | `attr_skill_general` | `""` | Category |
| `<input>` | text | `attr_skill_spec` | `""` | Specialization |
| `<input>` | number | `attr_skill_base` | `0` | Base rating |
| `<input>` | number | `attr_skill_foci` | `0` | Foci bonus |
| `<input>` | number | `attr_skill_misc` | `0` | Misc modifier |
| `<input>` | number | `attr_skill_total` | `0` | `readonly`; worker computed |
| `<button>` | roll | `roll_btn_skill_roll` | — | Roll button |

---

**`repeating_spells`**
`data-groupname="repeating_spells"` — 8 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_spell_name` | `""` | Spell name |
| `<select>` | select | `attr_spell_type` | `M` | `<select>` element |
| `<select>` | select | `attr_spell_duration` | `I` | `<select>` element |
| `<input>` | text | `attr_spell_target` | `""` | Target |
| `<input>` | number | `attr_spell_force` | `0` | Force rating |
| `<input>` | text | `attr_spell_drain` | `""` | Drain code string |
| `<button>` | roll | `roll_btn_cast_spell` | — | Roll button |
| `<button>` | roll | `roll_btn_drain_resist` | — | Roll button |

---

**`repeating_mutations`**
`data-groupname="repeating_mutations"` — 5 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_mutation_name` | `""` | Mutation name |
| `<input>` | number | `attr_mutation_level` | `0` | Mutation level |
| `<input>` | number | `attr_mutation_essence` | `0` | Essence cost; parseFloat in worker |
| `<input>` | number | `attr_mutation_bp_cost` | `0` | BP cost |
| `<input>` | text | `attr_mutation_effect` | `""` | Wider display column |

---

**`repeating_adept_powers`**
`data-groupname="repeating_adept_powers"` — 5 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_power_name` | `""` | Power name |
| `<input>` | number | `attr_power_level` | `0` | Power level |
| `<input>` | text | `attr_power_pp_cost` | `""` | Display field; drain codes not pure integers |
| `<input>` | number | `attr_power_pp_cost_value` | `0` | CSS-hidden; worker sum target only |
| `<input>` | text | `attr_power_effect` | `""` | Wider display column |

---

**`repeating_weapons`**
`data-groupname="repeating_weapons"` — 14 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_weapon_name` | `""` | Weapon name |
| `<select>` | select | `attr_weapon_type` | `Edged` | `<select>` element |
| `<input>` | text | `attr_weapon_modifiers` | `""` | Modifier text |
| `<input>` | number | `attr_weapon_power` | `0` | Power rating |
| `<input>` | text | `attr_weapon_damage` | `""` | Damage code string |
| `<input>` | number | `attr_weapon_conceal` | `0` | Conceal rating |
| `<input>` | number | `attr_weapon_reach` | `0` | Reach rating |
| `<input>` | number | `attr_weapon_ep` | `0` | Feeds ep_total sum |
| `<input>` | text | `attr_weapon_range_short` | `""` | Short range |
| `<input>` | text | `attr_weapon_range_medium` | `""` | Medium range |
| `<input>` | text | `attr_weapon_range_long` | `""` | Long range |
| `<input>` | text | `attr_weapon_range_extreme` | `""` | Extreme range |
| `<button>` | roll | `roll_btn_attack_ranged` | — | Roll button |
| `<button>` | roll | `roll_btn_attack_melee` | — | Roll button |

---

**`repeating_equipment`**
`data-groupname="repeating_equipment"` — 3 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_equip_name` | `""` | Equipment name |
| `<input>` | text | `attr_equip_description` | `""` | Description |
| `<input>` | number | `attr_equip_ep` | `0` | Feeds ep_total sum |

---

**`repeating_contacts`**
`data-groupname="repeating_contacts"` — 3 fields per row

| Field | Input type | `name=` in row | Default | Notes |
|---|---|---|---|---|
| `<input>` | text | `attr_contact_name` | `""` | Contact name |
| `<input>` | text | `attr_contact_info` | `""` | Contact info |
| `<select>` | select | `attr_contact_level` | `1` | `<select>` element — stored value is the integer (1/2/3); option display labels are "1-Contact" / "2-Buddy" / "3-Friend" |

---

*(Part B complete — continues in Part C)*

---


---

## Phase 2 — HTML Skeleton Blueprint (Part C)

*(Sections 4–6 — final segment of the Phase 2 blueprint)*

---

### Section 4: Hidden and Worker-Only Input Inventory

These are inputs present in the HTML but not primary user-entry fields. Required for K-scaffold to read/write computed values via `getAttrs()` / `setAttrs()`.

**Category A — `type="hidden"` inputs:** Worker-only fields never displayed to the player. Sheet Worker writes them; CSS reads them via attribute selector for state styling.

**Category B — Readonly visible inputs:** Worker-computed fields displayed to the player but not directly editable. Use `type="text"` or `type="number"` with the `readonly` attribute.

---

#### Table A — Hidden inputs (`type="hidden"`)

| Field | `name=` | Default | Location in DOM | Notes |
|---|---|---|---|---|
| `char_db_id` | `attr_char_db_id` | `""` | Hidden-infrastructure div | Companion sync: Turso character record ID |
| `char_sync_version` | `attr_char_sync_version` | `0` | Hidden-infrastructure div | Increments each successful sync; used for conflict detection |
| `campaign_db_id` | `attr_campaign_db_id` | `""` | Hidden-infrastructure div | Companion sync: Turso campaign record ID |
| `reaction_base` | `attr_reaction_base` | `0` | Core tab — Attributes region | Worker: `floor((int + dex) / 2)` |
| `pool_spell_base` | `attr_pool_spell_base` | `0` | Core tab — Dice Pools region | Worker-computed base before `pool_spell_misc` modifier |
| `pool_combat_base` | `attr_pool_combat_base` | `0` | Core tab — Dice Pools region | Worker-computed base before `pool_combat_misc` modifier |
| `pool_control_base` | `attr_pool_control_base` | `0` | Core tab — Dice Pools region | Worker-computed base before `pool_control_misc` modifier |
| `pool_astral_base` | `attr_pool_astral_base` | `0` | Core tab — Dice Pools region | Worker-computed base before `pool_astral_misc` modifier |
| `tn_warning_level` | `attr_tn_warning_level` | `0` | Magic tab — immediately before `.sheet-tn-warning` element | **CRITICAL:** CSS sibling selector dependency; see Developer Note 4 |

---

#### Table B — Readonly visible inputs (`readonly` attribute)

[CARRY-FORWARD NOTE — Table B count resolved]: The 29 fields below are the complete set of worker-computed visible inputs, verified against the Phase 1 scalar registry. The "(32 total)" figure in the original spec was a documentation error — 29 is the correct count.

| Field | `name=` | Type | Default | Location | Notes |
|---|---|---|---|---|---|
| `body` | `attr_body` | number | `0` | Core tab — Attributes table | `body_base + body_mutations + body_magic + body_misc` |
| `dex` | `attr_dex` | number | `0` | Core tab — Attributes table | `dex_base + dex_mutations + dex_magic + dex_misc` |
| `str` | `attr_str` | number | `0` | Core tab — Attributes table | `str_base + str_mutations + str_magic + str_misc` |
| `cha` | `attr_cha` | number | `0` | Core tab — Attributes table | `cha_base + cha_mutations + cha_magic + cha_misc` |
| `int` | `attr_int` | number | `0` | Core tab — Attributes table | `int_base + int_mutations + int_magic + int_misc` |
| `wil` | `attr_wil` | number | `0` | Core tab — Attributes table | `wil_base + wil_mutations + wil_magic + wil_misc` |
| `hum` | `attr_hum` | number | `0` | Core tab — Attributes table | `hum_base + hum_mutations + hum_magic + hum_misc` |
| `mag` | `attr_mag` | number | `0` | Core tab — Attributes table | `mag_base + mag_misc` — no mutations or magic sub-categories for mag |
| `reaction` | `attr_reaction` | number | `0` | Core tab — Attributes table | `reaction_base + reaction_misc` |
| `pool_spell` | `attr_pool_spell` | number | `0` | Core tab — Dice Pools table | `pool_spell_base + pool_spell_misc` |
| `pool_combat` | `attr_pool_combat` | number | `0` | Core tab — Dice Pools table | `pool_combat_base + pool_combat_misc` |
| `pool_control` | `attr_pool_control` | number | `0` | Core tab — Dice Pools table | `pool_control_base + pool_control_misc` |
| `pool_astral` | `attr_pool_astral` | number | `0` | Core tab — Dice Pools table | `pool_astral_base + pool_astral_misc` |
| `init_score` | `attr_init_score` | number | `0` | Core tab — Initiative row | Worker-computed initiative base |
| `karma_total` | `attr_karma_total` | number | `0` | Core tab — Karma row | Sum of all karma sub-fields |
| `ep_total` | `attr_ep_total` | number | `0` | Gear tab — EP row | Sum of all `weapon_ep` + `equip_ep` repeating values |
| `ep_max` | `attr_ep_max` | number | `0` | Gear tab — EP row | EP capacity cap; readonly display |
| `armor_total_piercing` | `attr_armor_total_piercing` | number | `0` | Armor panel — totals row | Column sum of all `armor_*_piercing` values |
| `armor_total_slashing` | `attr_armor_total_slashing` | number | `0` | Armor panel — totals row | Column sum of all `armor_*_slashing` values |
| `armor_total_impact` | `attr_armor_total_impact` | number | `0` | Armor panel — totals row | Column sum of all `armor_*_impact` values |
| `cm_tn_mod` | `attr_cm_tn_mod` | number | `0` | Core tab — header strip | Condition monitor TN penalty; worker-computed from CM track state |
| `cm_init_mod` | `attr_cm_init_mod` | number | `0` | Core tab — header strip | Condition monitor initiative penalty; worker-computed from CM track state |
| `power_points_max` | `attr_power_points_max` | number | `0` | Skills tab — Adept Powers header | `= mag` (direct copy of computed magic rating total) |
| `power_points_used` | `attr_power_points_used` | number | `0` | Skills tab — Adept Powers header | Sum of all `power_pp_cost_value` in `repeating_adept_powers` |
| `power_points_remaining` | `attr_power_points_remaining` | number | `0` | Skills tab — Adept Powers header | `power_points_max − power_points_used` |
| `essence_total` | `attr_essence_total` | number | `0` | Skills tab — Mutations header | Running essence value after all mutations applied |
| `sustained_tn_mod` | `attr_sustained_tn_mod` | number | `0` | Magic tab — summary row | TN penalty from sustained spells: `spells_sustained × 2` |
| `sync_status` | `attr_sync_status` | text | `"Never synced"` | Core tab — header strip | Displays feedback string e.g. `"Synced ✓"`; `type="text"` |
| `skill_total` | `attr_skill_total` | number | `0` | `repeating_skills` row template | Readonly per-row computed total |

---

### Section 5: Roll Button and Action Button Stub Registry

**Total button count: 18** (9 attribute + 1 initiative + 2 combat + 5 repeating + 1 action)

> Note: `btn_pull_db` is V2 scope — NOT included in V1 per DECISION-08.

| Button ID | Button type | `name=` attribute | Stub value | Location | Notes |
|---|---|---|---|---|---|
| `btn_roll_body` | roll | `roll_btn_roll_body` | `"0"` | Core tab — Attributes table | Triggers body pool roll |
| `btn_roll_dex` | roll | `roll_btn_roll_dex` | `"0"` | Core tab — Attributes table | Triggers dex pool roll |
| `btn_roll_str` | roll | `roll_btn_roll_str` | `"0"` | Core tab — Attributes table | Triggers str pool roll |
| `btn_roll_cha` | roll | `roll_btn_roll_cha` | `"0"` | Core tab — Attributes table | Triggers cha pool roll |
| `btn_roll_int` | roll | `roll_btn_roll_int` | `"0"` | Core tab — Attributes table | Triggers int pool roll |
| `btn_roll_wil` | roll | `roll_btn_roll_wil` | `"0"` | Core tab — Attributes table | Triggers wil pool roll |
| `btn_roll_hum` | roll | `roll_btn_roll_hum` | `"0"` | Core tab — Attributes table | Triggers hum pool roll |
| `btn_roll_reaction` | roll | `roll_btn_roll_reaction` | `"0"` | Core tab — Attributes table | Triggers reaction pool roll |
| `btn_roll_mag` | roll | `roll_btn_roll_mag` | `"0"` | Core tab — Attributes table | Triggers mag pool roll |
| `btn_init_roll` | roll | `roll_btn_init_roll` | `"0"` | Core tab — Initiative row | Triggers initiative roll |
| `btn_dodge` | roll | `roll_btn_dodge` | `"0"` | Core tab — Combat Panel | Triggers dodge pool roll |
| `btn_damage_resist_body` | roll | `roll_btn_damage_resist_body` | `"0"` | Core tab — Combat Panel | Triggers damage resistance roll |
| `btn_skill_roll` | roll | `roll_btn_skill_roll` | `"0"` | `repeating_skills` row template | Per-row skill roll |
| `btn_cast_spell` | roll | `roll_btn_cast_spell` | `"0"` | `repeating_spells` row template | Per-row spell casting roll |
| `btn_drain_resist` | roll | `roll_btn_drain_resist` | `"0"` | `repeating_spells` row template | Per-row drain resistance roll |
| `btn_attack_ranged` | roll | `roll_btn_attack_ranged` | `"0"` | `repeating_weapons` row template | Per-row ranged attack roll |
| `btn_attack_melee` | roll | `roll_btn_attack_melee` | `"0"` | `repeating_weapons` row template | Per-row melee attack roll |
| `btn_sync_db` | action | `act_btn_sync_db` | N/A | Core tab — header strip | No `value` attr; fires `clicked:btn_sync_db` Sheet Worker event; does NOT emit a chat roll |

---

### Section 6: Developer Guidance Notes

**Note 1 — K-scaffold `name=` conventions**

- Scalar input fields: `name="attr_{fieldname}"`
- Roll buttons (dice-rolling): `name="roll_btn_{name}"` with `type="roll"` — e.g. `roll_btn_roll_body`. The Sheet Worker event fires as `clicked:btn_{name}` (K-scaffold strips the `roll_btn_` prefix). **DO NOT** use `name="roll_{name}"` — the `_btn_` segment is required.
- Action buttons (Sheet Worker events only, no dice): `name="act_btn_{name}"` with `type="action"` — fires `clicked:btn_{name}` event
- Repeating section fieldset: `data-groupname="repeating_{sectionname}"`
- Repeating section row template: inner `<div>` is the row template; K-scaffold handles add/remove controls automatically

[CARRY-FORWARD NOTE — K-scaffold version]: Confirm these naming conventions against the specific K-scaffold version in use. Some K-scaffold versions auto-generate the `name=` attributes; others require manual declaration. Auto-generation behavior differs across major versions.

---

**Note 2 — `readonly` vs `type="hidden"`**

- Use `readonly` (visible input) for any value the player needs to **see** — computed totals, dice pools, condition modifier displays
- Use `type="hidden"` for values the player never sees directly but Sheet Workers must read/write — `reaction_base`, pool bases, `tn_warning_level`, sync infrastructure fields
- Do **NOT** use the `disabled` attribute — Roll20's `getAttrs()` cannot read disabled inputs in some configurations
- All computed fields still require an HTML element — Roll20 stores attributes server-side but only updates the DOM element if an input with the matching `name=` exists
- Checkboxes **must** include `value="1"` — without it, Roll20 stores the string `"on"` when checked, breaking Sheet Worker comparisons to numeric `1`

---

**Note 3 — Tab radio/label pattern (CSS visibility)**

The standard Roll20 tab pattern uses radio inputs + CSS `~` sibling selector:

```html
<input type="radio" name="sheet-tab-nav" id="tab-core-radio" value="core" checked>
<label for="tab-core-radio" class="sheet-tab-label">Core</label>
<!-- ...other tab radios/labels... -->

<div class="sheet-tab-panel sheet-tab-core">...</div>

/* CSS: */
/* .sheet-tab-panel { display: none; } */
/* #tab-core-radio:checked ~ .sheet-tab-panel.sheet-tab-core { display: block; } */
```

All tab radio inputs must appear in the DOM **before** all tab panel divs for the `~` selector to work. Default active tab: `tab-core` carries the `checked` attribute.

---

**Note 4 — `tn_warning_level` sibling ordering (CRITICAL)**

The `<input type="hidden" name="attr_tn_warning_level">` must appear **immediately before** the `.sheet-tn-warning` element in the DOM. The CSS attribute selector `input[name="attr_tn_warning_level"][value="1"] ~ .sheet-tn-warning` requires the input to be a preceding sibling of the warning display element. If this ordering is violated, the CSS warning states will never activate.

---

**Note 5 — Compact mode toggle ordering (CRITICAL)**

The `<input type="checkbox" name="attr_sheet_compact_mode" id="sheet-compact-mode">` must appear **before all tab panel divs** in the DOM. The CSS general sibling selector `#sheet-compact-mode:checked ~ .sheet-compact-target` requires the checkbox to precede all `.sheet-compact-target` elements. Placement: after the hidden-infrastructure div, before the tab radio inputs.

---

**Note 6 — Condition monitor radio group pattern**

Each condition track (`cm_mental`, `cm_stun`, `cm_physical`) uses a **radio group** where all radios share the same `name=` attribute (e.g., `name="attr_cm_mental"`) and have `value="0"` through `value="4"`. Stun and physical tracks additionally include `value="5"` for the Unconscious tier. The selected radio's integer value is the stored character attribute. CSS `:checked` pseudo-class drives per-tier visual highlighting.

Do **NOT** use separate boolean checkboxes per tier — the radio group pattern is the only correct implementation for this mechanic.

---

**Note 7 — Phase 3 stub values**

All `<button type="roll">` elements carry `value="0"` as a placeholder. Phase 3 replaces these with production roll formula strings (e.g., `&{template:skill} {{charname=@{char_name}}} ...`). The stub `"0"` is a safe placeholder: if accidentally clicked during development it produces a plain d0 roll and does not cause errors.

---

*Phase 2 blueprint complete. All three parts (A, B, C) form the complete HTML Skeleton Blueprint.*
