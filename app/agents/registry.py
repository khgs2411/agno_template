"""
AgentRegistry - State management for discovered agents.

Singleton registry that handles all agent discovery and management:
- Agent discovery across different patterns
- Agent registration and metadata tracking
- Discovery path management
- Hot reload and caching support
- Error handling with graceful degradation

Follows the ProviderRegistry pattern from app/models/provider_registry.py
"""

import importlib
import importlib.util
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any
from dataclasses import asdict

from .base import (
    AgentDefinition,
    AgentMetadata,
    DiscoveryPattern,
    AgentFilter,
    discovery_logger
)


class AgentRegistry:
    """
    Singleton registry for agent discovery and management.

    Handles all state-related logic including:
    - Agent discovery across different patterns
    - Agent registration and metadata tracking
    - Discovery path management
    - Hot reload support with file modification tracking
    - Error handling with graceful degradation
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

        # Core registry state
        self._agent_definitions: Dict[str, AgentDefinition] = {}
        self._decorated_functions: Dict[str, Callable] = {}
        self._discovery_paths: List[Path] = []
        self._discovery_completed: bool = False

        # Hot reload support
        self._module_modification_times: Dict[str, float] = {}
        self._cached_modules: Dict[str, Any] = {}

        # Error tracking
        self._failed_imports: Set[str] = set()

        # Set default discovery paths
        self._setup_default_discovery_paths()

        self._initialized = True
        discovery_logger.info("AgentRegistry initialized")

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

    def add_discovery_path(self, path: Path) -> None:
        """
        Add a new discovery path for agent scanning.

        Args:
            path: Directory path to scan for agents
        """
        path = Path(path).resolve()
        if path not in self._discovery_paths:
            self._discovery_paths.append(path)
            discovery_logger.info(f"Added discovery path: {path}")

    def remove_discovery_path(self, path: Path) -> None:
        """
        Remove a discovery path.

        Args:
            path: Directory path to remove from scanning
        """
        path = Path(path).resolve()
        if path in self._discovery_paths:
            self._discovery_paths.remove(path)
            discovery_logger.info(f"Removed discovery path: {path}")

    def get_discovery_paths(self) -> List[Path]:
        """Get current discovery paths."""
        return self._discovery_paths.copy()

    def discover_agents(self, force_refresh: bool = False) -> None:
        """
        Discover all agents using all patterns in priority order.

        Args:
            force_refresh: Whether to force rediscovery of all agents
        """
        if self._discovery_completed and not force_refresh:
            discovery_logger.debug("Discovery already completed, skipping")
            return

        discovery_logger.info("Starting agent discovery")

        if force_refresh:
            self.clear_registry()

        # Discover agents by pattern priority (lower numbers = higher priority)
        for pattern in sorted(DiscoveryPattern, key=lambda p: p.value):
            try:
                if pattern == DiscoveryPattern.DECORATOR:
                    self._discover_decorator_pattern()
                elif pattern == DiscoveryPattern.CONVENTION:
                    self._discover_convention_pattern()
                elif pattern == DiscoveryPattern.CONFIGURATION:
                    self._discover_configuration_pattern()
            except Exception as e:
                discovery_logger.error(f"Error in {pattern.name} pattern discovery: {e}")
                # Continue with other patterns even if one fails

        self._discovery_completed = True
        discovery_logger.info(f"Discovery completed. Found {len(self._agent_definitions)} agents")

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
                if hasattr(func, '_agent_metadata'):
                    metadata = func._agent_metadata
                    self._register_agent_definition(name, func, metadata,
                                                   getattr(func, '__module__', 'unknown'),
                                                   getattr(func, '__file__', 'unknown'))

    def _discover_convention_pattern(self) -> None:
        """Discover agents using file naming convention (*_agent.py)."""
        discovery_logger.debug("Starting convention pattern discovery")

        for path in self._discovery_paths:
            for agent_file in path.glob("*_agent.py"):
                if agent_file.name == "__init__.py":
                    continue

                try:
                    module_name = agent_file.stem
                    agent_name = module_name.replace("_", " ").title().replace(" ", "")

                    if agent_name in self._agent_definitions:
                        continue  # Already discovered by higher priority pattern

                    module = self._import_module_from_file(agent_file)
                    if module is None:
                        continue

                    # Look for agent instance or factory function
                    factory_func = None
                    if hasattr(module, 'create_agent') and callable(getattr(module, 'create_agent')):
                        factory_func = getattr(module, 'create_agent')
                    elif hasattr(module, 'agent'):
                        # Wrap agent instance in a factory function
                        agent_instance = getattr(module, 'agent')
                        factory_func = lambda: agent_instance

                    if factory_func:
                        # Extract metadata from module variables
                        metadata = self._extract_convention_metadata(module, agent_name)
                        self._register_agent_definition(
                            agent_name, factory_func, metadata,
                            module.__name__, str(agent_file)
                        )
                        discovery_logger.debug(f"Discovered convention agent: {agent_name}")

                except Exception as e:
                    discovery_logger.error(f"Error processing convention file {agent_file}: {e}")
                    self._failed_imports.add(str(agent_file))

    def _discover_configuration_pattern(self) -> None:
        """Discover agents using AGENT_CONFIG exports."""
        discovery_logger.debug("Starting configuration pattern discovery")

        for path in self._discovery_paths:
            for py_file in path.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue

                try:
                    module = self._import_module_from_file(py_file)
                    if module is None or not hasattr(module, 'AGENT_CONFIG'):
                        continue

                    config = getattr(module, 'AGENT_CONFIG')
                    if not isinstance(config, dict):
                        continue

                    agent_name = config.get('name')
                    if not agent_name or agent_name in self._agent_definitions:
                        continue

                    # Look for factory function
                    factory_func_name = config.get('factory', 'create_agent')
                    if hasattr(module, factory_func_name):
                        factory_func = getattr(module, factory_func_name)
                        metadata = self._extract_config_metadata(config, agent_name)
                        self._register_agent_definition(
                            agent_name, factory_func, metadata,
                            module.__name__, str(py_file)
                        )
                        discovery_logger.debug(f"Discovered config agent: {agent_name}")

                except Exception as e:
                    discovery_logger.error(f"Error processing config file {py_file}: {e}")
                    self._failed_imports.add(str(py_file))

    def _scan_path_for_modules(self, path: Path) -> None:
        """Scan a path and import all Python modules."""
        for py_file in path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            self._import_module_from_file(py_file)

    def _import_module_from_file(self, file_path: Path) -> Optional[Any]:
        """
        Import a module from a file path with error handling.

        Args:
            file_path: Path to the Python file

        Returns:
            Imported module or None if import failed
        """
        try:
            # Check if we should reload based on modification time
            file_path_str = str(file_path)
            current_mtime = os.path.getmtime(file_path)

            if file_path_str in self._module_modification_times:
                if current_mtime <= self._module_modification_times[file_path_str]:
                    # File hasn't changed, return cached module if available
                    return self._cached_modules.get(file_path_str)

            # Import the module
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)

            # Add to sys.modules for proper import resolution
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

            # Cache the module and track modification time
            self._cached_modules[file_path_str] = module
            self._module_modification_times[file_path_str] = current_mtime

            return module

        except Exception as e:
            discovery_logger.error(f"Failed to import module {file_path}: {e}")
            self._failed_imports.add(str(file_path))
            return None

    def _extract_convention_metadata(self, module: Any, agent_name: str) -> AgentMetadata:
        """Extract metadata from module variables for convention pattern."""
        return AgentMetadata(
            name=agent_name,
            pattern=DiscoveryPattern.CONVENTION,
            tags=getattr(module, 'AGENT_TAGS', []),
            priority=getattr(module, 'AGENT_PRIORITY', 50),
            enabled=getattr(module, 'AGENT_ENABLED', True),
            dependencies=getattr(module, 'AGENT_DEPENDENCIES', []),
            custom_attributes=getattr(module, 'AGENT_CUSTOM_ATTRIBUTES', {})
        )

    def _extract_config_metadata(self, config: Dict[str, Any], agent_name: str) -> AgentMetadata:
        """Extract metadata from AGENT_CONFIG dictionary."""
        return AgentMetadata(
            name=agent_name,
            pattern=DiscoveryPattern.CONFIGURATION,
            tags=config.get('tags', []),
            priority=config.get('priority', 50),
            enabled=config.get('enabled', True),
            dependencies=config.get('dependencies', []),
            custom_attributes=config.get('custom_attributes', {})
        )

    def register_decorated_function(self, name: str, func: Callable, metadata: AgentMetadata) -> None:
        """
        Register a function decorated with @register_agent.

        This is called by the decorator itself during module import.
        """
        # Avoid duplicate registration during hot reload
        if name in self._decorated_functions:
            discovery_logger.debug(f"Skipping duplicate decorated function registration: {name}")
            return

        self._decorated_functions[name] = func
        func._agent_metadata = metadata
        discovery_logger.debug(f"Collected decorated function: {name}")

    def _register_agent_definition(self, name: str, factory_func: Callable,
                                  metadata: AgentMetadata, module_path: str, source_file: str) -> None:
        """Register a complete agent definition."""
        try:
            # Check if agent already exists and has higher or equal priority
            if name in self._agent_definitions:
                existing_priority = self._agent_definitions[name].metadata.priority
                new_priority = metadata.priority
                if existing_priority >= new_priority:
                    discovery_logger.debug(
                        f"Skipping agent {name} - existing priority {existing_priority} >= new priority {new_priority}"
                    )
                    return
                else:
                    discovery_logger.debug(
                        f"Replacing agent {name} - new priority {new_priority} > existing priority {existing_priority}"
                    )

            agent_def = AgentDefinition(
                name=name,
                factory_function=factory_func,
                metadata=metadata,
                module_path=module_path,
                source_file=source_file
            )
            self._agent_definitions[name] = agent_def
            discovery_logger.info(f"Registered agent: {name} (pattern: {metadata.pattern.name}, priority: {metadata.priority})")
        except Exception as e:
            discovery_logger.error(f"Failed to register agent {name}: {e}")

    def get_agent_definition(self, name: str) -> Optional[AgentDefinition]:
        """Get agent definition by name."""
        return self._agent_definitions.get(name)

    def list_agents(self, filter_obj: Optional[AgentFilter] = None) -> List[AgentDefinition]:
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
        """
        Enable an agent.

        Args:
            name: Agent name

        Returns:
            True if successful, False if agent not found
        """
        agent_def = self._agent_definitions.get(name)
        if agent_def:
            agent_def.metadata.enabled = True
            discovery_logger.info(f"Enabled agent: {name}")
            return True
        return False

    def disable_agent(self, name: str) -> bool:
        """
        Disable an agent.

        Args:
            name: Agent name

        Returns:
            True if successful, False if agent not found
        """
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
        self._module_modification_times.clear()
        self._cached_modules.clear()
        self._failed_imports.clear()
        self._discovery_completed = False
        discovery_logger.info("Agent registry cleared")

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics for debugging."""
        enabled_count = sum(1 for agent in self._agent_definitions.values()
                           if agent.metadata.enabled)

        pattern_counts = {}
        for pattern in DiscoveryPattern:
            count = sum(1 for agent in self._agent_definitions.values()
                       if agent.metadata.pattern == pattern)
            pattern_counts[pattern.name] = count

        return {
            'total_agents': len(self._agent_definitions),
            'enabled_agents': enabled_count,
            'disabled_agents': len(self._agent_definitions) - enabled_count,
            'discovery_paths': [str(p) for p in self._discovery_paths],
            'pattern_counts': pattern_counts,
            'failed_imports': len(self._failed_imports),
            'discovery_completed': self._discovery_completed
        }