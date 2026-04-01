# Kael Player Report — Companion App UX Evaluation

**Date:** 2026-04-01  
**Persona:** Player (experienced TTRPG player, first time using this companion app)  
**Agent:** Human Preference (Kael)  
**Status:** Complete — awaiting GM-Kael before Layer 1 planning

---

## Friction Report

### Blockers (Cannot Complete Core Task)

| # | Issue | Impact |
|---|---|---|
| B1 | No mobile/responsive layout | Library and character pages unusable on phones/tablets at the table |
| B2 | No column sorting | Cannot find items in long catalog lists (e.g., 156 spells) without alphabetical sort |
| B3 | No drain filter | Spells missing the single most important filter for in-play reference |
| B4 | No cross-referencing | Character skills/spells don't link to library entries — must manually navigate |
| B5 | No global search | Cannot search across all catalogs at once — must check each individually |
| B6 | Equipment, Mutations, Adept Powers have no filters | Three catalogs with no way to narrow results |

### Friction (Slows Me Down)

| # | Issue | Impact |
|---|---|---|
| F1 | Overwhelming sub-nav | 11 catalog links shown at all times — cognitive overload |
| F2 | One-at-a-time expand | Expanding a row collapses any other — can't compare two items side by side |
| F3 | Name-only search | Search box only matches name field; can't find items by description content |
| F4 | No URL tab anchors | Sharing a link to "my character's skills tab" is impossible — tab state not in URL |
| F5 | Useless landing page | Library index just shows card grid with counts — no guidance or orientation |
| F6 | Raw UTC timestamps | "2026-03-31T22:14:07Z" means nothing to a player — should be relative ("2 hours ago") |
| F7 | Raw field name filter labels | Labels like "pp_cost" and "drain_type" shown to users instead of human-readable names |
| F8 | No catalog intros | Player arrives at "Spells" with no context about what the catalog contains |
| F9 | Confusing karma labels | Karma fields use internal naming that doesn't match player mental model |

### Smooth (Working Well)

| # | What Works | Why It's Good |
|---|---|---|
| S1 | Library card grid | Visual, scannable, good information density |
| S2 | Character detail tabs | Logical grouping, keeps long character sheets manageable |
| S3 | Expandable rows | Click to see details without leaving the list — excellent pattern |
| S4 | Instant client-side filtering | No page reload, feels responsive and modern |
| S5 | Sync metadata | Players can see when their character was last synced |

---

## Feature Wishlist

### Must-Have (Required for regular use)

1. **Mobile responsive layout** — Card grid, filter sidebar, character tabs must work on phone screens
2. **Column sorting** — Click column headers to sort ascending/descending
3. **Cross-link character to library** — Character's skills/spells/powers link directly to library detail
4. **Global search** — Single search box that queries across all catalogs
5. **Better filter coverage** — Add filters to Equipment, Mutations, Adept Powers catalogs
6. **Full-text search in descriptions** — Search should match description/notes content, not just name

### Nice-to-Have (Would use frequently)

7. **"My Stuff" filter** — Show only items my character actually has (cross-reference character data)
8. **Favorites / bookmarks** — Star items for quick access during sessions
9. **Relative timestamps** — "2 hours ago" instead of ISO 8601
10. **Tab URL state** — Character tab selection persisted in URL hash for sharing
11. **Side-by-side comparison** — Compare two items (spells, weapons) in a split view
12. **Dark mode** — Essential for evening/in-person game sessions
13. **Catalog grouping** — Sub-categories within large catalogs (Combat Spells, Detection Spells, etc.)
14. **Intro descriptions** — Brief flavor text at top of each catalog page explaining the category

### Dream (Aspirational)

15. **Session notes / journal** — Per-session notes attached to character, viewable by GM
16. **Current Party View** — Drag-and-drop session roster. Players pick which PC(s) they're running for a given session — could be one, could be all. Supports cross-group composition (some from Group A, some from Group B). Shows need-to-know summary (initiative, condition monitor, edge remaining), not full character sheets.
17. **Condition tracking (bidirectional sync)** — *Investigate feasibility.* Would require the companion app to push condition state back to the Roll20-native character sheet, not just read from it. Amazing feature if feasible, but Roll20 API constraints may block it. Research item.
18. **Quick-reference combat card** — One-page summary of combat-relevant stats, initiative, weapons, active spells
19. **Offline PWA** — Cache library data for use without internet (conventions, basements)
20. **Dice roller** — *Tabled for future version.* Roll20's `startRoll`/`finishRoll` API is proprietary and non-portable. Core UX must be airtight first. Revisit in a later release cycle.

---

## User Refinements

### Current Party View Caveats
- **Drag-and-drop session roster**: Not static groups. Players drag their PC(s) into the "current session" roster. One player might run one character, or all of them.
- **Cross-group composition**: Groups A–C exist as organizational concepts, but any session can draw from any group. Party A characters and Party B characters might deploy together.
- **Need-to-know summary**: Shows initiative, condition monitor, edge remaining — not the full character sheet.
- **Multi-party data model**: A single player may have characters in different groups. The data model must support N groups with M characters each, and ad-hoc session rosters that span groups.

### Condition Tracking Caveats
- **Bidirectional sync required**: Current sync is one-way (Roll20 → companion). Condition tracking would require companion → Roll20 writes.
- **Roll20 API constraints**: Sheet workers can read/write attributes, but the companion app would need Roll20 API access (not just sheet worker hooks) to push state back. Feasibility is uncertain.
- **Investigate before designing**: This is a research item. Do not commit design time until Roll20 API capabilities are confirmed.

### Dice Roller — Tabled
- **Deferred to future version**: Core UX must be airtight first. Players already have Roll20 open for rolls.
- **Roll20 API is proprietary**: `startRoll()` / `finishRoll()` are Roll20-specific. Cannot reuse existing sheet worker dice logic.
- **Revisit later**: If the companion app becomes the primary session tool, a standalone web dice roller may justify itself. Not now.

---

## Seed Data Snapshot (at time of report)

| Catalog | Count |
|---|---|
| Spells | 156 |
| Weapons | 21 |
| Armor | 17 |
| Equipment | 99 |
| Skills | 48 |
| Adept Powers | 51 |
| Mutations | 54 |
| Totems | 56 |
| Spirits | 18 |
| Spirit Powers | 15 |
| Elemental Services | 5 |
| **Total** | **540** |
