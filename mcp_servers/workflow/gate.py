"""Pre-fill completeness gate for the TEMPO Shape→Fill workflow engine.

Validates a ShapeSkeleton before any fill invocation. Four invariants enforced
in collection mode — all violations reported before returning.
"""
from __future__ import annotations

from mcp_servers.utils.results import Result
from mcp_servers.workflow.shape import ShapeSkeleton


class PreFillGate:
    """Synchronous gate that validates a ShapeSkeleton before fill dispatch.

    All four invariants are checked without short-circuit. A single fail call
    returns the full violation list.
    """

    @staticmethod
    def validate(skeleton: ShapeSkeleton) -> Result:
        """Validate skeleton completeness. Returns Result.ok(skeleton) or Result.fail(violations)."""
        violations: list[str] = []

        # Invariant 1: phase_id must be non-empty
        if not skeleton.phase_id:
            violations.append("phase_id is empty")

        # Invariant 2: components list must be non-empty
        if not skeleton.components:
            violations.append("components list is empty")

        # Invariant 3: per-component checks
        for c in skeleton.components:
            if not c.interface_contract.inputs or not c.interface_contract.outputs:
                violations.append(
                    f"component '{c.id}': interface_contract inputs and outputs must both be non-empty"
                )
            if not c.constraint_surfaces:
                violations.append(
                    f"component '{c.id}': constraint_surfaces must be non-empty"
                )

        # Invariant 4: output_schema.required_fields must be non-empty
        if not skeleton.output_schema.required_fields:
            violations.append("output_schema.required_fields is empty")

        if violations:
            return Result.fail(violations)
        return Result.ok(skeleton)
