# Tasks: Agent Discovery System

**Input**: Design documents from `/specs/001-create-an-agent/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md

## Execution Summary
This feature implements automatic agent discovery for the Agno template project following KISS principles with container-based validation instead of complex test files. The implementation follows existing patterns from ModelFactory and ProviderRegistry.

**IMPORTANT**: Each task references specific sections in the feature documents. Read the referenced documents for complete implementation context.

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- All paths are in app/agents/ structure following single project layout

## Context Documents in This Feature Folder:
- **research.md**: Technology decisions and integration patterns (lines 72-241)
- **data-model.md**: Entity definitions and validation rules (lines 1-178)
- **contracts/**: API contracts for AgentManager, AgentBuilder, discovery patterns
- **quickstart.md**: Validation scenarios and container testing approach (lines 244-331)
- **plan.md**: Constitutional approach and validation strategy (lines 60-66, 201-211)

## Phase 3.1: Setup
- [x] T001 Create app/agents/ folder structure following research.md lines 107-123 (base.py, registry.py, manager.py, builder.py, decorators.py, definitions/, templates/, __init__.py)
- [x] T002 [P] Verify Python dependencies from research.md lines 194-200 available (importlib, inspect, pathlib, dataclasses, enum, logging)
- [x] T003 [P] Configure discovery logging per research.md lines 99-105 with existing app.utils.log logger

## Phase 3.2: Core Data Models (Based on data-model.md entities)
- [x] T004 [P] DiscoveryPattern enum per data-model.md lines 47-55 with priority values (DECORATOR=1, CONVENTION=2, CONFIGURATION=3) in app/agents/base.py
- [x] T005 [P] AgentMetadata dataclass per data-model.md lines 5-25 with validation rules in app/agents/base.py
- [x] T006 [P] AgentDefinition dataclass per data-model.md lines 27-45 with factory function and relationships in app/agents/base.py
- [x] T007 [P] AgentFilter dataclass per data-model.md lines 57-68 for discovery criteria in app/agents/base.py

## Phase 3.3: Registry Implementation (Core Infrastructure)
- [x] T008 AgentRegistry singleton class per research.md lines 21-32 with __new__ pattern following app/models/provider_registry.py:57-126 in app/agents/registry.py
- [x] T009 Registry discovery path management per research.md lines 125-131 and initialization in app/agents/registry.py
- [x] T010 Registry decorator pattern discovery per contracts/discovery_patterns.py lines 46-58 using inspect module in app/agents/registry.py
- [x] T011 Registry convention pattern discovery per contracts/discovery_patterns.py lines 69-86 (*_agent.py files) using importlib in app/agents/registry.py
- [x] T012 Registry configuration pattern discovery per contracts/discovery_patterns.py lines 147-170 (AGENT_CONFIG exports) in app/agents/registry.py
- [x] T013 Registry validation and error handling per research.md lines 214-221 with graceful degradation in app/agents/registry.py
- [x] T014 Registry caching per research.md lines 183-190 and file modification time tracking per research.md lines 135-142 for hot reload in app/agents/registry.py

## Phase 3.4: Agent Builder Implementation
- [x] T015 [P] AgentBuilder class per data-model.md lines 70-86 with fluent API initialization per research.md lines 34-45 in app/agents/builder.py
- [x] T016 [P] Builder model integration (with_model) per contracts/agent_builder_api.py lines 17-35 using ModelFactory patterns in app/agents/builder.py
- [x] T017 [P] Builder MCP tools integration (with_mcp) per contracts/agent_builder_api.py lines 38-52 using MCPManager.get() per research.md lines 91-97 in app/agents/builder.py
- [x] T018 [P] Builder database integration (with_db, with_vector_db) per contracts/agent_builder_api.py lines 70-97 using PostgresSettings per research.md lines 83-89 in app/agents/builder.py
- [x] T019 [P] Builder memory and tools integration (with_memory, with_tools) per contracts/agent_builder_api.py lines 54-68, 104-119 in app/agents/builder.py
- [x] T020 [P] Builder instructions and configuration (with_instructions, with_metadata, with_config) per contracts/agent_builder_api.py lines 121-180 in app/agents/builder.py
- [x] T021 Builder build() method per contracts/agent_builder_api.py lines 182-197 creating Agno Agent instances in app/agents/builder.py

## Phase 3.5: Manager Implementation
- [x] T022 AgentManager class per research.md lines 74-81 facade following ModelFactory pattern from app/models/factory.py:23-36 in app/agents/manager.py
- [x] T023 Manager discovery control methods per contracts/agent_manager_api.py lines 27-48, 161-168 (discover, refresh) in app/agents/manager.py
- [x] T024 Manager retrieval methods per contracts/agent_manager_api.py lines 50-85 (get_all, get, get_enabled) in app/agents/manager.py
- [x] T025 Manager filtering methods per contracts/agent_manager_api.py lines 87-121 (get_by_tags, get_by_pattern) in app/agents/manager.py
- [x] T026 Manager agent lifecycle control per contracts/agent_manager_api.py lines 123-159 (enable, disable) in app/agents/manager.py
- [x] T027 Manager agent creation methods per contracts/agent_manager_api.py lines 170-201 (create_agent, create_enabled_agents) in app/agents/manager.py

## Phase 3.6: Discovery Patterns Implementation
- [x] T028 [P] @register_agent decorator per contracts/discovery_patterns.py lines 20-44 implementation in app/agents/decorators.py

## Phase 3.7: Integration
- [x] T029 Public API exports per research.md lines 113-114 (AgentManager, register_agent, AgentBuilder) in app/agents/__init__.py
- [x] T030 Update AgentOS integration per quickstart.md lines 145-162 in app/server.py replacing manual agent list with AgentManager.create_enabled_agents()

## Phase 3.8: Migration
- [x] T031 Create app/agents/definitions/ folder per research.md lines 125-131 with __init__.py
- [x] T032 Migrate existing docs_agent.py per quickstart.md lines 31-49 to AgentBuilder pattern in app/agents/definitions/docs_agent.py
- [ ] T033 Remove old app/agents/docs_agent.py file after migration verification
- [ ] T034 Create agent templates per quickstart.md lines 51-88 and examples in app/agents/templates/

## Phase 3.9: Container Validation (No test files - runtime validation only)
- [ ] T035 Create example agents for each discovery pattern in app/agents/definitions/ for validation
- [ ] T036 Container restart validation: docker-compose up --build and verify discovery logs
- [ ] T037 Runtime validation: verify agents discovered through application startup
- [ ] T038 Quickstart scenario execution: run quickstart.md steps for validation
- [ ] T039 Performance validation: verify <100ms discovery overhead during startup
- [ ] T040 Backward compatibility validation: ensure existing agent functionality preserved

## Dependencies

### Sequential Dependencies (Same File)
- T001 blocks all tasks (folder structure required)
- T008 → T009 → T010,T011,T012 → T013,T014 (registry implementation order)
- T015 → T016,T017,T018,T019,T020 → T021 (builder implementation order)
- T022 → T023,T024,T025,T026 → T027 (manager implementation order)

### Cross-File Dependencies
- T004-T007 must complete before T008 (registry needs base types)
- T008 must complete before T022 (manager needs registry)
- T015 must complete before T029 (exports need builder)
- T022 must complete before T029 (exports need manager)
- T028 must complete before T029 (exports need decorator)
- T029 must complete before T030,T032 (integration needs public API)
- T030,T032 must complete before T035-T040 (validation needs implementation)

### Independent Parallel Groups
- T002,T003 (setup tasks after T001)
- T004,T005,T006,T007 (base types - different entities)
- T016,T017,T018,T019,T020 (builder methods after T015)
- T028 (decorator - independent file)
- T035,T036,T037,T038,T039,T040 (validation tasks after implementation)

## Parallel Execution Examples

### Base Types Creation (T004-T007):
```
Task: "DiscoveryPattern enum with priority values (DECORATOR=1, CONVENTION=2, CONFIGURATION=3) in app/agents/base.py"
Task: "AgentMetadata dataclass with validation rules in app/agents/base.py"
Task: "AgentDefinition dataclass with factory function and relationships in app/agents/base.py"
Task: "AgentFilter dataclass for discovery criteria in app/agents/base.py"
```

### Builder Methods (T016-T020):
```
Task: "Builder model integration (with_model) using ModelFactory patterns in app/agents/builder.py"
Task: "Builder MCP tools integration (with_mcp) using MCPManager.get() in app/agents/builder.py"
Task: "Builder database integration (with_db, with_vector_db) using PostgresSettings in app/agents/builder.py"
Task: "Builder memory and tools integration (with_memory, with_tools) in app/agents/builder.py"
Task: "Builder instructions and configuration (with_instructions, with_metadata, with_config) in app/agents/builder.py"
```

### Validation Tasks (T035-T040):
```
Task: "Create example agents for each discovery pattern in app/agents/definitions/ for validation"
Task: "Container restart validation: docker-compose up --build and verify discovery logs"
Task: "Runtime validation: verify agents discovered through application startup"
Task: "Quickstart scenario execution: run quickstart.md steps for validation"
Task: "Performance validation: verify <100ms discovery overhead during startup"
Task: "Backward compatibility validation: ensure existing agent functionality preserved"
```

## Implementation Notes

### Key Reference Patterns:
- **Registry Singleton**: Follow `app/models/provider_registry.py:57-126`
- **Factory Facade**: Follow `app/models/factory.py:23-36`
- **Caching**: Follow `app/tools/mcp/manager.py:19-24`
- **Error Handling**: Follow `app/tools/mcp/manager.py:28-29`
- **Agent Creation**: Extend `app/agents/docs_agent.py:15-57`

### Validation Approach:
- **NO test files created** (following KISS principle)
- **Container-based validation** via Docker restart
- **Runtime discovery testing** through application startup
- **Log output verification** for discovery success/failure
- **Performance measurement** during actual system operation

### Success Criteria:
- Zero configuration required for basic usage
- <100ms discovery overhead on startup
- All existing agents continue to work
- Clear error messages for malformed agents
- Hot reload works in development mode
- Container restart shows successful discovery logs

## Notes
- Container-based validation preferred over mock/unit tests
- Real system integration testing through FastAPI runtime
- Hot reload compatibility maintained throughout
- Backward compatibility with existing agents required
- Discovery logging provides validation feedback