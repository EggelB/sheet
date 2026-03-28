"""Benchmark record schema for routing decision validation.

Stdlib imports only. Captures leaf count, threshold, routing decision,
latency, and result status for each test case.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BenchmarkRecord:
    """Single benchmark run result."""
    
    test_case_id: str
    leaf_count: int
    threshold: int
    routing_decision: str          # "single_pass" or "shape_fill"
    latency_ms: float
    result_status: str             # "success" or "failure"
    error_summary: Optional[str] = None


@dataclass
class BenchmarkReport:
    """Aggregated benchmark report with summary statistics."""
    
    records: list[BenchmarkRecord]
    run_timestamp: str
    shape_fill_threshold: int
    summary: dict = field(default_factory=dict)

    def compute_summary(self) -> None:
        """Compute summary statistics: total cases, routing counts, threshold correctness."""
        total = len(self.records)
        single = sum(1 for r in self.records if r.routing_decision == "single_pass")
        shape = sum(1 for r in self.records if r.routing_decision == "shape_fill")
        
        # Verify threshold fires correctly for all successful cases
        fires_correctly = all(
            (r.routing_decision == "shape_fill") == (r.leaf_count >= r.threshold)
            for r in self.records
            if r.result_status == "success"
        )
        
        self.summary = {
            "total_cases": total,
            "single_pass_count": single,
            "shape_fill_count": shape,
            "threshold_fires_correctly": fires_correctly,
        }
