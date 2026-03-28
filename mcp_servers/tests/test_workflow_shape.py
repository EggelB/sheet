"""Tests for mcp_servers/workflow/shape.py — ShapeSkeleton parse and leaf detection."""
import pytest
from mcp_servers.workflow.shape import (
    InterfaceContract,
    ShapeComponent,
    ShapeSkeleton,
)

VALID_YAML = """
phase_id: phase-1
phase_type: implementation
components:
  - id: comp-a
    name: Component A
    interface_contract:
      inputs: [input1]
      outputs: [output1]
    constraint_surfaces: [surface1]
    fillable: true
    fill_dependencies: []
  - id: comp-b
    name: Component B
    interface_contract:
      inputs: [input2]
      outputs: [output2]
    constraint_surfaces: [surface2]
    fillable: true
    fill_dependencies: [comp-a]
  - id: comp-c
    name: Component C
    interface_contract:
      inputs: [input3]
      outputs: [output3]
    constraint_surfaces: [surface3]
    fillable: true
    fill_dependencies: []
output_schema:
  format: json
  required_fields: [result]
"""


class TestShapeComponent:
    def test_leaf_when_fillable_no_dependencies(self):
        c = ShapeComponent(
            id="x", name="X",
            interface_contract=InterfaceContract(inputs=["i"], outputs=["o"]),
            constraint_surfaces=["s"],
            fillable=True,
            fill_dependencies=[],
        )
        assert c.is_leaf() is True

    def test_not_leaf_when_has_dependencies(self):
        c = ShapeComponent(
            id="x", name="X",
            interface_contract=InterfaceContract(inputs=["i"], outputs=["o"]),
            constraint_surfaces=["s"],
            fillable=True,
            fill_dependencies=["dep1"],
        )
        assert c.is_leaf() is False

    def test_not_leaf_when_not_fillable(self):
        c = ShapeComponent(
            id="x", name="X",
            interface_contract=InterfaceContract(inputs=["i"], outputs=["o"]),
            constraint_surfaces=["s"],
            fillable=False,
            fill_dependencies=[],
        )
        assert c.is_leaf() is False


class TestShapeSkeletonFromYaml:
    def test_parses_valid_yaml(self):
        skeleton = ShapeSkeleton.from_yaml(VALID_YAML)
        assert skeleton.phase_id == "phase-1"
        assert skeleton.phase_type == "implementation"
        assert len(skeleton.components) == 3
        assert skeleton.output_schema.required_fields == ["result"]

    def test_leaf_count_counts_only_leaves(self):
        skeleton = ShapeSkeleton.from_yaml(VALID_YAML)
        # comp-a and comp-c are leaves (fillable, no deps); comp-b has dep on comp-a
        assert skeleton.leaf_count() == 2

    def test_invalid_yaml_raises(self):
        with pytest.raises(Exception):
            ShapeSkeleton.from_yaml("not: valid: yaml: ::::")

    def test_non_mapping_yaml_raises(self):
        with pytest.raises((ValueError, Exception)):
            ShapeSkeleton.from_yaml("- item1\n- item2\n")

    def test_missing_optional_keys_use_defaults(self):
        skeleton = ShapeSkeleton.from_yaml("phase_id: p\nphase_type: review\n")
        assert skeleton.components == []
        assert skeleton.output_schema.required_fields == []
        assert skeleton.leaf_count() == 0
