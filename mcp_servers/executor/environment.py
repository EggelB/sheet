"""Environment detection for tempo.executor.

Determines validation tier from file path, content markers, and optional
caller override.  Priority: override > extension > path_prefix > content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from mcp_servers.executor.config import TempoConfig, load_config


class EnvironmentTier(str, Enum):
    """Validation tier assigned by EnvironmentDetector.

    Tiers:
        LOCAL_PYTHON    (1) — full execution: py_compile, pytest, ruff.
        DATABRICKS_NB   (2) — static analysis ONLY. Never execute.
        DATABRICKS_PIPE (2) — static analysis ONLY. Never execute.
        SQL_DDL         (3) — structural review: sqlfluff, schema extraction.
        RELEASE_SCRIPT  (3) — structural review: release script analysis.
        UNKNOWN             — advisory only; no execution.
        CSHARP          (4) — C#/F# source; default gates use dotnet SDK.
        TYPESCRIPT      (4) — TypeScript source; default gates use npx.
        JAVASCRIPT      (4) — JavaScript source; default gates use npx.
        GENERIC             — identified non-Python; toolchain unknown.
    """

    LOCAL_PYTHON = "local_python"
    DATABRICKS_NB = "databricks_notebook"
    DATABRICKS_PIPE = "databricks_pipeline"
    SQL_DDL = "sql_ddl"
    RELEASE_SCRIPT = "release_script"
    UNKNOWN = "unknown"
    CSHARP = "csharp"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GENERIC = "generic"


@dataclass
class DetectionResult:
    """Output of EnvironmentDetector.detect()."""

    tier: EnvironmentTier
    confidence: float           # 0.0–1.0; <1.0 when signals conflict
    signals: list[str] = field(default_factory=list)  # evidence trail
    override_used: bool = False


class EnvironmentDetector:
    """Determine the correct validation tier for a given file.

    Priority chain (strict order):
        1. override  — explicit caller instruction, confidence=1.0
        2. extension — .sql → SQL_DDL; .ipynb → DATABRICKS_NB
        3. path_prefix — first match in PATH_PREFIX_TIERS wins
        4. content_markers — any DATABRICKS_MARKERS hit → DATABRICKS_NB
        5. fallback — LOCAL_PYTHON, confidence=0.5
    """

    _BUILTIN_EXTENSIONS: dict[str, str] = {
        ".cs": "csharp", ".fs": "csharp", ".fsx": "csharp",
        ".vb": "csharp", ".csproj": "csharp", ".fsproj": "csharp", ".sln": "csharp",
        ".ts": "typescript", ".tsx": "typescript",
        ".js": "javascript", ".jsx": "javascript",
        ".mjs": "javascript", ".cjs": "javascript",
        ".java": "generic", ".kt": "generic", ".kts": "generic",
        ".go": "generic", ".rs": "generic", ".rb": "generic", ".swift": "generic",
    }

    def __init__(self, config: TempoConfig | None = None) -> None:
        self.config: TempoConfig = config if config is not None else load_config(".")

    def detect(
        self,
        file_path: str | Path | None = None,
        content: str | None = None,
        override: str | None = None,
    ) -> DetectionResult:
        """Detect the appropriate validation tier."""
        # 1. Explicit override
        if override:
            try:
                tier = EnvironmentTier(override)
            except ValueError:
                tier = EnvironmentTier.UNKNOWN
            return DetectionResult(
                tier=tier,
                confidence=1.0,
                signals=[f"override:{override}"],
                override_used=True,
            )

        signals: list[str] = []

        # 2. Extension check
        if file_path is not None:
            normalised = str(file_path).replace("\\", "/")
            ext = Path(normalised).suffix.lower()
            if ext == ".sql":
                signals.append("extension:.sql")
                return DetectionResult(
                    tier=EnvironmentTier.SQL_DDL,
                    confidence=1.0,
                    signals=signals,
                )
            if ext == ".ipynb":
                signals.append("extension:.ipynb")
                return DetectionResult(
                    tier=EnvironmentTier.DATABRICKS_NB,
                    confidence=1.0,
                    signals=signals,
                )

            # 2b. Built-in + workspace extension → named tier
            # extra_extensions checked first so workspace overrides win.
            tier_str = (
                self.config.environment.extra_extensions.get(ext)
                or self._BUILTIN_EXTENSIONS.get(ext)
            )
            if tier_str:
                try:
                    tier = EnvironmentTier(tier_str)
                    signals.append(f"extension:{ext}")
                    return DetectionResult(tier=tier, confidence=1.0, signals=signals)
                except ValueError:
                    signals.append(f"extension_unknown_tier:{tier_str}")

            # 3. Path prefix
            for prefix, tier_str in self.config.environment.path_prefix_tiers.items():
                if normalised.startswith(prefix) or ("/" + prefix) in normalised:
                    signals.append(f"path_prefix:{prefix}")
                    return DetectionResult(
                        tier=EnvironmentTier(tier_str),
                        confidence=1.0,
                        signals=signals,
                    )

        # 4. Content markers
        if content:
            matched = [m for m in self.config.environment.databricks_markers if m in content]
            if matched:
                signals.extend(f"content_marker:{m}" for m in matched[:3])
                return DetectionResult(
                    tier=EnvironmentTier.DATABRICKS_NB,
                    confidence=0.9,
                    signals=signals,
                )

        # 5. Fallback
        signals.append("fallback:no_signals")
        return DetectionResult(
            tier=EnvironmentTier.LOCAL_PYTHON,
            confidence=0.5,
            signals=signals,
        )
