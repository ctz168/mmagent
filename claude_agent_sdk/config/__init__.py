"""MiniMax Agent Configuration System."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class AgentConfig:
    """Main configuration for MiniMax Agent."""

    # LLM Configuration
    llm_gateway_url: str = field(default_factory=lambda: os.getenv("LLM_GATEWAY_BASE_URL", "http://10.138.255.202:8080"))
    anthropic_base_url: str = field(default_factory=lambda: os.getenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:8765"))
    default_model: str = "claude-sonnet-4-5"

    # Claude Code Configuration
    claude_code_entrypoint: str = field(default_factory=lambda: os.getenv("CLAUDE_CODE_ENTRYPOINT", "sdk-py-client"))
    permission_mode: str = "default"

    # Workspace Configuration
    workspace_dir: str = field(default_factory=lambda: os.getenv("WORKSPACE_DIR", "/workspace"))
    python_path: str = field(default_factory=lambda: os.getenv("PYTHONPATH", "/workspace:/app"))

    # Browser Configuration
    display: str = field(default_factory=lambda: os.getenv("DISPLAY", ":99"))
    playwright_browsers_path: str = field(default_factory=lambda: os.getenv("PLAYWRIGHT_BROWSERS_PATH", "/opt/playwright-browsers"))

    # Python Environment
    uv_index_url: str = field(default_factory=lambda: os.getenv("UV_INDEX_URL", "http://mirrors.cloud.aliyuncs.com/pypi/simple"))
    uv_project_environment: str = field(default_factory=lambda: os.getenv("UV_PROJECT_ENVIRONMENT", "/tmp/.venv"))

    # MCP Servers
    mcp_servers: dict[str, dict[str, Any]] = field(default_factory=dict)

    # Tool Configuration
    allowed_tools: list[str] = field(default_factory=lambda: [
        "bash", "browser", "file", "search", "code", "git"
    ])
    max_tool_calls: int = 100
    tool_timeout: int = 300

    # Environment Info
    env_name: Optional[str] = field(default_factory=lambda: os.getenv("ENV_NAME"))
    agent_type: Optional[str] = field(default_factory=lambda: os.getenv("AGENT_TYPE"))
    idc: Optional[str] = field(default_factory=lambda: os.getenv("IDC"))

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create configuration from environment variables."""
        return cls()

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "llm_gateway_url": self.llm_gateway_url,
            "anthropic_base_url": self.anthropic_base_url,
            "default_model": self.default_model,
            "claude_code_entrypoint": self.claude_code_entrypoint,
            "permission_mode": self.permission_mode,
            "workspace_dir": self.workspace_dir,
            "python_path": self.python_path,
            "display": self.display,
            "playwright_browsers_path": self.playwright_browsers_path,
            "uv_index_url": self.uv_index_url,
            "uv_project_environment": self.uv_project_environment,
            "mcp_servers": list(self.mcp_servers.keys()),
            "allowed_tools": self.allowed_tools,
            "max_tool_calls": self.max_tool_calls,
            "tool_timeout": self.tool_timeout,
            "env_name": self.env_name,
            "agent_type": self.agent_type,
            "idc": self.idc,
        }

    def validate(self) -> list[str]:
        """Validate configuration and return list of warnings."""
        warnings = []

        if not Path(self.workspace_dir).exists():
            warnings.append(f"Workspace directory does not exist: {self.workspace_dir}")

        if not Path(self.playwright_browsers_path).exists():
            warnings.append(f"Playwright browsers path does not exist: {self.playwright_browsers_path}")

        return warnings


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    type: str = "stdio"  # stdio, sse, streamable-http
    command: Optional[str] = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to MCP server configuration dict."""
        result: dict[str, Any] = {"type": self.type}

        if self.type == "stdio":
            result["command"] = self.command
            result["args"] = self.args
            result["env"] = self.env
        elif self.type in ("sse", "streamable-http"):
            result["url"] = self.url

        return result


class ConfigManager:
    """Manager for loading and saving agent configuration."""

    def __init__(self, config_dir: str = "/workspace/.minimax"):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.json"

    def load(self) -> AgentConfig:
        """Load configuration from file."""
        if not self.config_file.exists():
            return AgentConfig()

        import json
        with open(self.config_file) as f:
            data = json.load(f)

        return AgentConfig(**data)

    def save(self, config: AgentConfig) -> None:
        """Save configuration to file."""
        import json
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "w") as f:
            json.dump(config.to_dict(), f, indent=2)
