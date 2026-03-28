# Roll20 Character Sheet — Layer 1: Strategic Summary (v2 — Revised for Multi-Player + Database)

## Project Overview
Build a custom TTRPG character sheet **template** for 6 players (each with ~2-3 characters) on the Roll20 VTT platform. The system is a custom game combining Shadowrun-style mechanics with medieval fantasy. The end-state is a reusable sheet template all 6 players deploy for each of their characters, with a lightweight companion database for character management outside Roll20.

## Characters Inventoried (Bryce's 3 — canonical validation targets)
| Character | Race/Station | Age | Archetype | Magic |
|---|---|---|---|---|
| Breit the Wide | Human / Serf | 32 | Bear Shaman (Conjurer) | No (0) |
| Rohan Drake | Human / Professional | 25 | Anthropologist / Scholar | No (0) |
| Caellum | Human / Peasant | 17 | Full Sorcerer / Poisoner | Yes (6) |

Estimated total scale: 6 players × ~3 characters = ~18 character sheets. ~180KB total data. Trivial storage — constraint is dormancy behavior on free tiers, not volume.

## Critical Roll20 Architecture Findings (from Deep Research)
- Roll20 Sheet Workers are a single-script-tag, callback-only sandbox — ZERO external HTTP calls allowed. No fetch(), no axios, no external DB access from within the sheet.
- Roll20 Pro tier is required to upload a Custom Character Sheet to a game. (Free/Plus cannot upload custom sheets.)
- Beacon SDK is gated to commercial publishers — NOT available for homebrew games. Do not use.
- Roll20's built-in attribute persistence is fully sufficient at 18-character scale. Each character = one Roll20 Character object using the shared template.
- K-scaffold (open-source Roll20 Sheet Worker framework) significantly reduces Sheet Worker complexity and is recommended for maintainability.
- The "chat bridge" pattern (Roll20 Pro API Mod + findObjs/set) is the only Roll20-native external sync mechanism, but adds complexity we should avoid unless specifically needed.
- repeating_sectionname fieldsets are how Roll20 handles dynamic lists. Attribute name format: repeating_skills_$0_skill_base_rating. This must be designed carefully upfront — renames break all macros.

## Database Options Analysis
| Option | VTT Integration | Dormancy Risk | Dev Effort | Cost | Verdict |
|---|---|---|---|---|---|
| Roll20 Native Only | Native | None | Low | Included w/ Pro | ✅ Sufficient for pure VTT play |
| Supabase Free | External (companion app) | HIGH — pauses after 1 week inactive | Medium | Free / $25/mo | ❌ Disqualified — hobby groups go dormant |
| Firebase Firestore | External (companion app) | None | Medium | Free tier generous | ✅ Viable for companion app |
| Turso (libSQL) | External (companion app) | None | Low-Medium | Free (5GB, HTTP API) | ✅ Best lightweight option |
| PocketBase | External (self-hosted) | None (self-hosted) | Medium | Free (self-host cost) | ⚠️ Pre-v1.0 instability risk |
| localStorage only | None (browser-local) | None | Lowest | Free | ❌ No multi-player or cross-device |

## Recommended Architecture: Two-Layer System

### Layer A: Roll20 Native Sheet (Primary VTT Interface)
The custom HTML+CSS+Sheet Worker sheet lives entirely within Roll20. All in-session play — rolls, attribute tracking, condition monitor — happens here. Roll20 handles persistence natively. This is the primary deliverable.

### Layer B: Companion Character Builder Web App (Secondary — Nice to Have)
A simple web app where players can build/view/export their characters between sessions. Uses Turso (free edge SQLite, HTTP API, no dormancy risk) as the database. Characters can be exported as JSON and imported into Roll20 via a chat command bridge or manual attribute entry. This layer is decoupled — it can be built after the Roll20 sheet is complete.

**Rationale for separation:** Roll20 Sheet Workers cannot touch an external DB. The companion app is purely additive — players can use the sheet without it. Building it second means we don't gate Phase 1-4 on web infrastructure.

## Revised Development Phases (5 Phases)

### Phase 1: Data Architecture & Roll20 Attribute Naming Contract
Goal: Lock the complete data contract before writing any UI. This is the highest-leverage planning work in the whole project.
- Map every field to a Roll20-safe attr_name (lowercase_snake_case, no spaces, no special chars)
- Design all repeating_ section schemas with full attribute path examples
- Build the attribute dependency graph: what Sheet Worker events trigger which recalculations
- Define the Sheet Worker listener registration map
- Determine which attributes are current_value tracked (condition checkboxes, editable fields) vs computed (dice pools, reaction)
- Justification: Attribute name renames in Roll20 break ALL player macros retroactively. Lock them first.

### Phase 2: HTML Structure & CSS Design System
Goal: Build the visual shell — all sections, tabs, inputs wired, styled.
- Tabbed layout: [Main] [Skills] [Inventory] [Spells/Mutations] [Notes]
- Dark theme CSS design system with variables — matches Roll20's dark UI
- All Roll20 name="attr_*" inputs placed in HTML
- Condition monitor: tiered checkbox grid with red fill on check, TN/Init modifier labels
- Armor location table (Torso / Legs / Head × Piercing/Slashing/Impact)
- repeating_ fieldsets for all dynamic lists with Add/Remove row buttons (Roll20's native pattern)
- Justification: Visual HTML shell can be tested locally and in Roll20's sheet sandbox before any JS.

### Phase 3: Sheet Worker Logic & Auto-Calculations
Goal: Wire all derived stats so they auto-update when inputs change.
- Reaction = Math.floor((int_total + dex_total) / 2)
- Attribute totals = base + mutations + magic + misc
- Dice Pools: Spell=(cha+int+wil)/2, Combat=(dex+int+wil)/2, Control=reaction, Astral=(int+wil+mag)/3 (all floor'd)
- Condition monitor: count filled boxes per tier per track → drive tn_modifier and init_modifier attributes
- Karma Pool = Math.floor(karma_total / 10) + 1
- Skill cost calculation (tiered: 1:1 up to linked attr, 2:1 above)
- Mutation humanity cost sum → drives magic_base value
- Use K-scaffold to reduce boilerplate and register listeners cleanly
- Justification: Sheet Workers are the heart of Roll20 automation. K-scaffold makes this maintainable at ~20+ listeners.

### Phase 4: Roll Buttons, Dice Integration & Roll Templates
Goal: Make every roll in the game clickable.
- Custom Roll Template: branded result card (character name, roll type, dice result, TN)
- Initiative: button → [[1d6 + @{reaction} + @{init_misc_mod} - @{init_condition_penalty}]]
- Dice Pool buttons (Spell / Combat / Control / Astral) with current TN display
- Skill roll buttons in the repeating_skills section: pull linked attr total + skill total, roll pool
- Weapon roll (Power + damage type, range band selector)
- Spell roll (Force, Drain, TN from spell record)
- Justification: Roll integration is the unique value proposition of Roll20 vs a static sheet.

### Phase 5: Companion Builder Web App + Character Migration
Goal: Build the optional external layer and migrate all characters.
- Simple HTML+JS (or minimal framework) web app against Turso DB
- Character CRUD: create, view, edit, delete characters
- Export to JSON (for Roll20 manual import or chat bridge)
- Populate Breit, Rohan, Caellum in Roll20 sheet — validate math against XLSX source
- Document the sheet setup process for the other 5 players
- Justification: Companion app is additive and migration is last — both should land on a stable template.

## Scope Boundary: What This Project Is NOT
- Not a real-time sync system between Roll20 and the companion app (chat bridge complexity not justified at hobby scale)
- Not a campaign manager or GM tool
- Not a mobile app
- Not a multi-campaign system (scoped to this one game)

## Prior Work Assessment
| Asset | Fate |
|---|---|
| elements/*.json | ✅ Direct input to Phase 1 attribute naming |
| plans/phase1_data_modeling.md | ✅ Data model carries over; architecture sections superseded |
| plans/phase1_application_architecture.md | ⚠️ localStorage/DOM pattern superseded by Roll20 native + companion split |
| archive/Test_ver3.html | ✅ CSS patterns for condition monitor + tabs are reusable |
| mcp_servers/ | ✅ TEMPO infrastructure unchanged |

## Open Questions Requiring User Input
1. Does Bryce (or the GM) have Roll20 Pro? (Required to upload custom sheets.)
2. Is the companion web app in Phase 5 a real requirement, or is Roll20-native-only sufficient?
3. Should spells and mutations be visible/rollable from the main Roll20 interface, or just as reference data?
4. Are there any other game mechanics not captured in the XLSX (combat maneuvers, status effects, etc.)?
