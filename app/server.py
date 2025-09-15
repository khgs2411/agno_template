import os
from agno.os import AgentOS
from fastapi import FastAPI

from app.agents import AgentManager
from app.utils.log import logger


class Server:
    agent_os: AgentOS
    app: FastAPI

    def __init__(self):
        # Discover and create all enabled agents
        try:
            # Perform agent discovery
            discovered_count = AgentManager.discover()
            logger.info(f"Agent discovery completed: {discovered_count} agents found")

            # Get discovery statistics
            stats = AgentManager.get_stats()
            logger.debug(f"Discovery stats: {stats}")

            # Create instances of all enabled agents
            agents = AgentManager.create_enabled_agents()
            logger.info(f"Created {len(agents)} enabled agent instances")

            # Log agent names for debugging
            if agents:
                agent_names = [getattr(agent, 'name', 'Unknown') for agent in agents]
                logger.info(f"Loaded agents: {', '.join(agent_names)}")
            else:
                logger.warning("No enabled agents found")

        except Exception as e:
            logger.error(f"Failed to load agents: {e}")
            # Fallback to empty list if agent loading fails
            agents = []
            logger.warning("Starting AgentOS with no agents due to loading failure")

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
