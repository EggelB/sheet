"""Tier router for the TEMPO Shape→Fill workflow engine.

Routes a ShapeSkeleton to SINGLE_PASS or SHAPE_FILL based on leaf component count
vs. the configurable threshold.
"""
from __future__ import annotations

from mcp_servers.workflow.shape import RoutingDecision, ShapeSkeleton


class TierRouter:
    """Routes a skeleton to SINGLE_PASS or SHAPE_FILL.

    Break-even rule: leaf_count >= threshold → SHAPE_FILL; else SINGLE_PASS.
    """

    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold

    def route(self, skeleton: ShapeSkeleton) -> RoutingDecision:
        """Return SHAPE_FILL if skeleton.leaf_count() >= self.threshold, else SINGLE_PASS."""
        if skeleton.leaf_count() >= self.threshold:
            return RoutingDecision.SHAPE_FILL
        return RoutingDecision.SINGLE_PASS
