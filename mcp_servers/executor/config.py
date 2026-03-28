"""TEMPO configuration — schema, defaults, and workspace-local loader.

Centralises all environment-detection constants and gate commands that were
previously hardcoded in environment.py and server.py source literals.

D-1  tomllib (stdlib, Python 3.11+): zero new runtime dependencies.
D-2  Deep merge: workspace config overrides individual keys only.
D-3  path_prefix_tiers={} in defaults: no org-specific paths in source.
D-4  resolve_tier_gates(): single lookup shared by _run_gate and validate_code.
"""

from __future__ import annotations

import copy
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError as e:
        raise ImportError(
            "Python < 3.11 requires 'tomli' package: pip install tomli"
        ) from e


@dataclass
class TierGates:
    """Command token lists for one tier. Each list is full subprocess argv
    excluding the path argument, which the gate runner appends at call time."""
    test:     list[str] = field(default_factory=list)
    lint:     list[str] = field(default_factory=list)
    security: list[str] = field(default_factory=list)


@dataclass
class GatesConfig:
    """Global default gates plus optional per-tier overrides.
    Resolution: per_tier[tier] if present, else default."""
    default:  TierGates = field(default_factory=TierGates)
    per_tier: dict[str, TierGates] = field(default_factory=dict)


@dataclass
class EnvironmentConfig:
    """Environment detection configuration.

    path_prefix_tiers: ordered prefix → tier-value-string map; first match wins.
    databricks_markers: content strings that signal a Databricks notebook.
    extra_extensions: workspace extension → tier-value-string overrides;
                      checked before _BUILTIN_EXTENSIONS in detect().
    """
    path_prefix_tiers:  dict[str, str] = field(default_factory=dict)
    databricks_markers: list[str]      = field(default_factory=list)
    extra_extensions:   dict[str, str] = field(default_factory=dict)


@dataclass
class TempoConfig:
    """Top-level TEMPO configuration container."""
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    gates:       GatesConfig       = field(default_factory=GatesConfig)
    shape_fill_threshold: int  = 3
    provider_registry:    dict = field(default_factory=dict)


_DEFAULTS = TempoConfig(
    environment=EnvironmentConfig(
        path_prefix_tiers={},
        databricks_markers=[
            "dbutils.",
            "spark.",
            "from pyspark",
            "import pyspark",
            "%sql",
            "%python",
            "%scala",
            "DeltaTable.",
            "display(",
            "spark.sql(",
            "spark.read.",
            "spark.createDataFrame",
        ],
        extra_extensions={},
    ),
    gates=GatesConfig(
        default=TierGates(
            test=     ["python", "-m", "pytest", "-x", "-q"],
            lint=     ["python", "-m", "ruff", "check"],
            security= ["python", "-m", "bandit", "-r", "-ll"],
        ),
        per_tier={
            "csharp": TierGates(
                test=     ["dotnet", "test", "--no-build"],
                lint=     ["dotnet", "format", "--verify-no-changes"],
                security= ["dotnet", "list", "package", "--vulnerable"],
            ),
            "typescript": TierGates(
                test=     ["npx", "jest", "--passWithNoTests"],
                lint=     ["npx", "eslint", "--max-warnings", "0"],
                security= ["npx", "audit-ci", "--moderate"],
            ),
            "javascript": TierGates(
                test=     ["npx", "jest", "--passWithNoTests"],
                lint=     ["npx", "eslint", "--max-warnings", "0"],
                security= ["npx", "audit-ci", "--moderate"],
            ),
        },
    ),
)


def load_config(workspace_root: str = ".") -> TempoConfig:
    """Load .tempo.config.toml from workspace_root; deep-merge over _DEFAULTS.
    Returns a fresh _DEFAULTS copy if the file does not exist."""
    config_path = Path(workspace_root) / ".tempo.config.toml"
    if not config_path.exists():
        return copy.deepcopy(_DEFAULTS)
    with config_path.open("rb") as fh:
        raw = tomllib.load(fh)
    return _merge(copy.deepcopy(_DEFAULTS), raw)


def _merge(base: TempoConfig, raw: dict) -> TempoConfig:
    """Deep-merge raw TOML dict into base. Per-key wins; unknown keys ignored."""
    env_raw = raw.get("environment", {})
    if "path_prefix_tiers" in env_raw:
        base.environment.path_prefix_tiers = dict(env_raw["path_prefix_tiers"])
    if "databricks_markers" in env_raw:
        base.environment.databricks_markers = list(env_raw["databricks_markers"])
    if "extra_extensions" in env_raw:
        base.environment.extra_extensions = dict(env_raw["extra_extensions"])

    gates_raw   = raw.get("gates", {})
    default_raw = gates_raw.get("default", {})
    if "test"     in default_raw:
        base.gates.default.test     = list(default_raw["test"])
    if "lint"     in default_raw:
        base.gates.default.lint     = list(default_raw["lint"])
    if "security" in default_raw:
        base.gates.default.security = list(default_raw["security"])

    for tier_name, tier_raw in gates_raw.get("per_tier", {}).items():
        base.gates.per_tier[tier_name] = TierGates(
            test=     list(tier_raw.get("test",     [])),
            lint=     list(tier_raw.get("lint",     [])),
            security= list(tier_raw.get("security", [])),
        )
    return base


def resolve_tier_gates(config: TempoConfig, tier_value: str) -> TierGates:
    """Return TierGates for tier_value, falling back to config.gates.default.
    Single source of truth for tier → toolchain resolution (D-4)."""
    return config.gates.per_tier.get(tier_value, config.gates.default)
