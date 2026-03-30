# Sandbox Fix Cycle — Roll20 Character Sheet

**Date:** 2026-03-29
**Context:** P1-P4c complete. First Roll20 sandbox test revealed 5 issues. Root causes diagnosed.

---

## Fix Plan

### F1: CSS Extraction (CRITICAL)
**Problem:** Roll20 Custom Sheet ignores inline `<style>` blocks. Our ~1100 lines of CSS are invisible.
**Root Cause:** Roll20 requires CSS in its dedicated CSS tab, not inline in HTML.
**Fix:** Extract everything between `<style>` and `</style>` into a new `sheet.css` file. Remove the `<style>` block from `sheet.html`. User pastes CSS into Roll20's CSS tab and HTML into the HTML tab.
**Risk:** Low — mechanical extraction, no logic changes.

### F2: Worker Rewrite (CRITICAL)
**Problem:** No totals, pools, or derived values calculate. All fields stay at 0.
**Root Cause:** All 13 `k.registerFuncs()` calls + `k.sheetOpens()` + `k.getAllAttrs()` use K-scaffold API, which is a build-time framework NOT available in Roll20's runtime sandbox. `k` is undefined → every worker silently fails.
**Fix:** Rewrite entire `<script type="text/worker">` using vanilla Roll20 API:
- `k.registerFuncs({ name, trigger, affects, callback })` → `on('change:trigger1 change:trigger2', function() { getAttrs([...], function(v) { setAttrs({...}); }); })`
- `k.sheetOpens()` → `on('sheet:opened', function() {...})`
- `k.getAllAttrs()` → `getAttrs([...])`
- `k.setAttrs()` → `setAttrs()`
- Keep cascade logic intact — same inputs, same formulas, same outputs
**Risk:** Medium — must preserve all cascade dependencies.

### F3: Condition Monitor Redesign
**Problem:** Condition monitor displays as 3 vertical radio-button groups. User wants horizontal damage-box table.
**Root Cause:** Design mismatch with SR3 condition monitor format.
**Fix:** Replace radio tracks with a table: 3 rows (Mental / Stun / Physical), columns for damage boxes grouped by damage code (Light=2 boxes, Moderate=2, Serious=2, Deadly=2, + Overflow/Unconscious where applicable). Use checkboxes for damage tracking. Update CSS Section 5 to style the new table.
**Risk:** Medium — new HTML structure + CSS needed. Workers for `cm_tn_mod` / `cm_init_mod` must be updated to count checkboxes instead of reading radio values.

### F4: Specialization Field Type Change
**Problem:** Specialization is a freeform text input. Should be a boolean toggle.
**Fix:** Change `<input type="text" name="attr_skill_spec" placeholder="Specialization">` to `<input type="checkbox" name="attr_skill_spec" value="1">`. Update CSS for narrower width.
**Risk:** Trivial.

### F5: Seed Data (DEFERRED)
**Status:** Acknowledged as companion app concern. Addressed in P5.

---

## Execution Order
F1 → F2 → F3 → F4 → Re-test in Roll20 sandbox

## Sign-off
User approved: "we are approved to make the fixes"
