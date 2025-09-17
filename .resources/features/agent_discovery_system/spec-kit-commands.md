# Agent Discovery System - Spec-Kit Commands

This document contains the complete spec-kit command sequence for implementing the Agent Discovery System.

**Reference**: See `plan.md` in this folder for the detailed technical implementation plan.

---

## Step 1: Initialize Spec (/specify command)

```
/specify

Create an Agent Discovery System for the Agno template project that automatically discovers and registers AI agents without manual configuration.

The system should allow developers to create agent files in designated folders and have them automatically discovered and registered with AgentOS at startup. Agents can be created using three methods: decorators, naming conventions, or configuration exports.

Key Requirements:
- Automatic discovery of agents in the definitions folder
- Support for three discovery patterns: decorator-based, convention-based, and configuration-based
- A fluent builder API for creating agents programmatically
- Ability to filter agents by tags, status, or custom criteria
- Dynamic enable/disable of agents at runtime
- Metadata system for agent categorization (tags, priority, enabled state)
- Lazy loading to improve startup performance
- Validation to ensure agents meet requirements before registration
- Hot reload compatibility for development mode
- Zero configuration required for basic usage

The system should integrate seamlessly with the existing AgentOS, replacing the current manual agent list in the constructor with automatically discovered agents. Developers should be able to simply create a Python file with an agent definition and have it work immediately.

User Scenarios:
1. Developer creates a new file "customer_support_agent.py" in the definitions folder, defines an agent, and it's automatically available on next startup (production) or hot reload (development)
2. Developer uses the @register_agent decorator to mark a function as an agent factory
3. Developer uses the AgentBuilder to programmatically create agents with a fluent API
4. Operations team disables specific agents in production without code changes
5. Developer filters agents by tags to load only production-ready agents
```

---

## Step 2: Clarify Specification

After the spec is created, clarify:

```
The agent discovery system should scan folders in a specific order: decorators first (highest priority), then convention-based (files ending with _agent.py), then configuration-based (AGENT_CONFIG exports).

For the builder pattern, ensure it supports method chaining for all common agent configurations including models, tools, databases, memory, instructions, and knowledge bases.

The system should maintain backward compatibility - existing agent definitions should continue to work while we migrate them to the new pattern.

Add a requirement that the discovery system should log which agents are discovered and from which pattern, to help with debugging.

The metadata system should support arbitrary key-value pairs in addition to the standard tags, priority, and enabled fields.
```

Then validate:

```
Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.
```

---

## Step 3: Generate Technical Plan (/plan command)

```
/plan

Plan the Agent Discovery System using Python 3.10+ with the following technical approach:

Technology Stack:
- Python 3.10+ with type hints
- importlib for dynamic module loading
- inspect module for decorator and function discovery
- Pydantic for configuration validation
- Standard library pathlib for file system operations
- Singleton pattern for AgentManager and Registry
- Factory pattern for agent creation

The implementation should follow the existing patterns in the codebase:
- Similar to the ModelFactory pattern in app/models/factory.py
- Similar to the provider registry pattern in app/models/provider_registry.py
- Similar to the MCP manager lazy loading in app/tools/mcp/manager.py

Use the existing Agno Agent class without modification. Create a builder that wraps Agent construction.

The discovery mechanism should use Python's importlib to dynamically import modules and inspect to find decorated functions or specific exports.

Maintain the existing PostgreSQL and vector database configurations - allow them to be used in the AgentBuilder.

Reference the detailed architecture design and folder structure from resources/features/agent_discovery_system/plan.md for implementation details.
```

---

## Step 4: Validate Plan

```
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.

Also review resources/features/agent_discovery_system/plan.md to ensure the technical details are comprehensive enough for implementation.
```

Then ask for final plan validation:

```
Review the implementation plan and verify:
1. The discovery mechanism correctly handles all three patterns (decorator, convention, config)
2. The builder pattern properly chains all methods
3. The registry uses appropriate caching to avoid re-discovery
4. The system handles import errors gracefully
5. Hot reload compatibility is maintained
6. The plan includes proper error handling for malformed agents

Check that the implementation details reference the appropriate sections for each component in resources/features/agent_discovery_system/plan.md.

Go through the checklist once more before implementation to ensure nothing is missing.
```

---

## Step 5: Generate Tasks (/tasks command)

```
/tasks

Break down the Agent Discovery System implementation into specific, actionable development tasks.

Use the technical plan in resources/features/agent_discovery_system/plan.md as reference for the detailed architecture and implementation approach.

Create a detailed task breakdown that covers:
1. Core infrastructure setup (registry, manager, builder)
2. Discovery mechanism implementation for all three patterns
3. Integration with existing AgentOS
4. Migration of current docs_agent
5. Testing and validation
6. Documentation updates

Each task should be:
- Specific and actionable
- Have clear acceptance criteria
- Include estimated effort
- Reference the relevant sections in resources/features/agent_discovery_system/plan.md
- Identify any dependencies on other tasks

The tasks should follow the three-phase migration plan outlined in the technical plan:
- Phase 1: Core Infrastructure
- Phase 2: Migration
- Phase 3: Enhanced Features
```

---

## Step 6: Context Verification

```
I need you to review and think about the tasks.md file you just created and ensure that
it outlines all tasks to such a degree that by giving this report to a new AI instance it will have all the necessary
context to pick up and continue from where we are right now
```

## Step 7: Final Implementation Command

spec-kit creates its own spec structure:

```
implement specs/[FEATURE-NUMBER]-agent-discovery-system/plan.md
```

---

## Notes for Execution

1. **Reference Files**: The technical plan in `plan.md` contains all architectural details
2. **Existing Patterns**: Implementation should follow existing patterns in the codebase
3. **Migration Strategy**: Three-phase approach ensures backward compatibility
4. **Testing**: Comprehensive testing strategy included in the plan
5. **Documentation**: Migration guide and API documentation requirements specified
