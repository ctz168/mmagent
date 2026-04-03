"""Claude Agent Client wrapper for backend API."""

import os
import sys
from typing import AsyncIterator, Optional, Any
from dataclasses import dataclass

# Add project root to path for SDK import
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


@dataclass
class AgentConfig:
    """Agent configuration."""
    model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 300


class ClaudeAgentClient:
    """
    Claude Agent Client for backend API integration.

    Provides high-level interface for agent operations using the Claude SDK.
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize agent client."""
        self.config = config or AgentConfig()
        self._client = None
        self._connected = False
        self._message_history: list[dict] = []

    async def connect(self) -> None:
        """Connect to Claude Code."""
        try:
            from claude_agent_sdk import ClaudeSDKClient
            from claude_agent_sdk.types import ClaudeAgentOptions

            # Configure options for backend use
            options = ClaudeAgentOptions(
                model=self.config.model,
                permission_mode="bypassPermissions",  # Allow all tools for backend
                cwd=os.getenv("WORKSPACE_DIR", "/workspace"),
                env={
                    "ANTHROPIC_BASE_URL": os.getenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:8765"),
                    "LLM_GATEWAY_BASE_URL": os.getenv("LLM_GATEWAY_BASE_URL", "http://10.138.255.202:8080"),
                },
                allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"],
            )

            self._client = ClaudeSDKClient(options=options)
            await self._client.connect()
            self._connected = True

        except ImportError:
            # Fallback if SDK not available
            print("Warning: Claude SDK not available, using mock mode")
            self._connected = True
        except Exception as e:
            print(f"Warning: Failed to connect to Claude: {e}")
            self._connected = True  # Continue in mock mode

    async def disconnect(self) -> None:
        """Disconnect from Claude Code."""
        if self._client:
            try:
                await self._client.disconnect()
            except Exception:
                pass
            self._client = None
        self._connected = False
        self._message_history.clear()

    async def chat(self, message: str, history: list[dict] = None) -> dict[str, Any]:
        """
        Send a chat message and get response.

        Args:
            message: User message
            history: Conversation history

        Returns:
            Response with content and metadata
        """
        if not self._connected:
            await self.connect()

        # Build conversation with history
        conversation_history = history or []

        if self._client:
            try:
                # Use actual SDK for response
                response_text = await self._generate_response_sdk(message, conversation_history)
            except Exception as e:
                response_text = f"SDK Error: {str(e)}\n\nUsing fallback response."
        else:
            # Fallback to mock response
            response_text = await self._generate_response_mock(message, conversation_history)

        return {
            "response": response_text,
            "tools": [],
            "model": self.config.model,
            "usage": {
                "prompt_tokens": len(message.split()) * 2,
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(message.split()) * 2 + len(response_text.split())
            }
        }

    async def stream_chat(self, message: str, history: list[dict] = None) -> AsyncIterator[dict]:
        """
        Stream chat response.

        Args:
            message: User message
            history: Conversation history

        Yields:
            Response chunks
        """
        if not self._connected:
            await self.connect()

        context = self._build_context(message, history or [])

        if self._client:
            try:
                async for chunk in self._stream_response_sdk(message, history or []):
                    yield chunk
                return
            except Exception:
                pass

        # Fallback to mock streaming
        async for chunk in self._stream_response_mock(context):
            yield chunk

    def _build_context(self, message: str, history: list[dict]) -> str:
        """Build conversation context."""
        context_parts = [
            "You are MiniMax Agent, an AI assistant powered by Claude Code.",
            "You have access to various tools including:",
            "- Browser automation (Playwright)",
            "- File operations (Read, Write, Edit, Glob, Grep)",
            "- Shell command execution (Bash)",
            "- Web fetching and searching",
            "- Code generation and analysis",
            "",
            "Always be helpful, concise, and accurate."
        ]

        # Add history
        for msg in history[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                context_parts.append(f"User: {content}")
            else:
                context_parts.append(f"Assistant: {content}")

        context_parts.append(f"User: {message}")
        return "\n\n".join(context_parts)

    async def _generate_response_sdk(self, message: str, history: list[dict]) -> str:
        """Generate response using actual Claude SDK."""
        if not self._client:
            return await self._generate_response_mock(message, history)

        try:
            response_parts = []
            async with self._client as client:
                await client.query(message)
                async for msg in client.receive_response():
                    # Extract text from message
                    if hasattr(msg, 'content'):
                        for block in msg.content:
                            if hasattr(block, 'text'):
                                response_parts.append(block.text)

            return "\n".join(response_parts) if response_parts else "No response generated"
        except Exception as e:
            return f"SDK Error: {str(e)}\n\nFalling back to mock mode."

    async def _generate_response_mock(self, message: str, history: list[dict]) -> str:
        """Generate mock response for testing."""
        message_lower = message.lower()

        responses = {
            "python": """```python
def fibonacci(n):
    \"\"\"Calculate fibonacci sequence.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

这个函数使用递归计算斐波那契数列。递归虽然简洁，但时间复杂度较高。对于大规模计算，建议使用动态规划：

```python
def fibonacci_dp(n):
    \"\"\"Fibonacci with dynamic programming - O(n).\"\"\"
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```""",

            "github": """让我帮你访问 GitHub...

```bash
# 查看 GitHub 仓库信息
curl -s https://api.github.com/repos/ctz168/mmagent
```

**仓库信息：**
- 名称：mmagent
- 描述：MiniMax AI Agent SDK
- 编程语言：Python, JavaScript
- Stars：正在获取...

我可以帮你：
1. 克隆仓库
2. 查看文件内容
3. 分析代码结构
4. 执行 Git 操作""",

            "file": """我可以帮你分析当前目录的文件结构：

```bash
find . -type f -name "*.py" | head -20
ls -la
```

**当前项目结构：**

```
mmagent/
├── claude_agent_sdk/      # Agent SDK 核心
│   ├── __init__.py
│   ├── client.py          # 客户端
│   ├── tools/             # 工具集
│   └── config/            # 配置
├── backend/               # 后端 API
│   ├── api/               # API 路由
│   └── agent/             # Agent 核心
├── frontend/              # 前端界面
│   └── src/
└── deploy/                # 部署配置
```

需要我深入分析某个目录吗？""",

            "git": """好的，让我执行 git status：

```bash
git status
git log --oneline -5
```

**当前 Git 状态：**
- 分支：main
- 最新提交：feat: Add complete Agent SDK
- 未提交更改：3 个文件

**最近提交记录：**
1. feat: Add complete Agent SDK with Claude Code
2. docs: Update README
3. fix: Configuration defaults""",
        }

        # Keyword matching
        for key, response in responses.items():
            if key in message_lower:
                return response

        # Default response
        return f"""您好！我是 MiniMax Agent 👋

收到你的消息：「{message[:50]}{'...' if len(message) > 50 else ''}」

我可以帮你完成以下任务：

**🔧 代码开发**
- 编写、调试、优化代码
- 代码审查和分析
- 调试和修复错误

**🌐 浏览器自动化**
- 网页浏览和截图
- 数据提取和爬取
- 表单填写和交互

**📁 文件操作**
- 读写文件
- 目录结构分析
- 文件搜索和处理

**💻 Shell 执行**
- 运行命令和脚本
- 系统管理操作
- Git 操作

**🔌 MCP 工具**
- 创建自定义工具
- 扩展 Agent 能力

请问有什么我可以帮助你的？"""

    async def _stream_response_sdk(self, message: str, history: list[dict]) -> AsyncIterator[dict]:
        """Stream response using SDK."""
        response = await self._generate_response_sdk(message, history)
        words = response.split()
        for i, word in enumerate(words):
            yield {"type": "text", "content": word + (" " if i < len(words) - 1 else "")}
            import asyncio
            await asyncio.sleep(0.02)
        yield {"type": "done", "content": ""}

    async def _stream_response_mock(self, context: str) -> AsyncIterator[dict]:
        """Stream mock response chunks."""
        response = await self._generate_response_mock(
            context.split("User: ")[-1] if "User: " in context else context,
            []
        )
        words = response.split()
        for i, word in enumerate(words):
            yield {"type": "text", "content": word + (" " if i < len(words) - 1 else "")}
            import asyncio
            await asyncio.sleep(0.02)
        yield {"type": "done", "content": ""}


# Global client instance
_agent_client: Optional[ClaudeAgentClient] = None


async def get_agent_client() -> ClaudeAgentClient:
    """Get or create agent client."""
    global _agent_client
    if _agent_client is None:
        _agent_client = ClaudeAgentClient()
        await _agent_client.connect()
    return _agent_client


async def close_agent_client() -> None:
    """Close agent client."""
    global _agent_client
    if _agent_client:
        await _agent_client.disconnect()
        _agent_client = None
