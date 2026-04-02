# Sheet UAT R1 — Layer 1: Strategic Summary

**Project:** `sheet_uat_r1`
**Goal:** Address all 13 UAT Round 1 feedback items from players and GM on the Roll20 character sheet (HTML/CSS/Sheet Workers).
**Branch:** `fix/sheet-uat-r1`

---

## Resolved Before Planning (Out of Scope)

| # | Item | Resolution |
|---|---|---|
| G2 | Attribute rolls not incorporating condition modifiers | User confirmed fixed in latest Roll20 version |
| G3 | Remove 20 Qs from Bio section | User confirmed removed in latest Roll20 version |

> **NOTE (resolved):** User confirmed the repo files ARE the source of truth — changes were applied from repo to Roll20, not the reverse. No staleness concern.

---

## ADR-001: Mutation Essence → Magic Penalty Model

**Context:** Humanity (Essence) starts at 6 for all characters. Adding mutations decreases Humanity by the total essence cost of those mutations. Magic rating (`mag`) currently computes as `mag_base + mag_misc` and ignores mutations entirely.

The existing Layer 5e worker sums `mutation_essence` across all repeating mutation rows and writes to `essence_total`. However, there is a **semantic mismatch**: the HTML default for `essence_total` is `value="6"` (representing full starting Humanity), but the worker computes the *cost sum* (additive from 0). For a character with no mutations, the worker never fires — so `getAttrs` returns the HTML default of 6, which would incorrectly penalize Magic.

**Decision:** Introduce two clearly-named fields to eliminate ambiguity:

- `essence_spent` — sum of all `mutation_essence` values across repeating rows (starts at 0)
- `essence_total` — displayed Humanity = `6 - essence_spent` (starts at 6, HTML default stays correct)

Magic formula becomes:

```
mag = max(0, mag_base + mag_misc - essence_spent)
```

The existing Layer 5e worker is renamed to write `essence_spent` instead of `essence_total`. A new dependent worker computes `essence_total = 6 - essence_spent`. The `sheet:opened` handler must re-trigger the `essence_spent` calculation to guard against never-fired workers on legacy characters.

**Consequences:**
- Magic rating floors at 0 (can't go negative)
- Humanity (essence_total) also floors at 0 — reaching 0 Humanity has serious in-game consequences; negative values are meaningless and must not display
- Humanity display on the Mutations summary shows correct remaining value (6 minus costs)
- The Magic overview on the Magic tab reads `attr_mag` — no HTML change needed
- Adept Power Points max (`power_points_max = mag`) cascades automatically
- Dice pools that depend on `mag` (Astral Pool) recalculate automatically
- Sync payload must add `essence_spent` to scalar fields

---

## ADR-002: Skill Specialization Model

**Context:** Player feedback (P4) requests that checking the "Spec" checkbox on a skill should create a specialized sub-skill with `base + 1` while reducing the parent skill to `base - 1`.

**Decision:** Use Roll20's `generateRowID()` to programmatically create a child row when Spec is checked. Track the parent↔child relationship via a hidden `attr_skill_parent_id` field on the child row and `attr_skill_child_id` on the parent.

**Mechanic:**
- **On check:** Read parent's `skill_base`. Guard: if `skill_base < 1`, abort (can't specialize a skill at 0). Create child row: `skill_name = "{ParentName} (Spec)"`, `skill_base = parent_base + 1`, copy `skill_linked_attr` and `skill_general`. Set parent's `skill_base = parent_base - 1`. Store cross-references.
- **On uncheck:** Read child row via stored ID. Restore parent's `skill_base += 1`. Remove child row via `removeRepeatingRow()`.
- **Guard:** If `skill_base < 1` when spec is checked, block the action (can't specialize a skill with 0 base).

**Consequences:**
- Two new hidden fields per skill row (`skill_parent_id`, `skill_child_id`)
- Child rows are editable (name can be customized) but base adjustment is automated
- Sync payload already includes all existing skill fields. New cross-reference fields (`skill_parent_id`, `skill_child_id`) must be added to the SECTIONS map
- Must handle orphans in **both directions** on `sheet:opened`:
  - Child deleted manually → parent's `skill_child_id` points to non-existent row → clear it and restore parent's `skill_base += 1`
  - Parent deleted manually → child's `skill_parent_id` points to non-existent row → remove the orphaned child row

---

## ADR-003: Animal Companion / Critter Stat Block Model

**Context:** GM feedback (G4, G5) requests an Animal Companions section. 2 players currently have animal companions. These need their own stat block, condition monitor, and attack rolls that use the CREATURE's stats — not the player's TN modifiers.

**Decision:** Add a `repeating_companions` section with:
- Full stat row: B, Q, S, C, I, W, E, R (all number inputs)
- Reaction computed as `floor((I+Q)/2)` (same formula as player, but stored per-row)
- Simplified condition track: 3 severity levels (L/M/S) → TN penalty per creature
- Attack roll button that uses the creature's own stats and its own condition penalty
- Name field for identification

**Consequences:**
- New repeating section with ~15 fields per row
- Simplified condition select (3 severity levels: L/M/S) whose value IS the TN penalty — no per-row CM worker needed
- Attack roll macro references row-level attributes, not player-level — correctly isolated
- Sync payload (REGION 4) must add `companions` to the SECTIONS map
- Placed in Bio tab alongside existing Notes/Karma/Milestones sections

---

## Development Phases

### Phase 1: Critical Bug Fixes
**Goal:** Fix broken math and roll macros that directly impact gameplay accuracy.

| Item | What | Root Cause | Fix |
|---|---|---|---|
| P6 | Initiative score missing condition penalty | `init_score = reaction + init_reaction_mod + init_misc_mod` — missing `cm_init_mod` | Add `cm_init_mod` to formula and trigger list |
| P11 | Karma total adding instead of subtracting | `karma_total = karma_good + karma_used` | Change `+` to `-` |
| G1 | Resist Damage (Body) penalized by condition | Roll macro includes `@{cm_tn_mod}` | Remove `@{cm_tn_mod}` from body resist button |
| P2 | Power points stuck at 0 | User fills text `power_pp_cost`, but worker listens on hidden numeric `power_pp_cost_value` which never gets set | Add change handler for text field that parses with `parseFloat` and writes to numeric field (PP costs are frequently fractional: 0.25, 0.5, 1.5) |
| P7 | Magic ignores mutation essence cost | `mag = mag_base + mag_misc` | Subtract `essence_spent` per ADR-001; add `essence_spent` recalc to `sheet:opened` |

**Justification:** These affect combat, progression, and resource tracking — core gameplay loops. Every session is impacted.

**Dependencies:** None. All fixes are isolated formula corrections.

---

### Phase 2: UX Fixes
**Goal:** Fix visual issues and performance problems that degrade the player experience.

| Item | What | Root Cause | Fix |
|---|---|---|---|
| P3a | Adept power row self-deleting on rapid edits | Roll20 repeating section timing race — `setAttrs` on a row during creation event causes deletion | Defer `setAttrs` inside creation handler with `setTimeout(0)` or guard with existence check |
| P3b | Mutation BP column clips at 4 digits | CSS column width too narrow | Widen `.sheet-mutations .sheet-bp` column |
| P5 | Skill total calculation lag | Cascading attribute changes triggering redundant recalculations | Apply `{silent: true}` to intermediate `setAttrs` in cascade chain |
| P9 | Weapon category header misalignment | CSS alignment mismatch between header and row grid definitions | Fix grid-template-columns on weapon header to match row layout |
| P1a | Effect text boxes clipping content | CSS overflow hidden on effect text areas | Allow overflow/scrolling on `.sheet-effect` textareas |

**Justification:** These don't break math but directly frustrate users and eat session time. P3a (self-deletion) is especially disruptive during character creation.

**Dependencies:** None. All fixes are CSS or isolated JS timing adjustments.

---

### Phase 3: Data Entry Enhancements
**Goal:** Add missing fields and options that players need for accurate character representation.

| Item | What | Fix |
|---|---|---|
| P8 | Weapon type select needs full overhaul per Equipment reference | Replace current select with canonical weapon types from Equipment spreadsheet (see below) |
| P10 | Equipment has no quantity column | Add `equip_qty` number input to repeating_equipment row + CSS column + sync field. EP worker must multiply: `ep_total += equip_ep × equip_qty` per row. (Backpack/bandolier EP reduction deferred to companion app.) |
| P1b | Effect text only visible on hover/scroll | Add "Send to chat" roll button on spell/mutation/power effect fields |

**Canonical Weapon Types (from Equipment spreadsheet):**

```
Edged — Throwing    Blunt — Throwing     Whip        Bow
Edged — Light       Blunt — Light        Flail       Crossbow — Hand
Edged — Single      Blunt — Single       Staff       Crossbow — Medium
Edged — Great       Blunt — Great        Unarmed     Crossbow — Heavy
Polearm
```

> Mounted and Siege categories exist in the reference but are not player-relevant — omitted from select.

**Justification:** Small HTML/CSS additions that address "I can't represent my character accurately." Low risk, high impact.

**Dependencies:** P1a (Phase 2) should be done first so effect text is visible before we add the chat button.

---

### Phase 4: Skill Specialization
**Goal:** Implement the spec checkbox → sub-skill creation flow (ADR-002).

| Item | What | Fix |
|---|---|---|
| P4 | Spec checkbox creates specialized sub-skill, adjusts base points | New Sheet Worker: `on("change:repeating_skills:skill_spec")` + `generateRowID()` + cross-reference tracking + orphan cleanup |

**Justification:** Isolated as its own phase because it's the most complex Sheet Worker logic (cross-row manipulation, lifecycle management). Needs careful testing. Players need this when porting from their Excel sheets.

**Dependencies:** Phase 2/P5 (skill cascade optimization) should be done first so specialization triggers don't compound the lag issue.

---

### Phase 5: Creature Systems
**Goal:** Add Animal Companions (ADR-003) and Spirit favor rolls.

| Item | What | Fix |
|---|---|---|
| G4 | Animal Companions section | New `repeating_companions` with stat block, condition track, placement in Bio tab |
| G5 | Creature attack rolls with own condition tracking | Attack roll button per companion row using row-level stats and condition penalty |
| P12 | Spirit summon + attack rolls | Two new roll buttons in Spirit Calculator: (1) **Summon** — rolls Conjuring vs TN, net successes = number of services/favors owed; (2) **Attack** — rolls using the spirit's computed stats and its own condition (not player's). Summon button needs Conjuring skill dice + TN prompt; Attack button reads spirit stat block already computed by the calculator. |

**Justification:** Largest scope — new repeating section with per-row condition tracking and isolated roll macros. Grouped because G4 and G5 share the creature stat block pattern, and P12 touches the same Spirit Calculator section (summon roll for services, attack roll using computed spirit stats).

**Dependencies:** Phase 1 (bug fixes) should be done first to ensure the cascade chain is stable before adding new sections.

---

## Risk Register

| ID | Risk | Mitigation | Blocking? |
|---|---|---|---|
| R1 | `removeRepeatingRow()` behavior varies across Roll20 versions | Test on live Roll20 sandbox during Phase 4 implementation | No |
| R2 | Per-row condition tracking for companions adds significant HTML bulk | Keep companion CM to 3 severity levels (not full 32-box tracks) | No |
| R3 | Cascade chains between `essence_total` → `mag` → `power_points_max` → `remaining` may cause perceptible lag | Use `{silent: true}` on intermediate `setAttrs` (addressed in Phase 2/P5) | No |
| ~~R4~~ | ~~Repo sheet files may be out of sync~~ | **Resolved** — user confirmed repo is source of truth; Roll20 was updated FROM repo. | **No** |

---

## Execution Summary

| Phase | Items | Type | Complexity |
|---|---|---|---|
| 1 | P6, P11, G1, P2, P7 | Bug fixes | Low |
| 2 | P3a, P3b, P5, P9, P1a | UX fixes | Low-Medium |
| 3 | P8, P10, P1b | Data entry | Low |
| 4 | P4 | Specialization | Medium-High |
| 5 | G4, G5, P12 | Creature systems | High |

**Total:** 5 phases, 13 items (15 sub-tasks), 3 ADRs, 4 risks (1 resolved).