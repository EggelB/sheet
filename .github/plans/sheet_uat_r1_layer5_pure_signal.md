# Sheet UAT R1 — Layer 5: Pure Signal Brief

**Project:** `sheet_uat_r1` | **Branch:** `fix/sheet-uat-r1`
**Files:** `roll20/sheet.html` (~1348 lines), `roll20/sheet.css` (~1833 lines)
**Scope:** 13 UAT items → 5 phases → 65 tasks → 0 DRY consolidations
**Layer 4 result:** All blueprints already DRY. Zero changes.

---

## Governing Decisions

| ADR | Rule | Implementation |
|---|---|---|
| ADR-001 | Magic penalized by mutation essence cost | `essence_spent` (sum) + `essence_total` (6 − spent). `mag = max(0, base + misc − spent)`. |
| ADR-002 | Spec checkbox creates child skill row | `generateRowID()`, hidden `skill_parent_id`/`skill_child_id`, 3 guards, orphan cleanup in `sheet:opened`. |
| ADR-003 | Creature rolls use creature stats, not player's | `@{comp_cm_level}` (row-level) in companion TN. Spirit attack omits `@{cm_tn_mod}`. Spirit summon includes it (player skill). |

---

## Phase 1: Critical Bug Fixes

> **Why:** Broken math in combat, progression, and resource tracking. Every session impacted.

All edits in `roll20/sheet.html`. No CSS.

### 1.1 — P11: Karma Total Sign Fix
**~Line 245.** Change `+` to `-` in `setAttrs({ karma_total: good + used })` → `good - used`.

### 1.2 — G1: Resist Body — Remove Wound Penalty
**~Line 1190.** Delete both `+@{cm_tn_mod}` from the `roll_btn_damage_resist_body` value string. Two deletions in one line.

### 1.3 — P6: Initiative — Add CM Init Mod
**~Lines 134–141.** Add `change:cm_init_mod` to trigger, `'cm_init_mod'` to getAttrs, `var cm_init_mod = parseInt(...)`, add to formula.

### 1.4 — P2: PP Text→Numeric Sync Worker (NEW)
**Insert after ~line 225** (after Layer 5d PP remaining worker). New Layer 5d2:
```js
on('change:repeating_adept_powers:power_pp_cost', function() {
  getAttrs(['power_pp_cost'], function(v) {
    setAttrs({ power_pp_cost_value: parseFloat(v.power_pp_cost) || 0 });
  });
});
```

### 1.5 — P2: PP Cost Recalc in `sheet:opened` (NEW)
**Insert inside `sheet:opened`**, after skill recalc block (~line 332). `getSectionIDs('repeating_adept_powers', ...)` → batch read `power_pp_cost` → batch write `power_pp_cost_value` via `parseFloat`.

### 1.6 — P7/ADR-001: Hidden `essence_spent` Field
**~Line 915.** Add `<input type="hidden" name="attr_essence_spent" value="0">` inside `.sheet-mutations-summary`, after `essence_total` input.

### 1.7 — P7/ADR-001: Rename Layer 5e Output
**~Line 235.** Change `setAttrs({ essence_total: total })` → `setAttrs({ essence_spent: total })`.

### 1.8 — P7/ADR-001: New `essence_total` Worker (NEW)
**Insert after ~line 237:**
```js
on('change:essence_spent', function() {
  getAttrs(['essence_spent'], function(v) {
    setAttrs({ essence_total: Math.max(0, 6 - (parseFloat(v.essence_spent) || 0)) });
  });
});
```

### 1.9 — P7/ADR-001: Rewrite Mag Worker
**~Lines 53–58.** Replace comment + handler. New formula: `mag = max(0, base + misc - essence_spent)`. Add `change:essence_spent` to trigger, `parseFloat` for spent.

### 1.10 — P7/ADR-001: Essence Recalc in `sheet:opened` (NEW)
**Insert inside `sheet:opened`**, after PP block (1.5). `getSectionIDs('repeating_mutations', ...)` → sum `mutation_essence` → write `essence_spent`. Triggers both `essence_total` and `mag` workers on legacy load.

### 1.11 — P7/ADR-001: Add `essence_spent` to scalarFields
**~Line 477.** Append `'essence_spent',` after `'essence_total',`.

**Phase 1 total: 11 edits, 1 file.**

---

## Phase 2: UX Fixes

> **Why:** Visual bugs and performance issues eat session time. P3a (self-deletion) is especially disruptive.

Edits across `sheet.html` + `sheet.css`.

### 2.1 — P3b: Mutation BP Column Width
**sheet.css ~lines 769, 776.** Header + row: `40px` → `55px` (both flex and width).

### 2.2 — P1a: Effect Ellipsis Overflow
**sheet.css ~lines 777, 824.** Add `text-overflow: ellipsis; overflow: hidden; white-space: nowrap;` to `.sheet-mutation-effect` and `.sheet-power-effect`.

### 2.3 — P1a: Effect Title Attributes
**sheet.html ~lines 931, 960.** Add `title="View full effect text"` to mutation and power effect inputs.

### 2.4 — P9: Weapon Button Alignment
**sheet.html ~lines 1244–1245.** Wrap both attack buttons in `<div class="sheet-weapon-roll-group">`.
**sheet.css after ~line 1687.** New `.sheet-weapon-roll-group { display: flex; gap: 2px; flex: 0 0 70px; }`.
**sheet.css ~line 1684.** Button flex: `0 0 auto` → `1 1 auto`.

### 2.5 — P3a: setTimeout(0) Deferral
**sheet.html ~lines 206–216.** Wrap PP used summation handler body in `setTimeout(function() { ... }, 0);`.
**sheet.html (Phase 1 output).** Wrap PP sync handler (1.4) body in `setTimeout(function() { ... }, 0);`.

### 2.6 — P5: Pool Base+Total Merge with `{silent: true}`
**sheet.html ~lines 81–112.** Rewrite all 4 Layer 4a handlers to read `pool_X_misc`, compute both `pool_X_base` and `pool_X` in single `setAttrs({...}, {silent: true})`. Retain `calcPoolTotal` for direct misc edits.

### 2.7 — P5: Skill Recalc Silent
**sheet.html ~line 330.** Change `setAttrs(out)` → `setAttrs(out, {silent: true})` in `sheet:opened` skill block.

**Phase 2 total: 16 edits, 2 files.**

---

## Phase 3: Data Entry Enhancements

> **Why:** "I can't represent my character accurately." Small additions, high player impact.

### 3.1 — P8: Weapon Type Select Overhaul
**sheet.html ~lines 1223–1231.** Replace 7-option flat select with 17-option grouped select:
- Edged (Throwing/Light/Single/Great)
- Blunt (Throwing/Light/Single/Great)
- Other Melee (Polearm/Whip/Flail/Staff/Unarmed)
- Ranged (Bow/Crossbow Hand/Medium/Heavy)

Values: lowercase hyphenated (`edged-light`, `crossbow-heavy`). Breaks old values — intentional for 5 players.

### 3.2 — P8: Weapon Type Column Width
**sheet.css ~lines 1646, 1658.** Header + row: `80px` → `110px`.

### 3.3 — P10: Equipment Qty Header + Input
**sheet.html ~line 1253.** Insert `<span class="sheet-hdr-equip-qty">Qty</span>` after Name.
**sheet.html ~line 1259.** Insert `<input type="number" class="sheet-equip-qty" name="attr_equip_qty" value="1" min="1">` after name input.

### 3.4 — P10: Equipment Qty CSS
**sheet.css after ~lines 1155, 1159.** Header: `.sheet-hdr-equip-qty { flex: 0 0 40px; text-align: center; }`. Row: `.sheet-equip-qty { flex: 0 0 40px; width: 40px; text-align: center; }`.

### 3.5 — P10: EP Total Worker Update
**sheet.html ~lines 154–168.** Add `change:repeating_equipment:equip_qty` to trigger. Push both `equip_ep` and `equip_qty` per equipment ID. Summation: `ep * qty` with `(qty || 0) || 1` guard for legacy rows.

### 3.6 — P10: Add `equip_qty` to SECTIONS
**sheet.html ~line 441.** Insert `'equip_qty',` after `'equip_name',`.

### 3.7 — P1b: Chat Effect Buttons
**sheet.html ~lines 931, 960.** Insert `<button type="roll" class="sheet-btn-chat-effect" value="&{template:desc} ...">💬</button>` before `</fieldset>` in mutation and power fieldsets.

### 3.8 — P1b: Chat Header Spacers
**sheet.html ~lines 918, 948.** Insert `<span class="sheet-hdr-chat">💬</span>` before spacer in mutation and power headers.

### 3.9 — P1b: Chat Button + Header CSS
**sheet.css after ~line 824.** `.sheet-btn-chat-effect { flex: 0 0 24px; width: 24px; height: 24px; ... }` + `.sheet-hdr-chat { flex: 0 0 24px; text-align: center; }`.

### 3.10 — P1b: New `desc` Roll Template
**sheet.html after ~line 1448.** New `<rolltemplate class="sheet-rolltemplate-desc">` with header (`{{charname}} — {{rollname}}`) + body (`{{desc}}` with `pre-wrap`).

### 3.11 — P1b: Desc Template CSS
**sheet.css.** New `.sheet-rolltemplate-desc` wrapper + header (`#2a3a2a` dark olive). Extend 4 shared selector groups (body/row/label/value) from 3→4 templates. Add `.sheet-template-desc { padding: 4px 8px; white-space: pre-wrap; }`.

**Phase 3 total: 16 tasks, 2 files. 1 new roll template.**

---

## Phase 4: Skill Specialization

> **Why:** Most complex Sheet Worker logic — cross-row manipulation with lifecycle management. Isolated for careful testing.

All edits in `sheet.html`. No CSS.

### 4.1 — P4/ADR-002: Hidden Cross-Ref Inputs
**~Line 898.** Insert `<input type="hidden" name="attr_skill_parent_id" value="">` and `<input type="hidden" name="attr_skill_child_id" value="">` after spec checkbox.

### 4.2 — P4/ADR-002: SECTIONS Map Update
**~Lines 429–430.** Append `'skill_parent_id', 'skill_child_id'` to skills array.

### 4.3 — P4/ADR-002: New Spec Handler (Layer 5c2) — ~55 lines
**Insert after ~line 196** (after Layer 5c skill total worker).

**On check (spec=1):**
1. Extract parentId from `eventInfo.sourceAttribute` via regex
2. **Guard 1:** `skill_parent_id` non-empty → revert `{silent: true}` (prevent grandchild)
3. **Guard 2:** `skill_child_id` non-empty → revert (prevent duplicate)
4. **Guard 3:** `skill_base < 1` → revert (can't specialize at 0)
5. `generateRowID()` → create child: name + " (Spec)", base+1, copy linked_attr + general
6. Parent: base−1, store child_id

**On uncheck (spec=0):**
1. Read `skill_child_id` → if empty, return
2. `setAttrs` parent base+1, clear child_id → callback → `removeRepeatingRow(child)`

Key: `_.object([[key, val]])` for guard reverts. `removeRepeatingRow` in `setAttrs` callback for safety ordering.

### 4.4 — P4/ADR-002: Rewrite `sheet:opened` Skill Block — ~35 lines
**~Lines 315–332.** Replace existing skill recalc with 3-pass orphan cleanup:

1. **Pass 1 — Detect:** Build `validIds` set. For each row: if `child_id` points to deleted row → clear ref + uncheck spec + restore base+1. If `parent_id` points to deleted row → mark for removal.
2. **Pass 2 — Remove:** `removeRepeatingRow` all orphaned children.
3. **Pass 3 — Recalc:** Compute `skill_total` for remaining rows. Use orphan-fixed `base` from Pass 1 when available. Skip removed rows.

Final `setAttrs(out, {silent: true})`.

**Phase 4 total: 4 logical edits, 1 file. ~90 new lines JS.**

---

## Phase 5: Creature Systems

> **Why:** Largest scope — new repeating section with per-row condition tracking and isolated roll macros. G4/G5/P12 share creature stat pattern.

Edits across `sheet.html` + `sheet.css`.

### 5.1 — G4/ADR-003: Companion Section HTML
**sheet.html after ~line 1319** (after milestones `</fieldset>`, before bio-section `</div>`).

Insert: `<h3>` title + flex header (Name, B–R, Rcn, CM, Atk, spacer) + `<fieldset class="repeating_companions">` with:
- `comp_name` text input
- 8 stat number inputs (`comp_b` through `comp_r`, all `class="sheet-comp-stat"`)
- `comp_reaction` readonly number input
- `comp_cm_level` select: None(0)/Light(1)/Moderate(2)/Serious(3)
- Attack button (embedded — see 5.4)

### 5.2 — G4: SECTIONS Map Entry
**sheet.html ~lines 444–446.** Add trailing comma to milestones, insert:
```js
companions: ['comp_name','comp_b','comp_q','comp_s','comp_c','comp_i','comp_w','comp_e','comp_r','comp_reaction','comp_cm_level']
```

### 5.3 — G4: Companion CSS
**sheet.css after ~line 1833** (after milestones CSS, before SECTION 20).

- `.sheet-companions-header`: flex, `#f2f2f2` bg, `2px solid #5f5f5f` border, `margin-top: 12px`
- Header columns: name auto, stats 38px, CM 90px, atk 36px
- Row columns: mirror header widths. Reaction: bold, grey bg, solid border
- `.sheet-comp-cm-level { flex: 0 0 90px; }`, `.sheet-comp-attack { flex: 0 0 36px; cursor: pointer; }`

### 5.4 — G5/ADR-003: Companion Attack Button
**Inside `repeating_companions` fieldset (5.1).** Uses `attack` template.

Critical isolation: `TN = ?{Target Number|4} + @{comp_cm_level}` — **row-level** creature penalty, NOT `@{cm_tn_mod}`. Dice default `@{comp_reaction}`. Power = `@{comp_s}`. Label: 🐾 (`&#x1F43E;`).

### 5.5 — G4: Companion Reaction Worker (Layer 5g)
**sheet.html after ~line 421** (after REGION 3b, before REGION 4).
```js
on('change:repeating_companions:comp_i change:repeating_companions:comp_q', function() {
  getAttrs(['comp_i', 'comp_q'], function(v) {
    setAttrs({ comp_reaction: Math.floor(((parseInt(v.comp_i,10)||0) + (parseInt(v.comp_q,10)||0)) / 2) });
  });
});
```
Short-form auto-scoped attrs. Formula: `floor((I+Q)/2)`.

### 5.6 — G4: Companion Recalc in `sheet:opened`
**Insert after Phase 4's rewritten skill block**, still inside `sheet:opened`.
`getSectionIDs('repeating_companions', ...)` → early return if empty → batch read `comp_i`+`comp_q` → batch write `comp_reaction`.

### 5.7 — P12: Spirit Roll Buttons
**sheet.html ~lines 1113–1116** (inside `.sheet-spirit-combat`, after Attack display field).

**Summon button:** `skill` template. TN = `@{spirit_force} + @{cm_tn_mod}` (player skill → player wounds). Conjuring dice prompted (repeating skill, can't reference as scalar). 🔮 (`&#x1F52E;`) label.

**Attack button:** `attack` template. TN = `?{Target Number|4}` — **NO** `@{cm_tn_mod}` (spirit independence). Dice default `@{spirit_b}`. Power = `@{spirit_s}`. Damage = `@{spirit_attack}`. ⚔ (`&#x2694;`) label.

### 5.8 — P12: Spirit Button CSS
**sheet.css after ~line 1128** (after `.sheet-spirit-textarea`, before SECTION 9d).
```css
.sheet-spirit-roll-btn { padding: 4px 10px; font-size: 13px; cursor: pointer; margin-top: 4px; }
```

**Phase 5 total: 8 edits, 2 files. ~30 lines HTML, ~30 lines CSS, ~15 lines JS.**

---

## `sheet:opened` Final Structure (Post-All-Phases)

```
on('sheet:opened', function() {
  getAttrs([8 cascade roots], function(v) { setAttrs({...}); });   // existing
  calcCMPenalty();                                                   // existing

  getSectionIDs('repeating_skills', function(ids) {                 // Phase 4 rewrite
    // 3-pass orphan cleanup + skill_total recalc
    setAttrs(out, {silent: true});                                   // Phase 2 silent
  });

  getSectionIDs('repeating_adept_powers', function(ids) { ... });   // Phase 1 P2
  getSectionIDs('repeating_mutations', function(ids) { ... });      // Phase 1 P7
  getSectionIDs('repeating_companions', function(ids) { ... });     // Phase 5 G4
});
```

---

## SECTIONS Map Final State (Post-All-Phases)

```js
var SECTIONS = {
  skills:       [..., 'skill_parent_id', 'skill_child_id'],         // Phase 4
  weapons:      [...],                                                // unchanged
  equipment:    ['equip_name', 'equip_qty', ...],                    // Phase 3
  spells:       [...],                                                // unchanged
  mutations:    [...],                                                // unchanged
  adept_powers: [...],                                                // unchanged
  karma:        [...],                                                // unchanged
  milestones:   [...],                                                // unchanged (+ trailing comma)
  companions:   ['comp_name', 'comp_b', ..., 'comp_cm_level']       // Phase 5 NEW
};
```

---

## Cross-Phase Dependency Chain

```
Phase 1 ─── P2 task 4.1 creates PP sync worker
  └──→ Phase 2 ─── P3a task 2.2 wraps it in setTimeout(0)
Phase 2 ─── P5 task 4.5 adds {silent: true} to skill recalc
  └──→ Phase 4 ─── rewrites entire skill block (retains silent)
Phase 4 ─── rewrites sheet:opened skill block
  └──→ Phase 5 ─── companion recalc inserts AFTER rewritten block
Phase 2 ─── P1a adds title attrs to effect inputs
  └──→ Phase 3 ─── P1b adds chat buttons after titled inputs
```

**Execution order is strict: 1 → 2 → 3 → 4 → 5.** No parallel execution.

---

## Cascade Layer Map (Post-All-Phases)

```
Layer 2:  body_base → body, ... , mag_base + mag_misc - essence_spent → mag   [P7 rewrite]
Layer 3:  int + dex → reaction_base → reaction
Layer 4a: cha+int+wil → pool_spell_base + pool_spell  {silent:true}          [P5 merge]
          dex+int+wil → pool_combat_base + pool_combat {silent:true}
          reaction → pool_control_base + pool_control  {silent:true}
          int+wil+mag → pool_astral_base + pool_astral {silent:true}
Layer 4b: pool_X_misc → pool_X (via calcPoolTotal, for direct edits only)
Layer 4c: reaction + init_mods + cm_init_mod → init_score                    [P6 fix]
Layer 5a: weapon_ep + (equip_ep × equip_qty) → ep_total                     [P10 update]
Layer 5c: skill_base + foci + misc → skill_total
Layer 5c2: skill_spec → parent base±1, child create/remove                   [P4 NEW]
Layer 5d: pp_cost_value → pp_used → pp_remaining  (setTimeout wrapped)      [P3a fix]
Layer 5d2: pp_cost(text) → pp_cost_value  (setTimeout wrapped)              [P2 NEW]
Layer 5e: mutation_essence → essence_spent                                    [P7 rename]
          essence_spent → essence_total (6 - spent)                          [P7 NEW]
Layer 5g: comp_i + comp_q → comp_reaction                                    [G4 NEW]
Layer 6a: karma_good - karma_used → karma_total                             [P11 fix]
```

---

## Risk Mitigations Active

| Risk | Mitigation | Status |
|---|---|---|
| `removeRepeatingRow` variance | Test on live Roll20 sandbox in Phase 4 | Open |
| Companion HTML bulk | 3-level CM select, not 32-box track | Resolved in ADR-003 |
| Cascade lag | `{silent: true}` on pool, skill, essence chains | Resolved in Phase 2 |
| Repo sync | Confirmed repo = source of truth | Resolved |

---

## Verification Checklist (Per Phase)

Each phase must satisfy before proceeding:

- [ ] All code blocks from blueprint applied verbatim
- [ ] Line numbers verified against actual source (drift expected; match by context)
- [ ] HTML tags balanced (every `<div>` closed, every `<fieldset>` closed)
- [ ] JS parens balanced (every `function(` has `)`, every `{` has `}`)
- [ ] Roll20 macro syntax: `&{template:X} {{key=value}}` — no stray `}` or `{`
- [ ] `@{attr}` references: repeating row attrs auto-scoped inside fieldsets; player attrs use scalar names
- [ ] No `@{cm_tn_mod}` in creature roll buttons (ADR-003 isolation)
- [ ] `setAttrs` calls: `{silent: true}` where specified, omitted where cascade propagation needed
- [ ] SECTIONS map entries match fieldset attribute names exactly
- [ ] CSS `flex` values: header and row widths match for column alignment

---

**End of Pure Signal Brief. Ready for Developer handoff.**
