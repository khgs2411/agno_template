"""
Documentation Agent - Convention Pattern Example.

This demonstrates MEDIUM PRIORITY discovery pattern using file naming convention.
Files ending with '_agent.py' are automatically discovered and scanned for:
1. 'agent' variable containing an Agent instance
2. 'create_agent()' function returning an Agent instance

Metadata is provided via module variables.
"""

from app.agents import AgentBuilder

# Agent metadata for convention-based discovery
AGENT_TAGS = ["example", "documentation", "convention-pattern"]
AGENT_PRIORITY = 80  # Medium priority
AGENT_ENABLED = False  # Disabled to avoid conflicts with decorator example
AGENT_DEPENDENCIES = []
AGENT_CUSTOM_ATTRIBUTES = {
    "pattern_type": "convention",
    "example": True,
    "version": "1.0"
}


def create_agent():
    """
    Factory function for convention-based discovery.

    The discovery system looks for this function in *_agent.py files.
    This is the standard way to create agents using convention pattern.
    """
    return (AgentBuilder("Docs Agent (Convention)")
            .with_model("openai")
            .with_db()
            .with_memory()
            .with_mcp("docs")
            .with_instructions("You are a documentation assistant created via convention pattern.")
            .with_config(
                add_history_to_context=True,
                num_history_sessions=5,
                num_history_runs=20,
                enable_session_summaries=True,
                markdown=True,
                id="docs_agent_convention",
                user_id="1",
                session_id="convention_session"
            )
            .build())


# Alternative: provide agent instance directly
# The discovery system also looks for 'agent' variable
# Uncomment this if you want to provide instance instead of factory:

# agent = create_agent()

# Note: Using factory function is preferred for lazy loading