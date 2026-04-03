"""File Operations Tool for Agent Workspace."""

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class FileToolConfig:
    """Configuration for file operations tool."""

    workspace_root: str = "/workspace"
    allowed_extensions: Optional[list[str]] = None
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    blocked_patterns: list[str] = field(default_factory=lambda: [".git", "__pycache__", "node_modules"])


class FileTool:
    """
    File operations tool for safe file manipulation in workspace.

    Provides methods for:
    - Reading files (text, binary)
    - Writing files
    - Listing directory contents
    - File metadata
    - Safe path operations
    """

    def __init__(self, config: Optional[FileToolConfig] = None):
        """Initialize file tool with configuration."""
        self.config = config or FileToolConfig()

    def _safe_path(self, path: str) -> Path:
        """Resolve and validate path within workspace."""
        resolved = Path(path).resolve()
        root = Path(self.config.workspace_root).resolve()

        if not str(resolved).startswith(str(root)):
            raise ValueError(f"Path {path} is outside workspace")

        for pattern in self.config.blocked_patterns:
            if pattern in resolved.parts:
                raise ValueError(f"Path contains blocked pattern: {pattern}")

        return resolved

    def read(self, path: str, binary: bool = False) -> dict[str, Any]:
        """
        Read file contents.

        Args:
            path: File path relative to workspace
            binary: Read as binary if True

        Returns:
            File content and metadata
        """
        safe_path = self._safe_path(path)

        if not safe_path.exists():
            return {"success": False, "error": "File not found"}

        if safe_path.is_dir():
            return {"success": False, "error": "Path is a directory"}

        file_size = safe_path.stat().st_size
        if file_size > self.config.max_file_size:
            return {"success": False, "error": f"File too large: {file_size} bytes"}

        try:
            if binary:
                content = safe_path.read_bytes()
                return {"success": True, "content": content, "size": file_size}
            else:
                content = safe_path.read_text(encoding="utf-8")
                return {"success": True, "content": content, "size": file_size}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def write(self, path: str, content: str | bytes) -> dict[str, Any]:
        """
        Write file contents.

        Args:
            path: File path relative to workspace
            content: Content to write

        Returns:
            Write result with success status
        """
        safe_path = self._safe_path(path)

        try:
            safe_path.parent.mkdir(parents=True, exist_ok=True)

            if isinstance(content, bytes):
                safe_path.write_bytes(content)
            else:
                safe_path.write_text(content, encoding="utf-8")

            return {"success": True, "path": str(safe_path), "size": safe_path.stat().st_size}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list(self, path: str = ".", recursive: bool = False) -> dict[str, Any]:
        """
        List directory contents.

        Args:
            path: Directory path relative to workspace
            recursive: List subdirectories recursively

        Returns:
            Directory listing
        """
        safe_path = self._safe_path(path)

        if safe_path.exists() and not safe_path.is_dir():
            return {"success": False, "error": "Path is not a directory"}

        try:
            entries = []
            if recursive:
                for item in safe_path.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(safe_path)
                        entries.append({
                            "name": item.name,
                            "path": str(rel_path),
                            "size": item.stat().st_size,
                            "type": "file"
                        })
            else:
                for item in safe_path.iterdir():
                    entries.append({
                        "name": item.name,
                        "path": item.name,
                        "size": item.stat().st_size if item.is_file() else 0,
                        "type": "directory" if item.is_dir() else "file"
                    })

            return {"success": True, "entries": entries, "path": str(safe_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def info(self, path: str) -> dict[str, Any]:
        """
        Get file/directory information.

        Args:
            path: Path relative to workspace

        Returns:
            File metadata
        """
        safe_path = self._safe_path(path)

        if not safe_path.exists():
            return {"success": False, "error": "Path not found"}

        stat = safe_path.stat()
        return {
            "success": True,
            "path": str(safe_path.relative_to(Path(self.config.workspace_root))),
            "name": safe_path.name,
            "type": "directory" if safe_path.is_dir() else "file",
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_readable": os.access(safe_path, os.R_OK),
            "is_writable": os.access(safe_path, os.W_OK),
        }

    def exists(self, path: str) -> bool:
        """Check if path exists."""
        try:
            safe_path = self._safe_path(path)
            return safe_path.exists()
        except ValueError:
            return False

    def delete(self, path: str) -> dict[str, Any]:
        """
        Delete file or directory.

        Args:
            path: Path relative to workspace

        Returns:
            Delete result
        """
        safe_path = self._safe_path(path)

        if not safe_path.exists():
            return {"success": False, "error": "Path not found"}

        try:
            if safe_path.is_dir():
                shutil.rmtree(safe_path)
            else:
                safe_path.unlink()
            return {"success": True, "path": str(safe_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def copy(self, src: str, dst: str) -> dict[str, Any]:
        """
        Copy file or directory.

        Args:
            src: Source path
            dst: Destination path

        Returns:
            Copy result
        """
        src_path = self._safe_path(src)
        dst_path = self._safe_path(dst)

        if not src_path.exists():
            return {"success": False, "error": "Source not found"}

        try:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            return {"success": True, "src": str(src_path), "dst": str(dst_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
