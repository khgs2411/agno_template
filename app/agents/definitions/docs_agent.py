"""
Documentation Agent - Migrated to Agent Discovery System.

This agent provides documentation and help functionality using the new AgentBuilder pattern.
Migrated from the original app/agents/docs_agent.py to use the discovery system.
"""

from app.agents import AgentBuilder, register_agent


@register_agent(
    tags=["core", "documentation", "help"],
    priority=75,
    enabled=True,  # Enabled for simplified discovery system
)
def create_docs_agent():
    """
    Create the documentation agent using AgentBuilder.

    This is the modern way to create agents using the discovery system.
    The agent provides the same functionality as the original docs_agent
    but uses the new builder pattern for consistency.
    """
    return (
        AgentBuilder("Agno Documentation Agent")
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
            session_id="user_1_session",
        )
        .build()
    )


# Note: No immediate agent creation - agents are created only during discovery
# This prevents duplicate agent creation during module import
