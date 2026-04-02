# TEMPO Memory Log

---

## [2026-04-01] sheet_uat_r1 - Layer 5 — Pure Signal Brief

**What Was Built:** Layer 5 Pure Signal Brief: 18,270 bytes of dense developer handoff document. Covers all 13 UAT items across 5 phases (65 implementation tasks). Includes: 3 ADR governance tables, per-phase numbered task lists, sheet:opened final structure, SECTIONS map final state, cascade layer map (15 entries), cross-phase dependency chain (strict 1→2→3→4→5), 4 risk mitigations, and 10-item per-phase verification checklist. All CCE planning layers (1-5) now complete.

**Technical Choices:** Compressed L3 blueprints into grouped action items (41 L5 items covering 65 L3 sub-tasks). Retained approximate line numbers for developer orientation. Included post-all-phases structural diagrams (sheet:opened, SECTIONS, cascade) to give developer full end-state visibility. Kept roll20 @{attr} scoping rules explicit per ADR-003.

**Failures:** Initial save_plan(layer=5) failed because L4 gate file didn't exist as separate file. Resolved by saving L4 as formal plan first.

**Debt Avoided:** Resisted adding task-level code snippets to L5 — kept it as actionable descriptions pointing to L3 blueprints for full code blocks. Avoided inflating the brief beyond its purpose as a navigation/verification document.

**Performance:** L5 written and reviewed in single conversation turn. Reviewer found zero blocking issues. All 5 CCE layers complete — ready for implementation.

**Learnings:** save_plan gate check requires each layer N-1 file to exist as a separate formal plan file — appending L4 audit to L3 blueprints file wasn't sufficient; needed save_plan(layer=4) to create the gate file. Reviewer PASS WITH NOTES on first attempt — 6 findings all MINOR/NOTE (terminology consistency, upstream L3/L1 errata). Pure Signal Brief format effective: grouped tasks reduce cognitive load vs. raw sub-task enumeration.

---

## [2026-04-01] sheet_uat_r1 - Layer 3 (all 5 phases) + Layer 4 DRY Audit

**What Was Built:** Complete Layer 3 technical blueprints for all 5 phases (65 tasks, 13 UAT items) + Layer 4 DRY audit with zero consolidation recommendations. Phase 1: Critical Bug Fixes (P11 karma sign, G1 resist body, P6 init mod, P2 PP sync, P7/ADR-001 essence model) — 11 tasks. Phase 2: UX Fixes (P3b mutation BP width, P1a effect ellipsis, P9 weapon button alignment, P3a setTimeout(0) deferral, P5 pool base+total merge with {silent:true}) — 16 tasks. Phase 3: Data Entry Enhancements (P8 17-option grouped weapon type select, P10 equip_qty with EP×qty multiplication, P1b chat effect buttons + new desc rolltemplate) — 16 tasks. Phase 4: Skill Specialization (P4/ADR-002 — spec checkbox→child creation via generateRowID, 3 guards, sheet:opened orphan cleanup with 3-pass validIds approach) — 9 tasks. Phase 5: Creature Systems (G4/ADR-003 repeating_companions section, G5 companion attack with row-level CM isolation, P12 spirit summon+attack roll buttons) — 12 impl + 5 verification tasks.

**Technical Choices:** ADR-001: essence_spent as intermediate attr (6-spent=essence_total), mag worker reads essence_spent directly. ADR-002: Hidden skill_parent_id/skill_child_id cross-refs, _.object() for guard reverts, removeRepeatingRow in setAttrs callback for safety. ADR-003: comp_cm_level (row-level select 0-3) replaces cm_tn_mod for creature isolation; companion reaction uses short-form auto-scoped attrs matching Layer 5c pattern. Pool optimization: base+total merged in single setAttrs with {silent:true}, calcPoolTotal retained for direct misc edits. Spirit rolls: summon uses player cm_tn_mod (player skill), attack omits it (creature independence). New desc rolltemplate with #2a3a2a dark olive header for effect chat output.

**Failures:** 

**Debt Avoided:** Resisted creating generic recalcSection() helper for sheet:opened blocks — 4 different computation patterns would make it more complex than the blocks themselves. Resisted extracting shared CSS header base class — only 8 lines of savings for 3 headers, 2 of which are out-of-scope existing code. Resisted inlining essence_total into mutations worker — would break sheet:opened propagation chain.

**Performance:** 5 Layer 3 phases + 1 Layer 4 audit completed in single session. All 5 adversarial reviews passed (3 PASS, 2 PASS WITH NOTES). Total findings: 5 (2 MAJOR fixed, 3 MINOR accepted/fixed). Zero CRITICAL or FAIL verdicts.

**Learnings:** 1. Roll20 repeating section change handlers use short-form attr names (comp_i not repeating_companions_comp_i) — auto-scoped by API. Long form risks silent failure. 2. sheet:opened recalc blocks for different sections can't be meaningfully abstracted — each has distinct patterns (3-pass orphan, scalar sum, per-row transform, dual-field compute). 3. L2 wrapper divs can be legitimately simplified away at L3 if existing codebase doesn't use them (karma/milestones have no wrappers → companions shouldn't either). 4. DRY audit found zero consolidation candidates — blueprints were already lean from proactive P5 pool optimization. >30% threshold not close. 5. Reviewer run_quality_gates bypass must be explicitly stated in every reviewer prompt — proven across 5 reviews.

---

## [2026-04-01] sheet_uat_r1 - Layer 2 Complete + Layer 3 Phase 1 Approved

**What Was Built:** CCE Layer 1 (strategic plan: 3 ADRs, 5 phases, 4 risks) + Layer 2 (operational plans for all 5 phases: 13 UAT items, 60+ tasks) + Layer 3 Phase 1 blueprint (Critical Bug Fixes: P11 karma sign, G1 resist damage CM removal, P6 init penalty, P2 PP text→numeric sync, P7 ADR-001 essence/magic chain). All reviewed adversarially and approved. Branch: fix/sheet-uat-r1.

**Technical Choices:** ADR-001: essence_spent (sum) + essence_total (6-spent) + mag = max(0, base+misc-spent). ADR-002: generateRowID() child rows for skill spec with bidirectional orphan cleanup. ADR-003: repeating_companions with simplified 3-level CM select (value=penalty), per-row reaction worker. Spirit summon/attack buttons reuse existing templates. Reviewer bypass pattern: explicit "Do NOT call run_quality_gates" constraint prevents MCP hang.

**Failures:** Initial save_plan call overwrote L1 plan with stub text — recovered via replace_string_in_file. Phase 5 companion reaction formula had paren bug caught by reviewer.

**Debt Avoided:** Did not add full 32-box CM track for companions (3-level select instead). Did not store spirit services as attribute (narrative concern). Did not add CSS for hidden inputs (unnecessary). Resisted urge to add {silent:true} to Phase 1 workers — that's Phase 2/P5 scope.

**Performance:** Layer 2: 5 phases planned, reviewed, approved in single session. Layer 3 Phase 1: blueprint written, reviewed, approved. All reviewer verdicts: PASS WITH NOTES. Zero CRITICAL findings on final submissions (all caught and fixed pre-presentation).

**Learnings:** 1) Reviewer run_quality_gates hangs indefinitely — bypass with explicit constraint in every reviewer prompt. 2) save_plan can overwrite content; prefer direct file edits. 3) Line number references drift by 1-2 lines — always use ~ prefix and verify against source before blueprint. 4) Parenthesis placement in pseudocode formulas needs extra scrutiny (caught Math.floor bug in Phase 5). 5) ADR wording can go stale as L2 simplifies design — reviewer catches these. 6) For sheet workers: setAttrs before removeRepeatingRow is safer (recovery via sheet:opened orphan cleanup).

---

## [2026-03-31] companion_app_v2 - Layer 2 — Phases 1-3 Operational Planning

**What Was Built:** Completed Layer 2 operational plans for Phases 1-3 of the companion app v2. Phase 1 (Data Foundation): 6 tasks — schema DDL for 6 new tables (groups, sessions, session_characters, group_treasure, group_currency, karma_events), ALTER TABLE migration for 3 existing tables, seed scripts for groups + karma events, character-to-group migration, verification pass. Phase 2 (GM Command Center): 6 tasks — route scaffolding (/dashboard, /roster), character list enrichment, GM dashboard, player roster + group reassignment, GM karma award, character upload portal (SheetJS). Phase 3 (Session & Party Management): 7 tasks — session/treasure route stubs, session CRUD with continuation model, roster management, party stat view (initiative + CM), party treasure UI (gold/silver/copper), player karma allocation ledger, milestone progression CRUD.

**Technical Choices:** ADR-004 resolved: SheetJS client-side (Option A) for Excel parsing — not Python. Edge attribute confirmed non-existent in game system — removed from all plans. CM columns: physical (11 boxes), stun (11 boxes), mental (10 boxes — intentionally excluded from stat view, mental damage can't reduce condition). Initiative column is `init_score`. Currency system uses gold crowns (GC), silver stags (SS), copper pennies (CP) — NOT nuyen. Separate `group_currency` table (Option A) confirmed. Sessions table needs `name TEXT` and `status TEXT NOT NULL DEFAULT 'active'` columns (BD-2 downgraded to DEV DECISION). `session_characters` needs UNIQUE(session_id, character_id) for INSERT OR IGNORE. Companion-originated rep rows use `roll20_row_id = 'comp-{uuid}'` sentinel. STALE_THRESHOLD_DAYS = 7. All routes top-level: /dashboard, /roster. Player-to-player reassignment deferred. Duplicate upload rejected with error.

**Failures:** Reviewer agent gets stuck on `run_quality_gates()` MCP tool call — had to bypass and do manual adversarial reviews for both Phase 2 and Phase 3. PowerShell `Set-Content -Encoding UTF8` (PS 5.1) writes UTF-8 with BOM and caused double-encoding corruption of em-dashes and arrows in the layer2 plan file — fixed via Python cp1252-roundtrip decoder. Phase 3 was appended twice to the plan file by the planner subagent — cleaned up duplicate content. multi_replace_string_in_file can hit wrong section when file has duplicate content patterns (original + revised Phase 1 both in same file).

**Debt Avoided:** Resisted adding edge attribute to schema when it doesn't exist in the game system (planner hallucinated it). Resisted using nuyen as currency when the actual system uses gold/silver/copper. Did not auto-create character_milestones table — correctly identified that rep_milestones already exists and should be reused with a `source` column. Did not implement multi-campaign logic — flagged as known debt for future.

**Performance:** 3 phases planned, reviewed, and all blocking items resolved in a single session. Plan file is 1068 lines covering 19 tasks across 3 phases. All 5 Phase 2 blocking items + 2 Phase 3 blocking items resolved. Zero remaining blockers for Phases 1-3.

**Learnings:** NEVER use PowerShell Set-Content for UTF-8 files with special characters — use Python or .NET with explicit UTF-8NoBOM encoding. When a plan file contains multiple sections with similar text (original + revised), use very specific context in replace operations to avoid hitting the wrong section. The reviewer agent MCP quality gates tool is unreliable — manual review is the fallback. Always verify schema column names against actual DDL before planning queries — planner agents will hallucinate column names (attr_edge, initiative_base). Game system currency names matter — always confirm with the user rather than assuming standard RPG conventions.

---

## [2026-03-31] companion_app - Pre-Layer 1 — UX Evaluation & Ambiguity Resolution

**What Was Built:** 1. Invoked Human Preference agent (Kael) as both Player and GM personas against the companion app.
2. Player Kael: 6 blockers, 9 friction items, 5 smooth. Wishlist: 6 must-have, 8 nice-to-have, 5 dream.
3. GM Kael: 6 blockers, 11 friction items, 7 smooth. Wishlist: 6 must-have, 8 nice-to-have, 5 dream.
4. Combined synthesis: 35 unified features across 5 tiers. 7 ambiguities identified, all resolved.
5. Deep Researcher investigated Roll20 API — no REST API exists. Browser extension viable (Beyond20 pattern).

Artifacts saved:
- .github/plans/companion_app_kael_player_report.md
- .github/plans/companion_app_kael_gm_report.md
- .github/plans/companion_app_kael_synthesis.md (master document)

**Technical Choices:** • A1: Bidirectional sync deferred to future-state (browser extension track) alongside dice engine
• A2: PC ownership 1:*, session aggregation M:N, sessions first-class entities, groups organizational with cross-group play
• A4: GM creates sessions, continuation model, pre-populate previous roster, flexible composition
• A6: Party treasure ELEVATED to Tier 1 — companion app becomes source of truth (historically nightmarish in Excel)
• A3/A5: NPCs + Lore wiki deferred
• A7: Visual staleness indicators first, build the sync habit

**Failures:** No failures. Both Kael invocations produced high-quality output. Deep Researcher conclusively answered the Roll20 API question.

**Debt Avoided:** Resisted designing bidirectional sync or dice engine — both deferred to future-state with clear rationale. Resisted over-specifying NPC and lore wiki schemas before core platform is built.

**Performance:** 

**Learnings:** 1. Human Preference agent produces dramatically different priorities when primed as Player vs GM. Both perspectives were essential.
2. GM's #1 gap is workflow (sessions, roster, parties), not features. The app does things TO items but not TO sessions.
3. Party treasure was massively underrated by both Kael personas — user's domain knowledge caught what the agent missed.
4. Roll20 has zero external write API. The only viable path is a browser extension (Beyond20 proves it) or chat-command relay via Mod API.
5. Session continuation is the norm — "New Session" should pre-populate from previous roster, not start blank.

---

