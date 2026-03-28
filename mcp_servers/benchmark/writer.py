"""Benchmark report writer — stdout table and JSON output."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from mcp_servers.benchmark.schema import BenchmarkReport


class BenchmarkWriter:
    """Writes benchmark reports to stdout and disk."""
    
    @staticmethod
    def write_report(
        report: BenchmarkReport,
        output_dir: Path | str = ".",
        quiet: bool = False,
    ) -> Path:
        """Write benchmark report as latest.json; optionally print table to stdout.
        
        Args:
            report: BenchmarkReport instance
            output_dir: Directory to write latest.json to; defaults to current directory
            quiet: If True, suppress stdout table; defaults to False
            
        Returns:
            Path to written latest.json file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / "latest.json"
        out_path.write_text(json.dumps(asdict(report), indent=2))

        if not quiet:
            print(f"\n{'Case ID':<22} {'Leaves':>6} {'Threshold':>9} {'Routing':<12} {'Latency(ms)':>11} {'Status':<8}")
            print("-" * 75)
            for r in report.records:
                print(f"{r.test_case_id:<22} {r.leaf_count:>6} {r.threshold:>9} {r.routing_decision:<12} {r.latency_ms:>11.3f} {r.result_status:<8}")
            print("-" * 75)
            s = report.summary
            print(f"Total: {s['total_cases']} | Single-pass: {s['single_pass_count']} | Shape-fill: {s['shape_fill_count']} | Threshold fires correctly: {s['threshold_fires_correctly']}")

        return out_path
