"""Configuration management for Agent API."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    # LLM Configuration
    llm_gateway_url: str = "http://10.138.255.202:8080"
    anthropic_base_url: str = "http://127.0.0.1:8765"
    default_model: str = "claude-sonnet-4-5"
    claude_code_entrypoint: str = "sdk-py-client"

    # Workspace - Use environment variable or default to project directory
    workspace_dir: str = os.getenv("WORKSPACE_DIR", "/workspace")

    # Python Path - Include project root for SDK imports
    @property
    def python_path(self) -> str:
        """Get Python path with project root included."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.getenv("PYTHONPATH", "")
        paths = [project_root]
        if env_path:
            paths.append(env_path)
        return ":".join(paths)

    # Engine Configuration
    engine_dir: str = os.getenv("ENGINE_DIR", "/workspace/mmagent/engine")

    # Browser Configuration
    display: str = os.getenv("DISPLAY", ":99")
    playwright_browsers_path: Optional[str] = os.getenv("PLAYWRIGHT_BROWSERS_PATH")

    # Python Environment
    uv_index_url: Optional[str] = os.getenv("UV_INDEX_URL")
    uv_project_environment: str = os.getenv("UV_PROJECT_ENVIRONMENT", "/tmp/.venv")

    # CORS
    cors_origins: list[str] = ["*"]

    # Claude Code CLI Path
    claude_cli_path: Optional[str] = os.getenv("CLAUDE_CODE_CLI_PATH")

    # Tool Configuration
    bash_timeout: int = int(os.getenv("BASH_TIMEOUT", "300"))
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_workspace_dir() -> str:
    """Get the workspace directory, creating it if necessary."""
    workspace = settings.workspace_dir
    Path(workspace).mkdir(parents=True, exist_ok=True)
    return workspace


def get_engine_dir() -> str:
    """Get the engine directory."""
    return settings.engine_dir


def get_claude_cli_path() -> str:
    """Get the Claude CLI path."""
    if settings.claude_cli_path:
        return settings.claude_cli_path

    # Try to find Claude CLI in common locations
    possible_paths = [
        "/workspace/mmagent/engine/claude",
        "/workspace/mmagent/bin/claude",
        "/usr/local/bin/claude",
        os.path.expanduser("~/.npm-global/bin/claude"),
    ]

    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    # Fallback to 'claude' command in PATH
    return "claude"
