"""Tests for tempo.memory MemoryServer — 7 tests.

Coverage
--------
1  write_prepend_order     Two writes produce newest-first ordering
2  auto_archive_trigger    File over 500 lines → write_memory archives before writing
3  filter_passthrough      Project filter returns only matching entries
4  search_term_match       Keyword in entry body is found by search_memory
5  zero_result_query       search_memory on unknown term returns empty list
6  missing_file_graceful   read_memory with no memory.md returns ok with empty list
7  lock_contention         Concurrent writes produce correct entry count (no corruption)
"""

import threading

import pytest

import mcp_servers.memory.server as memory_module
from mcp_servers.memory.server import MemoryServer


# ---------------------------------------------------------------------------
# Shared fixture — redirect all paths to a tmp directory
# ---------------------------------------------------------------------------

@pytest.fixture()
def server(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_module, "MEMORY_PATH",              tmp_path / ".github" / "memory.md")
    monkeypatch.setattr(memory_module, "ARCHIVE_DIR",              tmp_path / ".github" / "archives")
    monkeypatch.setattr(memory_module, "MAX_LINES_BEFORE_ARCHIVE", 500)
    return MemoryServer()


def _write(server: MemoryServer, project: str, phase: str = "p1") -> None:
    """Convenience: write a minimal memory entry."""
    server.write_memory(
        project=project,
        phase=phase,
        what_was_built="built something",
        technical_choices="choice A",
        learnings="learned X",
    )


# ---------------------------------------------------------------------------
# 1. Write + prepend order
# ---------------------------------------------------------------------------

class TestWritePrependOrder:
    def test_newest_entry_at_top(self, server, tmp_path):
        """Two successive writes produce newest-first ordering in memory.md."""
        _write(server, "alpha")
        _write(server, "beta")

        result = server.read_memory()
        assert result.status.value == "success", result.errors
        entries = result.data
        assert len(entries) == 2
        assert entries[0]["project"] == "beta"    # newest first
        assert entries[1]["project"] == "alpha"


# ---------------------------------------------------------------------------
# 2. Auto-archive trigger
# ---------------------------------------------------------------------------

class TestAutoArchiveTrigger:
    def test_archive_fires_when_file_exceeds_threshold(self, server, tmp_path, monkeypatch):
        """write_memory triggers archive when memory.md line count exceeds threshold."""
        monkeypatch.setattr(memory_module, "MAX_LINES_BEFORE_ARCHIVE", 5)

        mem_path = tmp_path / ".github" / "memory.md"
        mem_path.parent.mkdir(parents=True, exist_ok=True)
        # Write 10 lines so we're already over the 5-line threshold
        mem_path.write_text("\n".join(f"line {i}" for i in range(10)), encoding="utf-8")

        # Trigger via the write_memory result
        _write(server, "proj")
        r = server.write_memory(
            project="proj", phase="test_archive",
            what_was_built="x", technical_choices="y", learnings="z",
        )
        assert r.status.value == "success"
        assert r.data["archived"] is True

        archive_dir = tmp_path / ".github" / "archives"
        archive_files = list(archive_dir.glob("memory_archive_*.md"))
        assert archive_files, "Expected an archive file to be created"


# ---------------------------------------------------------------------------
# 3. Project filter pass-through
# ---------------------------------------------------------------------------

class TestFilterPassthrough:
    def test_project_filter_returns_matching_only(self, server):
        """project_filter returns only entries whose project name matches."""
        _write(server, "alpha_project")
        _write(server, "beta_project")

        result = server.read_memory(project_filter="alpha")
        assert result.status.value == "success", result.errors
        assert len(result.data) == 1
        assert result.data[0]["project"] == "alpha_project"


# ---------------------------------------------------------------------------
# 4. Search term match
# ---------------------------------------------------------------------------

class TestSearchTermMatch:
    def test_search_finds_entry_with_keyword_in_body(self, server):
        """search_memory finds an entry containing the query term."""
        server.write_memory(
            project="proj",
            phase="p1",
            what_was_built="implemented the fluxcapacitor module",
            technical_choices="chose asyncio",
            learnings="async is great",
        )
        result = server.search_memory("fluxcapacitor")
        assert result.status.value == "success", result.errors
        assert result.data, "Expected at least one matching entry"
        assert any("fluxcapacitor" in e.get("what_was_built", "") for e in result.data)


# ---------------------------------------------------------------------------
# 5. Zero-result query
# ---------------------------------------------------------------------------

class TestZeroResultQuery:
    def test_search_unknown_term_returns_empty_list(self, server):
        """search_memory on a term not in any entry returns empty list without error."""
        _write(server, "proj")

        result = server.search_memory("xyzzy_totally_absent_42")
        assert result.status.value == "success", result.errors
        assert result.data == []


# ---------------------------------------------------------------------------
# 6. Missing file graceful return
# ---------------------------------------------------------------------------

class TestMissingFileGraceful:
    def test_read_memory_on_absent_file_returns_ok_empty(self, server):
        """read_memory with no memory.md returns ok with an empty list."""
        result = server.read_memory()
        assert result.status.value == "success", result.errors
        assert result.data == []

    def test_search_memory_on_absent_file_returns_ok_empty(self, server):
        """search_memory with no memory.md returns ok with an empty list."""
        result = server.search_memory("anything")
        assert result.status.value == "success", result.errors
        assert result.data == []


# ---------------------------------------------------------------------------
# 7. Lock contention — concurrent writes produce no corruption
# ---------------------------------------------------------------------------

class TestLockContention:
    def test_concurrent_writes_all_persist(self, server):
        """10 concurrent write_memory calls all produce persisted entries without corruption."""
        n = 10
        errors: list[str] = []

        def do_write(i: int) -> None:
            r = server.write_memory(
                project=f"proj_{i}",
                phase=f"phase_{i}",
                what_was_built=f"built item {i}",
                technical_choices="concurrent",
                learnings="thread safety",
            )
            if r.status.value != "success":
                errors.append(f"write {i} failed: {r.errors}")

        threads = [threading.Thread(target=do_write, args=(i,)) for i in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Write failures: {errors}"

        result = server.read_memory()
        assert result.status.value == "success"
        assert len(result.data) == n, f"Expected {n} entries, got {len(result.data)}"
