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

---


---

## Phase 3 — Sheet Worker Blueprint

**Goal:** Produce the complete specification for the K-scaffold Sheet Worker script. After this phase a Developer has everything needed to implement `sheet.html`'s `<script type="text/worker">` block without making any logic, formula, or sequencing decisions.

**Input:** Layer 3 Phase 1 (122-field naming contract + 7 repeating section schemas), Layer 3 Phase 2 (HTML skeleton — all inputs, buttons, DOM ordering), Layer 2 Phase 3 specification (Tasks 3.1–3.17 + Critical Failure Amendment).

**Phase 3 does NOT cover:** HTML structure (Phase 2), CSS (Phase 4), companion app (Phase 5).

---

### Section 1: K-scaffold Worker Script Skeleton

The `<script type="text/worker">` block in `sheet.html` is organized into 5 sequential regions:

```
// ═══════════════════════════════════════════════════════════
// REGION 1 — K-scaffold initialization + version block
// ═══════════════════════════════════════════════════════════
// k.version = '...';   // Required by K-scaffold — fill with installed version string

// ═══════════════════════════════════════════════════════════
// REGION 2 — Constants
// ═══════════════════════════════════════════════════════════
// SYNC_PROXY_URL = '';  // Cloudflare Worker proxy URL — fill after deployment
// REPEATING_SECTIONS = [
//   'repeating_skills', 'repeating_spells', 'repeating_mutations',
//   'repeating_adept_powers', 'repeating_weapons', 'repeating_equipment',
//   'repeating_contacts'
// ];

// ═══════════════════════════════════════════════════════════
// REGION 3 — Computed field worker registrations
// ═══════════════════════════════════════════════════════════
// k.registerFuncs({ ... });  // See Section 5 for complete registration map

// ═══════════════════════════════════════════════════════════
// REGION 4 — Sheet opens handler
// ═══════════════════════════════════════════════════════════
// k.sheetOpens(() => { /* trigger full cascade recalculation */ });

// ═══════════════════════════════════════════════════════════
// REGION 5 — Event-driven handlers (non-cascade)
// ═══════════════════════════════════════════════════════════
// on('clicked:btn_sync_db', syncHandler);  // V1 outbound sync only
```

**Region notes:**
- **Region 1–2:** Script setup — runs once on parse
- **Region 3:** K-scaffold builds its internal dependency graph from `trigger` / `affects` declarations here. Execution order within this block does not matter — K-scaffold resolves it topologically
- **Region 4:** `k.sheetOpens` triggers full cascade recalculation on sheet load; see Section 7.6
- **Region 5:** Button-click handlers NOT in the cascade. Only `btn_sync_db` in V1

---

### Section 2: Computed Field Worker Specifications

**K-scaffold registration pattern (used for all cascade workers):**

```
k.registerFuncs({
  workerFunctionName: {
    name: 'workerFunctionName',
    trigger: ['triggerField1', 'triggerField2'],  // attribute changes that fire this worker
    affects: ['outputField'],                      // what this worker computes — used for graph ordering
    callback: function(attrs) {
      // attrs.outputField = formula using attrs.triggerField1 etc.
      // return attrs;
    }
  }
});
```

`trigger` defines which attribute changes fire the worker. `affects` declares outputs — K-scaffold guarantees any worker whose `trigger` includes a field in this `affects` array fires AFTER this worker resolves.

---

#### Layer 2 — Core Attribute Total Workers (8 workers)

**Fires on:** any change to raw sub-fields (leaf inputs — no computed dependencies).

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcBody` | `body_base`, `body_mutations`, `body_magic`, `body_misc` | `body` | `base + mutations + magic + misc` |
| `calcDex` | `dex_base`, `dex_mutations`, `dex_magic`, `dex_misc` | `dex` | same pattern |
| `calcStr` | `str_base`, `str_mutations`, `str_magic`, `str_misc` | `str` | same pattern |
| `calcCha` | `cha_base`, `cha_mutations`, `cha_magic`, `cha_misc` | `cha` | same pattern |
| `calcInt` | `int_base`, `int_mutations`, `int_magic`, `int_misc` | `int` | same pattern |
| `calcWil` | `wil_base`, `wil_mutations`, `wil_magic`, `wil_misc` | `wil` | same pattern |
| `calcHum` | `hum_base`, `hum_mutations`, `hum_magic`, `hum_misc` | `hum` | same pattern |
| `calcMag` | `mag_base`, `mag_misc` | `mag` | `base + misc` — **no `_mutations` or `_magic` fields** |

**Formula detail:** `parseInt(base, 10) + parseInt(mutations, 10) + parseInt(magic, 10) + parseInt(misc, 10)` — integer addition, no rounding, no floor. All sub-fields are integers. `parseInt` guards against Roll20 returning attribute values as strings.

[CARRY-FORWARD NOTE — parseInt required for ALL addition-based workers]: Roll20's `getAttrs()` callback returns every attribute value as a string regardless of the declared type in `sheet.json`. JavaScript's `+` operator performs **string concatenation** on string operands, not numeric addition. This guard is not limited to L2 attribute workers — it applies to every formula that uses `+` to add values read from `attrs`. Affected workers (all must coerce with `parseInt(value, 10) || 0`): `calcReactionBase` (`int + dex`), `calcInitScore` (`reaction + init_reaction_mod + init_misc_mod`), all L4b pool total workers (`base + misc`), `calcArmorTotals` (all three sum expressions), `calcKarmaTotal` (`karma_good + karma_used`), and `calcPowerPointsRemaining` (`power_points_max - power_points_used`). Workers using only `Math.floor`, `Math.max`, `Math.min`, or `*` operators are unaffected (JS coerces operands for those). Section 7.2 covers `parseFloat` for decimal fields specifically.

[CARRY-FORWARD NOTE — mag exception]: `mag` has no `_mutations` or `_magic` sub-fields by design (magic rating cannot itself be modified by mutations or magic — it is the source of those effects). `calcMag` watches only `mag_base` and `mag_misc`. Do not add `mag_mutations` or `mag_magic` to the trigger set.

---

#### Layer 3 — Reaction Workers

**Fires after:** L2 `calcInt` and `calcDex` resolve (K-scaffold cascade guarantee via their `affects: ['int']` / `affects: ['dex']` declarations).

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcReactionBase` | `int`, `dex` | `reaction_base` | `Math.floor((int + dex) / 2)` |
| `calcReaction` | `reaction_base`, `reaction_misc` | `reaction` | `Math.max(1, reaction_base + reaction_misc)` |

[CARRY-FORWARD NOTE — reaction floor]: `reaction` must apply `Math.max(1, result)` before writing. If `int + dex = 0` (fully debuffed edge case), `reaction_base = 0` and `reaction = 0 + misc`. If misc is also 0, the floor prevents `reaction = 0`. Roll20's `@{reaction}d6` with reaction = 0 produces an error or no roll. The floor applies to the **final `reaction` output only** — `reaction_base` may legitimately be 0. See Section 7.4 for full rationale.

---

#### Layer 4a — Dice Pool Base Workers (4 workers)

**Fires after:** L2 attribute total workers and L3 reaction worker resolve.

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcPoolSpellBase` | `cha`, `int`, `wil` | `pool_spell_base` | `Math.max(0, Math.floor((cha + int + wil) / 2))` |
| `calcPoolCombatBase` | `dex`, `int`, `wil` | `pool_combat_base` | `Math.max(0, Math.floor((dex + int + wil) / 2))` |
| `calcPoolControlBase` | `reaction` | `pool_control_base` | `reaction` (direct copy — no arithmetic) |
| `calcPoolAstralBase` | `int`, `wil`, `mag` | `pool_astral_base` | `Math.max(0, Math.floor((int + wil + mag) / 3))` |

**Floor behavior:** All 4 base outputs clamp at 0 via `Math.max(0, computed)`. A pool of 0 is valid — the player has no dice to spend from that pool. Negative totals must not propagate.

---

#### Layer 4b — Dice Pool Total Workers (4 workers)

**Fires after:** L4a pool base workers resolve.

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcPoolSpell` | `pool_spell_base`, `pool_spell_misc` | `pool_spell` | `Math.max(0, pool_spell_base + pool_spell_misc)` |
| `calcPoolCombat` | `pool_combat_base`, `pool_combat_misc` | `pool_combat` | `Math.max(0, pool_combat_base + pool_combat_misc)` |
| `calcPoolControl` | `pool_control_base`, `pool_control_misc` | `pool_control` | `Math.max(0, pool_control_base + pool_control_misc)` |
| `calcPoolAstral` | `pool_astral_base`, `pool_astral_misc` | `pool_astral` | `Math.max(0, pool_astral_base + pool_astral_misc)` |

**Note:** `pool_*_misc` fields are player-editable and may be negative (debuffs). `Math.max(0, total)` prevents a negative misc modifier from driving the displayed pool below zero.

---

#### Layer 4c — Initiative Score Worker

**Fires after:** L3 `calcReaction` resolves.

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcInitScore` | `reaction`, `init_reaction_mod`, `init_misc_mod` | `init_score` | `reaction + init_reaction_mod + init_misc_mod` |

**Note:** No floor applied. `init_score` can be negative under extreme debuffs — this is a valid narrative state. The roll formula `@{init_dice}d6 + @{init_score}` handles a negative `init_score` correctly in Roll20 (sum result can be negative).

---

#### Layer 5 — Aggregate Workers

**Fires after:** relevant L2–L4 workers resolve, or on repeating section row changes.

##### L5a — Encumbrance

| Worker name | Trigger fields | Output field | Formula |
|---|---|---|---|
| `calcEpMax` | `str`, `body` | `ep_max` | `Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)` |
| `calcEpTotal` | `repeating_weapons:weapon_ep`, `repeating_equipment:equip_ep` (all rows) | `ep_total` | `parseFloat` sum across both sections |

[CARRY-FORWARD NOTE — cross-section repeating iteration for ep_total]: `calcEpTotal` must iterate two sections in one pass. Use K-scaffold's `k.getAllAttrs` with both section names. Guard each row value: `parseFloat(row.weapon_ep || 0)` and `parseFloat(row.equip_ep || 0)`. An empty section must contribute 0, not NaN. `weapon_ep` and `equip_ep` are integer fields but may arrive as strings from Roll20.

##### L5b — Armor Totals

| Worker name | Trigger fields (all 9) | Output fields | Formulas |
|---|---|---|---|
| `calcArmorTotals` | `armor_torso_piercing`, `armor_torso_slashing`, `armor_torso_impact`, `armor_legs_piercing`, `armor_legs_slashing`, `armor_legs_impact`, `armor_head_piercing`, `armor_head_slashing`, `armor_head_impact` | `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact` | Sum of 3 locations per type; all three outputs in one combined handler |

**Formulas:**
```
armor_total_piercing = torso_piercing + legs_piercing + head_piercing
armor_total_slashing = torso_slashing + legs_slashing + head_slashing
armor_total_impact   = torso_impact   + legs_impact   + head_impact
```

All inputs are integers. No `parseFloat` needed. No floor needed.

##### L5c — Skill Total (per repeating row)

| Worker name | Trigger (per row) | Output (per row) | Formula |
|---|---|---|---|
| `calcSkillTotal` | `skill_base`, `skill_foci`, `skill_misc` | `skill_total` | `skill_base + skill_foci + skill_misc` |

**Registration note:** Registered as a repeating section row worker. K-scaffold fires it within the context of the changed row and writes `skill_total` back to that row only. Does not iterate all rows.

**Comment in code (not logic):** `// If skill_total = 0 at roll time, player rolls linked attribute at +4 TN. Not sheet-enforced — player responsibility.`

##### L5d — Adept Power Points (3 workers)

| Worker name | Trigger | Output | Formula |
|---|---|---|---|
| `calcPowerPointsMax` | `mag` | `power_points_max` | `mag` (direct copy) |
| `calcPowerPointsUsed` | `repeating_adept_powers:power_pp_cost_value` (all rows) | `power_points_used` | `parseFloat` sum of all `power_pp_cost_value` across all rows |
| `calcPowerPointsRemaining` | `power_points_max`, `power_points_used` | `power_points_remaining` | `power_points_max - power_points_used` |

[CARRY-FORWARD NOTE — decimal arithmetic for power_pp_cost_value]: PP costs are decimals (e.g., 0.25, 0.5, 1.5). Always `parseFloat(row.power_pp_cost_value || 0)`, never `parseInt`. `parseInt(0.25)` returns `0` — every decimal cost would silently be treated as free. `power_points_remaining` will also be a decimal — do not round. See Section 7.2.

[CARRY-FORWARD NOTE — power_pp_cost vs power_pp_cost_value]: The text display field `power_pp_cost` (e.g., `"0.25/level"`) is player-reference only. The worker MUST use `power_pp_cost_value` (number field) as the sum source. The L2 Phase 3 spec and L3 Phase 1 blueprint both confirm this. `power_pp_cost` must NOT be used as a trigger or sum source.

##### L5e — Essence Total

| Worker name | Trigger | Output | Formula |
|---|---|---|---|
| `calcEssenceTotal` | `repeating_mutations:mutation_essence` (all rows) | `essence_total` | `parseFloat` sum of all `mutation_essence` values across all rows |

[CARRY-FORWARD NOTE — decimal arithmetic for mutation_essence]: Essence costs are decimals (e.g., 0.2, 1.15). Always `parseFloat(row.mutation_essence || 0)`. Guard empty section → 0, not NaN.

---

#### Layer 6 — Modifier Workers

**Fires on:** player-edited inputs directly (not downstream of other workers).

##### L6a — Karma Total

| Worker name | Trigger fields | Output | Formula |
|---|---|---|---|
| `calcKarmaTotal` | `karma_good`, `karma_used` | `karma_total` | `karma_good + karma_used` |

No floor, no rounding.

##### L6b — Condition Monitor Penalties (combined handler)

| Worker name | Trigger fields | Output fields | Formulas |
|---|---|---|---|
| `calcCmPenalties` | `cm_mental`, `cm_stun`, `cm_physical` | `cm_tn_mod`, `cm_init_mod` | See below |

**Penalty mapping:** `penaltyOf = (level) => Math.min(parseInt(level, 10) || 0, 3)`

```
cm_tn_mod  = Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))
cm_init_mod = -1 * cm_tn_mod
```

Both outputs computed in one handler (same trigger set). `cm_init_mod` is always the negative of `cm_tn_mod`.

**CM Level → Penalty reference:**

| Level | State | TN Penalty | Init Penalty |
|---|---|---|---|
| 0 | Clean | 0 | 0 |
| 1 | Light | +1 | −1 |
| 2 | Moderate | +2 | −2 |
| 3 | Serious | +3 | −3 |
| 4 | Deadly | +3 (capped) | −3 (capped) |
| 5 | Unconscious | +3 (capped) | −3 (capped) |

Level 4+ caps at 3 — Deadly is a narrative incapacitation state, not a higher mechanical penalty. `Math.min(level, 3)` implements the cap.

##### L6c — Sustained Spell TN + Warning Level (combined handler)

| Worker name | Trigger | Output fields | Formulas |
|---|---|---|---|
| `calcSustainedPenalty` | `spells_sustained` | `sustained_tn_mod`, `tn_warning_level` | See below |

```
sustained_tn_mod = spells_sustained * 2

tn_warning_level:
  if sustained_tn_mod >= 6  → 3  (red)
  else if sustained_tn_mod >= 4  → 2  (orange)
  else if sustained_tn_mod >= 2  → 1  (amber)
  else                           → 0  (no warning)
```

[CARRY-FORWARD NOTE — tn_warning_level DOM dependency]: This worker writes `tn_warning_level` as a hidden input (integer 0–3). CSS drives warning colors via `input[name="attr_tn_warning_level"][value="1"] ~ .sheet-tn-warning`. Roll20 updates the `value` attribute on `setAttrs` for hidden inputs. The `value` must be written as a string matching the CSS selector exactly (e.g., `"1"`, `"2"`, `"3"`). The DOM ordering constraint (hidden input immediately before `.sheet-tn-warning`) is a Phase 2 requirement — the worker itself has no DOM awareness. See Phase 4 Amendment 4-A.

---

### Section 3: Roll Template HTML Blueprints

Roll templates are defined in `sheet.html` as `<rolltemplate class="sheet-rolltemplate-{name}">` blocks. They appear **outside the tab structure** — after all tab panel `<div>`s, before the end of the document. They do not interact with the CSS tab system.

**General Mustache structure (all 3 templates follow this pattern):**

```html
<rolltemplate class="sheet-rolltemplate-{name}">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-{name}">
      <!-- charname + rollname — colored background defined in Phase 4 CSS -->
    </div>
    <div class="sheet-template-body">
      <!-- parameter rows -->
      <!-- {{^successes}} warning block at bottom of body -->
    </div>
  </div>
</rolltemplate>
```

**Roll20 Mustache conditionals:**
- `{{#paramName}}...{{/paramName}}` — renders block only if `paramName` is present and non-empty/non-zero
- `{{^paramName}}...{{/paramName}}` — renders block only if `paramName` is absent, empty, or zero
- Roll20 treats `successes = 0` (no hits from the inline roll) as falsy — `{{^successes}}` fires on any zero-success result

---

#### Template: `rolltemplate-skill`

**CSS class:** `.sheet-rolltemplate-skill`
**Header background:** `#1a1a2e` (dark navy — Phase 4 locked color token)
**Used by:** all 9 attribute roll buttons, `btn_skill_roll` (per skill row), `btn_dodge`, `btn_damage_resist_body`

**Parameter bindings:**

| Mustache key | Source | Required | Display location |
|---|---|---|---|
| `{{charname}}` | `@{char_name}` | Yes | Header bar |
| `{{rollname}}` | Hardcoded string (e.g., `"Body"`) or `@{skill_name}` | Yes | Header bar |
| `{{linked_attr}}` | `@{skill_linked_attr}` | Optional (skill rolls only; omit for raw attribute rolls) | Body row — hidden when not passed via `{{#linked_attr}}` conditional |
| `{{tn}}` | `?{Target Number\|4}` | Yes | Body row |
| `{{successes}}` | `[[Nd6cs>=TN cf<=1]]` inline roll | Yes | Body row (central result display) |
| `{{^successes}}` warning | Automatic (fires when successes = 0) | Auto | Body row below successes |

**`{{^successes}}` warning text:** `⚠ No successes — check dice tray. All red dice = Critical Failure.`

**Structural skeleton:**

```html
<rolltemplate class="sheet-rolltemplate-skill">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-skill">
      {{charname}} — {{rollname}}
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
        ⚠ No successes — check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

[CARRY-FORWARD NOTE — linked_attr parameter naming (CRITICAL)]: The parameter name is `linked_attr`. Layer 2 Task 3.15 incorrectly used `{{linked=@{skill_linked_attr}}}` in the button formula. The template Mustache block is `{{#linked_attr}}` / `{{/linked_attr}}`. If the button formula passes `{{linked=...}}`, Roll20 silently ignores the unrecognized parameter and the linked attribute row never renders. The roll button formula (Section 4) and this template skeleton are both authoritative. The L2 formula is wrong.

---

#### Template: `rolltemplate-attack`

**CSS class:** `.sheet-rolltemplate-attack`
**Header background:** `#3a1c1c` (dark maroon — Phase 4 locked color token)
**Used by:** `btn_attack_ranged`, `btn_attack_melee` (both in `repeating_weapons`)

**Parameter bindings:**

| Mustache key | Source | Required | Display |
|---|---|---|---|
| `{{charname}}` | `@{char_name}` | Yes | Header |
| `{{rollname}}` | `"Ranged Attack"` or `"Melee Attack"` | Yes | Header |
| `{{weapon_name}}` | `@{weapon_name}` | Yes | Body |
| `{{tn}}` | Query at roll time | Yes | Body |
| `{{successes}}` | `[[Nd6cs>=TN cf<=1]]` | Yes | Body (central) |
| `{{damage_code}}` | `@{weapon_damage}` | Yes | Body (GM reference) |
| `{{power}}` | `@{weapon_power}` | Yes | Body (damage resist TN reference) |
| `{{reach}}` | `@{weapon_reach}` (melee only; not passed for ranged) | Optional | Body — `{{#reach}}` conditional |
| `{{range_band}}` | `?{Range Band\|Short}` (ranged only; not passed for melee) | Optional | Body — `{{#range_band}}` conditional |
| `{{^successes}}` warning | Automatic | Auto | Body below successes |

**Structural skeleton:**

```html
<rolltemplate class="sheet-rolltemplate-attack">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-attack">
      {{charname}} — {{rollname}}
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
        ⚠ No successes — check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

---

#### Template: `rolltemplate-spell`

**CSS class:** `.sheet-rolltemplate-spell`
**Header background:** `#1c3a5e` (dark blue — Phase 4 locked color token)
**Used by:** `btn_cast_spell`, `btn_drain_resist` (both in `repeating_spells`)

**Parameter bindings:**

| Mustache key | Source | Required | Display |
|---|---|---|---|
| `{{charname}}` | `@{char_name}` | Yes | Header |
| `{{rollname}}` | `"Cast Spell"` or `"Drain Resist"` | Yes | Header |
| `{{spell_name}}` | `@{spell_name}` | Yes | Body |
| `{{spell_type}}` | `@{spell_type}` | Yes | Body (`M` or `P`) |
| `{{spell_duration}}` | `@{spell_duration}` | Yes | Body (`I`/`S`/`P`) |
| `{{force}}` | `@{spell_force}` | Yes | Body |
| `{{tn}}` | Query at roll time | Yes | Body |
| `{{successes}}` | `[[Nd6cs>=TN cf<=1]]` | Yes | Body (central) |
| `{{drain_code}}` | `@{spell_drain}` | Yes | Body (GM reference) |
| `{{sustained_penalty}}` | `@{sustained_tn_mod}` | Yes | Body (informational — active TN mod at roll time) |
| `{{^successes}}` warning | Automatic | Auto | Body below successes |

**Structural skeleton:**

```html
<rolltemplate class="sheet-rolltemplate-spell">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-spell">
      {{charname}} — {{rollname}}
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
        ⚠ No successes — check dice tray. All red dice = Critical Failure.
      </div>
      {{/successes}}
    </div>
  </div>
</rolltemplate>
```

**SR3 Critical Failure mechanic note:**
- `cf<=1` causes Roll20 to render 1-showing dice in **red** in the dice tray
- SR3 Critical Failure condition: **all dice** in the pool show 1 — visually the entire tray is red with successes = 0
- The `{{^successes}}` warning fires on **any** zero-success result — ordinary misses AND critical failures — it is an advisory hint, not a definitive critical failure declaration; the dice tray is authoritative
- A second independent roll expression `[[Nd6cs<=1]]` for ones-counting would roll a completely separate set of dice and cannot reference the already-rolled dice — `cf<=1` on the same expression is the only correct Roll20-native implementation; see Section 7.3

---

### Section 4: Production Roll Button Formula Registry

**Convention:** Every `type="roll"` button that counts successes uses `cf<=1`. `btn_init_roll` is the only exempt button — it is a plain sum roll, not success-counting. See Section 7.3 for rationale.

| Button `name=` | Type | Location | Final `value=` |
|---|---|---|---|
| `roll_btn_roll_body` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Body}} {{tn=?{Target Number\|4}}} {{successes=[[@{body}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_dex` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Dexterity}} {{tn=?{Target Number\|4}}} {{successes=[[@{dex}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_str` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Strength}} {{tn=?{Target Number\|4}}} {{successes=[[@{str}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_cha` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Charisma}} {{tn=?{Target Number\|4}}} {{successes=[[@{cha}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_int` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Intelligence}} {{tn=?{Target Number\|4}}} {{successes=[[@{int}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_wil` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Willpower}} {{tn=?{Target Number\|4}}} {{successes=[[@{wil}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_hum` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Humanity}} {{tn=?{Target Number\|4}}} {{successes=[[@{hum}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_reaction` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Reaction}} {{tn=?{Target Number\|4}}} {{successes=[[@{reaction}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_roll_mag` | roll | Core — Attributes table | `&{template:skill} {{charname=@{char_name}}} {{rollname=Magic}} {{tn=?{Target Number\|4}}} {{successes=[[@{mag}d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_init_roll` | roll | Core — Initiative row | `@{init_dice}d6 + @{init_score}` |
| `roll_btn_dodge` | roll | Core — Combat Panel | `&{template:skill} {{charname=@{char_name}}} {{rollname=Dodge}} {{tn=4}} {{successes=[[?{Combat Pool dice for dodge\|0}d6cs>=4 cf<=1]]}}` |
| `roll_btn_damage_resist_body` | roll | Core — Combat Panel | `&{template:skill} {{charname=@{char_name}}} {{rollname=Resist Damage (Body)}} {{tn=?{TN (Power - Armor)\|0}}} {{successes=[[(@{body} + ?{Combat Pool dice\|0})d6cs>=?{TN (Power - Armor)\|0} cf<=1]]}}` |
| `roll_btn_skill_roll` | roll | `repeating_skills` row | `&{template:skill} {{charname=@{char_name}}} {{rollname=@{skill_name}}} {{linked_attr=@{skill_linked_attr}}} {{tn=?{Target Number\|4}}} {{successes=[[(@{skill_total} + ?{Pool dice to add\|0})d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_cast_spell` | roll | `repeating_spells` row | `&{template:spell} {{charname=@{char_name}}} {{rollname=Cast Spell}} {{spell_name=@{spell_name}}} {{spell_type=@{spell_type}}} {{spell_duration=@{spell_duration}}} {{force=@{spell_force}}} {{drain_code=@{spell_drain}}} {{sustained_penalty=@{sustained_tn_mod}}} {{tn=?{Target Number\|4}}} {{successes=[[(?{Sorcery dice\|0} + ?{Spell Pool dice\|0})d6cs>=?{Target Number\|4} cf<=1]]}}` |
| `roll_btn_drain_resist` | roll | `repeating_spells` row | `&{template:spell} {{charname=@{char_name}}} {{rollname=Drain Resist}} {{spell_name=@{spell_name}}} {{spell_type=@{spell_type}}} {{spell_duration=@{spell_duration}}} {{force=@{spell_force}}} {{drain_code=@{spell_drain}}} {{sustained_penalty=@{sustained_tn_mod}}} {{tn=?{Drain TN\|0}}} {{successes=[[(@{wil} + ?{Remaining Spell Pool dice\|0})d6cs>=?{Drain TN\|0} cf<=1]]}}` |
| `roll_btn_attack_ranged` | roll | `repeating_weapons` row | `&{template:attack} {{charname=@{char_name}}} {{rollname=Ranged Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{range_band=?{Range Band\|Short}}} {{tn=?{Range TN\|4}}} {{successes=[[(?{Skill dice\|0} + ?{Combat Pool dice\|0})d6cs>=?{Range TN\|4} cf<=1]]}}` |
| `roll_btn_attack_melee` | roll | `repeating_weapons` row | `&{template:attack} {{charname=@{char_name}}} {{rollname=Melee Attack}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{reach=@{weapon_reach}}} {{tn=?{TN\|4}}} {{successes=[[(?{Skill dice\|0} + ?{Combat Pool dice\|0})d6cs>=?{TN\|4} cf<=1]]}}` |
| `act_btn_sync_db` | action | Core — Header strip | N/A — no `value` attribute on action buttons; fires `clicked:btn_sync_db` event only |

**Button count: 18 total** (9 attribute + 1 initiative + 2 combat + 5 repeating + 1 action) — matches Phase 2 Section 5 registry

[CARRY-FORWARD NOTE — btn_init_roll formula (CRITICAL)]: The correct value is the plain-sum expression `@{init_dice}d6 + @{init_score}`. Layer 2 Task 3.15 showed an invalid formula mixing `/roll` prefix with `&{template:...}` — this is not valid Roll20 button syntax. `/roll` is a chat-command prefix for user input, not a button value prefix. No template. No `cs`/`cf`. This blueprint is authoritative.

[CARRY-FORWARD NOTE — linked_attr in skill roll formula (CRITICAL)]: The parameter passed in the skill roll button is `{{linked_attr=@{skill_linked_attr}}}`. Layer 2 Task 3.15 incorrectly uses `{{linked=...}}`. The Mustache template conditional is `{{#linked_attr}}` / `{{/linked_attr}}`. Using `{{linked=...}}` in the button formula causes silent failure — the linked attribute row never renders. This blueprint is authoritative.

[CARRY-FORWARD NOTE — cf<=1 mandate]: All success-counting roll expressions require `cf<=1`. `btn_init_roll` is exempt — initiative is a sum roll (SR3 critical failure mechanic does not apply to initiatives). Dodge TN is hardcoded `4` (SR3: Dodge TN is always 4). Drain Resist uses `?{Drain TN|0}` — default `0` is a safety placeholder; player must always enter the correct Drain TN derived from the spell's drain code and Force.

---

### Section 5: K-scaffold Cascade Registration Guide

The `k.registerFuncs({...})` call in Region 3 registers all 30 computed field workers. K-scaffold builds the dependency graph from `trigger` and `affects` — the order workers appear within the object does not matter; execution order is resolved topologically.

| Function name | Layer | Trigger fields | Affects (output) | Dependency constraint |
|---|---|---|---|---|
| `calcBody` | L2 | `body_base`, `body_mutations`, `body_magic`, `body_misc` | `body` | Leaf — no computed inputs |
| `calcDex` | L2 | `dex_base`, `dex_mutations`, `dex_magic`, `dex_misc` | `dex` | Leaf |
| `calcStr` | L2 | `str_base`, `str_mutations`, `str_magic`, `str_misc` | `str` | Leaf |
| `calcCha` | L2 | `cha_base`, `cha_mutations`, `cha_magic`, `cha_misc` | `cha` | Leaf |
| `calcInt` | L2 | `int_base`, `int_mutations`, `int_magic`, `int_misc` | `int` | Leaf |
| `calcWil` | L2 | `wil_base`, `wil_mutations`, `wil_magic`, `wil_misc` | `wil` | Leaf |
| `calcHum` | L2 | `hum_base`, `hum_mutations`, `hum_magic`, `hum_misc` | `hum` | Leaf |
| `calcMag` | L2 | `mag_base`, `mag_misc` | `mag` | Leaf; no `_mutations`/`_magic` |
| `calcReactionBase` | L3 | `int`, `dex` | `reaction_base` | After `calcInt`, `calcDex` |
| `calcReaction` | L3 | `reaction_base`, `reaction_misc` | `reaction` | After `calcReactionBase` |
| `calcPoolSpellBase` | L4a | `cha`, `int`, `wil` | `pool_spell_base` | After `calcCha`, `calcInt`, `calcWil` |
| `calcPoolCombatBase` | L4a | `dex`, `int`, `wil` | `pool_combat_base` | After `calcDex`, `calcInt`, `calcWil` |
| `calcPoolControlBase` | L4a | `reaction` | `pool_control_base` | After `calcReaction` |
| `calcPoolAstralBase` | L4a | `int`, `wil`, `mag` | `pool_astral_base` | After `calcInt`, `calcWil`, `calcMag` |
| `calcPoolSpell` | L4b | `pool_spell_base`, `pool_spell_misc` | `pool_spell` | After `calcPoolSpellBase` |
| `calcPoolCombat` | L4b | `pool_combat_base`, `pool_combat_misc` | `pool_combat` | After `calcPoolCombatBase` |
| `calcPoolControl` | L4b | `pool_control_base`, `pool_control_misc` | `pool_control` | After `calcPoolControlBase` |
| `calcPoolAstral` | L4b | `pool_astral_base`, `pool_astral_misc` | `pool_astral` | After `calcPoolAstralBase` |
| `calcInitScore` | L4c | `reaction`, `init_reaction_mod`, `init_misc_mod` | `init_score` | After `calcReaction` |
| `calcEpMax` | L5 | `str`, `body` | `ep_max` | After `calcStr`, `calcBody` |
| `calcEpTotal` | L5 | `repeating_weapons:weapon_ep`, `repeating_equipment:equip_ep` | `ep_total` | Repeating section iteration; fires on any row change in either section |
| `calcArmorTotals` | L5 | All 9 armor sub-fields | `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact` | Leaf inputs |
| `calcSkillTotal` | L5 | `skill_base`, `skill_foci`, `skill_misc` (per row) | `skill_total` (per row) | Repeating section row worker; row-scoped |
| `calcPowerPointsMax` | L5 | `mag` | `power_points_max` | After `calcMag` |
| `calcPowerPointsUsed` | L5 | `repeating_adept_powers:power_pp_cost_value` | `power_points_used` | Repeating section iteration |
| `calcPowerPointsRemaining` | L5 | `power_points_max`, `power_points_used` | `power_points_remaining` | After `calcPowerPointsMax`, `calcPowerPointsUsed` |
| `calcEssenceTotal` | L5 | `repeating_mutations:mutation_essence` | `essence_total` | Repeating section iteration |
| `calcKarmaTotal` | L6 | `karma_good`, `karma_used` | `karma_total` | Leaf inputs |
| `calcCmPenalties` | L6 | `cm_mental`, `cm_stun`, `cm_physical` | `cm_tn_mod`, `cm_init_mod` | Leaf inputs |
| `calcSustainedPenalty` | L6 | `spells_sustained` | `sustained_tn_mod`, `tn_warning_level` | Leaf input |

**Total registered workers: 30**

**`k.sheetOpens` wiring:** The sheet-open handler calls `k.getAllAttrs` to collect all stored attribute values, then re-triggers the full cascade. K-scaffold may expose a built-in full-cascade method for this — consult version docs. If not, manually invoke the registered worker functions in cascade order.

**Repeating section worker registration notes:** K-scaffold distinguishes two patterns for repeating section workers:

**Pattern A — Full-section iteration** (used by `calcEpTotal`, `calcPowerPointsUsed`, `calcEssenceTotal`):
```
// Fires when any row in the section changes; callback receives all rows
k.registerFuncs({
  calcEpTotal: {
    trigger: ['repeating_weapons:weapon_ep', 'repeating_equipment:equip_ep'],
    affects: ['ep_total'],
    callback: function(attrs, sections) {
      // sections['repeating_weapons'] = array of row objects
      // sections['repeating_equipment'] = array of row objects
      // sum parseFloat(row.weapon_ep || 0) across all rows in both sections
    }
  }
});
```

**Pattern B — Per-row scope** (used by `calcSkillTotal`):
```
// Fires when any trigger field changes within a single row;
// callback receives that row's attrs only; writes back to that row only
k.registerFuncs({
  calcSkillTotal: {
    trigger: ['repeating_skills:skill_base', 'repeating_skills:skill_foci', 'repeating_skills:skill_misc'],
    affects: ['repeating_skills:skill_total'],
    callback: function(attrs) {
      // attrs.skill_base, attrs.skill_foci, attrs.skill_misc = this row's values
      // attrs.skill_total = parseInt(skill_base) + parseInt(skill_foci) + parseInt(skill_misc)
    }
  }
});
```

The exact K-scaffold API for these patterns (parameter names, callback signature) varies by major version. The structural distinction above is version-agnostic; confirm specific syntax against the installed version's documentation.

---

### Section 6: Sync Handler Architecture Blueprint

The outbound sync handler is **event-driven, not cascade-driven**. It is registered as a bare `on()` call in Region 5 — outside `k.registerFuncs`.

**Trigger:** `on('clicked:btn_sync_db', callback)` — fires when player clicks `act_btn_sync_db`

**Handler execution flow:**

```
Step 1 — Immediate feedback
  k.setAttrs({ sync_status: 'Syncing…' })
  → Gives the player immediate visual confirmation that the click registered

Step 2 — Collect all data
  k.getAllAttrs({
    sections: REPEATING_SECTIONS,   // all 7 section names from Region 2 constant
    callback: function(attrs, sections) {
      buildPayloadAndSend(attrs, sections);
    }
  })

Step 3 — Build Turso payload
  const syncVersionFrom = parseInt(attrs.char_sync_version, 10) || 0;  // declared here for reuse in Step 5a
  payload = {
    campaign_db_id: attrs.campaign_db_id,
    char_db_id: attrs.char_db_id || null,             // null on first sync
    sync_version_from: syncVersionFrom,
    scalars: {
      // All 118 scalar fields (122 total minus the 4 sync infrastructure fields)
      // i.e., exclude: char_db_id, char_sync_version, campaign_db_id, sync_status
      body_base: attrs.body_base,
      dex_base: attrs.dex_base,
      // ... all remaining fields from the Phase 1 scalar registry
    },
    repeating: {
      skills:       sections['repeating_skills']       || [],
      spells:       sections['repeating_spells']       || [],
      mutations:    sections['repeating_mutations']    || [],
      adept_powers: sections['repeating_adept_powers'] || [],
      weapons:      sections['repeating_weapons']      || [],
      equipment:    sections['repeating_equipment']    || [],
      contacts:     sections['repeating_contacts']     || []
    }
  }

Step 4 — POST to Cloudflare Worker proxy
  fetch(SYNC_PROXY_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

Step 5a — Success branch
  response.json() → { char_db_id: '...', sync_version: N }
  k.setAttrs({
    char_db_id:        attrs.char_db_id || response.char_db_id,   // preserve existing ID; use server ID on first sync
    char_sync_version: response.sync_version.toString(),           // SERVER-authoritative value; never (syncVersionFrom + 1)
    sync_status:       'Synced ✓ — ' + new Date().toLocaleString()
  })

Step 5b — Failure branch
  console.error('Sync failed:', error)
  k.setAttrs({ sync_status: 'Sync failed — check console' })
  // DO NOT modify char_db_id or char_sync_version on failure
```

**Fields mutated as sync side effects (not cascade outputs):**

| Field | On success | On failure |
|---|---|---|
| `sync_status` | `"Synced ✓ — {timestamp}"` | `"Sync failed — check console"` |
| `char_db_id` | `attrs.char_db_id \|\| response.char_db_id` — existing value preserved; server response used only on first sync (when field is empty) | Unchanged |
| `char_sync_version` | Set to `response.sync_version` (server-authoritative; not local increment) | Unchanged |

[CARRY-FORWARD NOTE — SYNC_PROXY_URL placeholder]: `SYNC_PROXY_URL` is a constant defined in Region 2 of the worker script. It is an empty string `''` during development. The Developer fills in the actual Cloudflare Worker deployment URL after deploying the proxy. Do not hardcode a URL in the source during development.

[CARRY-FORWARD NOTE — V1 is outbound-only]: No inbound pull handler exists in V1. `btn_pull_db` and its handler are V2 scope per DECISION-08. Do not implement any logic that reads from Turso and writes to the sheet.

[CARRY-FORWARD NOTE — scalar field exclusions in payload]: The 4 sync infrastructure fields (`char_db_id`, `char_sync_version`, `campaign_db_id`, `sync_status`) are top-level sync metadata — they are NOT included in the `scalars` object. Including them there would attempt to store operational sync metadata in the character data rows in Turso, corrupting the schema.

[CARRY-FORWARD NOTE — Turso auth token]: The Cloudflare Worker proxy holds the real Turso token in its environment variables. The Sheet Worker sends to the proxy URL only — no auth token in the worker script. `turso_auth_token` is not a sheet attribute per DECISION-14.

---

### Section 7: Developer Guidance Notes

---

#### 7.1 Why `k.registerFuncs` Over Bare `on()` Calls

K-scaffold's `k.registerFuncs` builds an internal dependency graph from each worker's `trigger` and `affects` declarations. When a trigger attribute changes, K-scaffold resolves the full downstream cascade in topological order — every worker that depends (directly or transitively) on the changed value fires in the correct sequence before any `setAttrs` writes occur.

Bare `on('change:int', ...)` calls have no awareness of other watchers. If two `on('change:int')` handlers exist and one produces a value the other needs (e.g., `calcInt` and `calcReactionBase` both watch `int`), execution order is undefined. K-scaffold eliminates this class of sequencing bug entirely.

**Rule:** Every computed field worker must be registered via `k.registerFuncs`. Only the sync button event handler (`on('clicked:btn_sync_db')`) is registered as a bare `on()` call — it is event-driven, not cascade-driven, and has no downstream computed dependencies.

---

#### 7.2 Decimal Arithmetic — Always `parseFloat`; Integer Arithmetic — Always `parseInt`

**Integer fields (all workers using `+` addition on numeric attrs):** Roll20's `getAttrs()` returns ALL attribute values as strings regardless of declared type in `sheet.json`. JavaScript's `+` operator performs string concatenation on strings, not numeric addition. Use `parseInt(value, 10) || 0` for every integer field read from `attrs` that is then added to another value. This applies to: reaction workers, initiative worker, pool total workers, armor total workers, karma total worker, and power points remaining worker. Workers using only `Math.floor`, `Math.max`, `Math.min`, or `*` are unaffected (JS coerces for those operators).

**Decimal fields** require `parseFloat` instead of `parseInt`: Three fields carry decimal values:
- `mutation_essence` — per mutation row (e.g., `0.2`, `1.15`)
- `power_pp_cost_value` — per adept power row (e.g., `0.25`, `0.5`, `1.5`)

Always use `parseFloat(value || 0)`, never `parseInt`. `parseInt(0.25)` returns `0` — every fractional PP cost would silently be treated as free, corrupting `power_points_used` with no runtime error. `power_points_remaining` will be a decimal — do not round it; the UI displays it as-is.

---

#### 7.3 SR3 Critical Failure Implementation Rationale

**Rule (SR3):** If ALL dice in a pool show a 1, it is a Critical Failure. One non-1 die anywhere prevents it. Zero successes alone is not a critical failure.

**Roll20 implementation:** `cf<=1` in the roll expression causes Roll20 to render 1-showing dice in red in the dice tray. The all-red visual with successes = 0 is the critical failure signal. No additional computation is required or possible.

**Why no second roll:** A separate `[[Nd6cs<=1]]` expression rolls a completely independent set of d6 — different physical values from the main roll. Roll20 has no mechanism to reference already-rolled dice from a separate inline expression. The `cf<=1` visual marking on the same expression is the only correct Roll20-native technique for this mechanic.

**The `{{^successes}}` advisory:** This fires on any zero-success result — ordinary misses and critical failures alike. It is a hint to check the dice tray, not a definitive declaration. The dice tray is the authoritative visual.

**Initiative exemption:** `btn_init_roll` uses a plain sum roll (`@{init_dice}d6 + @{init_score}`). Initiative is not a success-counting roll; the SR3 critical failure mechanic does not apply to initiative. No `cs`, no `cf`, no template.

---

#### 7.4 `Math.max(1, reaction)` Floor — Why Reaction Cannot Be Zero

The `reaction` attribute is used directly in roll formulas as `@{reaction}d6` and as the source for `pool_control_base`. If `reaction = 0`:
- `@{reaction}d6` attempts to roll 0 dice — Roll20 behavior is undefined (may error, may produce a broken chat message, may roll nothing visibly)
- `pool_control_base = 0`, potentially driving `pool_control` to 0 or negative

The `Math.max(1, result)` floor in `calcReaction` guarantees `reaction ≥ 1` at all times. The floor is applied to the final `reaction` output only — `reaction_base` may legitimately be 0 (e.g., if both `int` and `dex` total to 0 or 1). Never apply the floor to `reaction_base` — it is an intermediate value that other calculations (`pool_control_base`) may need to treat as 0 before the floor is applied.

---

#### 7.5 Repeating Section Row Iteration — K-scaffold Pattern

Three workers iterate all rows across one or more sections:
- `calcEpTotal` — iterates `repeating_weapons` AND `repeating_equipment`
- `calcPowerPointsUsed` — iterates `repeating_adept_powers`
- `calcEssenceTotal` — iterates `repeating_mutations`

K-scaffold provides `k.getAllAttrs` with a `sections` parameter. The callback receives a `sections` object: each key is a section name, each value is an array of row attribute objects. An empty section returns an empty array — guard with `|| []` for all section references to prevent null-reference errors.

`calcSkillTotal` is different — it fires within a single row context on any change to `skill_base`, `skill_foci`, or `skill_misc` in that row. K-scaffold's per-row repeating section registration handles this. The worker reads and writes within the row's scope — it does not need to iterate all rows.

Consult the K-scaffold version's documentation for the exact API difference between full-section iteration and row-scoped registration. The API surface has changed across K-scaffold major versions.

---

#### 7.6 `k.sheetOpens` — Full Cascade Recalculation Requirement

Roll20 fires the sheet open event when a character sheet is first loaded in a campaign session. `k.sheetOpens` registers a handler for this event. The handler must trigger a full cascade recalculation across all 30 computed workers.

**Why required:** Attribute sub-fields may have been modified outside the sheet (Roll20 API, Mod scripts, direct attribute editing). Without an open-sheet recalculation, computed totals such as `body`, `reaction`, pools, and EP may show stale values from a previous write. The full recalculation guarantees data consistency on every sheet load.

**Pattern (two implementation options — choose based on installed K-scaffold version):**

```
k.sheetOpens(() => {

  // Option A — K-scaffold built-in full recalculation (preferred if available):
  // k.recalcAll();   // or equivalent: consult installed version docs for exact method name

  // Option B — Manual cascade trigger (fallback if built-in not available):
  // Trigger a synthetic change on a root L1 attribute; K-scaffold cascades from there.
  // Using 'body_base' as the root trigger guarantees the full L2→L3→L4→L5 chain fires.
  k.getAllAttrs({
    callback: function(attrs) {
      // Re-set body_base to its current value to trigger the cascade
      // (or use k.setCascades if available in the installed version)
      k.setAttrs({ body_base: attrs.body_base });
      // Note: This only triggers cascades downstream of body_base.
      // For a full recalc, trigger root attributes for all independent L2 chains:
      // str_base, cha_base, int_base, wil_base, hum_base, mag_base,
      // karma_good, cm_mental, spells_sustained, and each repeating section change
    }
  });
});
```

[CARRY-FORWARD NOTE — k.sheetOpens Option B scope]: Option B (manual trigger on `body_base`) only cascades through attributes downstream of `body_base`. An L6 worker like `calcKarmaTotal` (watching `karma_good`/`karma_used`) is independent and will NOT fire from a `body_base` trigger. For a complete recalculation using Option B, trigger one root attribute per independent cascade chain. Option A (K-scaffold built-in) is strongly preferred — it handles all chains automatically.

---

*Phase 3 blueprint complete.*

---

## Phase 4 — CSS Blueprint

**Source:** Layer 2 Phase 4 + Amendments 4-A through 4-J + DEV DECISION resolutions D1–D10

**Scope:** Complete `<style>` block specification for `sheet.html`. All selectors, color values, and layout models documented. Developer implements the entire `<style>` block from this document alone — no archive files, no aesthetic judgment calls.

**Colors:** All 8 lock-confirmed tokens from DEV DECISION resolutions D1–D4 are incorporated throughout. No `var()`, no `:root`.

**Amendments status:** All FAIL and MAJOR findings from the L2 Reviewer are resolved inline below. Amendments 4-A through 4-J are fully reflected — no separate amendment block needed.

---

### Section 1: Style Block Region Map

The `<style>` block is organized in exactly this order:

```
1.  Color token comment block
2.  Global reset & base typography
3.  Tab navigation
4.  Attribute table
5.  Condition monitor tracks + damage checkboxes
6.  Dice pools + initiative black box
7.  Initiative row (4-field input row — Amendment 4-H)
8.  Karma row (Amendment 4-F)
9.  Repeating sections — base row styles + controls
10. Repeating sections — Skills tab column widths (Amendment 4-E)
11. Repeating sections — Magic tab column widths (spells, mutations, adept powers)
12. Repeating sections — Gear tab weapon column widths (Amendment 4-D)
13. Repeating sections — Gear/Bio tab (equipment, contacts) column widths
14. Computed display badges — Essence, Power Points (Amendment 4-G)
15. Roll template CSS (skill / attack / spell)
16. Combat panel + armor table (Amendment 4-B)
17. Magic tab — TN warning ramp (Amendment 4-A attribute selector pattern)
18. Gear tab — EP tracker
19. Bio tab — textarea & Session 0 blocks
20. Compact fallback (Amendment 4-I)
```

---

### Section 2: Color Token Comment Block

**Placement:** First content inside `<style>` — before any rules. These are inline comments, NOT CSS custom properties. Zero `var()` anywhere in the sheet.

```css
/*
 * =====================================================
 * COLOR PALETTE — ALL TOKENS LOCKED (DEV DECISIONS D1–D4)
 *
 * DO NOT use var() anywhere in this stylesheet.
 * DO NOT use :root — not accessible inside Roll20 iframe.
 * =====================================================
 *
 * COLOR_TEXT_PRIMARY:        #000000  — body text, primary labels
 * COLOR_TEXT_ON_DARK:        #ffffff  — text on dark backgrounds
 * COLOR_SURFACE_HEADER:      #f2f2f2  — header bg, column headers, read-only cells
 * COLOR_BORDER_STRONG:       #5f5f5f  — strong borders, active tab, section dividers
 * COLOR_BORDER_LIGHT:        #cccccc  — general borders, row separators
 * COLOR_BORDER_FOCUS:        #888888  — input focus ring
 * COLOR_CHECKBOX_BORDER:     #555555  — damage checkbox unchecked border
 * COLOR_DAMAGE_X:            #b81a1a  — ✘ glyph, Uncon header, delete controls
 * COLOR_TAB_NAV:             #dddddd  — tab bar background
 * COLOR_SURFACE_INIT:        #000000  — initiative box background
 * COLOR_WARN_AMBER:          #e6a817  — TN warning sustained_tn_mod +2 (dark text)
 * COLOR_WARN_ORANGE:         #e06c00  — TN warning sustained_tn_mod +4 (white text)
 * COLOR_WARN_RED:            #cc2200  — TN warning sustained_tn_mod +6+ (white text)
 * COLOR_SUCCESS_HIGHLIGHT:   #1a7a1a  — roll template success count badge
 * COLOR_ROLLTEMPLATE_SKILL:  #1a1a2e  — skill roll template header bar
 * COLOR_ROLLTEMPLATE_ATTACK: #3a1c1c  — attack roll template header bar
 * COLOR_ROLLTEMPLATE_SPELL:  #1c3a5e  — spell roll template header bar
 * COLOR_ROW_ALT:             #f9f9f9  — alternating even-row background in tables/repeating sections
 */
```

---

### Section 3: Global Reset & Base Typography

**Constraint:** Roll20 injects `height`, `border-radius`, and `padding` onto inputs globally. All must be explicitly overridden here. Never use `:root`, `var()`, or `@import`.

```css
/* === GLOBAL RESET === */

*, *::before, *::after {
  box-sizing: border-box;
}

/* Normalize Roll20-inflated input styles */
input[type="text"],
input[type="number"],
input[type="checkbox"],
textarea,
select {
  font-family: sans-serif;
  font-size: 14px;
}

input[type="text"],
input[type="number"] {
  border: 1px solid #cccccc;
  padding: 2px 4px;
  border-radius: 0;
  height: auto;
}

/* select: Roll20 may inject height and border-radius on dropdowns too (FINDING-3) */
select {
  border-radius: 0;
  height: auto;
}

textarea {
  border: 1px solid #cccccc;
  padding: 4px 6px;
  border-radius: 0;
  height: auto;
  resize: vertical;
}

label {
  font-size: 14px;
  font-weight: normal;
  display: inline-block;
}

h1 { margin: 0; font-size: 22px; }
h2 { margin: 0; font-size: 18px; }
h3 { margin: 0; font-size: 15px; }
h4 { margin: 0; font-size: 15px; }

table {
  border-collapse: collapse;
  width: 100%;
}

th {
  text-align: left;
  font-size: 13px;
  font-weight: bold;
  padding: 2px 4px;
}

td {
  padding: 2px 4px;
  vertical-align: middle;
}

button[type="roll"] {
  cursor: pointer;
  padding: 2px 6px;
  font-size: 12px;
}
```

---

### Section 4: Tab Navigation

**HTML dependency (Phase 2):** `input.sheet-tab-radio` + `label.sheet-tab-label` pairs, followed by `.sheet-tab-panel-{slug}` divs — all direct children of the same parent. Tab slugs: `core` | `skills` | `magic` | `gear` | `bio`.

**Amendment 4-J FINDING-15:** Active label must use the fully qualified selector — shortened version fails specificity against Roll20's base styles.

```css
/* === TAB NAVIGATION === */

.sheet-tab-nav {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  background-color: #dddddd;
  padding: 6px 10px;
  gap: 4px;
  margin-bottom: 0;
}

input.sheet-tab-radio {
  display: none;
}

label.sheet-tab-label {
  padding: 5px 12px;
  cursor: pointer;
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
  font-size: 13px;
  user-select: none;
  white-space: nowrap;
}

/* Active tab label — fully qualified (Amendment 4-J FINDING-15) */
input.sheet-tab-radio:checked + label.sheet-tab-label {
  background-color: #5f5f5f;
  color: #ffffff;
  font-weight: bold;
  border-color: #5f5f5f;
}

/* All panels: hidden by default */
.sheet-tab-panel {
  display: none;
}

/* Active panel: one rule per tab (5 total) */
input#tab-core:checked   ~ .sheet-tab-panel-core   { display: block; }
input#tab-skills:checked ~ .sheet-tab-panel-skills  { display: block; }
input#tab-magic:checked  ~ .sheet-tab-panel-magic   { display: block; }
input#tab-gear:checked   ~ .sheet-tab-panel-gear    { display: block; }
input#tab-bio:checked    ~ .sheet-tab-panel-bio     { display: block; }
```

**[CARRY-FORWARD NOTE — DOM ordering]:** The `~` combinator only reaches siblings that follow in DOM order. All five `input.sheet-tab-radio` elements must appear before the `.sheet-tab-panel-*` wrappers in the Phase 2 HTML source.

---

### Section 5: Attribute Table

```css
/* === ATTRIBUTE TABLE === */

.sheet-box-attribute {
  display: inline-flex;
  align-items: flex-start;
  border: 1px solid #5f5f5f;
  padding: 10px;
  margin-bottom: 20px;
  max-width: 850px;
}

.sheet-box-attribute table {
  width: auto;
}

.sheet-box-attribute th {
  background-color: #f2f2f2;
  border-bottom: 2px solid #5f5f5f;
  text-align: center;
  padding: 2px 4px;
  font-size: 13px;
}

/*
 * Column min-widths (7 columns):
 *   1: Attribute name      — 140px
 *   2–5: Base/Mutations/Magic/Misc — 55px each
 *   6: Total               — 55px
 *   7: Roll button         — 50px
 */
.sheet-box-attribute th:nth-child(1),
.sheet-box-attribute td:nth-child(1) { min-width: 140px; }

.sheet-box-attribute th:nth-child(2),
.sheet-box-attribute td:nth-child(2),
.sheet-box-attribute th:nth-child(3),
.sheet-box-attribute td:nth-child(3),
.sheet-box-attribute th:nth-child(4),
.sheet-box-attribute td:nth-child(4),
.sheet-box-attribute th:nth-child(5),
.sheet-box-attribute td:nth-child(5),
.sheet-box-attribute th:nth-child(6),
.sheet-box-attribute td:nth-child(6) { min-width: 55px; }

.sheet-box-attribute th:nth-child(7),
.sheet-box-attribute td:nth-child(7) { min-width: 50px; }

.sheet-box-attribute tr:nth-child(even) { background-color: #f9f9f9; }
.sheet-box-attribute tr:nth-child(odd)  { background-color: #ffffff; }

/* Attribute name column */
.sheet-box-attribute td:first-child {
  font-weight: bold;
  white-space: nowrap;
}

.sheet-box-attribute td input[type="number"] {
  width: 45px;
  text-align: center;
  padding: 1px 2px;
}

/* Total cell: display-only, no input box */
.sheet-attr-total {
  font-weight: bold;
  text-align: center;
  color: #000000;
}

/* Roll button column */
.sheet-attr-roll {
  text-align: center;
}

.sheet-attr-roll button[type="roll"] {
  padding: 2px 6px;
  font-size: 12px;
}
```

---

### Section 6: Condition Monitor Tracks

**Amendment 4-J FINDING-10:** All `appearance: none` + base dimensions belong on the BASE checkbox rule — the `:checked` rule adds visual state only.
**Amendment 4-J FINDING-11:** `.sheet-condition-init-penalty` added for italic initiative penalty labels.
**DEV DECISION D5:** "No Damage" is a first leftmost tier column on all 3 tracks — label-only, no checkboxes, italic gray.

```css
/* === CONDITION MONITOR === */

.sheet-box-condition {
  border: 1px solid #cccccc;
  padding: 10px;
  margin-bottom: 20px;
}

.sheet-condition-track {
  margin-bottom: 12px;
}

.sheet-condition-track h3 {
  margin: 0;
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 4px;
}

.sheet-condition-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 3px;
}

.sheet-condition-tier {
  flex: 0 0 calc(12% - 6px);
  min-width: 36px;
  margin-bottom: 10px;
}

.sheet-condition-tier h4 {
  margin: 0;
  font-size: 13px;
  margin-bottom: 2px;
}

/* "No Damage" column (DEV DECISION D5) — visual baseline only, no checkboxes */
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

/* TN penalty label below each tier header */
.sheet-condition-penalty {
  font-size: 11px;
  color: #555555;
  display: block;
  margin-top: 2px;
}

/* Initiative penalty label (Amendment 4-J FINDING-11) */
.sheet-condition-init-penalty {
  font-size: 10px;
  color: #888888;
  display: block;
  margin-top: 1px;
  font-style: italic;
}

/* "Uncon" tier header — red severity indicator */
.sheet-condition-tier-uncon h4 {
  color: #b81a1a;
}

/* Overflow damage input — Physical track, after Uncon column */
.sheet-condition-overflow {
  width: 40px;
  font-size: 12px;
  text-align: center;
  border: 1px solid #5f5f5f;
  padding: 1px 2px;
}

/*
 * DAMAGE CHECKBOX RULES (Amendment 4-J FINDING-10):
 *   BASE rule — all appearance normalization + dimensions.
 *   :checked rule — visual additions ONLY, no repeated dimensions.
 */
input[type="checkbox"].sheet-damage-checkbox {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  position: relative;
  width: 16px;
  height: 16px;
  border: 1px solid #555555;
  border-radius: 3px;
  cursor: pointer;
  display: inline-block;
  vertical-align: middle;
}

input[type="checkbox"].sheet-damage-checkbox:checked::before {
  content: "\2718";
  display: block;
  position: absolute;
  top: -1px;
  left: 2px;
  font-size: 12px;
  line-height: 1;
  color: #b81a1a;
  width: 16px;
  height: 16px;
  text-align: center;
}

input[type="checkbox"].sheet-damage-checkbox:focus {
  outline: 0;
  border: 2px solid #888888;
}
```

**[DEV DECISION D8 — RUN SANDBOX TEST FIRST]:** Test `appearance: none` on `input[type="checkbox"]` in Chrome + Firefox on Roll20 before writing any condition monitor CSS. If native checkbox rendering is not suppressed, rebuild with the hidden-checkbox + adjacent-label fallback pattern:

```css
/* D8 fallback — only if appearance: none fails */
input[type="checkbox"].sheet-damage-checkbox { opacity: 0; position: absolute; width: 16px; height: 16px; }
input[type="checkbox"].sheet-damage-checkbox + label::before { /* unchecked 16×16 box */ }
input[type="checkbox"].sheet-damage-checkbox:checked + label::before { content: "\2718"; /* ✘ glyph */ }
```

This fallback requires Phase 2 HTML changes to the condition monitor structure. Run D8 first.

---

### Section 7: Dice Pools, Initiative Black Box & Initiative Row

**Amendment 4-H:** Initiative Row (4 input fields + read-only score) is a separate component from the Init Black Box (roll button). Both appear on the Core tab.

```css
/* === DICE POOLS + INIT BLACK BOX === */

.sheet-box-dice-pool {
  display: inline-flex;
  align-items: flex-start;
  border: 1px solid #cccccc;
  padding: 10px;
  margin-bottom: 20px;
  max-width: 600px;
}

/* Init black box */
.sheet-box-init {
  background-color: #000000;
  color: #ffffff;
  padding: 10px;
  margin-right: 10px;
  text-align: center;
  min-width: 80px;
  max-width: 120px;
  flex-shrink: 0;
}

.sheet-box-init h4 {
  color: #ffffff;
  font-size: 15px;
  margin: 0 0 6px 0;
}

/* Roll20 does NOT inherit color: #ffffff in dark containers — set explicitly */
.sheet-box-init button[type="roll"] {
  background-color: #333333;
  color: #ffffff;
  border: 1px solid #888888;
  padding: 4px 10px;
  cursor: pointer;
  font-size: 12px;
}

/* Pool summary table */
.sheet-dice-pool-table th {
  background-color: #f2f2f2;
  border-bottom: 1px solid #5f5f5f;
  font-size: 12px;
  white-space: nowrap;
}

.sheet-pool-formula {
  font-size: 12px;
  color: #555555;
  font-style: italic;
}

.sheet-pool-base,
.sheet-pool-total {
  text-align: center;
  font-weight: bold;
}

.sheet-pool-misc input {
  width: 45px;
  text-align: center;
}

/* === INITIATIVE ROW (Amendment 4-H) ===
   Separate from the init black box.
   Fields: init_dice, init_reaction_mod, init_misc_mod (editable) + init_score (read-only). */

.sheet-initiative-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.sheet-initiative-row label {
  font-size: 12px;
  color: #555555;
  white-space: nowrap;
}

/* init_dice, init_reaction_mod, init_misc_mod */
.sheet-initiative-row input[type="number"] {
  width: 42px;
  text-align: center;
  font-size: 13px;
}

/* init_score — read-only, echoes init black box aesthetic */
.sheet-init-score {
  width: 42px;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
  border: 1px solid #5f5f5f;
  background-color: #000000;
  color: #ffffff;
  padding: 2px 4px;
}
```

---

### Section 8: Karma Row

**Source:** Amendment 4-F (Task 4.5a). Compact inline flex row. `karma_good`, `karma_used`, `karma_pool` are editable; `karma_total` is read-only computed display.

```css
/* === KARMA ROW === */

.sheet-karma-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 10px;
  border: 1px solid #cccccc;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.sheet-karma-row label {
  font-weight: bold;
  font-size: 13px;
  white-space: nowrap;
}

/* karma_good, karma_used, karma_pool — editable */
.sheet-karma-row input[type="number"] {
  width: 55px;
  text-align: center;
  font-size: 14px;
}

/* karma_total — read-only computed; gray background distinguishes from editable inputs */
.sheet-karma-total {
  width: 55px;
  text-align: center;
  font-size: 14px;
  font-weight: bold;
  border: 1px solid #5f5f5f;
  background-color: #f2f2f2;
  padding: 2px 4px;
}
```

---

### Section 9: Repeating Section Base Styles

**[DEV DECISION D7 — SANDBOX REQUIRED]:** K-scaffold may generate `.repcontainer` (not `.sheet-repcontainer`) as the outer wrapper. Both variants listed — implement whichever sandbox confirms.

```css
/* === REPEATING SECTIONS — BASE ROW STYLES ===
   DEV DECISION D7: outer container is .sheet-repcontainer OR .repcontainer.
   After sandbox test, remove the variant that does not apply.           */

.sheet-repcontainer,
.repcontainer {
  width: 100%;
  margin-bottom: 12px;
}

/* .repitem is Roll20-injected — do NOT rename */
.repitem {
  display: flex;
  align-items: center;
  padding: 3px 6px;
  border-bottom: 1px solid #cccccc;
  gap: 6px;
}

.repitem:nth-child(even) { background-color: #f9f9f9; }
.repitem:nth-child(odd)  { background-color: #ffffff; }

/* Roll20-injected delete control — right-aligned, red, minimal */
.repcontrol_del {
  margin-left: auto;
  font-size: 11px;
  color: #b81a1a;
  cursor: pointer;
  border: none;
  background: none;
  padding: 1px 4px;
}

/* Roll20-injected add row button */
.repcontrol_add {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  padding: 2px 8px;
  cursor: pointer;
}

/* Roll buttons inside repeating rows */
.repitem button[type="roll"] {
  padding: 2px 6px;
  font-size: 12px;
  flex-shrink: 0;
}
```

**[CARRY-FORWARD NOTE — K-scaffold control class names]:** If delete/add buttons don't receive these styles, inspect the live DOM and adjust. K-scaffold may wrap injected controls with different class names.

#### Skills Tab Column Widths (Amendment 4-E)

Cell wrapper classes (`.sheet-skill-name` etc.) are applied to the `<span>` or `<div>` wrapping each input in the repeating section row.

```css
/* === repeating_skills — Skills tab column widths (Amendment 4-E) === */

.sheet-tab-panel-skills .repitem .sheet-skill-name    { flex: 2 1 100px; }
.sheet-tab-panel-skills .repitem .sheet-skill-linked  { flex: 0 0 70px; }
.sheet-tab-panel-skills .repitem .sheet-skill-general { flex: 1 1 55px; }
.sheet-tab-panel-skills .repitem .sheet-skill-spec    { flex: 1 1 55px; }
.sheet-tab-panel-skills .repitem .sheet-skill-base    { flex: 0 0 38px; text-align: center; }
.sheet-tab-panel-skills .repitem .sheet-skill-foci    { flex: 0 0 38px; text-align: center; }
.sheet-tab-panel-skills .repitem .sheet-skill-misc    { flex: 0 0 38px; text-align: center; }

/* skill_total — read-only computed; visually distinct from editable inputs */
.sheet-tab-panel-skills .repitem .sheet-skill-total {
  flex: 0 0 42px;
  text-align: center;
  font-weight: bold;
  border: none;
  background-color: #f2f2f2;
}
```

#### Magic Tab Column Widths (spells, mutations, adept powers)

```css
/* === repeating_spells — Magic tab === */
.sheet-tab-panel-magic .repitem .sheet-spell-name   { flex: 2 1 120px; }
.sheet-tab-panel-magic .repitem .sheet-spell-drain  { flex: 0 0 50px; text-align: center; }
.sheet-tab-panel-magic .repitem .sheet-spell-force  { flex: 0 0 50px; text-align: center; }

/* === repeating_mutations — Magic tab === */
.sheet-tab-panel-magic .repitem .sheet-mutation-name { flex: 2 1 120px; }
.sheet-tab-panel-magic .repitem .sheet-mutation-desc { flex: 3 1 150px; }

/* === repeating_adept_powers — Magic tab === */
.sheet-tab-panel-magic .repitem .sheet-power-name    { flex: 2 1 120px; }
.sheet-tab-panel-magic .repitem .sheet-power-pp-cost { flex: 0 0 50px; text-align: center; }
```

#### Gear Tab Equipment Column Widths

```css
/* === repeating_equipment — Gear tab === */
.sheet-tab-panel-gear .repitem .sheet-equip-name   { flex: 2 1 120px; }
.sheet-tab-panel-gear .repitem .sheet-equip-qty    { flex: 0 0 40px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-equip-weight { flex: 0 0 50px; text-align: center; }
```

#### Bio Tab Contacts Column Widths

```css
/* === repeating_contacts — Bio tab === */
.sheet-tab-panel-bio .repitem .sheet-contact-name       { flex: 2 1 120px; }
.sheet-tab-panel-bio .repitem .sheet-contact-loyalty    { flex: 0 0 50px; text-align: center; }
.sheet-tab-panel-bio .repitem .sheet-contact-connection { flex: 0 0 50px; text-align: center; }
```

#### Computed Display Badges — Essence & Power Points (Amendment 4-G)

```css
/* === COMPUTED DISPLAY BADGES (Amendment 4-G) === */

/* Section header bar above Mutations and Adept Powers repeating sections */
.sheet-skills-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 2px solid #5f5f5f;
  margin-bottom: 6px;
}

.sheet-skills-section-header h2 {
  margin: 0;
  font-size: 16px;
}

/* Shared computed badge — used for essence_total and power_points_* displays */
.sheet-computed-badge {
  display: inline-block;
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
  border-radius: 2px;
  padding: 1px 8px;
  font-size: 12px;
  font-weight: bold;
}

/* .sheet-essence-display and .sheet-pp-display extend .sheet-computed-badge — no additional rules */
```

---

### Section 10: Roll Template CSS

All 3 templates share identical structural rules. Per-template header `background-color` and container `border-color` are the only differentiators.

```css
/* === ROLL TEMPLATES ===
   Structural pattern identical for all 3 types.
   Header background-color only:
     skill:  #1a1a2e  (dark navy)
     attack: #3a1c1c  (dark maroon)
     spell:  #1c3a5e  (dark blue)              */

/* --- Outer wrappers + template headers (per-type) --- */

.sheet-rolltemplate-skill {
  display: block;
  border: 1px solid #1a1a2e;
  font-family: sans-serif;
  font-size: 13px;
  width: 100%;
  box-sizing: border-box;
  min-width: 200px;
}

.sheet-rolltemplate-skill .sheet-template-header {
  background-color: #1a1a2e;
  color: #ffffff;
  padding: 6px 10px;
  font-weight: bold;
  font-size: 14px;
}

.sheet-rolltemplate-attack {
  display: block;
  border: 1px solid #3a1c1c;
  font-family: sans-serif;
  font-size: 13px;
  width: 100%;
  box-sizing: border-box;
  min-width: 200px;
}

.sheet-rolltemplate-attack .sheet-template-header {
  background-color: #3a1c1c;
  color: #ffffff;
  padding: 6px 10px;
  font-weight: bold;
  font-size: 14px;
}

.sheet-rolltemplate-spell {
  display: block;
  border: 1px solid #1c3a5e;
  font-family: sans-serif;
  font-size: 13px;
  width: 100%;
  box-sizing: border-box;
  min-width: 200px;
}

.sheet-rolltemplate-spell .sheet-template-header {
  background-color: #1c3a5e;
  color: #ffffff;
  padding: 6px 10px;
  font-weight: bold;
  font-size: 14px;
}

/* --- Shared body rules (all 3 templates via group selector) --- */

.sheet-rolltemplate-skill .sheet-template-body,
.sheet-rolltemplate-attack .sheet-template-body,
.sheet-rolltemplate-spell .sheet-template-body {
  padding: 2px 0;
}

.sheet-rolltemplate-skill .sheet-template-row,
.sheet-rolltemplate-attack .sheet-template-row,
.sheet-rolltemplate-spell .sheet-template-row {
  display: flex;
  align-items: baseline;
  padding: 3px 10px;
  border-bottom: 1px solid #cccccc;
}

.sheet-rolltemplate-skill .sheet-template-label,
.sheet-rolltemplate-attack .sheet-template-label,
.sheet-rolltemplate-spell .sheet-template-label {
  font-weight: bold;
  color: #555555;
  min-width: 80px;
  flex-shrink: 0;
  font-size: 12px;
}

.sheet-rolltemplate-skill .sheet-template-value,
.sheet-rolltemplate-attack .sheet-template-value,
.sheet-rolltemplate-spell .sheet-template-value {
  flex: 1;
  font-size: 13px;
}

/* Success count badge — prominent green block */
.sheet-rolltemplate-skill .sheet-template-successes,
.sheet-rolltemplate-attack .sheet-template-successes,
.sheet-rolltemplate-spell .sheet-template-successes {
  display: inline-block;
  background-color: #1a7a1a;
  color: #ffffff;
  font-weight: bold;
  padding: 2px 10px;
  font-size: 16px;
  border-radius: 2px;
}

/* No-success warning — rendered by Mustache {{^successes}} inverse block */
.sheet-rolltemplate-skill .sheet-template-nosuccess,
.sheet-rolltemplate-attack .sheet-template-nosuccess,
.sheet-rolltemplate-spell .sheet-template-nosuccess {
  color: #b81a1a;
  font-weight: bold;
  font-style: italic;
  font-size: 13px;
  padding: 4px 10px;
}

/* Critical failure note — cf<=1 threshold reached */
.sheet-rolltemplate-skill .sheet-template-critfail,
.sheet-rolltemplate-attack .sheet-template-critfail,
.sheet-rolltemplate-spell .sheet-template-critfail {
  color: #b81a1a;
  font-weight: bold;
  background-color: #fce8e8;
  padding: 3px 10px;
  font-size: 12px;
}
```

**[CARRY-FORWARD NOTE — roll template scope]:** Roll template CSS lives in the same `<style>` block as all sheet CSS — Roll20 applies it to chat output. The `.sheet-rolltemplate-{name}` prefix is Roll20's mandatory naming convention. The `.sheet-template-nosuccess` selector targets the HTML wrapper of the `{{^successes}}` block, not the Mustache expression itself.

---

### Section 11: Combat Panel & Armor Table

**Amendment 4-B (CRITICAL):** Armor is a 3-column × 4-row table (15 editable inputs + 3 computed totals in `<tfoot>`), not a single field. `.sheet-armor-region` is a child of `.sheet-combat-panel`.

**Columns:** Torso | Legs | Head
**Rows:** Name (text) | Piercing (number) | Slashing (number) | Impact (number) | Totals (computed, tfoot)

```css
/* === COMBAT PANEL === */

.sheet-combat-panel {
  border: 1px solid #5f5f5f;
  padding: 10px;
  margin-top: 8px;
  margin-bottom: 20px;
}

/* Armor table (Amendment 4-B) */
.sheet-armor-region {
  margin-bottom: 20px;
}

.sheet-armor-region table {
  border-collapse: collapse;
  width: 100%;
  max-width: 500px;
}

/* Column headers: Torso / Legs / Head */
.sheet-armor-region thead th {
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
  text-align: center;
  padding: 3px 6px;
  font-size: 13px;
  min-width: 120px;
}

/* Row label cells: "Name", "Piercing", "Slashing", "Impact", "Totals" */
.sheet-armor-region tbody tr th,
.sheet-armor-region tfoot th {
  text-align: right;
  padding: 3px 8px;
  font-size: 13px;
  font-weight: bold;
  white-space: nowrap;
  border-right: 2px solid #5f5f5f;
  color: #555555;
}

.sheet-armor-region tbody td {
  border: 1px solid #cccccc;
  padding: 2px 4px;
  text-align: center;
}

/* Name row — text input, full cell width */
.sheet-armor-region tbody td input[type="text"] {
  width: 100%;
  font-size: 13px;
  border: 1px solid #cccccc;
  padding: 2px 4px;
}

/* Piercing / Slashing / Impact rows — compact number inputs */
.sheet-armor-region tbody td input[type="number"] {
  width: 48px;
  text-align: center;
  font-size: 13px;
  border: 1px solid #cccccc;
  padding: 2px 4px;
}

/* Totals row — read-only display, no input element */
.sheet-armor-region tfoot tr {
  background-color: #f2f2f2;
  border-top: 2px solid #5f5f5f;
}

.sheet-armor-region tfoot td {
  font-weight: bold;
  text-align: center;
  border: 1px solid #5f5f5f;
  padding: 3px 6px;
  font-size: 13px;
}

/* Combat roll buttons — Dodge + Resist Damage equal-width via flex: 1 1 auto */
.sheet-combat-buttons {
  display: flex;
  gap: 8px;
}

.sheet-combat-buttons button[type="roll"] {
  flex: 1 1 auto;
  padding: 6px 10px;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
}
```

---

### Section 12: Magic Tab — TN Warning Ramp

**Amendment 4-A (CRITICAL):** Warning states use CSS attribute selectors on a hidden `input[name="attr_tn_warning_level"]`. The class-based approach (`.sheet-warn-amber` etc.) is void — do not implement it.

**HTML dependency (Phase 2 + Amendment 4-A):** Required DOM structure inside `.sheet-tab-panel-magic`:
```html
<!-- Hidden input MUST immediately precede .sheet-tn-warning as a DOM sibling -->
<input type="hidden" name="attr_tn_warning_level" value="0">
<div class="sheet-tn-warning">TN +2 sustained!</div>
```

**Amendment 4-C:** All selectors use `.sheet-tab-panel-magic` prefix.

```css
/* === MAGIC TAB === */

/* Sustained spell count badge */
.sheet-tab-panel-magic .sheet-sustained-count {
  display: inline-block;
  background-color: #dddddd;
  border: 1px solid #5f5f5f;
  border-radius: 3px;
  padding: 1px 6px;
  font-size: 12px;
  font-weight: bold;
  min-width: 24px;
  text-align: center;
}

/* TN warning container — hidden by default */
.sheet-tab-panel-magic .sheet-tn-warning {
  display: none;
  font-size: 12px;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: 2px;
}

/*
 * Attribute-selector warning ramp (Amendment 4-A)
 * ~ combinator: hidden input must be a direct preceding DOM sibling (DEV DECISION D9).
 */

/* Level 1: amber — sustained_tn_mod +2 — dark text for contrast on amber */
input[name="attr_tn_warning_level"][value="1"] ~ .sheet-tn-warning {
  display: inline-block;
  background-color: #e6a817;
  color: #000000;
}

/* Level 2: orange — sustained_tn_mod +4 */
input[name="attr_tn_warning_level"][value="2"] ~ .sheet-tn-warning {
  display: inline-block;
  background-color: #e06c00;
  color: #ffffff;
}

/* Level 3: red — sustained_tn_mod +6+ */
input[name="attr_tn_warning_level"][value="3"] ~ .sheet-tn-warning {
  display: inline-block;
  background-color: #cc2200;
  color: #ffffff;
}

/* Magic section region headers */
.sheet-tab-panel-magic .sheet-magic-region-header {
  border-bottom: 1px solid #5f5f5f;
  margin-bottom: 8px;
  padding-bottom: 4px;
}
```

**[DEV DECISION D9 — SANDBOX REQUIRED]:** After Phase 4 HTML is rendered in Roll20, verify `input[name="attr_tn_warning_level"]` and `.sheet-tn-warning` are direct DOM siblings inside the same parent. If they are in different containers, the `~` selector fires against nothing — reposition in Phase 2 HTML.

**[CARRY-FORWARD NOTE — setAttrs string write]:** The Phase 3 `calcTNWarningLevel` worker must write `setAttrs({ tn_warning_level: level.toString() })`. The CSS `value="1"` attribute selector matches the HTML attribute string. A numeric write may also stringify correctly, but confirm via sandbox.

---

### Section 13: Gear Tab — Weapon Rows & EP Tracker

**Amendment 4-C:** All selectors use `.sheet-tab-panel-gear` prefix.
**Amendment 4-D (CRITICAL):** Weapon row has 15 columns. `.sheet-weapon-mode` is void — correct class is `.sheet-weapon-type`.

**Weapon row column reference (Amendment 4-D):**

| Field | Wrapper class | CSS |
|---|---|---|
| `weapon_name` | `.sheet-weapon-name` | `flex: 2 1 100px` |
| `weapon_type` (select) | `.sheet-weapon-type` | `flex: 0 0 80px` |
| `weapon_modifiers` | `.sheet-weapon-modifiers` | `flex: 1 1 60px` |
| `weapon_power` | `.sheet-weapon-power` | `flex: 0 0 40px; text-align: center` |
| `weapon_damage` | `.sheet-weapon-damage` | `flex: 0 0 55px; text-align: center` |
| `weapon_conceal` | `.sheet-weapon-conceal` | `flex: 0 0 36px; text-align: center` |
| `weapon_reach` | `.sheet-weapon-reach` | `flex: 0 0 36px; text-align: center` |
| `weapon_ep` | `.sheet-weapon-ep` | `flex: 0 0 36px; text-align: center` |
| Range band wrapper | `.sheet-range-bands` | flex container |
| `weapon_range_short` | `.sheet-range-short` | `width: 36px` |
| `weapon_range_medium` | `.sheet-range-medium` | `width: 36px` |
| `weapon_range_long` | `.sheet-range-long` | `width: 36px` |
| `weapon_range_extreme` | `.sheet-range-extreme` | `width: 36px` |
| `btn_attack_ranged` | `.sheet-btn-attack` | `flex: 0 0 auto` |
| `btn_attack_melee` | `.sheet-btn-attack` | `flex: 0 0 auto` |

**Weapons header row labels (order must match repitem flex columns):** Name | Type | Mods | PWR | DMG | Conc | Rch | EP | Short | Med | Long | Ext | Ranged | Melee

```css
/* === GEAR TAB === */

/* Static weapons header row — column labels above repeating section */
.sheet-tab-panel-gear .sheet-weapons-header {
  display: flex;
  align-items: center;
  padding: 2px 6px;
  gap: 6px;
  background-color: #f2f2f2;
  border-bottom: 2px solid #5f5f5f;
  font-size: 12px;
  font-weight: bold;
}

/* Weapon row column widths (Amendment 4-D) */
.sheet-tab-panel-gear .repitem .sheet-weapon-name      { flex: 2 1 100px; }
.sheet-tab-panel-gear .repitem .sheet-weapon-type      { flex: 0 0 80px; }
.sheet-tab-panel-gear .repitem .sheet-weapon-modifiers { flex: 1 1 60px; }
.sheet-tab-panel-gear .repitem .sheet-weapon-power     { flex: 0 0 40px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-weapon-damage    { flex: 0 0 55px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-weapon-conceal   { flex: 0 0 36px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-weapon-reach     { flex: 0 0 36px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-weapon-ep        { flex: 0 0 36px; text-align: center; }

/* Range band wrapper + 4 × 36px range inputs */
.sheet-tab-panel-gear .repitem .sheet-range-bands {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.sheet-tab-panel-gear .repitem .sheet-range-short,
.sheet-tab-panel-gear .repitem .sheet-range-medium,
.sheet-tab-panel-gear .repitem .sheet-range-long,
.sheet-tab-panel-gear .repitem .sheet-range-extreme {
  width: 36px;
  text-align: center;
  font-size: 11px;
}

/* Roll buttons inside weapon rows */
.sheet-tab-panel-gear .repitem .sheet-btn-attack {
  flex: 0 0 auto;
  padding: 2px 4px;
  font-size: 11px;
}

/* EP tracker */
.sheet-tab-panel-gear .sheet-ep-tracker {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid #5f5f5f;
  margin-bottom: 12px;
  margin-top: 8px;
}

.sheet-tab-panel-gear .sheet-ep-label {
  font-weight: bold;
  font-size: 14px;
}

.sheet-tab-panel-gear .sheet-ep-current,
.sheet-tab-panel-gear .sheet-ep-max {
  width: 45px;
  text-align: center;
  font-size: 14px;
}

/* "/" separator between current and max EP */
.sheet-tab-panel-gear .sheet-ep-separator {
  font-size: 16px;
  color: #555555;
}
```

---

### Section 14: Bio Tab

**Amendment 4-C:** All selectors use `.sheet-tab-panel-bio` prefix.

```css
/* === BIO TAB === */

.sheet-tab-panel-bio .sheet-bio-region {
  padding: 10px;
}

/* Full-width textareas — resize: vertical; box-sizing prevents overhang in padded containers */
.sheet-tab-panel-bio textarea {
  width: 100%;
  min-height: 80px;
  border: 1px solid #cccccc;
  padding: 6px;
  font-family: sans-serif;
  font-size: 13px;
  resize: vertical;
  box-sizing: border-box;
}

.sheet-tab-panel-bio .sheet-bio-field-label {
  display: block;
  font-weight: bold;
  font-size: 13px;
  margin-bottom: 2px;
  margin-top: 10px;
}

/* Character info text inputs — full width */
.sheet-tab-panel-bio input[type="text"] {
  width: 100%;
  border: 1px solid #cccccc;
  padding: 4px 6px;
  font-size: 13px;
  box-sizing: border-box;
}

/* Session 0 question blocks — left-border accent */
.sheet-tab-panel-bio .sheet-session0-block {
  border: 1px solid #dddddd;
  border-left: 3px solid #5f5f5f;
  padding: 8px;
  margin-bottom: 10px;
  background-color: #fafafa;
}

.sheet-tab-panel-bio .sheet-session0-block h4 {
  margin: 0 0 6px 0;
  font-size: 14px;
  font-weight: bold;
  color: #000000;
}

.sheet-tab-panel-bio .sheet-session0-block textarea {
  min-height: 60px;
}
```

---

### Section 15: Compact Fallback

**Amendment 4-I:** The `~` combinator requires `input#sheet-compact-mode` and all `.sheet-compact-target` elements to share the same DOM parent. Document and verify in Phase 2 HTML (DEV DECISION D10).

**Primary approach:** Manual toggle via `#sheet-compact-mode:checked ~ .sheet-compact-target`. The `@media` block is commented out pending DEV DECISION D6.

```css
/* === COMPACT FALLBACK === */

/*
 * Minimum width — horizontal scroll acceptable below this threshold.
 * Apply to outermost sheet container:
 * min-width: 340px;
 */

/*
 * input#sheet-compact-mode: the manual compact toggle checkbox.
 *
 * DOM CONSTRAINT (Amendment 4-I / DEV DECISION D10):
 * This input MUST be a direct child of the same parent as all
 * .sheet-tab-panel-* and .sheet-compact-target elements.
 * Do NOT place it inside a header sub-container.
 * Verify co-level placement in Phase 2 HTML before implementing.
 */
/* Visually hidden but label-clickable. No pointer-events: none — that can break label
 * activation in Safari and older Chromium builds (FINDING-2). */
input#sheet-compact-mode[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

/* Compact toggle label — visible interactive affordance */
label[for="sheet-compact-mode"] {
  cursor: pointer;
  border: 1px solid #5f5f5f;
  padding: 3px 8px;
  font-size: 12px;
  user-select: none;
  background-color: #f2f2f2;
  display: inline-block;
}

/* Attribute table → block layout */
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-attribute {
  display: block;
  max-width: 100%;
}

/* Hide Mutations (3rd col) and Magic (4th col) in compact mode */
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-attribute table th:nth-child(3),
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-attribute table td:nth-child(3),
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-attribute table th:nth-child(4),
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-attribute table td:nth-child(4) {
  display: none;
}

/* Dice pool area → stack vertically */
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-box-dice-pool {
  display: block;
  max-width: 100%;
}

/* Weapon rows → range bands wrap to second line */
input#sheet-compact-mode:checked ~ .sheet-compact-target .sheet-tab-panel-gear .repitem {
  flex-wrap: wrap;
}

/*
 * @media fallback — uncomment ONLY if DEV DECISION D6 confirms
 * that @media queries apply inside Roll20's iframe.
 *
 * @media (max-width: 500px) {
 *   .sheet-box-attribute { display: block; max-width: 100%; }
 *   .sheet-box-attribute table th:nth-child(3),
 *   .sheet-box-attribute table td:nth-child(3),
 *   .sheet-box-attribute table th:nth-child(4),
 *   .sheet-box-attribute table td:nth-child(4) { display: none; }
 *   .sheet-box-dice-pool { display: block; max-width: 100%; }
 *   .sheet-tab-panel-gear .repitem { flex-wrap: wrap; }
 * }
 */
```

**[CARRY-FORWARD NOTE — `.sheet-compact-target` is a SINGLE ancestor wrapper, NOT a per-element class (FINDING-1)]:** The compact selectors (`~ .sheet-compact-target .sheet-box-attribute`, `~ .sheet-compact-target .sheet-box-dice-pool`, `~ .sheet-compact-target .sheet-tab-panel-gear .repitem`) require `.sheet-compact-target` to be a **single div** that is a direct sibling of `input#sheet-compact-mode` AND wraps all tab panel content. Correct Phase 2 HTML structure:

```html
<input id="sheet-compact-mode" type="checkbox" name="attr_sheet_compact_mode">
<label for="sheet-compact-mode">Compact</label>
<!-- tab radio inputs + labels here -->
<div class="sheet-compact-target">  <!-- SINGLE wrapper -->
  <div class="sheet-tab-panel sheet-tab-panel-core">...</div>
  <div class="sheet-tab-panel sheet-tab-panel-skills">...</div>
  <div class="sheet-tab-panel sheet-tab-panel-magic">...</div>
  <div class="sheet-tab-panel sheet-tab-panel-gear">...</div>
  <div class="sheet-tab-panel sheet-tab-panel-bio">...</div>
</div>
```

Do NOT add `.sheet-compact-target` to individual elements like `.sheet-box-attribute` — `A ~ B C` requires C to be a descendant of B, and an element cannot be its own descendant. All compact selectors would fire against nothing and no CSS error would surface.

**[CARRY-FORWARD NOTE — repcontainer selector in compact context]:** If D7 confirms `.repcontainer` (not `.sheet-repcontainer`), verify the compact `flex-wrap: wrap` override still reaches weapon rows. The targeted selector is `.sheet-tab-panel-gear .repitem` which does not depend on the outer container class — this should be unaffected, but confirm.

---

### Section 16: Pre-Implementation Sandbox Verification Checklist

Run these tests in Roll20's live sandbox **before writing any CSS**. D8 drives an HTML structure decision — if it fails, Phase 2 HTML must be restructured before Phase 4 CSS can be finalized.

| # | Test | If TRUE | If FALSE |
|---|---|---|---|
| **D8** *(run first)* | Does `appearance: none` suppress native checkbox rendering on `input[type="checkbox"]` in Chrome + Firefox on Roll20? | Use `input[type="checkbox"]::before` pattern as specified in Section 6 | Restructure Phase 2 HTML: hidden checkbox + adjacent `<label>`; use `label::before` pattern |
| **D7** | Does K-scaffold generate `.sheet-repcontainer` as the outer repeating wrapper? | Keep `.sheet-repcontainer` in Sections 9 + 15 | Replace all `.sheet-repcontainer` with `.repcontainer` across Sections 9 + 15 |
| **D9** | Is `input[name="attr_tn_warning_level"]` a direct DOM sibling of `.sheet-tn-warning`? | Section 12 `~` selectors fire correctly | Reposition hidden input in Phase 2 HTML to be a true sibling of `.sheet-tn-warning` |
| **D10** | Is `input#sheet-compact-mode` a direct DOM sibling of all `.sheet-tab-panel-*` elements? | Section 15 compact toggle fires correctly | Move compact checkbox in Phase 2 HTML to tab-panel sibling level |
| **D6** | Does `@media (max-width: 500px)` apply inside Roll20's iframe? | Uncomment `@media` block in Section 15 as a supplement | Leave `@media` commented out — manual toggle is the sole compact mechanism |

---

### Section 17: Developer Guidance Notes

#### 17.1 Authoring Order

Always implement CSS regions in the order listed in Section 1. The global reset (Section 3) must precede all component rules. Roll20's injected styles will override component rules if the reset comes after them.

#### 17.2 Forbidden Constructs

Three constructs fail silently inside Roll20's iframe — never use them:
- `var(--anything)` — parent frame CSS custom properties are not accessible; resolves to `unset`
- `:root { ... }` — `:root` is the parent frame, not the sheet iframe
- `@import` — not supported inside Roll20 sheet `<style>` blocks

#### 17.3 Amendment 4-C Scoping Reference

All tab-scoped selectors use Phase 2 panel class names, not tab radio class names:

| Incorrect (dead selector) | Correct |
|---|---|
| `.sheet-tab-magic .sheet-tn-warning` | `.sheet-tab-panel-magic .sheet-tn-warning` |
| `.sheet-tab-gear .repitem` | `.sheet-tab-panel-gear .repitem` |
| `.sheet-tab-bio textarea` | `.sheet-tab-panel-bio textarea` |

#### 17.4 Weapon Row Header Alignment

The static `.sheet-weapons-header` row must exactly match the `.repitem` flex column widths from Section 13. After implementing, render at least 3 weapon rows alongside the header and confirm column label alignment visually. Any flex-basis mismatch causing drift requires a header column width adjustment — do not adjust the `.repitem` column widths.

#### 17.5 Roll Template Scope

Roll template CSS lives in the same `<style>` block as all sheet CSS — Roll20 applies it to chat output automatically. Never create a separate stylesheet for templates. The `.sheet-rolltemplate-{name}` prefix is Roll20's mandatory naming convention — do not rename. The `.sheet-template-nosuccess` selector targets the HTML wrapper of the `{{^successes}}` Mustache inverse block; it does not select the Mustache expression itself.

#### 17.6 Compact Mode Checkbox Position

Phase 2 HTML must place `<input type="checkbox" id="sheet-compact-mode" name="attr_sheet_compact_mode">` at the same DOM level as the `.sheet-tab-panel-*` wrappers. If it is nested inside a header `<div>`, the `~` combinator cannot reach `.sheet-compact-target` siblings and compact mode silently fails — no CSS error will surface.

#### 17.7 K-scaffold `.repcontrol_del` / `.repcontrol_add` Class Names

These are Roll20-injected class names on the delete and add controls. If the red/right-aligned delete button or the add row button does not render correctly, inspect the live DOM in Roll20's sandbox and adjust the selector names to match the actual generated class names. K-scaffold may wrap or rename these controls.

*Phase 4 blueprint complete.*

---

---

# Layer 3 Blueprint — Phase 5: Companion App Architecture & Data Sync

## Overview

**Input sources:**
- Layer 2 Phase 5 (Tasks 5.1–5.7) + Amendments 5-A through 5-G + all 16 DECISION resolutions
- Phase 1 blueprint: 122 scalar fields (Groups 1–19), 7 repeating section schemas (42 data fields)
- Phase 2 blueprint: Group 18 hidden fields (`char_db_id`, `char_sync_version`, `campaign_db_id`, `sync_status`), `btn_sync_db` action button per Amendment 5-B
- Phase 3 blueprint: `on('clicked:btn_sync_db', ...)` handler guidance per Amendment 5-B carry-forward

**What this blueprint produces:**
1. Turso schema specification: all 12 tables (3 entity + 1 scalar blob + 7 repeating + optional migration notes)
2. Outbound sync payload field mapping: Roll20 attribute names → JSON payload keys
3. Cloudflare Worker proxy contract: request format, validation skeleton, Turso pipeline API target
4. Roll20 Sheet Worker `btn_sync_db` handler skeleton (extends Phase 3)
5. SvelteKit project structure: file/folder layout, `adapter-cloudflare` config, environment variables
6. Auth.js Discord OAuth configuration skeleton: `hooks.server.ts`, session shape, player upsert
7. Turso client singleton pattern for Cloudflare Pages/Workers runtime
8. Route server load function skeletons: `/characters` list, `/characters/[id]` full sheet view
9. Companion app computed field recalculation reference (`computed.ts`)
10. Sandbox verification checklist: items 5-SV1 through 5-SV3 from Amendment 5-C
11. Developer guidance notes: bootstrap processes, V2 deferred items, OWASP constraints

**V1 scope boundary (non-negotiable):**
- READ-ONLY companion app — zero Turso write paths from the companion app (DECISION-08)
- Outbound sync only: Roll20 → Cloudflare Worker proxy → Turso (no inbound Pull in V1)
- Active routes: `/`, `/login`, `/auth/[...auth]`, `/characters`, `/characters/[id]`, `/logout`
- Auth: Discord OAuth via Auth.js (DECISION-12)
- Frontend: SvelteKit + `adapter-cloudflare`, deployed to Cloudflare Pages (DECISION-10, DECISION-14)
- No GM dashboard, no bidirectional sync, no offline/PWA, no character edit forms (all V2)

**Companion app implementation is a separate TEMPO workflow.** This blueprint is the handoff document for that workflow.

---

## Section 1: Turso Schema Specification

**SQLite-only types:** All columns must use SQLite-native types: `INTEGER`, `TEXT`, `REAL`, `BLOB`. No `SERIAL`, `BOOLEAN`, `UUID`, `DATETIME`, `JSON` column types — Turso is libSQL (SQLite-compatible). Booleans are `INTEGER 0/1`. UUIDs are `TEXT`. Timestamps are `TEXT` (ISO 8601). JSON blobs are `TEXT`.

---

### 1.1 `campaigns` Table

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID, application-assigned on creation |
| `name` | TEXT | NOT NULL | Campaign display name |
| `created_at` | TEXT | NOT NULL | ISO 8601 timestamp |
| `updated_at` | TEXT | NOT NULL | ISO 8601 timestamp; updated on any campaign mutation |

One row per campaign. This project has one campaign row. No FK dependencies.

---

### 1.2 `players` Table

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID, application-assigned on first login |
| `campaign_id` | TEXT | NOT NULL, FK → campaigns.id | Campaign membership |
| `display_name` | TEXT | NOT NULL | Display name from Discord profile (`profile.username`) |
| `discord_user_id` | TEXT | NOT NULL, UNIQUE | Discord user ID — stable, non-secret public identifier. This is the `auth_credential` column resolved by DECISION-02/DECISION-12. Stored as TEXT. NOT hashed — Discord user IDs are non-secret. |
| `is_gm` | INTEGER | NOT NULL DEFAULT 0 | `0` = player, `1` = GM. Set directly in Turso by the GM during campaign setup. Not self-assignable via app. Retained for V2 GM dashboard extensibility; not used for access control in V1. |
| `created_at` | TEXT | NOT NULL | ISO 8601 timestamp of first login/upsert |

One row per player. Upserted on first Discord OAuth login (`/auth/callback/discord` — Auth.js handler).

---

### 1.3 `characters` Table

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID, application-assigned on first outbound sync from Roll20 |
| `player_id` | TEXT | NOT NULL, FK → players.id | Owning player |
| `campaign_id` | TEXT | NOT NULL, FK → campaigns.id | Campaign membership (denormalized for campaign-wide dashboard queries) |
| `char_name` | TEXT | NOT NULL DEFAULT '' | Character name, denormalized from scalar blob for fast lookups. Updated on every sync cycle. |
| `is_active` | INTEGER | NOT NULL DEFAULT 1 | `1` = active character visible in app. `0` = archived. |
| `created_at` | TEXT | NOT NULL | ISO 8601 timestamp of record creation (first sync) |
| `updated_at` | TEXT | NOT NULL | ISO 8601 timestamp of last successful sync write from Roll20 (set by CF Worker proxy on each outbound push). In V1, this is always written by the outbound sync path — inbound sync (V2) will also update this field. |
| `sync_version` | INTEGER | NOT NULL DEFAULT 0 | Monotonic counter. Incremented by 1 on every successful write. Used for conflict detection (Task 5.6). `sync_version_from` in the Roll20 payload must match this value for a write to succeed (relaxed: ≤ is also accepted). |

---

### 1.4 `character_scalars` Table

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `character_id` | TEXT | PRIMARY KEY, FK → characters.id | One blob per character. Enforced unique by PK. |
| `data` | TEXT | NOT NULL | JSON-serialized object of all included scalar attributes. Keys are Roll20 attribute names (per Phase 1 contract minus excluded computed fields — see Section 2.2). SQLite `json_extract()` can query specific fields without full deserialize. |

`data` blob size estimate: 122 fields × ~20 chars avg value = ~2.5KB uncompressed. Well within Turso row limits.

[CARRY-FORWARD NOTE — JSON blob schema evolution]: As the attribute contract evolves (V2 mutations, house-rule additions), the `data` blob absorbs new fields without ALTER TABLE. The companion app JSON.parses the blob; unknown keys are ignored. A field added to Roll20 but not yet in the companion app's rendering code is silently omitted from the display — no app crash.

---

### 1.5 Repeating Section Tables

Each table uses the Roll20-assigned row ID as the primary key, preserving sync identity without a separate mapping layer. `row_order` preserves display order since Roll20 does not guarantee repeating row ordering.

**Column type conventions:** TEXT fields map to Roll20 `type: "text"` fields. INTEGER/REAL fields map to Roll20 `type: "number"` fields. For decimal fields (`mutation_essence`, `power_pp_cost_value`) use REAL. For integer-typed number fields use INTEGER.

---

#### `rep_skills`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID (e.g., `-M7X9hqxZ...`) |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | Display order |
| `skill_name` | TEXT | |
| `skill_linked_attr` | TEXT | One of: body / dex / str / cha / int / wil / hum / mag / reaction |
| `skill_general` | TEXT | |
| `skill_spec` | TEXT | |
| `skill_base` | INTEGER | |
| `skill_foci` | INTEGER | |
| `skill_misc` | INTEGER | |

`skill_total` is NOT stored — it is a worker-only computed field (Phase 1 Group, repeating_skills `worker_only: true`). Companion app recomputes from `skill_base + skill_foci + skill_misc`.

---

#### `rep_spells`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `spell_name` | TEXT | |
| `spell_type` | TEXT | "M" or "P" |
| `spell_duration` | TEXT | "I", "S", or "P" |
| `spell_target` | TEXT | |
| `spell_force` | INTEGER | |
| `spell_drain` | TEXT | Drain code string (e.g., "+2D", "F/2+2S") — stored as TEXT |

---

#### `rep_mutations`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `mutation_name` | TEXT | |
| `mutation_level` | INTEGER | |
| `mutation_essence` | REAL | Decimal: 0.2, 1.15, etc. Use REAL, not INTEGER |
| `mutation_bp_cost` | INTEGER | |
| `mutation_effect` | TEXT | |

`essence_total` (worker_only) not stored; companion app sums `mutation_essence` across rows.

---

#### `rep_adept_powers`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `power_name` | TEXT | |
| `power_level` | INTEGER | |
| `power_pp_cost` | TEXT | Display string only (e.g., "0.25/level") — human reference, NOT used for arithmetic |
| `power_pp_cost_value` | REAL | Numeric PP cost — REAL for decimal precision. Used for `power_points_used` computation. |
| `power_effect` | TEXT | |

`power_points_used` and `power_points_remaining` (worker_only) not stored; companion app computes from `SUM(power_pp_cost_value)`.

---

#### `rep_weapons`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `weapon_name` | TEXT | |
| `weapon_type` | TEXT | One of: Edged / Club / Polearm / Unarmed / Projectile / Thrown |
| `weapon_modifiers` | TEXT | |
| `weapon_power` | INTEGER | |
| `weapon_damage` | TEXT | Damage code string (e.g., "4M", "(STR)L") |
| `weapon_conceal` | INTEGER | |
| `weapon_reach` | INTEGER | |
| `weapon_ep` | INTEGER | Contributes to `ep_total` sum |
| `weapon_range_short` | TEXT | May be a number or "—" |
| `weapon_range_medium` | TEXT | |
| `weapon_range_long` | TEXT | |
| `weapon_range_extreme` | TEXT | |

`ep_total` (worker_only) not stored; companion app sums `weapon_ep` across rep_weapons + `equip_ep` across rep_equipment.

---

#### `rep_equipment`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `equip_name` | TEXT | |
| `equip_description` | TEXT | |
| `equip_ep` | INTEGER | Contributes to `ep_total` sum |

---

#### `rep_contacts`

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Roll20 row ID |
| `character_id` | TEXT FK → characters.id | |
| `row_order` | INTEGER | |
| `contact_name` | TEXT | |
| `contact_info` | TEXT | |
| `contact_level` | INTEGER | 1 = Contact, 2 = Buddy, 3 = Friend |

---

### 1.6 Index Specification

All indices named (no DDL — implementation details for developer):

| Index name | Table | Column(s) | Purpose |
|---|---|---|---|
| `idx_characters_player` | `characters` | `player_id` | Lookup all characters for authenticated player (primary `/characters` query) |
| `idx_characters_campaign` | `characters` | `campaign_id` | Lookup all characters in campaign (V2 GM dashboard) |
| `idx_scalars_char` | `character_scalars` | `character_id` (UNIQUE enforced by PK) | Fast lookup of scalar blob; uniqueness enforced |
| `idx_rep_skills_char` | `rep_skills` | `character_id` | All skill rows for character Y |
| `idx_rep_spells_char` | `rep_spells` | `character_id` | |
| `idx_rep_mutations_char` | `rep_mutations` | `character_id` | |
| `idx_rep_adept_powers_char` | `rep_adept_powers` | `character_id` | |
| `idx_rep_weapons_char` | `rep_weapons` | `character_id` | |
| `idx_rep_equipment_char` | `rep_equipment` | `character_id` | |
| `idx_rep_contacts_char` | `rep_contacts` | `character_id` | |

---

## Section 2: Sync Payload Schema

### 2.1 Outbound Payload Top-Level Structure (Roll20 → Turso)

Sent as an HTTP POST body from the Roll20 Sheet Worker (via Cloudflare Worker proxy). Always a complete snapshot — no delta patches.

```
{
  character_id:       STRING  — current value of attr 'char_db_id'; empty string "" on first sync
  campaign_id:        STRING  — current value of attr 'campaign_db_id'
  sync_version_from:  INTEGER — current value of attr 'char_sync_version' (parsed as int, default 0)
  synced_at:          STRING  — ISO 8601 timestamp from Date.now() in the Sheet Worker
  scalars:            OBJECT  — all included scalar fields (see 2.2); keys = Roll20 attr names
  repeating:          OBJECT  — 7 keys, one per section (see 2.3); each = array of row objects
}
```

**`char_db_id`, `char_sync_version`, `campaign_db_id` are excluded from the `scalars` object.** They are sent as top-level payload fields: `character_id`, `sync_version_from`, `campaign_id`.

**`sync_status` is excluded from the payload entirely.** It is a transient display field written by the Sheet Worker as a sync side-effect; it has no persistent value in Turso.

### 2.2 Scalar Field Inclusion/Exclusion Table

The `scalars` object contains all 122 Phase 1 fields MINUS the fields listed as excluded below. The proxy/Turso write handler stores the `scalars` object as `JSON.stringify(payload.scalars)` in `character_scalars.data`.

**Worker-only computed fields — EXCLUDED from `scalars`:**

These are recalculated from source fields by the companion app's `computed.ts` (Section 9). Storing them creates a double-truth problem.

| Field | Computed by | Recalculated as |
|---|---|---|
| `body`, `dex`, `str`, `cha`, `int`, `wil`, `hum`, `mag` (Group 5 totals) | L2 worker | `{attr}_base + {attr}_mutations + {attr}_magic + {attr}_misc` |
| `reaction_base` | L3 worker | `Math.floor((int + dex) / 2)` |
| `reaction` | L3 worker | `reaction_base + reaction_misc` |
| `pool_spell_base`, `pool_combat_base`, `pool_control_base`, `pool_astral_base` | L4a worker | Formula per Phase 1 Group 7 |
| `pool_spell`, `pool_combat`, `pool_control`, `pool_astral` | L4b worker | `base + misc` |
| `init_score` | L4c worker | `reaction + init_reaction_mod + init_misc_mod` |
| `ep_max` | L5 worker | `Math.max(str, body) * 4 + Math.floor(Math.min(str, body) / 2)` |
| `ep_total` | L5 worker | Sum of `weapon_ep` + `equip_ep` across repeating sections |
| `armor_total_piercing`, `armor_total_slashing`, `armor_total_impact` | L5 worker | Sum of 3 locations |
| `power_points_max` | L5 worker | `= mag` |
| `power_points_used` | L5 worker | Sum of `power_pp_cost_value` across rep_adept_powers |
| `power_points_remaining` | L5 worker | `power_points_max - power_points_used` |
| `essence_total` | L5 worker | Sum of `mutation_essence` across rep_mutations |
| `karma_total` | L6 worker | `karma_good + karma_used` |
| `cm_tn_mod` | L6 worker | `Math.max(penaltyOf(cm_mental), penaltyOf(cm_stun), penaltyOf(cm_physical))` |
| `cm_init_mod` | L6 worker | `-1 * cm_tn_mod` |
| `sustained_tn_mod` | L6 worker | `spells_sustained * 2` |
| `tn_warning_level` | L6 worker | Threshold compare on `sustained_tn_mod` |
| `skill_total` (per repeating_skills row) | L5 worker | `skill_base + skill_foci + skill_misc` (computed at row level) |

**Roll button fields — EXCLUDED:**

All `btn_*` / `roll_btn_*` / `act_btn_*` fields are HTML elements only; they are not Roll20 stored attributes and will not appear in `getAttrs()` output.

**Sync infrastructure fields — EXCLUDED from `scalars` (sent as top-level payload fields):**

`char_db_id` → `character_id`, `char_sync_version` → `sync_version_from`, `campaign_db_id` → `campaign_id`, `sync_status` → excluded entirely.

**All remaining Phase 1 fields — INCLUDED:**

Groups 1–4 (attribute sub-values and misc: 30 fields), Group 6 `reaction_misc` (1), Groups 7–8 misc/non-computed (5), Groups 9 CM inputs (4 + `cm_physical_overflow`), Groups 10–11 (10), Group 12 (0 — both ep fields excluded), Groups 13 armor inputs (12), Group 15 `spells_sustained` (1), Group 17 bio questions (20, per DECISION-05), Group 19 `sheet_compact_mode` (1).

**Total included scalar fields: 122 − 28 excluded worker-only − 4 sync infra = ~90 fields in `scalars`.**

[CARRY-FORWARD NOTE — `init_dice` inclusion]: DECISION-05 confirmed: `init_dice` (Group 8) is INCLUDED in the sync payload and stored in the scalar blob. It is player-configured data, not computed. Included in the companion app's Core tab display.

### 2.3 Repeating Section Payload Format

The `repeating` object has 7 keys, one per section. Each value is an array of row objects. Each row object contains:
- `_rowId`: the Roll20-assigned row ID string (e.g., `-M7X9hqxZ...`)
- `_rowOrder`: integer position for `row_order` column
- All data fields for that section per the Section 1.5 table definitions

**Example `repeating.skills` entry:**
```
{
  _rowId: "-M7X9hqxZ...",
  _rowOrder: 0,
  skill_name: "Pistols",
  skill_linked_attr: "dex",
  skill_general: "Combat",
  skill_spec: "Semi-Auto",
  skill_base: 5,
  skill_foci: 1,
  skill_misc: 0
}
```

`skill_total` is NOT included in the row object (excluded computed field).

**Included repeating sections (7 keys):**
`skills`, `spells`, `mutations`, `adept_powers`, `weapons`, `equipment`, `contacts`

---

## Section 3: Cloudflare Worker Proxy

The proxy is a **standalone Cloudflare Worker** — NOT part of the SvelteKit Pages app. It is deployed separately (e.g., in a `proxy/` subdirectory of the monorepo with its own `wrangler.toml`). It receives the sync payload from Roll20's Sheet Worker and forwards it to Turso's HTTP pipeline API, holding the real Turso write token server-side in Cloudflare Worker environment variables.

### 3.1 Request Contract (Roll20 → Proxy)

```
POST {PROXY_URL}/sync
Content-Type: application/json
X-Campaign-Secret: {value of Roll20 sheet attribute 'attr_campaign_secret'}

Body: {full payload JSON from Section 2.1}
```

[CARRY-FORWARD NOTE — Amendment 5-G: proxy security scope]: The `campaign_secret` value in the Roll20 sheet attribute IS readable by all 6 players with the sheet open. The proxy's security benefit is that the real Turso write token is never transmitted to the browser. A player who knows the `campaign_secret` and proxy URL could craft write requests. Under the stated threat model (6 known trusted players), this is an accepted residual risk. Document in companion app README.

### 3.2 Proxy Validation Skeleton

```
WORKER ENTRY: fetch(request, env)

1. Validate request method: reject non-POST with 405
2. Validate X-Campaign-Secret header:
     if header !== env.CAMPAIGN_SECRET → return 401
3. Parse JSON body; reject malformed JSON with 400
4. Validate required fields:
     - payload.campaign_id is non-empty string
     - payload.campaign_id === env.KNOWN_CAMPAIGN_ID  (hardcoded expected value)
     - payload.character_id is string (may be empty on first sync)
     - payload.scalars is an object
     - payload.repeating is an object with 7 expected keys
   → missing/invalid fields: return 400 with descriptive message
5. If payload.character_id === "":
     — first-sync path: generate a new UUID for this character
     — CREATE character record in Turso before proceeding to write
     — store generated UUID; include in response body so Sheet Worker can save it
6. Forward payload to Turso via Section 3.3 pipeline API
7. On Turso success:
     — return 200 with JSON body: { ok: true, char_db_id: <uuid>, new_sync_version: <N> }
8. On Turso failure:
     — return 502 with JSON body: { ok: false, error: <turso_error_message> }
```

**Environment variables required (Cloudflare Worker):**
- `CAMPAIGN_SECRET` — the shared secret value matched against the `X-Campaign-Secret` header
- `KNOWN_CAMPAIGN_ID` — the Turso campaign UUID for this campaign
- `TURSO_DB_URL` — `https://{db-name}-{org}.turso.io` (HTTP URL scheme — not `libsql://`)
- `TURSO_WRITE_TOKEN` — write-only, single-database-scoped Turso token (never transmitted to client)

### 3.3 Turso HTTP Pipeline API Target

**Endpoint:** `POST {TURSO_DB_URL}/v2/pipeline`  
**Auth header:** `Authorization: Bearer {TURSO_WRITE_TOKEN}`  
**Content-Type:** `application/json`

**Pipeline request structure (batched transaction):**

```json
{
  "requests": [
    { "type": "execute", "stmt": { "sql": "BEGIN" } },

    // Character upsert (scalar blob)
    { "type": "execute", "stmt": {
      "sql": "INSERT INTO character_scalars (character_id, data) VALUES (?, ?) ON CONFLICT(character_id) DO UPDATE SET data = excluded.data",
      "args": [ { "type": "text", "value": "<character_id>" },
                { "type": "text", "value": "<JSON.stringify(payload.scalars)>" } ]
    }},

    // Update characters.char_name + updated_at + sync_version
    { "type": "execute", "stmt": {
      "sql": "UPDATE characters SET char_name = ?, updated_at = ?, sync_version = sync_version + 1 WHERE id = ?",
      "args": [ { "type": "text", "value": "<payload.scalars.char_name>" },
                { "type": "text", "value": "<payload.synced_at>" },
                { "type": "text", "value": "<character_id>" } ]
    }},

    // For each of 7 rep_* tables: DELETE then INSERT
    { "type": "execute", "stmt": {
      "sql": "DELETE FROM rep_skills WHERE character_id = ?",
      "args": [ { "type": "text", "value": "<character_id>" } ]
    }},
    // ... INSERT per row from payload.repeating.skills ...
    // Same pattern for rep_spells, rep_mutations, rep_adept_powers,
    //   rep_weapons, rep_equipment, rep_contacts

    { "type": "execute", "stmt": { "sql": "COMMIT" } }
  ]
}
```

**Atomicity (Amendment 5-E):** BEGIN / COMMIT wraps all statements in a single transaction. If any statement fails, Turso rolls back the entire batch. No partial writes can be committed.

**After successful pipeline write:** Query `SELECT sync_version FROM characters WHERE id = ?` to retrieve the incremented `sync_version` value. Return it as `new_sync_version` in the 200 response body so the Sheet Worker can update `char_sync_version`.

### 3.4 First-Sync (Empty `character_id`) Path

Triggered when `payload.character_id === ""` — Roll20 sheet has never synced to Turso before.

```
1. Generate UUID (crypto.randomUUID() — available in CF Workers runtime)
2. Build the pipeline transaction for this first-sync, inserting the characters row
   AS THE FIRST STATEMENT inside the BEGIN/COMMIT block:

     BEGIN
     INSERT INTO characters (id, player_id, campaign_id, char_name, is_active, created_at, updated_at, sync_version)
       VALUES (uuid, <player_id_lookup>, <campaign_id>, <char_name>, 1, <now>, <now>, 0)
     — followed by the standard INSERT INTO character_scalars, 7×DELETE, N×INSERT, UPDATE characters statements
     COMMIT

   **CRITICAL — atomicity (Amendment 5-E):** Do NOT INSERT INTO characters outside the transaction
   and then run the pipeline separately. If the out-of-transaction INSERT succeeds but the pipeline
   fails, Turso is left with a characters row that has no scalar blob and no rep rows — an invalid
   state. ALL first-sync statements including the characters INSERT must be inside BEGIN/COMMIT.

   — player_id_lookup: proxy may derive from X-Player-Token or a separate player handshake.
     Simplest V1: include player_id as a payload field OR player is resolved from campaign.
     See NOTE below.
3. Return { ok: true, char_db_id: uuid, new_sync_version: 1 }
```

[CARRY-FORWARD NOTE — player_id resolution in first-sync]: The proxy needs to know which `players.id` to associate with the new character on first sync. Options: (a) include `player_discord_id` as an extra payload field from the Sheet Worker — the proxy queries `players.discord_user_id = payload.player_discord_id`; (b) GM manually inserts the first character row in Turso and assigns a known UUID in the Roll20 `char_db_id` attribute. Option (b) is simplest for V1 (no additional payload field). Option (a) is cleaner but requires the player's Discord user ID to be stored as a Roll20 attribute. Decision is implementation-time; document in companion app operational README.

---

## Section 4: Roll20 Sheet Worker Sync Handler

This section extends Phase 3 Section 10 (`btn_sync_db` handler). The Phase 3 blueprint listed the handler name and high-level steps. This blueprint provides the structural skeleton with all data-gathering steps fully specified.

**Handler name:** `on('clicked:btn_sync_db', ...)`  
**Location in Sheet Worker:** After the cascade worker registrations; before `k.sheetOpens`.

### 4.1 Scalar Fields Array

The handler must declare the complete list of included scalar field names to pass to `getAttrs()`. These are all Phase 1 Group 1–4 sub-fields + Phase 1 non-computed non-sync-infra fields:

```
SCALAR_FIELDS_TO_SYNC = [
  // Group 1 — attribute base values
  'body_base', 'dex_base', 'str_base', 'cha_base', 'int_base', 'wil_base', 'hum_base', 'mag_base',
  // Group 2 — attribute mutation sub-values (mag excluded)
  'body_mutations', 'dex_mutations', 'str_mutations', 'cha_mutations', 'int_mutations', 'wil_mutations', 'hum_mutations',
  // Group 3 — attribute magic sub-values (mag excluded)
  'body_magic', 'dex_magic', 'str_magic', 'cha_magic', 'int_magic', 'wil_magic', 'hum_magic',
  // Group 4 — misc modifiers (all 8 including mag)
  'body_misc', 'dex_misc', 'str_misc', 'cha_misc', 'int_misc', 'wil_misc', 'hum_misc', 'mag_misc',
  // Group 6 — reaction misc (the only non-computed reaction field)
  'reaction_misc',
  // Group 7 — pool misc modifiers (non-computed)
  'pool_spell_misc', 'pool_combat_misc', 'pool_control_misc', 'pool_astral_misc',
  // Group 8 — Initiative (init_dice included per DECISION-05; init_score excluded worker_only)
  'init_dice', 'init_reaction_mod', 'init_misc_mod',
  // Group 9 — Condition Monitor inputs
  'cm_mental', 'cm_stun', 'cm_physical', 'cm_physical_overflow',
  // Group 10 — Character Identity
  'char_name', 'char_race_station', 'char_sex', 'char_age', 'char_description', 'char_notes',
  // Group 11 — Karma (karma_total excluded worker_only)
  'karma_good', 'karma_used', 'karma_pool',
  // Group 13 — Armor Inputs (armor totals excluded worker_only)
  'armor_torso_name', 'armor_torso_piercing', 'armor_torso_slashing', 'armor_torso_impact',
  'armor_legs_name', 'armor_legs_piercing', 'armor_legs_slashing', 'armor_legs_impact',
  'armor_head_name', 'armor_head_piercing', 'armor_head_slashing', 'armor_head_impact',
  // Group 15 — spells_sustained (only non-computed field)
  'spells_sustained',
  // Group 17 — Bio Questions (all 20; DECISION-05 confirmed)
  'bio_q01','bio_q02','bio_q03','bio_q04','bio_q05','bio_q06','bio_q07','bio_q08','bio_q09','bio_q10',
  'bio_q11','bio_q12','bio_q13','bio_q14','bio_q15','bio_q16','bio_q17','bio_q18','bio_q19','bio_q20',
  // Group 19 — UI state
  'sheet_compact_mode'
]
```

**Do NOT include in this array:** `char_db_id`, `char_sync_version`, `campaign_db_id`, `sync_status` — these are fetched separately as the sync control fields.

### 4.2 Handler Skeleton

```
on('clicked:btn_sync_db', function() {

  // Step 1: Fetch sync control fields first
  getAttrs(['char_db_id', 'campaign_db_id', 'char_sync_version'], function(control) {
    const campaignId = (control['campaign_db_id'] || '').trim();
    const charDbId   = (control['char_db_id'] || '').trim();
    const syncVersion = parseInt(control['char_sync_version']) || 0;

    // Guard: campaign must be configured
    if (!campaignId) {
      setAttrs({ sync_status: 'Sync failed — campaign_db_id not set. Ask GM.' });
      sendChat('Sheet Worker', 'Sync error: campaign_db_id is empty. Have the GM set it first.');
      return;
    }

    // Step 2: Fetch all scalar fields
    getAttrs(SCALAR_FIELDS_TO_SYNC, function(attrs) {

      // Build scalars object from attrs; coerce number fields to avoid string drift
      const scalars = {};
      SCALAR_FIELDS_TO_SYNC.forEach(function(field) {
        scalars[field] = attrs[field] !== undefined ? attrs[field] : '';
      });

      // Step 3: Gather all 7 repeating sections serially via getSectionIDs
      //   Use a sequential reduce or nested callback chain across the 7 sections
      //   Developer note: promisifying getSectionIDs + getAttrs is strongly recommended
      //   to avoid callback pyramid. Pseudocode below shows the structure; implementation
      //   may use a promise-based wrapper.

      COLLECT_REPEATING_SECTIONS(
        ['skills', 'spells', 'mutations', 'adept_powers', 'weapons', 'equipment', 'contacts'],
        // For each section, collect all data field names per Section 2.3 row structure
        // Returns { skills: [...], spells: [...], ..., contacts: [...] }
        function(repeating) {

          // Step 4: Build full payload
          const payload = {
            character_id:      charDbId,
            campaign_id:       campaignId,
            sync_version_from: syncVersion,
            synced_at:         new Date().toISOString(),
            scalars:           scalars,
            repeating:         repeating
          };

          // Step 5: POST to proxy
          fetch(PROXY_URL, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Campaign-Secret': CAMPAIGN_SECRET
            },
            body: JSON.stringify(payload)
          })
          .then(function(res) { return res.json(); })
          .then(function(data) {
            if (data.ok) {
              // Step 6: Update sync control fields on success
              const updates = {
                char_sync_version: data.new_sync_version,
                sync_status: 'Synced \u2713 \u2014 ' + new Date().toLocaleString()
              };
              if (charDbId === '' && data.char_db_id) {
                updates.char_db_id = data.char_db_id;
              }
              setAttrs(updates);
              // No chat on success (DECISION-07: chat is for errors only)
            } else {
              setAttrs({ sync_status: 'Sync failed \u2014 ' + (data.error || 'unknown error') });
              sendChat('Sheet Worker', 'Sync failed: ' + (data.error || 'unknown error'));
            }
          })
          .catch(function(err) {
            setAttrs({ sync_status: 'Sync failed \u2014 network error' });
            sendChat('Sheet Worker', 'Sync failed (network): ' + String(err));
          });

        }// end repeating callback
      );

    }); // end getAttrs scalars
  }); // end getAttrs control

}); // end on clicked:btn_sync_db
```

**`PROXY_URL` and `CAMPAIGN_SECRET` constants:** Defined as module-level constants at the top of the Sheet Worker JS. `PROXY_URL` is the Cloudflare Worker URL (public; safe to hardcode). `CAMPAIGN_SECRET` is a Roll20 sheet attribute read via `getAttrs` in the handler if the proxy requires it, OR a hardcoded lightweight value — see Amendment 5-G.

**`COLLECT_REPEATING_SECTIONS` helper:** Developer-implemented function that serially calls `getSectionIDs` + `getAttrs` for each of the 7 sections and assembles the combined `repeating` object. The Roll20 Sheet Worker sandbox does not support native Promises, but K-scaffold may expose a queue or the developer can implement a serial callback chain. Each section's row objects must include `_rowId` and `_rowOrder` per Section 2.3.

---

## Section 5: SvelteKit Project Structure

### 5.1 Directory Layout

```
companion-app/
├── src/
│   ├── app.html                          — HTML shell template
│   ├── app.d.ts                          — TypeScript global types (Session, Locals augmentation)
│   ├── hooks.server.ts                   — Auth.js SvelteKitAuth handle export (Section 6)
│   ├── lib/
│   │   ├── db.ts                         — Turso @libsql/client singleton (Section 7)
│   │   ├── computed.ts                   — Derived field recalculation (Section 9.2)
│   │   └── types.ts                      — TypeScript interfaces: Character, ScalarBlob, RepRow, Session
│   └── routes/
│       ├── +layout.server.ts             — Session guard: redirect to /login if unauthenticated
│       ├── +layout.svelte                — Nav shell (player name, character list link, logout)
│       ├── +page.svelte                  — / landing: redirect authenticated → /characters
│       ├── login/
│       │   └── +page.svelte              — Discord OAuth button: <a href="/auth/signin/discord">
│       ├── auth/
│       │   └── [...auth]/
│       │       └── +server.ts            — Auth.js catch-all route handler (handles /auth/signin,
│       │                                     /auth/callback/discord, /auth/signout, etc.)
│       ├── characters/
│       │   ├── +page.server.ts           — load(): query characters for authenticated player
│       │   ├── +page.svelte              — Character list with name, race/station, active status
│       │   └── [id]/
│       │       ├── +page.server.ts       — load(): query full character (scalars + 7 rep tables)
│       │       └── +page.svelte          — Read-only character sheet (tabbed, matches Roll20 layout)
│       └── logout/
│           └── +server.ts                — GET handler: Auth.js signOut() → redirect to /
├── static/
│   └── favicon.ico
├── svelte.config.js                      — adapter-cloudflare
├── vite.config.ts
├── tsconfig.json
├── package.json
├── .env                                  — NOT committed; holds DISCORD_CLIENT_ID, etc.
└── wrangler.toml                         — Cloudflare Pages deployment config
```

### 5.2 Key Dependencies

```json
{
  "dependencies": {
    "@auth/sveltekit": "latest",
    "@auth/core": "latest",
    "@libsql/client": "latest"
  },
  "devDependencies": {
    "@sveltejs/adapter-cloudflare": "latest",
    "@sveltejs/kit": "latest",
    "svelte": "latest",
    "typescript": "latest",
    "vite": "latest"
  }
}
```

[CARRY-FORWARD NOTE — `@libsql/client` import for Cloudflare edge runtime]: Cloudflare Pages/Workers runs in the Workers runtime (not Node.js). Import the edge-compatible Turso client:
```typescript
import { createClient } from '@libsql/client/web';
```
NOT `from '@libsql/client'` (the default export uses Node.js native modules). The `/web` subpath export uses the Fetch API and is compatible with the Workers runtime. If `@libsql/client/web` is not available in the installed version, use the HTTP URL scheme (`https://` prefix on the Turso DB URL) with the standard import — the HTTP transport does not require Node.js net/tls.

### 5.3 `svelte.config.js` Skeleton

```javascript
import adapter from '@sveltejs/adapter-cloudflare';

const config = {
  kit: {
    adapter: adapter(),
    // Auth.js requires: exclude /auth/* routes from prerendering
    prerender: { entries: [] }
  }
};

export default config;
```

### 5.4 Environment Variables

Stored in `.env.local` (not `.env` — the `.local` file is gitignored by SvelteKit's default `.gitignore`). For Cloudflare Pages production, these are set as Pages environment variables in the Cloudflare dashboard:

| Variable | Description | Used by |
|---|---|---|
| `DISCORD_CLIENT_ID` | Discord developer app OAuth client ID | Auth.js |
| `DISCORD_CLIENT_SECRET` | Discord developer app OAuth client secret | Auth.js |
| `AUTH_SECRET` | Random 32+ char secret for Auth.js JWT signing | Auth.js |
| `TURSO_APP_URL` | `https://{db-name}-{org}.turso.io` | companion app server load functions |
| `TURSO_APP_TOKEN` | Turso read+write token, scoped to campaign database. NEVER the same token as the CF Worker proxy's write-only token. Lives in Cloudflare Pages env vars only — never transmitted to the browser. | companion app server load functions |

---

## Section 6: Auth.js Discord OAuth Configuration

### 6.1 `hooks.server.ts` Skeleton

```typescript
import { SvelteKitAuth } from '@auth/sveltekit';
import Discord from '@auth/core/providers/discord';
import { db } from '$lib/db';

export const { handle } = SvelteKitAuth(async (event) => ({
  providers: [
    Discord({
      clientId: event.platform?.env.DISCORD_CLIENT_ID,
      clientSecret: event.platform?.env.DISCORD_CLIENT_SECRET,
    }),
  ],
  secret: event.platform?.env.AUTH_SECRET,
  trustHost: true,
  callbacks: {
    async jwt({ token, account, profile }) {
      // account and profile are only populated on the first sign-in.
      // This is the ONLY place where player_id can be persisted into the JWT —
      // signIn() callback cannot return player_id to the token.
      if (account && profile) {
        token.discord_user_id = profile.id;
        // Upsert player and get player_id (see 6.2)
        // db requires env — pass event.platform.env into SvelteKitAuth via the async form
        const playerId = await upsertAndGetPlayerId(profile, env);
        token.player_id = playerId;
      }
      return token;
    },
    async session({ session, token }) {
      // Copy from JWT token to session object (see 6.3 for app.d.ts augmentation)
      session.discord_user_id = token.discord_user_id as string;
      session.player_id = token.player_id as string;
      return session;
    },
  },
}));
```

[CARRY-FORWARD NOTE — Cloudflare Pages env access pattern]: In `adapter-cloudflare`, environment variables are accessed via `event.platform?.env.VARIABLE_NAME` in hooks and server load functions, NOT via `process.env.VARIABLE_NAME` (Node.js-only). If using `$env/dynamic/private` from SvelteKit's virtual module, that also works on Cloudflare Pages for build-time env vars. Verify which pattern is preferred for your Auth.js + SvelteKit + Cloudflare setup — the `event.platform.env` pattern is the most reliable at runtime.

### 6.2 First-Login Player Upsert (`signIn` callback)

```
On signIn with profile:
  1. Extract discord_user_id = profile.id  (stable Discord snowflake ID)
  2. Query: SELECT id FROM players WHERE discord_user_id = ?
  3. If row exists: player already registered; proceed
  4. If no row:
       Generate new player UUID
       INSERT INTO players (id, campaign_id, display_name, discord_user_id, is_gm, created_at)
       VALUES (uuid, KNOWN_CAMPAIGN_ID, profile.username, profile.id, 0, now)
       is_gm defaults to 0; GM sets their own flag manually in Turso
  5. Store player_id (UUID) in JWT token for session attachment
```

[CARRY-FORWARD NOTE — KNOWN_CAMPAIGN_ID bootstrap]: The single campaign row must exist in Turso before any player can log in. GM inserts this row manually (or via a one-time setup script) before deploying the companion app. The `KNOWN_CAMPAIGN_ID` value is then hardcoded in the companion app's environment or the hooks file as a constant.

### 6.3 Session Shape (`app.d.ts` augmentation)

```typescript
declare module '@auth/core/types' {
  interface Session {
    user: {
      name?: string | null;
      email?: string | null;
      image?: string | null;
    };
    discord_user_id: string;  // Discord snowflake ID — stable across sessions
    player_id: string;        // Turso players.id UUID for this authenticated player
  }
}
```

The `player_id` is the key used in all Turso ownership checks (authoritative identification for `characters.player_id = session.player_id`).

---

## Section 7: Turso Client Singleton

```typescript
// src/lib/db.ts
import { createClient, type Client } from '@libsql/client/web';

let _client: Client | null = null;

export function getDb(env: { TURSO_APP_URL: string; TURSO_APP_TOKEN: string }): Client {
  if (!_client) {
    _client = createClient({
      url: env.TURSO_APP_URL,
      authToken: env.TURSO_APP_TOKEN,
    });
  }
  return _client;
}
```

[CARRY-FORWARD NOTE — Singleton in Cloudflare Workers runtime]: Cloudflare Workers may re-instantiate between requests in some edge cases. The singleton pattern is still preferred to avoid unnecessary connection overhead, but developers should not rely on the singleton surviving across all requests. If connection errors occur, recreating the client is safe.

**All Turso queries must use parameterized syntax (Amendment 5-F, OWASP A03):**

```typescript
// CORRECT — parameterized
await db.execute({
  sql: 'SELECT * FROM characters WHERE player_id = ? AND is_active = 1',
  args: [session.player_id],
});

// FORBIDDEN — string concatenation
await db.execute(`SELECT * FROM characters WHERE player_id = '${session.player_id}'`);
```

No exceptions. This applies to all WHERE clause values, all INSERT values, all UPDATE SET values.

---

## Section 8: Route Server Load Functions

### 8.1 `/characters` — `+page.server.ts`

**Purpose:** List all characters owned by the authenticated player.

```
load(event):
  1. session = await event.locals.auth()
     if !session → throw redirect(302, '/login')

  2. db = getDb(event.platform.env)

  3. result = db.execute({
       sql: 'SELECT id, char_name, char_race_station, is_active, updated_at FROM characters
             WHERE player_id = ? AND is_active = 1
             ORDER BY char_name ASC',
       args: [session.player_id]
     })

  4. return { characters: result.rows }
```

**Page component receives:** `data.characters` — array of `{ id, char_name, char_race_station, is_active, updated_at }`.

No scalar blob or repeating data needed on the list page.

### 8.2 `/characters/[id]` — `+page.server.ts`

**Purpose:** Full character sheet view (read-only).

```
load(event):
  1. session = await event.locals.auth()
     if !session → throw redirect(302, '/login')

  2. characterId = event.params.id
     — basic UUID format validation (non-empty string with expected format);
       reject obviously malformed IDs with 400 before hitting the DB

  3. db = getDb(event.platform.env)

  4. charResult = db.execute({
       sql: 'SELECT c.id, c.char_name, c.sync_version, c.updated_at,
                    cs.data as scalar_data
             FROM characters c
             JOIN character_scalars cs ON cs.character_id = c.id
             WHERE c.id = ? AND c.player_id = ?',
       args: [characterId, session.player_id]
     })
     if charResult.rows.length === 0 → throw error(404, 'Character not found')
     — The player_id check in the WHERE clause IS the ownership guard.
       A player who guesses another character's UUID gets 404, not the sheet.

  5. scalars = JSON.parse(charResult.rows[0].scalar_data)

  6. Fetch all 7 repeating sections in parallel:
     [skills, spells, mutations, powers, weapons, equipment, contacts] = await Promise.all([
       db.execute({ sql: 'SELECT * FROM rep_skills WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_spells WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_mutations WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_adept_powers WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_weapons WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_equipment WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
       db.execute({ sql: 'SELECT * FROM rep_contacts WHERE character_id = ? ORDER BY row_order', args: [characterId] }),
     ])

  7. derived = computeDerivedFields(scalars, {
       skills: skills.rows,
       mutations: mutations.rows,
       adept_powers: powers.rows,
       weapons: weapons.rows,
       equipment: equipment.rows,
     })

  8. return {
       character: charResult.rows[0],
       scalars,
       repeating: {
         skills: skills.rows, spells: spells.rows, mutations: mutations.rows,
         adept_powers: powers.rows, weapons: weapons.rows,
         equipment: equipment.rows, contacts: contacts.rows,
       },
       derived
     }
```

**Ownership model note:** The `WHERE c.id = ? AND c.player_id = ?` pattern is the access control gate. It must be present on every character read query with no exception. An authenticated player who does not own character `[id]` receives a 404 — not a 403, to avoid leaking existence information.

### 8.3 `/logout` — `+server.ts`

```typescript
// GET handler
import { signOut } from '@auth/sveltekit';
export const GET = signOut({ redirectTo: '/' });
```

---

## Section 9: Companion App Data Rendering

### 9.1 Character Sheet Tab Structure

The `/characters/[id]` page renders tabs matching the Roll20 sheet layout. Tab visibility and content mirrors Phase 2 HTML structure:

| Tab | Content source | Visibility gate |
|---|---|---|
| Core | `scalars` (attributes, condition monitors, pools, init, armor, karma, sync status) | Always visible |
| Skills | `repeating.skills` | Always visible |
| Magic | `repeating.spells`, `repeating.mutations`, `repeating.adept_powers`; magic scalar fields | Only rendered if `scalars.mag_base > 0 OR scalars.mag_magic > 0 OR scalars.mag_misc > 0` (i.e., `derived.mag > 0`) |
| Gear | `repeating.weapons`, `repeating.equipment` | Always visible |
| Bio | `scalars.bio_q01`–`bio_q20`, `scalars.char_description`, `scalars.char_notes`, `repeating.contacts` | Always visible |

Compact mode (`sheet_compact_mode`) is Roll20-only CSS behavior; not meaningful in the companion app. Ignore this field.

### 9.2 Computed Field Recalculation (`computed.ts`)

The `computeDerivedFields` function mirrors the Phase 3 Sheet Worker cascade exactly. All formulas are from Phase 1 Groups 1–16 and the Phase 5 Section 2.2 exclusion table.

```typescript
// src/lib/computed.ts
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
  skill_total: Record<string, number>;   // keyed by Roll20 row ID
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
  const gf = (k: string, fb = 0) => parseFloat(String(s[k] ?? fb)) || fb;

  // L2 — Attribute totals
  const body = gi('body_base') + gi('body_mutations') + gi('body_magic') + gi('body_misc');
  const dex  = gi('dex_base')  + gi('dex_mutations')  + gi('dex_magic')  + gi('dex_misc');
  const str  = gi('str_base')  + gi('str_mutations')  + gi('str_magic')  + gi('str_misc');
  const cha  = gi('cha_base')  + gi('cha_mutations')  + gi('cha_magic')  + gi('cha_misc');
  const int  = gi('int_base')  + gi('int_mutations')  + gi('int_magic')  + gi('int_misc');
  const wil  = gi('wil_base')  + gi('wil_mutations')  + gi('wil_magic')  + gi('wil_misc');
  const hum  = gi('hum_base')  + gi('hum_mutations')  + gi('hum_magic')  + gi('hum_misc');
  const mag  = gi('mag_base')  + gi('mag_misc');  // no mutations/magic sub-fields

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

  // L4c — Initiative score
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
  // Matches Phase 1 Group 16 and Phase 3 Task 3.12: worker computes parseFloat sum of mutation_essence rows.
  // To display REMAINING essence, the page component renders: 6.0 - derived.essence_total
  // Do NOT compute 6.0 - sum here — that would disagree with the Roll20 attribute's value.
  const essence_total = rep.mutations.reduce((s, r) => s + (parseFloat(String(r.mutation_essence)) || 0), 0);

  // L6 — Modifiers
  const karma_total = gi('karma_good') + gi('karma_used');

  const penaltyOf = (lvl: number) => Math.min(lvl, 3);
  const cm_tn_mod   = Math.max(penaltyOf(gi('cm_mental')), penaltyOf(gi('cm_stun')), penaltyOf(gi('cm_physical')));
  const cm_init_mod = -1 * cm_tn_mod;

  const sustained_tn_mod = gi('spells_sustained') * 2;
  const tn_warning_level = sustained_tn_mod >= 6 ? 3 : sustained_tn_mod >= 4 ? 2 : sustained_tn_mod >= 2 ? 1 : 0;

  // Per-row skill totals
  const skill_total: Record<string, number> = {};
  rep.skills.forEach((row) => {
    const rowId = String(row.id);
    skill_total[rowId] = (parseInt(String(row.skill_base)) || 0)
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

[CARRY-FORWARD NOTE — essence formula direction]: `essence_total` = total essence SPENT (SUM of `mutation_essence` rows). This matches the Phase 3 Sheet Worker formula (Task 3.12) and stores the same semantic value as the Roll20 attribute. The companion app page component renders REMAINING essence as `{6.0 - derived.essence_total}` — NOT `{derived.essence_total}` directly. If a feature requires displaying spent vs. remaining in the companion app, the `computed.ts` value is SPENT; subtract from 6.0 at the render layer.

### 9.3 Magic Tab Visibility Gate

The Magic tab renders only if the character has any magic attribute allocation:

```svelte
{#if derived.mag > 0}
  <!-- Magic tab content -->
{/if}
```

This mirrors the Phase 2 HTML conditional rendering note for the `has_magic` implied condition. In the companion app, `derived.mag` (the computed attribute total) is the guard — no separate `has_magic` field is needed.

---

## Section 10: Sandbox Verification Checklist

These items are from Amendment 5-C. They must be verified in the Roll20 Sheet Worker sandbox before companion app integration begins.

| ID | Test | Expected Result |
|---|---|---|
| 5-SV1 | Fire `clicked:btn_sync_db` from a `<button type="action" name="act_btn_sync_db">` element; confirm the `on('clicked:btn_sync_db', ...)` Sheet Worker handler fires WITHOUT triggering a dice roll in Roll20 chat | Handler fires; no roll output appears in chat; action button confirmed viable for non-roll network triggers |
| 5-SV2 | Call K-scaffold's `removeRepeatingRow(rowId)` for a known repeating section row; confirm the row is removed from the Roll20 sheet DOM and that no error is thrown in the Sheet Worker console | Row removed from DOM; K-scaffold wrapper confirmed to expose `removeRepeatingRow`; no console errors |
| 5-SV3 | Call `setAttrs({ 'repeating_skills_-NEWTESTID_skill_name': 'TestSkill' })` where `-NEWTESTID` is a row ID that does not currently exist in the sheet; confirm a new row is created with that exact row ID value | New row created in `repeating_skills` section; row ID matches `-NEWTESTID`; setAttrs-based row creation confirmed in K-scaffold context |

[CARRY-FORWARD NOTE — Sandbox verification timing]: Items 5-SV1 through 5-SV3 should be tested BEFORE Roll20 Sheet Worker sync code is written. Discovering that action buttons trigger rolls (SV1), that `removeRepeatingRow` is unavailable (SV2), or that row creation by ID doesn't work (SV3) would require significant rework of the K-scaffold sync handler design. Test these first.

---

## Section 11: Developer Guidance Notes

### 11.1 `campaign_db_id` Bootstrap Process

**The companion app is read-only in V1 — there is no UI to set `campaign_db_id`.** This value must be initialized via a two-step manual process:

1. **Before first sync:** GM inserts the campaign row into Turso directly (via Turso shell or API) with a known UUID. This UUID is also stored in the Cloudflare Worker's `KNOWN_CAMPAIGN_ID` environment variable.

2. **Set on the Roll20 sheet:** GM opens the Roll20 character sheet and manually types the campaign UUID into the `campaign_db_id` attribute input (the hidden input field from Phase 2 Group 18). Alternatively, a one-time setup button or a script console call can set it.

Once `campaign_db_id` is non-empty, all subsequent sync calls include it in the payload. The proxy validates it against `env.KNOWN_CAMPAIGN_ID`.

### 11.2 `char_db_id` First-Sync UUID Assignment

On the first outbound sync, `char_db_id === ""`. The flow:

1. Proxy detects `payload.character_id === ""`
2. Proxy creates the character row in Turso with a new UUID
3. Proxy returns `{ ok: true, char_db_id: <new-uuid>, new_sync_version: 1 }`
4. Sheet Worker calls `setAttrs({ char_db_id: data.char_db_id, char_sync_version: 1 })`
5. All subsequent syncs use the persisted UUID

The `char_db_id` attribute is effectively write-once from Roll20's perspective — once set, the Sheet Worker only reads it, never overwrites it.

### 11.3 V2 Deferred Items

The following are explicitly out of V1 scope. Do not implement:

| Item | Deferred to | DECISION ref |
|---|---|---|
| `btn_pull_db` action button | V2 companion app workflow | DECISION-08 |
| `on('clicked:btn_pull_db', ...)` Sheet Worker handler | V2 | DECISION-08 |
| `k.sheetOpens` auto-pull guard | V2 | DECISION-08 |
| Companion app character edit forms | V2 | DECISION-08 |
| Write paths in companion app (companion app → Turso) | V2 | DECISION-08 |
| Conflict resolution (sync_version conflict behavior) | V2 | DECISION-16 (N/A in V1) |
| Offline/PWA service worker caching | V2 | DECISION-13 |
| GM dashboard routes (`/gm`, `/gm/[id]`) | V2 | DECISION-15 |
| Debounced idle-batch sync trigger (Option D) | V2 | DECISION-04 |
| `/characters/new` route (companion-app-side character creation) | V2 | DECISION-15 cascade |

`sync_version` IS maintained in V1 (Turso increments it on every outbound push; Roll20 updates `char_sync_version`) to ensure V2 bidirectional sync can be implemented without a migration.

### 11.4 OWASP A03 — Parameterized Query Mandate (Amendment 5-F)

Every Turso read and write in the companion app and the Cloudflare Worker proxy MUST use the `@libsql/client` parameterized query interface. Zero exceptions:

```typescript
// Required pattern
await db.execute({ sql: 'SELECT ... WHERE id = ?', args: [id] });

// Forbidden — SQL injection vector
await db.execute(`SELECT ... WHERE id = '${id}'`);
```

This applies to: character ID lookups, player ID lookups, scalar blob UPSERT (JSON.stringify is a parameter, not interpolated), all repeating section INSERT/DELETE WHERE clauses, all route param values (`event.params.id`).

### 11.5 Atomic Transaction Mandate (Amendment 5-E)

All Turso writes for a single sync payload (scalar UPSERT + 7 × DELETE + N × INSERT) MUST use the Turso HTTP pipeline API with BEGIN/COMMIT wrapping. A partial write (e.g., scalar blob updated but `rep_weapons` not written) is an invalid database state. The next inbound pull (V2) would populate Roll20 with inconsistent data.

The companion app's character save operations (V2) must apply the same atomicity: scalar update + repeating section modification(s) in a single transaction.

### 11.6 Proxy Secret Scope Transparency (Amendment 5-G)

The `campaign_secret` value sent by the Roll20 Sheet Worker (`X-Campaign-Secret` header) is stored as a Roll20 sheet attribute, readable by all 6 players. This is an accepted residual risk (see Amendment 5-G). Document this in the companion app's `README.md` under "Security Model." The Turso write token is NOT exposed — that is the proxy's guarantee.

### 11.7 Discord OAuth Callback URL Registration

When creating the Discord developer application, the OAuth redirect URI must be registered as:
```
{COMPANION_APP_URL}/auth/callback/discord
```
For local development: `http://localhost:5173/auth/callback/discord`  
For production: `https://{your-pages-subdomain}.pages.dev/auth/callback/discord`

Both URIs must be registered in the Discord developer application's OAuth2 settings before authentication will work. Auth.js generates the callback URL as `/auth/callback/{provider-id}` where `provider-id` is `discord` for the Discord provider.

### 11.8 Two Turso Tokens — Never Mix

Two separate Turso tokens are required and must never be confused:

| Token | Scope | Lives in | Used by |
|---|---|---|---|
| Sync write token | Write-only, single database | Cloudflare Worker `TURSO_WRITE_TOKEN` env var | CF Worker proxy only |
| App token | Read+write, single database | Cloudflare Pages `TURSO_APP_TOKEN` env var | SvelteKit server load functions only |

The write-only sync token cannot read data. The app token should never be placed in any client bundle or exposed to the browser in any form. Cloudflare Pages env vars are server-side only and are not included in static assets or client JS.

---

*Phase 5 blueprint complete.*
