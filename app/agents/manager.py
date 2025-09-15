"""
AgentManager - Public API facade for agent discovery system.

Provides a high-level facade interface for managing agents, following the ModelFactory pattern.
Handles discovery, retrieval, filtering, lifecycle management, and agent creation.

This class provides the primary public API that external code should use to interact
with the agent discovery system.

Follows the facade pattern from app/models/factory.py
"""

from typing import List, Optional, Dict, Any, Union
from pathlib import Path

from agno.agent import Agent
from .registry import AgentRegistry
from .base import AgentDefinition, AgentFilter, DiscoveryPattern, discovery_logger


class AgentManager:
    """
    Public API facade for agent discovery and management.

    Provides stateless class methods that delegate to the AgentRegistry singleton
    for all agent-related operations. This follows the ModelFactory pattern.
    """

    @classmethod
    def _get_registry(cls) -> AgentRegistry:
        """Get the singleton AgentRegistry instance."""
        return AgentRegistry()

    @classmethod
    def discover(cls, paths: Optional[List[Union[str, Path]]] = None, force_refresh: bool = False) -> int:
        """
        Discover agents from specified paths or default discovery paths.

        Args:
            paths: Optional list of paths to scan for agents
            force_refresh: Whether to force rediscovery of all agents

        Returns:
            Number of agents discovered

        Raises:
            ValueError: If discovery paths are invalid
            ImportError: If agent modules cannot be imported
        """
        registry = cls._get_registry()

        # Add custom paths if provided
        if paths:
            for path in paths:
                path_obj = Path(path) if isinstance(path, str) else path
                if not path_obj.exists():
                    raise ValueError(f"Discovery path does not exist: {path_obj}")
                registry.add_discovery_path(path_obj)

        # Perform discovery
        registry.discover_agents(force_refresh=force_refresh)

        # Return number of discovered agents
        all_agents = registry.list_agents()
        discovered_count = len(all_agents)
        discovery_logger.info(f"Discovery completed: {discovered_count} agents found")
        return discovered_count

    @classmethod
    def refresh(cls) -> int:
        """
        Refresh agent discovery (re-scan for new/changed agents).

        Returns:
            Number of agents after refresh
        """
        discovery_logger.info("Refreshing agent discovery")
        return cls.discover(force_refresh=True)

    @classmethod
    def get_all(cls) -> List[AgentDefinition]:
        """
        Get all registered agent definitions.

        Returns:
            List of all agent definitions sorted by priority
        """
        registry = cls._get_registry()
        return registry.list_agents()

    @classmethod
    def get(cls, name: str) -> Optional[AgentDefinition]:
        """
        Get agent definition by name.

        Args:
            name: Agent name to retrieve

        Returns:
            AgentDefinition if found, None otherwise
        """
        if not name or not isinstance(name, str):
            return None

        registry = cls._get_registry()
        return registry.get_agent_definition(name)

    @classmethod
    def get_enabled(cls) -> List[AgentDefinition]:
        """
        Get all enabled agent definitions.

        Returns:
            List of enabled agent definitions
        """
        filter_obj = AgentFilter(enabled=True)
        registry = cls._get_registry()
        return registry.list_agents(filter_obj)

    @classmethod
    def get_by_tags(cls, tags: List[str], match_all: bool = False) -> List[AgentDefinition]:
        """
        Filter agents by tags.

        Args:
            tags: List of tags to filter by
            match_all: If True, agent must have all tags. If False, any tag matches.

        Returns:
            List of agent definitions matching tag criteria
        """
        if not tags or not isinstance(tags, list):
            return []

        registry = cls._get_registry()
        all_agents = registry.list_agents()

        # Filter agents based on tag matching strategy
        filtered_agents = []
        for agent in all_agents:
            agent_tags = agent.metadata.tags
            if match_all:
                # Agent must have all specified tags
                if all(tag in agent_tags for tag in tags):
                    filtered_agents.append(agent)
            else:
                # Agent must have at least one of the specified tags
                if any(tag in agent_tags for tag in tags):
                    filtered_agents.append(agent)

        discovery_logger.debug(f"Filtered by tags {tags} (match_all={match_all}): {len(filtered_agents)} agents")
        return filtered_agents

    @classmethod
    def get_by_pattern(cls, pattern: Union[str, DiscoveryPattern]) -> List[AgentDefinition]:
        """
        Filter agents by discovery pattern.

        Args:
            pattern: Discovery pattern (DECORATOR, CONVENTION, CONFIGURATION)

        Returns:
            List of agent definitions discovered via specified pattern
        """
        try:
            if isinstance(pattern, str):
                pattern_enum = DiscoveryPattern[pattern.upper()]
            else:
                pattern_enum = pattern

            filter_obj = AgentFilter(pattern=pattern_enum)
            registry = cls._get_registry()
            agents = registry.list_agents(filter_obj)
            discovery_logger.debug(f"Filtered by pattern {pattern_enum.name}: {len(agents)} agents")
            return agents

        except (KeyError, AttributeError):
            discovery_logger.error(f"Invalid discovery pattern: {pattern}")
            return []

    @classmethod
    def enable(cls, name: str) -> bool:
        """
        Enable an agent.

        Args:
            name: Agent name to enable

        Returns:
            True if agent was enabled, False if not found
        """
        if not name or not isinstance(name, str):
            return False

        registry = cls._get_registry()
        success = registry.enable_agent(name)
        if success:
            discovery_logger.info(f"Enabled agent: {name}")
        else:
            discovery_logger.warning(f"Agent not found for enabling: {name}")
        return success

    @classmethod
    def disable(cls, name: str) -> bool:
        """
        Disable an agent.

        Args:
            name: Agent name to disable

        Returns:
            True if agent was disabled, False if not found
        """
        if not name or not isinstance(name, str):
            return False

        registry = cls._get_registry()
        success = registry.disable_agent(name)
        if success:
            discovery_logger.info(f"Disabled agent: {name}")
        else:
            discovery_logger.warning(f"Agent not found for disabling: {name}")
        return success

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
        if not name or not isinstance(name, str):
            return None

        agent_def = cls.get(name)
        if not agent_def:
            discovery_logger.warning(f"Agent definition not found: {name}")
            return None

        if not agent_def.metadata.enabled:
            discovery_logger.warning(f"Agent is disabled: {name}")
            return None

        try:
            agent = agent_def.factory_function()
            discovery_logger.info(f"Created agent instance: {name}")
            return agent
        except Exception as e:
            error_msg = f"Failed to create agent {name}: {e}"
            discovery_logger.error(error_msg)
            raise RuntimeError(error_msg)

    @classmethod
    def create_enabled_agents(cls) -> List[Agent]:
        """
        Create instances of all enabled agents.

        Returns:
            List of created agent instances

        Raises:
            RuntimeError: If any agent creation fails
        """
        enabled_agents = cls.get_enabled()
        created_agents = []
        failed_agents = []

        for agent_def in enabled_agents:
            try:
                agent = agent_def.factory_function()
                created_agents.append(agent)
                discovery_logger.debug(f"Created agent: {agent_def.name}")
            except Exception as e:
                failed_agents.append((agent_def.name, str(e)))
                discovery_logger.error(f"Failed to create agent {agent_def.name}: {e}")

        if failed_agents:
            error_details = ", ".join([f"{name}: {error}" for name, error in failed_agents])
            error_msg = f"Failed to create {len(failed_agents)} agents: {error_details}"
            discovery_logger.error(error_msg)
            raise RuntimeError(error_msg)

        discovery_logger.info(f"Created {len(created_agents)} enabled agents")
        return created_agents

    @classmethod
    def add_discovery_path(cls, path: Union[str, Path]) -> None:
        """
        Add a discovery path for agent scanning.

        Args:
            path: Directory path to scan for agents
        """
        path_obj = Path(path) if isinstance(path, str) else path
        registry = cls._get_registry()
        registry.add_discovery_path(path_obj)

    @classmethod
    def remove_discovery_path(cls, path: Union[str, Path]) -> None:
        """
        Remove a discovery path.

        Args:
            path: Directory path to remove from scanning
        """
        path_obj = Path(path) if isinstance(path, str) else path
        registry = cls._get_registry()
        registry.remove_discovery_path(path_obj)

    @classmethod
    def get_discovery_paths(cls) -> List[Path]:
        """
        Get current discovery paths.

        Returns:
            List of current discovery paths
        """
        registry = cls._get_registry()
        return registry.get_discovery_paths()

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """
        Get discovery system statistics.

        Returns:
            Dictionary containing discovery statistics
        """
        registry = cls._get_registry()
        return registry.get_registry_stats()

    @classmethod
    def clear_registry(cls) -> None:
        """
        Clear all registered agents and reset discovery state.

        Warning: This will clear all discovered agents. Use with caution.
        """
        registry = cls._get_registry()
        registry.clear_registry()
        discovery_logger.warning("Agent registry cleared")