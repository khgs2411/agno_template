# Agent Discovery System - Technical Plan

## Overview

This document outlines the technical implementation plan for an automatic agent discovery system for the Agno template project.

## Architecture Design

### Folder Structure

```
app/agents/
├── __init__.py           # Re-exports AgentManager, register_agent, AgentBuilder
├── manager.py            # High-level AgentManager API
├── registry.py           # Agent registry and discovery logic
├── builder.py            # Fluent AgentBuilder API
├── base.py              # BaseAgent protocol/abstract class
├── decorators.py        # @register_agent decorator
│
├── definitions/         # All agent definitions (auto-discovered)
│   ├── __init__.py
│   └── docs_agent.py    # Documentation agent
│
├── tools/               # Agent-specific tools and utilities
│   ├── __init__.py
│   └── .gitkeep
│
└── templates/           # Agent templates and examples
    ├── __init__.py
    └── example_agent.py.template
```

### Key Components

#### 1. AgentBuilder (Fluent API)

```python
# Example usage
agent = (
    AgentBuilder("Customer Support Agent")
    .with_model("openai", "gpt-4o")  # or .with_model(ModelFactory.get("openai"))
    .with_mcp("docs", "search")       # Add MCP tools
    .with_memory()                    # Add memory tools
    .with_db("postgres")              # Configure database
    .with_vector_db("embeddings")     # Configure vector store
    .with_tools([EmailTools()])       # Add custom tools
    .with_instructions([...])         # Set instructions
    .with_knowledge_base(urls=[...])  # Configure knowledge
    .with_metadata(                  # Set discovery metadata
        tags=["support", "production"],
        priority=100,
        enabled=True
    )
    .build()
)
```

#### 2. Discovery Patterns (Priority Order)

1. **Decorator-based** (highest priority)

   ```python
   @register_agent(tags=["core"], priority=100)
   def create_support_agent():
       return AgentBuilder("Support").with_model("openai").build()
   ```

2. **Convention-based** (medium priority)

   - Files ending with `_agent.py` in designated folders
   - Must export an `agent` variable or `create_agent()` function

3. **Configuration-based** (lowest priority)
   ```python
   # In any Python file
   AGENT_CONFIG = {
       "name": "Research Agent",
       "factory": lambda: AgentBuilder("Research")...,
       "metadata": {"tags": ["research"], "enabled": True}
   }
   ```

#### 3. AgentManager API

```python
from app.agents import AgentManager

# Get all agents
agents = AgentManager.get_all()

# Filter agents
production_agents = AgentManager.get_by_tags(["production"])
enabled_agents = AgentManager.get_enabled()

# Get specific agent
docs_agent = AgentManager.get("docs_agent")

# Dynamic control
AgentManager.enable("experimental_agent")
AgentManager.disable("debug_agent")

# Discovery control
AgentManager.discover()  # Discover from definitions folder
AgentManager.refresh()  # Re-scan for new agents
```

#### 4. Server Integration

```python
# app/server.py
from app.agents import AgentManager

class Server:
    def __init__(self):
        # Automatic discovery on startup
        agents = AgentManager.get_enabled()

        # Or with filtering
        agents = AgentManager.get_by_tags(["production"])

        self.agent_os = AgentOS(
            os_id="my-first-os",
            description="My first AgentOS",
            agents=agents,  # Auto-discovered agents
        )
```

## Features

### Core Features

- **Zero Configuration**: Agents in `definitions/` folder are auto-discovered
- **Flexible Registration**: Support decorator, convention, and config patterns
- **Builder Pattern**: Fluent API for programmatic agent creation
- **Lazy Loading**: Agents initialized only when needed
- **Hot Reload Support**: Compatible with development mode
- **Validation**: Ensure agents meet requirements before registration

### Advanced Features

- **Metadata System**: Tags, priority, enabled/disabled state
- **Discovery Control**: Scan the definitions folder for agents
- **Agent Lifecycle**: Hooks for initialization, shutdown
- **Dependency Injection**: Agents can declare dependencies
- **Testing Support**: Mock agents for testing

## Technical Implementation

### Technology Stack
- Python 3.10+ with type hints
- importlib for dynamic module loading
- inspect module for decorator and function discovery
- Pydantic for configuration validation
- Standard library pathlib for file system operations
- Singleton pattern for AgentManager and Registry
- Factory pattern for agent creation

### Design Patterns
The implementation follows existing patterns in the codebase:
- Similar to the ModelFactory pattern in `app/models/factory.py`
- Similar to the provider registry pattern in `app/models/provider_registry.py`
- Similar to the MCP manager lazy loading in `app/tools/mcp/manager.py`

### Integration Points
- Use existing Agno Agent class without modification
- Create builder that wraps Agent construction
- Maintain existing PostgreSQL and vector database configurations
- Support existing MCP tools and memory systems

## Migration Plan

### Phase 1: Core Infrastructure
1. Create base structure and interfaces
2. Implement AgentBuilder
3. Implement Registry with basic discovery
4. Implement AgentManager

### Phase 2: Migration
1. Refactor existing `docs_agent.py` to use builder pattern
2. Move to `definitions/` folder
3. Update server.py to use AgentManager

### Phase 3: Enhanced Features
1. Add decorator support
2. Add configuration-based discovery
3. Add metadata and filtering
4. Add hot reload support

## Testing Strategy

- Unit tests for each discovery pattern
- Integration tests for AgentManager
- Mock agents for testing discovery
- Performance tests for startup time

## Documentation Requirements

- API documentation for AgentBuilder
- Discovery pattern examples
- Migration guide from manual registration
- Troubleshooting guide

## Success Criteria

1. Zero configuration required for basic usage
2. < 100ms overhead for discovery on startup
3. All existing agents continue to work
4. Clear error messages for malformed agents
5. Hot reload works in development mode