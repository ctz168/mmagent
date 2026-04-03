# MMAgent - MiniMax AI Agent SDK

A powerful Python and Node.js AI Agent framework powered by Claude Code, featuring LLM integration, browser automation, and extensible MCP tool system.

## Overview

MMAgent is a comprehensive AI Agent SDK that provides:

- **Claude SDK Integration**: Full Python SDK for interacting with Claude Code
- **LLM Gateway Support**: Built-in support for Anthropic Claude API and custom LLM gateways
- **Browser Automation**: Playwright-based web browsing and scraping
- **MCP (Model Context Protocol)**: Standardized tool and resource system
- **File Operations**: Safe workspace file manipulation
- **Shell Execution**: Secure bash command execution
- **Multi-language Support**: Python 3.12+, Node.js 18+, and Go

## Features

### Core SDK
- `ClaudeSDKClient` - Full-featured async client for Claude Code
- `query()` function - Simple one-shot queries
- Streaming support with `receive_messages()`
- Model switching and permission control
- Hook system for customization

### Tools System
- `BrowserTool` - Headless browser automation with Playwright
- `FileTool` - Safe file read/write within workspace
- `BashTool` - Secure shell command execution
- MCP Server support for extending capabilities

### Agent Capabilities
- Autonomous task execution
- Multi-turn conversations with context
- Tool calling and result processing
- Real-time response streaming
- Interruptible execution

## Installation

### Python SDK

```bash
# Clone the repository
git clone https://github.com/ctz168/mmagent.git
cd mmagent

# Install dependencies with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Node.js CLI

```bash
# Install dependencies
npm install

# Run CLI
npm start
```

## Quick Start

### Python SDK

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def main():
    # Simple query
    result = await ClaudeSDKClient.query("Hello, how are you?")
    print(result)

    # Streaming conversation
    async with ClaudeSDKClient() as client:
        await client.query("Explain Python asyncio")
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

### With Browser Automation

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, tool, create_sdk_mcp_server
from claude_agent_sdk.tools import BrowserTool, PlaywrightConfig

@tool(name="browse", description="Browse webpage", input_schema={"url": str})
async def browse(args: dict) -> dict:
    async with BrowserTool() as browser:
        await browser.navigate(args["url"])
        title = await browser.get_text("title")
        return {"content": [{"type": "text", "text": f"Title: {title}"}]}

server = create_sdk_mcp_server("browser", tools=[browse])

async with ClaudeSDKClient(options={"mcp_servers": {"browser": server}}) as client:
    await client.query("Visit example.com and tell me the title")
```

## Project Structure

```
mmagent/
├── claude_agent_sdk/          # Python SDK source
│   ├── __init__.py           # Main exports
│   ├── client.py             # Claude SDK client
│   ├── types.py              # Type definitions
│   ├── query.py              # Query utilities
│   ├── config/               # Configuration system
│   │   └── __init__.py
│   ├── tools/                # Built-in tools
│   │   ├── browser_tool.py  # Playwright browser
│   │   ├── file_tool.py     # File operations
│   │   └── bash_tool.py     # Shell execution
│   ├── _internal/           # Internal implementation
│   │   ├── client.py
│   │   ├── query.py
│   │   ├── message_parser.py
│   │   └── transport/
│   └── examples/            # Usage examples
│       ├── basic_usage.py
│       ├── browser_automation.py
│       ├── mcp_server.py
│       └── streaming_chat.py
├── cli/                     # Node.js CLI
│   └── mmagent.js
├── examples/                # Example scripts
├── tests/                   # Test suite
├── pyproject.toml           # Python package config
├── package.json             # Node.js package config
└── README.md                # This file
```

## Requirements

### Python SDK
- Python 3.12.0+
- aiohttp >= 3.11.0
- httpx >= 0.28.0
- pydantic >= 2.10.0
- playwright >= 1.52.0

### Node.js CLI
- Node.js >= 18.0.0
- npm or yarn

### Optional
- Xvfb (for headless browser)
- Playwright browsers (`npx playwright install`)

## Environment Variables

### LLM Configuration
| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_GATEWAY_BASE_URL` | Custom LLM gateway URL | `http://10.138.255.202:8080` |
| `ANTHROPIC_BASE_URL` | Anthropic API base URL | `http://127.0.0.1:8765` |

### Claude Code
| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_CODE_ENTRYPOINT` | Claude Code entry point | `sdk-py-client` |

### Workspace
| Variable | Description | Default |
|----------|-------------|---------|
| `WORKSPACE_DIR` | Agent workspace directory | `/workspace` |
| `PYTHONPATH` | Python module search path | `/workspace:/app` |

### Browser
| Variable | Description | Default |
|----------|-------------|---------|
| `DISPLAY` | X display for browser | `:99` |
| `PLAYWRIGHT_BROWSERS_PATH` | Playwright browsers cache | `/opt/playwright-browsers` |

### Python Environment
| Variable | Description | Default |
|----------|-------------|---------|
| `UV_INDEX_URL` | Python package index | `http://mirrors.cloud.aliyuncs.com/pypi/simple` |
| `UV_PROJECT_ENVIRONMENT` | Virtual environment path | `/tmp/.venv` |

## Configuration

### AgentConfig

```python
from claude_agent_sdk.config import AgentConfig

config = AgentConfig(
    llm_gateway_url="http://10.138.255.202:8080",
    default_model="claude-sonnet-4-5",
    workspace_dir="/workspace",
    allowed_tools=["bash", "browser", "file"],
    max_tool_calls=100,
)
```

## MCP Server Support

MMAgent supports the Model Context Protocol for extending capabilities:

### Built-in MCP Servers

```python
from claude_agent_sdk.mcp_servers import (
    GitMcpServer,
    FilesystemMcpServer,
    GithubMcpServer,
)
```

### Custom MCP Tools

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(name="my_tool", description="My custom tool", input_schema={"input": str})
async def my_tool(args: dict) -> dict:
    return {"content": [{"type": "text", "text": f"Result: {args['input']}"}]}

server = create_sdk_mcp_server("my_server", tools=[my_tool])
```

## API Reference

### ClaudeSDKClient

Main client for interacting with Claude Code.

```python
class ClaudeSDKClient:
    async def __aenter__(self) -> "ClaudeSDKClient"]
    async def __aexit__(self, ...) -> bool
    async def connect(self, prompt: str | AsyncIterable) -> None
    async def query(self, prompt: str) -> None
    async def receive_messages() -> AsyncIterator[Message]
    async def receive_response() -> AsyncIterator[Message]
    async def interrupt() -> None
    async def set_permission_mode(mode: str) -> None
    async def set_model(model: str) -> None
    async def disconnect() -> None
```

### Tool Decorator

Decorator for creating MCP tools.

```python
@tool(name: str, description: str, input_schema: dict)
async def my_tool(args: dict) -> dict:
    ...
```

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py` - Simple SDK usage
- `browser_automation.py` - Web browsing
- `mcp_server.py` - Custom MCP tools
- `streaming_chat.py` - Streaming conversation

## License

MIT License

## Contributing

Contributions are welcome! Please see the repository for details.
