# Implementation Plan: Agent Discovery System

**Branch**: `001-create-an-agent` | **Date**: 2025-09-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-create-an-agent/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Create an Agent Discovery System that automatically discovers and registers AI agents without manual configuration. The system will support three discovery patterns (decorator-based, convention-based, configuration-based) with a fluent builder API for programmatic agent creation, enabling zero-configuration usage while maintaining backward compatibility with existing agents.

## Technical Context
**Language/Version**: Python 3.10+ with type hints
**Primary Dependencies**: importlib, inspect, Pydantic, pathlib, Agno framework (v2.0.3)
**Storage**: PostgreSQL via existing app/db/postgres configuration, PgVector for embeddings
**Testing**: pytest (to be verified in codebase)
**Target Platform**: Linux/macOS server environments, Docker containers
**Project Type**: single (agent framework extension)
**Performance Goals**: <100ms discovery overhead on startup, lazy loading for agents
**Constraints**: Zero configuration for basic usage, backward compatibility required
**Scale/Scope**: Support 50+ agents, hot reload compatibility, AgentOS integration

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (single agent framework extension)
- Using framework directly? YES (extends Agno Agent class without modification)
- Single data model? YES (AgentDefinition and AgentMetadata entities)
- Avoiding patterns? NO (using Builder, Factory, Registry patterns from existing codebase)

**Architecture**:
- EVERY feature as library? YES (agent discovery as library in app/agents/)
- Libraries listed: agent_discovery (discovery system), agent_builder (fluent API)
- CLI per library: NO (framework extension, not CLI tool)
- Library docs: YES (will follow existing patterns)

**Testing (SIMPLIFIED APPROACH)**:
- Container restart validation? YES (practical testing via Docker restart)
- KISS principle followed? YES (simple implementation over complex mocking)
- Single responsibility? YES (each module has clear, focused purpose)
- Real system validation? YES (actual agent discovery during startup)
- Avoiding mock complexity? YES (container-based validation preferred)

**Observability**:
- Structured logging included? YES (discovery process logging required)
- Frontend logs → backend? N/A (server-side framework)
- Error context sufficient? YES (detailed error handling for discovery failures)

**Versioning**:
- Version number assigned? YES (follows Agno v2.0.3 compatibility)
- BUILD increments on every change? YES (will follow project standards)
- Breaking changes handled? YES (backward compatibility maintained)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/bash/update-agent-context.sh claude` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Core modules: AgentRegistry, AgentManager, AgentBuilder, decorators [P]
- Discovery patterns: decorator, convention, configuration implementations [P]
- Integration: AgentOS integration, existing agent migration
- Validation: Container restart testing, discovery validation

**Ordering Strategy**:
- KISS approach: Implementation with container validation
- Dependency order: Registry → Manager → Builder → Discovery patterns → Integration
- Mark [P] for parallel execution (independent modules)
- Focus on single responsibility per module

**Estimated Output**: 15-20 numbered, ordered tasks in tasks.md

**Validation Strategy**:
- Container restart validation over complex unit tests
- Real system testing with actual agent creation
- Discovery process validation through logging
- AgentOS integration testing

**Hot Reload Implementation**:
- File modification time tracking (similar to MCP manager cleanup patterns)
- Registry cache invalidation on file changes
- Graceful error recovery during module reload
- Reference: `app/tools/mcp/manager.py:28-29` for cleanup patterns

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*