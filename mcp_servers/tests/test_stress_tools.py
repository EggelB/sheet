"""Stress tests: direct end-to-end invocation of all 14 tool handler methods.

These tests exercise the full call path:
    sync wrapper → _run() → ThreadPoolExecutor → asyncio.run() → async handler

This mirrors exactly what VS Code dispatches when Copilot calls a tool via MCP,
without the nested event-loop complication of the live MCP stdio transport.

Run with:
    pytest mcp_servers/tests/test_stress_tools.py -v

Coverage:
    Session  — 7 tests  (load_session, save_session, save_plan × 2, load_plan × 2, checkpoint)
    Executor — 9 tests  (validate_code × 2, get_server_health, verify_tool_registration × 3,
                          verify_sync_wrappers, find_symbol_usages × 3, run_quality_gates)
    Memory   — 6 tests  (read_memory × 3, write_memory, search_memory × 2)
"""

import os
from pathlib import Path

import pytest

# Ensure CWD is workspace root so every relative path resolves correctly.
# (servers set workspace_root = str(Path(".").resolve()) in __init__)
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
os.chdir(WORKSPACE_ROOT)

from mcp_servers.session.server import SessionServer      # noqa: E402
from mcp_servers.executor.server import ExecutorServer    # noqa: E402
from mcp_servers.memory.server import MemoryServer        # noqa: E402

STRESS_PROJECT = "stress_test_run"
SESSION_FILES = ["session/server.py", "executor/server.py", "memory/server.py"]


# ---------------------------------------------------------------------------
# Fixtures — module-scoped so each server is instantiated once
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def session():
    return SessionServer()


@pytest.fixture(scope="module")
def executor():
    return ExecutorServer()


@pytest.fixture(scope="module")
def memory():
    return MemoryServer()


# ---------------------------------------------------------------------------
# Session — load_session
# ---------------------------------------------------------------------------

def test_load_session_returns_expected_keys(session):
    r = session.load_session()
    assert not r.errors, r.errors
    assert isinstance(r.data, dict)
    assert "is_fresh" in r.data
    assert "modified_files" in r.data
    assert "last_memory_entry" in r.data
    assert isinstance(r.data["modified_files"], list)
    assert isinstance(r.data["modified_file_count"], int)


# ---------------------------------------------------------------------------
# Session — save_session
# ---------------------------------------------------------------------------

def test_save_session_writes_state_file(session):
    r = session.save_session(
        project_name=STRESS_PROJECT,
        current_layer=1,
        summary="stress test run",
        last_checkpoint_reason="stress testing all 14 tools",
    )
    assert not r.errors, r.errors
    assert "state" in r.data
    assert r.data["state"]["project_name"] == STRESS_PROJECT
    assert Path(".github/workflow-state.json").exists()


# ---------------------------------------------------------------------------
# Session — save_plan / load_plan
# ---------------------------------------------------------------------------

def test_save_plan_layer1_creates_file(session):
    r = session.save_plan(
        project_name=STRESS_PROJECT,
        layer=1,
        content="# Stress Test Layer 1\n\nTest plan content for verification.",
    )
    assert not r.errors, r.errors
    assert r.data["layer"] == 1
    plan_file = Path(f".github/plans/{STRESS_PROJECT}_layer1_strategic.md")
    assert plan_file.exists()


def test_save_plan_gate_blocks_skipped_layer(session):
    """save_plan(layer=2) without an existing layer 1 for a new project must fail."""
    r = session.save_plan(
        project_name="gate_sentinel_xyz",
        layer=2,
        content="This should be blocked by the structural gate.",
    )
    assert r.errors
    assert "Gate check failed" in r.errors[0]


def test_load_plan_reads_written_content(session):
    r = session.load_plan(project_name=STRESS_PROJECT, layer=1)
    assert not r.errors, r.errors
    assert "Stress Test Layer 1" in r.data["content"]


def test_load_plan_missing_returns_error(session):
    r = session.load_plan(project_name=STRESS_PROJECT, layer=5)
    assert r.errors
    assert "not found" in r.errors[0].lower() or "Plan not found" in r.errors[0]


# ---------------------------------------------------------------------------
# Session — checkpoint
# ---------------------------------------------------------------------------

def test_checkpoint_updates_state_and_reminds_memory(session):
    r = session.checkpoint(
        project_name=STRESS_PROJECT,
        reason="stress test checkpoint",
        current_layer=1,
        summary="verifying all tools work end-to-end",
    )
    assert not r.errors, r.errors
    assert "memory_reminder" in r.data
    assert STRESS_PROJECT in r.data["memory_reminder"]
    assert "state" in r.data


# ---------------------------------------------------------------------------
# Executor — validate_code
# ---------------------------------------------------------------------------

def test_validate_code_known_good_file(executor):
    r = executor.validate_code(path="mcp_servers/session/server.py")
    assert not r.errors, r.errors
    assert r.data["syntax_ok"] is True
    assert r.data["tier"] is not None


def test_validate_code_missing_file_returns_error(executor):
    r = executor.validate_code(path="totally_nonexistent_file_xyz.py")
    assert r.errors


# ---------------------------------------------------------------------------
# Executor — get_server_health
# ---------------------------------------------------------------------------

def test_get_server_health_all_three_healthy(executor):
    r = executor.get_server_health()
    assert not r.errors, r.errors
    assert r.data["total_count"] == 4
    assert r.data["healthy_count"] == 4, (
        f"Unhealthy servers: "
        f"{[s for s in r.data['servers'] if not s['syntax_ok']]}"
    )


# ---------------------------------------------------------------------------
# Executor — verify_tool_registration (all 3 servers)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("server_file", SESSION_FILES)
def test_verify_tool_registration_no_gaps(executor, server_file):
    r = executor.verify_tool_registration(
        server_path=f"mcp_servers/{server_file}"
    )
    assert not r.errors, r.errors
    assert r.data["gap_count"] == 0, (
        f"{server_file} has registration gaps: {r.data['gaps']}"
    )


# ---------------------------------------------------------------------------
# Executor — verify_sync_wrappers (all 3 servers)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("server_file", SESSION_FILES)
def test_verify_sync_wrappers_no_gaps(executor, server_file):
    r = executor.verify_sync_wrappers(
        server_path=f"mcp_servers/{server_file}"
    )
    assert not r.errors, r.errors
    assert r.data["gap_count"] == 0, (
        f"{server_file} has missing sync wrappers: {r.data['gaps']}"
    )


# ---------------------------------------------------------------------------
# Executor — find_symbol_usages
# ---------------------------------------------------------------------------

def test_find_symbol_usages_finds_known_symbol(executor):
    r = executor.find_symbol_usages(
        symbol="BaseAgentServer",
        search_path="mcp_servers",
    )
    assert not r.errors, r.errors
    assert r.data["usage_count"] > 0
    assert all("file_path" in u for u in r.data["usages"])
    assert all("usage_type" in u for u in r.data["usages"])


def test_find_symbol_usages_nonexistent_returns_empty(executor):
    r = executor.find_symbol_usages(
        symbol="__COMPLETELY_NONEXISTENT_SYM_XYZ__",
        search_path="mcp_servers",
    )
    assert not r.errors, r.errors
    assert r.data["usage_count"] == 0


def test_find_symbol_usages_bad_search_path_returns_error(executor):
    r = executor.find_symbol_usages(
        symbol="BaseAgentServer",
        search_path="this/path/does/not/exist",
    )
    assert r.errors


# ---------------------------------------------------------------------------
# Executor — run_quality_gates (lint-only: avoids pytest/bandit subprocess hang)
# ---------------------------------------------------------------------------

def test_run_quality_gates_lint_only(executor):
    """Verify the gate runner machinery works end-to-end with lint only.

    pytest and bandit gates are excluded here to avoid the Windows asyncio
    nested-subprocess hang observed when run_quality_gates is invoked through
    the live MCP event loop. The lint gate is sufficient to exercise the full
    _run_subprocess_gate → asyncio.create_subprocess_exec path.
    """
    r = executor.run_quality_gates(
        paths=["mcp_servers/session"],
        gates=["lint"],
        stop_on_failure=False,
    )
    assert not r.errors, r.errors
    assert "all_passed" in r.data
    assert r.data["gates_run"] == 1
    results = r.data["results"]
    assert len(results) == 1
    assert results[0]["gate"] == "lint"


# ---------------------------------------------------------------------------
# Memory — write_memory
# ---------------------------------------------------------------------------

def test_write_memory_creates_entry(memory):
    r = memory.write_memory(
        project=STRESS_PROJECT,
        phase="tool verification",
        what_was_built="All 14 ATLAS tools stress-tested via direct sync wrapper invocation",
        technical_choices="Sync wrappers → _run() → ThreadPoolExecutor → asyncio.run()",
        learnings="All tools functional outside of MCP event loop context.",
        failures="run_quality_gates hangs in live MCP context on Windows (asyncio nested loop)",
        debt_avoided="Did not suppress subprocess tools — documented limitation instead",
        performance="Full 14-tool coverage in single pytest run",
    )
    assert not r.errors, r.errors
    assert "file_path" in r.data
    assert Path(".github/memory.md").exists()


# ---------------------------------------------------------------------------
# Memory — read_memory
# ---------------------------------------------------------------------------

def test_read_memory_returns_list(memory):
    r = memory.read_memory()
    assert not r.errors, r.errors
    assert isinstance(r.data, list)
    assert len(r.data) > 0


def test_read_memory_project_filter_finds_entry(memory):
    r = memory.read_memory(project_filter=STRESS_PROJECT)
    assert not r.errors, r.errors
    assert isinstance(r.data, list)
    assert any(e.get("project") == STRESS_PROJECT for e in r.data), (
        f"No entry for project '{STRESS_PROJECT}' found. Got: "
        f"{[e.get('project') for e in r.data]}"
    )


def test_read_memory_query_returns_relevance_scores(memory):
    r = memory.read_memory(query="stress test tools", top_n=5)
    assert not r.errors, r.errors
    assert isinstance(r.data, list)
    if r.data:
        assert "relevance_score" in r.data[0], (
            "Expected relevance_score in ranked results"
        )


# ---------------------------------------------------------------------------
# Memory — search_memory
# ---------------------------------------------------------------------------

def test_search_memory_finds_written_entry(memory):
    r = memory.search_memory(STRESS_PROJECT)
    assert not r.errors, r.errors
    assert isinstance(r.data, list)
    assert len(r.data) > 0, (
        f"search_memory(keywords=['{STRESS_PROJECT}']) returned no matches"
    )


def test_search_memory_no_match_returns_empty(memory):
    r = memory.search_memory("__NONEXISTENT_KEYWORD_XYZ_STRESS_9999__")
    assert not r.errors, r.errors
    assert r.data == []


# ---------------------------------------------------------------------------
# Cleanup — remove stress plan files written during this run
# ---------------------------------------------------------------------------

def test_zzz_cleanup_stress_plans(session):
    """Remove .github/plans/ files written by this stress run."""
    removed = []
    for f in Path(".github/plans").glob(f"{STRESS_PROJECT}_*.md"):
        f.unlink()
        removed.append(f.name)
    assert not list(Path(".github/plans").glob(f"{STRESS_PROJECT}_*.md")), (
        "Not all stress plan files were cleaned up"
    )
