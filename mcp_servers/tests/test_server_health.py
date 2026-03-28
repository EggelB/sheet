"""Tests for get_server_health dynamic discovery — 2 tests.

F-4 applied: sync wrapper used; no asyncio in test bodies.
"""

import pytest
from mcp_servers.executor.server import ExecutorServer


@pytest.fixture
def server():
    return ExecutorServer()


class TestServerHealthDiscovery:
    def test_only_mcp_servers_included(self, tmp_path, server):
        for name, content in [
            ("session",    "Tool(name='load_session')\n"),
            ("executor",   "Tool(name='run_quality_gates')\n"),
            ("memory",     "Tool(name='read_memory')\n"),
            ("workflow",   "Tool(name='run_workflow')\n"),
            ("notaserver", "def main(): pass\n"),
        ]:
            d = tmp_path / "mcp_servers" / name
            d.mkdir(parents=True)
            (d / "server.py").write_text(content, encoding="utf-8")

        server.workspace_root = str(tmp_path)
        result = server.get_server_health()
        assert result.data["total_count"] == 4
        assert not any("notaserver" in h["server_path"] for h in result.data["servers"])

    def test_new_server_auto_discovered(self, tmp_path, server):
        for name in ("session", "executor", "memory", "workflow", "newserver"):
            d = tmp_path / "mcp_servers" / name
            d.mkdir(parents=True)
            (d / "server.py").write_text(f"Tool(name='{name}_tool')\n", encoding="utf-8")

        server.workspace_root = str(tmp_path)
        result = server.get_server_health()
        assert result.data["total_count"] == 5


class TestWorkflowServerToolCount:
    def test_workflow_server_has_at_most_20_tools(self):
        from mcp_servers.workflow.server import TempoWorkflowServer
        s = TempoWorkflowServer()
        assert len(s._get_tools()) <= 20
