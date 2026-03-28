"""tempo.memory — Memory read/write/search for the TEMPO CCE workflow.

Manages .github/memory.md: prepend-on-write, keyword search, project/phase
filtering, and auto-archive when the file exceeds MAX_LINES_BEFORE_ARCHIVE.
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool
from mcp_servers.base import BaseAgentServer
from mcp_servers.utils.results import Result


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MEMORY_PATH             = Path(".github/memory.md")
ARCHIVE_DIR             = Path(".github/archives")
MAX_LINES_BEFORE_ARCHIVE = 500
HEADER                  = "# TEMPO Memory Log\n\n---\n\n"


# ---------------------------------------------------------------------------
# MemoryEntry
# ---------------------------------------------------------------------------

class MemoryEntry:
    """Parsed memory entry from ATLAS memory.md format."""

    def __init__(
        self,
        date: str,
        project: str,
        phase: str,
        what_was_built: str = "",
        technical_choices: str = "",
        failures: str = "",
        debt_avoided: str = "",
        performance: str = "",
        learnings: str = "",
    ):
        self.date             = date
        self.project          = project
        self.phase            = phase
        self.what_was_built   = what_was_built
        self.technical_choices = technical_choices
        self.failures         = failures
        self.debt_avoided     = debt_avoided
        self.performance      = performance
        self.learnings        = learnings

    def to_dict(self) -> dict[str, Any]:
        return {
            "date":             self.date,
            "project":          self.project,
            "phase":            self.phase,
            "what_was_built":   self.what_was_built,
            "technical_choices": self.technical_choices,
            "failures":         self.failures,
            "debt_avoided":     self.debt_avoided,
            "performance":      self.performance,
            "learnings":        self.learnings,
        }

    def to_markdown(self) -> str:
        return (
            f"## [{self.date}] {self.project} - {self.phase}\n\n"
            f"**What Was Built:** {self.what_was_built}\n\n"
            f"**Technical Choices:** {self.technical_choices}\n\n"
            f"**Failures:** {self.failures}\n\n"
            f"**Debt Avoided:** {self.debt_avoided}\n\n"
            f"**Performance:** {self.performance}\n\n"
            f"**Learnings:** {self.learnings}\n\n---\n\n"
        )


# ---------------------------------------------------------------------------
# Inline scorer  (replaces score_results import chain)
# ---------------------------------------------------------------------------

def _score_entry(entry: MemoryEntry, query: str) -> float:
    """Keyword-frequency relevance: fraction of query words found in entry text."""
    words = {w.lower() for w in query.split() if w}
    if not words:
        return 0.0
    text = " ".join([
        entry.project, entry.phase, entry.what_was_built,
        entry.technical_choices, entry.failures, entry.learnings,
    ]).lower()
    return sum(1 for w in words if w in text) / len(words)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

class MemoryServer(BaseAgentServer):
    """tempo.memory — thread-safe TEMPO memory read/write."""

    def __init__(self):
        super().__init__()
        self._write_lock = Lock()

    @property
    def agent_name(self) -> str:
        return "tempo.memory"

    def _get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="read_memory",
                description=(
                    "Read entries from .github/memory.md with optional filtering. "
                    "Supply query for relevance-ranked results, top_n to truncate."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_filter": {"type": "string"},
                        "phase_filter":   {"type": "string"},
                        "date_after":     {"type": "string", "description": "YYYY-MM-DD"},
                        "query":          {"type": "string"},
                        "top_n":          {"type": "integer"},
                    },
                },
            ),
            Tool(
                name="write_memory",
                description=(
                    "Write a new ATLAS memory entry. Thread-safe. "
                    "Auto-archives to .github/archives/ if memory.md exceeds 500 lines."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project":          {"type": "string"},
                        "phase":            {"type": "string"},
                        "what_was_built":   {"type": "string"},
                        "technical_choices":{"type": "string"},
                        "failures":         {"type": "string"},
                        "debt_avoided":     {"type": "string"},
                        "performance":      {"type": "string"},
                        "learnings":        {"type": "string"},
                    },
                    "required": ["project", "phase", "what_was_built", "technical_choices", "learnings"],
                },
            ),
            Tool(
                name="search_memory",
                description="Keyword search across all memory entries (OR logic on keywords list).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Keywords to match (OR logic)",
                        },
                    },
                    "required": ["keywords"],
                },
            ),
        ]

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    async def _tool_read_memory(
        self,
        project_filter: str | None = None,
        phase_filter:   str | None = None,
        date_after:     str | None = None,
        query:          str | None = None,
        top_n:          int | None = None,
    ) -> Result:
        """Read and optionally rank memory entries."""
        if not MEMORY_PATH.exists():
            return Result.ok([], total_entries=0, filtered_count=0)

        content  = MEMORY_PATH.read_text(encoding="utf-8")
        entries  = self._parse_memory_entries(content)
        filtered = self._apply_filters(entries, project_filter, phase_filter, date_after)
        dicts    = [e.to_dict() for e in filtered]

        if query is not None:
            scored = sorted(filtered, key=lambda e: _score_entry(e, query), reverse=True)
            if top_n:
                scored = scored[:top_n]
            dicts = [
                {**e.to_dict(), "relevance_score": round(_score_entry(e, query), 4)}
                for e in scored
            ]

        return Result.ok(dicts, total_entries=len(entries), filtered_count=len(filtered))

    async def _tool_write_memory(
        self,
        project: str,
        phase: str,
        what_was_built: str,
        technical_choices: str,
        learnings: str,
        failures: str = "",
        debt_avoided: str = "",
        performance: str = "",
    ) -> Result:
        """Thread-safe prepend new entry; auto-archive if over threshold."""
        entry = MemoryEntry(
            date=datetime.now().strftime("%Y-%m-%d"),
            project=project,
            phase=phase,
            what_was_built=what_was_built,
            technical_choices=technical_choices,
            failures=failures,
            debt_avoided=debt_avoided,
            performance=performance,
            learnings=learnings,
        )
        with self._write_lock:
            archived = self._archive_if_needed()
            self._prepend_entry(entry)
        return Result.ok({"file_path": str(MEMORY_PATH), "archived": archived})

    async def _tool_search_memory(self, keywords: list[str]) -> Result:
        """Keyword search (OR logic)."""
        if not MEMORY_PATH.exists():
            return Result.ok([], total_entries=0, match_count=0)

        entries = self._parse_memory_entries(MEMORY_PATH.read_text(encoding="utf-8"))
        matched = [
            e for e in entries
            if any(kw.lower() in e.to_markdown().lower() for kw in keywords)
        ]
        return Result.ok(
            [e.to_dict() for e in matched],
            total_entries=len(entries),
            match_count=len(matched),
            keywords=keywords,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _archive_if_needed(self) -> bool:
        """Archive and reset memory.md if over the line threshold. Must be called under lock."""
        if not MEMORY_PATH.exists():
            return False
        lines = MEMORY_PATH.read_text(encoding="utf-8").splitlines()
        if len(lines) <= MAX_LINES_BEFORE_ARCHIVE:
            return False
        self._archive_memory("\n".join(lines))
        MEMORY_PATH.write_text(HEADER, encoding="utf-8")
        return True

    def _prepend_entry(self, entry: MemoryEntry) -> None:
        """Prepend entry after the file header (newest entries first)."""
        MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        existing = MEMORY_PATH.read_text(encoding="utf-8") if MEMORY_PATH.exists() else ""
        if not existing.strip():
            MEMORY_PATH.write_text(HEADER + entry.to_markdown(), encoding="utf-8")
        else:
            body = existing.removeprefix(HEADER) if existing.startswith(HEADER) else existing
            MEMORY_PATH.write_text(HEADER + entry.to_markdown() + body, encoding="utf-8")

    def _archive_memory(self, content: str) -> None:
        """Write content to a timestamped archive file."""
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        stamp        = datetime.now().strftime("%Y%m%d")
        archive_file = ARCHIVE_DIR / f"memory_archive_{stamp}.md"
        archive_file.write_text(content, encoding="utf-8")

    def _parse_memory_entries(self, content: str) -> list[MemoryEntry]:
        """Parse memory.md content into MemoryEntry objects."""
        entries = []
        pattern = r'## \[(\d{4}-\d{2}-\d{2})\] (.+?) - (.+?)(?=\n\n|\n##|\Z)'
        for match in re.finditer(pattern, content, re.DOTALL):
            date    = match.group(1)
            project = match.group(2).strip()
            phase   = match.group(3).strip()

            entry_content = content[match.end():]
            next_entry    = re.search(r'## \[\d{4}-\d{2}-\d{2}\]', entry_content)
            if next_entry:
                entry_content = entry_content[:next_entry.start()]

            entries.append(MemoryEntry(
                date=date,
                project=project,
                phase=phase,
                what_was_built    = self._extract_section(entry_content, "What Was Built"),
                technical_choices  = self._extract_section(entry_content, "Technical Choices"),
                failures          = self._extract_section(entry_content, "Failures"),
                debt_avoided      = self._extract_section(entry_content, "Debt Avoided"),
                performance       = self._extract_section(entry_content, "Performance"),
                learnings         = self._extract_section(entry_content, "Learnings"),
            ))
        return entries

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract bold-section content."""
        pattern = rf'\*\*{section_name}:\*\* (.+?)(?=\n\n\*\*|\n\n---|\Z)'
        match   = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _apply_filters(
        self,
        entries: list[MemoryEntry],
        project_filter: str | None,
        phase_filter:   str | None,
        date_after:     str | None,
    ) -> list[MemoryEntry]:
        """Apply optional filters."""
        result = entries
        if project_filter:
            result = [e for e in result if project_filter.lower() in e.project.lower()]
        if phase_filter:
            result = [e for e in result if phase_filter.lower() in e.phase.lower()]
        if date_after:
            result = [e for e in result if e.date >= date_after]
        return result

    # ------------------------------------------------------------------
    # Sync public API  (Task 3.6: param names now match async handler)
    # ------------------------------------------------------------------

    def read_memory(
        self,
        project_filter: str | None = None,
        phase_filter:   str | None = None,
        date_after:     str | None = None,
        query:          str | None = None,
        top_n:          int | None = None,
    ) -> Result:
        return self._run(self._tool_read_memory(
            project_filter=project_filter,
            phase_filter=phase_filter,
            date_after=date_after,
            query=query,
            top_n=top_n,
        ))

    def write_memory(self, **kwargs) -> Result:
        return self._run(self._tool_write_memory(**kwargs))

    def search_memory(self, query: str) -> Result:
        """Converts single query string to keywords list for handler call."""
        return self._run(self._tool_search_memory(keywords=[query]))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    MemoryServer.cli_main()
