"""Public service ports used by DGM-MAT agents.

These protocols keep agent implementations independent from DGM-MAT Core internals.
Core supplies concrete adapters at composition time.
"""
from __future__ import annotations

from typing import Protocol


class AgentLogger(Protocol):
    def info(self, message: str) -> None: ...
    def error(self, message: str) -> None: ...
    def critical(self, message: str) -> None: ...


class ProviderService(Protocol):
    def run(self) -> None: ...


class TaskService(Protocol):
    def analyze_issue(self, issue_type: str, description: str, origin: str = "repo_analysis") -> None: ...


class NullAgentLogger:
    """No-op logger for standalone agent execution and tests."""
    def info(self, message: str) -> None:
        return None

    def error(self, message: str) -> None:
        return None

    def critical(self, message: str) -> None:
        return None


class NullProviderService:
    def run(self) -> None:
        return None


class NullTaskService:
    def analyze_issue(self, issue_type: str, description: str, origin: str = "repo_analysis") -> None:
        return None
