import os
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.tools.mem0 import Mem0Tools
from agno.tools.memory import MemoryTools
from agno.tools.user_control_flow import UserControlFlowTools
from app.utils.log import logger
from agno.vectordb.pgvector import PgVector
from app.models.factory import ModelFactory
from app.models.provider_registry import Providers
from app.db.postgres.settings import PostgresSettings
from app.tools.mcp import MCPManager


model = ModelFactory.get(Providers.OPENAI)

# Initialize database connection using settings
postgres_settings = PostgresSettings()
database_url = postgres_settings.get_db_url()
db = PostgresDb(db_url=database_url)

vector_db = PgVector(
    table_name="embeddings",
    db_url=database_url,
)

# this adds reasoning to the agent
memory = MemoryTools(
    db=db,
)

# Only initialize Mem0Tools if API key is available
mem0_api_key = os.getenv("MEM0_API_KEY")
mem0 = Mem0Tools(api_key=mem0_api_key, user_id="1")
mcp = MCPManager.get("docs")

controlFlow = UserControlFlowTools()

# Create the Agent
agno_agent = Agent(
    name="Agno Documentation Agent",
    model=model,
    # Add a database to the Agent
    db=db,
    # Add the Agno MCP server to the Agent (lazy-loaded to prevent hot reload issues)
    tools=[memory, controlFlow],
    # Add the previous session history to the context
    add_history_to_context=True,
    num_history_sessions=5,
    num_history_runs=20,
    enable_session_summaries=True,
    instructions="Your name is Joker",
    markdown=True,
    id="agno_doc_agent",
    user_id="1",
    session_id="user_1_session",
)
