"""
Common types and protocols for agent discovery system.

This module defines the core data structures used throughout the agent discovery system:
- DiscoveryPattern: Enum for discovery method priorities
- AgentMetadata: Descriptive information about agents
- AgentDefinition: Complete discovered agent with factory function
- AgentFilter: Criteria for selecting agents during retrieval
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable, Dict, Any, List, Optional
from pathlib import Path

from app.utils.log import get_logger

# Logger for agent discovery system
discovery_logger = get_logger("agent-discovery")


class DiscoveryPattern(IntEnum):
    """
    Discovery pattern enumeration - simplified to decorator only.

    Keeping enum for backward compatibility but only decorator pattern is used.
    """
    DECORATOR = 1    # Only supported pattern: @register_agent decorated functions


@dataclass
class AgentMetadata:
    """
    Descriptive information about agents for discovery and management.

    Contains all metadata needed for agent categorization, filtering, and lifecycle management.
    """
    name: str
    pattern: DiscoveryPattern
    tags: List[str] = field(default_factory=list)
    priority: int = 50
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate metadata fields after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Agent name must be a non-empty string")
        if not isinstance(self.priority, int) or self.priority < 0:
            raise ValueError("Priority must be a positive integer")
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list of strings")
        if not all(isinstance(tag, str) for tag in self.tags):
            raise ValueError("All tags must be strings")
        if not isinstance(self.dependencies, list):
            raise ValueError("Dependencies must be a list of strings")
        if not all(isinstance(dep, str) for dep in self.dependencies):
            raise ValueError("All dependencies must be strings")


@dataclass
class AgentDefinition:
    """
    Complete discovered agent with its creation mechanism.

    Represents a fully discovered agent including the factory function to create instances
    and all associated metadata.
    """
    name: str
    factory_function: Callable[[], Any]  # Returns Agno Agent instance
    metadata: AgentMetadata
    module_path: str
    source_file: str

    def __post_init__(self):
        """Validate agent definition after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Agent name must be a non-empty string")
        if not callable(self.factory_function):
            raise ValueError("Factory function must be callable")
        if not isinstance(self.metadata, AgentMetadata):
            raise ValueError("Metadata must be an AgentMetadata instance")
        if self.name != self.metadata.name:
            raise ValueError("Agent name must match metadata name")
        if not isinstance(self.module_path, str):
            raise ValueError("Module path must be a string")
        if not isinstance(self.source_file, str):
            raise ValueError("Source file must be a string")

        # Validate source file exists (skip for decorator pattern as file may be unknown)
        if self.source_file != 'unknown' and not Path(self.source_file).exists():
            raise ValueError(f"Source file does not exist: {self.source_file}")


@dataclass
class AgentFilter:
    """
    Criteria for selecting agents during discovery or retrieval.

    Supports filtering by various agent attributes for flexible agent selection.
    """
    tags: Optional[List[str]] = None
    enabled: Optional[bool] = None
    pattern: Optional[DiscoveryPattern] = None
    priority_min: Optional[int] = None
    priority_max: Optional[int] = None
    custom_criteria: Dict[str, Any] = field(default_factory=dict)

    def matches(self, agent_def: AgentDefinition) -> bool:
        """
        Check if an agent definition matches this filter.

        Args:
            agent_def: Agent definition to check

        Returns:
            True if the agent matches all filter criteria
        """
        metadata = agent_def.metadata

        # Check enabled status
        if self.enabled is not None and metadata.enabled != self.enabled:
            return False

        # Check discovery pattern
        if self.pattern is not None and metadata.pattern != self.pattern:
            return False

        # Check priority range
        if self.priority_min is not None and metadata.priority < self.priority_min:
            return False
        if self.priority_max is not None and metadata.priority > self.priority_max:
            return False

        # Check tags (any match)
        if self.tags is not None and self.tags:
            if not any(tag in metadata.tags for tag in self.tags):
                return False

        # Check custom criteria
        for key, expected_value in self.custom_criteria.items():
            if key not in metadata.custom_attributes:
                return False
            if metadata.custom_attributes[key] != expected_value:
                return False

        return True