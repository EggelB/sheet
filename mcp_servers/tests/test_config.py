"""Tests for mcp_servers/executor/config.py — 6 tests."""

from mcp_servers.executor.config import (
    TempoConfig,
    EnvironmentConfig,
    GatesConfig,
    TierGates,
    load_config,
    resolve_tier_gates,
    _DEFAULTS,
)
from mcp_servers.executor.environment import EnvironmentDetector, EnvironmentTier


class TestLoadConfig:
    def test_no_file_returns_defaults(self, tmp_path):
        config = load_config(str(tmp_path))
        assert config.gates.default.lint == _DEFAULTS.gates.default.lint
        assert config.environment.databricks_markers == _DEFAULTS.environment.databricks_markers
        assert config is not _DEFAULTS

    def test_workspace_overrides_single_key(self, tmp_path):
        (tmp_path / ".tempo.config.toml").write_text(
            '[gates.default]\nlint = ["npx", "eslint"]\n', encoding="utf-8"
        )
        config = load_config(str(tmp_path))
        assert config.gates.default.lint == ["npx", "eslint"]
        assert config.gates.default.test == _DEFAULTS.gates.default.test
        assert config.gates.default.security == _DEFAULTS.gates.default.security

    def test_unknown_keys_ignored(self, tmp_path):
        (tmp_path / ".tempo.config.toml").write_text(
            '[totally_unknown]\nkey = "value"\n', encoding="utf-8"
        )
        config = load_config(str(tmp_path))  # must not raise
        assert config.gates.default.lint == _DEFAULTS.gates.default.lint


class TestEnvironmentDetectorConfig:
    def test_detector_respects_config_path_prefixes(self):
        config = TempoConfig(
            environment=EnvironmentConfig(
                path_prefix_tiers={"my_org/": "sql_ddl"},
                databricks_markers=[],
            ),
        )
        result = EnvironmentDetector(config=config).detect(file_path="my_org/schema.py")
        assert result.tier == EnvironmentTier.SQL_DDL
        assert result.confidence == 1.0


class TestResolveTierGates:
    def test_returns_per_tier_when_present(self):
        config = TempoConfig(
            gates=GatesConfig(
                default=TierGates(lint=["python", "-m", "ruff", "check"]),
                per_tier={"csharp": TierGates(lint=["dotnet", "format"])},
            )
        )
        assert resolve_tier_gates(config, "csharp").lint == ["dotnet", "format"]

    def test_falls_back_to_default(self):
        config = TempoConfig(
            gates=GatesConfig(
                default=TierGates(lint=["python", "-m", "ruff", "check"]),
                per_tier={},
            )
        )
        assert resolve_tier_gates(config, "csharp").lint == ["python", "-m", "ruff", "check"]


class TestTempoConfigNewFields:
    def test_shape_fill_threshold_default(self):
        config = TempoConfig()
        assert config.shape_fill_threshold == 3

    def test_provider_registry_default(self):
        config = TempoConfig()
        assert config.provider_registry == {}
        # Verify that two instances don't share the same dict object
        config2 = TempoConfig()
        assert config.provider_registry is not config2.provider_registry
