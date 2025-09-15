"""
@register_agent decorator for agent discovery.

Provides the @register_agent decorator that marks functions for automatic agent discovery.
This is the highest priority discovery pattern and enables zero-configuration agent registration.

Usage:
    @register_agent(tags=["core"], priority=100)
    def create_my_agent():
        return AgentBuilder("My Agent").with_model("openai").build()
"""

from functools import wraps
from typing import Callable, List, Optional, Dict, Any, Protocol, TypeVar, cast
from typing_extensions import ParamSpec

from .base import AgentMetadata, DiscoveryPattern, discovery_logger
from .registry import AgentRegistry

# Type variables for proper typing
P = ParamSpec('P')
T = TypeVar('T')


class AgentFactoryProtocol(Protocol):
    """Protocol for agent factory functions with metadata."""
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    # These will be set by our decorator registry
    _agent_registry_id: str
    _is_agent_factory: bool


# Global registry to store metadata for decorated functions
_decorator_metadata_registry: Dict[str, AgentMetadata] = {}
_decorator_name_registry: Dict[str, str] = {}


def register_agent(
    tags: Optional[List[str]] = None,
    priority: int = 50,
    enabled: bool = True,
    dependencies: Optional[List[str]] = None,
    **custom_attributes
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to register agent factory functions for automatic discovery.

    This decorator marks functions for automatic discovery by the agent registry.
    The decorated function will be registered immediately during module import
    and can be discovered later by the discovery system.

    Args:
        tags: Agent tags for categorization (default: [])
        priority: Agent priority for loading order (default: 50, higher = higher priority)
        enabled: Whether agent is enabled by default (default: True)
        dependencies: List of required dependencies (default: [])
        **custom_attributes: Custom metadata attributes

    Returns:
        Decorator function

    Usage:
        @register_agent(tags=["core"], priority=100)
        def create_my_agent():
            return AgentBuilder("My Agent").with_model("openai").build()

        @register_agent(tags=["docs", "search"], priority=75, enabled=True)
        def create_documentation_agent():
            return (AgentBuilder("Documentation Agent")
                   .with_model("openai")
                   .with_mcp("docs")
                   .with_memory()
                   .build())
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        # Extract agent name from function name
        func_name = func.__name__
        if func_name.startswith('create_'):
            agent_name = func_name[7:]  # Remove 'create_' prefix
        else:
            agent_name = func_name

        # Convert snake_case to Title Case for agent name
        agent_name = agent_name.replace('_', ' ').title()

        # Create metadata for the agent
        metadata = AgentMetadata(
            name=agent_name,
            pattern=DiscoveryPattern.DECORATOR,
            tags=tags or [],
            priority=priority,
            enabled=enabled,
            dependencies=dependencies or [],
            custom_attributes=custom_attributes
        )

        # Create unique registry ID for this function
        registry_id = f"{func.__module__}.{func.__name__}_{id(func)}"

        # Store metadata in global registries
        _decorator_metadata_registry[registry_id] = metadata
        _decorator_name_registry[registry_id] = agent_name

        # Register the function with the registry immediately
        try:
            registry = AgentRegistry()
            registry.register_decorated_function(agent_name, func, metadata)
        except Exception as e:
            discovery_logger.error(f"Failed to register decorated function {agent_name}: {e}")

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """Wrapper that preserves the original function behavior."""
            return func(*args, **kwargs)

        # Type-safe way to add metadata
        # We use setattr to avoid type checker issues
        setattr(wrapper, '_agent_registry_id', registry_id)
        setattr(wrapper, '_is_agent_factory', True)

        return wrapper

    return decorator


def is_agent_factory(func: Callable[..., Any]) -> bool:
    """
    Check if a function is marked as an agent factory.

    Args:
        func: Function to check

    Returns:
        True if function is decorated with @register_agent
    """
    return hasattr(func, '_is_agent_factory') and getattr(func, '_is_agent_factory', False)


def get_agent_name(func: Callable[..., Any]) -> Optional[str]:
    """
    Get the agent name from a decorated function.

    Args:
        func: Decorated function

    Returns:
        Agent name if function is decorated, None otherwise
    """
    registry_id = getattr(func, '_agent_registry_id', None)
    if registry_id is None:
        return None
    return _decorator_name_registry.get(registry_id)


def get_agent_metadata(func: Callable[..., Any]) -> Optional[AgentMetadata]:
    """
    Get the agent metadata from a decorated function.

    Args:
        func: Decorated function

    Returns:
        AgentMetadata if function is decorated, None otherwise
    """
    registry_id = getattr(func, '_agent_registry_id', None)
    if registry_id is None:
        return None
    return _decorator_metadata_registry.get(registry_id)


def clear_decorator_registry() -> None:
    """
    Clear the decorator metadata registry.

    This is primarily for testing purposes.
    """
    _decorator_metadata_registry.clear()
    _decorator_name_registry.clear()
    discovery_logger.debug("Cleared decorator metadata registry")