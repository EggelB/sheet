"""Shape skeleton types for the TEMPO Shape→Fill workflow engine.

Defines the typed YAML schema parsed from agent-produced ShapeSkeleton output.
All types are dataclasses for easy JSON serialization.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import yaml


class PhaseType(Enum):
    RESEARCH = "research"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"


class RoutingDecision(Enum):
    SINGLE_PASS = "single_pass"
    SHAPE_FILL = "shape_fill"


@dataclass
class InterfaceContract:
    inputs: list[str]
    outputs: list[str]


@dataclass
class OutputSchema:
    format: str
    required_fields: list[str]


@dataclass
class ShapeComponent:
    id: str
    name: str
    interface_contract: InterfaceContract
    constraint_surfaces: list[str]
    fillable: bool
    fill_dependencies: list[str]

    def is_leaf(self) -> bool:
        """True iff fillable with no fill_dependencies (parallel-eligible)."""
        return self.fillable and len(self.fill_dependencies) == 0


@dataclass
class ShapeSkeleton:
    phase_id: str
    phase_type: str
    components: list[ShapeComponent]
    output_schema: OutputSchema

    @classmethod
    def from_yaml(cls, text: str) -> ShapeSkeleton:
        """Parse a YAML string into a ShapeSkeleton.

        Raises yaml.YAMLError on invalid YAML.
        Missing optional keys default to safe empty values.
        """
        raw = yaml.safe_load(text)
        if not isinstance(raw, dict):
            raise ValueError("ShapeSkeleton YAML must be a mapping at the top level")

        components: list[ShapeComponent] = []
        for c in raw.get("components", []):
            ic_raw = c.get("interface_contract", {})
            components.append(ShapeComponent(
                id=c.get("id", ""),
                name=c.get("name", ""),
                interface_contract=InterfaceContract(
                    inputs=list(ic_raw.get("inputs", [])),
                    outputs=list(ic_raw.get("outputs", [])),
                ),
                constraint_surfaces=list(c.get("constraint_surfaces", [])),
                fillable=bool(c.get("fillable", False)),
                fill_dependencies=list(c.get("fill_dependencies", [])),
            ))

        os_raw = raw.get("output_schema", {})
        output_schema = OutputSchema(
            format=str(os_raw.get("format", "")),
            required_fields=list(os_raw.get("required_fields", [])),
        )

        return cls(
            phase_id=str(raw.get("phase_id", "")),
            phase_type=str(raw.get("phase_type", "")),
            components=components,
            output_schema=output_schema,
        )

    def leaf_count(self) -> int:
        """Return the number of independently fillable leaf components."""
        return sum(1 for c in self.components if c.is_leaf())
