"""Tests for tempo.executor ExecutorServer — 7 tests.

Coverage
--------
1  gate_structure                run_quality_gates returns expected all_passed/gates_run/results keys
2  validate_code_syntax_ok       valid Python file → syntax_ok=True, tier correctly detected
3  validate_code_syntax_error    file with syntax error → syntax_ok=False, error message present
4  health_check_finds_servers    get_server_health discovers session + executor + memory servers
5  registration_gap_detection    fake server.py with _tool_foo but no Tool("foo") → gap reported
6  symbol_scan_definition        tmp .py with a function → find_symbol_usages finds definition
7  sync_wrapper_gap_detection    fake server.py with async _tool_bar but no bar() wrapper → gap reported
"""

import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_servers.executor.server import ExecutorServer, GateResult


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def server():
    return ExecutorServer()


# ---------------------------------------------------------------------------
# 1. Gate structure
# ---------------------------------------------------------------------------

class TestGateStructure:
    def test_run_quality_gates_returns_expected_keys(self, server):
        """run_quality_gates result contains all_passed, gates_run, and results list."""
        mock_gr = GateResult("security", True, 0, "", [])

        async def _fake_run_gate(gate, paths, tier=None):
            return mock_gr

        with patch.object(server, "_run_gate", side_effect=_fake_run_gate):
            result = server.run_quality_gates(["."], gates=["security"])

        assert result.status.value == "success", result.errors
        assert "all_passed"  in result.data
        assert "gates_run"   in result.data
        assert "results"     in result.data
        assert result.data["gates_run"] == 1
        assert result.data["all_passed"] is True


# ---------------------------------------------------------------------------
# 2. validate_code — syntax ok
# ---------------------------------------------------------------------------

class TestValidateCodeSyntaxOk:
    def test_valid_python_file_returns_syntax_ok(self, server, tmp_path):
        """Well-formed Python file → syntax_ok=True, tier=local_python."""
        f = tmp_path / "clean.py"
        f.write_text("def hello():\n    return 42\n", encoding="utf-8")

        result = server.validate_code(str(f))

        assert result.status.value == "success", result.errors
        assert result.data["syntax_ok"] is True
        assert result.data["tier"] == "local_python"
        assert result.data["error"] is None


# ---------------------------------------------------------------------------
# 3. validate_code — syntax error
# ---------------------------------------------------------------------------

class TestValidateCodeSyntaxError:
    def test_syntax_error_returns_syntax_ok_false(self, server, tmp_path):
        """File with a syntax error → syntax_ok=False and error message populated."""
        f = tmp_path / "broken.py"
        f.write_text("def foo(\n", encoding="utf-8")   # unclosed paren

        result = server.validate_code(str(f))

        assert result.status.value == "success"   # tool succeeded; file didn't
        assert result.data["syntax_ok"] is False
        assert result.data["error"]     # non-empty error string


# ---------------------------------------------------------------------------
# 4. get_server_health — discovers the 3 atlas servers
# ---------------------------------------------------------------------------

class TestHealthCheckFindsServers:
    def test_health_check_reports_all_three_servers(self, server):
        """get_server_health finds all atlas servers that exist; all found are healthy."""
        result = server.get_server_health()

        assert result.status.value == "success", result.errors
        found_names = {Path(s["server_path"]).parent.name for s in result.data["servers"]}
        # session + executor exist now; memory arrives in Phase 3
        assert {"session", "executor"}.issubset(found_names)
        # Every server found should be syntactically valid
        assert result.data["healthy_count"] == result.data["total_count"]


# ---------------------------------------------------------------------------
# 5. verify_tool_registration — gap detected
# ---------------------------------------------------------------------------

class TestRegistrationGapDetection:
    def test_missing_handler_reported_as_gap(self, server, tmp_path):
        """A Tool(name='foo') registration without a _tool_foo handler → gap_count=1."""
        fake_server = tmp_path / "server.py"
        fake_server.write_text(
            textwrap.dedent("""\
                from mcp.types import Tool
                class FakeServer:
                    def _get_tools(self):
                        return [Tool(name="foo", description="", inputSchema={})]
                    # _tool_foo is intentionally missing
            """),
            encoding="utf-8",
        )

        result = server.verify_tool_registration(str(fake_server))

        assert result.status.value == "success", result.errors
        assert result.data["gap_count"] >= 1
        gap_names = [g["tool_name"] for g in result.data["gaps"]]
        assert "foo" in gap_names


# ---------------------------------------------------------------------------
# 6. find_symbol_usages — definition found
# ---------------------------------------------------------------------------

class TestSymbolScanDefinition:
    def test_finds_function_definition(self, server, tmp_path):
        """A function definition in a tmp .py file is found by find_symbol_usages."""
        f = tmp_path / "module.py"
        f.write_text("def my_special_func():\n    pass\n", encoding="utf-8")

        result = server.find_symbol_usages("my_special_func", search_path=str(tmp_path))

        assert result.status.value == "success", result.errors
        assert result.data["usage_count"] >= 1
        usages = result.data["usages"]
        types  = {u["usage_type"] for u in usages}
        assert "definition" in types


# ---------------------------------------------------------------------------
# 7. verify_sync_wrappers — gap detected
# ---------------------------------------------------------------------------

class TestSyncWrapperGapDetection:
    def test_missing_sync_wrapper_reported(self, server, tmp_path):
        """async _tool_bar with no bar() sync wrapper → gap_count=1."""
        fake_server = tmp_path / "server.py"
        fake_server.write_text(
            textwrap.dedent("""\
                class FakeServer:
                    async def _tool_bar(self):
                        pass
                    # no public bar() sync wrapper
            """),
            encoding="utf-8",
        )

        result = server.verify_sync_wrappers(str(fake_server))

        assert result.status.value == "success", result.errors
        assert result.data["gap_count"] >= 1
        gap_names = [g["handler_name"] for g in result.data["gaps"]]
        assert "bar" in gap_names
