"""Claude Agent Client wrapper."""

import os
import asyncio
import json
from typing import AsyncIterator, Optional, Any
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Agent configuration."""
    model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 300


class ClaudeAgentClient:
    """
    Claude Agent Client for interacting with Claude Code.

    This provides a high-level interface for agent operations.
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize agent client."""
        self.config = config or AgentConfig()
        self._query = None
        self._connected = False

    async def connect(self) -> None:
        """Connect to Claude Code."""
        # Set environment variables
        os.environ["CLAUDE_CODE_ENTRYPOINT"] = "sdk-py-client"
        os.environ["ANTHROPIC_BASE_URL"] = os.getenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:8765")

        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from Claude Code."""
        if self._query:
            await self._query.close()
            self._query = None
        self._connected = False

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

        # Build conversation context
        context = self._build_context(message, history or [])

        # Simulate response for demo (in real implementation, this would call Claude SDK)
        response = await self._generate_response(context)

        return {
            "response": response,
            "tools": [],
            "model": self.config.model,
            "usage": {
                "prompt_tokens": len(message.split()),
                "completion_tokens": len(response.split()),
                "total_tokens": len(message.split()) + len(response.split())
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

        # Stream response chunks
        async for chunk in self._stream_response(context):
            yield chunk

    def _build_context(self, message: str, history: list[dict]) -> str:
        """Build conversation context."""
        context_parts = []

        # Add system prompt
        context_parts.append(
            "You are MiniMax Agent, an AI assistant powered by Claude Code. "
            "You have access to various tools including:\n"
            "- Browser automation (Playwright)\n"
            "- File operations\n"
            "- Shell command execution\n"
            "- Code generation and analysis\n\n"
            "Always be helpful, concise, and accurate."
        )

        # Add history
        for msg in history[-10:]:  # Limit to last 10 messages
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                context_parts.append(f"User: {content}")
            else:
                context_parts.append(f"Assistant: {content}")

        # Add current message
        context_parts.append(f"User: {message}")

        return "\n\n".join(context_parts)

    async def _generate_response(self, context: str) -> str:
        """
        Generate response (placeholder for actual Claude SDK call).

        In production, this would use the Claude Agent SDK.
        """
        # Simulate processing time
        await asyncio.sleep(0.5)

        # Extract the user's actual question
        lines = context.split("\n")
        user_lines = [l for l in lines if l.startswith("User: ")]
        if user_lines:
            last_question = user_lines[-1].replace("User: ", "")

            # Generate contextual response
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

                "default": f"""您好！我是 MiniMax Agent 👋

收到你的消息：「{last_question[:50]}{'...' if len(last_question) > 50 else ''}」

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
            }

            # Simple keyword matching
            response = responses["default"]
            for key, value in responses.items():
                if key != "default" and key.lower() in last_question.lower():
                    response = value
                    break

            return response

        return responses["default"]

    async def _stream_response(self, context: str) -> AsyncIterator[dict]:
        """Stream response chunks."""
        response = await self._generate_response(context)

        # Split into words and stream
        words = response.split()
        for i, word in enumerate(words):
            yield {
                "type": "text",
                "content": word + (" " if i < len(words) - 1 else "")
            }
            await asyncio.sleep(0.02)  # Simulate streaming

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
