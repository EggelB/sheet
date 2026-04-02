# Sheet UAT R1 — Layer 3: Technical Blueprints

**Project:** `sheet_uat_r1`
**Branch:** `fix/sheet-uat-r1`
**Source:** Layer 2 operational plan (approved 2026-04-01)

---
---

## Phase 1: Critical Bug Fixes — Technical Blueprint

**5 items (P6, P11, G1, P2, P7), 11 tasks. All changes in `roll20/sheet.html`.**
**Execution order:** P11 → G1 → P6 → P2 → P7 (as specified in L2)

---

### P11: Karma Total — Fix `+` to `-` (Task 2.1)

**File:** `roll20/sheet.html` — Layer 6a, line 245
**Current code:**
```js
on('change:karma_good change:karma_used', function() {
  getAttrs(['karma_good', 'karma_used'], function(v) {
    setAttrs({
      karma_total: (parseInt(v.karma_good, 10) || 0) + (parseInt(v.karma_used, 10) || 0)
    });
  });
});
```

**Blueprint — change `+` to `-`:**
```js
on('change:karma_good change:karma_used', function() {
  getAttrs(['karma_good', 'karma_used'], function(v) {
    setAttrs({
      karma_total: (parseInt(v.karma_good, 10) || 0) - (parseInt(v.karma_used, 10) || 0)
    });
  });
});
```

**Affected lines:** 245 only (the `+` on the `karma_total` formula)
**Cascade impact:** `karma_total` is terminal — no downstream listeners.

---

### G1: Resist Damage (Body) — Remove Wound Penalty (Tasks 3.1–3.2)

**File:** `roll20/sheet.html` — Combat Buttons, line 1190
**Current code (single line, reformatted for clarity):**
```html
<button type="roll" name="roll_btn_damage_resist_body"
  value="&{template:skill}
    {{charname=@{char_name}}}
    {{rollname=Resist Damage (Body)}}
    {{tn=[[?{TN (Power - Armor)|0}+@{cm_tn_mod}]]}}
    {{successes=[[{(@{body}+?{Combat Pool dice|0})d6!!}>[[?{TN (Power - Armor)|0}+@{cm_tn_mod}]]]]}}">
  Resist Damage (Body)</button>
```

**Blueprint — remove both `+@{cm_tn_mod}` references:**
```html
<button type="roll" name="roll_btn_damage_resist_body"
  value="&{template:skill}
    {{charname=@{char_name}}}
    {{rollname=Resist Damage (Body)}}
    {{tn=[[?{TN (Power - Armor)|0}]]}}
    {{successes=[[{(@{body}+?{Combat Pool dice|0})d6!!}>[[?{TN (Power - Armor)|0}]]]]}}">
  Resist Damage (Body)</button>
```

**Note:** This is a single HTML line in the source. The reformatting above is for clarity — the actual edit is two string deletions of `+@{cm_tn_mod}` within that one line.
**Affected lines:** 1190 only.
**Cascade impact:** None — roll macro output only.

---

### P6: Initiative Score — Add `cm_init_mod` (Tasks 1.1–1.3)

**File:** `roll20/sheet.html` — Layer 4c, lines 134–141
**Current code:**
```js
on('change:reaction change:init_reaction_mod change:init_misc_mod', function() {
  getAttrs(['reaction', 'init_reaction_mod', 'init_misc_mod'], function(v) {
    var reaction       = parseInt(v.reaction, 10) || 0;
    var init_react_mod = parseInt(v.init_reaction_mod, 10) || 0;
    var init_misc_mod  = parseInt(v.init_misc_mod, 10) || 0;
    setAttrs({ init_score: reaction + init_react_mod + init_misc_mod });
  });
});
```

**Blueprint — add `cm_init_mod` to trigger, getAttrs, and formula:**
```js
on('change:reaction change:init_reaction_mod change:init_misc_mod change:cm_init_mod', function() {
  getAttrs(['reaction', 'init_reaction_mod', 'init_misc_mod', 'cm_init_mod'], function(v) {
    var reaction       = parseInt(v.reaction, 10) || 0;
    var init_react_mod = parseInt(v.init_reaction_mod, 10) || 0;
    var init_misc_mod  = parseInt(v.init_misc_mod, 10) || 0;
    var cm_init_mod    = parseInt(v.cm_init_mod, 10) || 0;
    setAttrs({ init_score: reaction + init_react_mod + init_misc_mod + cm_init_mod });
  });
});
```

**Affected lines:** 134 (trigger), 135 (getAttrs), new line for var, 140 (formula).
**Note:** `cm_init_mod` is stored as a negative value by `calcCMPenalty` (line 267: `cm_init_mod: -1 * tn_mod`), so we ADD it to reduce the initiative score.
**Cascade impact:** `init_score` is terminal — no downstream listeners.

---

### P2: Power Points — Text→Numeric Sync (Tasks 4.1–4.2)

#### Task 4.1: New sync worker

**File:** `roll20/sheet.html` — insert after Layer 5d PP remaining worker (after line ~225, before Layer 5e)
**Insertion point:** After the `power_points_remaining` worker closing `});`, before the `// ─── Layer 5e:` comment.

**Blueprint — new worker:**
```js
// ─── Layer 5d2: PP Cost text→numeric sync ────────────────

on('change:repeating_adept_powers:power_pp_cost', function() {
  getAttrs(['power_pp_cost'], function(v) {
    setAttrs({ power_pp_cost_value: parseFloat(v.power_pp_cost) || 0 });
  });
});
```

**Design note:** Writing to `power_pp_cost_value` triggers the existing `change:repeating_adept_powers:power_pp_cost_value` listener (line ~207), which sums all rows into `power_points_used`. The cascade continues: `power_points_used → power_points_remaining`. No additional wiring needed.

#### Task 4.2: `sheet:opened` recalc for legacy characters

**File:** `roll20/sheet.html` — inside `on('sheet:opened', ...)`, after the skill totals `getSectionIDs` block (after line ~332, before the closing `});` of `sheet:opened`).

**Blueprint — new block inside `sheet:opened`:**
```js
  // Recalculate PP cost numeric values on sheet open (legacy character fix)
  getSectionIDs('repeating_adept_powers', function(ids) {
    var fields = [];
    ids.forEach(function(id) {
      fields.push('repeating_adept_powers_' + id + '_power_pp_cost');
    });
    getAttrs(fields, function(v) {
      var out = {};
      ids.forEach(function(id) {
        var p = 'repeating_adept_powers_' + id + '_';
        out[p + 'power_pp_cost_value'] = parseFloat(v[p + 'power_pp_cost'] || 0) || 0;
      });
      setAttrs(out);
    });
  });
```

**Note:** This writes all `power_pp_cost_value` fields in one batch `setAttrs`. Each write triggers the PP used summation worker (line ~207), but since we're inside `sheet:opened`, the repeat triggering is acceptable — the final value converges correctly. The `parseFloat` handles fractional costs (0.25, 0.5, 1.5).

---

### P7: Magic Ignores Mutation Essence Cost — ADR-001 (Tasks 5.1–5.6)

This is the most complex item — 6 tasks across HTML, workers, and sync. Blueprint covers each in execution order.

#### Task 5.1: Add hidden `essence_spent` field

**File:** `roll20/sheet.html` — Mutations summary, after `attr_essence_total` (line 915)
**Current HTML at lines 912–916:**
```html
      <div class="sheet-mutations-summary">
        <span class="sheet-summary-title">ESSENCE</span>
        <label>Total:</label>
        <input type="number" name="attr_essence_total" value="6" readonly class="sheet-computed-badge">
      </div>
```

**Blueprint — add hidden field after `essence_total` input, before `</div>`:**
```html
      <div class="sheet-mutations-summary">
        <span class="sheet-summary-title">ESSENCE</span>
        <label>Total:</label>
        <input type="number" name="attr_essence_total" value="6" readonly class="sheet-computed-badge">
        <input type="hidden" name="attr_essence_spent" value="0">
      </div>
```

**Note:** `essence_total` HTML default remains `value="6"` — correct, because `essence_total = 6 - essence_spent`, and `essence_spent` defaults to 0.

#### Task 5.2: Rename Layer 5e worker output from `essence_total` to `essence_spent`

**File:** `roll20/sheet.html` — Layer 5e, line 235
**Current code (lines 228–238):**
```js
on('change:repeating_mutations:mutation_essence remove:repeating_mutations', function() {
  getSectionIDs('repeating_mutations', function(ids) {
    var fields = [];
    ids.forEach(function(id) { fields.push('repeating_mutations_' + id + '_mutation_essence'); });
    getAttrs(fields, function(v) {
      var total = 0;
      ids.forEach(function(id) { total += parseFloat(v['repeating_mutations_' + id + '_mutation_essence'] || 0); });
      setAttrs({ essence_total: total });
    });
  });
});
```

**Blueprint — change output attr name:**
```js
on('change:repeating_mutations:mutation_essence remove:repeating_mutations', function() {
  getSectionIDs('repeating_mutations', function(ids) {
    var fields = [];
    ids.forEach(function(id) { fields.push('repeating_mutations_' + id + '_mutation_essence'); });
    getAttrs(fields, function(v) {
      var total = 0;
      ids.forEach(function(id) { total += parseFloat(v['repeating_mutations_' + id + '_mutation_essence'] || 0); });
      setAttrs({ essence_spent: total });
    });
  });
});
```

**Affected lines:** 235 only — `essence_total` → `essence_spent`.

#### Task 5.3: New `essence_total` dependent worker

**File:** `roll20/sheet.html` — insert immediately after the renamed Layer 5e worker (after line ~237).

**Blueprint — new worker:**
```js
on('change:essence_spent', function() {
  getAttrs(['essence_spent'], function(v) {
    setAttrs({ essence_total: Math.max(0, 6 - (parseFloat(v.essence_spent) || 0)) });
  });
});
```

**Design note:** Floors at 0 — `essence_total` (Humanity) can't go negative per ADR-001. Uses `parseFloat` for consistency with the mutation essence summation (though integer costs are expected, the existing worker uses `parseFloat`).

#### Task 5.4: Rewrite mag worker

**File:** `roll20/sheet.html` — Layer 2, lines 53–58 (line 53 is a comment)
**Current code (line 53 is a comment that must also be replaced — see note below):**
```js
// mag has no _mutations or _magic sub-fields by design
on('change:mag_base change:mag_misc', function() {
  getAttrs(['mag_base', 'mag_misc'], function(v) {
    setAttrs({ mag: (parseInt(v.mag_base, 10) || 0) + (parseInt(v.mag_misc, 10) || 0) });
  });
});
```

**Blueprint — add `essence_spent` dependency (replaces comment + worker):**
```js
// mag = base + misc - essence_spent (ADR-001; floors at 0)
on('change:mag_base change:mag_misc change:essence_spent', function() {
  getAttrs(['mag_base', 'mag_misc', 'essence_spent'], function(v) {
    var base  = parseInt(v.mag_base, 10) || 0;
    var misc  = parseInt(v.mag_misc, 10) || 0;
    var spent = parseFloat(v.essence_spent) || 0;
    setAttrs({ mag: Math.max(0, base + misc - spent) });
  });
});
```

**Affected lines:** 53 (comment replaced), 54 (trigger), 55 (getAttrs), 56 (formula — expanded to 4 lines for clarity).
**Cascade impact:** Writing `mag` triggers: `power_points_max` (Layer 5d) → `power_points_remaining`, and `pool_astral_base` (Layer 4b) → `pool_astral`. Existing cascade chain handles propagation automatically.

#### Task 5.5: Add `essence_spent` recalc to `sheet:opened`

**File:** `roll20/sheet.html` — inside `on('sheet:opened', ...)`, after the PP cost recalc block (task 4.2), before the closing `});`.

**Blueprint — new block inside `sheet:opened`:**
```js
  // Recalculate essence_spent on sheet open (legacy character migration)
  getSectionIDs('repeating_mutations', function(ids) {
    var fields = [];
    ids.forEach(function(id) {
      fields.push('repeating_mutations_' + id + '_mutation_essence');
    });
    getAttrs(fields, function(v) {
      var total = 0;
      ids.forEach(function(id) {
        total += parseFloat(v['repeating_mutations_' + id + '_mutation_essence'] || 0);
      });
      setAttrs({ essence_spent: total });
    });
  });
```

**Design note:** Writing `essence_spent` triggers both the new `essence_total` worker (task 5.3) and the updated `mag` worker (task 5.4). This ensures legacy characters with pre-existing mutations get correct Humanity and Magic values on first load.

#### Task 5.6: Add `essence_spent` to sync scalar fields

**File:** `roll20/sheet.html` — scalarFields array, line 477
**Current value at line 477:**
```js
    'spells_sustained', 'sustained_tn_mod', 'tn_warning_level', 'essence_total',
```

**Blueprint — add `essence_spent` after `essence_total`:**
```js
    'spells_sustained', 'sustained_tn_mod', 'tn_warning_level', 'essence_total', 'essence_spent',
```

**Affected lines:** 477 only.

---

### Full `sheet:opened` Blueprint (Post-Phase 1)

For clarity, here is the complete `sheet:opened` handler structure after all Phase 1 additions. New additions marked with `[NEW]`:

```js
on('sheet:opened', function() {
  // Re-trigger cascade roots
  getAttrs([...], function(v) {
    setAttrs({ body_base: v.body_base, ... });   // existing
  });

  calcCMPenalty();                                 // existing

  // Recalculate all skill totals                  // existing
  getSectionIDs('repeating_skills', function(ids) { ... });

  // [NEW — Task 4.2] Recalculate PP cost numeric values
  getSectionIDs('repeating_adept_powers', function(ids) { ... });

  // [NEW — Task 5.5] Recalculate essence_spent
  getSectionIDs('repeating_mutations', function(ids) { ... });
});
```

**Ordering note:** `repeating_adept_powers` block goes before `repeating_mutations` block. This is intentional for readability (matches execution order P2 → P7) but functionally independent — the two `getSectionIDs` callbacks don't depend on each other since Roll20's sheet worker API serializes `setAttrs` calls internally.

---

### Implementation Checklist

| Task | What Changes | Lines Affected | Complexity |
|---|---|---|---|
| 2.1 | `+` → `-` | 245 | Trivial |
| 3.1–3.2 | Delete `+@{cm_tn_mod}` (×2) | 1190 | Trivial |
| 1.1–1.3 | Add `cm_init_mod` to trigger, getAttrs, formula | 134–141 | Low |
| 4.1 | New `power_pp_cost` → `power_pp_cost_value` worker | Insert after ~225 | Low |
| 4.2 | New `sheet:opened` PP cost recalc block | Insert after ~332 | Low |
| 5.1 | Add `<input type="hidden" ... essence_spent>` | After 915 | Trivial |
| 5.2 | `essence_total` → `essence_spent` in setAttrs | 235 | Trivial |
| 5.3 | New `essence_total` worker from `essence_spent` | Insert after ~237 | Low |
| 5.4 | Replace comment + rewrite mag worker with `essence_spent` | 53–58 | Low |
| 5.5 | New `sheet:opened` essence recalc block | Insert after 4.2's block | Low |
| 5.6 | Add `essence_spent` to scalarFields | 477 | Trivial |

**Total:** 11 edits in 1 file. No file creations. No CSS changes. No new roll templates.

---

Phase 1 Blueprint: 5 items, 11 tasks — all code blocks finalized with exact before/after, line numbers verified against current source.

---
---

## Phase 2: UX Fixes — Technical Blueprint

**5 items (P3b, P1a, P9, P3a, P5), 16 tasks. Changes across `roll20/sheet.html` and `roll20/sheet.css`.**
**Execution order:** P3b → P1a → P9 → P3a → P5 (as specified in L2)
**Phase 1 dependency:** P3a task 2.2 modifies the text→numeric sync worker added by Phase 1 P2 (task 4.1).

---

### P3b: Mutation BP Column Clips at 4 Digits (Tasks 3.1–3.2)

Two CSS edits — widen header and row BP column from `40px` to `55px`.

#### Task 3.1: Widen header BP column

**File:** `roll20/sheet.css` — Mutation header column widths, line ~769
**Current code:**
```css
.sheet-hdr-mutation-bp      { flex: 0 0 40px; text-align: center; }
```

**Blueprint — change `40px` to `55px`:**
```css
.sheet-hdr-mutation-bp      { flex: 0 0 55px; text-align: center; }
```

**Affected lines:** ~769 only.

#### Task 3.2: Widen row BP column

**File:** `roll20/sheet.css` — Mutation repeating row column widths, line ~776
**Current code:**
```css
.sheet-tab-panel-skills .repitem .sheet-mutation-bp      { flex: 0 0 40px; width: 40px; text-align: center; }
```

**Blueprint — change `40px` to `55px` in both flex and width:**
```css
.sheet-tab-panel-skills .repitem .sheet-mutation-bp      { flex: 0 0 55px; width: 55px; text-align: center; }
```

**Affected lines:** ~776 only.
**Cascade impact:** None — CSS only.

---

### P1a: Effect Text Boxes Clipping Content (Tasks 1.1–1.4)

CSS ellipsis overflow on mutation and power effect columns, plus `title` attributes on the HTML inputs for usability.

#### Task 1.1: Add ellipsis overflow to mutation effect

**File:** `roll20/sheet.css` — Mutation repeating row column widths, line ~777
**Current code:**
```css
.sheet-tab-panel-skills .repitem .sheet-mutation-effect   { flex: 2 1 120px; min-width: 0; }
```

**Blueprint — add overflow handling:**
```css
.sheet-tab-panel-skills .repitem .sheet-mutation-effect   { flex: 2 1 120px; min-width: 0; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
```

**Affected lines:** ~777 only.

#### Task 1.2: Add ellipsis overflow to power effect

**File:** `roll20/sheet.css` — Powers repeating row column widths, line ~824
**Current code:**
```css
.sheet-tab-panel-skills .repitem .sheet-power-effect  { flex: 2 1 120px; min-width: 0; }
```

**Blueprint — add overflow handling:**
```css
.sheet-tab-panel-skills .repitem .sheet-power-effect  { flex: 2 1 120px; min-width: 0; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
```

**Affected lines:** ~824 only.

#### Task 1.3: Add `title` attribute to mutation effect input

**File:** `roll20/sheet.html` — Mutation fieldset, line ~931
**Current code:**
```html
        <input type="text" name="attr_mutation_effect" placeholder="Effect" class="sheet-mutation-effect">
```

**Blueprint — add static `title`:**
```html
        <input type="text" name="attr_mutation_effect" placeholder="Effect" class="sheet-mutation-effect" title="View full effect text">
```

**Affected lines:** ~931 only.

#### Task 1.4: Add `title` attribute to power effect input

**File:** `roll20/sheet.html` — Adept powers fieldset, line ~960
**Current code:**
```html
        <input type="text" name="attr_power_effect" placeholder="Effect" class="sheet-power-effect">
```

**Blueprint — add static `title`:**
```html
        <input type="text" name="attr_power_effect" placeholder="Effect" class="sheet-power-effect" title="View full effect text">
```

**Affected lines:** ~960 only.
**Cascade impact:** None — CSS + HTML attributes only.
**Note:** Roll20 inputs cannot bind `title` dynamically to attribute values. The static hint is the practical maximum. The ellipsis treatment is the primary fix; `title` is supplementary.

---

### P9: Weapon Category Header Misalignment (Tasks 5.1–5.3)

Wrap both attack buttons in a container div matching the header "Roll" column width, then adjust button flex to share the container.

#### Task 5.1: Wrap attack buttons in roll group div

**File:** `roll20/sheet.html` — `repeating_weapons` fieldset, lines ~1244–1245
**Current code:**
```html
        <button type="roll" class="sheet-btn-attack" name="roll_btn_attack_ranged" value="&{template:attack} {{charname=@{char_name}}} {{rollname=Ranged: @{weapon_name}}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{range_band=?{Range Band|Short}}} {{tn=[[?{Range TN|4}+@{cm_tn_mod}]]}} {{successes=[[{(?{Skill dice|0}+?{Combat Pool dice|0})d6!!}>[[?{Range TN|4}+@{cm_tn_mod}]]]]}}">Rng</button>
        <button type="roll" class="sheet-btn-attack" name="roll_btn_attack_melee" value="&{template:attack} {{charname=@{char_name}}} {{rollname=Melee: @{weapon_name}}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{reach=@{weapon_reach}}} {{tn=[[?{TN|4}+@{cm_tn_mod}]]}} {{successes=[[{(?{Skill dice|0}+?{Combat Pool dice|0})d6!!}>[[?{TN|4}+@{cm_tn_mod}]]]]}}">Mel</button>
```

**Blueprint — wrap in container div:**
```html
        <div class="sheet-weapon-roll-group">
          <button type="roll" class="sheet-btn-attack" name="roll_btn_attack_ranged" value="&{template:attack} {{charname=@{char_name}}} {{rollname=Ranged: @{weapon_name}}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{range_band=?{Range Band|Short}}} {{tn=[[?{Range TN|4}+@{cm_tn_mod}]]}} {{successes=[[{(?{Skill dice|0}+?{Combat Pool dice|0})d6!!}>[[?{Range TN|4}+@{cm_tn_mod}]]]]}}">Rng</button>
          <button type="roll" class="sheet-btn-attack" name="roll_btn_attack_melee" value="&{template:attack} {{charname=@{char_name}}} {{rollname=Melee: @{weapon_name}}} {{weapon_name=@{weapon_name}}} {{damage_code=@{weapon_damage}}} {{power=@{weapon_power}}} {{reach=@{weapon_reach}}} {{tn=[[?{TN|4}+@{cm_tn_mod}]]}} {{successes=[[{(?{Skill dice|0}+?{Combat Pool dice|0})d6!!}>[[?{TN|4}+@{cm_tn_mod}]]]]}}">Mel</button>
        </div>
```

**Affected lines:** ~1244–1245 (wrapped with 3 new lines: opening div, re-indented buttons, closing div).
**Design note:** Mirrors the existing `.sheet-range-bands` wrapper pattern (line ~1238) — a flex container grouping related elements under a single header column.

#### Task 5.2: Add roll group CSS

**File:** `roll20/sheet.css` — insert after `.sheet-btn-attack` rule (after line ~1687)
**Insertion point:** After the closing `}` of the `.sheet-btn-attack` rule.

**Blueprint — new rule:**
```css
.sheet-tab-panel-gear .repitem .sheet-weapon-roll-group {
  display: flex;
  gap: 2px;
  flex: 0 0 70px;
}
```

**Design note:** `flex: 0 0 70px` matches `.sheet-hdr-weapon-roll { flex: 0 0 70px; }` (line ~1654), ensuring the row "Roll" column aligns with the header.

#### Task 5.3: Adjust attack button flex

**File:** `roll20/sheet.css` — `.sheet-btn-attack` rule, line ~1684
**Current code:**
```css
.sheet-tab-panel-gear .repitem .sheet-btn-attack {
  flex: 0 0 auto;
  padding: 2px 4px;
  font-size: 11px;
}
```

**Blueprint — change flex to share container:**
```css
.sheet-tab-panel-gear .repitem .sheet-btn-attack {
  flex: 1 1 auto;
  padding: 2px 4px;
  font-size: 11px;
}
```

**Affected lines:** ~1684 only (`flex: 0 0 auto` → `flex: 1 1 auto`).
**Design note:** With `flex: 1 1 auto`, both Rng and Mel buttons grow equally to share the 70px container (minus 2px gap = ~34px each). This replaces the previous behavior where each button was `flex: 0 0 auto` (~30px) and occupied separate flex slots in the fieldset row.

**Cascade impact:** None — HTML wrapper + CSS only.

---

### P3a: Adept Power Row Self-Deleting on Rapid Edits (Tasks 2.1–2.2)

Wrap `getSectionIDs` calls in `setTimeout(0)` to defer execution out of Roll20's creation event stack. Both `repeating_adept_powers` change handlers need this.

#### Task 2.1: Defer PP used summation handler

**File:** `roll20/sheet.html` — Layer 5d, lines ~206–216
**Current code:**
```js
on('change:repeating_adept_powers:power_pp_cost_value remove:repeating_adept_powers', function() {
  getSectionIDs('repeating_adept_powers', function(ids) {
    var fields = [];
    ids.forEach(function(id) { fields.push('repeating_adept_powers_' + id + '_power_pp_cost_value'); });
    getAttrs(fields, function(v) {
      var total = 0;
      ids.forEach(function(id) { total += parseFloat(v['repeating_adept_powers_' + id + '_power_pp_cost_value'] || 0); });
      setAttrs({ power_points_used: total });
    });
  });
});
```

**Blueprint — wrap body in `setTimeout(0)`:**
```js
on('change:repeating_adept_powers:power_pp_cost_value remove:repeating_adept_powers', function() {
  setTimeout(function() {
    getSectionIDs('repeating_adept_powers', function(ids) {
      var fields = [];
      ids.forEach(function(id) { fields.push('repeating_adept_powers_' + id + '_power_pp_cost_value'); });
      getAttrs(fields, function(v) {
        var total = 0;
        ids.forEach(function(id) { total += parseFloat(v['repeating_adept_powers_' + id + '_power_pp_cost_value'] || 0); });
        setAttrs({ power_points_used: total });
      });
    });
  }, 0);
});
```

**Affected lines:** ~206–216 (entire handler body re-indented inside `setTimeout`).

#### Task 2.2: Defer text→numeric sync handler (Phase 1 addition)

**File:** `roll20/sheet.html` — Layer 5d2 (added by Phase 1 P2 task 4.1, after line ~225)
**Input state (Phase 1 blueprint output):**
```js
// ─── Layer 5d2: PP Cost text→numeric sync ────────────────

on('change:repeating_adept_powers:power_pp_cost', function() {
  getAttrs(['power_pp_cost'], function(v) {
    setAttrs({ power_pp_cost_value: parseFloat(v.power_pp_cost) || 0 });
  });
});
```

**Blueprint — wrap body in `setTimeout(0)`:**
```js
// ─── Layer 5d2: PP Cost text→numeric sync ────────────────

on('change:repeating_adept_powers:power_pp_cost', function() {
  setTimeout(function() {
    getAttrs(['power_pp_cost'], function(v) {
      setAttrs({ power_pp_cost_value: parseFloat(v.power_pp_cost) || 0 });
    });
  }, 0);
});
```

**Note:** This modifies the worker that Phase 1 task 4.1 creates. The "before" state is Phase 1's output, not the current file state. The `setTimeout(0)` deferral is the only change — the referenced attrs, logic, and cascade behavior are identical.
**Cascade impact:** None — same attrs written, same cascade chain. Only timing changes (deferred by one event loop tick).

---

### P5: Skill Total Calculation Lag — Cascade Optimization (Tasks 4.1–4.5)

Merge Layer 4a (pool base computation) + Layer 4b (pool total computation) into single handlers with `{silent: true}`. The `calcPoolTotal` helper and calls remain for direct `pool_X_misc` edits.

#### Task 4.1: Merge spell pool base+total

**File:** `roll20/sheet.html` — Layer 4a spell, lines ~81–88
**Current code:**
```js
on('change:cha change:int change:wil', function() {
  getAttrs(['cha', 'int', 'wil'], function(v) {
    var cha = parseInt(v.cha, 10) || 0;
    var i   = parseInt(v.int, 10) || 0;
    var wil = parseInt(v.wil, 10) || 0;
    setAttrs({ pool_spell_base: Math.max(0, Math.floor((cha + i + wil) / 2)) });
  });
});
```

**Blueprint — read misc, compute both base and total, `{silent: true}`:**
```js
on('change:cha change:int change:wil', function() {
  getAttrs(['cha', 'int', 'wil', 'pool_spell_misc'], function(v) {
    var cha  = parseInt(v.cha, 10) || 0;
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var misc = parseInt(v.pool_spell_misc, 10) || 0;
    var base = Math.max(0, Math.floor((cha + i + wil) / 2));
    setAttrs({ pool_spell_base: base, pool_spell: Math.max(0, base + misc) }, {silent: true});
  });
});
```

**Affected lines:** ~81–88.

#### Task 4.2: Merge combat pool base+total

**File:** `roll20/sheet.html` — Layer 4a combat, lines ~90–97
**Current code:**
```js
on('change:dex change:int change:wil', function() {
  getAttrs(['dex', 'int', 'wil'], function(v) {
    var dex = parseInt(v.dex, 10) || 0;
    var i   = parseInt(v.int, 10) || 0;
    var wil = parseInt(v.wil, 10) || 0;
    setAttrs({ pool_combat_base: Math.max(0, Math.floor((dex + i + wil) / 2)) });
  });
});
```

**Blueprint — read misc, compute both base and total, `{silent: true}`:**
```js
on('change:dex change:int change:wil', function() {
  getAttrs(['dex', 'int', 'wil', 'pool_combat_misc'], function(v) {
    var dex  = parseInt(v.dex, 10) || 0;
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var misc = parseInt(v.pool_combat_misc, 10) || 0;
    var base = Math.max(0, Math.floor((dex + i + wil) / 2));
    setAttrs({ pool_combat_base: base, pool_combat: Math.max(0, base + misc) }, {silent: true});
  });
});
```

**Affected lines:** ~90–97.

#### Task 4.3: Merge control pool base+total

**File:** `roll20/sheet.html` — Layer 4a control, lines ~99–103
**Current code:**
```js
on('change:reaction', function() {
  getAttrs(['reaction'], function(v) {
    setAttrs({ pool_control_base: parseInt(v.reaction, 10) || 0 });
  });
});
```

**Blueprint — read misc, compute both base and total, `{silent: true}`:**
```js
on('change:reaction', function() {
  getAttrs(['reaction', 'pool_control_misc'], function(v) {
    var base = parseInt(v.reaction, 10) || 0;
    var misc = parseInt(v.pool_control_misc, 10) || 0;
    setAttrs({ pool_control_base: base, pool_control: Math.max(0, base + misc) }, {silent: true});
  });
});
```

**Affected lines:** ~99–103.

#### Task 4.4: Merge astral pool base+total

**File:** `roll20/sheet.html` — Layer 4a astral, lines ~105–112
**Current code:**
```js
on('change:int change:wil change:mag', function() {
  getAttrs(['int', 'wil', 'mag'], function(v) {
    var i   = parseInt(v.int, 10) || 0;
    var wil = parseInt(v.wil, 10) || 0;
    var mag = parseInt(v.mag, 10) || 0;
    setAttrs({ pool_astral_base: Math.max(0, Math.floor((i + wil + mag) / 3)) });
  });
});
```

**Blueprint — read misc, compute both base and total, `{silent: true}`:**
```js
on('change:int change:wil change:mag', function() {
  getAttrs(['int', 'wil', 'mag', 'pool_astral_misc'], function(v) {
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var mag  = parseInt(v.mag, 10) || 0;
    var misc = parseInt(v.pool_astral_misc, 10) || 0;
    var base = Math.max(0, Math.floor((i + wil + mag) / 3));
    setAttrs({ pool_astral_base: base, pool_astral: Math.max(0, base + misc) }, {silent: true});
  });
});
```

**Affected lines:** ~105–112.

**Design note (tasks 4.1–4.4):** The `calcPoolTotal` helper (lines ~116–130) and its four invocations are **retained unchanged**. They still listen on `change:pool_X_base change:pool_X_misc`. After this change:
- During attribute cascades: Layer 4a sets `pool_X_base` with `{silent: true}` → `calcPoolTotal` does NOT fire (desired — we already computed the total).
- On direct `pool_X_misc` edits: `calcPoolTotal` DOES fire (correct — the Layer 4a handler isn't involved, so `calcPoolTotal` is the only path to update the total).
- Nothing else in the codebase writes `pool_X_base` directly except the Layer 4a handlers, so this is safe.

#### Task 4.5: Add `{silent: true}` to `sheet:opened` skill recalc

**File:** `roll20/sheet.html` — `sheet:opened` handler, line ~330
**Current code:**
```js
      setAttrs(out);
```

**Blueprint — add `{silent: true}`:**
```js
      setAttrs(out, {silent: true});
```

**Affected lines:** ~330 only.
**Design note:** `skill_total` is display-only — no downstream listeners depend on it. Silencing eliminates N `change:repeating_skills:skill_total` events on every sheet open (one per skill row). This is purely a performance optimization with zero functional impact.

---

### Full Layer 4a Post-Phase 2 Blueprint

For clarity, here is the complete Layer 4a section structure after P5 tasks 4.1–4.4. Layer 4b (`calcPoolTotal` + calls) remains unchanged.

```js
// ─── Layer 4a: Dice Pool Bases ───────────────────────────

on('change:cha change:int change:wil', function() {
  getAttrs(['cha', 'int', 'wil', 'pool_spell_misc'], function(v) {
    var cha  = parseInt(v.cha, 10) || 0;
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var misc = parseInt(v.pool_spell_misc, 10) || 0;
    var base = Math.max(0, Math.floor((cha + i + wil) / 2));
    setAttrs({ pool_spell_base: base, pool_spell: Math.max(0, base + misc) }, {silent: true});
  });
});

on('change:dex change:int change:wil', function() {
  getAttrs(['dex', 'int', 'wil', 'pool_combat_misc'], function(v) {
    var dex  = parseInt(v.dex, 10) || 0;
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var misc = parseInt(v.pool_combat_misc, 10) || 0;
    var base = Math.max(0, Math.floor((dex + i + wil) / 2));
    setAttrs({ pool_combat_base: base, pool_combat: Math.max(0, base + misc) }, {silent: true});
  });
});

on('change:reaction', function() {
  getAttrs(['reaction', 'pool_control_misc'], function(v) {
    var base = parseInt(v.reaction, 10) || 0;
    var misc = parseInt(v.pool_control_misc, 10) || 0;
    setAttrs({ pool_control_base: base, pool_control: Math.max(0, base + misc) }, {silent: true});
  });
});

on('change:int change:wil change:mag', function() {
  getAttrs(['int', 'wil', 'mag', 'pool_astral_misc'], function(v) {
    var i    = parseInt(v.int, 10) || 0;
    var wil  = parseInt(v.wil, 10) || 0;
    var mag  = parseInt(v.mag, 10) || 0;
    var misc = parseInt(v.pool_astral_misc, 10) || 0;
    var base = Math.max(0, Math.floor((i + wil + mag) / 3));
    setAttrs({ pool_astral_base: base, pool_astral: Math.max(0, base + misc) }, {silent: true});
  });
});

// ─── Layer 4b: Dice Pool Totals ──────────────────────────
// (unchanged — handles direct pool_X_misc edits)

var calcPoolTotal = function(name) { ... };
calcPoolTotal('spell');
calcPoolTotal('combat');
calcPoolTotal('control');
calcPoolTotal('astral');
```

---

### Implementation Checklist

| Task | What Changes | File | Lines Affected | Complexity |
|---|---|---|---|---|
| 3.1 | Header BP `40px` → `55px` | `sheet.css` | ~769 | Trivial |
| 3.2 | Row BP `40px/40px` → `55px/55px` | `sheet.css` | ~776 | Trivial |
| 1.1 | Mutation effect ellipsis overflow | `sheet.css` | ~777 | Trivial |
| 1.2 | Power effect ellipsis overflow | `sheet.css` | ~824 | Trivial |
| 1.3 | Mutation effect `title` attr | `sheet.html` | ~931 | Trivial |
| 1.4 | Power effect `title` attr | `sheet.html` | ~960 | Trivial |
| 5.1 | Wrap attack buttons in roll group div | `sheet.html` | ~1244–1245 | Low |
| 5.2 | New `.sheet-weapon-roll-group` CSS | `sheet.css` | Insert after ~1687 | Low |
| 5.3 | Button flex `0 0 auto` → `1 1 auto` | `sheet.css` | ~1684 | Trivial |
| 2.1 | PP used handler `setTimeout(0)` | `sheet.html` | ~206–216 | Low |
| 2.2 | PP sync handler `setTimeout(0)` | `sheet.html` | Phase 1 output | Low |
| 4.1 | Merge spell pool base+total | `sheet.html` | ~81–88 | Medium |
| 4.2 | Merge combat pool base+total | `sheet.html` | ~90–97 | Medium |
| 4.3 | Merge control pool base+total | `sheet.html` | ~99–103 | Medium |
| 4.4 | Merge astral pool base+total | `sheet.html` | ~105–112 | Medium |
| 4.5 | Skill recalc `{silent: true}` | `sheet.html` | ~330 | Trivial |

**Total:** 16 edits across 2 files (`sheet.html` + `sheet.css`). 6 CSS edits, 10 HTML/JS edits. No file creations. No new roll templates.

---
---

## Phase 3: Data Entry Enhancements — Technical Blueprint

**3 items (P8, P10, P1b), 16 tasks. Changes across `roll20/sheet.html` and `roll20/sheet.css`.**
**Execution order:** P8 → P10 → P1b (as specified in L2)
**Phase 2 dependency:** P1b depends on Phase 2 P1a (effect text visible with ellipsis before adding chat button).

---

### P8: Weapon Type Select — Full Overhaul (Tasks 1.1–1.3)

Replace the 7-option flat `<select>` with a 17-option grouped `<select>` using `<optgroup>`, and widen the CSS column.

#### Task 1.1: Replace weapon type select

**File:** `roll20/sheet.html` — `repeating_weapons` fieldset, lines ~1223–1231
**Current code:**
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

**Blueprint — 17-option grouped select:**
```html
        <select class="sheet-weapon-type" name="attr_weapon_type">
          <optgroup label="Edged">
            <option value="edged-throwing">Edged — Throwing</option>
            <option value="edged-light">Edged — Light</option>
            <option value="edged-single">Edged — Single</option>
            <option value="edged-great">Edged — Great</option>
          </optgroup>
          <optgroup label="Blunt">
            <option value="blunt-throwing">Blunt — Throwing</option>
            <option value="blunt-light">Blunt — Light</option>
            <option value="blunt-single">Blunt — Single</option>
            <option value="blunt-great">Blunt — Great</option>
          </optgroup>
          <optgroup label="Other Melee">
            <option value="polearm">Polearm</option>
            <option value="whip">Whip</option>
            <option value="flail">Flail</option>
            <option value="staff">Staff</option>
            <option value="unarmed">Unarmed</option>
          </optgroup>
          <optgroup label="Ranged">
            <option value="bow">Bow</option>
            <option value="crossbow-hand">Crossbow — Hand</option>
            <option value="crossbow-medium">Crossbow — Medium</option>
            <option value="crossbow-heavy">Crossbow — Heavy</option>
          </optgroup>
        </select>
```

**Affected lines:** ~1223–1231 (9 lines replaced with 25 lines).
**Value format:** Lowercase hyphenated (e.g., `edged-light`, `crossbow-heavy`). This breaks backwards compatibility with old capitalized values (`"Edged"`, `"Club"`, etc.) — intentional per L2 plan. Existing characters show a blank select and re-select on next edit. No migration worker needed for 5 players.

#### Task 1.2: Widen weapon type CSS column

**File:** `roll20/sheet.css` — Weapon header + row column widths

**Header (line ~1646):**
**Current code:**
```css
.sheet-hdr-weapon-type    { flex: 0 0 80px; }
```

**Blueprint:**
```css
.sheet-hdr-weapon-type    { flex: 0 0 110px; }
```

**Row (line ~1658):**
**Current code:**
```css
.sheet-tab-panel-gear .repitem .sheet-weapon-type      { flex: 0 0 80px; width: 80px; }
```

**Blueprint:**
```css
.sheet-tab-panel-gear .repitem .sheet-weapon-type      { flex: 0 0 110px; width: 110px; }
```

**Affected lines:** ~1646 (header) and ~1658 (row).
**Design note:** 110px accommodates "Crossbow — Heavy" (~105px at 13px font) with minimal margin. The extra 30px comes from the flex layout's available space — all other columns use fixed `flex: 0 0 Npx`, so the `flex: 2 1 100px` name column absorbs the loss gracefully.

#### Task 1.3: Verify sync SECTIONS map (no code change)

**File:** `roll20/sheet.html` — Line ~438
**Current code:**
```js
    weapons:      ['weapon_name', 'weapon_type', 'weapon_modifiers', 'weapon_power',
                   'weapon_damage', 'weapon_conceal', 'weapon_reach', 'weapon_ep',
                   'weapon_range_short', 'weapon_range_medium',
                   'weapon_range_long', 'weapon_range_extreme'],
```

**Result:** `weapon_type` is already present in the SECTIONS map. **No change needed.**

**Cascade impact:** None — HTML select options only; the stored value changes format but no workers reference `weapon_type`.

---

### P10: Equipment Quantity Column (Tasks 2.1–2.6)

Add a quantity field to equipment rows and update the EP Total worker to multiply EP by quantity.

#### Task 2.1: Add quantity header column

**File:** `roll20/sheet.html` — Equipment header, line ~1253
**Current code:**
```html
      <div class="sheet-equipment-header">
        <span class="sheet-hdr-equip-name">Name</span>
        <span class="sheet-hdr-equip-desc">Description</span>
        <span class="sheet-hdr-equip-ep">EP</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Blueprint — add Qty span after Name:**
```html
      <div class="sheet-equipment-header">
        <span class="sheet-hdr-equip-name">Name</span>
        <span class="sheet-hdr-equip-qty">Qty</span>
        <span class="sheet-hdr-equip-desc">Description</span>
        <span class="sheet-hdr-equip-ep">EP</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Affected lines:** ~1253 (one span inserted after name).

#### Task 2.2: Add quantity input to equipment fieldset

**File:** `roll20/sheet.html` — `repeating_equipment` fieldset, line ~1259
**Current code:**
```html
      <fieldset class="repeating_equipment">
        <input type="text" class="sheet-equip-name" name="attr_equip_name" placeholder="Item Name">
        <input type="text" class="sheet-equip-desc" name="attr_equip_description" placeholder="Description">
        <input type="number" class="sheet-equip-ep" name="attr_equip_ep" value="0">
      </fieldset>
```

**Blueprint — add qty input after name:**
```html
      <fieldset class="repeating_equipment">
        <input type="text" class="sheet-equip-name" name="attr_equip_name" placeholder="Item Name">
        <input type="number" class="sheet-equip-qty" name="attr_equip_qty" value="1" min="1">
        <input type="text" class="sheet-equip-desc" name="attr_equip_description" placeholder="Description">
        <input type="number" class="sheet-equip-ep" name="attr_equip_ep" value="0">
      </fieldset>
```

**Affected lines:** ~1259 (one input inserted after name).

#### Task 2.3: Add header qty CSS

**File:** `roll20/sheet.css` — After `.sheet-hdr-equip-name` (line ~1155)
**Current code:**
```css
.sheet-hdr-equip-name { flex: 2 1 120px; }
.sheet-hdr-equip-desc { flex: 3 1 150px; }
.sheet-hdr-equip-ep   { flex: 0 0 40px; text-align: center; }
```

**Blueprint — insert qty after name:**
```css
.sheet-hdr-equip-name { flex: 2 1 120px; }
.sheet-hdr-equip-qty  { flex: 0 0 40px; text-align: center; }
.sheet-hdr-equip-desc { flex: 3 1 150px; }
.sheet-hdr-equip-ep   { flex: 0 0 40px; text-align: center; }
```

**Affected lines:** ~1155 (one line inserted).

#### Task 2.4: Add row qty CSS

**File:** `roll20/sheet.css` — After `.sheet-equip-name` row rule (line ~1159)
**Current code:**
```css
.sheet-tab-panel-gear .repitem .sheet-equip-name { flex: 2 1 120px; min-width: 0; }
.sheet-tab-panel-gear .repitem .sheet-equip-desc { flex: 3 1 150px; min-width: 0; }
.sheet-tab-panel-gear .repitem .sheet-equip-ep   { flex: 0 0 40px; width: 40px; text-align: center; }
```

**Blueprint — insert qty after name:**
```css
.sheet-tab-panel-gear .repitem .sheet-equip-name { flex: 2 1 120px; min-width: 0; }
.sheet-tab-panel-gear .repitem .sheet-equip-qty  { flex: 0 0 40px; width: 40px; text-align: center; }
.sheet-tab-panel-gear .repitem .sheet-equip-desc { flex: 3 1 150px; min-width: 0; }
.sheet-tab-panel-gear .repitem .sheet-equip-ep   { flex: 0 0 40px; width: 40px; text-align: center; }
```

**Affected lines:** ~1159 (one line inserted).
**Design note:** The 40px qty column matches the EP column width — both are short numeric fields. The `flex: 3 1 150px` description column absorbs the 46px loss (40px + 6px gap) gracefully.

#### Task 2.5: Update EP Total worker

**File:** `roll20/sheet.html` — Layer 5a EP Total worker, lines ~154–168
**Current code:**
```js
// EP Total — sums weapon_ep + equip_ep across repeating sections
on('change:repeating_weapons:weapon_ep remove:repeating_weapons change:repeating_equipment:equip_ep remove:repeating_equipment', function() {
  getSectionIDs('repeating_weapons', function(weaponIds) {
    getSectionIDs('repeating_equipment', function(equipIds) {
      var fields = [];
      weaponIds.forEach(function(id) { fields.push('repeating_weapons_' + id + '_weapon_ep'); });
      equipIds.forEach(function(id) { fields.push('repeating_equipment_' + id + '_equip_ep'); });
      getAttrs(fields, function(v) {
        var total = 0;
        weaponIds.forEach(function(id) { total += parseFloat(v['repeating_weapons_' + id + '_weapon_ep'] || 0); });
        equipIds.forEach(function(id) { total += parseFloat(v['repeating_equipment_' + id + '_equip_ep'] || 0); });
        setAttrs({ ep_total: total });
      });
    });
  });
});
```

**Blueprint — add `equip_qty` to trigger, fields, and multiply in summation:**
```js
// EP Total — sums weapon_ep + (equip_ep × equip_qty) across repeating sections
on('change:repeating_weapons:weapon_ep remove:repeating_weapons change:repeating_equipment:equip_ep change:repeating_equipment:equip_qty remove:repeating_equipment', function() {
  getSectionIDs('repeating_weapons', function(weaponIds) {
    getSectionIDs('repeating_equipment', function(equipIds) {
      var fields = [];
      weaponIds.forEach(function(id) { fields.push('repeating_weapons_' + id + '_weapon_ep'); });
      equipIds.forEach(function(id) {
        fields.push('repeating_equipment_' + id + '_equip_ep');
        fields.push('repeating_equipment_' + id + '_equip_qty');
      });
      getAttrs(fields, function(v) {
        var total = 0;
        weaponIds.forEach(function(id) { total += parseFloat(v['repeating_weapons_' + id + '_weapon_ep'] || 0); });
        equipIds.forEach(function(id) {
          var ep  = parseFloat(v['repeating_equipment_' + id + '_equip_ep'] || 0);
          var qty = parseFloat(v['repeating_equipment_' + id + '_equip_qty'] || 0) || 1;
          total += ep * qty;
        });
        setAttrs({ ep_total: total });
      });
    });
  });
});
```

**Affected lines:** ~154–168 (trigger, fields push, summation loop).
**Key changes:**
1. Trigger: Added `change:repeating_equipment:equip_qty`
2. Fields: Push both `equip_ep` and `equip_qty` for each equipment ID
3. Summation: `ep * qty` with `(qty || 0) || 1` guard — if `equip_qty` is undefined/empty (legacy rows), `parseFloat(undefined || 0)` = 0, then `0 || 1` = 1. This preserves existing EP totals without migration.

**Cascade impact:** `ep_total` is terminal — no downstream listeners.

#### Task 2.6: Add `equip_qty` to sync SECTIONS

**File:** `roll20/sheet.html` — SECTIONS map, line ~441
**Current code:**
```js
    equipment:    ['equip_name', 'equip_description', 'equip_ep'],
```

**Blueprint — add `equip_qty`:**
```js
    equipment:    ['equip_name', 'equip_qty', 'equip_description', 'equip_ep'],
```

**Affected lines:** ~441 only.

---

### P1b: Effect "Send to Chat" Buttons (Tasks 3.1–3.7)

Add chat buttons to mutation and power rows, plus a new `desc` roll template to display the effect text cleanly.

#### Task 3.1: Add mutation effect chat button

**File:** `roll20/sheet.html` — Mutation fieldset, line ~931 (after `mutation_effect` input)
**Current code (after Phase 2 P1a task 1.3 adds `title`):**
```html
        <input type="text" name="attr_mutation_effect" placeholder="Effect" class="sheet-mutation-effect" title="View full effect text">
      </fieldset>
```

**Blueprint — add button before `</fieldset>`:**
```html
        <input type="text" name="attr_mutation_effect" placeholder="Effect" class="sheet-mutation-effect" title="View full effect text">
        <button type="roll" name="roll_btn_mutation_effect" class="sheet-btn-chat-effect" value="&{template:desc} {{charname=@{char_name}}} {{rollname=@{mutation_name}}} {{desc=@{mutation_effect}}}" title="Send effect to chat">&#x1F4AC;</button>
      </fieldset>
```

**Affected lines:** ~931 (one button inserted before `</fieldset>`).
**Note:** The "Current code" above reflects Phase 2 P1a's output (added `title` attribute). At time of Phase 3 implementation, Phase 2 will already be applied.

#### Task 3.2: Add power effect chat button

**File:** `roll20/sheet.html` — Adept powers fieldset, line ~960 (after `power_effect` input)
**Current code (after Phase 2 P1a task 1.4 adds `title`):**
```html
        <input type="text" name="attr_power_effect" placeholder="Effect" class="sheet-power-effect" title="View full effect text">
      </fieldset>
```

**Blueprint — add button before `</fieldset>`:**
```html
        <input type="text" name="attr_power_effect" placeholder="Effect" class="sheet-power-effect" title="View full effect text">
        <button type="roll" name="roll_btn_power_effect" class="sheet-btn-chat-effect" value="&{template:desc} {{charname=@{char_name}}} {{rollname=@{power_name}}} {{desc=@{power_effect}}}" title="Send effect to chat">&#x1F4AC;</button>
      </fieldset>
```

**Affected lines:** ~960 (one button inserted before `</fieldset>`).

#### Task 3.3: Add chat effect button CSS

**File:** `roll20/sheet.css` — After power effect row CSS (after line ~824)
**Insertion point:** After the `.sheet-power-effect` rule, before the `/* Shared summary title span */` comment (line ~826).

**Blueprint — new rule:**
```css
/* Chat effect button — shared by mutations + adept powers */
.sheet-btn-chat-effect {
  flex: 0 0 24px;
  width: 24px;
  height: 24px;
  padding: 0;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid #cccccc;
  background: #f9f9f9;
  text-align: center;
  line-height: 24px;
}
```

**Affected lines:** Insert after ~824 (new block).

#### Task 3.4: Add chat button header spacers

**File:** `roll20/sheet.html` — Mutation header (line ~918) and Power header (line ~948)

**Mutation header — current code:**
```html
      <div class="sheet-mutations-header">
        <span class="sheet-hdr-mutation-name">Name</span>
        <span class="sheet-hdr-mutation-level">Level</span>
        <span class="sheet-hdr-mutation-essence">Essence</span>
        <span class="sheet-hdr-mutation-bp">BP</span>
        <span class="sheet-hdr-mutation-effect">Effect</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Blueprint — add chat header before spacer:**
```html
      <div class="sheet-mutations-header">
        <span class="sheet-hdr-mutation-name">Name</span>
        <span class="sheet-hdr-mutation-level">Level</span>
        <span class="sheet-hdr-mutation-essence">Essence</span>
        <span class="sheet-hdr-mutation-bp">BP</span>
        <span class="sheet-hdr-mutation-effect">Effect</span>
        <span class="sheet-hdr-chat">&#x1F4AC;</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Power header — current code:**
```html
      <div class="sheet-powers-header">
        <span class="sheet-hdr-power-name">Name</span>
        <span class="sheet-hdr-power-level">Level</span>
        <span class="sheet-hdr-power-cost">PP Cost</span>
        <span class="sheet-hdr-power-effect">Effect</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Blueprint — add chat header before spacer:**
```html
      <div class="sheet-powers-header">
        <span class="sheet-hdr-power-name">Name</span>
        <span class="sheet-hdr-power-level">Level</span>
        <span class="sheet-hdr-power-cost">PP Cost</span>
        <span class="sheet-hdr-power-effect">Effect</span>
        <span class="sheet-hdr-chat">&#x1F4AC;</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
```

**Affected lines:** ~918 (mutation header) and ~948 (power header) — one span inserted in each.

#### Task 3.5: Add header chat column CSS

**File:** `roll20/sheet.css` — After the chat effect button CSS (task 3.3 insertion)

**Blueprint — new rule:**
```css
.sheet-hdr-chat { flex: 0 0 24px; text-align: center; font-size: 12px; }
```

**Affected lines:** Insert after task 3.3's block.

#### Task 3.6: Add description roll template

**File:** `roll20/sheet.html` — After the `spell` rolltemplate (after line ~1448)
**Insertion point:** After `</rolltemplate>` closing tag of the spell template.

**Blueprint — new roll template:**
```html

<rolltemplate class="sheet-rolltemplate-desc">
  <div class="sheet-template-wrapper">
    <div class="sheet-template-header sheet-header-desc">
      {{charname}} — {{rollname}}
    </div>
    <div class="sheet-template-body">
      <div class="sheet-template-desc">
        {{desc}}
      </div>
    </div>
  </div>
</rolltemplate>
```

**Design note:** Minimal template — just header + description text. No TN, successes, or conditional blocks. The `sheet-template-desc` class gets `white-space: pre-wrap` so multi-word effect text wraps naturally in chat. Matches the structural pattern of existing templates (wrapper → header → body).

#### Task 3.7: Add description template CSS

**File:** `roll20/sheet.css` — Roll template CSS section

**Three changes:**

**A) Outer wrapper rule (after `.sheet-rolltemplate-spell .sheet-template-header`, line ~1335):**
**Insertion point:** After the spell header rule block.

**Blueprint — new rules:**
```css

.sheet-rolltemplate-desc {
  display: block;
  border: 1px solid #2a3a2a;
  font-family: sans-serif;
  font-size: 13px;
  width: 100%;
  box-sizing: border-box;
  min-width: 200px;
}

.sheet-rolltemplate-desc .sheet-template-header {
  background-color: #2a3a2a;
  color: #ffffff;
  padding: 6px 10px;
  font-weight: bold;
  font-size: 14px;
}
```

**B) Add `desc` to shared body/row/label/value selector lists (lines ~1338–1370):**

Each grouped selector list currently has 3 templates (skill, attack, spell). Add `desc` as a 4th.

**Current (body):**
```css
.sheet-rolltemplate-skill .sheet-template-body,
.sheet-rolltemplate-attack .sheet-template-body,
.sheet-rolltemplate-spell .sheet-template-body {
  padding: 2px 0;
}
```

**Blueprint:**
```css
.sheet-rolltemplate-skill .sheet-template-body,
.sheet-rolltemplate-attack .sheet-template-body,
.sheet-rolltemplate-spell .sheet-template-body,
.sheet-rolltemplate-desc .sheet-template-body {
  padding: 2px 0;
}
```

**Current (row):**
```css
.sheet-rolltemplate-skill .sheet-template-row,
.sheet-rolltemplate-attack .sheet-template-row,
.sheet-rolltemplate-spell .sheet-template-row {
  display: flex;
  align-items: baseline;
  padding: 3px 10px;
  border-bottom: 1px solid #cccccc;
}
```

**Blueprint:**
```css
.sheet-rolltemplate-skill .sheet-template-row,
.sheet-rolltemplate-attack .sheet-template-row,
.sheet-rolltemplate-spell .sheet-template-row,
.sheet-rolltemplate-desc .sheet-template-row {
  display: flex;
  align-items: baseline;
  padding: 3px 10px;
  border-bottom: 1px solid #cccccc;
}
```

**Current (label):**
```css
.sheet-rolltemplate-skill .sheet-template-label,
.sheet-rolltemplate-attack .sheet-template-label,
.sheet-rolltemplate-spell .sheet-template-label {
  font-weight: bold;
  color: #555555;
  min-width: 80px;
  flex-shrink: 0;
  font-size: 12px;
}
```

**Blueprint:**
```css
.sheet-rolltemplate-skill .sheet-template-label,
.sheet-rolltemplate-attack .sheet-template-label,
.sheet-rolltemplate-spell .sheet-template-label,
.sheet-rolltemplate-desc .sheet-template-label {
  font-weight: bold;
  color: #555555;
  min-width: 80px;
  flex-shrink: 0;
  font-size: 12px;
}
```

**Current (value):**
```css
.sheet-rolltemplate-skill .sheet-template-value,
.sheet-rolltemplate-attack .sheet-template-value,
.sheet-rolltemplate-spell .sheet-template-value {
  flex: 1;
  font-size: 13px;
}
```

**Blueprint:**
```css
.sheet-rolltemplate-skill .sheet-template-value,
.sheet-rolltemplate-attack .sheet-template-value,
.sheet-rolltemplate-spell .sheet-template-value,
.sheet-rolltemplate-desc .sheet-template-value {
  flex: 1;
  font-size: 13px;
}
```

**C) Unique desc text style (after the shared selector lists, line ~1400):**

**Blueprint — new rule:**
```css
/* Description text block — desc template only */
.sheet-rolltemplate-desc .sheet-template-desc {
  padding: 4px 8px;
  white-space: pre-wrap;
  font-size: 13px;
}
```

**Design note:** The `#2a3a2a` header color is a dark olive-green, distinct from:
- skill: `#1a1a2e` (dark navy)
- attack: `#3a1c1c` (dark crimson)
- spell: `#1c3a5e` (dark blue)

This provides visual differentiation in chat — players immediately recognize a description output vs. a roll result.

---

### Implementation Checklist

| Task | What Changes | File | Lines Affected | Complexity |
|---|---|---|---|---|
| 1.1 | Replace 7-option select with 17-option grouped select | `sheet.html` | ~1223–1231 | Low |
| 1.2 | Widen weapon type CSS `80px` → `110px` | `sheet.css` | ~1646, ~1658 | Trivial |
| 1.3 | Verify `weapon_type` in SECTIONS (no change) | `sheet.html` | ~438 | None |
| 2.1 | Add equipment qty header span | `sheet.html` | ~1253 | Trivial |
| 2.2 | Add equipment qty input | `sheet.html` | ~1259 | Trivial |
| 2.3 | Add header qty CSS | `sheet.css` | After ~1155 | Trivial |
| 2.4 | Add row qty CSS | `sheet.css` | After ~1159 | Trivial |
| 2.5 | Update EP Total worker (trigger + qty × ep) | `sheet.html` | ~154–168 | Medium |
| 2.6 | Add `equip_qty` to SECTIONS map | `sheet.html` | ~441 | Trivial |
| 3.1 | Add mutation chat button | `sheet.html` | ~931 | Low |
| 3.2 | Add power chat button | `sheet.html` | ~960 | Low |
| 3.3 | Add chat button CSS | `sheet.css` | After ~824 | Low |
| 3.4 | Add chat header spacers (×2 headers) | `sheet.html` | ~918, ~948 | Trivial |
| 3.5 | Add header chat column CSS | `sheet.css` | After 3.3 | Trivial |
| 3.6 | Add `desc` roll template HTML | `sheet.html` | After ~1448 | Low |
| 3.7 | Add `desc` template CSS (wrapper + shared selectors + desc style) | `sheet.css` | ~1335, ~1338–1370, ~1400 | Medium |

**Total:** 16 tasks across 2 files (`sheet.html` + `sheet.css`). 1 new roll template. 1 new repeating field (`equip_qty`). 17 new weapon type options. No new workers (EP Total modified only).

---
---

## Phase 4: Skill Specialization — Technical Blueprint

**1 item (P4), 9 tasks. All changes in `roll20/sheet.html` (HTML + JS). No CSS changes.**
**Governing design:** ADR-002 (Skill Specialization Model)

---

### P4: Spec Checkbox → Sub-Skill Creation Flow (Tasks 4.1–4.9)

#### Task 4.1: Add `skill_parent_id` hidden input

**File:** `roll20/sheet.html` — `repeating_skills` fieldset, after spec checkbox (line ~898)
**Current code (lines ~897–908):**
```html
        <input type="checkbox" name="attr_skill_spec" value="1" class="sheet-skill-spec">
        <input type="number" name="attr_skill_base" value="0" class="sheet-skill-base">
        <input type="number" name="attr_skill_foci" value="0" class="sheet-skill-foci">
        <input type="number" name="attr_skill_misc" value="0" class="sheet-skill-misc">
        <input type="number" name="attr_skill_total" value="0" readonly class="sheet-skill-total">
```

**Blueprint — add hidden parent_id and child_id after spec checkbox:**
```html
        <input type="checkbox" name="attr_skill_spec" value="1" class="sheet-skill-spec">
        <input type="hidden" name="attr_skill_parent_id" value="">
        <input type="hidden" name="attr_skill_child_id" value="">
        <input type="number" name="attr_skill_base" value="0" class="sheet-skill-base">
        <input type="number" name="attr_skill_foci" value="0" class="sheet-skill-foci">
        <input type="number" name="attr_skill_misc" value="0" class="sheet-skill-misc">
        <input type="number" name="attr_skill_total" value="0" readonly class="sheet-skill-total">
```

**Affected lines:** ~898 (two hidden inputs inserted after spec checkbox).
**Note:** Tasks 4.1 and 4.2 are combined here — both inputs in one insertion. Hidden inputs don't render in the flex row layout.

#### Task 4.3: Add cross-ref fields to SECTIONS map

**File:** `roll20/sheet.html` — SECTIONS map, line ~429
**Current code:**
```js
    skills:       ['skill_name', 'skill_linked_attr', 'skill_general', 'skill_spec',
                   'skill_base', 'skill_foci', 'skill_misc', 'skill_total'],
```

**Blueprint — add `skill_parent_id`, `skill_child_id`:**
```js
    skills:       ['skill_name', 'skill_linked_attr', 'skill_general', 'skill_spec',
                   'skill_base', 'skill_foci', 'skill_misc', 'skill_total',
                   'skill_parent_id', 'skill_child_id'],
```

**Affected lines:** ~429–430 (array extended to 3 lines).

#### Task 4.4 + 4.5: New spec check/uncheck handler

**File:** `roll20/sheet.html` — Insert as new Layer 5c2 block after the skill total worker, before Layer 5d.
**Insertion point:** After line ~196 (closing `});` of the Layer 5c skill total worker), before line ~198 (`// ─── Layer 5d:` comment).

**Blueprint — new worker:**
```js

// ─── Layer 5c2: Skill Specialization (ADR-002) ──────────

on('change:repeating_skills:skill_spec', function(eventInfo) {
  var match = (eventInfo.sourceAttribute || '').match(/repeating_skills_([^_]+)_skill_spec/);
  if (!match) return;
  var parentId = match[1];
  var p = 'repeating_skills_' + parentId + '_';

  getAttrs([p + 'skill_spec', p + 'skill_name', p + 'skill_base', p + 'skill_linked_attr',
            p + 'skill_general', p + 'skill_parent_id', p + 'skill_child_id'], function(v) {
    var spec = v[p + 'skill_spec'];
    var base = parseInt(v[p + 'skill_base'], 10) || 0;

    if (spec === '1') {
      // Guards: prevent invalid specialization
      if (v[p + 'skill_parent_id']) {
        setAttrs(_.object([[p + 'skill_spec', '0']]), {silent: true});
        return;
      }
      if (v[p + 'skill_child_id']) {
        setAttrs(_.object([[p + 'skill_spec', '0']]), {silent: true});
        return;
      }
      if (base < 1) {
        setAttrs(_.object([[p + 'skill_spec', '0']]), {silent: true});
        return;
      }

      // Create child specialization
      var newId = generateRowID();
      var cp = 'repeating_skills_' + newId + '_';
      var out = {};
      // Child row
      out[cp + 'skill_name']        = (v[p + 'skill_name'] || '') + ' (Spec)';
      out[cp + 'skill_base']        = base + 1;
      out[cp + 'skill_linked_attr'] = v[p + 'skill_linked_attr'] || 'body';
      out[cp + 'skill_general']     = v[p + 'skill_general'] || 'Active';
      out[cp + 'skill_parent_id']   = parentId;
      out[cp + 'skill_spec']        = '0';
      out[cp + 'skill_foci']        = 0;
      out[cp + 'skill_misc']        = 0;
      // Parent update
      out[p + 'skill_base']         = base - 1;
      out[p + 'skill_child_id']     = newId;
      setAttrs(out);
    } else {
      // Uncheck: restore parent + remove child
      var childId = v[p + 'skill_child_id'];
      if (!childId) return;

      var out = {};
      out[p + 'skill_base']     = base + 1;
      out[p + 'skill_child_id'] = '';
      setAttrs(out, {}, function() {
        removeRepeatingRow('repeating_skills_' + childId);
      });
    }
  });
});
```

**Design notes:**
1. **`eventInfo.sourceAttribute` regex:** Extracts the row ID from the fully qualified attribute name. This is the standard Roll20 pattern for identifying which row triggered a repeating section event.
2. **Guard order:** Child guard → duplicate guard → base guard. The child guard (`skill_parent_id` non-empty) runs first because it's the cheapest check and prevents the most dangerous failure (infinite grandchild chains).
3. **`_.object([[key, val]])`:** Roll20's sheet worker sandbox includes Underscore.js. `_.object()` creates a single-key object from key/value pairs — cleaner than a temp variable for the guard revert.
4. **On-uncheck `setAttrs` callback:** `removeRepeatingRow` runs in the `setAttrs` callback to ensure parent base is restored before the child is deleted. If `removeRepeatingRow` were first and execution interrupted, the parent would lose a point permanently. The reverse failure (child lingers) is recovered by `sheet:opened` orphan cleanup.
5. **Child `skill_spec: '0'`:** Explicitly set so the child row's checkbox starts unchecked. Combined with the `skill_parent_id` guard, this double-prevents grandchild creation.
6. **Child `skill_foci: 0` and `skill_misc: 0`:** Explicitly initialized so the skill total worker computes correctly on the new row.

#### Tasks 4.6–4.9: Rewrite `sheet:opened` skill block with orphan cleanup

**File:** `roll20/sheet.html` — Inside `on('sheet:opened', ...)`, the skill totals block (lines ~315–332)
**Note:** Current code shown is pre-Phase 2. After Phase 2 P5 task 4.5, the `setAttrs(out)` line will already include `{silent: true}`. This is a full-block replacement — match on block boundaries, not exact `setAttrs` call.
**Current code:**
```js
  // Recalculate all skill totals on sheet open
  getSectionIDs('repeating_skills', function(ids) {
    var fields = [];
    ids.forEach(function(id) {
      var p = 'repeating_skills_' + id + '_';
      fields.push(p + 'skill_base', p + 'skill_foci', p + 'skill_misc');
    });
    getAttrs(fields, function(v) {
      var out = {};
      ids.forEach(function(id) {
        var p = 'repeating_skills_' + id + '_';
        out[p + 'skill_total'] =
          (parseInt(v[p + 'skill_base'], 10) || 0) +
          (parseInt(v[p + 'skill_foci'], 10) || 0) +
          (parseInt(v[p + 'skill_misc'], 10) || 0);
      });
      setAttrs(out);
    });
  });
```

**Blueprint — add cross-ref fields + orphan cleanup:**
```js
  // Recalculate all skill totals + orphan cleanup on sheet open
  getSectionIDs('repeating_skills', function(ids) {
    var fields = [];
    ids.forEach(function(id) {
      var p = 'repeating_skills_' + id + '_';
      fields.push(p + 'skill_base', p + 'skill_foci', p + 'skill_misc',
                  p + 'skill_parent_id', p + 'skill_child_id', p + 'skill_spec');
    });
    getAttrs(fields, function(v) {
      var out = {};
      var validIds = {};
      ids.forEach(function(id) { validIds[id] = true; });
      var orphanChildren = {};

      // Pass 1: Detect orphans
      ids.forEach(function(id) {
        var p = 'repeating_skills_' + id + '_';
        var childId  = v[p + 'skill_child_id'] || '';
        var parentId = v[p + 'skill_parent_id'] || '';

        // Parent→child: child deleted externally
        if (childId && !validIds[childId]) {
          out[p + 'skill_child_id'] = '';
          out[p + 'skill_spec']     = '0';
          out[p + 'skill_base']     = (parseInt(v[p + 'skill_base'], 10) || 0) + 1;
        }

        // Child→parent: parent deleted externally
        if (parentId && !validIds[parentId]) {
          orphanChildren[id] = true;
        }
      });

      // Pass 2: Remove orphaned children
      Object.keys(orphanChildren).forEach(function(id) {
        removeRepeatingRow('repeating_skills_' + id);
      });

      // Pass 3: Recalculate skill totals for remaining rows
      ids.forEach(function(id) {
        if (orphanChildren[id]) return;
        var p = 'repeating_skills_' + id + '_';
        var base = out[p + 'skill_base'] !== undefined
                 ? out[p + 'skill_base']
                 : (parseInt(v[p + 'skill_base'], 10) || 0);
        out[p + 'skill_total'] = base
          + (parseInt(v[p + 'skill_foci'], 10) || 0)
          + (parseInt(v[p + 'skill_misc'], 10) || 0);
      });

      setAttrs(out, {silent: true});
    });
  });
```

**Key changes from current code:**
1. **Fields array (task 4.6):** Added `skill_parent_id`, `skill_child_id`, `skill_spec` to the push list.
2. **`validIds` set (task 4.7):** Built from `ids` array — used to check if a referenced row still exists.
3. **Parent→child orphan fix (task 4.7):** If `skill_child_id` points to a deleted row → clear child ref, uncheck spec, restore `base + 1`.
4. **Child→parent orphan removal (task 4.8):** If `skill_parent_id` points to a deleted row → `removeRepeatingRow`. Collected in `orphanChildren` set and removed in a separate loop.
5. **Skill total recalc (task 4.9):** Skips orphaned children (`if (orphanChildren[id]) return`). Uses orphan-fixed `base` from `out` when available (the `out[p + 'skill_base'] !== undefined` check) so restored parents get correct totals.
6. **`{silent: true}` on final `setAttrs`:** Carried forward from Phase 2 P5 task 4.5 — skill totals are display-only with no downstream cascade.

**Execution order within `sheet:opened` block:**
1. Gather fields (including cross-refs)
2. Build `validIds` set
3. Pass 1: Detect all orphans, fix parent→child in `out`, collect child→parent for removal
4. Pass 2: Remove orphaned children via `removeRepeatingRow`
5. Pass 3: Compute `skill_total` for remaining (non-orphaned) rows
6. Single `setAttrs(out, {silent: true})`

**Note on `removeRepeatingRow` timing:** Called before `setAttrs(out)`. This means the removed rows' attrs set in `out` (if any phantom refs existed) would be no-ops — Roll20 ignores `setAttrs` for deleted rows. The `orphanChildren` filter in Pass 3 prevents writing to them anyway, so this is belt-and-suspenders.

---

### Implementation Checklist

| Task | What Changes | Lines Affected | Complexity |
|---|---|---|---|
| 4.1–4.2 | Add `skill_parent_id` + `skill_child_id` hidden inputs | ~898 | Trivial |
| 4.3 | Add cross-ref fields to SECTIONS map | ~429–430 | Trivial |
| 4.4–4.5 | New spec check/uncheck handler (Layer 5c2) | Insert after ~196 | High |
| 4.6 | Add cross-ref fields to `sheet:opened` skill block | ~318–320 | Low |
| 4.7 | Orphan cleanup — parent→child direction | ~322–328 | Medium |
| 4.8 | Orphan cleanup — child→parent direction | Same block | Medium |
| 4.9 | Skill total recalc excludes orphans | ~325–330 | Low |

**Total:** 3 logical edits in 1 file (`sheet.html`). 2 hidden input additions, 1 SECTIONS array extension, 1 new worker (~55 lines), 1 rewritten `sheet:opened` skill block (~35 lines). No CSS changes. No new roll templates.

---

### Cascade Impact

```
skill_spec ──→ skill_base (parent: -1; child: parent_base+1) [via new 5c2 handler]
skill_base ──→ skill_total [via existing Layer 5c worker]
sheet:opened ──→ orphan cleanup ──→ skill_base / removeRepeatingRow

Cross-ref fields (skill_parent_id, skill_child_id) are terminal — no listeners.
Guard reverts use {silent: true} — no feedback loops.
```

---

## Phase 5: Creature Systems — Technical Blueprint

**Items:** G4 (Animal Companions), G5 (Companion Attack Rolls), P12 (Spirit Summon + Attack Rolls)
**Execution order:** G4 → G5 (button lives inside G4's fieldset) → P12
**Files touched:** `roll20/sheet.html` (HTML + JS), `roll20/sheet.css`
**Governing design:** ADR-003 (Animal Companion / Critter Stat Block Model)

> **Cross-phase note:** Phase 4 rewrites the `sheet:opened` skill block with orphan cleanup logic. The companion reaction recalc (task 5.8) inserts AFTER the Phase 4 rewritten skill block, inside the same `sheet:opened` handler.

---

### G4: Animal Companions Section (Bio Tab)

#### Task 5.1–5.3: Companion Section HTML (Bio Tab)

Insert a new "Animal Companions" section between the milestones fieldset and the bio-section closing div. Includes: section title, flex header row, `repeating_companions` fieldset with 8 editable stat inputs, 1 readonly reaction, CM severity select, and attack roll button (G5 task 5.9 — combined here because button is part of fieldset).

**Current (~line 1319–1320):**
```html
      </fieldset>
    </div>
```

**After:**
```html
      </fieldset>

      <h3 class="sheet-section-title">Animal Companions</h3>
      <div class="sheet-companions-header">
        <span class="sheet-hdr-comp-name">Name</span>
        <span class="sheet-hdr-comp-stat">B</span>
        <span class="sheet-hdr-comp-stat">Q</span>
        <span class="sheet-hdr-comp-stat">S</span>
        <span class="sheet-hdr-comp-stat">C</span>
        <span class="sheet-hdr-comp-stat">I</span>
        <span class="sheet-hdr-comp-stat">W</span>
        <span class="sheet-hdr-comp-stat">E</span>
        <span class="sheet-hdr-comp-stat">R</span>
        <span class="sheet-hdr-comp-stat">Rcn</span>
        <span class="sheet-hdr-comp-cm">CM</span>
        <span class="sheet-hdr-comp-atk">Atk</span>
        <span class="sheet-hdr-spacer"></span>
      </div>
      <fieldset class="repeating_companions">
        <input type="text" name="attr_comp_name" placeholder="Name" class="sheet-comp-name">
        <input type="number" name="attr_comp_b" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_q" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_s" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_c" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_i" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_w" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_e" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_r" value="0" class="sheet-comp-stat">
        <input type="number" name="attr_comp_reaction" value="0" readonly class="sheet-comp-reaction">
        <select name="attr_comp_cm_level" class="sheet-comp-cm-level">
          <option value="0">None</option>
          <option value="1">Light (+1)</option>
          <option value="2">Moderate (+2)</option>
          <option value="3">Serious (+3)</option>
        </select>
        <button type="roll" name="roll_btn_comp_attack" class="sheet-comp-attack" value="&{template:attack} {{charname=@{char_name}}} {{rollname=@{comp_name} Attack}} {{weapon_name=@{comp_name}}} {{damage_code=?{Damage Code|@{comp_s}M Physical}}} {{power=@{comp_s}}} {{tn=[[?{Target Number|4}+@{comp_cm_level}]]}} {{successes=[[{(?{Dice|@{comp_reaction}})d6!!}>[[?{Target Number|4}+@{comp_cm_level}]]]]}}" title="Companion attack">&#x1F43E;</button>
      </fieldset>
    </div>
```

**Design notes:**
- The `</fieldset>` on the first line is the existing milestones fieldset close (anchor context).
- The `</div>` on the last line is the existing `.sheet-bio-section` close (unchanged).
- Attack button (task 5.9) is embedded inside the fieldset so it can reference row-level `@{comp_*}` attributes.
- `@{comp_cm_level}` is used in TN (row-level creature penalty), NOT `@{cm_tn_mod}` (player penalty). This is the ADR-003 isolation requirement.
- Dice default to `@{comp_reaction}` with prompt override. Follows same `(?{Dice|@{default}})` pattern as attribute roll buttons.
- Paw print emoji `&#x1F43E;` (🐾) as button label.
- `comp_reaction` is `readonly` — computed by the Layer 5g worker (task 5.7).

---

#### Task 5.4: Add `companions` to SECTIONS Sync Map

**Current (~line 444–446):**
```js
    milestones:   ['milestone_trial', 'milestone_tier1', 'milestone_tier2',
                   'milestone_tier3', 'milestone_current']
  };
```

**After:**
```js
    milestones:   ['milestone_trial', 'milestone_tier1', 'milestone_tier2',
                   'milestone_tier3', 'milestone_current'],
    companions:   ['comp_name', 'comp_b', 'comp_q', 'comp_s', 'comp_c',
                   'comp_i', 'comp_w', 'comp_e', 'comp_r',
                   'comp_reaction', 'comp_cm_level']
  };
```

**Design notes:**
- Trailing comma added to `milestones` entry.
- `comp_reaction` included — it's computed but should be synced so the companion app can read it.
- `comp_cm_level` included — it's user-set and must persist.
- Attack button name (`roll_btn_comp_attack`) is NOT included — roll buttons aren't persisted attributes.

---

#### Tasks 5.5–5.6: Companion CSS (Header + Row)

Insert after the milestones CSS block (SECTION 14: Bio Tab), before SECTION 20. The milestones row CSS ends with `.sheet-milestone-current` at ~line 1833.

**Current (~line 1833–1836):**
```css
.sheet-milestone-current { flex: 0 0 50px; text-align: center; }

/* ===================================================
 * SECTION 20: SHEET ROOT
```

**After:**
```css
.sheet-milestone-current { flex: 0 0 50px; text-align: center; }

/* --- Bio Tab: Animal Companions repeating section --- */
.sheet-companions-header {
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

.sheet-hdr-comp-name { flex: 1 1 auto; }
.sheet-hdr-comp-stat { flex: 0 0 38px; text-align: center; }
.sheet-hdr-comp-cm   { flex: 0 0 90px; text-align: center; }
.sheet-hdr-comp-atk  { flex: 0 0 36px; text-align: center; }

.sheet-comp-name     { flex: 1 1 auto; min-width: 0; }
.sheet-comp-stat     { flex: 0 0 38px; width: 38px; text-align: center; }
.sheet-comp-reaction {
  flex: 0 0 38px;
  width: 38px;
  text-align: center;
  font-weight: bold;
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
}
.sheet-comp-cm-level { flex: 0 0 90px; }
.sheet-comp-attack   { flex: 0 0 36px; cursor: pointer; }

/* ===================================================
 * SECTION 20: SHEET ROOT
```

**Design notes:**
- Header follows same flex pattern as karma and milestones headers (`.sheet-*-header`).
- `margin-top: 12px` matches milestones header spacing.
- Stat columns are 38px — narrow but sufficient for 1–2 digit stat values.
- Reaction readonly styling mirrors skill total pattern (bold, grey background, solid border).
- CM select at 90px fits "Serious (+3)" text.
- Attack button column 36px — just enough for emoji button.
- `.sheet-tab-panel-bio .repitem` (defined at ~line 1798) already provides shared flex row + gap styling for all Bio tab repeating rows; no override needed.

---

#### Task 5.7: Companion Reaction Worker (Layer 5g)

New change handler for repeating companion reaction. Insert after REGION 3b spirit calculator close (~line 421) and before REGION 4 comment (~line 423).

**Current (~line 420–423):**
```js
  });
});

// ═══════════════════════════════════════════════════════════
// REGION 4 — Event-driven handlers (Sync to DB)
```

**After:**
```js
  });
});

// ─── Layer 5g: Companion Reaction ────────────────────────

on('change:repeating_companions:comp_i change:repeating_companions:comp_q', function() {
  getAttrs(['comp_i', 'comp_q'], function(v) {
    var I = parseInt(v.comp_i, 10) || 0;
    var Q = parseInt(v.comp_q, 10) || 0;
    setAttrs({ comp_reaction: Math.floor((I + Q) / 2) });
  });
});

// ═══════════════════════════════════════════════════════════
// REGION 4 — Event-driven handlers (Sync to DB)
```

**Design notes:**
- Formula `floor((I + Q) / 2)` mirrors player reaction formula `floor((int + dex) / 2)` (Layer 3a, ~line 66). In SR3, Quickness = Dexterity, Intelligence = Intelligence. Confirmed per ADR-003.
- The `on('change:repeating_companions:comp_i ...')` syntax auto-scopes to the changed row — Roll20 resolves the row ID implicitly. Short-form attribute names (`comp_i`, `comp_q`, `comp_reaction`) are used in `getAttrs`/`setAttrs` to match the established Layer 5c skill worker pattern (~line 188).
- Comment label `Layer 5g` follows existing cascade layer naming convention.

---

#### Task 5.8: Companion Reaction Recalc in `sheet:opened`

Insert a new `getSectionIDs` block inside the `sheet:opened` handler, after the skill total recalc block. The current skill recalc block ends at ~line 332 (after Phase 4's rewritten version with orphan cleanup). This new block mirrors the skill recalc pattern.

> **Cross-phase dependency:** Phase 4 rewrites the skill recalc block (~lines 316–332 post-Phase 4). This companion block goes AFTER that rewritten block, still inside the `sheet:opened` handler's outermost callback.

**Current (post-Phase 4, end of `sheet:opened` skill block):**
```js
      setAttrs(out);
    });
  });
});
```

**After:**
```js
      setAttrs(out);
    });
  });

  // Recalculate companion reaction on sheet open
  getSectionIDs('repeating_companions', function(ids) {
    if (!ids.length) return;
    var fields = [];
    ids.forEach(function(id) {
      var p = 'repeating_companions_' + id + '_';
      fields.push(p + 'comp_i', p + 'comp_q');
    });
    getAttrs(fields, function(v) {
      var out = {};
      ids.forEach(function(id) {
        var p = 'repeating_companions_' + id + '_';
        var I = parseInt(v[p + 'comp_i'], 10) || 0;
        var Q = parseInt(v[p + 'comp_q'], 10) || 0;
        out[p + 'comp_reaction'] = Math.floor((I + Q) / 2);
      });
      setAttrs(out);
    });
  });
});
```

**Design notes:**
- The first `});` (closing the skill `getSectionIDs` callback) is retained as anchor context.
- Early return on `!ids.length` avoids unnecessary `getAttrs` call when no companions exist.
- Same enumeration pattern as the existing skill total recalc: build field list from IDs, batch read, batch write.
- `setAttrs(out)` writes all companion reactions in one call (efficient for multiple companions).
- The `});` on the last line closes the `sheet:opened` handler.

---

### G5: Companion Attack Rolls — Verification

#### Task 5.9: Attack Button HTML

Combined with tasks 5.1–5.3 above — the button is embedded in the `repeating_companions` fieldset.

**Roll macro breakdown:**
| Field | Value | Rationale |
|---|---|---|
| `charname` | `@{char_name}` | Player's character name (owner) |
| `rollname` | `@{comp_name} Attack` | Companion's name from row |
| `weapon_name` | `@{comp_name}` | Displayed in attack template header |
| `damage_code` | `?{Damage Code\|@{comp_s}M Physical}` | Prompted with sensible default |
| `power` | `@{comp_s}` | Companion's Strength |
| `tn` | `[[?{Target Number\|4}+@{comp_cm_level}]]` | **Row-level** CM penalty, NOT player's `@{cm_tn_mod}` |
| `successes` | `[[{(?{Dice\|@{comp_reaction}})d6!!}>[[...tn...]]]]` | Dice default to companion reaction |

**Key isolation:** `@{comp_cm_level}` is a per-row attribute. Each companion has its own wound severity. The player's `cm_tn_mod` is never referenced — this is the ADR-003 creature isolation requirement. `reach` and `range_band` are omitted — their `{{#...}}` conditionals in the attack template will hide those rows.

#### Task 5.10: Attack Template Compatibility — Verification Note

The existing `attack` roll template (~line 1339) renders: `weapon_name`, `tn`, `power`, `damage_code`, `reach` (optional), `range_band` (optional), `successes`. All fields in the companion attack button map cleanly. `reach` and `range_band` are not passed → the template's `{{#reach}}` and `{{#range_band}}` conditionals hide them. **No template modification needed.**

---

### P12: Spirit Summon + Attack Roll Buttons

#### Tasks 5.11–5.12: Spirit Roll Buttons HTML

Insert two new button-containing divs inside `.sheet-spirit-combat`, after the Attack display field and before the combat div's closing tag. Each button is wrapped in a `.sheet-spirit-field` div to maintain the existing layout pattern.

**Current (~line 1113–1116):**
```html
        <div class="sheet-spirit-field">
          <label>Attack:</label>
          <input type="text" name="attr_spirit_attack" value="" readonly class="sheet-spirit-wide-display">
        </div>
      </div>
```

**After:**
```html
        <div class="sheet-spirit-field">
          <label>Attack:</label>
          <input type="text" name="attr_spirit_attack" value="" readonly class="sheet-spirit-wide-display">
        </div>
        <div class="sheet-spirit-field">
          <button type="roll" name="roll_btn_spirit_summon" class="sheet-spirit-roll-btn" value="&{template:skill} {{charname=@{char_name}}} {{rollname=Conjuring: @{spirit_type} (Force @{spirit_force})}} {{linked_attr=WIL}} {{tn=[[@{spirit_force}+@{cm_tn_mod}]]}} {{successes=[[{(?{Conjuring dice|0})d6!!}>[[@{spirit_force}+@{cm_tn_mod}]]]]}} {{dice=[[{(?{Conjuring dice|0})d6!!}]]}}" title="Summon — Conjuring vs Force">&#x1F52E; Summon</button>
        </div>
        <div class="sheet-spirit-field">
          <button type="roll" name="roll_btn_spirit_attack" class="sheet-spirit-roll-btn" value="&{template:attack} {{charname=@{char_name}}} {{rollname=@{spirit_type} Attack}} {{weapon_name=Spirit: @{spirit_type}}} {{damage_code=@{spirit_attack}}} {{power=@{spirit_s}}} {{tn=[[?{Target Number|4}]]}} {{successes=[[{(?{Attack dice|@{spirit_b}})d6!!}>[[?{Target Number|4}]]]]}}" title="Spirit melee attack">&#x2694; Attack</button>
        </div>
      </div>
```

**Summon button design notes:**
- Uses `skill` template — displays rollname, linked_attr, tn, successes, dice.
- TN = `@{spirit_force} + @{cm_tn_mod}`. Conjuring is a **player** skill, so the player's wound penalty applies.
- Conjuring dice are prompted (`?{Conjuring dice|0}`) — the skill lives in `repeating_skills` so its total can't be referenced as a scalar attribute. Default 0 forces the player to enter their Conjuring skill total.
- `{{dice=...}}` duplicates the roll expression so the `skill` template can show the raw dice result alongside successes.
- Crystal ball emoji `&#x1F52E;` (🔮) as label prefix.
- Net successes = number of services the spirit owes (narrative tracking, not stored).

**Attack button design notes:**
- Uses `attack` template — displays weapon_name, tn, power, damage_code, successes.
- TN does **NOT** include `@{cm_tn_mod}` — spirits don't share the player's condition track. This is the ADR-003 creature isolation requirement.
- Attack dice default to `@{spirit_b}` (Body stat, used by most spirit categories) with prompt override for categories that use different attack pools.
- Power = `@{spirit_s}` (Spirit Strength). Damage code = `@{spirit_attack}` (already computed by REGION 3b worker as human-readable strings like `"4M"`, `"As Powers"`).
- Crossed swords emoji `&#x2694;` (⚔) as label prefix.
- `reach` and `range_band` omitted — template conditionals hide them.

---

#### Task 5.13: Spirit Roll Button CSS

Insert after the existing spirit textarea CSS (~line 1128, end of `.sheet-spirit-textarea` block), before SECTION 9d (Gear Tab).

**Current (~line 1128–1132):**
```css
.sheet-spirit-textarea {
  width: 100%;
  min-height: 36px;
  font-size: 12px;
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
  padding: 4px 6px;
  resize: none;
  box-sizing: border-box;
}

/* ===================================================
 * SECTION 9d: GEAR TAB — EQUIPMENT REPEATING ROWS
```

**After:**
```css
.sheet-spirit-textarea {
  width: 100%;
  min-height: 36px;
  font-size: 12px;
  background-color: #f2f2f2;
  border: 1px solid #5f5f5f;
  padding: 4px 6px;
  resize: none;
  box-sizing: border-box;
}

.sheet-spirit-roll-btn {
  padding: 4px 10px;
  font-size: 13px;
  cursor: pointer;
  margin-top: 4px;
}

/* ===================================================
 * SECTION 9d: GEAR TAB — EQUIPMENT REPEATING ROWS
```

**Design notes:**
- Minimal styling — the spirit calculator section already has good spacing and the buttons sit inside `.sheet-spirit-field` divs which inherit the section's layout.
- `margin-top: 4px` adds a small gap between the stat display fields and the action buttons.
- No color overrides — uses browser default button appearance for consistency with other roll buttons on the sheet.

---

#### Task 5.14: Spirit Services Tracking — Design Note

Net successes from the summon roll are displayed in the roll template output but NOT tracked as a stored attribute. Tracking services is a narrative/GM concern — not a computed sheet field. If future demand arises, a simple `attr_spirit_services` number input can be added next to the summon button. **Explicitly a non-goal for this phase per ADR-003 scope.**

---

### Cross-Phase Verification Notes

#### Task 5.15: Scalar Field Conflict Check

No new scalar attributes introduced. All companion fields (`comp_name`, `comp_b`, ..., `comp_cm_level`) are repeating-section scoped — they only exist inside `repeating_companions` rows. Spirit roll buttons produce template output only — no `setAttrs`. The only SECTIONS map change is adding the `companions` entry (task 5.4). No conflict with any prior phase.

#### Task 5.16: Companion Reaction Formula Parity

| | Player | Companion |
|---|---|---|
| Formula | `floor((int + dex) / 2)` | `floor((comp_i + comp_q) / 2)` |
| Location | Layer 3a, ~line 66 | New Layer 5g, task 5.7 |
| Attributes | `int` (Intelligence), `dex` (Quickness) | `comp_i`, `comp_q` |
| Floor guard | `Math.max(1, base + misc)` in Layer 3a total | None — companion reaction can be 0 (creature may have 0 in a stat) |

Identical formula, different attributes. Confirmed per ADR-003. Note: player reaction has a `Math.max(1, ...)` floor to prevent `@{reaction}d6` errors in roll macros. Companion attack dice are prompted via `?{Dice|@{comp_reaction}}` so a 0-reaction companion can still have dice manually entered. No floor guard needed.

#### Task 5.17: CSS Section Placement

- Companion CSS (tasks 5.5–5.6): SECTION 14 (Bio Tab), after milestones CSS, before SECTION 20.
- Spirit button CSS (task 5.13): After `.sheet-spirit-textarea` in spirit calculator block, before SECTION 9d.
- No new CSS section numbers needed. Both insertions extend existing section blocks.

---

### Edit Summary Table

| Task | What | Where (~line) | Risk |
|---|---|---|---|
| 5.1–5.3 + 5.9 | Companion section HTML + attack button | Insert after ~1319 | Medium |
| 5.4 | SECTIONS map — add `companions` | ~445–446 | Low |
| 5.5–5.6 | Companion CSS (header + row) | After ~1833 | Low |
| 5.7 | Companion reaction worker (Layer 5g) | Insert after ~421 | Medium |
| 5.8 | `sheet:opened` companion recalc | After Phase 4 skill block | Medium |
| 5.11–5.12 | Spirit summon + attack buttons HTML | Insert after ~1115 | Low |
| 5.13 | Spirit roll button CSS | After ~1128 | Low |

**Total:** 7 logical edits across 2 files (`sheet.html` and `sheet.css`). 1 new repeating section (~30 lines HTML), 1 SECTIONS map entry, 1 new worker (~7 lines), 1 sheet:opened block (~15 lines), 2 spirit roll buttons (~10 lines HTML), companion CSS (~30 lines), spirit button CSS (~5 lines). No new roll templates.

---

### Cascade Impact

```
G4:  comp_i ──→ comp_reaction (via Layer 5g worker)
     comp_q ──→ comp_reaction (via same worker)
     comp_cm_level ──→ (terminal — read inline by roll button macro only)
     sheet:opened ──→ comp_reaction recalc (new getSectionIDs block)

G5:  (no cascade — roll button output only, no setAttrs)

P12: (no cascade — roll button output only, no setAttrs)
     Spirit buttons read existing attrs (spirit_type, spirit_force, spirit_b,
     spirit_s, spirit_attack) — all computed by REGION 3b worker.
     No new dependencies on the spirit calculator cascade.
```

G4 introduces one new cascade chain: `comp_i / comp_q → comp_reaction` (terminal display value, no downstream consumers). G5 and P12 are pure roll template output — zero cascade impact.

---
---

## Layer 4: DRY Audit

**Input:** Layer 3 blueprints (Phases 1–5) — 65 tasks across 13 UAT items
**Heuristics:** Delete (<5-line wrappers) · Merge (identical patterns on same data) · Inline (A→B→C orchestration) · Optimize (multi-pass → single-pass)

---

### 1. DELETE: Thin Wrappers (<5 lines)

| Candidate | Lines | Verdict |
|---|---|---|
| P7 task 5.3: `essence_total` worker | 4 | **KEEP.** Not a wrapper — legitimate dependent computation (`6 - essence_spent`). Removing it would require inlining into both the mutations worker AND the `sheet:opened` essence block, adding complexity. Cascade correctness depends on `change:essence_spent` triggering this worker automatically. |
| P2 task 4.1: PP sync worker | 3 | **KEEP.** Not a wrapper — bridge between text and numeric fields for repeating section. Used by the PP summation chain. |
| P5 task 5.7: companion reaction worker | 5 | **KEEP.** At threshold but not a wrapper — it's the sole computation path for `comp_reaction`. |

**Result: 0 deletions.** All small workers serve distinct cascade roles.

---

### 2. MERGE: Identical Patterns on Same Data

#### 2a. CSS Header Declarations

Karma, milestones, and companions headers share 8 identical base properties:
```css
display: flex; align-items: center; padding: 2px 6px; gap: 6px;
background-color: #f2f2f2; border-bottom: 2px solid #5f5f5f;
font-size: 12px; font-weight: bold;
```

**Assessment:** Only companions header is new (Phase 5). Karma and milestones are existing, unmodified code. Extracting a `.sheet-repeating-header` base class would require editing 2 out-of-scope headers + adding per-header overrides (`margin-top: 12px` on milestones/companions). Net savings: ~16 lines removed, ~8 lines added = ~8 lines. **Not worth the scope expansion for 8 lines.**

**Verdict: NO MERGE.** Revisit if a future UAT adds more repeating section headers.

#### 2b. `sheet:opened` Recalc Blocks

Post-all-phases, the handler contains 4 `getSectionIDs` blocks operating on different repeating sections:

| Block | Section | Pattern | Output |
|---|---|---|---|
| Skills (Phase 4) | `repeating_skills` | 3-pass orphan cleanup + total | Per-row `skill_total` |
| PP cost (Phase 1) | `repeating_adept_powers` | Single-field transform | Per-row `power_pp_cost_value` |
| Essence (Phase 1) | `repeating_mutations` | Scalar sum | `essence_spent` |
| Companions (Phase 5) | `repeating_companions` | Dual-field per-row compute | Per-row `comp_reaction` |

**Assessment:** Four different computation patterns (3-pass vs. per-row transform vs. scalar sum vs. dual-field compute). A generic `recalcSection(section, readFields, writeFn)` helper would need to handle all four patterns — more complex than the blocks themselves. Roll20's `getSectionIDs` only accepts one section name — no batch API available.

**Verdict: NO MERGE.** Blocks are structurally similar but logically distinct.

#### 2c. Roll Template CSS Shared Selectors

Phase 3 P1b already extends grouped selectors (body, row, label, value) from 3 templates to 4, which IS the merge pattern. **Already optimal.**

---

### 3. INLINE: A→B→C Orchestration

#### 3a. Essence Cascade: `mutation_essence → essence_spent → essence_total` + `mag`

**Assessment:** Could inline `essence_total = 6 - spent` into the mutations worker (Layer 5e). This would eliminate task 5.3's worker. BUT: `sheet:opened` task 5.5 also writes `essence_spent`, relying on the `change:essence_spent` event to propagate to both `essence_total` and `mag` workers. Inlining `essence_total` into the mutations worker breaks this — `sheet:opened` would need to duplicate the computation.

**Verdict: NO INLINE.** The 4-line worker pays for itself in cascade correctness and single-source-of-truth for the formula.

#### 3b. Pool Base→Total

**Already inlined in Phase 2 P5** (tasks 4.1–4.4). Layer 4a now writes both `pool_X_base` and `pool_X` with `{silent: true}`. This was the main DRY optimization and it's already in the blueprints.

---

### 4. OPTIMIZE: Multi-Pass → Single-Pass

#### 4a. Phase 4 Skill Orphan Cleanup (3 passes)

```
Pass 1: Detect orphans (parent→child + child→parent)
Pass 2: removeRepeatingRow on orphaned children
Pass 3: Recalculate skill_total for remaining rows
```

**Assessment:** Pass 2 must follow Pass 1 (need detection results). Pass 3 must follow Pass 2 (must skip removed rows + use restored base values). Merging Pass 1 + Pass 3 would require computing totals speculatively and then discarding orphan rows — possible but adds fragile branching with no measurable gain (these are <50 rows, not hot-path operations).

**Verdict: NO OPTIMIZE.** 3 passes is the correct, readable structure.

#### 4b. EP Total Worker — Nested `getSectionIDs`

Phase 3 P10 task 2.5 nests two `getSectionIDs` calls (weapons, then equipment). Roll20's API only accepts one section per call — no batch alternative exists.

**Verdict: NO OPTIMIZE.** API constraint.

---

### 5. DRY Threshold Check

| Metric | Value |
|---|---|
| New code blocks (workers, handlers, templates) | ~11 |
| Consolidation candidates viable | 0 |
| Reduction if all executed | 0% |
| >30% threshold met? | **No** |

---

### Audit Summary

**Result: ZERO consolidation recommendations.**

The Layer 3 blueprints are already DRY. The primary DRY optimization was executed proactively in Phase 2 P5 (pool base→total inlining with `{silent: true}`). Remaining code blocks serve distinct cascade roles and cannot be meaningfully consolidated without increasing complexity or breaking propagation correctness.

| Heuristic | Candidates Examined | Action |
|---|---|---|
| Delete | 3 small workers | None — all serve distinct cascade roles |
| Merge | 3 pattern groups | None — different data/sections/logic |
| Inline | 1 cascade chain | None — would break `sheet:opened` propagation |
| Optimize | 2 multi-pass structures | None — API constraints / correctness requires passes |

**Layer 4 gate: PASS — proceed to Layer 5.**