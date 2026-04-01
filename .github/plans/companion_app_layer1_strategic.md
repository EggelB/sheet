# Companion App -- Layer 1: Strategic Summary

## Project Overview

Build a companion web application for a custom TTRPG campaign (medieval Shadowrun 3e variant) serving 6 players (~18 characters). The app has two roles:

1. **Game Library** -- A curated catalog of all game items (spells, weapons, armor, equipment, skills, adept powers, mutations) seeded from the GM's Excel workbooks and maintainable through the app.
2. **Character Viewer** -- A read-only character sheet viewer displaying data synced from Roll20, enriched with computed derived fields.

The app connects to the Roll20 character sheet (already built, HTML+CSS+Sheet Workers) via a one-way sync endpoint -- characters push data from Roll20 to the companion app's database.

## Architecture Decisions (Locked)

| Decision | Choice | Rationale |
|---|---|---|
| Framework | SvelteKit on Cloudflare Pages | Single deployment, edge runtime, server-side rendering |
| Database | Turso (libSQL) | Free tier, no dormancy risk, HTTP API from CF Workers |
| Auth | Discord OAuth via @auth/sveltekit | Per-player ownership; GM uses inter-character secrecy |
| Sync model | Full-snapshot push from Roll20 | Simple, atomic, no delta complexity at ~2.5KB/character |
| Deployment | Single SvelteKit app (sync endpoint = API route) | One wrangler.toml, one set of secrets |
| Repo | companion/ subdirectory in existing sheet repo | Solo maintainer, shared context |

## The Reference Data Problem

### Source Material Inventory

8 Excel workbooks contain the campaign's game reference data:

| Workbook | Content | Approx. Records | Key Columns |
|---|---|---|---|
| Spells.xlsx | 9 spell categories, ~60+ spells | 60-80 | Name, Type(M/P), Target, Duration, Drain, Description |
| Equipment.xlsx > Weapons | Edged, Clubs, Projectile weapons | ~20 | Name, Conceal, Reach, Damage, EP, Cost |
| Equipment.xlsx > Armor | Light/Medium/Heavy + Shields + Helmets | ~15 | Name, Location, Conceal, P/S/I ratings, EP, Cost |
| Equipment.xlsx > Equipment | Adventure gear, tools, containers | ~100+ | Name, Conceal, EP, Cost, Notes |
| Skills.xlsx | Skills with linked attributes | ~40+ | Name, Linked Attribute, Category, Specializations |
| Adept Powers and Mutations.xlsx > Powers | Physical adept powers | ~20+ | Name, PP Cost, Description, Game Effect |
| Adept Powers and Mutations.xlsx > Mutations | Biological mutations | ~20+ | Name, Essence, BP Cost, Description, Game Effect |
| Totems and Spirits.xlsx | Spirit types + elementals | 18 types | Type, stat formulas (already built into Roll20 sheet) |

### Master Data vs Instance Data

This is the core architectural tension the user identified:

- **Master data (catalog):** The curated library of game items. Seeded from Excel, editable by GM.
- **Instance data (character):** What a specific character actually has on their sheet. Synced from Roll20.
- **Custom items:** Equipment, spells, or other items a character acquires during play that don't exist in the original Excels.

### Resolution: Catalog + Character Pattern

**Reference tables** (`ref_spells`, `ref_weapons`, `ref_armor`, `ref_equipment`, `ref_skills`, `ref_adept_powers`, `ref_mutations`) hold the curated game library. These are:
- Seeded from Excel workbooks via a one-time import script
- Browsable by all authenticated players (game library feature)
- Editable by GM only (add new items, correct stats)

**Character repeating tables** (`rep_spells`, `rep_weapons`, `rep_equipment`, etc.) hold instance data synced from Roll20. These:
- May reference a catalog item (by name match -- no foreign key; Roll20 has no concept of catalog IDs)
- May contain custom items that don't exist in the catalog
- Are NEVER written to by the companion app in V1 (read-only character viewing)

**V1 value proposition for reference data:** "What are the stats for a Polearm?" -- players can browse the full game library during and between sessions without digging through Excel files or asking the GM.

**V2+ opportunity:** Character builder UI where picking from catalog auto-fills Roll20 fields, and custom items can be promoted to the catalog by the GM. This is explicitly out of scope for V1.

## Sync Architecture

### Roll20 --> Companion (one-way, outbound only)

The Roll20 sheet already has:
- "Sync to DB" button (`act_btn_sync_db`)
- Sheet Worker handler that collects all scalar fields + (TODO) repeating sections
- `campaign_db_id` and `char_db_id` hidden fields
- `SYNC_PROXY_URL` constant (currently empty string)

The companion app provides:
- `POST /api/sync` endpoint (SvelteKit API route)
- Validates `X-Campaign-Secret` header
- Writes full snapshot to Turso (atomic transaction)
- Returns `{ ok: true, char_db_id, new_sync_version }`

### What Still Needs Building in Roll20

The sync handler in sheet.html does NOT yet collect repeating section data -- `payload.repeating` is hardcoded to `{}`. Before sync is functional, we need to add `getSectionIDs()` calls for all 8 repeating sections and collect their fields into the payload.

## Security Model

- **Discord OAuth** gates all companion app access
- **Player ownership:** Characters are linked to `player_id`; players only see their own characters
- **GM role:** `is_gm` flag in players table (set directly in DB by GM, not self-assignable); grants catalog edit access
- **Campaign secret:** Shared secret for sync endpoint auth. Acceptable residual risk with trusted 6-player group. Turso write token stays server-side only.
- **No public access:** All routes behind auth guard

## Development Phases

### Phase 1: Project Scaffold + Database Schema

**Goal:** Standing SvelteKit project with Turso connected, all tables created.

- Scaffold SvelteKit in `companion/` with `adapter-cloudflare`
- Create Turso database + auth tokens
- Define and run DDL: 12 character tables + 7 reference catalog tables + indices
- Turso client singleton (`@libsql/client/web` for CF Workers runtime)
- Seed script: parse Excel workbooks, populate reference tables
- **Testable:** `npm run dev` starts, seed script populates DB, tables visible in Turso CLI

### Phase 2: Sync Endpoint + Roll20 Wiring

**Goal:** Click "Sync to DB" in Roll20 and data lands in Turso.

- Build `/api/sync` API route with validation pipeline
- Update Roll20 sheet worker to collect repeating section data into sync payload
- First-sync flow: generate UUID for new characters
- Verify: cURL test payload --> data in DB; then live Roll20 sync test
- **Testable:** Full round-trip from Roll20 character to Turso row

### Phase 3: Auth + Character Viewer

**Goal:** Log in with Discord, see your characters, view full read-only sheet.

- Discord OAuth setup (Auth.js + provider config)
- Player upsert on first login
- Character list page (my characters)
- Character detail page (tabbed read-only view mirroring Roll20 layout)
- `computed.ts` for derived fields (attribute totals, pools, etc.)
- **Testable:** Login --> character list --> click character --> full sheet renders

### Phase 4: Game Library

**Goal:** Browse the curated catalog of all game items.

- Library index page with category navigation
- Spells browser (filterable by category, type, searchable by name)
- Weapons/Armor/Equipment browser
- Skills reference
- Adept Powers + Mutations browser
- GM edit capability (add/edit catalog entries, gated by `is_gm`)
- **Testable:** Any authenticated player can browse full game library; GM can add items

## Scope Boundary: What This Project Is NOT

- Not a character builder (V2+ if ever -- requires write-back to Roll20)
- Not a combat tracker or dice roller
- Not a campaign manager or session log
- Not a GM-facing admin dashboard (beyond catalog editing)
- Not a mobile-first app (desktop browser is primary; responsive is nice-to-have)

## Open Questions Requiring User Input

1. **Spirit/Totem data:** The Spirit Calculator is already built into the Roll20 sheet as a real-time calculator. Should the catalog also include spirits/totems as reference entries, or is the on-sheet calculator sufficient?
2. **Money tracking:** Characters have Gold/Silver/Copper fields in Excel but not in the Roll20 sheet currently. Should the companion app track currency, or is that out of scope?
3. **Contacts as reference data:** Contacts in the Excel are more of a GM reference (contact levels, pricing). Should contacts have a reference catalog, or are they purely character-specific?
4. **Seed script persistence:** Should the seed script be re-runnable (idempotent upsert) so the GM can update the catalog from updated Excels, or is a one-time import + manual edits sufficient?

---

# Companion App -- Layer 1: Strategic Summary (Amended)

## Project Overview

Build a companion web application for a custom TTRPG campaign (medieval Shadowrun 3e variant) serving 6 players (~18 characters). The app has two roles:

1. **Game Library** -- A curated catalog of all game items (spells, weapons, armor, equipment, skills, adept powers, mutations, totems, spirits, spirit powers) seeded from the GM's Excel workbooks and maintainable through the app.
2. **Character Viewer** -- A read-only character sheet viewer displaying data synced from Roll20, enriched with computed derived fields. Includes per-character **karma ledger**, **money tracking**, and **milestone progression** views.

The app connects to the Roll20 character sheet (already built, HTML+CSS+Sheet Workers) via a one-way sync endpoint -- characters push data from Roll20 to the companion app's database.

## Architecture Decisions (Locked)

| Decision | Choice | Rationale |
|---|---|---|
| Framework | SvelteKit on Cloudflare Pages | Single deployment, edge runtime, server-side rendering |
| Database | Turso (libSQL) | Free tier, no dormancy risk, HTTP API from CF Workers |
| Auth | Discord OAuth via @auth/sveltekit | Per-player ownership; GM uses inter-character secrecy |
| Sync model | Full-snapshot push from Roll20 | Simple, atomic, no delta complexity at ~2.5KB/character |
| Deployment | Single SvelteKit app (sync endpoint = API route) | One wrangler.toml, one set of secrets |
| Repo | companion/ subdirectory in existing sheet repo | Solo maintainer, shared context |

## Roll20 Sheet Prerequisites

Before the companion app sync is fully functional, the Roll20 sheet itself needs additions:

### New Scalar Fields

| Field | Type | Location | Notes |
|---|---|---|---|
| `money_gold` | number | Core tab (gear section or new) | Gold coins |
| `money_silver` | number | Core tab | Silver coins |
| `money_copper` | number | Core tab | Copper coins |

### New Repeating Sections

**`repeating_karma`** -- Karma event ledger (grants and expenditures):

| Attribute | Type | Notes |
|---|---|---|
| `karma_event` | text | Event name (e.g. "Fight with the ants", "Bought Increase Strength (f6)") |
| `karma_amount` | number | Positive = grant, negative = expenditure |

Existing scalar fields (`karma_good`, `karma_used`, `karma_total`, `karma_pool`) remain; the repeating section provides the detailed log that feeds those totals.

**`repeating_milestones`** -- Custom character advancement paths:

| Attribute | Type | Notes |
|---|---|---|
| `milestone_trial` | text | Trial name (e.g. "Trial of the Leech (Sustaining Spells)") |
| `milestone_tier1` | text | Tier 1 description |
| `milestone_tier2` | text | Tier 2 description |
| `milestone_tier3` | text | Tier 3 description |
| `milestone_current` | number | Current tier achieved (0/1/2/3) |

Milestones are **custom GM-designed advancement paths** unique to each character. Caellum has magic-themed trials (Leech, Centipede, Tick); Rohan has utility/combat trials (Encyclopedic Knowledge, Brain Bud, Whip Mastery). Each trial has 3 progressive tiers of mechanical benefits.

### Sync Handler Completion

The sync handler in sheet.html does NOT yet collect repeating section data -- `payload.repeating` is hardcoded to `{}`. Before sync is functional, we need:
- `getSectionIDs()` calls for all repeating sections (existing 8 + new karma + milestones = 10 total)
- Collect all fields per row into payload
- This is a prerequisite for Phase 2 of companion app development

## The Reference Data Problem

### Source Material Inventory

8 Excel workbooks contain the campaign's game reference data:

| Workbook | Content | Approx. Records | Key Columns |
|---|---|---|---|
| Spells.xlsx | 9 spell categories | ~60-80 spells | Name, Type(M/P), Target, Duration, Drain, Description |
| Equipment.xlsx > Weapons | Edged, Clubs, Projectile | ~20 weapons | Name, Conceal, Reach, Damage, EP, Cost |
| Equipment.xlsx > Armor | Light/Med/Heavy + Shields + Helmets | ~15 items | Name, Location, Conceal, P/S/I ratings, EP, Cost |
| Equipment.xlsx > Equipment | Adventure gear, tools, containers | ~100+ items | Name, Conceal, EP, Cost, Notes |
| Skills.xlsx | Skills with linked attributes | ~40+ skills | Name, Linked Attribute, Category, Specializations |
| Adept Powers and Mutations.xlsx > Powers | Physical adept powers | ~20+ powers | Name, PP Cost, Description, Game Effect |
| Adept Powers and Mutations.xlsx > Mutations | Biological mutations | ~20+ mutations | Name, Essence, BP Cost, Description, Game Effect |
| Totems and Spirits.xlsx > Totems | Animal + Nature totems | 43 totems | Name, Description, Environment, Advantages, Disadvantages |
| Totems and Spirits.xlsx > Spirits | Elementals + Nature Spirits | 4 elementals + 15 nature spirits | Type, B/Q/S/C/I/W/E/R formulas, INTV, Attack, Powers, Weaknesses |
| Totems and Spirits.xlsx > Spirit Powers | Spirit abilities | 18 powers | Name, Type(P/M), Action, Range, Duration, Description |
| Totems and Spirits.xlsx > Elemental Services | Elemental service types | 4 services | Name, Description |

### Totems/Spirits Deep Dive

This is the richest reference dataset:

- **43 Totems** (37 animal + 6 nature): Each has a paragraph-length description, environment, advantages (e.g. "+2 dice for combat spells, +2 dice for forest spirits"), and disadvantages (e.g. behavioral restrictions during combat). These are crucial for character creation and roleplay.
- **19 Spirit Types** (4 elementals + 15 nature spirits): Each has a full stat block with Force-derived attribute formulas (e.g. "B: F+4, Q: F-2(x2), S: F+4"), initiative formulas, attack codes, powers list, and weaknesses. This is the "deeper data" the Spirit Calculator doesn't capture -- the calculator computes stats for a given force, but doesn't show which **powers** each spirit type has or their **weaknesses**.
- **18 Spirit Powers**: Full rules text for each power (Accident, Binding, Concealment, Confusion, Engulf, Fear, Guard, Innate Spell, Materialization, Movement, Noxious Breath, Psychokinesis, Search, etc.). Some have sub-entries (e.g. Fire/Water/Air/Earth Engulf variants).
- **4 Elemental Services**: Aid Sorcery, Aid Study, Physical Service, Spell Sustaining, Remote Service -- each with detailed rules for how they work.

### Master Data vs Instance Data

This is the core architectural tension:

- **Master data (catalog):** The curated library of game items. Seeded from Excel, editable by GM.
- **Instance data (character):** What a specific character actually has on their sheet. Synced from Roll20.
- **Custom items:** Equipment, spells, or other items a character acquires during play that don't exist in the original Excels.
- **Contacts:** Character-specific in-game NPCs. NOT catalog data -- each contact is a unique relationship (e.g. Caellum knows Skaven NPC "Zeezaw"). Already captured as `repeating_contacts` in Roll20.
- **Milestones:** Character-specific GM-designed advancement paths. NOT catalog data -- each character's trials are bespoke.

### Resolution: Catalog + Character Pattern

**Reference tables** hold the curated game library:
- `ref_spells`, `ref_weapons`, `ref_armor`, `ref_equipment`, `ref_skills`, `ref_adept_powers`, `ref_mutations` -- item catalogs
- `ref_totems`, `ref_spirits`, `ref_spirit_powers`, `ref_elemental_services` -- spirit/totem reference
- Seeded from Excel workbooks via the seed utility
- Browsable by all authenticated players (game library feature)
- Editable by GM only (add new items, correct stats)

**Character repeating tables** (`rep_spells`, `rep_weapons`, `rep_equipment`, `rep_contacts`, `rep_karma`, `rep_milestones`, etc.) hold instance data synced from Roll20. These:
- May reference a catalog item (by name match -- no FK; Roll20 has no catalog ID concept)
- May contain custom items that don't exist in the catalog
- Are NEVER written to by the companion app in V1 (read-only character viewing)

## Sync Architecture

### Roll20 --> Companion (one-way, outbound only)

The Roll20 sheet already has:
- "Sync to DB" button (`act_btn_sync_db`)
- Sheet Worker handler that collects all scalar fields + (TODO) repeating sections
- `campaign_db_id` and `char_db_id` hidden fields
- `SYNC_PROXY_URL` constant (currently empty string)

The companion app provides:
- `POST /api/sync` endpoint (SvelteKit API route)
- Validates `X-Campaign-Secret` header
- Writes full snapshot to Turso (atomic transaction)
- Returns `{ ok: true, char_db_id, new_sync_version }`

### What Still Needs Building in Roll20

See "Roll20 Sheet Prerequisites" section above. Summary:
- 3 money scalar fields
- `repeating_karma` section (event + amount)
- `repeating_milestones` section (trial + 3 tiers + current)
- Sync handler: `getSectionIDs()` for all 10 repeating sections

## Security Model

- **Discord OAuth** gates all companion app access
- **Player ownership:** Characters are linked to `player_id`; players only see their own characters
- **GM role:** `is_gm` flag in players table (set directly in DB by GM, not self-assignable); grants catalog edit access
- **Campaign secret:** Shared secret for sync endpoint auth. Acceptable residual risk with trusted 6-player group. Turso write token stays server-side only.
- **No public access:** All routes behind auth guard

## Development Phases

### Phase 0: Roll20 Sheet Updates

**Goal:** Add missing fields, remove 20 Questions (companion app owns that data), and complete sync handler in Roll20 sheet.

- Add `money_gold`, `money_silver`, `money_copper` scalar fields + UI at top of Gear tab
- Remove 20 Questions (Q1-Q20) from Bio tab — companion app will own this data directly; frees space for new sections
- Add `repeating_karma` section (event, amount) + UI on Bio tab (below Description/Notes)
- Add `repeating_milestones` section (trial, tier1, tier2, tier3, current) + UI on Bio tab (below karma ledger)
- Complete sync handler: `getSectionIDs()` for all 10 repeating sections; remove bio_q fields from sync payload
- **Testable:** New fields visible in Roll20; 20 Questions removed from Bio tab; sync button collects full payload including repeating sections

### Phase 1: Project Scaffold + Database Schema + Seed Utility

**Goal:** Standing SvelteKit project with Turso connected, all tables created, reference data seeded.

- Scaffold SvelteKit in `companion/` with `adapter-cloudflare`
- Create Turso database + auth tokens
- Define and run DDL: character tables (scalars + 10 repeating section tables) + 11 reference catalog tables + indices
- Turso client singleton (`@libsql/client/web` for CF Workers runtime)
- **Seed utility:** Proper CLI tool (`companion/scripts/seed.ts` or similar) that:
  - Parses all Excel workbooks from `plans/`
  - Populates reference tables via idempotent upsert (re-runnable)
  - Can be run in CI/CD or locally
  - Reports: "Inserted N new, updated M existing, skipped K unchanged"
- **Testable:** `npm run dev` starts, seed utility populates DB, tables visible in Turso CLI

### Phase 2: Sync Endpoint + Roll20 Wiring

**Goal:** Click "Sync to DB" in Roll20 and data lands in Turso.

- Build `/api/sync` API route with validation pipeline
- Atomic Turso transaction: upsert character scalars + delete-and-reinsert repeating sections
- First-sync flow: generate UUID for new characters
- Verify: cURL test payload --> data in DB; then live Roll20 sync test
- **Testable:** Full round-trip from Roll20 character to Turso row

### Phase 3: Auth + Character Viewer

**Goal:** Log in with Discord, see your characters, view full read-only sheet.

- Discord OAuth setup (Auth.js + provider config)
- Player upsert on first login
- Character list page (my characters)
- Character detail page -- tabbed read-only view including:
  - Core stats, attributes, pools
  - Skills, spells, foci, gear, contacts (mirroring Roll20 layout)
  - **Money** (Gold/Silver/Copper display)
  - **Karma ledger** (event log with running total, filterable grants vs expenditures)
  - **Milestone paths** (trial cards with tier progression visualization)
- `computed.ts` for derived fields (attribute totals, pools, etc.)
- **Testable:** Login --> character list --> click character --> full sheet renders with all tabs

### Phase 4: Game Library

**Goal:** Browse the curated catalog of all game items and rules reference.

- Library index page with category navigation
- **Spells browser** (filterable by category + type, searchable by name)
- **Weapons/Armor/Equipment browser** (filterable, searchable)
- **Skills reference** (grouped by linked attribute)
- **Adept Powers + Mutations browser**
- **Totems browser** (animal + nature, with full descriptions + mechanical effects)
- **Spirits reference** (elemental + nature spirit stat blocks, powers list per type)
- **Spirit Powers reference** (full rules text, organized by power name)
- **Elemental Services reference** (rules text)
- GM edit capability (add/edit catalog entries, gated by `is_gm`)
- **Testable:** Any authenticated player can browse full game library; GM can add items

## Table Count Summary

| Category | Tables | Count |
|---|---|---|
| Character scalars | `characters` | 1 |
| Character repeating | `rep_skills`, `rep_mutations`, `rep_adept_powers`, `rep_spells`, `rep_foci`, `rep_weapons`, `rep_equipment`, `rep_contacts`, `rep_karma`, `rep_milestones` | 10 |
| Reference catalog | `ref_spells`, `ref_weapons`, `ref_armor`, `ref_equipment`, `ref_skills`, `ref_adept_powers`, `ref_mutations`, `ref_totems`, `ref_spirits`, `ref_spirit_powers`, `ref_elemental_services` | 11 |
| Auth/meta | `players`, `campaigns` | 2 |
| **Total** | | **24** |

## Scope Boundary: What This Project Is NOT

- Not a character builder (V2+ if ever -- requires write-back to Roll20)
- Not a combat tracker or dice roller
- Not a campaign manager or session log
- Not a GM-facing admin dashboard (beyond catalog editing)
- Not a mobile-first app (desktop browser is primary; responsive is nice-to-have)
- Not a party treasure tracker (party-level loose coin and shared items are GM-managed in Excel; only per-character money is synced)

## Resolved Questions

| # | Question | Answer |
|---|---|---|
| 1 | Spirit/Totem catalog? | **Yes.** Include as reference data. Totems (43) + Spirits (19 types + stat blocks) + Spirit Powers (18) + Elemental Services (4). This is the richest reference dataset -- the Spirit Calculator computes stats but doesn't show powers, weaknesses, or totem descriptions. |
| 2 | Money tracking? | **Yes.** Add Gold/Silver/Copper scalar fields to Roll20 sheet. Sync to companion. Simple display only -- no ledger, just current balances. |
| 3 | Contacts as reference? | **No catalog.** Contacts are character-specific in-game NPCs (e.g. Caellum ↔ Zeezaw). Already captured in `repeating_contacts`. No reference table needed. |
| 4 | Seed script persistence? | **Proper CI/CD tool.** Idempotent upsert, re-runnable, reports stats. Not a one-time throwaway script. |
| 5 | Karma tracker? | **Yes.** New `repeating_karma` section on Roll20 sheet. Event-based ledger (grant/expenditure entries). Companion app shows full log with running total. |
| 6 | Milestone paths? | **Yes.** New `repeating_milestones` section on Roll20 sheet. Trial name + 3-tier descriptions + current tier. Companion app renders progression cards. |