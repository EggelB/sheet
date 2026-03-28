"""Utility modules for ATLAS MCP servers.

Provides shared patterns used across all servers:
- results: Result<T> generic pattern for standardized return types
"""

from .results import Result, ResultStatus

__all__ = ["Result", "ResultStatus"]
