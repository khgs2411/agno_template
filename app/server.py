import os
from agno.os import AgentOS
from fastapi import FastAPI

from app.agents import discover_and_create_all
from app.utils.log import logger


class Server:
    agent_os: AgentOS
    app: FastAPI

    def __init__(self):
        # Discover and create all enabled agents - SIMPLIFIED
        try:
            agents = discover_and_create_all()
        except Exception as e:
            logger.error(f"Failed to discover and create agents: {e}")
            # Fallback to empty list if agent loading fails
            agents = []

        # Create the AgentOS
        self.agent_os = AgentOS(
            os_id="agno-template-os",
            description="Agno Template with Agent Discovery System",
            agents=agents,
        )

        # Get the FastAPI app
        self.app = self.agent_os.get_app()

    def serve(self):
        # use fastapi dev main.py to run the app with fastapi only
        # use python main.py to run the app with full agent os support
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        self.agent_os.serve(app="main:app", reload=True, port=port, host=host)
