"""Tests for config-driven gate dispatch and validate_code branches — 6 tests.

F-4 applied: import asyncio at module top; asyncio.run() not get_event_loop().
"""

import asyncio
import sys

import pytest
from unittest.mock import patch, AsyncMock

from mcp_servers.executor.environment import EnvironmentTier
from mcp_servers.executor.server import ExecutorServer, GateResult


@pytest.fixture
def server():
    return ExecutorServer()


class TestRunGateDispatch:
    def test_run_gate_uses_per_tier_csharp(self, server):
        """_run_gate builds dotnet command for CSHARP tier."""
        captured = {}

        async def fake_gate(gate, cmd, ff):
            captured["cmd"] = cmd
            return GateResult(gate, True, 0, "", [])

        with patch.object(server, "_run_subprocess_gate", side_effect=fake_gate):
            asyncio.run(server._run_gate("lint", "src/", EnvironmentTier.CSHARP))
        assert captured["cmd"][0] == "dotnet"

    def test_run_gate_falls_back_to_default_for_generic(self, server):
        """_run_gate uses Python defaults for GENERIC (no per_tier entry)."""
        captured = {}

        async def fake_gate(gate, cmd, ff):
            captured["cmd"] = cmd
            return GateResult(gate, True, 0, "", [])

        with patch.object(server, "_run_subprocess_gate", side_effect=fake_gate):
            asyncio.run(server._run_gate("lint", "src/Main.java", EnvironmentTier.GENERIC))
        assert sys.executable in captured["cmd"]

    def test_python_token_replaced_with_sys_executable(self, server):
        """'python' token in command list is replaced with sys.executable."""
        captured = {}

        async def fake_gate(gate, cmd, ff):
            captured["cmd"] = cmd
            return GateResult(gate, True, 0, "", [])

        with patch.object(server, "_run_subprocess_gate", side_effect=fake_gate):
            asyncio.run(server._run_gate("lint", "mcp_servers/", EnvironmentTier.LOCAL_PYTHON))
        assert "python" not in captured["cmd"]
        assert sys.executable in captured["cmd"]


class TestValidateCodeBranches:
    def test_validate_code_javascript_validated_true(self, tmp_path, server):
        js_file = tmp_path / "app.js"
        js_file.write_text("const x = 1;\n", encoding="utf-8")

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"", b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = asyncio.run(server._tool_validate_code(str(js_file)))
        assert result.data["validated"] is True

    def test_validate_code_typescript_validated_false_with_signal(self, tmp_path, server):
        ts_file = tmp_path / "app.ts"
        ts_file.write_text("const x: number = 1;\n", encoding="utf-8")
        result = asyncio.run(server._tool_validate_code(str(ts_file)))
        assert result.data["validated"] is False
        assert any("single_file_validation_not_supported" in s for s in result.data["signals"])


class TestQualityGatesTierUsed:
    def test_tier_used_in_result(self, tmp_path, server):
        py_file = tmp_path / "hello.py"
        py_file.write_text("print('hi')\n", encoding="utf-8")

        async def fake_gate(gate, paths, tier=EnvironmentTier.LOCAL_PYTHON):
            return GateResult(gate, True, 0, "", [])

        with patch.object(server, "_run_gate", side_effect=fake_gate):
            result = asyncio.run(
                server._tool_run_quality_gates([str(py_file)], gates=["lint"])
            )
        assert "tier_used" in result.data
