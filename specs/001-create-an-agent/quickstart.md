# Agent Discovery System - Quickstart Guide

## Overview
This quickstart demonstrates the Agent Discovery System by creating and discovering agents using all three discovery patterns.

## Prerequisites
- Agno template project running
- Python 3.10+ environment
- Access to app/agents/ directory

## Quick Start Steps

### Step 1: Verify Current Setup
```bash
# Start the application
python main.py

# Check current agents (before discovery system)
# Should see existing docs_agent
```

### Step 2: Create Discovery Folder Structure
```bash
# Create the agent definitions folder
mkdir -p app/agents/definitions

# Verify the structure
ls -la app/agents/
```

### Step 3: Create Your First Agent (Convention Pattern)

Create `app/agents/definitions/hello_agent.py`:
```python
from app.agents import AgentBuilder

def create_agent():
    return (
        AgentBuilder("Hello Agent")
        .with_model("openai")
        .with_instructions("You are a friendly greeting agent")
        .build()
    )

# Metadata
AGENT_TAGS = ["demo", "greeting"]
AGENT_PRIORITY = 50
AGENT_ENABLED = True
```

### Step 4: Create a Decorator-Based Agent

Create `app/agents/definitions/welcome.py`:
```python
from app.agents import AgentBuilder, register_agent

@register_agent(tags=["demo", "welcome"], priority=100)
def create_welcome_agent():
    return (
        AgentBuilder("Welcome Agent")
        .with_model("gemini")
        .with_instructions("You welcome new users warmly")
        .with_metadata(tags=["priority", "onboarding"])
        .build()
    )
```

### Step 5: Create a Configuration-Based Agent

Create `app/agents/definitions/utility.py`:
```python
from app.agents import AgentBuilder

AGENT_CONFIG = {
    "name": "Utility Agent",
    "factory": lambda: (
        AgentBuilder("Utility Agent")
        .with_model("openai")
        .with_instructions("You help with various utility tasks")
        .build()
    ),
    "metadata": {
        "tags": ["utility", "helper"],
        "priority": 25,
        "enabled": True
    }
}
```

### Step 6: Test Discovery

```python
# In Python shell or test file
from app.agents import AgentManager

# Discover agents
count = AgentManager.discover()
print(f"Discovered {count} agents")

# List all agents
agents = AgentManager.get_all()
for agent_def in agents:
    print(f"- {agent_def.name} (pattern: {agent_def.metadata.pattern.name})")

# Get enabled agents (for AgentOS)
enabled = AgentManager.get_enabled()
print(f"Enabled agents: {[a.name for a in enabled]}")
```

### Step 7: Filter and Manage Agents

```python
# Filter by tags
demo_agents = AgentManager.get_by_tags(["demo"])
print(f"Demo agents: {[a.name for a in demo_agents]}")

# Filter by pattern
decorated_agents = AgentManager.get_by_pattern("DECORATOR")
print(f"Decorated agents: {[a.name for a in decorated_agents]}")

# Manage agent state
AgentManager.disable("utility_agent")
AgentManager.enable("hello_agent")

# Get only enabled agents
enabled = AgentManager.get_enabled()
```

### Step 8: Create Agent Instances

```python
# Create specific agent
hello_agent = AgentManager.create_agent("hello_agent")
if hello_agent:
    response = hello_agent.run("Say hello!")
    print(response.content)

# Create all enabled agents (for AgentOS integration)
all_agents = AgentManager.create_enabled_agents()
print(f"Created {len(all_agents)} agent instances")
```

### Step 9: Integrate with AgentOS

Update `app/server.py`:
```python
from app.agents import AgentManager

class Server:
    def __init__(self):
        # Discover agents automatically
        count = AgentManager.discover()
        logger.info(f"Discovered {count} agents")

        # Get enabled agents for AgentOS
        agents = AgentManager.create_enabled_agents()

        self.agent_os = AgentOS(
            os_id="agno-discovery-demo",
            description="Agent Discovery System Demo",
            agents=agents,  # Auto-discovered agents
        )
```

### Step 10: Test Hot Reload (Development)

```bash
# With the server running in development mode
# Add a new agent file while server is running

# Create app/agents/definitions/test_agent.py
echo 'from app.agents import AgentBuilder

def create_agent():
    return AgentBuilder("Test Agent").with_model("openai").build()

AGENT_TAGS = ["test"]
' > app/agents/definitions/test_agent.py

# Refresh discovery
# In Python shell:
# AgentManager.refresh()
```

## Validation Steps

### Test 1: Discovery Works
```python
# Should find all three agents
agents = AgentManager.get_all()
assert len(agents) >= 3
assert any(a.name == "Hello Agent" for a in agents)
assert any(a.name == "Welcome Agent" for a in agents)
assert any(a.name == "Utility Agent" for a in agents)
```

### Test 2: Priority Resolution
```python
# Decorator pattern should have highest priority
welcome = AgentManager.get("Welcome Agent")
assert welcome.metadata.pattern.name == "DECORATOR"

# Check priority ordering
agents = sorted(AgentManager.get_all(), key=lambda a: (a.metadata.pattern.value, -a.metadata.priority))
print("Discovery order:", [f"{a.name} ({a.metadata.pattern.name})" for a in agents])
```

### Test 3: Filtering Works
```python
# Tag filtering
demo_agents = AgentManager.get_by_tags(["demo"])
assert len(demo_agents) >= 2

# Pattern filtering
decorated = AgentManager.get_by_pattern("DECORATOR")
convention = AgentManager.get_by_pattern("CONVENTION")
config = AgentManager.get_by_pattern("CONFIGURATION")

print(f"Patterns: {len(decorated)} decorated, {len(convention)} convention, {len(config)} config")
```

### Test 4: Agent Creation
```python
# Create and test agent
agent = AgentManager.create_agent("Hello Agent")
assert agent is not None
assert agent.name == "Hello Agent"

# Test agent functionality
response = agent.run("Hello there!")
assert response is not None
```

### Test 5: AgentOS Integration
```python
# Test AgentOS integration
from app.server import Server

server = Server()
assert server.agent_os is not None
assert len(server.agent_os.agents) > 0
```

## Container Testing

### Docker Restart Test
```bash
# Build and start container
docker-compose -f docker/docker-compose.yml up --build

# Check logs for discovery output
docker-compose -f docker/docker-compose.yml logs app

# Should see:
# - "Discovered X agents"
# - Agent names and patterns logged
# - No discovery errors
# - AgentOS starts successfully
```

### Validation in Container
```bash
# Exec into running container
docker-compose -f docker/docker-compose.yml exec app python

# Run validation in container
>>> from app.agents import AgentManager
>>> count = AgentManager.discover()
>>> print(f"Container discovered {count} agents")
>>> agents = AgentManager.get_all()
>>> for a in agents:
...     print(f"- {a.name} ({a.metadata.pattern.name})")
```

## Troubleshooting

### Common Issues

1. **No agents discovered**
   - Check discovery paths are correct
   - Verify agent files have correct syntax
   - Check log output for import errors

2. **Agent creation fails**
   - Verify model configuration
   - Check database connections
   - Validate MCP tool availability

3. **Hot reload not working**
   - Check file modification detection
   - Verify module reload functionality
   - Look for circular import issues

### Debug Commands
```python
# Enable debug logging
import logging
logging.getLogger('app.agents').setLevel(logging.DEBUG)

# Check discovery paths
from app.agents.registry import AgentRegistry
registry = AgentRegistry()
print(f"Discovery paths: {registry._discovery_paths}")

# Validate specific agent
definition = AgentManager.get("Hello Agent")
if definition:
    errors = registry.validate_agent_definition(definition)
    print(f"Validation errors: {errors}")
```

## Success Criteria

After completing this quickstart:

✅ Agent discovery system finds agents using all three patterns
✅ Priority resolution works correctly (decorator > convention > configuration)
✅ Agent filtering by tags and patterns works
✅ Agent instances can be created and used
✅ AgentOS integration works with discovered agents
✅ Container restart shows successful discovery
✅ Hot reload works in development mode (optional)
✅ Error handling gracefully handles malformed agents

## Next Steps

- Add more sophisticated agents with complex configurations
- Implement custom discovery patterns
- Add agent dependency resolution
- Create agent templates for common patterns
- Set up monitoring and metrics for agent discovery