"""
Agent Discovery System - Public API exports.

This module provides the public interface for the agent discovery system.
External code should import from this module to access agent functionality.

Main exports:
- AgentManager: Primary facade for agent operations
- AgentBuilder: Fluent API for creating agents
- register_agent: Decorator for automatic agent discovery

Usage:
    from app.agents import AgentManager, AgentBuilder, register_agent

    # Discover agents
    AgentManager.discover()

    # Create agent programmatically
    agent = (AgentBuilder("My Agent")
             .with_model("openai")
             .with_mcp("docs")
             .build())

    # Register agent with decorator
    @register_agent(tags=["core"])
    def create_example_agent():
        return AgentBuilder("Example").with_model("openai").build()
"""

# Core public API
from .manager import AgentManager
from .builder import AgentBuilder
from .decorators import register_agent

# Base types that might be useful for type annotations
from .base import (
    AgentDefinition,
    AgentMetadata,
    AgentFilter,
    DiscoveryPattern
)

# Registry access (for advanced use cases)
from .registry import AgentRegistry

# Version info
__version__ = "1.0.0"

# Public API
__all__ = [
    # Primary API
    "AgentManager",
    "AgentBuilder",
    "register_agent",

    # Types for annotations
    "AgentDefinition",
    "AgentMetadata",
    "AgentFilter",
    "DiscoveryPattern",

    # Advanced API
    "AgentRegistry",

    # Metadata
    "__version__"
]

# Note: Discovery is performed explicitly by the application
# No auto-discovery on import to avoid duplicate discoveries

# Convenience functions
def get_all_agents():
    """Get all discovered agents. Convenience function."""
    return AgentManager.get_all()

def get_enabled_agents():
    """Get all enabled agents. Convenience function."""
    return AgentManager.get_enabled()

def create_all_enabled_agents():
    """Create instances of all enabled agents. Convenience function."""
    return AgentManager.create_enabled_agents()

# Add convenience functions to __all__
__all__.extend([
    "get_all_agents",
    "get_enabled_agents",
    "create_all_enabled_agents"
])