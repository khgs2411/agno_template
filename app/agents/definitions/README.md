# Agent Discovery Patterns Examples

This folder contains examples of all three agent discovery patterns using the Documentation Agent as an example.

## Files Overview

1. **`docs_agent_decorator.py`** - Decorator Pattern (Priority 1)
2. **`docs_agent_convention.py`** - Convention Pattern (Priority 2)
3. **`docs_agent_configuration.py`** - Configuration Pattern (Priority 3)

## Pattern Comparison

### 1. Decorator Pattern (`@register_agent`) - **RECOMMENDED**

**File**: `docs_agent_decorator.py`
**Priority**: Highest (1)
**Best for**: Modern agent development

```python
@register_agent(tags=["core"], priority=100, enabled=True)
def create_docs_agent_decorator():
    return AgentBuilder("My Agent").with_model("openai").build()
```

**Advantages**:
- ✅ Clean, modern syntax
- ✅ Metadata defined at function level
- ✅ Type-safe with our implementation
- ✅ Supports multiple agents per file
- ✅ Immediate registration during import

### 2. Convention Pattern (`*_agent.py` files)

**File**: `docs_agent_convention.py`
**Priority**: Medium (2)
**Best for**: Simple agents, backward compatibility

```python
# Module variables for metadata
AGENT_TAGS = ["core", "docs"]
AGENT_PRIORITY = 80
AGENT_ENABLED = True

def create_agent():  # or 'agent' variable
    return AgentBuilder("My Agent").with_model("openai").build()
```

**Advantages**:
- ✅ No decorator import needed
- ✅ Clear file naming convention
- ✅ Module-level metadata
- ✅ Supports both factory function and instance

### 3. Configuration Pattern (`AGENT_CONFIG`)

**File**: `docs_agent_configuration.py`
**Priority**: Lowest (3)
**Best for**: Configuration-driven setups

```python
def create_my_agent():
    return AgentBuilder("My Agent").with_model("openai").build()

AGENT_CONFIG = {
    "name": "MyAgent",
    "factory": "create_my_agent",
    "tags": ["core"],
    "priority": 60,
    "enabled": True
}
```

**Advantages**:
- ✅ All metadata in one place
- ✅ JSON-like configuration
- ✅ Easy to generate programmatically
- ✅ Supports custom factory function names

## Discovery Priority

When multiple patterns define the same agent name, priority is:

1. **Decorator** (highest) - wins over others
2. **Convention** (medium) - wins over configuration
3. **Configuration** (lowest) - used if no higher priority found

## Usage with AgentBuilder + Dynamic Config

All examples now use the improved AgentBuilder with dynamic config validation:

```python
agent = (AgentBuilder("My Agent")
         .with_model("openai")
         .with_db()
         .with_memory()
         .with_mcp("docs")
         .with_instructions("You are helpful.")
         .with_config(
             add_history_to_context=True,  # Valid Agent param
             num_history_sessions=5,       # Valid Agent param
             markdown=True,                # Valid Agent param
             user_id="1"                   # Valid Agent param
             # invalid_param="test"        # Would raise ValueError!
         )
         .build())
```

The `with_config()` method now validates against the actual Agno Agent constructor parameters automatically!

## Testing the Examples

To test these patterns:

1. **Run discovery**:
   ```python
   from app.agents import AgentManager
   AgentManager.discover()
   ```

2. **List discovered agents**:
   ```python
   agents = AgentManager.get_all()
   for agent in agents:
       print(f"{agent.name} - {agent.metadata.pattern.name}")
   ```

3. **Filter by pattern**:
   ```python
   decorator_agents = AgentManager.get_by_pattern("DECORATOR")
   convention_agents = AgentManager.get_by_pattern("CONVENTION")
   config_agents = AgentManager.get_by_pattern("CONFIGURATION")
   ```

4. **Create agent instances**:
   ```python
   # Create all enabled agents
   agents = AgentManager.create_enabled_agents()

   # Create specific agent
   agent = AgentManager.create_agent("DocsAgentDecorator")
   ```