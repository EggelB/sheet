# GM Kael Report — Companion App UX Evaluation

**Date:** 2026-04-01  
**Persona:** GM (long-running Shadowrun campaign, 5 players, 3 groups, cross-group sessions)  
**Agent:** Human Preference (Kael)  
**Status:** Complete — ready for synthesis with Player Kael report

---

## Friction Report — GM Perspective

### 🔴 Blockers (I literally can't do this)

| # | Issue | Impact |
|---|---|---|
| B1 | **No concept of Groups (A/B/C) in the data model or UI** | Three parties exist but the app has no way to tag, filter, or view by group. Managing this in my head or a spreadsheet defeats the purpose of having a companion app. |
| B2 | **No session roster / "Current Party View"** | Can't answer "who's showing up tonight and what are they bringing?" Still need a Discord message thread for session coordination. (Approved in concept — but doesn't exist yet.) |
| B3 | **No combat-relevant stats at a glance** | Character list shows names and sync timestamps only. Need initiative, condition monitor, edge remaining for the whole party at a glance. 12-16 clicks minimum for a cross-group session of 6-8 characters. |
| B4 | **No way to un-assign or re-assign a character** | Assign Characters page only shows unclaimed characters. Once assigned, no undo. Player drops out? Misclick? Stuck. |
| B5 | **Character list has no player ownership info** | Flat list of character names — can't tell at a glance who owns what. "Can you check Razor's spells?" requires clicking into every character. |
| B6 | **No bulk library operations** | Updating a field across 20 spells (homebrew errata) means 20 individual edit-save-navigate cycles. 30-minute task that should take 30 seconds. |

### 🟡 Friction (I can do it, but it's painful)

| # | Issue | Impact |
|---|---|---|
| F1 | **Admin section is a single page with one function** | "Assign Characters" is the entire admin experience. No dashboard, no campaign overview, no at-a-glance health check. Feels like an afterthought. |
| F2 | **No player roster page** | Can't see players with their characters, join date, last active. Only place players appear is the assign dropdown. |
| F3 | **Raw database timestamps** | Worse for GM than players — need staleness detection. "This character hasn't synced in 3 weeks" matters for data trust. |
| F4 | **Library CRUD has no duplicate detection** | 540 entries — duplicates will happen. No dedup, no "did you mean?" on create. |
| F5 | **No confirmation/success feedback on library create/edit** | Silent redirect after save. Did it save? Did validation fail silently? No toast or flash message. |
| F6 | **Spirits form has 14 fields, zero guidance** | No placeholders or hints. What format for formula fields? "F+3"? "Force+3"? Free text? |
| F7 | **No way to preview what players see** | Can't toggle off GM controls to see the player experience. Useful for onboarding and QA. |
| F8 | **Landing page shows player onboarding message to GM** | "Ask your GM to assign you" — but I AM the GM. Should route me to admin tasks. |
| F9 | **Filter labels use raw field names** | Players see `pp_cost` and `drain_type` — makes the GM look bad for setting up the catalogs. |
| F10 | **No campaign-level settings page** | Campaign name, sync secret status, player count, character count — all invisible. Campaign exists in DB but has no UI. |
| F11 | **No control over library entry ordering** | Entries in insertion order. Can't reorder, pin, or set default sort. |

### 🟢 Smooth (This works well)

| # | What Works | Why It's Good |
|---|---|---|
| S1 | GM-only visibility of CRUD actions | Edit/New buttons only appear for GM. Clean separation. |
| S2 | Inline delete confirmation | In-page state toggle, no `window.confirm()`. No accidental deletions. |
| S3 | CatalogForm shared between create and edit | One component, two uses. Consistency matters when maintaining 540 entries. |
| S4 | Character detail is comprehensive | 5 tabs, all 10 rep sections, computed stats, money, karma, milestones. |
| S5 | Sync version tracking | `sync_version` visible on character detail — breadcrumb to debug sync issues. |
| S6 | Catalog-config as single source of truth | One file defines columns, filters, and form fields per catalog. |
| S7 | Auth guard pattern | `requireGm()` in actions, `parent()` checks in loads. Trust the access control. |

---

## Feature Wishlist — GM Perspective

### Must-Have (Every session / every prep session)

1. **Player Roster Dashboard** — GM admin home base: all players, their characters (grouped by player), group assignment (A/B/C), last active, links to character detail.
2. **Group/Party data model** — Characters need group membership. Groups A, B, C as first-class concepts, not organizational afterthoughts.
3. **Current Party View (session roster)** — "New Session" workflow: select deploying characters, see initiative order, condition monitor summary, edge remaining, active sustained spells.
4. **Re-assign / Un-assign characters** — Edit ownership. Player drops out? Reassign. Misclick? Undo.
5. **Character list enrichment** — Show owner, group, key combat stats, staleness indicator. Sort and filter by these fields.
6. **GM landing page / campaign dashboard** — Campaign name, player count, character count by group, recently synced, stale characters, quick links to admin.

### Nice-to-Have (Regular use, can live without initially)

7. **NPC quick-reference cards** — Lightweight: name, key stats, threat level, notes. Not full character sheets. For encounter reference.
8. **Session notes / journal** — Per-session log: date, deployed characters, what happened, GM-private notes. Campaign continuity tool.
9. **Bulk library edit** — Multi-select → apply field change. Even CSV import/export would help manage 540 entries.
10. **Library entry versioning / changelog** — `updated_at` + optional `changelog_note`. Players will call out undocumented changes.
11. **Form field hints/placeholders** — "e.g. F+3" for formula fields, "e.g. +2 dice for Detection spells" for advantages.
12. **Global search for GM** — Cross-catalog search doubles as duplicate detection before creating entries.
13. **"Impersonate player" view toggle** — See app as a specific player. Useful for onboarding walkthroughs.
14. **Dark mode** — Evening sessions. Bright white at 10 PM hurts.

### Dream (Vision features)

15. **Cross-group encounter tracker** — Session roster evolved: shared initiative with GM annotations (threat notes, plot hooks per character).
16. **Lore wiki / shared knowledge base** — Markdown pages by topic. Players see published; GM sees drafts. Character detail links to relevant lore.
17. **Player-facing session prep** — Players mark which character(s) they're deploying before a session. GM sees choices in real-time.
18. **Automated sync staleness alerts** — Visual flag for 14+ day stale characters. Drift indicator if Roll20 sheet modified but not synced.
19. **Party treasure / shared resources** — Group-level gold, items, resources. Currently in the Karma Tracker workbook — centralize in app.

---

## Priority Stack — Honest GM Ranking

### Tier 1: "I'll actually open this app every week"
- Player Roster Dashboard (#1)
- Group data model (#2)
- Current Party View / session roster (#3)
- Re-assign/un-assign characters (#4)
- GM landing page (#6)

### Tier 2: "Makes session prep significantly faster"
- Character list enrichment (#5)
- Session notes/journal (#8)
- NPC quick-reference cards (#7)
- Global search (#12)

### Tier 3: "Library quality-of-life"
- Bulk library operations (#9)
- Form hints/placeholders (#11)
- Library versioning (#10)
- Dark mode (#14)

### Tier 4: "Vision features — defines what this app becomes"
- Lore wiki (#16)
- Player-facing session prep (#17)
- Cross-group encounter tracker (#15)
- Party treasure (#19)

---

## Cross-Reference with Player Kael Report

| Player Kael Finding | GM Agreement | GM Priority Shift |
|---|---|---|
| B1 — No mobile responsive | Agree — but less critical for GM (desktop prep) | Drops to Nice-to-Have for GM |
| B2 — No column sorting | Agree — needed for library management too | Same priority |
| B3 — No drain filter | Agree — but GM cares about *all* filter gaps | Subsumed by broader filter coverage |
| B4 — No cross-referencing | Agree — essential for everyone | Same priority |
| B5 — No global search | Agree — doubles as duplicate detection for GM | Elevated for GM |
| B6 — Missing filters | Agree — built the catalogs, they should be filterable | Same priority |
| F6 — Raw UTC timestamps | Agree — worse for GM (staleness matters) | Elevated for GM |
| F7 — Raw filter labels | Agree — makes GM look bad | Elevated for GM |
| Current Party View | Strongly agree — makes or breaks GM use | Elevated to Must-Have |
| Condition tracking | Agree it's a research item | Same — investigate first |
| Dice roller | Agree it's tabled | Same — deferred |

---

## The Honest Bottom Line

> Right now, this app is a **library browser with character viewing**. The library CRUD is solid — clean forms, good config-driven architecture, proper auth guards. But the GM *workflow* hasn't been built yet.

> The app does things a GM needs to do *to items* (create/edit/delete library entries), but not things a GM needs to do *to sessions* (roster, prep, coordinate, track).

> **The single highest-impact investment is the session roster / Current Party View.** If I can see tonight's party with combat stats, that alone justifies keeping the app open during play.

> Second priority: **the GM dashboard and player roster.** Show me my campaign, my players, my groups. Make me feel like I'm managing a campaign, not browsing a database.
