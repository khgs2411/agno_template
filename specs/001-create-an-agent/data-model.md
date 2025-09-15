# Phase 1: Data Model Design

## Entity Definitions

### AgentMetadata
**Purpose**: Contains descriptive information about agents for discovery and management

**Fields**:
- `name: str` - Unique identifier for the agent
- `pattern: DiscoveryPattern` - Discovery method used (DECORATOR, CONVENTION, CONFIGURATION)
- `tags: List[str]` - Categorization tags for filtering
- `priority: int` - Priority for loading order (default: 50)
- `enabled: bool` - Whether agent is active (default: True)
- `dependencies: List[str]` - Required dependencies (default: empty)
- `custom_attributes: Dict[str, Any]` - Arbitrary key-value pairs for extensibility

**Validation Rules**:
- Name must be non-empty string
- Priority must be positive integer
- Tags must be valid strings
- Dependencies must be existing agent names

**State Transitions**:
- `enabled` can be toggled at runtime
- Other fields are immutable after discovery

### AgentDefinition
**Purpose**: Represents a complete discovered agent with its creation mechanism

**Fields**:
- `name: str` - Agent identifier (matches metadata.name)
- `factory_function: Callable[[], Agent]` - Function to create agent instance
- `metadata: AgentMetadata` - Agent metadata
- `module_path: str` - Python module path where agent was discovered
- `source_file: str` - Absolute file path to agent definition

**Validation Rules**:
- Factory function must be callable with no required arguments
- Factory function must return Agno Agent instance
- Module path must be valid Python module reference
- Source file must exist and be readable

**Relationships**:
- Contains one AgentMetadata instance
- Factory function creates Agent instances (Agno framework)

### DiscoveryPattern
**Purpose**: Enumeration of agent discovery methods with priority ordering

**Values**:
- `DECORATOR = 1` - Highest priority, functions marked with @register_agent
- `CONVENTION = 2` - Medium priority, files ending with _agent.py
- `CONFIGURATION = 3` - Lowest priority, AGENT_CONFIG exports

**Usage**: Used for priority sorting during discovery process

### AgentFilter
**Purpose**: Criteria for selecting agents during discovery or retrieval

**Fields**:
- `tags: Optional[List[str]]` - Filter by tags (any match)
- `enabled: Optional[bool]` - Filter by enabled status
- `pattern: Optional[DiscoveryPattern]` - Filter by discovery pattern
- `priority_min: Optional[int]` - Minimum priority threshold
- `priority_max: Optional[int]` - Maximum priority threshold
- `custom_criteria: Dict[str, Any]` - Custom filtering criteria

**Usage**: Applied by AgentManager for filtered retrieval

### AgentBuilder
**Purpose**: Fluent API for programmatic agent creation

**Configuration Methods**:
- `with_model(provider, model_id, **kwargs)` - Configure model
- `with_mcp(*tools)` - Add MCP tools
- `with_memory()` - Add memory tools
- `with_db(db_config)` - Configure database
- `with_vector_db(config)` - Configure vector store
- `with_tools(tools)` - Add custom tools
- `with_instructions(instructions)` - Set agent instructions
- `with_knowledge_base(**config)` - Configure knowledge
- `with_metadata(**metadata)` - Set discovery metadata
- `build()` - Create final Agent instance

**Validation**: Each method validates its inputs before chaining

### AgentRegistry
**Purpose**: Central storage and management of discovered agents

**State**:
- `_agent_definitions: Dict[str, AgentDefinition]` - Registry of all agents
- `_decorated_functions: Dict[str, Callable]` - Functions with @register_agent
- `_discovery_paths: List[Path]` - Paths to scan for agents
- `_discovery_completed: bool` - Whether initial discovery finished

**Methods**:
- Discovery: `discover_agents()`, pattern-specific discovery methods
- Retrieval: `get_agent_definition()`, `list_agents()`, filtering methods
- Management: `enable_agent()`, `disable_agent()`, `clear_registry()`

## Data Flow

### Discovery Process
1. **Scan discovery paths** for Python files
2. **Load modules** using importlib
3. **Inspect modules** for agent definitions based on pattern
4. **Create AgentDefinition** with metadata and factory function
5. **Register in AgentRegistry** with validation
6. **Sort by priority** and pattern precedence

### Agent Creation Flow
1. **Retrieve AgentDefinition** from registry
2. **Call factory_function()** to create Agent instance
3. **Apply any runtime configuration**
4. **Return configured Agent** for use

### Builder Pattern Flow
1. **Start with AgentBuilder(name)**
2. **Chain configuration methods** (with_model, with_tools, etc.)
3. **Call build()** to create Agent instance
4. **Optionally register** with discovery system

## Relationships

### Core Relationships
- AgentRegistry **contains many** AgentDefinition
- AgentDefinition **has one** AgentMetadata
- AgentDefinition **creates** Agent (via factory_function)
- AgentBuilder **creates** Agent (via build method)

### Discovery Relationships
- DiscoveryPattern **categorizes** AgentDefinition
- AgentFilter **selects** AgentDefinition subset
- Discovery paths **contain** agent definition files

### Integration Relationships
- Agent **uses** ModelFactory for model selection
- Agent **uses** PostgresSettings for database
- Agent **uses** MCPManager for tool integration
- AgentManager **provides** Agent instances to AgentOS

## Storage

### In-Memory Storage
All agent definitions stored in memory during application runtime:
- AgentRegistry as singleton with dictionary storage
- No persistent storage required for discovery metadata
- Agent instances created on-demand (lazy loading)

### File System Integration
- Discovery paths scanned for agent definition files
- Module modification times tracked for hot reload
- Source file paths stored for debugging and reload

### Configuration Persistence
- Agent metadata can be externalized to configuration files
- Environment variables for discovery path configuration
- Database/tool configurations follow existing patterns

## Validation

### Discovery-Time Validation
- Python syntax validation during module import
- Agent definition structure validation
- Factory function signature validation
- Metadata completeness and type validation

### Runtime Validation
- Agent instance creation validation
- Dependency resolution validation
- Configuration parameter validation
- Error handling with graceful degradation

### Integration Validation
- AgentOS compatibility validation
- Database connection validation (if configured)
- MCP tool availability validation (if configured)
- Model provider availability validation (if configured)