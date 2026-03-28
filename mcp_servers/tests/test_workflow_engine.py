"""Tests for mcp_servers/workflow/engine.py — WorkflowEngine pipeline."""
from mcp_servers.executor.config import TempoConfig
from mcp_servers.utils.results import ResultStatus
from mcp_servers.workflow.engine import WorkflowEngine
from mcp_servers.workflow.shape import RoutingDecision


SINGLE_PASS_YAML = """
phase_id: p1
phase_type: research
components:
  - id: c1
    name: C1
    interface_contract:
      inputs: [input]
      outputs: [output]
    constraint_surfaces: [surface]
    fillable: true
    fill_dependencies: []
  - id: c2
    name: C2
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

SHAPE_FILL_YAML = """
phase_id: p2
phase_type: implementation
components:
  - id: leaf-1
    name: Leaf 1
    interface_contract:
      inputs: [input]
      outputs: [output]
    constraint_surfaces: [surface]
    fillable: true
    fill_dependencies: []
  - id: leaf-2
    name: Leaf 2
    interface_contract:
      inputs: [input]
      outputs: [output]
    constraint_surfaces: [surface]
    fillable: true
    fill_dependencies: []
  - id: leaf-3
    name: Leaf 3
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


class TestWorkflowEngine:
    def test_single_pass_routing(self):
        result = WorkflowEngine(TempoConfig()).run(SINGLE_PASS_YAML)
        assert result.status == ResultStatus.SUCCESS
        assert result.data["routing"] == RoutingDecision.SINGLE_PASS.value

    def test_shape_fill_routing(self):
        result = WorkflowEngine(TempoConfig()).run(SHAPE_FILL_YAML)
        assert result.status == ResultStatus.SUCCESS
        assert result.data["routing"] == RoutingDecision.SHAPE_FILL.value

    def test_gate_rejection_returns_failure(self):
        bad_yaml = """
phase_id: ""
phase_type: research
components: []
output_schema:
  format: json
  required_fields: []
"""
        result = WorkflowEngine(TempoConfig()).run(bad_yaml)
        assert result.status == ResultStatus.FAILURE
        assert len(result.errors) > 0

    def test_parse_error_returns_failure(self):
        result = WorkflowEngine(TempoConfig()).run("not: valid: yaml: ::::")
        assert result.status == ResultStatus.FAILURE
        assert any("parse" in e.lower() or "yaml" in e.lower() for e in result.errors)

    def test_custom_threshold_via_config(self):
        config = TempoConfig()
        config.shape_fill_threshold = 1
        result = WorkflowEngine(config).run(SINGLE_PASS_YAML)
        assert result.status == ResultStatus.SUCCESS
        assert result.data["routing"] == RoutingDecision.SHAPE_FILL.value

    def test_result_has_routing_key(self):
        result = WorkflowEngine(TempoConfig()).run(SINGLE_PASS_YAML)
        assert "routing" in result.data
