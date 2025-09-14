# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- **Full Agent OS support**: `python main.py` - Runs the app with full AgentOS support
- **FastAPI only**: `fastapi dev main.py` - Runs with FastAPI only (development mode)
- **Production**: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Environment Setup
- Python virtual environment is in `.venv/`
- Dependencies managed via `pyproject.toml` (requirements.txt auto-generated during Docker build)
- Environment variables loaded from `.env`
- **Docker workflow**: Only update `pyproject.toml` - Docker builds handle dependency resolution

### Docker Development
- **Development with Docker**: `docker-compose -f docker/docker-compose.yml up --build`
- **Environment files**: Copy `.env.docker.example` to `.env.docker` and update with your API keys
- **Database included**: PostgreSQL container with health checks and performance optimizations
- **Hot reload**: Source code mounted for development (changes reflect immediately)

### Hot Reload & MCP Tools
- **MCP Hot Reload Issue**: If you experience async cleanup errors during hot reload, set `DISABLE_MCP=true` in your environment
- **Development Workaround**: MCP connections are automatically retried and gracefully fallback during hot reload conflicts
- **Production**: MCP tools work normally without hot reload concerns

### Testing and Quality
- No specific test commands configured - check for pytest or other testing frameworks when implementing tests
- Use `python -m flake8` or `ruff` for linting (verify availability first)

## Architecture Overview

### Core Framework: Agno + AgentOS
This is a template project built on the **Agno** framework (v2.0.3) with **AgentOS** orchestration:

- **AgentOS** (`app/server.py:17-21`): Central orchestration system that manages agents and provides FastAPI integration
- **Agent System**: Individual AI agents with specific capabilities, registered with AgentOS
- **Model Abstraction**: Sophisticated multi-provider model management system

### Key Architectural Patterns

#### 1. Agent-Based Architecture
- Agents are defined in `app/agents/` and registered with AgentOS
- Primary agent: `agno_agent` (Documentation Agent) with Gemini model and MCP tools
- Agent factory pattern in `app/agents/factory.py` for creating different agent types

#### 2. Multi-Provider Model System
**Central Factory Pattern** (`app/models/factory.py`):
- `ModelFactory` provides unified interface: `ModelFactory.get(provider)` or `ModelFactory.get_model(model_id)`
- Provider registry system with automatic initialization and synonym support
- IDE-friendly with typed constants: `ModelFactory.providers().GEMINI`

**Provider Structure**:
- **OpenAI Provider** (`app/models/providers/openai.py`): Comprehensive model definitions with metadata, parameters, and creation functions
- **Google Provider** (`app/models/providers/google.py`): Gemini model variants with configuration options
- **Registry System** (`app/models/provider_registry.py`): State management, provider initialization, and model registration

#### 3. Database Architecture (Configuration-Only)
**Agno's Auto-Management Approach**:
- **No Custom Migrations**: Agno's `PostgresDb` and `PgVector` classes handle table creation automatically
- **Configuration Layer** (`app/db/`): Provides database connection settings that Agno consumes
- **Built-in Tables**: Framework creates standard tables for agents, knowledge, embeddings automatically
- **Docker Integration**: Database container with optimized PostgreSQL settings

**Database Usage Pattern**:
```python
# Settings provide connection info
postgres_settings = PostgresSettings()
db_url = postgres_settings.get_db_url()

# Agno classes handle table management
db = PostgresDb(db_url=db_url)
vector_db = PgVector(table_name="embeddings", db_url=db_url)
```

#### 4. Configuration Management
- Environment-based configuration via `.env` and `load_dotenv()`
- Provider constants defined once in `ProviderConstants` class
- Synonym support (e.g., "google" and "gemini" refer to same provider)

### Project Structure
```
app/
├── server.py          # AgentOS server and FastAPI app setup
├── agents/            # Agent definitions and factory
│   ├── docs_agent.py  # Main documentation agent with MCP tools
│   └── factory.py     # Agent creation factory
├── db/                # Database configuration (settings only)
│   ├── db_settings.py # Base database settings with Pydantic
│   └── postgres/      # PostgreSQL-specific settings
└── models/            # Multi-provider model management
    ├── factory.py     # Central model factory with unified API
    ├── provider_registry.py  # Provider state management and initialization
    └── providers/     # Provider-specific implementations
        ├── openai.py  # OpenAI models with metadata and creation functions
        └── google.py  # Google/Gemini models with variants
docker/                # Docker configuration
├── Dockerfile         # Multi-stage build for production
├── docker-compose.yml # Development environment with PostgreSQL
└── docker-compose.override.yml  # Local development overrides
```

### Key Dependencies
- **agno==2.0.3**: Core agent framework
- **fastapi**: Web framework integration
- **anthropic**, **openai**, **google-genai**: Model provider clients
- **mcp**: Model Context Protocol for tool integration

## Development Guidelines

### Adding New Agents
1. Create agent definition in `app/agents/`
2. Import and register in `app/server.py` AgentOS initialization
3. Use existing model factory for model selection
4. Database integration: Use existing `PostgresSettings` for connection info
5. **MCP Tools**: Use `MCPFactory.create_lazy_mcp_list()` for hot reload compatibility

### Database Configuration (No Custom Code Needed)
- **Settings Only**: `app/db/` provides configuration classes, not database logic
- **Agno Handles Everything**: Framework creates tables, manages sessions, handles migrations
- **Environment Variables**: Use `POSTGRES_*` or `DATABASE_URL` for connections
- **Docker Ready**: Includes optimized PostgreSQL container with health checks

### Adding New Model Providers
1. Create provider file in `app/models/providers/`
2. Define model enums, metadata, and creation functions
3. Add provider to `PROVIDER_CONFIG` in `provider_registry.py`
4. Include registration function that calls `ModelFactory.register_model()`

### Model Usage Patterns
```python
# Provider-based access (recommended)
model = ModelFactory.get(ModelFactory.providers().GEMINI)

# Direct model access
model = ModelFactory.get_model(OpenAIModels.GPT_4O)

# With parameters
model = ModelFactory.get("openai", temperature=0.7, max_tokens=2000)
```

### Server Startup Pattern
The `main.py` uses a reloader-aware pattern to prevent double initialization:
- Checks `RUN_MAIN` environment variable to detect reloader subprocess
- Only creates full server in main process, dummy app in subprocess
- Always use the "agno-docs" mcp for documentation, or information retrieval about and for the "agno" ai framework, use the context7 mcp to fetch documentation for everything else. For websearch always use the 'fetch' mcp :)