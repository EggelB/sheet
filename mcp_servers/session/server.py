"""tempo.session — Session management and plan gate enforcement for TEMPO.

Tools
-----
load_session   Parallel I/O: state file + memory header + git modified files.
save_session   Write/update .github/workflow-state.json.
save_plan      Gate-enforced atomic write of a layer plan file.
load_plan      Read an existing layer plan file.
checkpoint     Save session state + remind about tempo.memory write_memory.

Gate contract
-------------
save_plan(layer=N) fails hard if the layer N-1 file does not exist in PLANS_DIR.
Gate = file existence. Content quality is the planning loop's responsibility.
"""

import asyncio
import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool
from mcp_servers.base import BaseAgentServer
from mcp_servers.utils.results import Result

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PLAN_LAYERS: dict[int, tuple[str, str | None]] = {
    1: ("layer1_strategic",   None),
    2: ("layer2_operational", "layer1_strategic"),
    3: ("layer3_blueprints",  "layer2_operational"),
    4: ("layer4_dry_audit",   "layer3_blueprints"),
    5: ("layer5_pure_signal", "layer4_dry_audit"),
}

STATE_FILE  = Path(".github/workflow-state.json")
PLANS_DIR   = Path(".github/plans")
MEMORY_FILE = Path(".github/memory.md")
GIT_TIMEOUT = 5  # seconds


# ---------------------------------------------------------------------------
# SessionState
# ---------------------------------------------------------------------------

@dataclass
class SessionState:
    project_name: str
    current_layer: int | str
    current_phase: int | None
    last_updated: str
    last_checkpoint_reason: str
    summary: str

    @classmethod
    def from_dict(cls, data: dict) -> "SessionState":
        known = set(cls.__dataclass_fields__)
        return cls(**{k: v for k, v in data.items() if k in known})

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

class SessionServer(BaseAgentServer):
    """tempo.session — plan state and structural file-gate enforcement."""

    @property
    def agent_name(self) -> str:
        return "tempo.session"

    def _get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="load_session",
                description=(
                    "Load current session state in parallel: workflow-state.json, "
                    "last memory.md header line, and git-modified file list. "
                    "Returns is_fresh=True when no prior state file exists."
                ),
                inputSchema={"type": "object", "properties": {}, "required": []},
            ),
            Tool(
                name="save_session",
                description="Write or update .github/workflow-state.json with the supplied state fields.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name":           {"type": "string"},
                        "current_layer":          {"type": ["integer", "string"]},
                        "current_phase":          {"type": ["integer", "null"]},
                        "last_checkpoint_reason": {"type": "string"},
                        "summary":                {"type": "string"},
                    },
                    "required": ["project_name"],
                },
            ),
            Tool(
                name="save_plan",
                description=(
                    "Write a layer plan file to .github/plans/. "
                    "Enforces structural gate: layer N requires layer N-1 file to exist. "
                    "Uses atomic .tmp + os.replace() write. "
                    "SAFE BY DEFAULT: if the file already exists, new content is appended after "
                    "existing content. Pass overwrite=true ONLY to replace the entire file. "
                    "Always pass only the NEW phase content — never re-paste prior phases."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "layer":        {"type": "integer", "minimum": 1, "maximum": 5},
                        "content":      {"type": "string"},
                        "overwrite":    {"type": "boolean", "description": "Set true ONLY to replace the entire file. Default false (safe): new content appends after existing content."},
                    },
                    "required": ["project_name", "layer", "content"],
                },
            ),
            Tool(
                name="load_plan",
                description="Read an existing layer plan file from .github/plans/. Returns full file content.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {"type": "string"},
                        "layer":        {"type": "integer", "minimum": 1, "maximum": 5},
                    },
                    "required": ["project_name", "layer"],
                },
            ),
            Tool(
                name="checkpoint",
                description=(
                    "Save current session state and return a checkpoint record. "
                    "Always appends a reminder to call tempo.memory write_memory "
                    "if substantive progress warrants it."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name":  {"type": "string"},
                        "reason":        {"type": "string"},
                        "current_layer": {"type": ["integer", "string"]},
                        "current_phase": {"type": ["integer", "null"]},
                        "summary":       {"type": "string"},
                    },
                    "required": ["project_name", "reason"],
                },
            ),
        ]

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    async def _tool_load_session(self) -> Result:
        """Parallel I/O: state file, memory header, git modified files."""
        state_dict, memory_header, git_files = await asyncio.gather(
            self._read_state_file(),
            self._read_last_memory_header(),
            self._read_git_modified_files(),
        )
        return Result.ok({
            "state":               state_dict,
            "last_memory_entry":   memory_header,
            "modified_files":      git_files,
            "modified_file_count": len(git_files),
            "is_fresh":            state_dict is None,
        })

    async def _tool_save_session(
        self,
        project_name: str,
        current_layer: int | str = 1,
        current_phase: int | None = None,
        last_checkpoint_reason: str = "",
        summary: str = "",
    ) -> Result:
        """Serialise SessionState to workflow-state.json."""
        state = SessionState(
            project_name=project_name,
            current_layer=current_layer,
            current_phase=current_phase,
            last_updated=datetime.now(timezone.utc).isoformat(),
            last_checkpoint_reason=last_checkpoint_reason,
            summary=summary,
        )
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state.to_dict(), indent=2), encoding="utf-8")
        return Result.ok({"file_path": str(STATE_FILE), "state": state.to_dict()})

    async def _tool_save_plan(
        self,
        project_name: str,
        layer: int,
        content: str,
        overwrite: bool = False,
    ) -> Result:
        """Gate check then atomic write.

        Safe-by-default: if the target file already exists and overwrite is False
        (the default), new content is appended after existing content.  Pass
        overwrite=True only when intentionally replacing the entire file.
        """
        if layer not in PLAN_LAYERS:
            return Result.fail([f"Layer must be 1–5, got {layer!r}"])
        suffix, required_prior = PLAN_LAYERS[layer]
        if required_prior:
            prior = PLANS_DIR / f"{project_name}_{required_prior}.md"
            if not prior.exists():
                return Result.fail([
                    f"Gate check failed: '{prior}' not found. "
                    f"Run save_plan(project_name='{project_name}', layer={layer - 1}, content=...) first."
                ])
        PLANS_DIR.mkdir(parents=True, exist_ok=True)
        target = PLANS_DIR / f"{project_name}_{suffix}.md"
        if not overwrite and target.exists():
            existing = target.read_text(encoding="utf-8")
            content = existing.rstrip("\n") + "\n\n---\n\n" + content
        tmp = target.with_suffix(".tmp")
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, target)
        return Result.ok({
            "file_path":   str(target),
            "layer":       layer,
            "bytes":       len(content.encode()),
            "overwritten": overwrite,
        })

    async def _tool_load_plan(self, project_name: str, layer: int) -> Result:
        """Read an existing plan file."""
        if layer not in PLAN_LAYERS:
            return Result.fail([f"Layer must be 1–5, got {layer!r}"])
        suffix, _ = PLAN_LAYERS[layer]
        target = PLANS_DIR / f"{project_name}_{suffix}.md"
        if not target.exists():
            return Result.fail([
                f"Plan not found: '{target}'. "
                f"Run save_plan(project_name='{project_name}', layer={layer}, content=...) to create it."
            ])
        return Result.ok({
            "file_path": str(target),
            "content":   target.read_text(encoding="utf-8"),
        })

    async def _tool_checkpoint(
        self,
        project_name: str,
        reason: str,
        current_layer: int | str = 1,
        current_phase: int | None = None,
        summary: str = "",
    ) -> Result:
        """Save state and always remind about tempo.memory write_memory."""
        save_result = await self._tool_save_session(
            project_name=project_name,
            current_layer=current_layer,
            current_phase=current_phase,
            last_checkpoint_reason=reason,
            summary=summary,
        )
        if save_result.errors:
            return save_result
        return Result.ok({
            "checkpoint_reason": reason,
            "state":             save_result.data["state"],
            "memory_reminder": (
                f"If substantive progress was made, call tempo.memory write_memory "
                f"with project='{project_name}' and phase='{reason}' to preserve context."
            ),
        })

    # ------------------------------------------------------------------
    # Private I/O helpers
    # ------------------------------------------------------------------

    async def _read_state_file(self) -> dict | None:
        """Return parsed and validated state dict, or None if absent/corrupt."""
        try:
            if not STATE_FILE.exists():
                return None
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return SessionState.from_dict(data).to_dict()
        except Exception:
            return None

    async def _read_last_memory_header(self) -> str | None:
        """Return the first ## heading from memory.md, or None."""
        try:
            if not MEMORY_FILE.exists():
                return None
            for line in MEMORY_FILE.read_text(encoding="utf-8").splitlines():
                if line.startswith("## "):
                    return line.lstrip("# ").strip()
            return None
        except Exception:
            return None

    async def _read_git_modified_files(self) -> list[str]:
        """Return git-modified file paths, or [] on timeout / git unavailable."""
        try:
            proc = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    "git", "diff", "--name-only", "HEAD",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                ),
                timeout=GIT_TIMEOUT,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=GIT_TIMEOUT)
            return [line for line in stdout.decode().splitlines() if line]
        except (asyncio.TimeoutError, FileNotFoundError, OSError):
            return []

    # ------------------------------------------------------------------
    # Sync public API (used by tests and direct callers)
    # ------------------------------------------------------------------

    def load_session(self) -> Result:
        return self._run(self._tool_load_session())

    def save_session(self, **kwargs) -> Result:
        return self._run(self._tool_save_session(**kwargs))

    def save_plan(self, project_name: str, layer: int, content: str, overwrite: bool = False) -> Result:
        return self._run(self._tool_save_plan(project_name, layer, content, overwrite))

    def load_plan(self, project_name: str, layer: int) -> Result:
        return self._run(self._tool_load_plan(project_name, layer))

    def checkpoint(self, **kwargs) -> Result:
        return self._run(self._tool_checkpoint(**kwargs))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    SessionServer.cli_main()
