"""Benchmark harness tests — validate routing decisions and report generation."""
import json
from pathlib import Path

import pytest

from mcp_servers.benchmark.runner import BenchmarkRunner, STANDARD_CASES
from mcp_servers.benchmark.writer import BenchmarkWriter
from mcp_servers.executor.config import TempoConfig


class TestStubRoutingInvariant:
    """Verify routing decision matches threshold for standard cases."""
    
    @pytest.mark.benchmark
    def test_2_leaves_routes_single_pass(self) -> None:
        """With default threshold=3, 2 leaves should route to single_pass."""
        runner = BenchmarkRunner()
        rec = runner.run_case("t", leaf_count=2)
        assert rec.routing_decision == "single_pass"
        assert rec.result_status == "success"

    @pytest.mark.benchmark
    def test_3_leaves_routes_shape_fill(self) -> None:
        """With default threshold=3, 3 leaves should route to shape_fill."""
        runner = BenchmarkRunner()
        rec = runner.run_case("t", leaf_count=3)
        assert rec.routing_decision == "shape_fill"

    @pytest.mark.benchmark
    def test_5_leaves_routes_shape_fill(self) -> None:
        """With default threshold=3, 5 leaves should route to shape_fill."""
        runner = BenchmarkRunner()
        rec = runner.run_case("t", leaf_count=5)
        assert rec.routing_decision == "shape_fill"


class TestThresholdConfigurability:
    """Verify custom threshold configuration is respected."""
    
    @pytest.mark.benchmark
    def test_custom_threshold_4_respected(self) -> None:
        """With threshold=4, 3 leaves should single_pass; 4 leaves should shape_fill."""
        config = TempoConfig(shape_fill_threshold=4)
        runner = BenchmarkRunner(config=config)
        assert runner.run_case("t", leaf_count=3).routing_decision == "single_pass"
        assert runner.run_case("t", leaf_count=4).routing_decision == "shape_fill"


class TestReportOutput:
    """Verify report aggregation and JSON serialization."""
    
    @pytest.mark.benchmark
    def test_report_threshold_fires_correctly(self) -> None:
        """Verify all standard cases route correctly according to threshold."""
        runner = BenchmarkRunner()
        report = runner.run_suite()
        assert report.summary["threshold_fires_correctly"] is True
        assert report.summary["total_cases"] == len(STANDARD_CASES)
        assert all(r.latency_ms >= 0.0 for r in report.records)

    @pytest.mark.benchmark
    def test_latest_json_is_valid(self, tmp_path: Path) -> None:
        """Verify latest.json is valid JSON with correct summary."""
        runner = BenchmarkRunner()
        report = runner.run_suite()
        out = BenchmarkWriter.write_report(report, output_dir=tmp_path, quiet=True)
        assert out.exists()
        data = json.loads(out.read_text())
        assert "records" in data
        assert "summary" in data
        assert data["summary"]["threshold_fires_correctly"] is True
