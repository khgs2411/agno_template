"""
Documentation Agent - Migrated to Agent Discovery System.

This agent provides documentation and help functionality using the new AgentBuilder pattern.
Migrated from the original app/agents/docs_agent.py to use the discovery system.
"""

from app.agents import AgentBuilder, register_agent

# Agent metadata for convention-based discovery
AGENT_TAGS = ["core", "documentation", "help"]
AGENT_PRIORITY = 75
AGENT_ENABLED = True
AGENT_DEPENDENCIES = []


@register_agent(
    tags=["core", "documentation", "help"],
    priority=75,
    enabled=True  # Enabled for simplified discovery system
)
def create_docs_agent():
    """
    Create the documentation agent using AgentBuilder.

    This is the modern way to create agents using the discovery system.
    The agent provides the same functionality as the original docs_agent
    but uses the new builder pattern for consistency.
    """
    return (AgentBuilder("Agno Documentation Agent")
            .with_model("openai")  # Use default OpenAI model
            .with_db()  # Use default PostgreSQL configuration
            .with_memory()  # Add memory tools with Mem0 if available
            .with_mcp("docs")  # Add docs MCP tool
            .with_instructions("Your name is Joker")
            .with_config(
                add_history_to_context=True,
                num_history_sessions=5,
                num_history_runs=20,
                enable_session_summaries=True,
                markdown=True,
                id="agno_doc_agent",
                user_id="1",
                session_id="user_1_session"
            )
            .build())


# Provide the agent instance for backward compatibility
# This supports both convention-based discovery and direct imports
agent = None

def create_agent():
    """Factory function for convention-based discovery."""
    global agent
    if agent is None:
        agent = create_docs_agent()
    return agent


# Initialize agent instance for backward compatibility
try:
    agent = create_docs_agent()
except Exception as e:
    # If agent creation fails, log it but don't break import
    from app.utils.log import logger
    logger.warning(f"Failed to initialize docs agent: {e}")
    agent = None