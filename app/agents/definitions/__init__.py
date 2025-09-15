"""
Agent definitions discovery folder.

This folder contains agent definition files that are automatically discovered
by the Agent Discovery System. Agents can be defined using multiple patterns:

1. Convention-based (*_agent.py files):
   - File name ending with '_agent.py'
   - Must contain either 'agent' variable or 'create_agent()' function
   - Metadata via module variables (AGENT_TAGS, AGENT_PRIORITY, etc.)

2. Configuration-based (AGENT_CONFIG export):
   - Any .py file with AGENT_CONFIG dictionary
   - Must specify factory function name
   - All metadata in AGENT_CONFIG

3. Decorator-based (@register_agent):
   - Functions decorated with @register_agent
   - Highest priority discovery pattern
   - Metadata specified in decorator arguments

Example files:
- docs_agent.py (convention-based)
- research_agent.py (configuration-based)
- support_agent.py (decorator-based)
"""

# This file enables the definitions folder as a Python package
# Agent discovery will scan this folder for agent definitions