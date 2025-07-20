from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

from src.gemini_client import GeminiClient, GeminiClientError

class ToolManager:
    def __init__(self, mcp_server: FastMCP, gemini_client: GeminiClient):
        self.mcp = mcp_server
        self.gemini_client = gemini_client
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        def gemini_ask(question: str) -> Dict[str, Any]:
            """Ask a simple question to the Gemini model."""
            try:
                return self.gemini_client.run_command("ask", question)
            except GeminiClientError as e:
                return {"stdout": "", "stderr": str(e), "returncode": -1}

        @self.mcp.tool()
        def gemini_yolo(prompt: str) -> Dict[str, Any]:
            """Run a complex prompt with Gemini Agent in auto-execution (--yolo) mode."""
            try:
                return self.gemini_client.run_command("agent", prompt, extra_args=["--yolo"])
            except GeminiClientError as e:
                return {"stdout": "", "stderr": str(e), "returncode": -1}

        @self.mcp.tool()
        def gemini_git_diff(diff_args: Optional[str] = None) -> Dict[str, Any]:
            """Summarize code changes using Gemini AI."""
            prompt = "Summarize the code changes."
            if diff_args:
                prompt += f" Use git diff arguments: '{diff_args}'."
            try:
                return self.gemini_client.run_command("ask", prompt)
            except GeminiClientError as e:
                return {"stdout": "", "stderr": str(e), "returncode": -1}
            
        @self.mcp.tool()
        def gemini_git_commit(branch_name: Optional[str] = None) -> Dict[str, Any]:
            """Generate a conventional commit message from staged changes and perform a git commit."""
            prompt = "Generate a conventional commit message for the current staged changes and commit them."
            if branch_name:
                prompt += f" Use the branch '{branch_name}'."
            try:
                return self.gemini_client.run_command("ask", prompt)
            except GeminiClientError as e:
                return {"stdout": "", "stderr": str(e), "returncode": -1}

        @self.mcp.tool()
        def gemini_git_pr(commit_message: Optional[str] = None, branch_name: Optional[str] = None, pr_title: Optional[str] = None) -> Dict[str, Any]:
            """Automatically commit, push, and create a PR with a conventional commit message."""
            prompt = "Create a pull request with a conventional commit message."
            if commit_message:
                prompt += f" Use this commit message: '{commit_message}'."
            if branch_name:
                prompt += f" Use the branch '{branch_name}'."
            if pr_title:
                prompt += f" PR title: '{pr_title}'."
            try:
                return self.gemini_client.run_command("ask", prompt)
            except GeminiClientError as e:
                return {"stdout": "", "stderr": str(e), "returncode": -1}