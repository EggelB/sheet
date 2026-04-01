# Enemies in the Shadows — TTRPG Toolkit

A complete toolkit for running the **Enemies in the Shadows** tabletop RPG campaign, built on a Shadowrun-hybrid game system. This repository contains:

1. **Roll20 Character Sheet** — A custom HTML/CSS character sheet with Sheet Worker automation
2. **Companion Web App** — A SvelteKit application for campaign management (GM dashboard, character sync, library, session tracking)
3. **Game Element Data** — Structured JSON data files powering both the sheet and the companion app

## Repository Structure

```
sheet/
├── roll20/                  # Roll20 custom character sheet
│   ├── sheet.html           #   HTML template
│   ├── sheet.css            #   Stylesheet
│   └── sheet.json           #   Sheet metadata (tabs, attributes, templates)
│
├── companion/               # SvelteKit companion web app
│   ├── src/                 #   Application source code
│   ├── db/                  #   Database schema (Turso/SQLite)
│   ├── scripts/             #   Migration and seed scripts
│   ├── package.json         #   Node dependencies
│   ├── wrangler.toml        #   Cloudflare Pages deployment config
│   └── .dev.vars            #   Local secrets (not committed)
│
├── elements/                # Game system data
│   ├── *.json               #   Structured data (attributes, skills, spells, etc.)
│   ├── *.xlsx               #   Excel reference workbooks (local-only, gitignored)
│   ├── *.png                #   Reference images (local-only, gitignored)
│   └── 1-6. */              #   Obsidian .md source materials (local-only, gitignored)
│
├── mcp_servers/             # TEMPO MCP servers (AI development tooling)
│   ├── base/                #   Base agent server
│   ├── executor/            #   Code quality gates
│   ├── memory/              #   Project memory persistence
│   ├── session/             #   Workflow state management
│   ├── workflow/            #   Shape→Fill routing engine
│   └── tests/               #   Test suite
│
└── .github/                 # AI agent configuration & project plans
    ├── agents/              #   Custom VS Code Copilot agents
    ├── plans/               #   CCE planning artifacts (Layer 1-5)
    ├── playbooks/           #   TEMPO methodology playbooks
    ├── prompts/             #   Reusable reasoning prompts
    ├── decision-trees/      #   Conflict resolution logic
    ├── exploits/            #   Advanced technique methodologies
    └── reference/           #   CCE rationale documentation
```

## Tech Stack

| Component | Technology |
|---|---|
| Character Sheet | HTML, CSS, JavaScript (Roll20 Sheet Workers) |
| Companion App | SvelteKit 2 + Svelte 5 (runes) |
| Hosting | Cloudflare Pages |
| Database | Turso (libSQL/SQLite) |
| Authentication | Discord OAuth via Auth.js |
| Character Import | SheetJS (xlsx) — client-side Excel parsing |
| AI Tooling | Python MCP servers (TEMPO methodology) |

## Prerequisites

- **Node.js** >= 18
- **Python** >= 3.11 (for MCP servers only)
- **npm** (comes with Node.js)

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd sheet
```

### 2. Companion App Setup

```bash
cd companion
npm install
```

Create `companion/.dev.vars` with your secrets:

```
TURSO_DATABASE_URL=libsql://your-database.turso.io
TURSO_AUTH_TOKEN=your-auth-token
AUTH_SECRET=your-auth-secret
AUTH_DISCORD_ID=your-discord-client-id
AUTH_DISCORD_SECRET=your-discord-client-secret
```

Run database migrations and seed reference data:

```bash
npm run migrate
npm run seed
npm run seed-campaign
```

Start the dev server:

```bash
npm run dev
```

### 3. MCP Servers Setup (optional — for TEMPO AI tooling)

```bash
cd ..
python -m venv .venv
.venv/Scripts/Activate.ps1   # Windows
pip install -r mcp_servers/requirements.txt
```

The MCP servers are configured in `.vscode/mcp.json` and start automatically when VS Code Copilot invokes them.

### 4. Roll20 Sheet

The files in `roll20/` are used by copying the HTML and CSS directly into Roll20's Custom Sheet Sandbox. No build step required.

## Game System Reference

The `elements/` folder contains both **committed** data and **local-only** reference materials:

**Committed (JSON):** Structured game data used by the sheet and companion app — attributes, skills, conditions, dice pools, karma, mutations, spells, initiative, and character templates.

**Local-only (gitignored):** Excel workbooks (`.xlsx`), reference images (`.png`), and the GM's Obsidian vault exports (numbered folders `1. Combat/` through `6. Magic/`). These are source materials for data modeling and comparison — they don't need to be in the repository.

## Campaign: Enemies in the Shadows

- **Players:** 5
- **Groups:** A, B, C
- **Currency:** Gold crowns (GC), Silver stags (SS), Copper pennies (CP)
- **System:** Shadowrun-hybrid with custom mutations, milestones, and adept powers

## Development

This project uses the **TEMPO** (Tactical Execution & Methodology Protocol Orchestrator) methodology with Cascading Context Expansion for planning and development. Planning artifacts live in `.github/plans/`.

### Common Commands

| Command | Location | Description |
|---|---|---|
| `npm run dev` | `companion/` | Start dev server |
| `npm run build` | `companion/` | Production build |
| `npm run check` | `companion/` | Svelte type checking |
| `npm run migrate` | `companion/` | Run database migrations |
| `npm run seed` | `companion/` | Seed reference data |
| `npm run seed-campaign` | `companion/` | Seed campaign data |
| `pytest mcp_servers/tests/` | repo root | Run MCP server tests |

## License

Private — not for public distribution.
