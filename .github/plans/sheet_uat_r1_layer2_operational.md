# Sheet UAT R1 — Layer 2: Operational Granularity

**Project:** `sheet_uat_r1`
**Branch:** `fix/sheet-uat-r1`
**Source:** Layer 1 strategic plan (approved 2026-04-01)

---

## Phase 1: Critical Bug Fixes

**5 items, 11 tasks. All changes in `roll20/sheet.html` only.**

---

### P6: Initiative Score Missing Condition Penalty

**Root:** Layer 4c (line ~134) — `init_score = reaction + init_reaction_mod + init_misc_mod`, missing `cm_init_mod`.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 1.1 | Add `cm_init_mod` to trigger list | Line 134 | `on('change:reaction change:init_reaction_mod change:init_misc_mod change:cm_init_mod', …)` |
| 1.2 | Add `cm_init_mod` to `getAttrs` array | Line 135 | Add `'cm_init_mod'` to the array |
| 1.3 | Add `cm_init_mod` to formula | Line 139 | `init_score: reaction + init_react_mod + init_misc_mod + cm_init_mod` (note: `cm_init_mod` is already stored as a negative value, so we add it) |

---

### P11: Karma Total Adding Instead of Subtracting

**Root:** Layer 6a (line ~245) — `karma_total = karma_good + karma_used`

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 2.1 | Change `+` to `-` | Line ~245 | `karma_total: (parseInt(v.karma_good, 10) \|\| 0) - (parseInt(v.karma_used, 10) \|\| 0)` |

---

### G1: Resist Damage (Body) Should Be Immune to Wound Penalties

**Root:** Combat buttons (line ~1191) — roll macro includes `+@{cm_tn_mod}` in both TN and successes formulas.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 3.1 | Remove `+@{cm_tn_mod}` from TN | Line 1191 | `{{tn=[[?{TN (Power - Armor)\|0}]]}}` — drop the `+@{cm_tn_mod}` |
| 3.2 | Remove `+@{cm_tn_mod}` from successes threshold | Line 1191 | `>[[?{TN (Power - Armor)\|0}]]` — drop the `+@{cm_tn_mod}` |

---

### P2: Power Points Not Updating

**Root:** User fills text field `power_pp_cost` but the worker only listens on hidden numeric `power_pp_cost_value` which never gets written. Layer 5d (line ~207) sums `power_pp_cost_value`.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 4.1 | Add text→numeric sync worker | After Layer 5d PP used worker (~line 216) | New `on('change:repeating_adept_powers:power_pp_cost', …)` handler that reads the text field, parses with `parseFloat`, and writes to `power_pp_cost_value`. This triggers the existing PP used summation worker. |
| 4.2 | Add `power_pp_cost` recalc to `sheet:opened` | Inside sheet:opened handler, after skill totals recalc block (before closing `});` at ~line 332) | Loop `repeating_adept_powers`, read each `power_pp_cost`, parse and write to `power_pp_cost_value` — ensures legacy characters get their PP totals fixed on first load. |

---

### P7: Magic Ignores Mutation Essence Cost (ADR-001)

**Root:** mag worker (line ~56) — `mag = mag_base + mag_misc`, no essence dependency. Layer 5e writes to `essence_total` but with semantic mismatch (HTML default=6 represents full Humanity, but worker computes cost sum additive from 0).

**ADR-001 decisions applied:**
- `essence_spent` — sum of all `mutation_essence` values across repeating rows (starts at 0)
- `essence_total` — displayed Humanity = `6 - essence_spent` (starts at 6, HTML default stays correct)
- `mag = max(0, mag_base + mag_misc - essence_spent)`

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 5.1 | Add hidden `essence_spent` field to HTML | After `attr_essence_total` in mutations summary (~line 915) | `<input type="hidden" name="attr_essence_spent" value="0">` |
| 5.2 | Rename Layer 5e worker output | Lines 232-240 | Change `setAttrs({ essence_total: total })` → `setAttrs({ essence_spent: total })` |
| 5.3 | Add `essence_total` dependent worker | After renamed Layer 5e | New `on('change:essence_spent', …)` → `setAttrs({ essence_total: Math.max(0, 6 - essence_spent) })` |
| 5.4 | Rewrite mag worker | Lines 56-59 | `on('change:mag_base change:mag_misc change:essence_spent', …)` → reads `mag_base`, `mag_misc`, `essence_spent` → `setAttrs({ mag: Math.max(0, base + misc - spent) })` |
| 5.5 | Add `essence_spent` to `sheet:opened` | Inside sheet:opened handler | Re-trigger `essence_spent` recalc by iterating mutation rows (same pattern as existing skill totals recalc). Ensures legacy characters and no-mutation characters get correct values on load. |
| 5.6 | Add `essence_spent` to sync scalar fields | ~line 486 | Add `'essence_spent'` to the `scalarFields` array (after `'essence_total'`) |

---

## Execution Order (within Phase 1)

1. **P11** (task 2.1) — one-character change, zero dependencies
2. **G1** (tasks 3.1–3.2) — HTML-only macro edit, zero dependencies
3. **P6** (tasks 1.1–1.3) — isolated worker edit, zero dependencies
4. **P2** (tasks 4.1–4.2) — new worker + sheet:opened addition
5. **P7** (tasks 5.1–5.6) — most complex, touches worker + HTML + sync + sheet:opened; done last so all other sheet:opened additions are in place

---

## Verification Checklist

- [ ] Paste updated sheet.html into Roll20 sandbox
- [ ] Create test character with known values
- [ ] P6: Change condition checkboxes → confirm initiative score changes accordingly
- [ ] P11: Set karma_good=20, karma_used=5 → confirm karma_total=15
- [ ] G1: Take wounds → confirm Resist Damage (Body) TN is NOT affected
- [ ] P2: Type "0.5" in PP Cost text field → confirm PP Used updates to 0.5
- [ ] P7: Add mutation with essence=2 → confirm Humanity drops to 4, Magic drops by 2
- [ ] P7: Character with zero mutations → confirm Humanity=6, Magic=mag_base+mag_misc (no penalty)
- [ ] P7: Add mutations totaling 7 essence → confirm Magic floors at 0 (not negative)
- [ ] P7: Add mutations totaling 7 essence → confirm Humanity floors at 0 (not negative)
- [ ] P7 cascade: After adding mutation → confirm pool_astral recalculates (mag → pool_astral_base → pool_astral)
- [ ] P7 cascade: After adding mutation → confirm power_points_remaining drops (mag → power_points_max → power_points_remaining)
- [ ] P2 cascade: Open legacy character with existing PP cost text values → confirm PP Used populates on sheet load
- [ ] P6 cascade: Open character with existing wounds → confirm init_score includes penalty immediately on sheet open

---

## Cascade Impact Analysis

```
P6:  cm_init_mod ──→ init_score                    (1 downstream)
P11: karma_good/karma_used ──→ karma_total          (1 downstream, display only)
G1:  (no cascade — roll macro only)
P2:  power_pp_cost ──→ power_pp_cost_value ──→ power_points_used ──→ power_points_remaining  (3 downstream)
P7:  mutation_essence(s) ──→ essence_spent ──→ essence_total (display)
                                            ──→ mag ──→ power_points_max ──→ power_points_remaining
                                                    ──→ pool_astral_base ──→ pool_astral
```

P7 has the deepest cascade chain (5 levels). All intermediate `setAttrs` calls in the existing cascade already trigger their dependents correctly. No `{silent: true}` needed in Phase 1 — that optimization is Phase 2/P5.

---
---

## Phase 2: UX Fixes

**5 items, 16 tasks. Changes across `roll20/sheet.html` and `roll20/sheet.css`.**

---

### P1a: Effect Text Boxes Clipping Content

**Root:** Mutation and adept power "Effect" fields are `<input type="text">` — single-line, cannot display long descriptions. CSS gives them `flex: 2 1 120px; min-width: 0` but no overflow handling. Long effect text simply clips.

**Affected selectors:**
- `.sheet-tab-panel-skills .repitem .sheet-mutation-effect` (CSS line 777) — `flex: 2 1 120px; min-width: 0`
- `.sheet-tab-panel-skills .repitem .sheet-power-effect` (CSS line 824) — `flex: 2 1 120px; min-width: 0`

**Fix direction:** Add `text-overflow: ellipsis; overflow: hidden; white-space: nowrap` to allow graceful truncation with hover-visible full text via `title` attribute on the HTML input.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 1.1 | Add ellipsis overflow to mutation effect | `sheet.css` | Line 777 | Add `text-overflow: ellipsis; overflow: hidden; white-space: nowrap;` to `.sheet-tab-panel-skills .repitem .sheet-mutation-effect` |
| 1.2 | Add ellipsis overflow to power effect | `sheet.css` | Line 824 | Add `text-overflow: ellipsis; overflow: hidden; white-space: nowrap;` to `.sheet-tab-panel-skills .repitem .sheet-power-effect` |
| 1.3 | Add `title` attribute to mutation effect input | `sheet.html` | Line 931 | Change `<input type="text" name="attr_mutation_effect" …>` to include `title="View full effect text"` — Roll20 does not support dynamic title binding, so this serves as a static usability hint |
| 1.4 | Add `title` attribute to power effect input | `sheet.html` | Line 960 | Same pattern as 1.3: add `title="View full effect text"` to the `<input type="text" name="attr_power_effect" …>` element |

**Note:** Roll20 inputs do not support dynamic `title` from attribute values. The ellipsis treatment is the practical maximum for `<input type="text">` in the Roll20 iframe. Converting to `<textarea>` would require per-row height management and complicates the flex row layout — not worth the complexity for a description field.

---

### P3a: Adept Power Row Self-Deleting on Rapid Edits

**Root:** When a user rapidly fills fields on a newly-created `repeating_adept_powers` row, the `change:repeating_adept_powers:power_pp_cost_value` handler (line 206) fires via Roll20's internal event queue. If the row is still being initialized by Roll20's DOM injection, `getSectionIDs` + `setAttrs` can collide with the creation process, causing Roll20 to interpret the row as invalid and delete it.

**Affected handler:** Layer 5d PP used summation worker (`sheet.html` line 206):
```js
on('change:repeating_adept_powers:power_pp_cost_value remove:repeating_adept_powers', function() {
  getSectionIDs('repeating_adept_powers', function(ids) { … });
});
```

**Fix direction:** Wrap the handler body in `setTimeout(function(){ … }, 0)` to defer execution out of the Roll20 creation event stack. This is a well-documented Roll20 community pattern for repeating section race conditions.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 2.1 | Defer PP used summation handler | `sheet.html` | Line 206 | Wrap entire `getSectionIDs(…)` call inside `setTimeout(function() { … }, 0)` |
| 2.2 | Defer text→numeric sync handler (P2 addition) | `sheet.html` | After line ~216 (Phase 1 P2 task 4.1 location) | The new `change:repeating_adept_powers:power_pp_cost` handler added in Phase 1 must also wrap its body in `setTimeout(0)`. Apply the same pattern as 2.1 |

**Note:** Both handlers that fire on `repeating_adept_powers` changes need the deferral. The `remove:` event does not suffer from this race (row already exists when removal fires), but `setTimeout(0)` is harmless on removal and simplifies the code vs. checking the event type.

---

### P3b: Mutation BP Column Clips at 4 Digits

**Root:** CSS gives the BP column `flex: 0 0 40px` which fits ~3 characters at 13px font. Mutation BP costs can reach 4+ digits (e.g., 1000+), clipping the display.

**Affected selectors:**
- `.sheet-hdr-mutation-bp` (CSS line 769) — `flex: 0 0 40px; text-align: center`
- `.sheet-tab-panel-skills .repitem .sheet-mutation-bp` (CSS line 776) — `flex: 0 0 40px; width: 40px; text-align: center`

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 3.1 | Widen header BP column | `sheet.css` | Line 769 | Change `.sheet-hdr-mutation-bp { flex: 0 0 40px; … }` → `flex: 0 0 55px` |
| 3.2 | Widen row BP column | `sheet.css` | Line 776 | Change `.sheet-mutation-bp { flex: 0 0 40px; width: 40px; … }` → `flex: 0 0 55px; width: 55px` |

---

### P5: Skill Total Calculation Lag (Cascade Optimization)

**Root:** When any attribute base changes (e.g., `int_base`), the cascade fires:

```
int_base → int (Layer 2: calcAttr4)
  int → reaction_base (Layer 3)
    reaction_base → reaction (Layer 3)
      reaction → pool_control_base (Layer 4a)
        pool_control_base → pool_control (Layer 4b: calcPoolTotal)
      reaction → init_score (Layer 4c)
  int → pool_spell_base (Layer 4a)
    pool_spell_base → pool_spell (Layer 4b)
  int → pool_combat_base (Layer 4a)
    pool_combat_base → pool_combat (Layer 4b)
  int → pool_astral_base (Layer 4a)
    pool_astral_base → pool_astral (Layer 4b)
```

That's **11 separate `setAttrs` calls** for a single `int_base` change. With 8 base attributes, `sheet:opened` triggers 8 × 11 ≈ 88 setAttrs calls. Each is async, creating visible latency.

**Fix direction:** Merge Layer 4a + 4b: each pool base handler also reads `pool_X_misc` and computes the final `pool_X` total in a single `setAttrs` with `{silent: true}`. The `calcPoolTotal` helpers are kept for direct `pool_X_misc` edits (user manually adjusting pool misc values), but no longer fire redundantly during attribute cascades.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 4.1 | Merge spell pool base+total | `sheet.html` | Lines 81-88 (Layer 4a spell) | Read `pool_spell_misc` alongside `cha, int, wil`. Compute `pool_spell_base` AND `pool_spell` in one `setAttrs` with `{silent: true}` |
| 4.2 | Merge combat pool base+total | `sheet.html` | Lines 90-97 (Layer 4a combat) | Same pattern: read `pool_combat_misc`, compute both base and total, `{silent: true}` |
| 4.3 | Merge control pool base+total | `sheet.html` | Lines 99-102 (Layer 4a control) | Read `pool_control_misc` alongside `reaction`, compute both base and total, `{silent: true}` |
| 4.4 | Merge astral pool base+total | `sheet.html` | Lines 105-112 (Layer 4a astral) | Read `pool_astral_misc`, compute both base and total, `{silent: true}` |
| 4.5 | Add `{silent: true}` to `sheet:opened` skill recalc | `sheet.html` | Lines 314-333 (target: `setAttrs(out)` at line 330) | Add `{silent: true}` to the bulk skill totals `setAttrs(out)` call. Skill totals are display-only (no downstream cascade), so silencing is safe. Eliminates N skill change events on every sheet open. |

**Impact:** Saves 4 `setAttrs` triggers per attribute change (4 pool base→total hops eliminated). Over 8 attributes on `sheet:opened`, that's **~11 fewer async calls** (only `int` triggers all 4 pools; most attributes trigger 0–3). The `calcPoolTotal` workers remain functional for direct `pool_X_misc` edits but no longer double-fire during cascade.

**Risk:** `calcPoolTotal` handlers still listen on `change:pool_X_base`. After task 4.1-4.4, the base attrs are set with `{silent: true}`, so `calcPoolTotal` will NOT fire during attribute cascades (desired). It WILL still fire if something else changes `pool_X_base` directly — but nothing does; only Layer 4a handlers write to `pool_X_base`. Safe.

---

### P9: Weapon Category Header Misalignment

**Root:** The weapon header (`.sheet-weapons-header`, CSS line 1633) and weapon rows (`.repitem` children) have a column count mismatch:

**Header children (11):** name, type, mods, power, damage, conceal, reach, ep, range, roll(70px), spacer(20px)
**Row children (12):** name, type, mods, power, damage, conceal, reach, ep, range-bands(152px), Rng-btn, Mel-btn, + repcontrol_del(20px injected by Roll20)

The row has TWO attack buttons (Rng + Mel) as separate flex children vs. ONE "Roll" header span. This creates a 12th flex child in the row, adding an extra 6px gap and misaligning all columns from Right→Left. The buttons also size at `flex: 0 0 auto` (~30px each = ~66px) vs. the header's fixed 70px, causing width drift.

**Fix direction:** Wrap both attack buttons in a container div (`.sheet-weapon-roll-group`) with `flex: 0 0 70px`, matching the header "Roll" column exactly. Internal layout uses flex with a smaller gap. This mirrors the existing `.sheet-range-bands` pattern.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 5.1 | Wrap attack buttons in roll group div | `sheet.html` | Lines 1244-1245 (inside `repeating_weapons`) | Wrap both `<button>` elements in `<div class="sheet-weapon-roll-group">…</div>` |
| 5.2 | Add roll group CSS | `sheet.css` | After `.sheet-btn-attack` rule (~line 1680) | `.sheet-tab-panel-gear .repitem .sheet-weapon-roll-group { display: flex; gap: 2px; flex: 0 0 70px; }` |
| 5.3 | Remove redundant flex from attack buttons | `sheet.css` | Line ~1680 | Change `.sheet-btn-attack { flex: 0 0 auto; }` → `flex: 1 1 auto;` so both buttons share the 70px container equally |

---

## Execution Order (within Phase 2)

1. **P3b** (tasks 3.1–3.2) — CSS-only, two-line edit, zero dependencies
2. **P1a** (tasks 1.1–1.3) — CSS + one HTML attr, zero dependencies
3. **P9** (tasks 5.1–5.3) — HTML wrapper + CSS, zero dependencies
4. **P3a** (tasks 2.1–2.2) — JS `setTimeout(0)` wrapping, depends on Phase 1 P2 being in place for task 2.2
5. **P5** (tasks 4.1–4.5) — JS cascade restructuring, most complex, done last

---

## Verification Checklist

- [ ] Paste updated sheet into Roll20 sandbox
- [ ] P3b: Create mutation with BP cost `1000` → confirm all 4 digits visible in column
- [ ] P3b: Create mutation with BP cost `99` → confirm no excess whitespace
- [ ] P1a: Enter long effect text (40+ chars) in mutation → confirm ellipsis shown, no column overflow
- [ ] P1a: Enter long effect text in adept power → same check
- [ ] P9: Add 3+ weapons → confirm Name/Type/Mods/Pwr/Dmg columns align with header labels
- [ ] P9: Confirm both Rng and Mel buttons visible and clickable within the Roll column
- [ ] P3a: Create new adept power → immediately type name and PP cost rapidly → confirm row persists (not deleted)
- [ ] P3a: Create 3 powers in quick succession, filling fields rapidly → confirm all 3 survive
- [ ] P3a: Delete a power row → confirm PP Used recalculates correctly (setTimeout does not break removal logic)
- [ ] P5: Change `int_base` by 1 → observe dice pools update (confirm cascade still works)
- [ ] P5: Check pool_spell_misc = 2, then change `cha_base` → confirm pool_spell = new_base + 2 (misc preserved)
- [ ] P5: Open sheet → confirm all skill totals display correct values (silent setAttrs didn't suppress them)
- [ ] P5: Manually change `pool_combat_misc` → confirm pool_combat updates (calcPoolTotal still works for direct misc edits)

---

## Cascade Impact Analysis

```
P1a: (no cascade — CSS-only)
P3a: (no cascade — timing fix, same attrs written)
P3b: (no cascade — CSS-only)
P5:  Restructures intermediate cascade:
     BEFORE: attr → pool_X_base ──→ pool_X  (2 hops)
     AFTER:  attr → pool_X_base + pool_X    (1 hop, silent)
     calcPoolTotal still active for pool_X_misc edits
P9:  (no cascade — HTML wrapper + CSS)
```

P5 is the only item that touches the cascade. All other items are CSS or timing fixes with zero cascade impact.

---
---

## Phase 3: Data Entry Enhancements

**3 items, 16 tasks. Changes across `roll20/sheet.html` and `roll20/sheet.css`.**

---

### P8: Weapon Type Select — Full Overhaul

**Root:** Current `<select>` for `attr_weapon_type` (line 1223) has only 7 options: Edged, Club, Polearm, Unarmed, Bow, Crossbow, Thrown. The Equipment reference spreadsheet defines 17 canonical weapon types organized into categories. Players cannot accurately represent their weapons.

**Current HTML (lines 1223-1231):**
```html
<select class="sheet-weapon-type" name="attr_weapon_type">
  <option value="Edged">Edged</option>
  <option value="Club">Club</option>
  <option value="Polearm">Polearm</option>
  <option value="Unarmed">Unarmed</option>
  <option value="Bow">Bow</option>
  <option value="Crossbow">Crossbow</option>
  <option value="Thrown">Thrown</option>
</select>
```

**Canonical types (from L1 strategic plan, Equipment spreadsheet):**
```
Edged — Throwing    Blunt — Throwing     Whip        Bow
Edged — Light       Blunt — Light        Flail       Crossbow — Hand
Edged — Single      Blunt — Single       Staff       Crossbow — Medium
Edged — Great       Blunt — Great        Unarmed     Crossbow — Heavy
Polearm
```
Mounted and Siege categories omitted (not player-relevant).

**Fix direction:** Replace the 7-option `<select>` with a 17-option grouped `<select>` using `<optgroup>` for visual organization. Values use hyphenated lowercase for canonical storage (e.g., `edged-throwing`). Display labels match the reference exactly.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 1.1 | Replace weapon type select | `sheet.html` | Lines 1223-1231 | Replace the existing 7-option `<select>` with the new 17-option grouped `<select>`. Grouping: `Edged` (4), `Blunt` (4), `Other Melee` (Polearm, Whip, Flail, Staff, Unarmed = 5), `Ranged` (Bow, 3× Crossbow = 4). Values are lowercase-hyphenated (e.g., `edged-light`, `blunt-great`, `crossbow-hand`). |
| 1.2 | Widen weapon type CSS column | `sheet.css` | Line ~1646 (header) + line ~1658 (row) | Current `.sheet-hdr-weapon-type { flex: 0 0 80px }` and `.sheet-weapon-type { flex: 0 0 80px; width: 80px }` may clip longer labels like "Crossbow — Heavy". Widen to `flex: 0 0 110px; width: 110px` |
| 1.3 | Update sync SECTIONS map | `sheet.html` | Line ~442 (weapons array) | No change needed — `weapon_type` is already in the SECTIONS map. Verify only. |

**Note:** Existing characters with old values (e.g., `"Edged"`, `"Club"`) will see an empty/unmatched select on load. This is acceptable — Roll20 `<select>` elements show blank when the stored value doesn't match any `<option value>`. Players re-select on next edit. Specifically: "Thrown" requires re-categorizing as `edged-throwing` or `blunt-throwing`; "Club" maps to the appropriate `blunt-*` subtype. A migration worker is not warranted for 5 players and is fragile across custom homebrew entries.

---

### P10: Equipment Quantity Column

**Root:** Equipment section has no quantity field. Players with multiple identical items (e.g., 5 healing herbs) enter duplicate rows or manually calculate total EP. The EP Total worker (line ~155) sums individual `equip_ep` values without quantity multiplication.

**Current equipment row (lines 1259-1261):**
```html
<input type="text" class="sheet-equip-name" name="attr_equip_name" placeholder="Item Name">
<input type="text" class="sheet-equip-desc" name="attr_equip_description" placeholder="Description">
<input type="number" class="sheet-equip-ep" name="attr_equip_ep" value="0">
```

**Fix direction:** Add `equip_qty` number field (default 1) between name and description. EP Total worker must read `equip_qty` and multiply: `total += equip_ep × equip_qty` per equipment row. Weapon rows are NOT affected (weapons are always qty=1 as individual items).

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 2.1 | Add quantity header column | `sheet.html` | Line 1253 (inside `.sheet-equipment-header`) | Add `<span class="sheet-hdr-equip-qty">Qty</span>` after the name span |
| 2.2 | Add quantity input to equipment fieldset | `sheet.html` | Line 1259 (inside `repeating_equipment`, after name input) | Add `<input type="number" class="sheet-equip-qty" name="attr_equip_qty" value="1" min="1">` |
| 2.3 | Add header qty CSS | `sheet.css` | After `.sheet-hdr-equip-name` (~line 1159) | `.sheet-hdr-equip-qty { flex: 0 0 40px; text-align: center; }` |
| 2.4 | Add row qty CSS | `sheet.css` | After `.sheet-equip-name` (~line 1163) | `.sheet-tab-panel-gear .repitem .sheet-equip-qty { flex: 0 0 40px; width: 40px; text-align: center; }` |
| 2.5 | Update EP Total worker — add qty trigger + field read | `sheet.html` | Line ~155 (EP Total worker) | Add `change:repeating_equipment:equip_qty` to the `on()` trigger list. In the `getAttrs` fields array, push `equip_qty` alongside `equip_ep` for each equipment ID. In the summation loop, compute `total += equip_ep × (equip_qty \|\| 1)` (default 1 if empty/undefined, so existing characters with no `equip_qty` still work). |
| 2.6 | Add `equip_qty` to sync SECTIONS | `sheet.html` | Line ~444 (equipment array) | Add `'equip_qty'` to the `equipment` array in the SECTIONS map: `equipment: ['equip_name', 'equip_description', 'equip_qty', 'equip_ep']` |

**Backward compatibility:** Existing equipment rows have no `equip_qty` attribute. `getAttrs` returns `undefined` → `parseFloat(undefined) || 0` = 0. We guard with `(qty || 1)` so missing qty defaults to 1 (not 0), preserving existing EP totals.

---

### P1b: Effect "Send to Chat" Buttons

**Root:** Mutation and adept power "Effect" fields are single-line text inputs that clip long text (addressed cosmetically in Phase 2 P1a with ellipsis). Users want to send the full effect text to the Roll20 chat for table-wide visibility during play. Per L1's dependency note: "P1a (Phase 2) should be done first so effect text is visible before we add the chat button."

**Scope note:** L1 referenced "spell/mutation/power" effect fields, but `repeating_spells` has no effect text field (only name, force, drain, and roll buttons). Spells are excluded — the L1 reference to spells was aspirational. Only mutations and adept powers have effect fields.

**Approach:** Add a small roll button (💬) next to each effect field that outputs the effect text to chat using a new `desc` roll template. Roll20 roll buttons inside repeating sections can reference same-row attributes with `@{attr_name}`.

**Tasks:**

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 3.1 | Add mutation effect chat button | `sheet.html` | Line 931 (after mutation effect input, inside `repeating_mutations`) | Add: `<button type="roll" name="roll_btn_mutation_effect" class="sheet-btn-chat-effect" value="&{template:desc} {{charname=@{char_name}}} {{rollname=@{mutation_name}}} {{desc=@{mutation_effect}}}" title="Send effect to chat">&#x1F4AC;</button>` |
| 3.2 | Add power effect chat button | `sheet.html` | Line 960 (after power effect input, inside `repeating_adept_powers`) | Add: `<button type="roll" name="roll_btn_power_effect" class="sheet-btn-chat-effect" value="&{template:desc} {{charname=@{char_name}}} {{rollname=@{power_name}}} {{desc=@{power_effect}}}" title="Send effect to chat">&#x1F4AC;</button>` |
| 3.3 | Add chat effect button CSS | `sheet.css` | After mutation/power row CSS sections (~line 830) | `.sheet-btn-chat-effect { flex: 0 0 24px; width: 24px; height: 24px; padding: 0; font-size: 14px; cursor: pointer; border: 1px solid #cccccc; background: #f9f9f9; text-align: center; line-height: 24px; }` |
| 3.4 | Add chat button header spacer | `sheet.html` | Lines 924 + 953 (mutation + power headers) | In both headers, add `<span class="sheet-hdr-chat">&#x1F4AC;</span>` before the spacer span. This provides a visual header above the chat button column. |
| 3.5 | Add header chat column CSS | `sheet.css` | After chat effect button CSS | `.sheet-hdr-chat { flex: 0 0 24px; text-align: center; font-size: 12px; }` |

**CSS interaction with P1a (Phase 2):** The effect field retains its `flex: 2 1 120px` sizing. Adding a 24px chat button column reduces the remaining flex space slightly but `flex: 2 1` absorbs this gracefully — the effect field shrinks by ~30px total (24px button + 6px gap), which is acceptable given its 120px+ flex-basis.

**Design note:** The `skill` template was initially considered but produces unwanted "TN unknown" noise via its `{{^tn}}` block. A minimal `description` roll template (8 lines of HTML) is cleaner than hacking around the `skill` template's conditional blocks.

| # | Task | File | Location | Detail |
|---|---|---|---|---|
| 3.6 | Add description roll template | `sheet.html` | After the `spell` rolltemplate (~line 1448) | New `<rolltemplate class="sheet-rolltemplate-desc">` with just `charname`, `rollname`, and `desc` fields. Minimal wrapper matching existing template styling. |
| 3.7 | Add description template CSS | `sheet.css` | After existing roll template CSS (~line 1400) | Add `.sheet-rolltemplate-desc .sheet-template-body` and `.sheet-rolltemplate-desc .sheet-template-row` to the existing grouped selector lists at lines ~1338-1346. Add unique header color: `.sheet-rolltemplate-desc .sheet-template-header { background-color: #2a3a2a; color: #ffffff; padding: 6px 10px; font-size: 13px; font-weight: bold; }`. Add `.sheet-rolltemplate-desc .sheet-template-desc { padding: 4px 8px; white-space: pre-wrap; font-size: 13px; }` for the description text block. |



---

## Execution Order (within Phase 3)

1. **P8** (tasks 1.1–1.3) — HTML select replacement + CSS width, zero dependencies
2. **P10** (tasks 2.1–2.6) — HTML + CSS + JS worker update, zero dependencies
3. **P1b** (tasks 3.1–3.7) — HTML buttons + roll template + CSS, depends on Phase 2 P1a being complete (effect field visible with ellipsis before adding chat button)

---

## Verification Checklist

- [ ] Paste updated sheet into Roll20 sandbox
- [ ] P8: Open weapon row → confirm all 17 types visible in grouped dropdown
- [ ] P8: Select "Crossbow — Heavy" → confirm label fully visible (not clipped)
- [ ] P8: Select "Edged — Light" → confirm value stored (check via API sandbox)
- [ ] P8: Existing character with old `weapon_type="Edged"` → confirm blank select shown (expected — re-select to fix)
- [ ] P10: Add equipment row → confirm Qty column visible with default value 1
- [ ] P10: Set Qty=3, EP=5 → confirm EP Total includes 15 (not 5)
- [ ] P10: Set Qty=1, EP=10 → confirm EP Total includes 10
- [ ] P10: Existing character with no qty field → confirm EP Total unchanged (defaults to ×1)
- [ ] P10: Add 2 weapons + 3 equipment items with various qtys → confirm EP Total = sum of (weapon_ep × 1) + sum of (equip_ep × equip_qty)
- [ ] P1b: Click chat button (💬) on mutation → confirm effect text appears in Roll20 chat with character name
- [ ] P1b: Click chat button on adept power → same check
- [ ] P1b: Mutation with empty effect → confirm chat button outputs just the character and mutation name (no crash)
- [ ] P1b: Confirm chat button header labels (💬) align with the button column

---

## Cascade Impact Analysis

```
P8:  (no cascade — HTML select options only, value stored as-is)
P10: equip_qty ──→ ep_total (1 downstream, via updated EP Total worker)
     New trigger adds: change:repeating_equipment:equip_qty
P1b: (no cascade — roll button output only, no setAttrs)
```

P10 is the only item with cascade impact. The EP Total worker already runs on `change:repeating_equipment:equip_ep` — we add `equip_qty` to the same trigger list. The worker's output (`ep_total`) is a terminal display value with no downstream listeners.

---

Phase 3: Data Entry Enhancements — 3 items (P8, P10, P1b), 16 tasks across sheet.html and sheet.css. Includes new desc rolltemplate for P1b chat buttons.

---
---

## Phase 4: Skill Specialization

**1 item (P4), 10 tasks. Changes in `roll20/sheet.html` only (HTML + JS). No CSS changes (hidden inputs don't render).**

**Governing Design:** ADR-002 (Skill Specialization Model)

---

### P4: Spec Checkbox → Sub-Skill Creation Flow

**Root:** Skill fieldset (`repeating_skills`, line ~882). Spec checkbox exists (line ~896, `attr_skill_spec` value="1") but currently does nothing — it's a visual-only marker. ADR-002 defines the full programmatic specialization lifecycle.

**Mechanic Summary:**
- **Check (spec=1):** Guard `base < 1` → abort. Otherwise: `generateRowID()` to create child row with `base + 1`, reduce parent `base - 1`, cross-link via hidden ID fields.
- **Uncheck (spec=0):** Restore parent `base += 1`, `removeRepeatingRow()` on child. Clear cross-references.
- **Orphan cleanup (`sheet:opened`):** If parent has `skill_child_id` pointing to a deleted row → restore parent base, clear ref, uncheck spec. If child has `skill_parent_id` pointing to a deleted row → remove the orphaned child.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 4.1 | Add `skill_parent_id` hidden input | sheet.html line ~897 (after spec checkbox) | `<input type="hidden" name="attr_skill_parent_id" value="">` — stores the row ID of the parent skill (empty on parent rows, populated on child rows) |
| 4.2 | Add `skill_child_id` hidden input | sheet.html line ~898 (after parent_id) | `<input type="hidden" name="attr_skill_child_id" value="">` — stores the row ID of the child specialization (empty on child rows, populated on parent rows) |
| 4.3 | Add `skill_parent_id`, `skill_child_id` to SECTIONS map | sheet.html line ~429 | Update skills array: `['skill_name', 'skill_linked_attr', 'skill_general', 'skill_spec', 'skill_base', 'skill_foci', 'skill_misc', 'skill_total', 'skill_parent_id', 'skill_child_id']` — ensures sync payload captures cross-references |
| 4.4 | New worker: spec check handler (on-check branch) | sheet.html — new Layer 5c2 block after skill total worker (line ~198) | `on('change:repeating_skills:skill_spec', function(eventInfo) { ... })`. On-check (spec="1") branch: (1) Extract parent row ID from `eventInfo.sourceAttribute` via regex. (2) Read `skill_name`, `skill_base`, `skill_linked_attr`, `skill_general`, `skill_parent_id`, `skill_child_id`. (3) **Guard — already a child:** if `skill_parent_id` is non-empty, revert `setAttrs({ skill_spec: 0 }, {silent:true})` and return (specializations can't specialize further). (3b) **Guard — already specialized:** if `skill_child_id` is non-empty, revert `setAttrs({ skill_spec: 0 }, {silent:true})` and return (prevents orphaning a prior child if state is inconsistent). (4) **Guard — base too low:** if `parseInt(skill_base) < 1`, revert with `{silent:true}` and return. (5) `var newId = generateRowID()`. (6) Build child attrs object with prefix `'repeating_skills_' + newId + '_'`: `skill_name` = parentName + " (Spec)", `skill_base` = parentBase + 1, `skill_linked_attr` = same, `skill_general` = same, `skill_parent_id` = parentRowId, `skill_spec` = "0". (7) Build parent update: `skill_base` = parentBase - 1, `skill_child_id` = newId. (8) Single `setAttrs` combining child creation + parent update. |
| 4.5 | Spec check handler (on-uncheck branch) | Same worker as 4.4 | On-uncheck (spec="0") branch: (1) Read `skill_child_id`, `skill_base`. (2) If `skill_child_id` is empty → return (nothing to undo, e.g., revert from guard). (3) `setAttrs` to restore parent: `skill_base` = currentBase + 1, clear `skill_child_id` to "". (4) `removeRepeatingRow('repeating_skills_' + childId)` after `setAttrs`. **Rationale:** `setAttrs` first ensures the parent's base is restored even if execution is interrupted after this step; if the child lingers, `sheet:opened` orphan cleanup removes it on next load. The reverse failure mode (child removed but parent base never restored) would leave a permanent -1 deficit with no automatic recovery. |
| 4.6 | Update `sheet:opened` — gather cross-ref fields | sheet.html lines ~318-333 (existing skill total recalc block) | In the `getSectionIDs('repeating_skills', ...)` callback, add `skill_parent_id` and `skill_child_id` to the fields array alongside `skill_base`, `skill_foci`, `skill_misc`. This makes the IDs available for orphan detection in the same getAttrs call. |
| 4.7 | Orphan cleanup — parent→child direction | sheet.html — inside `sheet:opened` skill block, after field gathering | After building the `out` object for skill totals: (1) Collect `validIds` set from the `ids` array. (2) For each row: if `skill_child_id` is non-empty AND not in `validIds` → add to `out`: `skill_child_id` = "", `skill_spec` = "0", `skill_base` = currentBase + 1. This restores the parent's point that was deducted when the (now-deleted) child was created. |
| 4.8 | Orphan cleanup — child→parent direction | sheet.html — inside `sheet:opened` skill block, after 4.7 | For each row: if `skill_parent_id` is non-empty AND not in `validIds` → call `removeRepeatingRow('repeating_skills_' + id)`. Note: `removeRepeatingRow` is called outside `setAttrs` since it's a separate API. Collect these orphan IDs in an array and loop after the main `setAttrs(out)` call. |
| 4.9 | Verify skill total recalc excludes orphans | sheet.html — `sheet:opened` skill block | After 4.8 removes orphaned children, the existing skill total recalc loop already runs on all remaining rows. No change needed — just a verification note that orphan removal happens BEFORE `setAttrs(out)` so removed rows don't pollute the output. Sequence: gather fields → detect orphans → remove child orphans → build totals for remaining rows → single `setAttrs(out)`. |

**Implementation Sequencing Note:**
Tasks 4.6–4.9 modify the same `sheet:opened` → `getSectionIDs('repeating_skills', ...)` block. The final code structure should be:
```
getSectionIDs('repeating_skills', function(ids) {
  // 1. Build fields array (existing + parent_id/child_id)     [Task 4.6]
  // 2. getAttrs(fields, function(v) {
  //   a. Build validIds set from ids array                     [Task 4.7]
  //   b. Detect parent→child orphans, fix in out{}             [Task 4.7]
  //   c. Detect child→parent orphans, collect for removal      [Task 4.8]
  //   d. Remove orphaned children via removeRepeatingRow       [Task 4.8]
  //   e. Build skill_total for remaining rows                  [Task 4.9]
  //      (filter out orphanChildren set so removed rows
  //       don't get phantom attrs; read base from out{}
  //       when an orphan-fixed value exists)
  //   f. setAttrs(out)
  // });
});
```

---

### Acceptance Criteria

- [ ] P4: Checking spec on a skill with `base >= 1` → new child row appears with `base + 1`, parent's `base` decreases by 1
- [ ] P4: Checking spec on a skill with `base = 0` → checkbox reverts, no child created
- [ ] P4: Checking spec on a child row (has `skill_parent_id`) → checkbox reverts, no grandchild
- [ ] P4: Unchecking spec → child row removed, parent's `base` restored
- [ ] P4: Manually deleting child row → on next `sheet:opened`, parent's base restored, spec unchecked, `skill_child_id` cleared
- [ ] P4: Manually deleting parent row → on next `sheet:opened`, orphaned child row removed
- [ ] P4: Child name editable (user can rename from default "(Spec)" suffix)
- [ ] P4: Child row's `skill_linked_attr` and `skill_general` inherited from parent
- [ ] P4: Child row's `skill_total` computes correctly (base + foci + misc)
- [ ] P4: Sync payload includes `skill_parent_id` and `skill_child_id`

---

## Cascade Impact Analysis

```
P4:  skill_spec ──→ skill_base (parent: -1; child: parent_base+1)
                ──→ skill_child_id / skill_parent_id (cross-reference)
     skill_base ──→ skill_total (existing Layer 5c worker, 1 downstream)
     sheet:opened ──→ orphan cleanup ──→ skill_base / removeRepeatingRow

     No new cascade chains — spec handler writes to skill_base which feeds
     the existing skill_total worker. Cross-ref fields are terminal (no
     downstream listeners). Orphan cleanup is sheet:opened only (no change
     triggers).
```

P4 touches `skill_base` which cascades to `skill_total` via the existing Layer 5c worker. No new downstream chains are created. The `{silent:true}` on guard reverts prevents feedback loops.

---

Phase 4: Skill Specialization — 1 item (P4), 10 tasks in sheet.html. New Sheet Worker for spec↔child lifecycle + bidirectional orphan cleanup in `sheet:opened`.

---
---

## Phase 5: Creature Systems

**3 items (G4, G5, P12), 17 tasks. Changes span `roll20/sheet.html` (HTML + JS) and `roll20/sheet.css`.**

**Governing Design:** ADR-003 (Animal Companion / Critter Stat Block Model)

---

### G4: Animal Companions Section (Bio Tab)

**Root:** Players have animal companions (2 of 5 players) with no place to track stats, condition, or rolls. ADR-003 specifies a `repeating_companions` section in the Bio tab (`.sheet-tab-panel-bio`, line ~1286 of sheet.html) after the existing Milestones section (line ~1313).

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 5.1 | Add companion header row HTML | sheet.html — inside `.sheet-tab-panel-bio`, after `</fieldset>` closing `repeating_milestones` (line ~1319) | New `<h3 class="sheet-section-title">Animal Companions</h3>` + `<div class="sheet-section-companions">` + header row div with spans: Name, B, Q, S, C, I, W, E, R, Rcn (Reaction, computed), CM, Atk, (spacer). Follow existing Bio tab header pattern (`.sheet-*-header` flex layout). |
| 5.2 | Add `repeating_companions` fieldset HTML | sheet.html — inside `.sheet-section-companions` after header | `<fieldset class="repeating_companions">` containing: `<input type="text" name="attr_comp_name" placeholder="Name" class="sheet-comp-name">`, 8 stat number inputs (`attr_comp_b`, `attr_comp_q`, `attr_comp_s`, `attr_comp_c`, `attr_comp_i`, `attr_comp_w`, `attr_comp_e`, `attr_comp_r`, all value="0"), 1 readonly reaction display (`attr_comp_reaction`, readonly), CM severity select (`attr_comp_cm_level` — see task 5.3), attack roll button (see G5 tasks), `</fieldset>`, `</div>` closing `.sheet-section-companions`. |
| 5.3 | Companion CM — simplified 3-level select | sheet.html — inside `repeating_companions` fieldset | `<select name="attr_comp_cm_level" class="sheet-comp-cm-level">` with options: `<option value="0">None</option>`, `<option value="1">Light (+1)</option>`, `<option value="2">Moderate (+2)</option>`, `<option value="3">Serious (+3)</option>`. ADR-003 specifies 3 severity levels (L/M/S) → TN penalty per creature. A select is simpler than checkboxes for critters (no full 32-box track needed). The value IS the TN penalty. |
| 5.4 | Add `companions` to SECTIONS sync map | sheet.html line ~448 (after `milestones` entry in SECTIONS object) | `companions: ['comp_name', 'comp_b', 'comp_q', 'comp_s', 'comp_c', 'comp_i', 'comp_w', 'comp_e', 'comp_r', 'comp_reaction', 'comp_cm_level']` |
| 5.5 | New CSS: companion header row | sheet.css — new block in SECTION 14 (Bio Tab), after milestones CSS (line ~1833 area, before SECTION 20) | `.sheet-companions-header` — flex layout mirroring other header rows. Column widths: Name `flex: 1 1 auto`, stats (B–R) `flex: 0 0 38px` each (8 columns), Rcn `flex: 0 0 38px`, CM `flex: 0 0 90px`, Atk `flex: 0 0 36px`. `margin-top: 12px` (matches milestones header). |
| 5.6 | New CSS: companion repeating row columns | sheet.css — after 5.5 | `.sheet-tab-panel-bio .repitem .sheet-comp-name { flex: 1 1 auto; min-width: 0; }`. Stats: `.sheet-comp-b, .sheet-comp-q, ...` all `flex: 0 0 38px; width: 38px; text-align: center;`. Reaction: `.sheet-comp-reaction { flex: 0 0 38px; ... font-weight: bold; border: 1px solid #5f5f5f; background-color: #f2f2f2; }` (mirrors skill total readonly pattern). CM select: `.sheet-comp-cm-level { flex: 0 0 90px; }`. Attack button: `.sheet-comp-attack { flex: 0 0 36px; }`. |
| 5.7 | New worker: companion reaction | sheet.html — new Layer 5g block in REGION 2, after spirit calculator (line ~420 area, before REGION 4) | `on('change:repeating_companions:comp_i change:repeating_companions:comp_q', function() { getAttrs(['comp_i', 'comp_q'], function(v) { setAttrs({ comp_reaction: Math.floor(((parseInt(v.comp_i,10)||0) + (parseInt(v.comp_q,10)||0)) / 2) }); }); })`. Per ADR-003: `reaction = floor((I+Q)/2)`, same formula as player reaction. |
| 5.8 | Add companion reaction recalc to `sheet:opened` | sheet.html — inside `sheet:opened` handler (line ~293), after skill total recalc block | New `getSectionIDs('repeating_companions', function(ids) { ... })` block that reads `comp_i` + `comp_q` for each row, computes `comp_reaction = floor((I+Q)/2)`, and writes via `setAttrs(out)`. Pattern mirrors the existing skill total recalc. |

---

### G5: Companion Attack Rolls (Per-Creature Isolation)

**Root:** ADR-003 requires each companion's attack roll to use the creature's own stats and its own condition penalty — NOT the player's `cm_tn_mod`. The attack button lives inside `repeating_companions` so it can reference row-level `@{comp_*}` attributes directly.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 5.9 | Companion attack roll button HTML | sheet.html — inside `repeating_companions` fieldset (added in 5.2) | `<button type="roll" name="roll_btn_comp_attack" class="sheet-comp-attack" value="&{template:attack} {{charname=@{char_name}}} {{rollname=@{comp_name} Attack}} {{weapon_name=@{comp_name}}} {{tn=[[?{Target Number\|4}+@{comp_cm_level}]]}} {{successes=[[{(?{Dice\|@{comp_reaction}})d6!!}>[[?{Target Number\|4}+@{comp_cm_level}]]]]}} {{power=@{comp_s}}} {{damage_code=?{Damage Code\|@{comp_s}M Physical}}}}" title="Companion attack">&#x1F43E;</button>`. **Key design points:** (a) TN adds `@{comp_cm_level}` (row-level penalty) instead of `@{cm_tn_mod}` (player penalty). (b) Dice default to `@{comp_reaction}` but prompt allows override (natural weapons may use other stat pools). (c) Power defaults to Strength; damage code prompts with a sensible default. (d) Reuses existing `attack` roll template — no new template needed. (e) Paw print emoji (🐾) as button label. |
| 5.10 | Verify `attack` template compatibility | No code change — verification note | The `attack` template (line ~1383) displays: weapon_name, tn, power, damage_code, reach (optional), range_band (optional), successes. All fields in 5.9 map cleanly. `reach` and `range_band` are not passed → their `{{#...}}` conditionals hide them. No template modification needed. |

---

### P12: Spirit Summon + Attack Rolls

**Root:** The Spirit Calculator (line ~1058, `.sheet-section-spirit-calc`) displays computed spirit stats but has no roll buttons. P12 adds: (1) **Summon** — rolls Conjuring skill vs TN to determine services owed. (2) **Attack** — rolls using the spirit's own computed stats (already stored as `attr_spirit_*` by the existing REGION 3b worker).

**Placement:** Both buttons go inside the existing `.sheet-spirit-combat` div (line ~1107), after the Attack display field closing `</div>` (line ~1115). This keeps all combat-relevant spirit info grouped together.

**Tasks:**

| # | Task | Location | Detail |
|---|---|---|---|
| 5.11 | Spirit summon roll button HTML | sheet.html — inside `.sheet-spirit-combat` div, after the Attack display `</div>` (line ~1118) | New `<div class="sheet-spirit-field">` containing: `<button type="roll" name="roll_btn_spirit_summon" class="sheet-spirit-roll-btn" value="&{template:skill} {{charname=@{char_name}}} {{rollname=Conjuring: @{spirit_type} (Force @{spirit_force})}} {{linked_attr=WIL}} {{tn=[[@{spirit_force}+@{cm_tn_mod}]]}} {{successes=[[{?{Conjuring dice\|0}d6!!}>[[@{spirit_force}+@{cm_tn_mod}]]]]}} {{dice=[[{?{Conjuring dice\|0}d6!!}]]}}" title="Summon — Conjuring vs Force">&#x1F52E; Summon</button>` `</div>`. **Key design points:** (a) Uses `skill` template (displays charname, rollname, linked_attr, tn, successes, dice). (b) TN = spirit's Force + player's wound penalty (`cm_tn_mod`). Conjuring is a player skill so player wound penalties apply. (c) Conjuring dice prompted — it's a `repeating_skills` value so can't be referenced as a scalar. (d) Net successes (visible in template) = number of services the spirit owes. (e) Crystal ball emoji (🔮) as label. |
| 5.12 | Spirit attack roll button HTML | sheet.html — inside `.sheet-spirit-combat` div, after summon button | New `<div class="sheet-spirit-field">` containing: `<button type="roll" name="roll_btn_spirit_attack" class="sheet-spirit-roll-btn" value="&{template:attack} {{charname=@{char_name}}} {{rollname=@{spirit_type} Attack}} {{weapon_name=Spirit: @{spirit_type}}} {{tn=[[?{Target Number\|4}]]}} {{successes=[[{?{Attack dice\|@{spirit_b}}d6!!}>[[?{Target Number\|4}]]]]}} {{power=@{spirit_s}}} {{damage_code=@{spirit_attack}}}" title="Spirit melee attack">&#x2694; Attack</button>` `</div>`. **Key design points:** (a) Uses `attack` template (weapon_name, tn, power, damage_code, successes). (b) NO `cm_tn_mod` — spirits don't share the player's condition track. (c) Attack dice default to `@{spirit_b}` (Body stat) but prompt allows override since some spirit categories use different attack pools. (d) Power = Spirit's Strength; damage_code = `@{spirit_attack}` (the spirit calculator already computes human-readable attack strings like "4M" or "As Powers"). (e) Crossed swords emoji (⚔) as label. |
| 5.13 | New CSS: spirit roll buttons | sheet.css — after existing spirit textarea CSS (line ~1128 area) | `.sheet-spirit-roll-btn { padding: 4px 10px; font-size: 13px; cursor: pointer; margin-top: 4px; }`. Keep styling minimal — the spirit calculator section already has good spacing. |
| 5.14 | Spirit summon — services tracking note | No code change — design note | Net successes from the summon roll are displayed in the roll template output but NOT tracked as a stored attribute. Tracking services is a narrative/GM concern — not a computed sheet field. If future demand arises, a simple `attr_spirit_services` number input can be added next to the summon button. This is explicitly a non-goal for this phase per ADR-003's scope. |

---

### Cross-Phase Integration Notes

| # | Task | Location | Detail |
|---|---|---|---|
| 5.15 | Verify no scalar field conflicts | Verification — no code change | New scalar attrs: none (all companion fields are repeating-section scoped; spirit attrs already exist). Sync payload impact: `companions` added to SECTIONS map (task 5.4). Spirit roll buttons produce template output only — no `setAttrs`. |
| 5.16 | Verify companion reaction formula parity | Verification — no code change | Player reaction (Layer 3a, line ~90): `reaction = floor((int + quickness) / 2)`. Companion reaction (task 5.7): `comp_reaction = floor((comp_i + comp_q) / 2)`. Identical formula, different attributes. Confirmed per ADR-003. |
| 5.17 | CSS section placement plan | sheet.css — verification note | Companion CSS (tasks 5.5-5.6) belongs in SECTION 14 (Bio Tab), after milestones CSS. Spirit button CSS (task 5.13) belongs in the spirit calculator block (after line ~1128). No new CSS sections needed. |

---

### Acceptance Criteria

- [ ] G4: Companions section appears in Bio tab below Milestones
- [ ] G4: Each companion row has: Name, B, Q, S, C, I, W, E, R (editable), Reaction (readonly, computed), CM select, Attack button
- [ ] G4: Adding a companion row and filling stats → Reaction computes as `floor((I+Q)/2)`
- [ ] G4: Companion section appears in sync payload via SECTIONS map
- [ ] G4: Header column widths align with repeating row columns
- [ ] G5: Companion attack button rolls using `attack` template
- [ ] G5: Companion attack TN includes `@{comp_cm_level}` (row-level), NOT `@{cm_tn_mod}` (player-level)
- [ ] G5: Companion attack dice default to `@{comp_reaction}` with prompt override
- [ ] G5: Damage code prompts with creature's Strength as default
- [ ] P12: Spirit Summon button visible in Spirit Calculator after selecting a type
- [ ] P12: Summon roll uses `skill` template, TN = Force + player wound mod, dice prompted
- [ ] P12: Spirit Attack button visible in Spirit Calculator
- [ ] P12: Spirit attack TN does NOT include `@{cm_tn_mod}` (spirit is independent)
- [ ] P12: Spirit attack dice default to `@{spirit_b}` with prompt override
- [ ] P12: Spirit attack power/damage reads from computed spirit stats
- [ ] P12: Both spirit roll buttons are non-functional when no spirit type selected (template displays blank fields — acceptable, no guard needed)

---

## Cascade Impact Analysis

```
G4:  comp_i ──→ comp_reaction (1 downstream, via new Layer 5g worker)
     comp_q ──→ comp_reaction (1 downstream, via same worker)
     comp_cm_level ──→ (no downstream — read inline by attack button macro only)
     sheet:opened ──→ comp_reaction recalc (new getSectionIDs block)

G5:  (no cascade — roll button output only, no setAttrs)

P12: (no cascade — roll button output only, no setAttrs)
     Spirit buttons read existing attrs (spirit_type, spirit_force, spirit_b,
     spirit_s, spirit_attack) — all computed by the existing REGION 3b worker.
     No new dependencies on the spirit calculator cascade.
```

G4 introduces one new cascade chain: `comp_i/comp_q → comp_reaction` (terminal display value, no further downstream). G5 and P12 are pure roll template output — zero cascade impact.

---

Phase 5: Creature Systems — 3 items (G4, G5, P12), 12 implementation tasks + 5 verification notes across sheet.html and sheet.css. New `repeating_companions` section, companion reaction worker, companion attack roll, spirit summon + attack roll buttons.