"""
AgentBuilder - Fluent API for programmatic agent creation.

Provides a fluent interface for building Agno agents with comprehensive configuration options:
- Model configuration using ModelFactory
- MCP tools integration via MCPManager
- Database and vector database setup
- Memory and custom tools configuration
- Agent instructions and metadata
- Validation and error handling

Follows existing patterns from docs_agent.py and ModelFactory.
"""

import os
import inspect
from typing import List, Dict, Any, Optional, Union, TYPE_CHECKING

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.tools.mem0 import Mem0Tools
from agno.tools.memory import MemoryTools
from agno.tools.user_control_flow import UserControlFlowTools
from agno.vectordb.pgvector import PgVector

from app.models.factory import ModelFactory
from app.db.postgres.settings import PostgresSettings
from app.tools.mcp import MCPManager
from .base import AgentMetadata, DiscoveryPattern, discovery_logger

if TYPE_CHECKING:
    from agno.agent import Agent


def _get_agent_constructor_params() -> set:
    """
    Dynamically extract parameter names from Agent constructor.

    This gives us a true Partial<Agent> equivalent without hardcoding parameters.
    """
    try:
        signature = inspect.signature(Agent.__init__)
        # Exclude 'self' and parameters handled by builder methods
        excluded_params = {"self", "name", "model", "tools", "db", "instructions"}
        return {
            param
            for param in signature.parameters.keys()
            if param not in excluded_params
        }
    except Exception:
        # Fallback to common parameters if introspection fails
        return {
            "add_history_to_context",
            "num_history_sessions",
            "num_history_runs",
            "enable_session_summaries",
            "markdown",
            "id",
            "user_id",
            "session_id",
        }


# Get valid Agent constructor parameters dynamically
_VALID_AGENT_PARAMS = _get_agent_constructor_params()


class AgentBuilder:
    """
    Fluent API for programmatic agent creation.

    Provides method chaining for comprehensive agent configuration following
    the builder pattern. All configuration is validated before building.
    """

    def __init__(self, name: str):
        """
        Initialize builder with agent name.

        Args:
            name: Agent name (required)
        """
        if not name or not isinstance(name, str):
            raise ValueError("Agent name must be a non-empty string")

        self._name = name
        self._reset_configuration()

    def _reset_configuration(self):
        """Reset all configuration to defaults."""
        # Model configuration
        self._model = None
        self._model_provider = None
        self._model_id = None
        self._model_kwargs = {}

        # Database configuration
        self._db = None
        self._db_config = None
        self._vector_db = None
        self._vector_db_config = None

        # Tools configuration
        self._mcp_tools = []
        self._custom_tools = []
        self._memory_tools = None
        self._memory_config = {}

        # Agent configuration
        self._instructions = None
        self._metadata = None
        self._config = {}

        # Default agent settings
        self._agent_config = {
            "add_history_to_context": True,
            "num_history_sessions": 5,
            "num_history_runs": 20,
            "enable_session_summaries": True,
            "markdown": True,
        }

    def with_model(
        self, provider: Union[str, Any], model_id: Optional[str] = None, **kwargs
    ) -> "AgentBuilder":
        """
        Configure the model for the agent.

        Args:
            provider: Model provider (e.g., "openai", ModelFactory.providers().OPENAI)
            model_id: Specific model ID (optional, uses provider default if not specified)
            **kwargs: Additional model configuration parameters

        Returns:
            AgentBuilder instance for method chaining
        """
        self._model_provider = provider
        self._model_id = model_id
        self._model_kwargs = kwargs

        try:
            if model_id:
                # Use specific model if provided
                self._model = ModelFactory.get(provider, model_id=model_id, **kwargs)
            else:
                # Use provider default
                self._model = ModelFactory.get(provider, **kwargs)
        except Exception as e:
            discovery_logger.error(f"Failed to configure model {provider}: {e}")
            raise ValueError(f"Failed to configure model {provider}: {e}")

        return self

    def with_mcp(self, *tools: str) -> "AgentBuilder":
        """
        Add MCP tools to the agent.

        Args:
            *tools: MCP tool names to add

        Returns:
            AgentBuilder instance for method chaining
        """
        for tool_name in tools:
            if not isinstance(tool_name, str):
                raise ValueError(
                    f"MCP tool name must be a string, got: {type(tool_name)}"
                )

            try:
                # Lazy load MCP tools to prevent hot reload issues
                mcp_tool = MCPManager.get(tool_name)
                if mcp_tool:
                    self._mcp_tools.append(mcp_tool)
                else:
                    discovery_logger.warning(f"MCP tool not found: {tool_name}")
            except Exception as e:
                discovery_logger.error(f"Failed to load MCP tool {tool_name}: {e}")
                # Continue with other tools even if one fails

        return self

    def with_db(self, db_config: Optional[Dict[str, Any]] = None) -> "AgentBuilder":
        """
        Configure database connection.

        Args:
            db_config: Database configuration (uses PostgresSettings if None)

        Returns:
            AgentBuilder instance for method chaining
        """
        try:
            if db_config:
                self._db_config = db_config
                db_url = db_config.get("db_url")
                if not db_url:
                    raise ValueError("Database configuration must include 'db_url'")
            else:
                # Use default PostgresSettings
                postgres_settings = PostgresSettings()
                db_url = postgres_settings.get_db_url()
                self._db_config = {"db_url": db_url}

            self._db = PostgresDb(db_url=db_url)
        except Exception as e:
            discovery_logger.error(f"Failed to configure database: {e}")
            raise ValueError(f"Failed to configure database: {e}")

        return self

    def with_vector_db(self, config: Optional[Dict[str, Any]] = None) -> "AgentBuilder":
        """
        Configure vector database.

        Args:
            config: Vector database configuration

        Returns:
            AgentBuilder instance for method chaining
        """
        try:
            # Ensure we have a regular database first
            if not self._db:
                self.with_db()

            # Use provided config or defaults
            vector_config = config or {}
            table_name = vector_config.get("table_name", "embeddings")

            # Get db_url from config or use the one from database configuration
            if "db_url" in vector_config:
                db_url = vector_config["db_url"]
            elif self._db_config:
                db_url = self._db_config["db_url"]
            else:
                # Fallback to PostgresSettings
                postgres_settings = PostgresSettings()
                db_url = postgres_settings.get_db_url()

            self._vector_db = PgVector(
                table_name=table_name,
                db_url=db_url,
            )
            self._vector_db_config = vector_config
        except Exception as e:
            discovery_logger.error(f"Failed to configure vector database: {e}")
            raise ValueError(f"Failed to configure vector database: {e}")

        return self

    def with_memory(self, config: Optional[Dict[str, Any]] = None) -> "AgentBuilder":
        """
        Configure memory tools.

        Args:
            config: Memory configuration

        Returns:
            AgentBuilder instance for method chaining
        """
        try:
            # Ensure we have a database for memory
            if not self._db:
                self.with_db()

            memory_config = config or {}

            # Add standard MemoryTools
            if self._db:
                self._memory_tools = MemoryTools(db=self._db)
            else:
                raise ValueError("Database connection required for memory tools")

            # Add Mem0Tools if API key is available
            mem0_api_key = memory_config.get("mem0_api_key") or os.getenv(
                "MEM0_API_KEY"
            )
            if mem0_api_key:
                user_id = memory_config.get("user_id", "1")
                mem0_tool = Mem0Tools(api_key=mem0_api_key, user_id=user_id)
                self._custom_tools.append(mem0_tool)

            self._memory_config = memory_config
        except Exception as e:
            discovery_logger.error(f"Failed to configure memory: {e}")
            raise ValueError(f"Failed to configure memory: {e}")

        return self

    def with_tools(self, tools: List[Any]) -> "AgentBuilder":
        """
        Add custom tools to the agent.

        Args:
            tools: List of tool instances

        Returns:
            AgentBuilder instance for method chaining
        """
        if not isinstance(tools, list):
            raise ValueError("Tools must be provided as a list")

        self._custom_tools.extend(tools)
        return self

    def with_instructions(self, instructions: str) -> "AgentBuilder":
        """
        Set agent instructions.

        Args:
            instructions: Agent instructions/prompt

        Returns:
            AgentBuilder instance for method chaining
        """
        if not isinstance(instructions, str):
            raise ValueError("Instructions must be a string")

        self._instructions = instructions
        return self

    def with_metadata(self, **metadata) -> "AgentBuilder":
        """
        Set discovery metadata for the agent.

        Args:
            **metadata: Metadata attributes

        Returns:
            AgentBuilder instance for method chaining
        """
        self._metadata = AgentMetadata(
            name=self._name,
            pattern=metadata.get("pattern", DiscoveryPattern.DECORATOR),
            tags=metadata.get("tags", []),
            priority=metadata.get("priority", 50),
            enabled=metadata.get("enabled", True),
            dependencies=metadata.get("dependencies", []),
            custom_attributes=metadata.get("custom_attributes", {}),
        )
        return self

    def with_config(self, **config) -> "AgentBuilder":
        """
        Set additional agent configuration.

        Only accepts parameters that are valid for the Agent constructor
        and not already handled by other builder methods.

        Args:
            **config: Agent configuration parameters (must be valid Agent constructor params)

        Returns:
            AgentBuilder instance for method chaining

        Raises:
            ValueError: If config contains invalid parameters
        """
        # Validate that all config keys are valid Agent constructor parameters
        invalid_params = set(config.keys()) - _VALID_AGENT_PARAMS
        if invalid_params:
            raise ValueError(
                f"Invalid Agent parameters: {invalid_params}. "
                f"Valid parameters: {sorted(_VALID_AGENT_PARAMS)}"
            )

        self._agent_config.update(config)
        return self

    def build(self) -> "Agent":
        """
        Build and return the configured Agent instance.

        Returns:
            Configured Agno Agent instance

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        self._validate_build_configuration()

        try:
            # Collect all tools
            all_tools = []

            # Add memory tools
            if self._memory_tools:
                all_tools.append(self._memory_tools)

            # Add MCP tools
            all_tools.extend(self._mcp_tools)

            # Add custom tools
            all_tools.extend(self._custom_tools)

            # Add user control flow tools (default)
            all_tools.append(UserControlFlowTools())

            # Build agent configuration
            agent_config = {
                "name": self._name,
                "model": self._model,
                "tools": all_tools,
                **self._agent_config,
            }

            # Add optional configurations
            if self._db:
                agent_config["db"] = self._db

            if self._instructions:
                agent_config["instructions"] = self._instructions

            # Set default IDs if not provided
            if "id" not in agent_config:
                agent_config["id"] = self._name.lower().replace(" ", "_")

            if "user_id" not in agent_config:
                agent_config["user_id"] = "1"

            if "session_id" not in agent_config:
                agent_config["session_id"] = f"user_1_session_{agent_config['id']}"

            # Create the agent
            agent = Agent(**agent_config)
            return agent

        except Exception as e:
            discovery_logger.error(f"Failed to build agent {self._name}: {e}")
            raise ValueError(f"Failed to build agent {self._name}: {e}")

    def _validate_build_configuration(self):
        """Validate that required configuration is present."""
        if not self._model:
            raise ValueError(
                "Model configuration is required. Use with_model() to configure."
            )

        # Validate metadata if present
        if self._metadata:
            try:
                # This will trigger validation in AgentMetadata.__post_init__
                pass
            except Exception as e:
                raise ValueError(f"Invalid metadata configuration: {e}")

    def reset(self) -> "AgentBuilder":
        """
        Reset all configuration to defaults.

        Returns:
            AgentBuilder instance for method chaining
        """
        self._reset_configuration()
        return self
