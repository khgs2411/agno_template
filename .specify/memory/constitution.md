# AGNO AI Constitution

## Core Principles

### 1. Agent-First Architecture

Every component serves the agent's functionality; Agents are self-contained with clear purpose and scope; Agent configuration must be declarative and version-controlled; No functionality outside the agent paradigm

### 2. MCP Integration Standard

All external tool access via MCP protocol; MCP servers must be documented and versioned; Transport layer (HTTP/stdio) clearly specified; Tool definitions follow MCP schema standards

### 3. Model Agnostic Design

Agent logic independent of specific model providers; Model configuration externalized via environment variables; Graceful degradation when model unavailable; Support for model switching without code changes

### 4. Observable and Debuggable

All agent interactions logged with context; Session history preserved and accessible; Error states clearly identified and recoverable; Request/response tracing for troubleshooting

### 5. Simplicity and Maintainability

Single responsibility per agent; Minimal dependencies and clear separation of concerns; Configuration over complex code; Human-readable agent definitions

## Security and API Requirements

### API Key Management

- All API keys externalized to environment variables
- No secrets in code or version control
- Graceful handling of missing/invalid API keys

### Agent Safety

- Input validation for all agent interactions
- Rate limiting and timeout protection
- Safe failure modes when external services unavailable
- No execution of arbitrary code without explicit user consent

## Development Standards

### Code Quality

- Follow Agno framework conventions and patterns
- Single file agent definitions preferred for simplicity
- Environment-based configuration over hardcoded values
- Clear separation between agent logic and infrastructure

### Testing Requirements

- Agent functionality must be testable in isolation
- MCP integrations require connection tests
- Model interactions should be mockable for testing
- Integration tests for complete agent workflows

### Documentation

- All agents documented with purpose, capabilities, and limitations
- MCP server configurations documented with examples
- Environment setup clearly specified
- Architecture decisions recorded in CLAUDE.md

## Governance

This constitution guides all development decisions for Agno agents; Changes require updating this document and related specifications; Complexity must be justified against simplicity principle; Use CLAUDE.md for operational development guidance

**Version**: 1.0.0 | **Ratified**: 2025-01-14 | **Last Amended**: 2025-01-14
