# TEMPO Memory Log

---

## [2026-03-28] roll20_character_sheet - Layer 2 Complete — All 5 Phases Approved

**What Was Built:** Full Layer 2 Operational Granularity plan across 5 phases: Phase 1 (Naming Contract, ~150 scalar fields + 7 repeating section schemas), Phase 2 (HTML structure, 5 tabs, 7 repeating sections), Phase 3 (Sheet Workers with K-scaffold, 6-layer dependency stack + critical failure mechanic), Phase 4 (CSS spec with 8 locked color tokens, Roll20 constraints, 13 reviewer findings resolved), Phase 5 (Companion App Architecture — Turso DB schema, sync contract, routing plan — all 16 DECISION items resolved). Plan file: .github/plans/roll20_character_sheet_layer2_operational.md (2,656 lines).

**Technical Choices:** Roll20 Pro + K-scaffold. 8 core attributes + derived reaction = floor((int+dex)/2). 4 dice pools: Spell=(CHA+INT+WIL)/2, Combat=(DEX+INT+WIL)/2, Control=Reaction, Astral=(INT+WIL+MAG)/3. Roll mechanic: Nd6 cs>=TN cf<=1; all-1s = critical failure (SR3). Turso hybrid schema: JSON blob scalars + 7 per-section rep tables. SvelteKit + Auth.js (Discord OAuth) + Cloudflare Worker proxy + Cloudflare Pages. Companion app V1 is read-only — bidirectional sync deferred to V2 TEMPO workflow. sync_version monotonic integer maintained for V2 readiness. No CSS custom properties (Roll20 doesn't support :root/var()). Magic TN warning via attribute selector, not class manipulation. 8 CSS color tokens locked (dark navy, maroon, blue for roll templates; amber/orange/red for TN warnings; green for success).

**Failures:** Phase 4 Reviewer FAIL: Magic TN warning used DOM class manipulation — impossible in Roll20 Sheet Workers. Armor region underspecified. Wrong tab scoping selectors (.sheet-tab-magic vs .sheet-tab-panel-magic). Phase 3 Reviewer finding: power_pp_cost watcher targeted wrong field type. Ghost roll bug from {{dice_rolled=...}} parameter removed from all button formulas. Phase 5 Reviewer found: outbound Turso write semantics for orphaned repeating rows unspecified — would cause ghost rows on full sync without explicit DELETE before INSERT.

**Debt Avoided:** No production code in Layer 2 — spec only. No bidirectional sync in V1 (eliminates inbound Sheet Worker logic, conflict resolution complexity, and pull-on-open race condition). No GM-only companion routes in V1. No CSS var()/custom properties. No percentage-based column containers. No delta sync (full payload always — eliminates dirty-field tracking requirement). No auto-save in companion (deferred — no write paths at all).

**Performance:** Layer 2 plan: 2,656 lines. 4 Reviewer runs total (Phases 1–3 combined, Phase 4, Phase 5 separate). Phase 4: FAIL → amended → approved. Phase 5: PASS WITH NOTES → amended → approved. All 16 Phase 5 DECISION items resolved. 3 sandbox test series totalling 14 items documented (D6–D10 Phase 4, 5-SV1–5-SV3 Phase 5).

**Learnings:** Roll20 Sheet Workers cannot manipulate DOM classes — setAttrs() only for dynamic state. Use attribute selectors for CSS state (input[name="attr_tn_warning_level"][value="2"] ~ .sheet-tn-warning). Full payload sync is simpler than delta at this scale. Explicit DELETE + INSERT is required on the Turso side for repeating sections — not just UPSERT. Cloudflare Worker proxy is the right call for token security even for a private game (free tier, keeps Turso token out of browser entirely). Discord OAuth is natural fit for TTRPG companions — all players already have Discord accounts. Read-only V1 is the correct scope: ship fast, prove out the sync pipeline, then add bidirectional in V2.

---

## [2026-03-28] Roll20 Custom Character Sheet — Shadowrun-Inspired - Deep Research — Roll20 Custom Sheet Architecture with External DB Options

**What Was Built:** 4-pass research investigation (10/11 gaps closed). Produced architecture decision matrix, DB evaluation, and Roll20 constraint map. Top recommendation: Roll20-native-first with Firebase or Turso companion if needed.

**Technical Choices:** Sources: 12 Primary (official docs), 2 Secondary (community), 1 Tertiary (forum). Both Roll20 sandboxes prohibit HTTP. Pro required to build sheets. Supabase Free has fatal 1-week inactivity pause. Firebase Firestore free has no pause, 50K reads/day. Turso free no pause, 5GB, HTTP API. Chat-command bridge pattern (API Mod + findObjs/set) is the only viable external→Roll20 sync. K-scaffold recommended for maintainability. Beacon SDK is gated to commercial publishers, NOT for homebrew.

**Failures:** Roll20 wiki (wiki.roll20.net) returns 403 on all direct URL fetches. Roll20 forum posts also 403. Must use help.roll20.net for official docs. Beacon SDK docs 404 at old URLs — use search results as proxy.

**Debt Avoided:** Did not recommend Supabase Free (would have caused weekly DB pauses). Did not recommend PocketBase as primary (pre-v1.0 instability risk). Did not recommend Beacon SDK for homebrew (publisher-gated). Did not overengineer with bi-directional sync before validating need.

**Performance:** 4 passes, 14 source fetches, 10/11 gaps closed. First-principles estimation closed GAP-10 without a search pass. Chat bridge pattern extracted from API Function Documentation (not a dedicated search).

**Learnings:** Critical: Supabase inactivity pause is disqualifying for hobby groups — always check dormancy behavior for free DB tiers. Roll20 sheet workers are single-script-tag, callback-only, zero external HTTP. The 'chat bridge' import pattern is the canonical Roll20 external sync mechanism. Data volume at hobby scale (~180KB total) is never the constraint — dormancy and rate limits at low usage are the real risks. K-scaffold significantly reduces Sheet Worker complexity at scale.

---

## [2026-03-28] stress_test_run - tool verification

**What Was Built:** All 14 ATLAS tools stress-tested via direct sync wrapper invocation

**Technical Choices:** Sync wrappers → _run() → ThreadPoolExecutor → asyncio.run()

**Failures:** run_quality_gates hangs in live MCP context on Windows (asyncio nested loop)

**Debt Avoided:** Did not suppress subprocess tools — documented limitation instead

**Performance:** Full 14-tool coverage in single pytest run

**Learnings:** All tools functional outside of MCP event loop context.

---

