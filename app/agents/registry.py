"""
AgentRegistry - Simplified agent discovery and management.

Singleton registry that handles decorator-based agent discovery only:
- Agent discovery via @register_agent decorators
- Agent registration and metadata tracking
- Simple discovery path management
- Graceful error handling

Simplified from original design following KISS principles.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

from agno.agent import Agent

from .base import (
    AgentDefinition,
    AgentMetadata,
    DiscoveryPattern,
    AgentFilter,
    discovery_logger,
)


class AgentRegistry:
    """
    Simplified singleton registry for decorator-based agent discovery.

    Handles only decorator-based agent discovery following KISS principles:
    - Agent discovery via @register_agent decorators only
    - Simple agent registration and metadata tracking
    - Basic discovery path management
    - Graceful error handling without complex caching
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize registry if not already initialized."""
        if self._initialized:
            return

        # Core registry state - simplified
        self._agent_definitions: Dict[str, AgentDefinition] = {}
        self._decorated_functions: Dict[str, Callable] = {}
        self._discovery_paths: List[Path] = []
        self._discovery_completed: bool = False

        # Set default discovery paths
        self._setup_default_discovery_paths()

        self._initialized = True
        discovery_logger.info("AgentRegistry initialized (simplified)")

    def _setup_default_discovery_paths(self):
        """Setup default discovery paths based on project structure."""
        # Primary discovery path: app/agents/definitions/
        definitions_path = Path(__file__).parent / "definitions"
        if definitions_path.exists():
            self._discovery_paths.append(definitions_path)
            discovery_logger.debug(f"Added default discovery path: {definitions_path}")

        # Also scan app/agents/ for backward compatibility
        agents_path = Path(__file__).parent
        self._discovery_paths.append(agents_path)
        discovery_logger.debug(f"Added agents discovery path: {agents_path}")

    def discover_agents(self, force_refresh: bool = False) -> None:
        """
        Discover agents using decorator pattern only.

        Args:
            force_refresh: Whether to force rediscovery of all agents
        """
        if self._discovery_completed and not force_refresh:
            discovery_logger.debug("Discovery already completed, skipping")
            return

        discovery_logger.info(
            "Starting simplified agent discovery (decorator pattern only)"
        )

        if force_refresh:
            self.clear_registry()

        # Only discover decorator pattern - SIMPLIFIED
        try:
            self._discover_decorator_pattern()
        except Exception as e:
            discovery_logger.error(f"Error in decorator pattern discovery: {e}")

        self._discovery_completed = True
        discovery_logger.info(
            f"Discovery completed. Found {len(self._agent_definitions)} agents"
        )

        # Log discovered agents
        for name, agent_def in self._agent_definitions.items():
            discovery_logger.debug(
                f"Discovered agent: {name} "
                f"[{agent_def.metadata.pattern.name}, "
                f"priority={agent_def.metadata.priority}, "
                f"enabled={agent_def.metadata.enabled}]"
            )

    def _discover_decorator_pattern(self) -> None:
        """Discover agents marked with @register_agent decorator."""
        discovery_logger.debug("Starting decorator pattern discovery")

        # Import all modules to trigger decorator registration
        for path in self._discovery_paths:
            self._scan_path_for_modules(path)

        # Register any decorated functions that were collected
        for name, func in self._decorated_functions.items():
            if name not in self._agent_definitions:
                discovery_logger.debug(f"Registering decorated agent: {name}")
                # Decorated functions should have metadata attached by the decorator
                if hasattr(func, "_agent_metadata"):
                    metadata = func._agent_metadata
                    self._register_agent_definition(
                        name,
                        func,
                        metadata,
                        getattr(func, "__module__", "unknown"),
                        getattr(func, "__file__", "unknown"),
                    )

    def _scan_path_for_modules(self, path: Path) -> None:
        """Scan a path and import all Python modules."""
        for py_file in path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            self._import_module_from_file(py_file)

    def _import_module_from_file(self, file_path: Path) -> Optional[object]:
        """
        Import a module from a file path with simple error handling.

        Args:
            file_path: Path to the Python file

        Returns:
            Imported module or None if import failed
        """
        try:
            # Simple import without caching - SIMPLIFIED
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)

            # Add to sys.modules for proper import resolution
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

            return module

        except Exception as e:
            discovery_logger.error(f"Failed to import module {file_path}: {e}")
            return None

    def register_decorated_function(
        self, name: str, func: Callable, metadata: AgentMetadata
    ) -> None:
        """
        Register a function decorated with @register_agent.

        This is called by the decorator itself during module import.
        """
        self._decorated_functions[name] = func
        func._agent_metadata = metadata
        discovery_logger.debug(f"Collected decorated function: {name}")

    def _register_agent_definition(
        self,
        name: str,
        factory_func: Callable,
        metadata: AgentMetadata,
        module_path: str,
        source_file: str,
    ) -> None:
        """Register a complete agent definition."""
        try:
            # Simple priority check - SIMPLIFIED
            if name in self._agent_definitions:
                existing_priority = self._agent_definitions[name].metadata.priority
                new_priority = metadata.priority
                if existing_priority >= new_priority:
                    discovery_logger.debug(
                        f"Skipping agent {name} - existing priority {existing_priority} >= new priority {new_priority}"
                    )
                    return

            agent_def = AgentDefinition(
                name=name,
                factory_function=factory_func,
                metadata=metadata,
                module_path=module_path,
                source_file=source_file,
            )
            self._agent_definitions[name] = agent_def
            discovery_logger.info(
                f"Registered agent: {name} (priority: {metadata.priority})"
            )
        except Exception as e:
            discovery_logger.error(f"Failed to register agent {name}: {e}")

    def get_agent_definition(self, name: str) -> Optional[AgentDefinition]:
        """Get agent definition by name."""
        return self._agent_definitions.get(name)

    def list_agents(
        self, filter_obj: Optional[AgentFilter] = None
    ) -> List[AgentDefinition]:
        """
        List all agent definitions, optionally filtered.

        Args:
            filter_obj: Optional filter criteria

        Returns:
            List of agent definitions matching the filter
        """
        agents = list(self._agent_definitions.values())

        if filter_obj:
            agents = [agent for agent in agents if filter_obj.matches(agent)]

        # Sort by priority (higher priority first) then by name
        agents.sort(key=lambda a: (-a.metadata.priority, a.name))
        return agents

    def enable_agent(self, name: str) -> bool:
        """Enable an agent."""
        agent_def = self._agent_definitions.get(name)
        if agent_def:
            agent_def.metadata.enabled = True
            discovery_logger.info(f"Enabled agent: {name}")
            return True
        return False

    def disable_agent(self, name: str) -> bool:
        """Disable an agent."""
        agent_def = self._agent_definitions.get(name)
        if agent_def:
            agent_def.metadata.enabled = False
            discovery_logger.info(f"Disabled agent: {name}")
            return True
        return False

    def clear_registry(self) -> None:
        """Clear all registered agents and reset discovery state."""
        self._agent_definitions.clear()
        self._decorated_functions.clear()
        self._discovery_completed = False
        discovery_logger.info("Agent registry cleared")

    @classmethod
    def discover_and_create_all(cls) -> List[Agent]:
        """
        One-shot discovery and creation of all enabled agents.

        This is the simplified public API for server integration.
        """
        registry = cls()
        registry.discover_agents()

        # Get enabled agents and create instances
        enabled_agents = [
            agent_def
            for agent_def in registry._agent_definitions.values()
            if agent_def.metadata.enabled
        ]

        agents = []
        for agent_def in enabled_agents:
            try:
                agent = agent_def.factory_function()
                agents.append(agent)
                discovery_logger.info(f"Created agent: {agent_def.name}")
            except Exception as e:
                discovery_logger.error(f"Failed to create agent {agent_def.name}: {e}")
                # Continue with other agents

        discovery_logger.info(f"Created {len(agents)} enabled agents")
        return agents
