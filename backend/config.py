"""Configuration management for Agent API."""

import os
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

    # Workspace
    workspace_dir: str = "/workspace"
    python_path: str = "/workspace:/app"

    # Browser
    display: str = ":99"
    playwright_browsers_path: str = "/opt/playwright-browsers"

    # Python Environment
    uv_index_url: str = "http://mirrors.cloud.aliyuncs.com/pypi/simple"
    uv_project_environment: str = "/tmp/.venv"

    # CORS
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
