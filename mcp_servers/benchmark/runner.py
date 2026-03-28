"""Benchmark runner — executes WorkflowEngine on synthetic skeletons.

Calls sync engine.run() directly. Measures latency and captures routing
decision for each case of varying leaf count.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

from mcp_servers.benchmark.schema import BenchmarkRecord, BenchmarkReport
from mcp_servers.executor.config import TempoConfig
from mcp_servers.workflow.engine import WorkflowEngine


def _build_skeleton_yaml(n: int) -> str:
    """Build a gate-passing ShapeSkeleton YAML with exactly n fillable leaf components.
    
    Args:
        n: Number of fillable (leaf) components to generate
        
    Returns:
        Valid YAML string representing a ShapeSkeleton with n leaves
    """
    components = ""
    for i in range(1, n + 1):
        components += f"""
  - id: "C{i}"
    name: "Component{i}"
    interface_contract:
      inputs: ["input_{i}"]
      outputs: ["output_{i}"]
    constraint_surfaces:
      - "Must produce output_{i}"
    fillable: true
    fill_dependencies: []
"""
    
    # Add one non-leaf non-fillable component to always satisfy components non-empty
    # when n==0, add a single non-fillable component so gate passes
    if n == 0:
        components = """
  - id: "C1"
    name: "Component1"
    interface_contract:
      inputs: ["input_1"]
      outputs: ["output_1"]
    constraint_surfaces:
      - "Must produce output_1"
    fillable: false
    fill_dependencies: []
"""
    
    return f"""phase_id: "P1"
phase_type: "implementation"
components:{components}
output_schema:
  format: "dataclass"
  required_fields: ["result"]
"""


STANDARD_CASES = [
    {"id": "case_0_leaves", "leaf_count": 0},
    {"id": "case_1_leaf",   "leaf_count": 1},
    {"id": "case_2_leaves", "leaf_count": 2},
    {"id": "case_3_leaves", "leaf_count": 3},
    {"id": "case_4_leaves", "leaf_count": 4},
    {"id": "case_5_leaves", "leaf_count": 5},
]


class BenchmarkRunner:
    """Executes benchmark test cases on the WorkflowEngine."""
    
    def __init__(self, config: TempoConfig | None = None) -> None:
        """Initialize runner with optional custom config.
        
        Args:
            config: TempoConfig instance; defaults to TempoConfig() if None
        """
        self._config = config or TempoConfig()
        self._engine = WorkflowEngine(config=self._config)

    def run_case(self, case_id: str, leaf_count: int) -> BenchmarkRecord:
        """Run a single benchmark case and capture routing result.
        
        Args:
            case_id: Unique test case identifier
            leaf_count: Number of fillable components to generate
            
        Returns:
            BenchmarkRecord with routing decision and latency
        """
        yaml_str = _build_skeleton_yaml(leaf_count)
        start = time.perf_counter()
        result = self._engine.run(yaml_str)
        latency_ms = (time.perf_counter() - start) * 1000
        
        if result.is_ok():
            routing = result.data["routing"]
            return BenchmarkRecord(
                test_case_id=case_id,
                leaf_count=leaf_count,
                threshold=self._config.shape_fill_threshold,
                routing_decision=routing,
                latency_ms=latency_ms,
                result_status="success",
            )
        else:
            return BenchmarkRecord(
                test_case_id=case_id,
                leaf_count=leaf_count,
                threshold=self._config.shape_fill_threshold,
                routing_decision="",
                latency_ms=latency_ms,
                result_status="failure",
                error_summary="; ".join(result.errors or []),
            )

    def run_suite(self, cases: list[dict] | None = None) -> BenchmarkReport:
        """Run full benchmark suite across all cases and return aggregated report.
        
        Args:
            cases: List of case dicts with 'id' and 'leaf_count' keys;
                   defaults to STANDARD_CASES
                   
        Returns:
            BenchmarkReport with all records and computed summary
        """
        cases = cases or STANDARD_CASES
        records = [self.run_case(c["id"], c["leaf_count"]) for c in cases]
        report = BenchmarkReport(
            records=records,
            run_timestamp=datetime.now(timezone.utc).isoformat(),
            shape_fill_threshold=self._config.shape_fill_threshold,
        )
        report.compute_summary()
        return report
