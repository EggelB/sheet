"""Integration tests — verify TEMPO server namespace, registration, and health."""
import json
from pathlib import Path

from mcp_servers.executor.config import TempoConfig


class TestTempoNamespace:
    """Verify TEMPO server naming convention."""
    
    def test_all_server_agent_names(self) -> None:
        """All four servers should have tempo.* agent names."""
        from mcp_servers.executor.server import ExecutorServer
        from mcp_servers.memory.server import MemoryServer
        from mcp_servers.session.server import SessionServer
        from mcp_servers.workflow.server import TempoWorkflowServer
        
        servers = [
            ExecutorServer(),
            MemoryServer(),
            SessionServer(),
            TempoWorkflowServer(),
        ]
        names = [s.agent_name for s in servers]
        for name in names:
            assert name.startswith("tempo."), f"Non-tempo agent name: {name}"
        assert set(names) == {"tempo.executor", "tempo.memory", "tempo.session", "tempo.workflow"}


class TestMCPJsonRegistration:
    """Verify .vscode/mcp.json contains all four servers."""
    
    def test_mcp_json_has_all_four_tempo_keys(self) -> None:
        """All four tempo.* servers must be registered in mcp.json."""
        mcp_path = Path(__file__).parents[2] / ".vscode" / "mcp.json"
        data = json.loads(mcp_path.read_text())
        keys = set(data["servers"].keys())
        assert {"tempo.session", "tempo.executor", "tempo.memory", "tempo.workflow"} <= keys


class TestTempoConfigSchema:
    """Verify TempoConfig has correct fields and no stale references."""
    
    def test_tempo_config_phase_fields(self) -> None:
        """TempoConfig must have shape_fill_threshold=3 and no min_fill_length."""
        config = TempoConfig()
        assert config.shape_fill_threshold == 3
        # Verify min_fill_length does not exist
        assert not hasattr(config, "min_fill_length")


class TestServerHealth:
    """Verify all four servers can be instantiated and are healthy."""
    
    def test_four_server_health_all_healthy(self) -> None:
        """All four servers must instantiate with tempo.* agent names."""
        from mcp_servers.executor.server import ExecutorServer
        from mcp_servers.memory.server import MemoryServer
        from mcp_servers.session.server import SessionServer
        from mcp_servers.workflow.server import TempoWorkflowServer
        
        servers = [
            ExecutorServer(),
            MemoryServer(),
            SessionServer(),
            TempoWorkflowServer(),
        ]
        total = len(servers)
        assert total == 4
        for s in servers:
            assert s.agent_name.startswith("tempo.")


class TestWorkflowServerTools:
    """Verify workflow server has correct tools registered."""
    
    def test_workflow_server_tool_registration(self) -> None:
        """Workflow server must have validate_skeleton and run_workflow tools."""
        from mcp_servers.workflow.server import TempoWorkflowServer
        
        server = TempoWorkflowServer()
        tools = server._get_tools()
        tool_names = [t.name for t in tools]
        assert "validate_skeleton" in tool_names
        assert "run_workflow" in tool_names
        assert len(tool_names) <= 20


class TestNoATLASResidueInCode:
    """Verify no ATLAS references remain in mcp_servers codebase."""
    
    def test_no_atlas_residue_in_mcp_servers(self) -> None:
        """No atlas. or AtlasConfig references should exist in mcp_servers."""
        src = Path(__file__).parents[1].parent / "mcp_servers"
        self_file = Path(__file__)
        for py_file in src.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            if ".install" in str(py_file):
                continue
            if py_file == self_file:
                continue
            text = py_file.read_text(encoding="utf-8")
            assert "atlas." not in text, f"atlas residue found in {py_file}"
            assert "AtlasConfig" not in text, f"AtlasConfig residue found in {py_file}"
