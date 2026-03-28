"""Tests for Phase 2 EnvironmentTier extensions — 6 tests."""

from mcp_servers.executor.config import TempoConfig, EnvironmentConfig
from mcp_servers.executor.environment import EnvironmentDetector, EnvironmentTier


class TestBuiltinExtensions:
    def test_cs_extension_detects_csharp(self):
        result = EnvironmentDetector(config=TempoConfig()).detect(file_path="src/MyService.cs")
        assert result.tier == EnvironmentTier.CSHARP
        assert result.confidence == 1.0

    def test_ts_extension_detects_typescript(self):
        result = EnvironmentDetector(config=TempoConfig()).detect(file_path="frontend/app.ts")
        assert result.tier == EnvironmentTier.TYPESCRIPT

    def test_js_extension_detects_javascript(self):
        result = EnvironmentDetector(config=TempoConfig()).detect(file_path="scripts/build.js")
        assert result.tier == EnvironmentTier.JAVASCRIPT

    def test_java_extension_detects_generic(self):
        result = EnvironmentDetector(config=TempoConfig()).detect(file_path="src/Main.java")
        assert result.tier == EnvironmentTier.GENERIC


class TestExtraExtensions:
    def test_extra_extension_adds_new_mapping(self):
        config = TempoConfig(
            environment=EnvironmentConfig(extra_extensions={".sol": "generic"})
        )
        result = EnvironmentDetector(config=config).detect(file_path="contracts/Token.sol")
        assert result.tier == EnvironmentTier.GENERIC

    def test_extra_extension_overrides_builtin(self):
        config = TempoConfig(
            environment=EnvironmentConfig(extra_extensions={".js": "typescript"})
        )
        result = EnvironmentDetector(config=config).detect(file_path="lib/util.js")
        assert result.tier == EnvironmentTier.TYPESCRIPT
