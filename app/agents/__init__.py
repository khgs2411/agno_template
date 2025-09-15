"""
Agent Discovery System - Simplified Public API.

This module provides the simplified interface for the agent discovery system.
External code should import from this module to access agent functionality.

Main exports:
- AgentRegistry: Direct registry access for discovery and creation
- AgentBuilder: Fluent API for creating agents
- register_agent: Decorator for automatic agent discovery

Usage:
    from app.agents import AgentRegistry, AgentBuilder, register_agent

    # Discover and create all agents (simplified)
    agents = AgentRegistry.discover_and_create_all()

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

# Core simplified API
from .registry import AgentRegistry
from .builder import AgentBuilder
from .decorators import register_agent

# Base types that might be useful for type annotations
from .base import (
    AgentDefinition,
    AgentMetadata,
    AgentFilter,
    DiscoveryPattern
)

# Version info
__version__ = "2.0.0"  # Bumped for simplified API

# Public API
__all__ = [
    # Primary simplified API
    "AgentRegistry",
    "AgentBuilder",
    "register_agent",

    # Types for annotations
    "AgentDefinition",
    "AgentMetadata",
    "AgentFilter",
    "DiscoveryPattern",

    # Metadata
    "__version__"
]

# Simplified convenience function
def discover_and_create_all():
    """Discover and create all enabled agents. Main convenience function."""
    return AgentRegistry.discover_and_create_all()