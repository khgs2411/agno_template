import os
from agno.os import AgentOS
from fastapi import FastAPI

from app.agents.docs_agent import agno_agent


class Server:
    agent_os: AgentOS
    app: FastAPI

    def __init__(self):
        # Create the model

        # Create the AgentOS
        self.agent_os = AgentOS(
            os_id="my-first-os",
            description="My first AgentOS",
            agents=[agno_agent],
        )

        # Get the FastAPI app
        self.app = self.agent_os.get_app()

    def serve(self):
        # use fastapi dev main.py to run the app with fastapi only
        # use python main.py to run the app with full agent os support
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 8000))
        self.agent_os.serve(app="main:app", reload=True, port=port, host=host)
