# TEMPO: Tactical Engine for Multi-agent Process Orchestration

TEMPO is a **4-server MCP (Model Context Protocol) fleet** that runs inside VS Code alongside GitHub Copilot. Each server is a specialised Python process that Copilot can call as a tool. Together they implement the **Cascading Context Expansion (CCE)** methodology — a structured 5-layer workflow for software planning, architecture, implementation, and verification.

---

## Prerequisites

| Requirement              | Minimum version | Notes                                                      |
| ------------------------ | --------------- | ---------------------------------------------------------- |
| Python                   | 3.11            | 3.12 works; 3.10 and below do not                          |
| VS Code                  | 1.90            |                                                            |
| GitHub Copilot extension | Latest          | Chat panel required                                        |
| Git                      | Any             | For cloning                                                |
| `mcp` Python package   | ≥ 1.0          | Installed automatically via `requirements.txt`           |
| Virtual environment      | —              | `.venv/` in the workspace root (created in step 2 below) |

---

## Quick Start

### 1. Clone the repository

```bash
git clone <repo-url>
cd dynamics
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the installer

```bash
python mcp_servers/.install/setup_atlas.py
```

This single command:

- Writes `.vscode/mcp.json` with all 4 server entries pointing to your venv Python
- Writes `.vscode/settings.json` with MCP sampling enabled for every server
- Writes `.vscode/tasks.json` with the four TEMPO helper tasks
- Copies `.github/` content (playbooks, exploits, decision trees) if not already present
- Scaffolds `.github/memory.md` and `.github/workflow-state.json` if they do not exist
- Writes `.copilotignore` if not already present
- Runs a health-check suite (venv packages · server syntax · MCP paths · sampling key)

> **Tip:** To skip the `.github/` copy step (e.g., you've already customised the files):
>
> ```bash
> python setup_tempo.py --no-copy-github
> ```

### 5. Reload VS Code

`Ctrl+Shift+P` → `Developer: Reload Window`

### 6. Verify all servers load

```bash
python mcp_servers/.install/verify_agents.py
```

Expected output: `4/4 servers loaded successfully`.

---

## Server Management

Use `manage_servers.py` to inspect the fleet status without re-running the full installer.

```bash
# List all servers with current status (ENABLED / DISABLED / PATH MISSING)
python mcp_servers/.install/manage_servers.py list

# Show detailed status
python mcp_servers/.install/manage_servers.py status
```

**All 3 servers are CORE** — disabling any will trigger a warning. The fleet is designed to run as a unit.

Valid server names: `session` · `executor` · `memory`

---

## Server Inventory

All 3 servers live under `mcp_servers/`. Each exposes tools that GitHub Copilot can call during a chat session.

### Session — `mcp_servers/session/` *(CORE)*

Workflow state persistence, session recovery, and layer plan management.

| Tool             | Purpose                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `load_session` | Restore workflow state from `workflow-state.json`                     |
| `save_session` | Persist current workflow state to disk                                  |
| `checkpoint`   | Create a timestamped checkpoint snapshot                                |
| `save_plan`    | Write a layer plan file to `.github/plans/` (enforces layer ordering) |
| `load_plan`    | Read an existing layer plan file                                        |

### Executor — `mcp_servers/executor/` *(CORE)*

Code quality gates, symbol analysis, and server health verification.

| Tool                         | Purpose                                                        |
| ---------------------------- | -------------------------------------------------------------- |
| `run_quality_gates`        | Run test / lint / security gates against a target path         |
| `find_symbol_usages`       | AST-walk `.py` files and return all usages of a named symbol |
| `get_server_health`        | Health-check all 4 TEMPO servers and return a status report    |
| `verify_tool_registration` | Validate tool registrations align with handler methods         |
| `verify_sync_wrappers`     | Check all async handlers have corresponding sync wrappers      |

### Memory — `mcp_servers/memory/` *(CORE)*

Persistent project memory. Reads and writes `.github/memory.md`.

| Tool              | Purpose                                                                 |
| ----------------- | ----------------------------------------------------------------------- |
| `read_memory`   | Read entries with optional date/project/phase filters and ranked recall |
| `write_memory`  | Append a structured entry in TEMPO format                               |
| `search_memory` | Keyword search across all memory entries                                |

---

## Shared Libraries

All servers import from `mcp_servers/base/` and `mcp_servers/utils/`.

| Module                   | Key exports         | Purpose                                                                |
| ------------------------ | ------------------- | ---------------------------------------------------------------------- |
| `base/agent_server.py` | `BaseAgentServer` | Base class: MCP server lifecycle, tool registration, sync wrappers     |
| `utils/results.py`     | `Result[T]`       | Generic result container (`ok`, `fail`, `partial`, `escalate`) |

---

## Running the Test Suite

```bash
# Full suite (24 tests)
pytest

# Verbose
pytest mcp_servers/tests/ -v
```

---

## Project Structure

```
your_repo/
├── QUICKSTART.md                # Start here — install and verify in ~5 minutes
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata and pytest config
│
├── mcp_servers/
│   ├── .install/                # Installation stack
   │   │   ├── _tempo_core.py       # ServerSpec registry, WorkspaceInfo, merge_json
   │   │   ├── setup_tempo.py       # Installer: writes .vscode/ configs, copies .github/
   │   │   ├── manage_servers.py    # Server manager: list / status / enable / disable
   │   │   ├── verify_agents.py     # Smoke-test: imports all 4 servers, exits 0 on success
│   │   └── requirements.txt     # Pinned dependencies
│   ├── base/                    # Shared: BaseAgentServer
│   ├── utils/                   # Result<T> and shared helpers
│   ├── session/                 # Server: workflow state + layer plans  (CORE)
│   ├── executor/                # Server: quality gates + symbol analysis  (CORE)
│   ├── memory/                  # Server: memory read/write  (CORE)
   ├── workflow/                # Server: Shape→Fill workflow engine  (CORE)
   └── tests/                   # 24-test suite for all 4 servers
│
└── .github/
    ├── copilot-instructions.md  # TEMPO methodology (auto-loads in Copilot chat)
    ├── memory.md                # Persistent project memory
    ├── workflow-state.json      # Current CCE layer / phase state
    ├── agents/                  # Custom VS Code agents (Quick Developer, Deep Researcher, Strategic Collaborator)
    ├── prompts/                 # Prompt library: 7 seed prompts indexed by intent tag
    ├── plans/                   # Layer plan files (written by tempo.session)
    ├── playbooks/               # Layer-specific tactical guides
    ├── exploits/                # Advanced technique methodologies
    ├── decision-trees/          # Conflict and ambiguity resolution logic
    ├── reference/               # CCE rationale and philosophy
    └── archives/                # Auto-archived memory files (>500 lines triggers archival)
```

---

## Memory System

The `tempo.memory` server maintains `.github/memory.md` as persistent project memory across sessions. Each entry follows this structure:

```markdown
## [YYYY-MM-DD] {Project} - {Phase/Layer}
**What Was Built:** ...
**Technical Choices:** ...
**Failures:** ...
**Debt Avoided:** ...
**Performance:** ...
**Learnings:** ...
```

When resuming work after a break, tell Copilot:

```
Read .github/memory.md for context
```

---

## Manual Setup (Fallback)

If `setup_tempo.py` cannot be used, register the servers manually.

Open `.vscode/mcp.json` (create it if absent):

```json
{
  "servers": {
    "tempo.session": {
      "command": ".venv/Scripts/python.exe",
      "args": ["-m", "mcp_servers.session.server"],
      "cwd": "<absolute-path-to-dynamics>",
      "env": { "PYTHONPATH": "<absolute-path-to-dynamics>" }
    },
    "tempo.executor": {
      "command": ".venv/Scripts/python.exe",
      "args": ["-m", "mcp_servers.executor.server"],
      "cwd": "<absolute-path-to-dynamics>",
      "env": { "PYTHONPATH": "<absolute-path-to-dynamics>" }
    },
    "tempo.memory": {
      "command": ".venv/Scripts/python.exe",
      "args": ["-m", "mcp_servers.memory.server"],
      "cwd": "<absolute-path-to-dynamics>",
      "env": { "PYTHONPATH": "<absolute-path-to-dynamics>" }
    },
    "tempo.workflow": {
      "command": ".venv/Scripts/python.exe",
      "args": ["-m", "mcp_servers.workflow.server"],
      "cwd": "<absolute-path-to-dynamics>",
      "env": { "PYTHONPATH": "<absolute-path-to-dynamics>" }
    }
  }
}
```

Use `.venv/bin/python` on macOS/Linux. Then enable MCP sampling in `.vscode/settings.json`:

```json
{
  "chat.mcp.serverSampling": {
    "dynamics/.vscode/mcp.json: tempo.session": { "allowedModels": ["*"] },
    "dynamics/.vscode/mcp.json: tempo.executor": { "allowedModels": ["*"] },
    "dynamics/.vscode/mcp.json: tempo.memory": { "allowedModels": ["*"] },
    "dynamics/.vscode/mcp.json: tempo.workflow": { "allowedModels": ["*"] }
  }
}
```

Replace `dynamics` with your actual workspace folder name.

---

## Troubleshooting

**Servers not appearing in Copilot chat**

- Run `python mcp_servers/.install/verify_agents.py` — confirm `4/4 servers loaded successfully`.
- Reload VS Code (`Developer: Reload Window`).
- Check VS Code Output panel → `MCP` for connection errors.
- Re-run `python mcp_servers/.install/setup_tempo.py` to regenerate `.vscode/mcp.json` with the correct venv paths.

**Health check failures after running `setup_tempo.py`**

- `Venv Packages FAIL` — run `pip install -r requirements.txt` inside the active venv.
- `Server Syntax FAIL` — a `mcp_servers/*/server.py` file has a syntax error; fix and re-run.
- `MCP Paths FAIL` — the venv was moved or recreated; re-run `python setup_tempo.py`.
- `Sampling Key FAIL` — run `python setup_tempo.py` again from a shell where `cwd` is the workspace root.

**`ModuleNotFoundError: mcp_servers`**

- `PYTHONPATH` must point to the workspace root. `setup_atlas.py` sets this automatically in each server entry.
- If running manually: `set PYTHONPATH=<path-to-dynamics>` (Windows) or `export PYTHONPATH=<path-to-dynamics>` (macOS/Linux).

**Tests fail on import**

- Run `pip install -r requirements.txt` inside the active virtual environment.
- Confirm `python --version` reports 3.11 or above.
