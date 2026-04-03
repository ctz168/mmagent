"""Bash/Shell Execution Tool for Agent."""

import asyncio
import os
import shlex
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BashToolConfig:
    """Configuration for bash execution tool."""

    timeout: int = 300  # seconds
    working_dir: str = "/workspace"
    allowed_commands: Optional[list[str]] = None
    blocked_commands: list[str] = field(default_factory=lambda: [
        "rm", "dd", "mkfs", "fdisk", "sfdisk", "parted",
        "shutdown", "reboot", "halt", "poweroff", "init"
    ])
    env_vars: dict[str, str] = field(default_factory=dict)
    capture_output: bool = True


class BashTool:
    """
    Bash/shell execution tool with security controls.

    Provides methods for:
    - Command execution
    - Output capture
    - Timeout handling
    - Environment management
    """

    def __init__(self, config: Optional[BashToolConfig] = None):
        """Initialize bash tool with configuration."""
        self.config = config or BashToolConfig()

    def _validate_command(self, command: str) -> None:
        """Validate command against security rules."""
        parts = shlex.split(command)
        if not parts:
            raise ValueError("Empty command")

        cmd = parts[0]

        # Check blocked commands
        for blocked in self.config.blocked_commands:
            if cmd == blocked or cmd.startswith(blocked + " "):
                raise ValueError(f"Command '{cmd}' is not allowed")

        # Check allowed commands if specified
        if self.config.allowed_commands and cmd not in self.config.allowed_commands:
            raise ValueError(f"Command '{cmd}' is not in allowed list")

    async def run(
        self,
        command: str,
        timeout: Optional[int] = None,
        env: Optional[dict[str, str]] = None,
        cwd: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Execute shell command.

        Args:
            command: Command to execute
            timeout: Optional timeout override
            env: Optional environment variables
            cwd: Optional working directory

        Returns:
            Execution result with stdout, stderr, return code
        """
        self._validate_command(command)

        cmd_timeout = timeout or self.config.timeout
        cmd_cwd = cwd or self.config.working_dir
        cmd_env = {**os.environ, **self.config.env_vars, **(env or {})}

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE if self.config.capture_output else asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE if self.config.capture_output else asyncio.subprocess.DEVNULL,
                cwd=cmd_cwd,
                env=cmd_env
            )

            try:
                stdout_data, stderr_data = await asyncio.wait_for(
                    process.communicate(),
                    timeout=cmd_timeout
                )

                return {
                    "success": process.returncode == 0,
                    "returncode": process.returncode,
                    "stdout": stdout_data.decode("utf-8", errors="replace") if stdout_data else "",
                    "stderr": stderr_data.decode("utf-8", errors="replace") if stderr_data else "",
                    "command": command,
                    "timeout": False,
                }
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Command timed out after {cmd_timeout} seconds",
                    "command": command,
                    "timeout": True,
                }

        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "command": command,
                "error": True,
            }

    async def run_script(self, script: str, language: str = "bash") -> dict[str, Any]:
        """
        Execute a script string.

        Args:
            script: Script content
            language: Script language ('bash', 'python', 'node')

        Returns:
            Execution result
        """
        commands = {
            "bash": ["bash", "-c"],
            "python": ["python3", "-c"],
            "node": ["node", "-e"],
        }

        if language not in commands:
            return {
                "success": False,
                "error": f"Unsupported language: {language}",
                "stdout": "",
                "stderr": f"Language '{language}' is not supported",
            }

        cmd_parts = commands[language] + [script]
        return await self.run(" ".join(shlex.quote(s) for s in cmd_parts))

    def get_env(self) -> dict[str, str]:
        """Get current environment variables."""
        return {**os.environ, **self.config.env_vars}

    def set_env(self, key: str, value: str) -> None:
        """Set environment variable for command execution."""
        self.config.env_vars[key] = value

    def unset_env(self, key: str) -> None:
        """Remove environment variable."""
        self.config.env_vars.pop(key, None)
