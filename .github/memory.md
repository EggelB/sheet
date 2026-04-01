# TEMPO Memory Log

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

