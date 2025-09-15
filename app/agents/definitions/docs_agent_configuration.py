"""
Documentation Agent - Configuration Pattern Example.

This demonstrates LOWEST PRIORITY discovery pattern using AGENT_CONFIG export.
Any .py file with an AGENT_CONFIG dictionary is scanned for agent definitions.
All metadata and configuration is specified in the AGENT_CONFIG dict.
"""

from app.agents import AgentBuilder


def create_docs_config_agent():
    """
    Factory function specified in AGENT_CONFIG.

    The factory function name is specified in AGENT_CONFIG['factory'].
    This function will be called to create the agent instance.
    """
    return (AgentBuilder("Docs Agent (Configuration)")
            .with_model("openai")
            .with_db()
            .with_memory()
            .with_mcp("docs")
            .with_instructions("You are a documentation assistant created via configuration pattern.")
            .with_config(
                add_history_to_context=True,
                num_history_sessions=5,
                num_history_runs=20,
                enable_session_summaries=True,
                markdown=True,
                id="docs_agent_configuration",
                user_id="1",
                session_id="configuration_session"
            )
            .build())


# Alternative factory function
def create_alternative_agent():
    """Alternative factory function example."""
    return (AgentBuilder("Alternative Docs Agent")
            .with_model("openai")
            .with_instructions("I'm an alternative documentation agent.")
            .build())


# AGENT_CONFIG: Configuration-based discovery
# This dictionary defines the agent and its metadata
AGENT_CONFIG = {
    # Required: agent name
    "name": "DocsAgentConfiguration",

    # Required: factory function name
    "factory": "create_docs_config_agent",

    # Optional: agent metadata
    "tags": ["example", "documentation", "configuration-pattern"],
    "priority": 60,  # Lower priority than decorator and convention
    "enabled": False,  # Disabled to avoid conflicts with decorator example
    "dependencies": [],

    # Optional: custom attributes
    "custom_attributes": {
        "pattern_type": "configuration",
        "example": True,
        "version": "1.0",
        "config_driven": True
    },

    # Optional: additional configuration
    "description": "Documentation agent discovered via configuration pattern",
    "author": "Agent Discovery System",
    "created_date": "2024-09-15"
}

# You can have multiple AGENT_CONFIG definitions by using different variable names
# and pointing to different factory functions:

SECONDARY_AGENT_CONFIG = {
    "name": "AlternativeDocsAgent",
    "factory": "create_alternative_agent",
    "tags": ["example", "alternative"],
    "priority": 40,
    "enabled": False,  # Disabled by default
    "custom_attributes": {
        "pattern_type": "configuration",
        "alternative": True
    }
}

# However, the discovery system only looks for 'AGENT_CONFIG' by default
# To support multiple configs, you'd need to extend the discovery logic