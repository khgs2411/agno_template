"""
Agent Builder API Contract

Defines the fluent API interface for the AgentBuilder class.
This contract specifies the expected method chaining behavior.
"""

from typing import List, Dict, Any, Optional, Union, Callable
from agno.agent import Agent

# Import types that will be defined in implementation
from typing import Protocol, runtime_checkable


@runtime_checkable
class AgentBuilderProtocol(Protocol):
    """Protocol for AgentBuilder fluent API."""

    def with_model(self, provider: Union[str, Any], model_id: Optional[str] = None, **kwargs) -> 'AgentBuilderProtocol':
        """
        Configure the model for the agent.

        Args:
            provider: Model provider (e.g., "openai", ModelFactory.providers().OPENAI)
            model_id: Specific model ID (optional, uses provider default if not specified)
            **kwargs: Additional model configuration parameters

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_model("openai")
            .with_model("openai", "gpt-4")
            .with_model(ModelFactory.providers().GEMINI, temperature=0.7)
        """
        ...

    def with_mcp(self, *tools: str) -> 'AgentBuilderProtocol':
        """
        Add MCP tools to the agent.

        Args:
            *tools: MCP tool names to add

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_mcp("docs")
            .with_mcp("docs", "search", "memory")
        """
        ...

    def with_memory(self, **config) -> 'AgentBuilderProtocol':
        """
        Add memory tools to the agent.

        Args:
            **config: Memory configuration options

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_memory()
            .with_memory(session_summaries=True)
        """
        ...

    def with_db(self, db_config: Optional[Union[str, Dict[str, Any]]] = None) -> 'AgentBuilderProtocol':
        """
        Configure database for the agent.

        Args:
            db_config: Database configuration (defaults to PostgresSettings if None)

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_db()  # Use default PostgresSettings
            .with_db("postgres")
            .with_db({"url": "postgresql://..."})
        """
        ...

    def with_vector_db(self, table_name: str = "embeddings", **config) -> 'AgentBuilderProtocol':
        """
        Configure vector database for the agent.

        Args:
            table_name: Vector table name
            **config: Vector database configuration

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_vector_db()
            .with_vector_db("agent_embeddings")
        """
        ...

    def with_tools(self, tools: List[Any]) -> 'AgentBuilderProtocol':
        """
        Add custom tools to the agent.

        Args:
            tools: List of tool instances

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_tools([EmailTools(), SlackTools()])
        """
        ...

    def with_instructions(self, instructions: Union[str, List[str]]) -> 'AgentBuilderProtocol':
        """
        Set agent instructions.

        Args:
            instructions: Instruction text or list of instructions

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_instructions("You are a helpful assistant")
            .with_instructions(["Be helpful", "Be concise"])
        """
        ...

    def with_knowledge_base(self, urls: Optional[List[str]] = None, **config) -> 'AgentBuilderProtocol':
        """
        Configure knowledge base for the agent.

        Args:
            urls: URLs to load into knowledge base
            **config: Knowledge base configuration

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_knowledge_base(urls=["https://docs.example.com"])
        """
        ...

    def with_metadata(self, tags: Optional[List[str]] = None, priority: int = 50,
                     enabled: bool = True, dependencies: Optional[List[str]] = None,
                     **custom_attributes) -> 'AgentBuilderProtocol':
        """
        Set discovery metadata for the agent.

        Args:
            tags: Agent tags for categorization
            priority: Agent priority (default: 50)
            enabled: Whether agent is enabled (default: True)
            dependencies: List of required dependencies
            **custom_attributes: Custom metadata attributes

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_metadata(tags=["production", "support"], priority=100)
            .with_metadata(tags=["debug"], enabled=False, team="engineering")
        """
        ...

    def with_config(self, **config) -> 'AgentBuilderProtocol':
        """
        Set additional agent configuration options.

        Args:
            **config: Agent configuration parameters

        Returns:
            AgentBuilder instance for method chaining

        Examples:
            .with_config(markdown=True, add_history_to_context=True)
            .with_config(num_history_sessions=5, enable_session_summaries=True)
        """
        ...

    def build(self) -> Agent:
        """
        Build and return the configured Agent instance.

        Returns:
            Configured Agent instance

        Raises:
            ValueError: If required configuration is missing
            RuntimeError: If agent creation fails
        """
        ...


class AgentBuilderContract:
    """
    Contract for AgentBuilder constructor and factory methods.
    """

    def __init__(self, name: str, agent_id: Optional[str] = None) -> None:
        """
        Initialize a new AgentBuilder.

        Args:
            name: Agent name (required)
            agent_id: Unique agent ID (optional, defaults to name)
        """
        ...

    @classmethod
    def create(cls, name: str, agent_id: Optional[str] = None) -> AgentBuilderProtocol:
        """
        Factory method to create a new AgentBuilder.

        Args:
            name: Agent name (required)
            agent_id: Unique agent ID (optional, defaults to name)

        Returns:
            AgentBuilder instance ready for configuration
        """
        ...


# Expected usage patterns for validation
class BuilderUsageExamples:
    """Examples of expected AgentBuilder usage patterns."""

    def simple_agent(self):
        """Simple agent with minimal configuration."""
        agent = (
            AgentBuilderContract.create("Simple Agent")
            .with_model("openai")
            .build()
        )
        return agent

    def production_agent(self):
        """Production agent with full configuration."""
        agent = (
            AgentBuilderContract.create("Customer Support Agent")
            .with_model("openai", "gpt-4", temperature=0.7)
            .with_mcp("docs", "search")
            .with_memory()
            .with_db()
            .with_vector_db("support_embeddings")
            .with_tools([])  # Custom tools would go here
            .with_instructions("You are a helpful customer support agent")
            .with_metadata(
                tags=["support", "production"],
                priority=100,
                enabled=True
            )
            .with_config(
                markdown=True,
                add_history_to_context=True,
                num_history_sessions=5
            )
            .build()
        )
        return agent

    def development_agent(self):
        """Development agent with debug configuration."""
        agent = (
            AgentBuilderContract.create("Debug Agent")
            .with_model("gemini")
            .with_memory()
            .with_instructions("Debug mode agent")
            .with_metadata(
                tags=["debug", "development"],
                priority=10,
                enabled=False,
                team="engineering"
            )
            .build()
        )
        return agent

    def decorator_pattern(self):
        """Usage pattern for decorator-based registration."""
        from app.agents import register_agent

        @register_agent(tags=["core"], priority=100)
        def create_core_agent():
            return (
                AgentBuilderContract.create("Core Agent")
                .with_model("openai")
                .with_mcp("docs")
                .with_memory()
                .build()
            )

        return create_core_agent

    def convention_pattern(self):
        """Usage pattern for convention-based discovery."""
        # File: customer_support_agent.py

        def create_agent():
            return (
                AgentBuilderContract.create("Customer Support")
                .with_model("openai")
                .with_mcp("support")
                .build()
            )

        # Agent tags and metadata
        AGENT_TAGS = ["support", "production"]
        AGENT_PRIORITY = 100
        AGENT_ENABLED = True

    def configuration_pattern(self):
        """Usage pattern for configuration-based discovery."""
        # File: research_agent.py

        AGENT_CONFIG = {
            "name": "Research Agent",
            "factory": lambda: (
                AgentBuilderContract.create("Research Agent")
                .with_model("gemini")
                .with_mcp("search", "docs")
                .with_memory()
                .build()
            ),
            "metadata": {
                "tags": ["research", "experimental"],
                "priority": 75,
                "enabled": True,
                "team": "research"
            }
        }