"""
Documentation Agent - Decorator Pattern Example.

This demonstrates the HIGHEST PRIORITY discovery pattern using @register_agent decorator.
Functions decorated with @register_agent are discovered first and have priority over other patterns.
"""

from app.agents import AgentBuilder, register_agent


@register_agent(
    tags=["example", "documentation", "decorator-pattern"],
    priority=100,  # High priority
    enabled=True,
    dependencies=[],
    custom_attributes={
        "pattern_type": "decorator",
        "example": True,
        "version": "1.0"
    }
)
def create_decorator_example_agent():
    """
    Create documentation agent using decorator pattern.

    This is the modern, recommended way to register agents.
    The decorator handles all the discovery registration automatically.
    """
    return (AgentBuilder("Decorator Example Agent")
            .with_model("openai")
            .with_db()
            .with_memory()
            .with_mcp("docs")
            .with_instructions("You are a documentation assistant created via decorator pattern. This is an example of the @register_agent decorator.")
            .with_config(
                add_history_to_context=True,
                num_history_sessions=3,
                num_history_runs=10,
                enable_session_summaries=True,
                markdown=True,
                id="decorator_example_agent",
                user_id="1",
                session_id="decorator_session"
            )
            .build())


# You can also register multiple agents in the same file
@register_agent(
    tags=["example", "secondary"],
    priority=90,
    enabled=False  # Disabled to reduce noise during testing
)
def create_secondary_docs_agent():
    """Secondary documentation agent example."""
    return (AgentBuilder("Secondary Docs Agent")
            .with_model("openai")
            .with_instructions("I'm a secondary documentation agent.")
            .build())