"""
Agent Manager API Contract

Defines the public interface for the AgentManager class.
This contract specifies the expected behavior and signatures.
"""

from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from agno.agent import Agent

# Import types that will be defined in implementation
# These serve as contract placeholders
from typing import Protocol, runtime_checkable


@runtime_checkable
class AgentDefinitionProtocol(Protocol):
    """Protocol for AgentDefinition objects."""
    name: str
    factory_function: callable
    metadata: 'AgentMetadataProtocol'
    module_path: str
    source_file: str

    def create_agent(self) -> Agent:
        """Create an instance of the agent."""
        ...


@runtime_checkable
class AgentMetadataProtocol(Protocol):
    """Protocol for AgentMetadata objects."""
    name: str
    tags: List[str]
    priority: int
    enabled: bool
    dependencies: List[str]
    custom_attributes: Dict[str, Any]

    def has_tag(self, tag: str) -> bool:
        """Check if agent has a specific tag."""
        ...

    def has_any_tags(self, tags: List[str]) -> bool:
        """Check if agent has any of the specified tags."""
        ...


class AgentManagerContract:
    """
    Public API contract for AgentManager.

    This defines the expected interface that external code can depend on.
    """

    @classmethod
    def discover(cls, paths: Optional[List[Union[str, Path]]] = None) -> int:
        """
        Discover agents from specified paths or default discovery paths.

        Args:
            paths: Optional list of paths to scan for agents

        Returns:
            Number of agents discovered

        Raises:
            ValueError: If discovery paths are invalid
            ImportError: If agent modules cannot be imported
        """
        ...

    @classmethod
    def get_all(cls) -> List[AgentDefinitionProtocol]:
        """
        Get all registered agent definitions.

        Returns:
            List of all agent definitions
        """
        ...

    @classmethod
    def get(cls, name: str) -> Optional[AgentDefinitionProtocol]:
        """
        Get agent definition by name.

        Args:
            name: Agent name to retrieve

        Returns:
            AgentDefinition if found, None otherwise
        """
        ...

    @classmethod
    def get_enabled(cls) -> List[AgentDefinitionProtocol]:
        """
        Get all enabled agent definitions.

        Returns:
            List of enabled agent definitions
        """
        ...

    @classmethod
    def get_by_tags(cls, tags: List[str], match_all: bool = False) -> List[AgentDefinitionProtocol]:
        """
        Filter agents by tags.

        Args:
            tags: List of tags to filter by
            match_all: If True, agent must have all tags. If False, any tag matches.

        Returns:
            List of agent definitions matching tag criteria
        """
        ...

    @classmethod
    def get_by_pattern(cls, pattern: str) -> List[AgentDefinitionProtocol]:
        """
        Filter agents by discovery pattern.

        Args:
            pattern: Discovery pattern name (DECORATOR, CONVENTION, CONFIGURATION)

        Returns:
            List of agent definitions discovered via specified pattern
        """
        ...

    @classmethod
    def enable(cls, name: str) -> bool:
        """
        Enable an agent.

        Args:
            name: Agent name to enable

        Returns:
            True if agent was enabled, False if not found
        """
        ...

    @classmethod
    def disable(cls, name: str) -> bool:
        """
        Disable an agent.

        Args:
            name: Agent name to disable

        Returns:
            True if agent was disabled, False if not found
        """
        ...

    @classmethod
    def refresh(cls) -> int:
        """
        Refresh agent discovery (re-scan for new/changed agents).

        Returns:
            Number of new agents discovered
        """
        ...

    @classmethod
    def create_agent(cls, name: str) -> Optional[Agent]:
        """
        Create an agent instance by name.

        Args:
            name: Agent name to create

        Returns:
            Agent instance if found and created successfully, None otherwise

        Raises:
            RuntimeError: If agent creation fails
        """
        ...

    @classmethod
    def create_enabled_agents(cls) -> List[Agent]:
        """
        Create instances of all enabled agents.

        Returns:
            List of created agent instances

        Raises:
            RuntimeError: If any agent creation fails
        """
        ...


# Expected usage patterns for validation
class UsageExamples:
    """Examples of expected API usage patterns."""

    def discover_and_get_agents(self):
        """Basic discovery and retrieval pattern."""
        # Discover agents from default paths
        count = AgentManagerContract.discover()

        # Get all agents
        all_agents = AgentManagerContract.get_all()

        # Get specific agent
        docs_agent = AgentManagerContract.get("docs_agent")

        # Get enabled agents for AgentOS
        enabled_agents = AgentManagerContract.get_enabled()

        return enabled_agents

    def filter_agents(self):
        """Agent filtering patterns."""
        # Get production agents
        prod_agents = AgentManagerContract.get_by_tags(["production"])

        # Get agents with all specified tags
        core_prod_agents = AgentManagerContract.get_by_tags(
            ["core", "production"],
            match_all=True
        )

        # Get agents by discovery pattern
        decorated_agents = AgentManagerContract.get_by_pattern("DECORATOR")

        return core_prod_agents

    def manage_agents(self):
        """Agent lifecycle management patterns."""
        # Enable/disable agents
        AgentManagerContract.enable("debug_agent")
        AgentManagerContract.disable("experimental_agent")

        # Refresh discovery
        new_count = AgentManagerContract.refresh()

        return new_count

    def create_agent_instances(self):
        """Agent instance creation patterns."""
        # Create specific agent
        agent = AgentManagerContract.create_agent("docs_agent")

        # Create all enabled agents (for AgentOS)
        agents = AgentManagerContract.create_enabled_agents()

        return agents