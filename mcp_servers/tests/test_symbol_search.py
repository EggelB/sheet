"""Tests for find_symbol_usages language branching — 5 tests.

F-4 applied: sync wrappers used; no asyncio in test bodies.
"""

import pytest
from mcp_servers.executor.server import ExecutorServer


@pytest.fixture
def server():
    return ExecutorServer()


class TestFindSymbolPython:
    def test_find_symbol_python_uses_ast(self, tmp_path, server):
        (tmp_path / "mod.py").write_text("def my_func():\n    pass\n", encoding="utf-8")
        server.workspace_root = str(tmp_path)
        result = server.find_symbol_usages("my_func", language="python")
        assert result.data["scan_method"] == "ast"
        assert result.data["usage_count"] >= 1

    def test_find_symbol_defaults_to_python(self, tmp_path, server):
        (tmp_path / "mod.py").write_text("def legacy_func():\n    pass\n", encoding="utf-8")
        server.workspace_root = str(tmp_path)
        result = server.find_symbol_usages("legacy_func")
        assert result.data["scan_method"] == "ast"


class TestFindSymbolNonPython:
    def test_find_symbol_typescript_uses_regex(self, tmp_path, server):
        (tmp_path / "app.ts").write_text(
            "export function myService(): void {}\nconst x = myService();\n",
            encoding="utf-8",
        )
        server.workspace_root = str(tmp_path)
        result = server.find_symbol_usages("myService", language="typescript")
        assert result.data["scan_method"] == "regex"
        assert result.data["usage_count"] == 2

    def test_find_symbol_csharp_whole_word_only(self, tmp_path, server):
        (tmp_path / "Services.cs").write_text(
            "public class MyClass {}\npublic class MyClassFactory {}\n",
            encoding="utf-8",
        )
        server.workspace_root = str(tmp_path)
        result = server.find_symbol_usages("MyClass", language="csharp")
        assert result.data["usage_count"] == 1
        assert "MyClassFactory" not in result.data["usages"][0]["context_line"]


class TestFindSymbolUnsupported:
    def test_unsupported_language_returns_fail(self, server):
        result = server.find_symbol_usages("SomeSymbol", language="cobol")
        assert result.status.value == "failure"
        assert any("cobol" in e for e in result.errors)
        assert any("Supported" in e for e in result.errors)
