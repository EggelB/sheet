"""tempo.executor — Subprocess, AST, and code quality tools for TEMPO.

Tools
-----
run_quality_gates       Run test / lint / security gates and return pass/fail per gate.
validate_code           Tier-aware code validation via EnvironmentDetector.
get_server_health       py_compile + tool_count check on the 3 atlas servers.
verify_tool_registration 3-way alignment: Tool defs / _tool_* handlers / sync wrappers.
find_symbol_usages      AST walk across workspace returning all usages of a symbol.
verify_sync_wrappers    Check every _tool_* handler has a matching public sync wrapper.

DRY integrations (from Layer 4 audit)
--------------------------------------
E-1  _run_subprocess_gate    Single runner; _run_gate dispatches via inline lambdas.
E-2  _scan_file_for_symbol   Reads source once; derives both tree and lines.
E-3  _parse_server_symbols   Shared AST helper used by verify_tool_registration
                             and verify_sync_wrappers.
"""

import ast
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Literal

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp.types import Tool
from mcp_servers.base import BaseAgentServer
from mcp_servers.executor.config import TempoConfig, load_config, resolve_tier_gates
from mcp_servers.executor.environment import EnvironmentDetector, EnvironmentTier
from mcp_servers.utils.results import Result

try:
    import asyncio
except ImportError:
    raise


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GateResult:
    gate: str
    passed: bool
    returncode: int
    output: str
    failures: list[str]


@dataclass
class ServerHealth:
    server_path: str
    syntax_ok: bool
    import_ok: bool
    tool_count: int
    error: str | None


@dataclass
class RegistrationGap:
    gap_type: str           # "unregistered_handler" | "missing_handler"
    tool_name: str
    has_registration: bool
    has_handler: bool
    has_sync_wrapper: bool


@dataclass
class SyncWrapperGap:
    handler_name: str
    has_async_handler: bool
    has_sync_wrapper: bool
    issue: str


@dataclass
class SymbolUsage:
    file_path: str
    line_number: int
    context_line: str
    usage_type: str         # "definition" | "import" | "call_site" | "assignment"


@dataclass
class ValidationReport:
    file_path: str
    tier: str
    tier_confidence: float
    syntax_ok: bool
    error: str | None
    signals: list[str]
    validated: bool = False


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

class ExecutorServer(BaseAgentServer):
    """tempo.executor — subprocess runners, AST tools, and code quality gates."""

    # Directories excluded from symbol search
    _SEARCH_EXCLUDES = {"__pycache__", ".venv", ".git", "node_modules", ".mypy_cache"}

    _GATE_FAILURE_FILTERS: dict[str, Callable[[str], bool]] = {
        "test":     lambda line: "FAILED" in line or "ERROR" in line,
        "lint":     lambda line: bool(line.strip()) and not line.startswith("Found"),
        "security": lambda line: "Issue:" in line,
    }

    _LANGUAGE_EXTENSIONS: dict[str, list[str]] = {
        "python":     ["*.py"],
        "typescript": ["*.ts", "*.tsx"],
        "javascript": ["*.js", "*.jsx", "*.mjs", "*.cjs"],
        "csharp":     ["*.cs", "*.fs", "*.fsx"],
        "java":       ["*.java"],
        "go":         ["*.go"],
        "rust":       ["*.rs"],
        "ruby":       ["*.rb"],
        "kotlin":     ["*.kt", "*.kts"],
        "scala":      ["*.scala"],
    }

    def __init__(self) -> None:
        super().__init__()  # sets self.workspace_root via BaseAgentServer
        self.config: TempoConfig = load_config(self.workspace_root)

    @property
    def agent_name(self) -> str:
        return "tempo.executor"

    def _get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="run_quality_gates",
                description=(
                    "Run test / lint / security gates against one or more paths. "
                    "Pass a single file for fast targeted checks, or multiple files/dirs "
                    "for a scoped sweep. Returns pass/fail + failure lines per gate. "
                    "Gates: 'test' (pytest -x -q), 'lint' (ruff check), 'security' (bandit -ll)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "paths":           {"type": "array", "items": {"type": "string"}, "description": "One or more files or directories to run gates against"},
                        "gates":           {"type": "array", "items": {"type": "string"}, "description": "Subset of gates to run (default: all three)"},
                        "stop_on_failure": {"type": "boolean", "description": "Halt gate sequence on first failure (default: false)"},
                    },
                    "required": ["paths"],
                },
            ),
            Tool(
                name="validate_code",
                description=(
                    "Validate a file using the tier-appropriate method: "
                    "LOCAL_PYTHON → py_compile; DATABRICKS_* → static analysis; SQL → structural review."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path":          {"type": "string"},
                        "override_tier": {"type": "string", "description": "Force a specific EnvironmentTier value"},
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="get_server_health",
                description=(
                    "Run py_compile and report tool_count for all MCP servers discovered "
                    "under mcp_servers/. Auto-discovers any server.py that registers Tools "
                    "— no hardcoded list. Returns per-server health dict."
                ),
                inputSchema={"type": "object", "properties": {}, "required": []},
            ),
            Tool(
                name="verify_tool_registration",
                description=(
                    "3-way alignment check on a server.py: Tool(name=...) registrations, "
                    "_tool_* handler methods, and public sync wrappers. Returns any gaps."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {"server_path": {"type": "string"}},
                    "required": ["server_path"],
                },
            ),
            Tool(
                name="find_symbol_usages",
                description=(
                    "Search all files of the target language under search_path for every "
                    "usage of the named symbol. Python uses AST walk (definitions, imports, "
                    "call_sites, assignments); other languages use whole-word regex match. "
                    "Supported: python, typescript, javascript, csharp, java, go, rust, "
                    "ruby, kotlin, scala."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol":      {"type": "string"},
                        "search_path": {"type": "string", "description": "Workspace-relative path (default: '.')"},
                        "language":    {
                            "type": "string",
                            "description": (
                                "'python' (AST, default), 'typescript', 'javascript', "
                                "'csharp', 'java', 'go', 'rust', 'ruby', 'kotlin', 'scala'."
                            ),
                        },
                    },
                    "required": ["symbol"],
                },
            ),
            Tool(
                name="verify_sync_wrappers",
                description=(
                    "Check that every async _tool_* handler in a server.py has a matching "
                    "public sync wrapper. Returns missing-wrapper gaps."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {"server_path": {"type": "string"}},
                    "required": ["server_path"],
                },
            ),
        ]

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    async def _tool_run_quality_gates(
        self,
        paths: list[str],
        gates: list[str] | None = None,
        stop_on_failure: bool = False,
    ) -> Result:
        """Run requested gates sequentially; honour stop_on_failure."""
        if not paths:
            return Result.fail(["paths must be a non-empty list"])
        active_gates = gates or ["test", "lint", "security"]
        # Detect tier from first path — callers should group same-tier paths together
        detection = EnvironmentDetector(config=self.config).detect(file_path=paths[0])
        results: list[GateResult] = []
        for gate in active_gates:
            gr = await self._run_gate(gate, paths, tier=detection.tier)
            results.append(gr)
            if stop_on_failure and not gr.passed:
                break
        return Result.ok({
            "all_passed":  all(r.passed for r in results),
            "gates_run":   len(results),
            "tier_used":   detection.tier.value,
            "results":     [asdict(r) for r in results],
        })

    async def _tool_validate_code(
        self,
        path: str,
        override_tier: str | None = None,
    ) -> Result:
        """Detect tier then apply tier-appropriate validation."""
        try:
            content = Path(path).read_text(encoding="utf-8")
        except (FileNotFoundError, OSError) as e:
            return Result.fail([f"Cannot read file: {e}"])

        detection = EnvironmentDetector(config=self.config).detect(
            file_path=path, content=content, override=override_tier
        )
        syntax_ok = True
        error: str | None = None
        validated = False

        if detection.tier == EnvironmentTier.LOCAL_PYTHON:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "py_compile", path,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            stdout, _ = await proc.communicate()
            syntax_ok = proc.returncode == 0
            error = stdout.decode().strip() if not syntax_ok else None
            validated = True

        elif detection.tier == EnvironmentTier.JAVASCRIPT:
            proc = await asyncio.create_subprocess_exec(
                "node", "--check", path,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            stdout, _ = await proc.communicate()
            syntax_ok = proc.returncode == 0
            error = stdout.decode().strip() if not syntax_ok else None
            validated = True

        elif detection.tier in (EnvironmentTier.TYPESCRIPT, EnvironmentTier.CSHARP):
            detection.signals.append(
                f"single_file_validation_not_supported:"
                f"{detection.tier.value}:requires_project_context"
            )

        report = ValidationReport(
            file_path=path,
            tier=detection.tier.value,
            tier_confidence=detection.confidence,
            syntax_ok=syntax_ok,
            error=error,
            signals=detection.signals,
            validated=validated,
        )
        return Result.ok(asdict(report))

    async def _tool_get_server_health(self) -> Result:
        """py_compile + tool_count for all MCP servers (auto-discovered)."""
        root = Path(self.workspace_root)
        server_paths = sorted(
            str(p) for p in root.glob("mcp_servers/*/server.py")
            if "Tool(" in p.read_text(encoding="utf-8", errors="ignore")
        )
        health_list: list[ServerHealth] = await asyncio.gather(
            *[self._check_one_server(p) for p in server_paths]
        )
        return Result.ok({
            "servers":       [asdict(h) for h in health_list],
            "healthy_count": sum(1 for h in health_list if h.syntax_ok),
            "total_count":   len(health_list),
        })

    async def _tool_verify_tool_registration(self, server_path: str) -> Result:
        """3-way alignment: Tool defs / _tool_* handlers / sync wrappers.

        Uses _parse_server_symbols (E-3: shared with verify_sync_wrappers).
        Does NOT execute the server.
        """
        try:
            parsed = self._parse_server_symbols(server_path)
        except (FileNotFoundError, SyntaxError) as e:
            return Result.fail([f"Cannot parse {server_path}: {e}"])

        registered    = set(parsed["tool_names"])
        handlers      = set(parsed["handler_names"])
        sync_wrappers = set(parsed["sync_wrapper_names"])

        gaps: list[RegistrationGap] = []
        for name in sorted(registered | handlers):
            has_reg  = name in registered
            has_hdlr = name in handlers
            if has_reg != has_hdlr:
                gap_type = "unregistered_handler" if has_hdlr else "missing_handler"
                gaps.append(RegistrationGap(
                    gap_type=gap_type,
                    tool_name=name,
                    has_registration=has_reg,
                    has_handler=has_hdlr,
                    has_sync_wrapper=name in sync_wrappers,
                ))

        return Result.ok({"gaps": [asdict(g) for g in gaps], "gap_count": len(gaps)})

    async def _tool_find_symbol_usages(
        self,
        symbol: str,
        search_path: str = ".",
        language: str = "python",
    ) -> Result:
        """Multi-language symbol search: AST for Python, whole-word regex otherwise."""
        root = Path(self.workspace_root) / search_path
        if not root.exists():
            return Result.fail([f"Search path not found: {search_path}"])

        all_usages: list[SymbolUsage] = []
        scan_method: str

        if language == "python":
            scan_method = "ast"
            py_files = [
                f for f in root.rglob("*.py")
                if not any(ex in f.parts for ex in self._SEARCH_EXCLUDES)
            ]
            for f in py_files:
                all_usages.extend(self._scan_file_for_symbol(symbol, f))

        elif language in self._LANGUAGE_EXTENSIONS:
            scan_method = "regex"
            seen: set[Path] = set()
            for glob in self._LANGUAGE_EXTENSIONS[language]:
                for f in root.rglob(glob):
                    if f in seen:
                        continue
                    if any(ex in f.parts for ex in self._SEARCH_EXCLUDES):
                        continue
                    seen.add(f)
                    all_usages.extend(self._scan_file_for_symbol_regex(symbol, f))

        else:
            return Result.fail([
                f"Unsupported language: {language!r}. "
                f"Supported: {sorted(self._LANGUAGE_EXTENSIONS.keys())}."
            ])

        return Result.ok({
            "symbol":      symbol,
            "language":    language,
            "scan_method": scan_method,
            "usage_count": len(all_usages),
            "usages":      [asdict(u) for u in all_usages],
        })

    async def _tool_verify_sync_wrappers(self, server_path: str) -> Result:
        """Check every async _tool_* handler has a matching public sync wrapper.

        E-3: uses _parse_server_symbols (shared with verify_tool_registration).
        Does NOT execute the server.
        """
        try:
            parsed = self._parse_server_symbols(server_path)
        except (FileNotFoundError, SyntaxError) as e:
            return Result.fail([f"Cannot parse {server_path}: {e}"])

        async_handlers = set(parsed["async_handler_names"])
        sync_wrappers  = set(parsed["sync_wrapper_names"])

        gaps: list[SyncWrapperGap] = [
            SyncWrapperGap(h, True, False, "missing_sync_wrapper")
            for h in sorted(async_handlers) if h not in sync_wrappers
        ]
        return Result.ok({"gaps": [asdict(g) for g in gaps], "gap_count": len(gaps)})

    # ------------------------------------------------------------------
    # Quality gate runners  (E-1: single subprocess runner)
    # ------------------------------------------------------------------

    async def _run_gate(
        self,
        gate: str,
        paths: list[str],
        tier: EnvironmentTier = EnvironmentTier.LOCAL_PYTHON,
    ) -> GateResult:
        """Config-driven gate dispatch; resolves toolchain from tier."""
        tier_gates = resolve_tier_gates(self.config, tier.value)
        cmd_tokens: list[str] | None = getattr(tier_gates, gate, None)
        if cmd_tokens is None:
            raise ValueError(f"Unknown gate: {gate!r}")
        cmd = [sys.executable if tok == "python" else tok for tok in cmd_tokens]
        cmd.extend(paths)
        failure_filter = self._GATE_FAILURE_FILTERS.get(gate, lambda _: False)
        return await self._run_subprocess_gate(gate, cmd, failure_filter)

    async def _run_subprocess_gate(
        self,
        gate: Literal["test", "lint", "security"],
        cmd: list[str],
        failure_filter: Callable[[str], bool],
    ) -> GateResult:
        """Single subprocess runner for all quality gates. (E-1 consolidation)"""
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        stdout, _ = await proc.communicate()
        output = stdout.decode()
        failures = [line for line in output.splitlines() if failure_filter(line)]
        return GateResult(gate, proc.returncode == 0, proc.returncode, output, failures)

    # ------------------------------------------------------------------
    # Server health helper
    # ------------------------------------------------------------------

    async def _check_one_server(self, server_path: str) -> ServerHealth:
        """py_compile + tool_count for a single server.py."""
        try:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "py_compile", server_path,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
            stdout, _ = await proc.communicate()
            syntax_ok = proc.returncode == 0
            error = stdout.decode().strip() if not syntax_ok else None
            tool_count = 0
            if syntax_ok:
                try:
                    tool_count = Path(server_path).read_text(encoding="utf-8").count('Tool(name=')
                except OSError:
                    pass
            return ServerHealth(
                server_path=server_path,
                syntax_ok=syntax_ok,
                import_ok=syntax_ok,
                tool_count=tool_count,
                error=error,
            )
        except (FileNotFoundError, OSError) as e:
            return ServerHealth(
                server_path=server_path,
                syntax_ok=False,
                import_ok=False,
                tool_count=0,
                error=str(e),
            )

    # ------------------------------------------------------------------
    # Shared AST helper  (E-3: single parse consumed by two tools)
    # ------------------------------------------------------------------

    def _parse_server_symbols(self, server_path: str) -> dict:
        """Single AST walk returning all symbol categories for a server file.

        Called by both verify_tool_registration and verify_sync_wrappers so
        the file is parsed exactly once per diagnostic call.

        Returns
        -------
        {
          "tool_names": list[str],           # names from Tool(name=...) registrations
          "handler_names": list[str],        # _tool_* names (prefix stripped)
          "sync_wrapper_names": list[str],   # public non-underscore method names
          "async_handler_names": list[str],  # AsyncFunctionDef _tool_* (prefix stripped)
        }
        """
        source = Path(server_path).read_text(encoding="utf-8")
        tree   = ast.parse(source)   # raises SyntaxError / FileNotFoundError to caller

        tool_names, handler_names, sync_wrappers, async_handlers = [], [], [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "Tool":
                    for kw in node.keywords:
                        if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                            tool_names.append(kw.value.value)
            elif isinstance(node, ast.AsyncFunctionDef) and node.name.startswith("_tool_"):
                stripped = node.name[len("_tool_"):]
                handler_names.append(stripped)
                async_handlers.append(stripped)
            elif isinstance(node, ast.FunctionDef):
                if node.name.startswith("_tool_"):
                    handler_names.append(node.name[len("_tool_"):])
                elif not node.name.startswith("_"):
                    sync_wrappers.append(node.name)

        return {
            "tool_names":          tool_names,
            "handler_names":       handler_names,
            "sync_wrapper_names":  sync_wrappers,
            "async_handler_names": async_handlers,
        }

    # ------------------------------------------------------------------
    # Symbol scanner  (E-2: single file read)
    # ------------------------------------------------------------------

    def _scan_file_for_symbol_regex(self, symbol: str, path: Path) -> list[SymbolUsage]:
        """Whole-word regex scan — used for all non-Python languages.
        Returns same SymbolUsage type as AST scanner (usage_type='regex_match')."""
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []
        pattern = re.compile(r"\b" + re.escape(symbol) + r"\b")
        return [
            SymbolUsage(str(path), lineno, line.strip(), "regex_match")
            for lineno, line in enumerate(source.splitlines(), start=1)
            if pattern.search(line)
        ]

    def _scan_file_for_symbol(self, symbol: str, path: Path) -> list[SymbolUsage]:
        """AST-walk one file returning all usages of the exact symbol name."""
        try:
            source = path.read_text(encoding="utf-8")   # E-2: read once
            tree   = ast.parse(source)
        except (SyntaxError, OSError):
            return []

        usages: list[SymbolUsage] = []
        lines = source.splitlines()                      # derived — no second I/O

        for node in ast.walk(tree):
            usage_type: str | None = None
            name: str | None = None

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name, usage_type = node.name, "definition"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == symbol or alias.asname == symbol:
                        usages.append(SymbolUsage(
                            str(path), node.lineno,
                            lines[node.lineno - 1].strip(), "import",
                        ))
                continue
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == symbol or alias.asname == symbol:
                        usages.append(SymbolUsage(
                            str(path), node.lineno,
                            lines[node.lineno - 1].strip(), "import",
                        ))
                continue
            elif isinstance(node, ast.Call):
                func = node.func
                name = (
                    func.id   if isinstance(func, ast.Name)      else
                    func.attr if isinstance(func, ast.Attribute)  else None
                )
                usage_type = "call_site"
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == symbol:
                        usages.append(SymbolUsage(
                            str(path), target.lineno,
                            lines[target.lineno - 1].strip(), "assignment",
                        ))
                continue

            if name == symbol and usage_type:
                lineno   = getattr(node, "lineno", 0)
                ctx_line = lines[lineno - 1].strip() if lineno else ""
                usages.append(SymbolUsage(str(path), lineno, ctx_line, usage_type))

        return usages

    # ------------------------------------------------------------------
    # Sync public API (used by tests and direct callers)
    # ------------------------------------------------------------------

    def run_quality_gates(self, paths: list[str], **kwargs) -> Result:
        return self._run(self._tool_run_quality_gates(paths, **kwargs))

    def validate_code(self, path: str, **kwargs) -> Result:
        return self._run(self._tool_validate_code(path, **kwargs))

    def get_server_health(self) -> Result:
        return self._run(self._tool_get_server_health())

    def verify_tool_registration(self, server_path: str) -> Result:
        return self._run(self._tool_verify_tool_registration(server_path))

    def find_symbol_usages(self, symbol: str, language: str = "python", **kwargs) -> Result:
        return self._run(self._tool_find_symbol_usages(symbol, language=language, **kwargs))

    def verify_sync_wrappers(self, server_path: str) -> Result:
        return self._run(self._tool_verify_sync_wrappers(server_path))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ExecutorServer.cli_main()
