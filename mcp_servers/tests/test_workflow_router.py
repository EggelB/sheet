"""Tests for mcp_servers/workflow/router.py — TierRouter routing decisions."""
from mcp_servers.workflow.router import TierRouter
from mcp_servers.workflow.shape import (
    InterfaceContract,
    OutputSchema,
    RoutingDecision,
    ShapeComponent,
    ShapeSkeleton,
)


def _make_skeleton(leaf_count: int, non_leaf_fillable: int = 0) -> ShapeSkeleton:
    """Create skeleton with exact leaf_count leaves and non_leaf_fillable non-leaves."""
    components = []
    for i in range(leaf_count):
        components.append(ShapeComponent(
            id=f"leaf-{i}", name=f"Leaf {i}",
            interface_contract=InterfaceContract(inputs=["i"], outputs=["o"]),
            constraint_surfaces=["s"],
            fillable=True,
            fill_dependencies=[],
        ))
    for i in range(non_leaf_fillable):
        components.append(ShapeComponent(
            id=f"nonleaf-{i}", name=f"NonLeaf {i}",
            interface_contract=InterfaceContract(inputs=["i"], outputs=["o"]),
            constraint_surfaces=["s"],
            fillable=True,
            fill_dependencies=[f"leaf-{i}"],
        ))
    return ShapeSkeleton(
        phase_id="p", phase_type="implementation",
        components=components,
        output_schema=OutputSchema(format="json", required_fields=["r"]),
    )


class TestTierRouter:
    def test_default_threshold_is_3(self):
        router = TierRouter()
        assert router.threshold == 3

    def test_below_threshold_is_single_pass(self):
        router = TierRouter(threshold=3)
        skeleton = _make_skeleton(leaf_count=2)
        assert router.route(skeleton) == RoutingDecision.SINGLE_PASS

    def test_at_threshold_is_shape_fill(self):
        router = TierRouter(threshold=3)
        skeleton = _make_skeleton(leaf_count=3)
        assert router.route(skeleton) == RoutingDecision.SHAPE_FILL

    def test_above_threshold_is_shape_fill(self):
        router = TierRouter(threshold=3)
        skeleton = _make_skeleton(leaf_count=5)
        assert router.route(skeleton) == RoutingDecision.SHAPE_FILL

    def test_custom_threshold(self):
        router = TierRouter(threshold=1)
        skeleton = _make_skeleton(leaf_count=1)
        assert router.route(skeleton) == RoutingDecision.SHAPE_FILL

    def test_non_leaf_components_do_not_count(self):
        router = TierRouter(threshold=3)
        # 2 leaves + 2 non-leaves → leaf_count==2 → SINGLE_PASS
        skeleton = _make_skeleton(leaf_count=2, non_leaf_fillable=2)
        assert router.route(skeleton) == RoutingDecision.SINGLE_PASS
