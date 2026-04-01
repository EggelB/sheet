# Combined Kael Synthesis — Player + GM UX Evaluation

**Date:** 2026-04-01  
**Sources:** [Player Kael Report](companion_app_kael_player_report.md) | [GM Kael Report](companion_app_kael_gm_report.md)  
**Purpose:** Unified priority stack + resolved ambiguities — ready for Layer 1  
**Last updated:** 2026-04-01 — All ambiguities resolved, priorities adjusted per user decisions

---

## Unified Priority Stack

Cross-referencing both reports, here's the combined ranking by impact across all user roles.

### Tier 1 — Core Platform (blocks both Player and GM workflows)

| # | Feature | Player | GM | Notes |
|---|---|---|---|---|
| U1 | **Group/Party data model** | Dream | Must-Have | Foundation for party view, session roster, character list enrichment. Nothing else works without this. |
| U2 | **Current Party View (session roster)** | Dream | Must-Have | Drag-and-drop session roster, cross-group composition, need-to-know stats. The single highest-impact feature for GM. |
| U3 | **GM landing page / campaign dashboard** | — | Must-Have | Campaign overview, player count, stale characters, quick links. Replaces the useless player onboarding message. |
| U4 | **Player Roster Dashboard** | — | Must-Have | GM admin home base: players → characters → groups mapping. |
| U5 | **Re-assign / Un-assign characters** | — | Must-Have | Edit ownership. Currently impossible once assigned. |
| U1b | **Party treasure / shared resources** | — | Must-Have | **ELEVATED from Tier 5.** Historically a nightmare ("Who's got the party sheet?" "The guy who runs it isn't playing this week"). Companion app becomes source of truth. |
| U6 | **Character list enrichment** | Blocker (B5) | Must-Have | Add owner, group, combat stats, staleness. Sort/filter. |

### Tier 2 — Library & Search (both roles benefit equally)

| # | Feature | Player | GM | Notes |
|---|---|---|---|---|
| U7 | **Mobile responsive layout** | Must-Have | Nice-to-Have | Players use phones at the table. GM preps on desktop but needs mobile for in-session reference. |
| U8 | **Column sorting** | Must-Have | Must-Have | Both roles need alphabetical/value sorting on catalog lists. |
| U9 | **Global search** | Must-Have | Nice-to-Have | Player: find anything fast. GM: duplicate detection before creating entries. |
| U10 | **Cross-link character ↔ library** | Must-Have | — | Character skills/spells link directly to library detail pages. |
| U11 | **Better filter coverage** | Must-Have | — | Equipment, Mutations, Adept Powers need filters. Drain filter for Spells. |
| U12 | **Full-text search in descriptions** | Must-Have | — | Search matches description/notes, not just name. |
| U13 | **Human-readable filter labels** | Friction | Friction | Replace `pp_cost` → "Power Point Cost", `drain_type` → "Drain Type". |
| U14 | **Relative timestamps** | Friction | Friction | "2 hours ago" instead of ISO 8601. Staleness indicator for GM. |

### Tier 3 — Quality of Life (polish that makes the app feel professional)

| # | Feature | Player | GM | Notes |
|---|---|---|---|---|
| U15 | **Dark mode** | Nice-to-Have | Nice-to-Have | Evening sessions. Both roles want this. |
| U16 | **Tab URL state** | Nice-to-Have | — | Persist character tab in URL hash for sharing. |
| U17 | **Catalog intros / descriptions** | Nice-to-Have | — | Brief context at top of each catalog page. |
| U18 | **Form field hints/placeholders** | — | Nice-to-Have | "e.g. F+3" for spirit formula fields. |
| U19 | **Library create/edit feedback** | — | Friction | Toast or flash message on save. No silent redirects. |
| U20 | **Sub-nav simplification** | Friction | — | 11 catalog links is cognitive overload. Group or collapse. |
| U21 | **"My Stuff" filter** | Nice-to-Have | — | Show only items the player's character actually has. |
| U22 | **Favorites / bookmarks** | Nice-to-Have | — | Star items for quick access during sessions. |

### Tier 4 — Session Management (the "between sessions" value proposition)

| # | Feature | Player | GM | Notes |
|---|---|---|---|---|
| U23 | **Session notes / journal** | Dream | Nice-to-Have | Per-session log: date, deployed characters, narrative, GM-private notes. |
| U24 | **NPC quick-reference cards** | — | Nice-to-Have | Lightweight: name, stats, threat level, notes. Not full character sheets. |
| U25 | **Quick-reference combat card** | Dream | — | One-page character summary for combat: initiative, weapons, active spells. |
| U26 | **Bulk library operations** | — | Nice-to-Have | Multi-select edit or CSV import/export for 540 entries. |
| U27 | **Library versioning / changelog** | — | Nice-to-Have | `updated_at` + changelog_note for homebrew errata tracking. |
| U28 | **"Impersonate player" view** | — | Nice-to-Have | GM sees app as a specific player — for onboarding and QA. |

### Tier 5 — Vision (defines what this app *becomes*)

| # | Feature | Player | GM | Notes |
|---|---|---|---|---|
| U29 | **Lore wiki / shared knowledge base** | — | Dream | Markdown pages, GM drafts / player published, linked from character detail. |
| U30 | **Player-facing session prep** | — | Dream | Players mark deploying characters before session. GM sees in real-time. |
| U31 | **Cross-group encounter tracker** | — | Dream | Session roster + GM annotations (threat notes, plot hooks). |
| U32 | ~~Condition tracking (bidirectional)~~ | ~~Dream~~ | — | **DEFERRED to future-state** alongside dice engine + browser extension. |
| U33 | **Offline PWA** | Dream | — | Cache library for offline use at conventions. |
| ~~U34~~ | ~~Party treasure / shared resources~~ | — | — | **ELEVATED to Tier 1** — see U1b below. |
| U35 | ~~Dice roller~~ | ~~Tabled~~ | ~~Tabled~~ | **DEFERRED to future-state** alongside bidirectional sync + browser extension. |

---

## Open Ambiguities Requiring Research

These items surfaced from both Kael reports where we lack clarity to make design decisions. Each needs investigation before Layer 1 planning can proceed confidently.

### A1: Roll20 API — Bidirectional Sync Feasibility ✅ RESEARCHED
**Question:** Can the companion app push data (conditions, status) back to a Roll20 character sheet?  
**What we know:** Current sync is one-way (Roll20 sheet worker → companion via POST). Sheet workers use `getAttrs`/`setAttrs` for read/write within Roll20. The companion app has no Roll20 API key or OAuth integration.  

**Research Findings (Deep Researcher, 2026-04-01):**

| Approach | Feasibility | Notes |
|---|---|---|
| Roll20 REST API | **NOT FEASIBLE** | Does not exist. No public REST API for external writes. |
| Mod API script as relay | **NOT FEASIBLE** | API sandbox explicitly blocks inbound HTTP. Documented limitation. |
| Firebase direct write | **NOT FEASIBLE** | Auth tokens and paths are private, browser-context only. |
| Sheet worker polling | **NOT FEASIBLE** | Sheet workers cannot make HTTP requests. |
| **Browser extension** | **VIABLE** | Beyond20 proves the pattern. Extension background worker polls companion API → page-injected script writes to `window.Campaign.characters` Backbone model. Our Shadowrun sheet is compatible. |
| Chat command + Mod API | **VIABLE (fallback)** | Companion generates copyable chat command → GM pastes in Roll20 → Pro Mod API script listens and applies changes. Requires Roll20 Pro. Lower UX, zero install. |

**Verdict:** No direct API path exists. Two viable approaches: (1) private Chrome/Firefox extension (proven pattern via Beyond20), (2) chat-command relay via Mod API for Pro subscribers.  
**Decision gate:** If extension development is out of scope, bidirectional sync is **permanently deferred** unless Roll20 ships a public REST API (no indication planned as of March 2026).  
**Impact:** Condition Tracking (U32) requires browser extension development. Recommend deferring to a future version unless the extension adds enough other value to justify the investment.

### A2: Group/Party Data Model — Schema Design ✅ DECIDED
**Question:** How should groups, session rosters, and cross-group play be modeled in the database?  

**User Decisions (2026-04-01):**
- **PC ownership is 1:*** — One player can own many characters.
- **Party/session aggregation is M:N** — A character can appear in multiple sessions; a session has multiple characters. A player may run multiple PCs in one session, or not play at all.
- **Sessions are first-class entities** — GM creates sessions (typically continuation of previous session). Sometimes switches parties for a session (GM discretion based on player availability + narrative). Established ahead of time.
- **Groups are organizational** — Characters belong to a primary group (A/B/C), but any session can draw from any group for cross-group play.

**Schema implications:**
- `groups` table (id, campaign_id, name)
- `characters.group_id` FK (1:1 primary group membership)
- `sessions` table (id, campaign_id, date, name, notes, status)
- `session_characters` join table (session_id, character_id) — M:N
- Player may have 0 characters in a given session

**Impact:** Foundation for U1, U2, U3, U4, U23, U30, U31. Nearly everything in Tier 1 depends on this.

### A3: NPC Data Type — Scope and Structure 🔜 DEFERRED
**Status:** Deferred alongside lore wiki (A5). Nice-to-have, not blocking Layer 1.  
**Revisit:** After core platform (Tier 1-2) is shipped.

### A4: Drag-and-Drop Session Roster — Interaction Model ✅ DECIDED
**Question:** What does "drag-and-drop session roster" actually look like?  

**User Decisions (2026-04-01):**
- **GM creates sessions** — Not player-initiated. GM decides party composition.
- **Continuation model** — Sessions are typically a continuation of the previous session. No ceremony needed for "new session" — it's mostly "same group, next week."
- **Party switching** — Sometimes GM switches which group is playing. This is decided ahead of time based on player availability and narrative arc. GM discretion.
- **Roster flexibility** — A player can run 0, 1, or all of their characters in a session. Cross-group composition is normal.
- **Need-to-know stat block** — Initiative, condition monitor, edge remaining (from Player Kael). Exact fields TBD in Layer 3.

**UX implications:**
- "New Session" is a lightweight action — select date, pick characters from any group, done.
- Default: pre-populate with previous session's roster (since continuation is the norm).
- GM can swap characters in/out before or during session.
- No lock mechanism needed — roster is always editable by GM.

**Impact:** Core UX of U2. Design decisions here cascade into Tier 4 and 5 features.

### A5: Lore Wiki — Architecture and Player Visibility 🔜 DEFERRED
**Status:** Deferred alongside NPCs (A3). Nice-to-have, not blocking Layer 1.  
**Revisit:** After core platform (Tier 1-2) is shipped.

### A6: Party Treasure / Shared Resources — Source of Truth ✅ ELEVATED
**Question:** Where does party treasure live?  
**What we know:** Currently tracked in the Karma Tracker & Treasure Excel workbook. Historically a nightmare — "Who's got the party sheet?" "Did someone jot that down?" "The person running it isn't playing this week."

**User Decision (2026-04-01):**
- **Much higher priority than originally assessed.** Elevated from Tier 5 (Dream) to Tier 1 (Core Platform).
- **Companion app becomes source of truth** — no more Excel sheet passed around.
- **Accessible to all group members** — whoever's playing can see and update.

**Still to decide (in Layer 2-3):**
- What does the current workbook track? (Gold? Items? Both? Per-group or per-character?)
- Do players edit their own group's treasure, or is it GM-only?
- How does treasure relate to the equipment catalog? (Owned items vs. library entries)

**Impact:** Now a Tier 1 feature (U1b). Design details in Layer 2-3.

### A7: Sync Staleness — Detection and Alerting ✅ CONFIRMED
**Question:** How do we detect and surface stale character data?  
**What we know:** Characters have `synced_at` timestamps. GM wants staleness indicators. Sync is triggered by saving in Roll20.  

**User Decision (2026-04-01):**
- **Confirmed as a good feature.** Need to build the habit of players refreshing sheets.
- **Start with visual indicators** — color/badge on character list. Elaborate later.
- **Thresholds and notification mechanisms** — details in Layer 2-3.
- **Cannot detect Roll20-side changes without sync** (confirmed by A1 research — no Roll20 API).

**Impact:** Part of U6 (character list enrichment) and U14 (relative timestamps).

---

## What's Needed Before Layer 1

### All ambiguities resolved! ✅

| # | Status | Decision |
|---|---|---|
| A1 | ✅ Researched | No direct API. Bidirectional sync + dice roller deferred to future-state (browser extension track). |
| A2 | ✅ Decided | 1:* ownership, M:N session aggregation, sessions are first-class, groups are organizational with cross-group play. |
| A3 | 🔜 Deferred | NPCs deferred alongside lore wiki. |
| A4 | ✅ Decided | GM creates sessions, continuation model, pre-populate previous roster, flexible cross-group composition. |
| A5 | 🔜 Deferred | Lore wiki deferred alongside NPCs. |
| A6 | ✅ Elevated | Party treasure elevated to Tier 1. Companion app = source of truth. |
| A7 | ✅ Confirmed | Visual staleness indicators first, build the habit. |

### Deferred to Future-State (browser extension track)
- Bidirectional sync / condition tracking (U32)
- Dice engine (U35)
- NPCs (U24 / A3)
- Lore wiki (U29 / A5)

**Layer 1 planning can now proceed.** All blocking decisions are resolved.
