"""TEMPO Shape→Fill Workflow Engine — parse → gate → route."""
from __future__ import annotations

from mcp_servers.executor.config import TempoConfig
from mcp_servers.utils.results import Result, ResultStatus
from mcp_servers.workflow.gate import PreFillGate
from mcp_servers.workflow.router import TierRouter
from mcp_servers.workflow.shape import ShapeSkeleton


class WorkflowEngine:
    """Orchestrates the Shape→Fill pipeline decision for a single skeleton.

    Parse → Gate → Route → Return routing decision.
    Copilot Chat agents perform the actual fills based on the routing decision.
    """

    def __init__(self, config: TempoConfig | None = None) -> None:
        self._config = config or TempoConfig()
        self._router = TierRouter(threshold=self._config.shape_fill_threshold)

    def run(self, skeleton_yaml: str) -> Result:
        """Parse, gate, and route skeleton_yaml. Returns routing decision."""
        try:
            skeleton = ShapeSkeleton.from_yaml(skeleton_yaml)
        except Exception as exc:
            return Result.fail([f"YAML parse error: {exc}"])

        gate_result = PreFillGate.validate(skeleton)
        if gate_result.status != ResultStatus.SUCCESS:
            return gate_result

        routing = self._router.route(skeleton)
        return Result.ok({"routing": routing.value})
