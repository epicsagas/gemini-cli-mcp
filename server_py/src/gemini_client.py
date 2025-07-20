import subprocess
import os
import shlex
import logging
from typing import Dict, Any, Optional

from src.config import GeminiCLIConfig

logger = logging.getLogger("gemini-cli-mcp")

class GeminiClientError(Exception):
    """Custom exception for GeminiClient errors."""
    pass

class GeminiClient:
    def __init__(self, config: GeminiCLIConfig):
        self.config = config

    def _verify_gemini_executable(self):
        """Verifies if the gemini executable is in PATH."""
        try:
            subprocess.run(["which", "gemini"], check=True, capture_output=True)
        except FileNotFoundError:
            raise GeminiClientError("gemini executable not found in PATH. Please ensure gemini-cli is installed and in your system's PATH.")
        except subprocess.CalledProcessError as e:
            raise GeminiClientError(f"Error checking gemini executable: {e.stderr.decode().strip()}")

    def _build_gemini_command(self, command_type: str, prompt: str, extra_args: Optional[list[str]] = None) -> list[str]:
        """Builds the gemini CLI command with common flags and tool-specific arguments."""
        cmd = ["gemini", command_type]

        if self.config.model:
            cmd.extend(["--model", self.config.model])
        if self.config.all_files:
            cmd.append("--all-files")
        if self.config.sandbox:
            cmd.append("--sandbox")

        if extra_args:
            cmd.extend(extra_args)

        cmd.extend(["--prompt", prompt])

        return cmd

    def _process_gemini_output(self, output: str) -> str:
        """Filters out unwanted messages from gemini CLI output."""
        lines = output.splitlines()
        filtered_lines = [
            line for line in lines 
            if "Loaded cached credentials." not in line.strip() and 
            not line.strip().startswith("[DEBUG]") and 
            "Flushing log events to Clearcut." not in line.strip()
        ]
        return "\n".join(filtered_lines).strip()

    def run_command(self, command_type: str, prompt: str, extra_args: Optional[list[str]] = None) -> Dict[str, Any]:
        """Executes a gemini CLI command and returns its output."""
        self._verify_gemini_executable()

        cmd = self._build_gemini_command(command_type, prompt, extra_args)

        full_env = os.environ.copy()
        if self.config.api_key:
            full_env["GEMINI_API_KEY"] = self.config.api_key
        
        # Set common environment variables for consistent behavior
        full_env["PYTHONUNBUFFERED"] = "1"
        full_env["LC_ALL"] = "C.UTF-8"
        full_env["LANG"] = "C.UTF-8"
        full_env["HOME"] = os.environ.get("HOME", "/tmp") # Ensure HOME is set for gemini-cli
        full_env["TERM"] = os.environ.get("TERM", "xterm-256color")
        full_env["COLORTERM"] = os.environ.get("COLORTERM", "truecolor")
        full_env["NODE_OPTIONS"] = "--no-warnings" # Suppress Node.js warnings if gemini-cli uses Node.js

        logger.debug(f"Running command: {' '.join(shlex.quote(arg) for arg in cmd)}")
        logger.debug(f"Environment variables: {full_env}")
        if self.config.debug:
            logger.debug("Processes before gemini command:")
            try:
                ps_before = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
                logger.debug(ps_before.stdout)
            except Exception as e:
                logger.debug(f"Could not run ps before: {e}")

        try:
            # Use shlex.quote for shell=True to correctly parse the command string
            # Otherwise, pass cmd as a list for shell=False
            process_cmd = ' '.join(shlex.quote(arg) for arg in cmd) if self.config.use_shell else cmd

            result = subprocess.run(
                process_cmd,
                capture_output=True,
                text=True,
                env=full_env,
                timeout=self.config.query_timeout,
                shell=self.config.use_shell,
                cwd=self.config.project_root if self.config.project_root else os.getcwd()
            )

            stdout = self._process_gemini_output(result.stdout)
            stderr = result.stderr.strip()
            returncode = result.returncode

            if self.config.debug:
                logger.debug(f"stdout: {stdout}")
                logger.debug(f"stderr: {stderr}")
                logger.debug(f"returncode: {returncode}")

            return {"stdout": stdout, "stderr": stderr, "returncode": returncode}

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {self.config.query_timeout}s: {' '.join(shlex.quote(arg) for arg in cmd)}")
            raise GeminiClientError(f"Command timed out after {self.config.query_timeout}s")
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with error: {e.stderr}")
            raise GeminiClientError(e.stderr.strip())
        except Exception as e:
            logger.error(f"Error running command: {e}")
            raise GeminiClientError(f"An unexpected error occurred: {str(e)}")
        finally:
            if self.config.debug:
                logger.debug("Processes after gemini command:")
                try:
                    ps_after = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
                    logger.debug(ps_after.stdout)
                except Exception as e:
                    logger.debug(f"Could not run ps after: {e}")