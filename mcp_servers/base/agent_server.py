"""BaseAgentServer abstract class for ATLAS Agent Fleet MCP servers.

Eliminates MCP boilerplate via inheritance pattern. All 8 specialized agents
inherit from BaseAgentServer, providing agent_name and _get_tools() methods.

Consolidation Impact: 64% boilerplate reduction (320 LOC → 115 LOC across 8 agents)
"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

# MCP SDK imports (will be installed via requirements.txt)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

from mcp_servers.utils.results import Result


class BaseAgentServer(ABC):
    """Abstract base class for all ATLAS agent MCP servers.
    
    Eliminates manual Server() init, @list_tools/@call_tool decorators,
    if-elif tool dispatch, and run() boilerplate per agent.
    
    Subclasses implement:
        - agent_name property: Unique agent identifier
        - _get_tools(): Returns list of Tool definitions
        - Tool handler methods: Named _tool_<tool_name>(arguments)
    
    Example:
        class ExampleServer(BaseAgentServer):
            @property
            def agent_name(self) -> str:
                return "example"

            def _get_tools(self) -> list[Tool]:
                return [
                    Tool(name="do_thing", description="...", inputSchema={...})
                ]

            async def _tool_do_thing(self, **kwargs) -> Result:
                return Result.ok({"done": True})
    """
    
    def __init__(self):
        """Initialize base agent server with tool registry."""
        self.server = Server(self.agent_name)
        self._tool_registry: dict[str, Any] = {}
        # Anchor to the repo root (two levels up from mcp_servers/base/)
        # so load_config() finds .tempo.config.toml regardless of the
        # working directory the MCP server process was launched from.
        self.workspace_root: str = str(Path(__file__).resolve().parent.parent.parent)
        self._register_tools()
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Return agent's unique name (used for MCP server identification)."""
        pass

    @property
    def agent_persona(self) -> str | None:
        """Optional one-line persona shown at the top of every tool response.

        Override in subclasses to provide companion-style framing in tool output.
        Return None (default) to omit the persona header entirely.

        Returns:
            Persona string or None to omit framing header.
        """
        return None

    @abstractmethod
    def _get_tools(self) -> list[Tool]:
        """Return list of Tool definitions for this agent.
        
        Each Tool should have:
            - name: Tool name (must match handler method _tool_<name>)
            - description: What the tool does
            - inputSchema: JSON schema for tool arguments
        
        Returns:
            List of Tool definitions
        """
        pass
    
    def _register_tools(self):
        """Register tools with MCP server and build tool dispatcher registry.
        
        Automatically called during __init__. For each tool from _get_tools():
        1. Registers with MCP server via @list_tools decorator
        2. Builds tool_name → handler method mapping
        3. Sets up @call_tool dispatcher
        
        Handler methods must be named _tool_<tool_name> and async.
        """
        tools = self._get_tools()
        
        # Register list_tools handler
        @self.server.list_tools()
        async def list_tools():
            return tools
        
        # Build tool registry: tool_name → handler method
        for tool in tools:
            handler_name = f"_tool_{tool.name}"
            if not hasattr(self, handler_name):
                raise AttributeError(
                    f"Agent '{self.agent_name}' missing handler method: {handler_name}"
                )
            handler = getattr(self, handler_name)
            if not callable(handler):
                raise TypeError(
                    f"Handler {handler_name} must be callable method"
                )
            self._tool_registry[tool.name] = handler
        
        # Register call_tool dispatcher
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name not in self._tool_registry:
                return [TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}' for agent '{self.agent_name}'"
                )]
            
            try:
                handler = self._tool_registry[name]
                result: Result = await handler(**arguments)
                
                # Format Result as MCP response
                import json
                import dataclasses
                from enum import Enum

                def _serialize(obj):
                    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
                        return dataclasses.asdict(obj)
                    if isinstance(obj, Enum):
                        return obj.value
                    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

                response_parts = []

                # Persona header for user-facing agents
                if self.agent_persona:
                    response_parts.append(self.agent_persona)

                # Add result data if present
                if result.data is not None:
                    data = result.data
                    if dataclasses.is_dataclass(data) and not isinstance(data, type):
                        data = dataclasses.asdict(data)
                    
                    response_parts.append(f"**Result:** {json.dumps(data, indent=2, default=_serialize)}")
                
                # Add warnings if present
                if result.warnings:
                    response_parts.append(f"**Warnings:** {', '.join(result.warnings)}")
                
                # Add errors if present
                if result.errors:
                    response_parts.append(f"**Errors:** {', '.join(result.errors)}")
                
                # Add metadata if present
                if result.metadata:
                    response_parts.append(f"**Metadata:** {json.dumps(result.metadata, indent=2, default=_serialize)}")
                
                # Status line - warm framing for user-facing agents, plain for execution agents
                if self.agent_persona:
                    status_val = result.status.value
                    if status_val == "success":
                        status_label = "✅ Done"
                    elif status_val == "partial":
                        status_label = "⚠️ Partial"
                    elif status_val == "escalation":
                        status_label = "🔼 Escalation needed"
                    else:
                        status_label = "❌ Failed"
                    response_parts.append(f"**Status:** {status_label}")
                else:
                    response_parts.append(f"**Status:** {result.status.value}")
                
                response_text = "\n\n".join(response_parts)
                
                return [TextContent(type="text", text=response_text)]
                
            except Exception as e:
                import traceback
                error_text = f"Error executing tool '{name}': {str(e)}\n\n{traceback.format_exc()}"
                return [TextContent(type="text", text=error_text)]
    
    async def run(self):
        """Run MCP server with stdio transport.
        
        Starts server listening on stdin/stdout for MCP protocol messages.
        Blocks until server stops.
        """
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
    
    @classmethod
    def cli_main(cls):
        """CLI entry point for running agent as MCP server.
        
        Usage:
            if __name__ == "__main__":
                ResearcherServer.cli_main()
        """
        import asyncio
        agent = cls()
        asyncio.run(agent.run())

    def _run(self, coro):
        """Run an async coroutine synchronously.

        Used by sync public API wrappers on each server subclass so integration
        tests and direct callers don't need to manage an event loop.
        """
        import asyncio
        import concurrent.futures
        try:
            asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(asyncio.run, coro).result()
        except RuntimeError:
            return asyncio.run(coro)
