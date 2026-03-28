"""Result<T> generic pattern for standardized return types across all agents.

Eliminates custom result dataclasses, provides consistent success/failure handling
with optional warnings and metadata.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar

T = TypeVar('T')


class ResultStatus(Enum):
    """Result status enumeration."""
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class Result(Generic[T]):
    """Generic result container with status, data, errors, warnings, and metadata."""
    
    status: ResultStatus
    data: T | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def ok(cls, data: T, metadata: dict = None, **kwargs) -> 'Result[T]':
        """Create successful result with data.
        
        Args:
            data: Result data of type T
            metadata: Optional metadata dict
            **kwargs: Additional metadata as keyword args
            
        Returns:
            Result with SUCCESS status
        """
        meta = {**(metadata or {}), **kwargs}
        return cls(status=ResultStatus.SUCCESS, data=data, metadata=meta)
    
    @classmethod
    def fail(cls, errors: list[str], data: Any = None, metadata: dict = None, **kwargs) -> 'Result[T]':
        """Create failure result with error messages.
        
        Args:
            errors: List of error messages
            data: Optional structured error data for callers that inspect result.data
            metadata: Optional metadata dict
            **kwargs: Additional metadata as keyword args
            
        Returns:
            Result with FAILURE status
        """
        meta = {**(metadata or {}), **kwargs}
        return cls(status=ResultStatus.FAILURE, data=data, errors=errors, metadata=meta)

    def is_ok(self) -> bool:
        """Check if result is successful."""
        return self.status == ResultStatus.SUCCESS

    def is_failure(self) -> bool:
        """Check if result is failure."""
        return self.status == ResultStatus.FAILURE


