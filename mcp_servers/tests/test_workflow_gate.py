"""Tests for mcp_servers/workflow/gate.py — PreFillGate invariant validation."""
from mcp_servers.utils.results import ResultStatus
from mcp_servers.workflow.gate import PreFillGate
from mcp_servers.workflow.shape import (
    InterfaceContract,
    OutputSchema,
    ShapeComponent,
    ShapeSkeleton,
)


def _valid_skeleton(phase_id="p1", extra_components=None) -> ShapeSkeleton:
    """Return a skeleton that passes all invariants."""
    return ShapeSkeleton(
        phase_id=phase_id,
        phase_type="implementation",
        components=[
            ShapeComponent(
                id="c1", name="C1",
                interface_contract=InterfaceContract(inputs=["in"], outputs=["out"]),
                constraint_surfaces=["surface"],
                fillable=True,
                fill_dependencies=[],
            ),
            *(extra_components or []),
        ],
        output_schema=OutputSchema(format="json", required_fields=["result"]),
    )


class TestPreFillGate:
    def test_valid_skeleton_passes(self):
        result = PreFillGate.validate(_valid_skeleton())
        assert result.status == ResultStatus.SUCCESS
        assert result.data is not None

    def test_invariant1_empty_phase_id_fails(self):
        skeleton = _valid_skeleton(phase_id="")
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        assert any("phase_id" in e for e in result.errors)

    def test_invariant2_empty_components_fails(self):
        skeleton = ShapeSkeleton(
            phase_id="p1", phase_type="design",
            components=[],
            output_schema=OutputSchema(format="json", required_fields=["r"]),
        )
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        assert any("components" in e for e in result.errors)

    def test_invariant3_empty_inputs_fails(self):
        skeleton = ShapeSkeleton(
            phase_id="p1", phase_type="design",
            components=[
                ShapeComponent(
                    id="c1", name="C1",
                    interface_contract=InterfaceContract(inputs=[], outputs=["out"]),
                    constraint_surfaces=["s"],
                    fillable=True, fill_dependencies=[],
                )
            ],
            output_schema=OutputSchema(format="json", required_fields=["r"]),
        )
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        assert any("c1" in e for e in result.errors)

    def test_invariant3_empty_constraint_surfaces_fails(self):
        skeleton = ShapeSkeleton(
            phase_id="p1", phase_type="design",
            components=[
                ShapeComponent(
                    id="c2", name="C2",
                    interface_contract=InterfaceContract(inputs=["in"], outputs=["out"]),
                    constraint_surfaces=[],
                    fillable=True, fill_dependencies=[],
                )
            ],
            output_schema=OutputSchema(format="json", required_fields=["r"]),
        )
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        assert any("c2" in e for e in result.errors)

    def test_invariant4_empty_required_fields_fails(self):
        skeleton = _valid_skeleton()
        skeleton.output_schema.required_fields = []
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        assert any("output_schema" in e for e in result.errors)

    def test_multiple_violations_all_collected(self):
        """Gate does not short-circuit — all violations reported."""
        skeleton = ShapeSkeleton(
            phase_id="",
            phase_type="design",
            components=[
                ShapeComponent(
                    id="c1", name="C1",
                    interface_contract=InterfaceContract(inputs=[], outputs=[]),
                    constraint_surfaces=[],
                    fillable=True, fill_dependencies=[],
                )
            ],
            output_schema=OutputSchema(format="json", required_fields=[]),
        )
        result = PreFillGate.validate(skeleton)
        assert result.status == ResultStatus.FAILURE
        # Should have at least 4 distinct violations
        assert len(result.errors) >= 4
