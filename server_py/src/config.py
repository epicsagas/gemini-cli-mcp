from dataclasses import dataclass, field
import os
from typing import Optional

@dataclass
class GeminiCLIConfig:
    model: str = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    all_files: bool = os.environ.get("GEMINI_ALL_FILES", "true").lower() == "true"
    sandbox: bool = os.environ.get("GEMINI_SANDBOX", "true").lower() == "true"
    api_key: Optional[str] = os.environ.get("GEMINI_API_KEY")
    query_timeout: int = int(os.environ.get("QUERY_TIMEOUT", 300))
    use_shell: bool = os.environ.get("USE_SHELL", "false").lower() == "true"
    project_root: Optional[str] = os.environ.get("PROJECT_ROOT")
    debug: bool = os.environ.get("DEBUG", "false").lower() == "true"

@dataclass
class AppConfig:
    gemini_cli: GeminiCLIConfig = field(default_factory=GeminiCLIConfig)

def load_config() -> AppConfig:
    return AppConfig()