import os
import sys
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.config import load_config, AppConfig
from src.logging_config import setup_logging
from src.gemini_client import GeminiClient
from src.tools import ToolManager

# Get version from package metadata
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # for Python <3.8

def get_version():
    try:
        return version("gemini-cli-mcp")
    except PackageNotFoundError:
        return "unknown"

def print_help():
    print("""Usage: gemini-cli-mcp [options]\n\nOptions:\n  --version, -V    Show version information\n  --verbose, -v    Enable debug mode (set DEBUG=true)\n  --http           Run in HTTP mode (default is STDIO)\n  --help, -h       Show this help message\n""")

def print_version_and_exit():
    print(f"gemini-cli-mcp version: {get_version()}")
    try:
        import subprocess
        result = subprocess.run(["gemini", "--version"], check=True, capture_output=True, text=True)
        gemini_version = result.stdout.strip()
        if gemini_version:
            print(f"gemini version: {gemini_version}")
    except Exception:
        pass
    sys.exit(0)

# Parse CLI options
args = sys.argv[1:]

if "--help" in args or "-h" in args:
    print_help()
    sys.exit(0)

if "--version" in args or "-V" in args:
    print_version_and_exit()

if "--verbose" in args or "-v" in args:
    os.environ["DEBUG"] = "true"

# Load configuration
app_config: AppConfig = load_config()

# Setup logging
logger = setup_logging(app_config.gemini_cli.debug)

# Initialize FastMCP server
mcp_server = FastMCP("gemini-cli-mcp", version=get_version())

# Initialize GeminiClient
gemini_client = GeminiClient(app_config.gemini_cli)

# Register tools
tool_manager = ToolManager(mcp_server, gemini_client)

# FastAPI app instance for HTTP mode
app = mcp_server.app

def main():
    if "--http" in sys.argv:
        logger.info("Starting MCP server in HTTP mode...")
        # Uvicorn will be run externally, this is just for logging/setup
        # The `app` object is exposed for uvicorn to pick up
    else:
        logger.info("Starting MCP server in STDIO mode...")
        mcp_server.run(transport="stdio")

if __name__ == "__main__":
    main()