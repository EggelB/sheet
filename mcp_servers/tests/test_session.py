"""Tests for tempo.session SessionServer — 10 tests.

Coverage
--------
1  gate_pass              Layer 2 save succeeds when layer 1 file exists
2  gate_fail              Layer 2 save fails with actionable message when layer 1 is absent
3  fresh_session_flag     load_session returns is_fresh=True when no state file exists
4  atomic_write_no_tmp    No .tmp residue after successful save_plan
5  git_fallback           Missing git binary returns modified_files=[] — load_session still succeeds
6  checkpoint_reminder    checkpoint() result always contains memory_reminder key
7  unknown_layer          save_plan with layer=99 returns failure with layer number in message
8  safe_default           save_plan on existing file appends by default (no overwrite= required)
9  overwrite_explicit     save_plan(overwrite=True) replaces entire file content
10 create_new             save_plan on nonexistent file creates it normally
"""

from unittest.mock import patch

import pytest

import mcp_servers.session.server as session_module
from mcp_servers.session.server import SessionServer


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def server(tmp_path, monkeypatch):
    """SessionServer with all file paths redirected to a temporary directory."""
    monkeypatch.setattr(session_module, "STATE_FILE",  tmp_path / ".github" / "workflow-state.json")
    monkeypatch.setattr(session_module, "PLANS_DIR",   tmp_path / ".github" / "plans")
    monkeypatch.setattr(session_module, "MEMORY_FILE", tmp_path / ".github" / "memory.md")
    return SessionServer()


# ---------------------------------------------------------------------------
# 1. Gate pass
# ---------------------------------------------------------------------------

class TestGatePass:
    def test_layer2_succeeds_when_layer1_exists(self, server):
        """Layer 2 save succeeds when the layer 1 file is already present."""
        r1 = server.save_plan("proj", 1, "# Layer 1 content")
        assert r1.status.value == "success", r1.errors

        r2 = server.save_plan("proj", 2, "# Layer 2 content")
        assert r2.status.value == "success", r2.errors
        assert "layer2_operational" in r2.data["file_path"]


# ---------------------------------------------------------------------------
# 2. Gate fail
# ---------------------------------------------------------------------------

class TestGateFail:
    def test_layer2_fails_without_layer1(self, server):
        """Layer 2 save returns failure with an actionable error when layer 1 is absent."""
        result = server.save_plan("proj", 2, "# content")
        assert result.status.value == "failure"
        assert result.errors, "Expected at least one error message"
        msg = result.errors[0]
        assert "Gate check failed" in msg
        assert "save_plan" in msg


# ---------------------------------------------------------------------------
# 3. Fresh session flag
# ---------------------------------------------------------------------------

class TestFreshSession:
    def test_is_fresh_true_when_no_state_file(self, server):
        """load_session returns is_fresh=True and state=None when no state file exists."""
        result = server.load_session()
        assert result.status.value == "success"
        assert result.data["is_fresh"] is True
        assert result.data["state"] is None


# ---------------------------------------------------------------------------
# 4. Atomic write — no .tmp residue
# ---------------------------------------------------------------------------

class TestAtomicWrite:
    def test_no_tmp_file_after_successful_save(self, server, tmp_path):
        """After save_plan completes no .tmp file should remain on disk."""
        server.save_plan("proj", 1, "# Layer 1")
        plans_dir = tmp_path / ".github" / "plans"
        stale = list(plans_dir.glob("*.tmp"))
        assert stale == [], f"Stale .tmp files found: {stale}"


# ---------------------------------------------------------------------------
# 5. Git timeout / missing git fallback
# ---------------------------------------------------------------------------

class TestGitFallback:
    def test_missing_git_returns_empty_list(self, server):
        """FileNotFoundError from git subprocess returns modified_files=[] — load_session still succeeds."""
        with patch("asyncio.create_subprocess_exec", side_effect=FileNotFoundError):
            result = server.load_session()
        assert result.status.value == "success"
        assert result.data["modified_files"] == []
        assert result.data["modified_file_count"] == 0


# ---------------------------------------------------------------------------
# 6. Checkpoint reminder
# ---------------------------------------------------------------------------

class TestCheckpointReminder:
    def test_checkpoint_always_has_memory_reminder(self, server):
        """checkpoint() result always contains a memory_reminder pointing to tempo.memory."""
        result = server.checkpoint(
            project_name="proj",
            reason="Phase 1 complete",
            current_layer=1,
        )
        assert result.status.value == "success", result.errors
        assert "memory_reminder" in result.data
        assert "tempo.memory" in result.data["memory_reminder"]
        assert "write_memory" in result.data["memory_reminder"]


# ---------------------------------------------------------------------------
# 7. Unknown layer
# ---------------------------------------------------------------------------

class TestUnknownLayer:
    def test_layer_99_returns_failure(self, server):
        """save_plan with an out-of-range layer returns failure with layer value in message."""
        result = server.save_plan("proj", 99, "content")
        assert result.status.value == "failure"
        assert result.errors
        assert "99" in result.errors[0]

    def test_load_plan_unknown_layer_returns_failure(self, server):
        """load_plan with an out-of-range layer also returns failure."""
        result = server.load_plan("proj", 0)
        assert result.status.value == "failure"
        assert result.errors
        assert "0" in result.errors[0]


# ---------------------------------------------------------------------------
# 8. Safe-default accumulation (no flag needed)
# ---------------------------------------------------------------------------

class TestSafeDefault:
    def test_second_save_appends_without_flag(self, server):
        """Calling save_plan twice without overwrite= preserves prior content by default."""
        server.save_plan("proj", 1, "# Phase 1 content")
        result = server.save_plan("proj", 1, "# Phase 2 content")
        assert result.status.value == "success", result.errors
        assert result.data["overwritten"] is False

        load = server.load_plan("proj", 1)
        full = load.data["content"]
        assert "# Phase 1 content" in full
        assert "# Phase 2 content" in full
        assert full.index("# Phase 1 content") < full.index("# Phase 2 content")

    def test_first_save_creates_file(self, server):
        """save_plan on a non-existent file creates it normally."""
        result = server.save_plan("proj", 1, "# Only phase")
        assert result.status.value == "success", result.errors
        load = server.load_plan("proj", 1)
        assert "# Only phase" in load.data["content"]


# ---------------------------------------------------------------------------
# 9. Explicit overwrite
# ---------------------------------------------------------------------------

class TestExplicitOverwrite:
    def test_overwrite_true_replaces_content(self, server):
        """save_plan(overwrite=True) replaces the entire file, discarding prior content."""
        server.save_plan("proj", 1, "# Phase 1 content")
        result = server.save_plan("proj", 1, "# Replacement only", overwrite=True)
        assert result.status.value == "success", result.errors
        assert result.data["overwritten"] is True

        load = server.load_plan("proj", 1)
        full = load.data["content"]
        assert "# Replacement only" in full
        assert "# Phase 1 content" not in full
