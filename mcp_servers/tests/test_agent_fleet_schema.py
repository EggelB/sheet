"""Test suite for agent fleet front-matter schema and behavioral contract sections.

Validates all 6 .agent.md files against the oracle table defined in the L5 pure signal brief.
Tests are static-analysis only — no network calls, no server instantiation.
"""

import pytest
import yaml
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

AGENTS_DIR = Path(__file__).parents[2] / ".github" / "agents"

ORACLE = {
    "strategic-collaborator.agent.md": {"tier": "opus", "workflow_role": "none"},
    "tempo-planner.agent.md": {"tier": "sonnet", "workflow_role": "shaper"},
    "tempo-synthesizer.agent.md": {"tier": "opus", "workflow_role": "synthesizer"},
    "quick-developer.agent.md": {"tier": "haiku", "workflow_role": "filler"},
    "tempo-reviewer.agent.md": {"tier": "opus", "workflow_role": "reviewer"},
    "deep-researcher.agent.md": {"tier": "sonnet", "workflow_role": "researcher"},
}

STUB_MARKERS = frozenset({
    "[STUB]", "[TODO]", "[PLACEHOLDER]", "[TBD]",
    "[FILL IN]", "[FILL_IN]", "[OMITTED]", "[INCOMPLETE]",
})


def _parse_frontmatter(path: Path) -> dict:
    """Extract YAML front-matter between leading --- delimiters."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def _read(filename: str) -> str:
    return (AGENTS_DIR / filename).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests — file existence
# ---------------------------------------------------------------------------

class TestFileExistence:
    def test_all_six_agent_files_exist(self):
        for filename in ORACLE:
            assert (AGENTS_DIR / filename).exists(), f"Missing: {filename}"

    def test_no_atlas_agent_files_exist(self):
        for stale in ("atlas-planner.agent.md", "atlas-synthesizer.agent.md", "atlas-reviewer.agent.md"):
            assert not (AGENTS_DIR / stale).exists(), f"Stale file still present: {stale}"


# ---------------------------------------------------------------------------
# Tests — front-matter schema
# ---------------------------------------------------------------------------

class TestFrontMatterFields:
    @pytest.mark.parametrize("filename", list(ORACLE))
    def test_tier_field_present(self, filename):
        fm = _parse_frontmatter(AGENTS_DIR / filename)
        assert "tier" in fm, f"{filename}: missing 'tier' field"

    @pytest.mark.parametrize("filename", list(ORACLE))
    def test_workflow_role_field_present(self, filename):
        fm = _parse_frontmatter(AGENTS_DIR / filename)
        assert "workflow_role" in fm, f"{filename}: missing 'workflow_role' field"


# ---------------------------------------------------------------------------
# Tests — oracle values
# ---------------------------------------------------------------------------

class TestOracleValues:
    @pytest.mark.parametrize("filename,expected", [
        (f, v) for f, v in ORACLE.items()
    ])
    def test_tier_matches_oracle(self, filename, expected):
        fm = _parse_frontmatter(AGENTS_DIR / filename)
        assert fm.get("tier") == expected["tier"], (
            f"{filename}: tier={fm.get('tier')!r}, expected {expected['tier']!r}"
        )

    @pytest.mark.parametrize("filename,expected", [
        (f, v) for f, v in ORACLE.items()
    ])
    def test_workflow_role_matches_oracle(self, filename, expected):
        fm = _parse_frontmatter(AGENTS_DIR / filename)
        assert fm.get("workflow_role") == expected["workflow_role"], (
            f"{filename}: workflow_role={fm.get('workflow_role')!r}, expected {expected['workflow_role']!r}"
        )


# ---------------------------------------------------------------------------
# Tests — behavioral contract sections
# ---------------------------------------------------------------------------

class TestBehavioralContracts:
    def test_shape_protocol_contract_in_tempo_planner_only(self):
        matches = [f for f in ORACLE if "## Shape Protocol Contract" in _read(f)]
        assert matches == ["tempo-planner.agent.md"], (
            f"Shape Protocol Contract found in wrong files: {matches}"
        )

    def test_fill_protocol_contract_in_quick_developer_only(self):
        matches = [f for f in ORACLE if "## Fill Protocol Contract" in _read(f)]
        assert matches == ["quick-developer.agent.md"], (
            f"Fill Protocol Contract found in wrong files: {matches}"
        )


# ---------------------------------------------------------------------------
# Tests — STUB_MARKERS completeness
# ---------------------------------------------------------------------------

class TestStubMarkers:
    @pytest.mark.parametrize("marker", sorted(STUB_MARKERS))
    def test_stub_marker_in_fill_protocol(self, marker):
        content = _read("quick-developer.agent.md")
        assert marker in content, (
            f"quick-developer.agent.md Fill Protocol Contract missing stub marker: {marker!r}"
        )
