"""
Discovery Patterns Contract

Defines the expected behavior for each discovery pattern.
This contract specifies how agents are discovered and registered.
"""

from typing import Callable, Dict, Any, List, Optional
from agno.agent import Agent


class DecoratorPatternContract:
    """
    Contract for decorator-based agent discovery.

    Agents are registered using the @register_agent decorator.
    This is the highest priority discovery pattern.
    """

    def register_agent(self,
                      tags: Optional[List[str]] = None,
                      priority: int = 50,
                      enabled: bool = True,
                      dependencies: Optional[List[str]] = None,
                      **custom_attributes) -> Callable:
        """
        Decorator to register agent factory functions.

        Args:
            tags: Agent tags for categorization
            priority: Agent priority (higher numbers = higher priority)
            enabled: Whether agent is enabled by default
            dependencies: List of required dependencies
            **custom_attributes: Custom metadata attributes

        Returns:
            Decorator function

        Usage:
            @register_agent(tags=["core"], priority=100)
            def create_my_agent():
                return AgentBuilder("My Agent").with_model("openai").build()
        """
        ...

    def discovery_behavior(self):
        """
        Expected behavior for decorator pattern discovery:

        1. Import all Python modules in discovery paths
        2. Find functions decorated with @register_agent
        3. Register the decorator metadata immediately during import
        4. Store factory function for lazy agent creation
        5. Priority: DECORATOR (1) - highest priority

        Registration happens during module import, not during discovery scan.
        """
        pass


class ConventionPatternContract:
    """
    Contract for convention-based agent discovery.

    Agents are discovered by file naming convention (*_agent.py).
    This is medium priority discovery pattern.
    """

    def discovery_behavior(self):
        """
        Expected behavior for convention pattern discovery:

        1. Scan discovery paths for files matching "*_agent.py"
        2. Import each matching module
        3. Look for:
           - 'agent' variable containing Agent instance, OR
           - 'create_agent()' function returning Agent instance
        4. Extract metadata from module variables:
           - AGENT_TAGS: List[str]
           - AGENT_PRIORITY: int (default: 50)
           - AGENT_ENABLED: bool (default: True)
           - AGENT_DEPENDENCIES: List[str] (default: [])
        5. Priority: CONVENTION (2) - medium priority

        File naming examples:
        - customer_support_agent.py
        - docs_agent.py
        - research_agent.py
        """
        pass

    def module_structure_examples(self):
        """
        Expected module structure for convention-based discovery.
        """

        # Example 1: Direct agent instance
        example_1 = """
        # File: docs_agent.py
        from app.agents import AgentBuilder

        # Agent instance
        agent = (
            AgentBuilder("Documentation Agent")
            .with_model("openai")
            .with_mcp("docs")
            .build()
        )

        # Optional metadata
        AGENT_TAGS = ["documentation", "core"]
        AGENT_PRIORITY = 100
        AGENT_ENABLED = True
        """

        # Example 2: Factory function
        example_2 = """
        # File: support_agent.py
        from app.agents import AgentBuilder

        def create_agent():
            return (
                AgentBuilder("Support Agent")
                .with_model("openai")
                .with_mcp("support")
                .build()
            )

        # Metadata
        AGENT_TAGS = ["support", "production"]
        AGENT_PRIORITY = 90
        AGENT_ENABLED = True
        AGENT_DEPENDENCIES = ["database"]
        """

        return [example_1, example_2]


class ConfigurationPatternContract:
    """
    Contract for configuration-based agent discovery.

    Agents are discovered by AGENT_CONFIG exports.
    This is the lowest priority discovery pattern.
    """

    def discovery_behavior(self):
        """
        Expected behavior for configuration pattern discovery:

        1. Scan all Python files in discovery paths (except *_agent.py)
        2. Import each module
        3. Look for AGENT_CONFIG dictionary export
        4. Validate AGENT_CONFIG structure
        5. Extract factory function and metadata
        6. Priority: CONFIGURATION (3) - lowest priority

        AGENT_CONFIG structure:
        {
            "name": str,              # Required: Agent name
            "factory": Callable,      # Required: Function returning Agent
            "metadata": {             # Optional: Discovery metadata
                "tags": List[str],
                "priority": int,
                "enabled": bool,
                "dependencies": List[str],
                "custom_attributes": Dict[str, Any]
            }
        }
        """
        pass

    def config_structure_examples(self):
        """
        Expected AGENT_CONFIG structure examples.
        """

        # Example 1: Basic configuration
        example_1 = """
        # File: research_tools.py
        from app.agents import AgentBuilder

        def create_research_agent():
            return (
                AgentBuilder("Research Agent")
                .with_model("gemini")
                .with_mcp("search", "docs")
                .build()
            )

        AGENT_CONFIG = {
            "name": "Research Agent",
            "factory": create_research_agent,
            "metadata": {
                "tags": ["research", "experimental"],
                "priority": 75,
                "enabled": True
            }
        }
        """

        # Example 2: Lambda factory
        example_2 = """
        # File: utils.py
        from app.agents import AgentBuilder

        AGENT_CONFIG = {
            "name": "Utility Agent",
            "factory": lambda: (
                AgentBuilder("Utility Agent")
                .with_model("openai")
                .build()
            ),
            "metadata": {
                "tags": ["utility"],
                "priority": 25,
                "enabled": False,
                "team": "engineering"
            }
        }
        """

        # Example 3: Minimal configuration
        example_3 = """
        # File: simple.py
        AGENT_CONFIG = {
            "name": "Simple Agent",
            "factory": lambda: Agent(name="Simple", model=None)
        }
        """

        return [example_1, example_2, example_3]


class DiscoveryPriorityContract:
    """
    Contract for discovery pattern priority resolution.

    When multiple patterns define the same agent name,
    priority determines which definition is used.
    """

    def priority_resolution(self):
        """
        Priority resolution rules:

        1. DECORATOR (priority 1) beats CONVENTION (priority 2)
        2. CONVENTION (priority 2) beats CONFIGURATION (priority 3)
        3. Within same pattern, higher priority number wins
        4. Within same pattern and priority, first discovered wins

        Examples:
        - @register_agent(priority=100) beats convention_agent.py with AGENT_PRIORITY=200
        - convention_agent.py with AGENT_PRIORITY=100 beats AGENT_CONFIG with priority=200
        - @register_agent(priority=100) beats @register_agent(priority=50)
        """
        pass

    def conflict_resolution_examples(self):
        """
        Examples of how naming conflicts are resolved.
        """

        # Example: Multiple definitions of "docs_agent"
        conflict_example = """
        # File 1: decorators.py
        @register_agent(priority=100)  # WINS - decorator pattern
        def docs_agent():
            return AgentBuilder("Docs v1").build()

        # File 2: docs_agent.py
        AGENT_PRIORITY = 200  # LOSES - convention pattern, lower precedence
        def create_agent():
            return AgentBuilder("Docs v2").build()

        # File 3: config.py
        AGENT_CONFIG = {  # LOSES - configuration pattern, lowest precedence
            "name": "docs_agent",
            "factory": lambda: AgentBuilder("Docs v3").build(),
            "metadata": {"priority": 300}
        }

        # Result: "Docs v1" from decorator pattern is used
        """

        return conflict_example


class DiscoveryValidationContract:
    """
    Contract for agent definition validation during discovery.
    """

    def validation_rules(self):
        """
        Validation rules applied during discovery:

        1. Agent name must be non-empty string
        2. Factory function must be callable
        3. Factory function must take no required arguments
        4. Factory function must return Agent instance (validated on first call)
        5. Metadata must conform to expected structure
        6. Tags must be list of strings
        7. Priority must be non-negative integer
        8. Dependencies must be list of strings

        Validation failures:
        - Log error with file path and reason
        - Skip the invalid agent definition
        - Continue discovery process
        """
        pass

    def error_handling_examples(self):
        """
        Examples of validation error handling.
        """

        # Example 1: Invalid factory function
        invalid_factory = """
        # File: broken_agent.py
        def create_agent(required_param):  # ERROR: requires parameter
            return AgentBuilder("Broken").build()

        # Result: Skip this agent, log error
        """

        # Example 2: Invalid metadata
        invalid_metadata = """
        # File: bad_metadata.py
        AGENT_CONFIG = {
            "name": "",  # ERROR: empty name
            "factory": lambda: None,  # ERROR: returns None
            "metadata": {
                "tags": "not a list",  # ERROR: tags must be list
                "priority": -1  # ERROR: negative priority
            }
        }

        # Result: Skip this agent, log validation errors
        """

        return [invalid_factory, invalid_metadata]