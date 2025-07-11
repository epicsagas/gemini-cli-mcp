# `gemini-cli-mcp` Node.js Server

This directory contains the Node.js (TypeScript) implementation of the `gemini-cli-mcp` server. It uses FastMCP to expose `gemini-cli` functionalities as MCP-compliant tools.

## 1. Features

This server exposes the following `gemini-cli` commands as MCP Tools:

*   `gemini_ask`: Ask a question to the Gemini model.
*   `gemini_agent`: Run a complex prompt with Gemini Agent in auto-execution (`--yolo`) mode.

> **Note:** Git-related tools (`gemini_git_commit`, `gemini_git_pr`, `gemini_git_diff`) are not implemented in the Node.js version by design.

## 2. Technology Stack

| Category         | Technology           |
| :--------------- | :------------------- |
| **Language**     | TypeScript (Node.js) |
| **Web Framework**| FastMCP              |
| **Process Exec** | `child_process.spawn`|
| **Config**       | dotenvx              |
| **Packaging**    | npm                  |

## 3. Setup

### Prerequisites

*   Node.js 18 or higher.
*   `gemini-cli` installed globally and accessible in your system's PATH.
*   `git` installed and configured (if needed for your project).

### Installation

1.  Navigate to the `server_node` directory:
    ```bash
    cd server_node
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the project:
    ```bash
    npm run build
    ```

### Environment Variables

The server uses environment variables for configuration. You can set these in a `.env` file in the project root (`/path/to/server_node/.env`) or directly in your environment. See `.env.example` for details.

*   `GEMINI_MODEL`: Specifies the Gemini model to use (e.g., `gemini-2.5-flash`).
*   `GEMINI_ALL_FILES`: Set to `true` to include all files in context (`--all-files`).
*   `GEMINI_SANDBOX`: Set to `true` to enable sandbox mode (`--sandbox`).
*   `GEMINI_API_KEY`: Your Gemini API key (required for Docker/server environments).
*   `PROJECT_ROOT`: The root directory of your project (important for `gemini-cli` operations).
*   `QUERY_TIMEOUT`: Timeout for `gemini-cli` commands in seconds.
*   `USE_SHELL`: Set to `true` to execute `gemini-cli` commands via shell (defaults to `false`).

## 4. Running the Server

You can select the execution mode via the `MCP_TRANSPORT` environment variable or npm scripts.

*   **STDIO Mode**: 
    ```bash
    npm run start:stdio
    # or
    MCP_TRANSPORT=stdio node dist/main.js
    ```
*   **HTTP Mode**: 
    ```bash
    npm start
    # or
    MCP_TRANSPORT=httpStream node dist/main.js
    ```

> **Note:** The default port for HTTP mode is 8000. Use `MCP_TRANSPORT` to switch modes.

## 5. Tool Usage

The server acts as a smart wrapper around `gemini-cli`. It constructs and executes the appropriate `gemini-cli` command based on the MCP tool invocation.

For example:
*   `gemini_ask(question="What is AI?")` translates to `gemini ask --model {model} --all-files --sandbox --prompt "What is AI?"`
*   `gemini_agent(prompt="Do something complex.")` translates to `gemini agent --model {model} --all-files --sandbox --yolo --prompt "Do something complex."`

## 6. MCP Client Integration Guide

The `gemini-cli-mcp` server supports both HTTP and STDIO modes. Below are instructions and configuration examples for integrating as an external MCP server in clients like Cursor, Windsurf, and Claude Code.

### 6.1 Integration via HTTP Mode

1. **Start the server**
   ```bash
   npm start
   # or
   MCP_TRANSPORT=httpStream node dist/main.js
   ```
   - Default port is `8000`.

2. **Register the MCP server in your client**
   - MCP server URL: `http://localhost:8000` (or your server's IP)

#### Cursor, Windsurf Example
```json
{
  "mcpServers": {
    "gemini-cli-mcp": {
      "url": "http://localhost:8000"
    }
  }
}
```

---

### 6.2 Integration via STDIO Mode

1. **No need to start the server manually**
   - The MCP client will launch the process and communicate via STDIO.
   - Just register the following configuration.

#### Cursor, Windsurf Example
```json
{
  "mcpServers": {
    "gemini-cli-mcp": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/project_root/server_node/dist/main.js"],
      "env": {
        "GEMINI_MODEL": "gemini-2.5-flash",
        "PROJECT_ROOT": "/path/to/project_root"
      }
    }
  }
}
```

#### Claude Code Example
```json
{
  "mcpServers": {
    "gemini-cli-mcp": {
      "command": "node",
      "args": ["/path/to/project_root/server_node/dist/main.js"],
      "env": {
        "GEMINI_API_KEY": "your_api_key",
        "GEMINI_MODEL": "gemini-2.5-flash",
        "PROJECT_ROOT": "/path/to/project_root"
      }
    }
  }
}
```

---

> **Notes:**
> - HTTP mode allows multiple clients to connect over the network.
> - STDIO mode launches a separate process per client.
> - Adjust environment variables (`env`) as needed for your use case.
> - If the server and client are on different machines, ensure firewall/port forwarding is configured appropriately.

## 7. Development & Testing

- Build: `npm run build`
- Test: `npm test` (add tests in `tests/` directory)
- Lint/Format: (add as needed)

## 8. Packaging & Distribution

- Update `package.json` with correct metadata before publishing.
- Publish to npm: `npm publish`
- Follow npm best practices for versioning and security.