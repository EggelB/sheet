"""tempo.workflow — TEMPO Shape→Fill Workflow MCP server.

Tools
-----
validate_skeleton   Validate a ShapeSkeleton YAML via PreFillGate.
run_workflow        Parse, gate, and route a ShapeSkeleton YAML.
                    Returns routing decision for Copilot agent orchestration.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool

from mcp_servers.base import BaseAgentServer
from mcp_servers.executor.config import TempoConfig
from mcp_servers.utils.results import Result
from mcp_servers.workflow.engine import WorkflowEngine
from mcp_servers.workflow.gate import PreFillGate
from mcp_servers.workflow.shape import ShapeSkeleton


class TempoWorkflowServer(BaseAgentServer):
    """MCP server exposing the TEMPO Shape→Fill workflow as two tools."""

    @property
    def agent_name(self) -> str:
        return "tempo.workflow"

    def _get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="validate_skeleton",
                description=(
                    "Validate a ShapeSkeleton YAML against the PreFillGate invariants. "
                    "Returns {valid: bool, errors: list[str]}."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "skeleton_yaml": {
                            "type": "string",
                            "description": "YAML text of the ShapeSkeleton to validate.",
                        }
                    },
                    "required": ["skeleton_yaml"],
                },
            ),
            Tool(
                name="run_workflow",
                description=(
                    "Parse, gate, and route a ShapeSkeleton YAML. "
                    "Returns routing decision for Copilot agent orchestration."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "skeleton_yaml": {
                            "type": "string",
                            "description": "YAML text of the ShapeSkeleton to route.",
                        }
                    },
                    "required": ["skeleton_yaml"],
                },
            ),
        ]

    async def _tool_validate_skeleton(self, skeleton_yaml: str) -> Result:
        """Validate skeleton_yaml via PreFillGate."""
        try:
            skeleton = ShapeSkeleton.from_yaml(skeleton_yaml)
            result = PreFillGate.validate(skeleton)
            return Result.ok({"valid": result.status.value == "success", "errors": result.errors})
        except Exception as exc:
            return Result.fail([str(exc)])

    async def _tool_run_workflow(self, skeleton_yaml: str) -> Result:
        """Parse, gate, and route skeleton_yaml."""
        engine = WorkflowEngine(config=TempoConfig())
        result = engine.run(skeleton_yaml)
        if result.is_ok():
            return Result.ok({"routing": result.data["routing"]})
        return Result.fail(result.errors)


if __name__ == "__main__":
    TempoWorkflowServer.cli_main()
