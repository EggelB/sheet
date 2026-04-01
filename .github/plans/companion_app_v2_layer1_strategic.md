# Companion App v2 — TEMPO Layer 1: Strategic Summary

**Status:** ADRs Proposed | Diagram v1 | Produced: 2026-03-31 | Revised: 2026-03-31 (Excel import, karma workflow, milestones)
**Source:** Kael Player Report + Kael GM Report + Combined Synthesis (35 features, 5 tiers, 7 ambiguities resolved) + Excel workbook investigation
**ADRs:** ADR-001 (Group/Session Data Model), ADR-002 (Party Treasure Source of Truth), ADR-003 (Defer Bidirectional Sync), ADR-004 (Excel Import via Python Engine)

---

## Problem Statement

The companion app v1 is a **library browser with character viewing**. The GM workflow hasn't been built: there's no concept of groups, sessions, or party management. Players can't find items efficiently (no sorting, no global search, no mobile layout). The single highest-impact gap is session management — "who's showing up tonight and what are they bringing?" — which currently requires Discord threads and GM memory. Party treasure lives in a shared Excel workbook that's been a persistent pain point for years.

Three additional gaps surfaced during Excel investigation: (1) there is **no way to import existing characters** — all 4 active PCs were built in Excel workbooks following a standard 2-page template, but the only data entry path is manual or Roll20 sync; (2) **karma management is incomplete** — the GM awards karma globally by adventure event (universal to all PCs regardless of session attendance), players allocate it individually (spend on attributes, skills, etc.), but neither action exists in the companion app; (3) **milestone progressions aren't tracked** — each PC has custom progression trees (always 3 milestones per progression) that players manage themselves, with no schema or UI to support them.

**Affected parties:** 1 GM + 5 players in "Enemies in the Shadows" campaign
**Stakes:** Without these features, the app stays open for library browsing but not during sessions — it doesn't justify being a primary tool.

## Success Criteria

1. GM can create a session, populate a roster from any group, and see need-to-know combat stats — without leaving the companion app
2. Party treasure is managed in the companion app, not Excel — accessible to all group members
3. Players can find any library item in <10 seconds on a phone (search + sort + filter + mobile layout)
4. Character lists show owner, group, combat stats, and staleness at a glance
5. All existing v1 functionality remains intact (zero regression)
6. Players can upload an existing character from their Excel workbook and see it in the companion app
7. GM can award karma by event (universally), and players can allocate/spend karma from a PC management view

## Design Constraints

| Constraint | Source |
|---|---|
| SvelteKit + Cloudflare Pages + Turso (libSQL) | Existing stack — non-negotiable |
| Svelte 5 runes (`$props`, `$state`, `$derived`, `$effect`) | In use across all components |
| Discord OAuth + `requireGm()` auth pattern | Existing auth — extend only |
| 24-table schema, 540 library entries, campaign seeded | Additive migrations only |
| One-way Roll20 sync (no REST API exists) | ADR-003 |
| `catalog-config.ts` single source of truth for library | Extend, don't replace |
| adapter-cloudflare edge runtime | No Node.js-only APIs |
| Excel character workbooks use 2-page template (pg1: identity/attributes/condition, pg2: weapons/gear/money) | Parser must handle variable sheet naming |
| Karma awards are universal: all PCs receive the same amount per event regardless of session attendance | Simplifies karma model — campaign-level events, character-level spending |
| Milestone progressions: always 3 milestones per progression, player-managed | Simple CRUD with fixed column count |

---

## ADR-001: Group/Session Data Model with M:N Session Aggregation

**Status:** Proposed
**Date:** 2026-03-31
**Deciders:** Bryce

### Context
The companion app v1 has no concept of groups, sessions, or party composition. The campaign has 3 groups (A/B/C) with 5 players whose characters may appear in any session. Cross-group play is normal — any session can draw characters from any group at GM discretion. A player may run 0, 1, or multiple characters per session.

### Decision
We will implement a relational group/session model: `groups` table for organizational grouping, `characters.group_id` FK for primary group membership, `sessions` as first-class entities (id, campaign_id, date, name, notes, status), and `session_characters` as an M:N join table. PC ownership remains 1:* (one player, many characters).

### Consequences
**Positive:**
- Foundation for session roster, party view, GM dashboard, and all Tier 1 features
- Cross-group play is a natural query (session_characters has no group constraint)
- Session history becomes queryable (which characters played when)

**Negative:**
- More complex queries for "current party" (join through session_characters)
- Migration must assign existing characters to groups (seeded)

**Risks:**
- If session model proves too rigid for encounter tracking or initiative, may need session_events table. Reversal cost: low (additive schema change).

### Alternatives Considered
**Alternative: Flat group membership with no session entity**
Why rejected: Cannot answer "who played last Tuesday" or "what was the roster for session 12." Session history is core to the GM workflow.

**Alternative: Character belongs to multiple groups (M:N groups)**
Why rejected: Adds complexity with no identified use case. Characters have one primary group; cross-group play is handled at the session level.

---

## ADR-002: Companion App as Source of Truth for Party Treasure

**Status:** Proposed
**Date:** 2026-03-31
**Deciders:** Bryce

### Context
Party treasure (currency, shared items, resources) is tracked in a shared Excel workbook ("Karma Tracker & Treasure"). Persistent pain point: "Who's got the party sheet?" "Did someone jot that down?" "The person tracking it isn't playing this week." Not version-controlled, not simultaneously accessible.

### Decision
We will make the companion app the source of truth for group-level party treasure. A treasure table will store shared resources per group. All group members can view; edit permissions TBD in Layer 2. The Excel workbook will be retired after data migration.

### Consequences
**Positive:**
- Single source of truth accessible to all players at all times
- Eliminates the "who has the sheet" problem permanently
- Data backed up (Turso) with audit trail possible

**Negative:**
- Must design treasure data model covering nuyen + shared items
- One-time migration of existing Excel data

**Risks:**
- If treasure model is too simple, may need redesign for complex items (vehicles, enchanted gear). Reversal cost: moderate.
- Concurrent edits: mitigated by Turso serialized writes.

### Alternatives Considered
**Alternative: Keep Excel, link from companion app**
Why rejected: Doesn't solve core problem (single-person access, no backup, no version history).

**Alternative: Google Sheets integration**
Why rejected: Adds external dependency + auth complexity. Companion already has auth and a database.

---

## ADR-003: Defer Bidirectional Roll20 Sync to Future-State

**Status:** Proposed
**Date:** 2026-03-31
**Deciders:** Bryce

### Context
Current sync is one-way: Roll20 sheet worker → companion via POST. Deep Researcher confirmed: Roll20 has no public REST API, Mod API sandbox blocks inbound HTTP, Firebase tokens are browser-context only, sheet workers cannot make HTTP requests.

### Decision
We will defer bidirectional sync and all dependent features (condition tracking U32, dice roller U35) to a future-state release. The only viable path is a private browser extension (Beyond20 pattern). Out of scope for v2.

### Consequences
**Positive:**
- Eliminates largest technical risk from v2 scope
- Focus on features fully within our control
- Extension can be pursued independently without blocking v2

**Negative:**
- Condition tracking remains manual
- Dice roller remains Roll20-native

**Risks:**
- If Roll20 ships a REST API, revisit. Reversal cost: low (additive sync module).

### Alternatives Considered
**Alternative: Build browser extension now**
Why rejected: Significant scope (Chrome + Firefox, DOM injection, Backbone model manipulation). Not justified until core UX is airtight.

**Alternative: Chat-command relay via Mod API**
Why rejected: Requires Roll20 Pro. Lower UX. Viable fallback but not worth building before core platform.

---

## ADR-004: Excel Character Import via Python Engine

**Status:** Proposed
**Date:** 2026-03-31
**Deciders:** Bryce

### Context
Players have existing characters in Excel workbooks following a standard template (pg1: identity, attributes, condition monitors; pg2: weapons, gear, money). The only data entry paths today are manual input and Roll20 sync. Importing from Excel requires parsing `.xlsx` files, which is best handled by `openpyxl` (Python). The existing stack is SvelteKit on Cloudflare edge (no Python runtime).

### Decision
We will provide a player-facing upload portal where players upload their `.xlsx` file and select the character name to extract. A Python engine will parse the workbook and map pg1 + pg2 data to the existing schema. The Python runtime strategy (Cloudflare Workers Python/Pyodide, separate microservice, or client-side WASM) will be evaluated in Layer 2-3.

### Consequences
**Positive:**
- Eliminates manual re-entry for existing characters
- Leverages the consistent 2-page template structure across all character workbooks
- openpyxl handles cell references, merged cells, and formatting reliably

**Negative:**
- Introduces Python into a pure JS/TS stack (new deployment surface)
- Sheet naming conventions vary per player — parser must be flexible

**Risks:**
- If Cloudflare Python Workers can't run openpyxl, may need a separate service. Reversal cost: low (swap runtime, keep parser logic).
- Template drift: if players modify the Excel structure, parser breaks. Mitigation: validate expected cell positions and report parse errors clearly.

### Alternatives Considered
**Alternative: Client-side parsing with SheetJS (xlsx npm package)**
Why deferred: SheetJS can parse .xlsx in the browser, but cell-position-based extraction is more natural in openpyxl. Worth evaluating in Layer 2-3.

**Alternative: Structured form with manual copy-paste**
Why rejected: Still requires manual per-field entry. Defeats the purpose of import.

---

## Component Inventory: Companion App v2

| Component | Type | Responsibility | Key Interfaces | External? |
|---|---|---|---|---|
| Auth Module | Service | Discord OAuth, session mgmt, GM guard | `requireGm()`, `locals.auth()` | No |
| **GM Dashboard** | UI+Server | Campaign overview, player count, stale alerts, quick links | Turso aggregate queries | No |
| **Player Roster** | UI+Server | Players → characters → groups mapping, reassignment | Turso joins | No |
| **Session Manager** | UI+Server | Session CRUD, continuation model, roster selection, stat view | `sessions`, `session_characters` | No |
| **Party Treasure** | UI+Server | Group-level shared resource management | `group_treasure` table | No |
| Library Module | UI+Server | 11 catalogs, CRUD, sort/filter/search | `catalog-config.ts`, Turso | No |
| Character Module | UI+Server | Character viewer, enriched list, staleness | Turso, Roll20 sync data | No |
| **Character Upload** | UI+Server | Player-facing Excel upload portal, character extraction | Python parser, Turso | No |
| **Karma Manager** | UI+Server | GM karma award (campaign-level), player karma allocation (character-level) | `karma_events`, `rep_karma` | No |
| **Milestone Tracker** | UI+Server | Per-character progression management (3 milestones per progression) | `character_milestones` | No |
| **Search Service** | Server | Global cross-catalog + full-text search | Turso FTS/LIKE | No |
| Turso DB | Store | SQLite-compat database (24+ tables) | libSQL wire protocol | No (managed) |
| Cloudflare Pages | Platform | Edge hosting, serverless fns | adapter-cloudflare | No (managed) |
| Discord OAuth | Gateway | Auth provider | OAuth2 redirect | Yes |
| Roll20 Sheet Worker | Gateway | One-way character sync | HTTP POST `/api/sync` | Yes |

**Bold** = new v2 components.

## Boundary Decisions

**In scope (v2):** GM Dashboard, Session Manager, Party Treasure, Player Roster, Search Service, Library enhancements (sort/filter/search/mobile), Character list enrichment, Character Upload from Excel (ADR-004), GM Karma Awards, Player Karma Allocation, Milestone Progressions

**Out of scope (v2):** Bidirectional Roll20 sync (ADR-003), Browser extension, Dice roller, NPC data model, Lore wiki, Offline PWA

**Deferred to Layer 2-3:** Treasure data model specifics, treasure edit permissions, session status lifecycle, search implementation strategy (FTS5 vs LIKE vs client-side), Python runtime strategy for Excel parsing (ADR-004)

---

## Layer 1: Strategic Summary

**Goal:** Transform the companion app from a library browser into a session-ready campaign management tool — covering all Tier 1 features (U1-U6, U1b), all Tier 2 features (U7-U14), and 4 newly identified features (U15-U18: character upload, GM karma awards, player karma allocation, milestone progressions).

### Phase 1: Data Foundation — Schema & Migrations

**Plan Summary:** Create the relational backbone: `groups` table, `characters.group_id` FK, `sessions` table, `session_characters` M:N join, `group_treasure` table, `karma_events` table (campaign-level: id, campaign_id, event_name, karma_amount, date_awarded), and `character_milestones` table (id, character_id, progression_name, milestone_1, milestone_2, milestone_3, active_tier). Extend `rep_karma` to support companion-originated entries (not just Roll20 sync). Seed groups A/B/C from campaign data. Migrate existing characters into their groups. Seed existing karma events from the Karma Tracker workbook (17 events, 36 total karma).

**Justification:** Every feature depends on this schema. Zero UI value alone, but nothing in Phases 2-5 can be built without it. This is the foundation that ADR-001, ADR-002, and the karma/milestone features mandate. Seeding karma events preserves the campaign's historical record.

**Features:** U1 (schema), U1b (schema), U16 (karma schema), U18 (milestone schema)

---

### Phase 2: GM Command Center — Dashboard, Roster & Character Management

**Plan Summary:** Build the GM's home base. Role-based landing page routing (GM → dashboard, player → character list). GM dashboard with campaign overview, player count, character counts by group, stale character alerts, and quick links. Player roster page: players → characters → groups mapping. Character reassignment (un-assign + re-assign). Character list enrichment: add owner, group, combat stats (initiative, condition monitor, edge), staleness indicator, column sorting, and filtering. **GM karma award action:** create a karma event (name + amount) that universally applies to all PCs in the campaign — karma event history visible on dashboard. **Character upload portal:** player-facing page to upload a `.xlsx` workbook, select a character by sheet name, and extract pg1 + pg2 data into the companion via Python engine (ADR-004).

**Justification:** GM Kael's #2 priority after session roster. "No dashboard, no campaign overview, no at-a-glance health check — feels like an afterthought." This transforms admin from a single assign page into actual campaign management. Character enrichment here enables the session roster (Phase 3) to display meaningful stats. GM karma award closes the loop on the retired Karma Tracker workbook — the GM can now award karma from the app instead of updating a shared spreadsheet. Character upload eliminates the manual re-entry barrier that prevents players from moving existing characters into the companion.

**Features:** U3 (GM dashboard), U4 (player roster), U5 (reassign/un-assign), U6 (character enrichment), U15 (character upload), U16 (GM karma award)

---

### Phase 3: Session & Party Management — The Crown Jewel

**Plan Summary:** Session CRUD with continuation model (new session pre-populates from previous roster). Roster selection: add/remove characters from any group. Need-to-know stat view (initiative, condition monitor, edge remaining). Party treasure UI: view and edit group-level shared resources (nuyen, items). Treasure accessible to all group members during sessions. **Player karma management:** PC management view where players see their karma balance (total awarded − total spent), browse the campaign's karma event history, and allocate karma (spend on attributes, skills, etc.) with a ledger that tracks each allocation. **Milestone progressions:** players can add, edit, and remove progression rows for their character — each row has a progression name and 3 milestone descriptions, with an active tier indicator.

**Justification:** "The single highest-impact investment is the session roster / Current Party View. If I can see tonight's party with combat stats, that alone justifies keeping the app open during play." (GM Kael). Party treasure bundled here because it's accessed during sessions and completing the "session experience" is the core value proposition. Player karma allocation and milestone management are bundled here because they're PC management actions that happen between sessions — players review what karma they've earned and decide how to spend it. Milestones are narratively driven and evolve alongside karma spending. This phase delivers Success Criteria #1, #2, and #7.

**Features:** U2 (session roster / party view), U1b (treasure UI), U17 (player karma allocation), U18 (milestone progressions)

---

### Phase 4: Library & Search Overhaul

**Plan Summary:** Column sorting on all catalog list pages. Filter coverage expansion (Equipment, Mutations, Adept Powers filters; Drain filter for Spells). Human-readable filter labels (replace `pp_cost` → "Power Point Cost"). Full-text search matching descriptions, not just names. Global cross-catalog search. Cross-link character skills/spells/powers to library detail pages.

**Justification:** Tier 2 features both roles need, batched because they all touch the same `catalog-config.ts` and list page infrastructure. Global search doubles as GM duplicate detection. Cross-linking bridges the character → library gap that Player Kael flagged as blocker B4. This phase delivers Success Criteria #3 (finding items efficiently).

**Features:** U8 (sorting), U9 (global search), U10 (cross-linking), U11 (filter coverage), U12 (full-text search), U13 (readable labels)

---

### Phase 5: Responsive Layout & Polish

**Plan Summary:** Mobile responsive layout (card grid, filter sidebar, character tabs must work on phone screens). Relative timestamps ("2 hours ago" instead of ISO 8601). Staleness badges on character lists and GM dashboard. Cross-cutting quality pass ensuring all new Phase 2-4 UI works on mobile.

**Justification:** "Players use phones at the table" (Player Kael B1). Raw UTC timestamps are friction for both roles (F6/F3). Staleness badges are the agreed-upon approach (A7) for building the sync habit. This phase is sequenced last because it's a cross-cutting pass that benefits from all prior phases being built. Delivers remaining Success Criteria #3 (mobile) and #4 (staleness at a glance).

**Features:** U7 (mobile responsive), U14 (relative timestamps + staleness badges)

---

## Phase Self-Check

| Phase | Achieves goal? | Enables next? |
|---|---|---|
| 1: Data Foundation | Schema only — no standalone value | ✅ Enables all subsequent phases |
| 2: GM Command Center | ✅ GM campaign management + karma awards + character upload | ✅ Enriched character data + karma events feed Phase 3 |
| 3: Session & Party | ✅ Session roster + party treasure + player karma + milestones (core value prop) | Independent — but library links enhance session view |
| 4: Library & Search | ✅ Efficient item discovery for both roles | ✅ Cross-links and search make Phase 5 mobile pass more valuable |
| 5: Responsive & Polish | ✅ Mobile usability + timestamp/staleness polish | Terminal phase |

**Coverage:** All 7 Tier 1 features (U1-U6, U1b) + all 8 Tier 2 features (U7-U14) + 4 newly identified features (U15-U18) = 19 features across 5 phases.
