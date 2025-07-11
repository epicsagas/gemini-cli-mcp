# Development Guidelines for gemini-cli-mcp

## 1. Project Overview
- This project implements an MCP-compatible server that exposes gemini-cli's core features as MCP Tools for AI agents.
- Supports both Python and Node.js implementations.
- Key features: ask, agent, commit, pr, diff (as MCP Tools).

## 2. Project Architecture
- Root directory must contain:
    - `README.md` (project documentation)
    - `shrimp-rules.md` (this file)
    - Implementation directories for each language (e.g., `/python/`, `/nodejs/` if present)
    - `tasks.json` (task tracking)
- All MCP tool schemas and logic must be kept in sync between Python and Node.js versions.

## 3. Code Standards
- Use snake_case for Python, camelCase for JavaScript/Node.js.
- All tool names and API endpoints must follow the MCP specification exactly.
- All CLI commands must be mapped 1:1 to gemini-cli commands as described in the README.
- Add comments only for project-specific logic or non-obvious decisions.

## 4. Functionality Implementation Standards
- When adding or modifying a Tool, update both Python and Node.js implementations.
- When changing the README, update all language-specific documentation if present.
- Always update `/v1/context` and `/v1/tools` logic together when changing tool schemas.
- When adding a new MCP Tool, provide its schema, description, and input/output contract in both implementations.

## 5. Framework/Plugin/Third-party Library Usage Standards
- Use only FastAPI for Python web servers, Express.js for Node.js web servers.
- Use Typer for Python CLI, Commander.js for Node.js CLI.
- Use Poetry for Python packaging, npm for Node.js packaging.
- Do not introduce new frameworks or libraries without updating this document and the README.

## 6. Workflow Standards
- All new features must be implemented and tested in both language versions before merging.
- All git commits must follow the Conventional Commits specification.
- When modifying MCP tool logic, run integration tests for both stdio and http modes.
- When updating Dockerfile, ensure compatibility with both Python and Node.js containers if applicable.

## 7. Key File Interaction Standards
- When modifying `README.md`, update all language or platform-specific documentation files.
- When changing tool schemas, update both `/v1/context` and `/v1/tools` handlers in all implementations.
- When adding a new tool, update the tool list in the documentation and all relevant code files.

## 8. AI Decision-making Standards
- When ambiguous, always prefer updating both implementations for consistency.
- If a rule or file is unclear, review the codebase and documentation before making changes.
- When in doubt, prefer explicitness and update this file with new rules.
- Use imperative instructions for all new rules.

## 9. Prohibited Actions
- Do NOT include general development knowledge or explanations already known to LLMs.
- Do NOT update only one implementation (Python or Node.js) without updating the other.
- Do NOT modify tool schemas in only one place; always update all relevant files.
- Do NOT introduce new dependencies without documenting them here and in the README.

## 10. Examples
- **Correct:**
    - When adding a new tool, update both Python and Node.js code, `/v1/context`, `/v1/tools`, and documentation.
    - When changing the README, also update `/docs/` or other language-specific docs if present.
- **Incorrect:**
    - Adding a tool only in Python but not in Node.js.
    - Modifying tool schema in code but not updating the documentation or context endpoint.
    - Adding a dependency without updating this file and the README.

**All rules must be followed strictly. Update this file whenever project-specific standards change.** 