"""MCP registry with definitions and groups."""

from typing import Dict, List, Any

# MCP connection definitions
MCP_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "docs": {
        "transport": "streamable-http",
        "url": "https://docs.agno.com/mcp",
        "description": "Agno documentation and help system",
    },
    # Add more MCP definitions as needed
    # Example for future Trackbox MCPs:
    # "trackbox_auth": {
    #     "transport": "streamable-http",
    #     "url": "https://auth.trackbox.com/mcp",
    #     "description": "Trackbox authentication service"
    # },
    # "trackbox_analytics": {
    #     "transport": "streamable-http",
    #     "url": "https://analytics.trackbox.com/mcp",
    #     "description": "Trackbox analytics and reporting"
    # },
    # "trackbox_billing": {
    #     "transport": "streamable-http",
    #     "url": "https://billing.trackbox.com/mcp",
    #     "description": "Trackbox billing and subscription management"
    # },
}

# MCP group definitions for related services
MCP_GROUPS: Dict[str, List[str]] = {
    # Example group for future Trackbox MCPs:
    # "trackbox": [
    #     "trackbox_auth",
    #     "trackbox_analytics",
    #     "trackbox_billing"
    # ],
    # "monitoring": [
    #     "metrics",
    #     "logs",
    #     "traces"
    # ],
}


def get_mcp_definition(name: str) -> Dict[str, Any]:
    """Get MCP definition by name."""
    if name not in MCP_DEFINITIONS:
        raise ValueError(
            f"MCP '{name}' not found in registry. Available: {list(MCP_DEFINITIONS.keys())}"
        )
    return MCP_DEFINITIONS[name].copy()


def get_group_definitions(group_name: str) -> List[Dict[str, Any]]:
    """Get all MCP definitions for a group."""
    if group_name not in MCP_GROUPS:
        raise ValueError(
            f"MCP group '{group_name}' not found. Available: {list(MCP_GROUPS.keys())}"
        )

    return [get_mcp_definition(mcp_name) for mcp_name in MCP_GROUPS[group_name]]


def list_available_mcps() -> List[str]:
    """List all available MCP names."""
    return list(MCP_DEFINITIONS.keys())


def list_available_groups() -> List[str]:
    """List all available group names."""
    return list(MCP_GROUPS.keys())
