# ATLAS Quick Start

## Prerequisites
- Python 3.11+
- VS Code with GitHub Copilot extension

## 1. Get the code
Unzip the archive and open the folder in VS Code:

    File → Open Folder → select the unzipped directory

## 2. Create a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## 4. Run the installer
```bash
python mcp_servers/.install/setup_atlas.py
```

## 5. Reload VS Code
Command Palette → "Developer: Reload Window"

This picks up the new `.vscode/mcp.json` entries.

## 6. Verify
```bash
python mcp_servers/.install/verify_agents.py
```

Expected: `3/3 servers loaded successfully`

## First ATLAS workflow
In Copilot Chat, select an agent from the agents dropdown:

- **Quick Developer** — bounded tasks ≤1 hour. Assess → Implement → Gate.
- **Deep Researcher** — multi-pass gap-analysis research with confidence-scored synthesis.
- **Strategic Collaborator** — systems design, ADRs, diagrams, and handoff plans.
- **Standard ATLAS** (no agent selected) — full 5-layer CCE workflow for complex initiatives.

---

## Starter Prompts

| Goal | Agent | Prompt |
|---|---|---|
| Begin new project | Standard ATLAS | `Start a new ATLAS Layer 1 plan for: [your goal]` |
| Resume work | Standard ATLAS | `Read .github/memory.md for context, then load my session` |
| Quick code task | Quick Developer | Describe the task — agent handles assess/implement/gate |
| Research a topic | Deep Researcher | Describe the question — agent runs gap-analysis loop |
| Design a system | Strategic Collaborator | Describe the system — agent opens design session |
| Run quality gates | Standard ATLAS | `Run quality gates on mcp_servers/` |
| Check server health | Standard ATLAS | `Check ATLAS server health` |
| Save progress | Any | `checkpoint` |

---

## Troubleshooting

**Servers not connecting after install:**
- Command Palette → "MCP: List Servers" — confirm `session`, `executor`, `memory` appear
- If missing: Command Palette → "Developer: Reload Window"
- If still missing: check Output panel → select "MCP" from dropdown for error details

**Tool calls silently ignored:**
- Copilot must be in **Agent mode** (not Chat mode) to call MCP tools
- Switch: click the mode selector in the Copilot Chat panel

**`verify_agents.py` shows FAIL:**
```bash
.venv\Scripts\python.exe -c "from mcp_servers.session.server import SessionServer"
```
If ImportError: `pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org`

**`setup_atlas.py` errors on first run:**
- Ensure you activated the venv before running: `.venv\Scripts\activate`
- Ensure you are running from the workspace root directory
