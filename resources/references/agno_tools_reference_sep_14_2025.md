# Agno Tools and Toolkits Reference

This document provides a comprehensive list of tools and toolkits available in the Agno AI framework with their usage and purpose, based on official documentation.

## Core Framework Tools & Memory

### **Memory System (Built-in)**
- **Purpose**: Store and retrieve user memories and context across conversations
- **Usage**: Enable with `enable_user_memories=True` or `enable_agentic_memory=True`
- **Key Features**: Automatic memory creation, user-specific memories, conversation continuity
- **Setup**:
  ```python
  from agno.agent import Agent
  from agno.db.sqlite import SqliteDb

  db = SqliteDb(db_file="agno.db")
  agent = Agent(
      db=db,
      enable_user_memories=True  # Auto memory creation
  )
  ```

### **KnowledgeTools toolkit**
- **Purpose**: Advanced reasoning and knowledge base interaction
- **Components**: `think`, `search`, `analyze` tools
- **Usage**: Vector database integration, document search, knowledge reasoning
- **Import**: `from agno.tools.knowledge import KnowledgeTools`

## Search & Information Retrieval

### **DuckDuckGoTools toolkit**
- **Purpose**: Privacy-focused web searching
- **Usage**: Web search, news retrieval without tracking
- **Import**: `from agno.tools.duckduckgo import DuckDuckGoTools`

### **GoogleSearchTools toolkit**
- **Purpose**: Google web search capabilities
- **Usage**: Comprehensive web search with Google
- **Requirements**: `pip install -U googlesearch-python pycountry`
- **Import**: `from agno.tools.googlesearch import GoogleSearchTools`

### **SerperTools toolkit**
- **Purpose**: Web searching and scraping via Serper
- **Usage**: Comprehensive web data extraction
- **Import**: `from agno.tools.serper import SerperTools`

### **TavilyTools toolkit**
- **Purpose**: Up-to-date web search results
- **Usage**: Current events, real-time information
- **Import**: `from agno.tools.tavily import TavilyTools`

### **ValyuTools toolkit**
- **Purpose**: Academic papers and credible web content search
- **Usage**: Research assistant capabilities with relevance scoring
- **Import**: `from agno.tools.valyu import ValyuTools`

### **WikipediaTools toolkit**
- **Purpose**: Encyclopedia knowledge access
- **Usage**: Research, factual information retrieval
- **Import**: `from agno.tools.wikipedia import WikipediaTools`

### **ArxivTools toolkit**
- **Purpose**: Scientific paper search and retrieval
- **Usage**: Academic research, paper analysis
- **Requirements**: `pip install -U arxiv pypdf`
- **Import**: `from agno.tools.arxiv import ArxivTools`
- **Functions**: `search_arxiv`, `search_arxiv_and_update_knowledge_base`

### **ExaTools toolkit**
- **Purpose**: Advanced web search functionalities
- **Usage**: Specialized search capabilities
- **Import**: `from agno.tools.exa import ExaTools`

### **BaiduSearchTools toolkit**
- **Purpose**: Chinese web search via Baidu
- **Usage**: China-focused information retrieval
- **Import**: `from agno.tools.baidusearch import BaiduSearchTools`

### **LinkupTools toolkit**
- **Purpose**: AI-focused web searching
- **Usage**: AI applications and services discovery
- **Requirements**: `pip install -U linkup-sdk openai agno`
- **Import**: `from agno.tools.linkup import LinkupTools`

### **SearxngTools toolkit**
- **Purpose**: Privacy-respecting metasearch engine
- **Usage**: Anonymous web searching with custom Searxng instance
- **Import**: `from agno.tools.searxng import SearxngTools`
- **Setup**: Requires Searxng server URL configuration

## Web Scraping & Data Extraction

### **WebsiteTools toolkit**
- **Purpose**: General website scraping
- **Usage**: Content extraction from web pages
- **Import**: `from agno.tools.website import WebsiteTools`

### **AgentQLTools toolkit**
- **Purpose**: Browser automation and scraping
- **Usage**: Interactive web browsing and data extraction
- **Import**: `from agno.tools.agentql import AgentQLTools`

### **BrowserBaseTools toolkit**
- **Purpose**: Browser interaction capabilities
- **Usage**: Automated browser operations
- **Import**: `from agno.tools.browserbase import BrowserBaseTools`

### **Crawl4AITools toolkit**
- **Purpose**: Web data crawling
- **Usage**: Large-scale web data extraction
- **Import**: `from agno.tools.crawl4ai import Crawl4AITools`

### **FirecrawlTools toolkit**
- **Purpose**: Web crawling and scraping services
- **Usage**: Structured web data extraction with crawl and scrape capabilities
- **Import**: `from agno.tools.firecrawl import FirecrawlTools`
- **Features**: `enable_scrape`, `enable_crawl` parameters

### **SpiderTools toolkit**
- **Purpose**: Website crawling and scraping
- **Usage**: Site-wide data extraction using Scrapy
- **Requirements**: `pip install -U scrapy openai agno`
- **Import**: `from agno.tools.spider import SpiderTools`

### **BrightDataTools toolkit**
- **Purpose**: Professional web scraping platform
- **Components**: Social media (Instagram, Facebook, TikTok, X), LinkedIn, Google Maps, YouTube, Reddit, etc.
- **Usage**: Enterprise-grade data extraction with screenshot capabilities
- **Requirements**: `pip install -U requests openai agno`
- **Import**: `from agno.tools.brightdata import BrightDataTools`
- **Setup**: Requires BRIGHT_DATA_API_KEY environment variable

### **JinaReaderTools toolkit**
- **Purpose**: Neural search and AI services
- **Usage**: Advanced content processing
- **Import**: `from agno.tools.jina import JinaReaderTools`

### **NewspaperTools toolkit**
- **Purpose**: News article extraction
- **Usage**: Article content and metadata retrieval
- **Import**: `from agno.tools.newspaper import NewspaperTools`

### **Newspaper4kTools toolkit**
- **Purpose**: Enhanced article reading and extraction
- **Usage**: Improved news content extraction with better parsing
- **Import**: `from agno.tools.newspaper4k import Newspaper4kTools`

### **ScrapeGraphTools toolkit**
- **Purpose**: LLM-powered intelligent web scraping
- **Usage**: Smart data extraction using natural language prompts
- **Requirements**: `pip install -U scrapegraph-py`
- **Import**: `from agno.tools.scrapegraph import ScrapeGraphTools`
- **Features**: `smartscraper` for AI-driven extraction

### **OxylabsTools toolkit**
- **Purpose**: Professional web scraping via Oxylabs
- **Usage**: High-scale web data extraction
- **Import**: `from agno.tools.oxylabs import OxylabsTools`

## Data Handling & Database

### **CSVTools toolkit**
- **Purpose**: CSV file operations
- **Usage**: Data import/export, spreadsheet manipulation
- **Import**: `from agno.tools.csv import CSVTools`

### **DuckDbTools toolkit**
- **Purpose**: SQL queries with DuckDB
- **Usage**: Fast analytical queries, CSV loading, table creation
- **Import**: `from agno.tools.duckdb import DuckDbTools`
- **Features**: `create_table_from_path`, `create_tables`, `export_tables`

### **PandasTools toolkit**
- **Purpose**: Data manipulation and analysis
- **Usage**: DataFrames, data transformation, analysis
- **Import**: `from agno.tools.pandas import PandasTools`

### **PostgresTools toolkit**
- **Purpose**: PostgreSQL database interaction
- **Usage**: Database operations, queries, management
- **Import**: `from agno.tools.postgres import PostgresTools`

### **SQLTools toolkit**
- **Purpose**: General SQL query execution
- **Usage**: Database queries across different engines
- **Import**: `from agno.tools.sql import SQLTools`

### **ZepTools toolkit**
- **Purpose**: Zep memory platform integration
- **Usage**: Advanced memory and context management
- **Import**: `from agno.tools.zep import ZepTools`

### **Mem0Tools toolkit**
- **Purpose**: Advanced memory management with Mem0
- **Usage**: Evolving user memory storage and retrieval
- **Import**: `from agno.tools.mem0 import Mem0Tools`
- **Features**: Custom configuration for vector store, LLM, and embedder

### **MemoriTools toolkit**
- **Purpose**: Persistent memory with database backend
- **Usage**: Long-term conversation memory with search capabilities
- **Import**: `from agno.tools.memori import MemoriTools`
- **Setup**: Requires database connection string and namespace

## Local Operations

### **CalculatorTools toolkit**
- **Purpose**: Mathematical calculations
- **Usage**: Arithmetic, mathematical operations
- **Import**: `from agno.tools.calculator import CalculatorTools`

### **DockerTools toolkit**
- **Purpose**: Docker container interaction
- **Usage**: Container management, deployment
- **Import**: `from agno.tools.docker import DockerTools`

### **FileTools toolkit**
- **Purpose**: File system operations
- **Usage**: Read, write, manage files and directories
- **Import**: `from agno.tools.file import FileTools`

### **PythonTools toolkit**
- **Purpose**: Python code execution
- **Usage**: Dynamic code generation and execution
- **Import**: `from agno.tools.python import PythonTools`

### **ShellTools toolkit**
- **Purpose**: Shell command execution
- **Usage**: System operations, command-line tasks
- **Import**: `from agno.tools.shell import ShellTools`

### **SleepTools toolkit**
- **Purpose**: Execution pausing
- **Usage**: Delays, timing control in workflows
- **Import**: `from agno.tools.sleep import SleepTools`

## Communication & Social

### **EmailTools toolkit**
- **Purpose**: Email sending capabilities
- **Usage**: Automated email communication
- **Import**: `from agno.tools.email import EmailTools`

### **SlackTools toolkit**
- **Purpose**: Slack workspace integration
- **Usage**: Message sending, channel interaction
- **Import**: `from agno.tools.slack import SlackTools`

### **ZoomTools toolkit**
- **Purpose**: Zoom meeting management
- **Usage**: Meeting scheduling, participant management
- **Import**: `from agno.tools.zoom import ZoomTools`

### **WebexTools toolkit**
- **Purpose**: Cisco Webex integration
- **Usage**: Communication and meeting management
- **Import**: `from agno.tools.webex import WebexTools`

### **TwilioTools toolkit**
- **Purpose**: SMS and phone services
- **Usage**: Text messaging, phone communication
- **Import**: `from agno.tools.twilio import TwilioTools`

### **GmailTools toolkit**
- **Purpose**: Gmail email management
- **Usage**: Email reading, sending, management
- **Import**: `from agno.tools.gmail import GmailTools`

## AI Model Integration

### **GroqTools toolkit**
- **Purpose**: Groq API interaction for audio and text processing
- **Usage**: Audio transcription, text translation, speech generation
- **Import**: `from agno.tools.models.groq import GroqTools`

### **GeminiTools toolkit**
- **Purpose**: Google Gemini model integration
- **Usage**: Advanced AI capabilities and model interactions
- **Import**: `from agno.tools.models.gemini import GeminiTools`

## Development & Sandbox

### **DaytonaTools toolkit**
- **Purpose**: Remote sandbox code execution environment
- **Components**: `run_code`, `create_file`, `read_file`, `list_files`, `delete_file`, `run_shell_command`
- **Usage**: Secure code execution with file management
- **Import**: `from agno.tools.daytona import DaytonaTools`
- **Languages**: Python, JavaScript, TypeScript support

## Additional Toolkits

### **ApifyTools toolkit**
- **Purpose**: Apify Actor integration for web automation
- **Usage**: Web scraping, crawling with multiple actors
- **Import**: `from agno.tools.apify import ApifyTools`
- **Features**: Support for multiple actors like `apify/rag-web-browser`

### **GoogleMapTools toolkit**
- **Purpose**: Google Maps integration for location services
- **Usage**: Location search, business information
- **Import**: `from agno.tools.google_maps import GoogleMapTools`

### **WebBrowserTools toolkit**
- **Purpose**: Web browser automation
- **Usage**: Open websites, browser interaction
- **Import**: `from agno.tools.webbrowser import WebBrowserTools`

### **MCPTools toolkit**
- **Purpose**: Model Context Protocol integration
- **Usage**: Connect to MCP servers for extended capabilities
- **Import**: `from agno.tools.mcp import MCPTools`
- **Features**: Async support, custom server parameters

## Usage Patterns

### Basic Tool Usage
```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

agent.print_response("What's happening in France?", stream=True)
```

### Tool Selection
```python
from agno.tools.gmail import GmailTools

# Include specific tools only
agent = Agent(
    tools=[GmailTools(include_tools=["get_latest_emails"])],
)

# Exclude specific tools
agent = Agent(
    tools=[GmailTools(exclude_tools=["create_draft_email"])],
)

# Advanced selection with multiple toolkits
from agno.tools.calculator import CalculatorTools
agent = Agent(
    tools=[
        CalculatorTools(exclude_tools=["exponentiate", "factorial"]),
        DuckDuckGoTools(include_tools=["duckduckgo_search"])
    ]
)
```

### Tool Confirmation
```python
# Require confirmation for specific tools
agent = Agent(
    tools=[DuckDuckGoTools(requires_confirmation_tools=["duckduckgo_search"])],
)
```

### Tool Caching
```python
# Enable result caching for performance
agent = Agent(
    tools=[DuckDuckGoTools(cache_results=True)],
)
```

### Custom Tools
```python
from agno.tools import tool
import random

@tool(stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Get the weather for the given city."""
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    return f"The weather in {city} is {random.choice(weather_conditions)}."

agent = Agent(
    tools=[get_weather],
    markdown=True
)
```

### Tool Results and Media
```python
from agno.tools.function import ToolResult
from agno.media import Image

@tool
def generate_image(prompt: str) -> ToolResult:
    """Generate an image from a prompt."""
    image = Image(url="https://example.com/image.jpg")

    return ToolResult(
        content=f"Generated image for: {prompt}",
        images=[image]
    )
```

## Key Features Across Toolkits

- **Tool Selection**: `include_tools` and `exclude_tools` parameters for granular control
- **Confirmation**: `requires_confirmation_tools` for user approval before execution
- **Caching**: `cache_results` for performance optimization and cost reduction
- **Hooks**: `tool_hooks` for pre/post execution logic and logging
- **Control Flow**: `stop_after_tool_call` and `show_result` options for workflow management
- **Instructions**: `instructions` and `add_instructions` for tool-specific guidance
- **Session State**: Access to `session_state` parameter for persistent data across conversations

## Memory Management

### Built-in Memory System
```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb

# Setup database
db = SqliteDb(db_file="agno.db")

# Enable automatic memory creation
agent = Agent(
    db=db,
    enable_user_memories=True,  # Auto-create memories after each run
    user_id="user_123"         # User-specific memories
)

# Enable agentic memory (agent controls memory)
agent = Agent(
    db=db,
    enable_agentic_memory=True  # Agent decides when to create/update memories
)
```

### Memory with Storage (Session Continuity)
```python
from agno.storage.sqlite import SqliteStorage

storage = SqliteStorage(table_name="agent_sessions", db_file="agent.db")

agent = Agent(
    db=db,
    storage=storage,
    enable_user_memories=True,
    add_history_to_messages=True,  # Include conversation history
    num_history_runs=5,            # Number of previous runs to include
    session_id="session_123"       # Resume specific session
)
```

### Manual Memory Operations
```python
# Retrieve user memories
memories = agent.get_user_memories(user_id="user_123")
print(memories)
```

## Tool Built-in Parameters

Agno automatically provides special parameters to tools:

- **`session_state`**: Access to persistent data across conversations
- **Media parameters**: `images`, `videos`, `audio`, `files` for multimodal input

This reference covers the comprehensive toolkit ecosystem available in Agno, enabling you to build sophisticated AI agents with diverse capabilities across search, data processing, communication, and specialized domains.