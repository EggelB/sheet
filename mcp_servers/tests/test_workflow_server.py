"""Tests for mcp_servers/workflow/server.py — TempoWorkflowServer tools."""
import asyncio
import pytest

from mcp_servers.utils.results import ResultStatus
from mcp_servers.workflow.server import TempoWorkflowServer


VALID_YAML = """
phase_id: p1
phase_type: implementation
components:
  - id: c1
    name: C1
    interface_contract:
      inputs: [input]
      outputs: [output]
    constraint_surfaces: [surface]
    fillable: true
    fill_dependencies: []
output_schema:
  format: json
  required_fields: [result]
"""

INVALID_YAML = """
phase_id: ""
phase_type: research
components: []
output_schema:
  format: json
  required_fields: []
"""


@pytest.fixture
def server():
    return TempoWorkflowServer()


class TestTempoWorkflowServer:
    def test_agent_name(self, server):
        assert server.agent_name == "tempo.workflow"

    def test_tool_count_at_most_20(self, server):
        assert len(server._get_tools()) <= 20

    def test_tool_names_include_validate_and_run(self, server):
        names = {t.name for t in server._get_tools()}
        assert "validate_skeleton" in names
        assert "run_workflow" in names

    def test_validate_skeleton_valid_returns_valid_true(self, server):
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(
                server._tool_validate_skeleton(VALID_YAML)
            )
        finally:
            loop.close()
        assert result.status == ResultStatus.SUCCESS
        assert result.data["valid"] is True
        assert result.data["errors"] == []

    def test_validate_skeleton_invalid_returns_valid_false(self, server):
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(
                server._tool_validate_skeleton(INVALID_YAML)
            )
        finally:
            loop.close()
        assert result.status == ResultStatus.SUCCESS
        assert result.data["valid"] is False
        assert len(result.data["errors"]) > 0

    def test_run_workflow_returns_routing(self, server):
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(
                server._tool_run_workflow(VALID_YAML)
            )
        finally:
            loop.close()
        assert result.status == ResultStatus.SUCCESS
        assert "routing" in result.data
        assert result.data["routing"] in ("single_pass", "shape_fill")
