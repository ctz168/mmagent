# MMAgent - MiniMax AI Agent SDK

> 强大的 Python 与 Node.js AI Agent 开发框架，基于 Claude Code 构建

[English](#english) | [中文](#中文)

---

## English

### Overview

MMAgent is a comprehensive AI Agent SDK that provides a complete development framework for building intelligent agents powered by large language models. Built on Claude Code technology, it offers seamless integration with LLMs, browser automation, and an extensible tool system.

### Key Features

| Feature | Description |
|---------|-------------|
| **Claude SDK Integration** | Full Python SDK for interacting with Claude Code |
| **Multi-LLM Support** | Anthropic Claude API, custom LLM gateways, and more |
| **Browser Automation** | Playwright-based web browsing and scraping |
| **MCP Protocol** | Model Context Protocol for standardized tool system |
| **Tool Framework** | Built-in file operations, shell execution, browser control |
| **Streaming Responses** | Real-time response streaming with async support |
| **Docker Ready** | Complete containerization with Docker and Docker Compose |

### Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         MMAgent Architecture                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      Frontend (React)                        │   │
│  │              Web UI - Chat Interface - Dashboard            │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      Backend (FastAPI)                       │   │
│  │            REST API - WebSocket - Session Management        │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Python SDK Layer                          │   │
│  │         ClaudeSDKClient - Tool System - MCP Servers         │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Agent Runner Engine                       │   │
│  │                   (Claude Code 2.0.33)                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │   │
│  │  │ Claude SDK   │  │Tool Executor │  │MCP Protocol  │     │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       LLM Gateway                            │   │
│  │            10.138.255.202:8080 / Anthropic API              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### System Components

#### 1. Agent Runner Engine (`/engine`)

The core AI engine based on Claude Code 2.0.33:

| Component | Size | Description |
|-----------|------|-------------|
| `agent-runner` | 9.7MB | Main Claude Code engine (minified Node.js) |
| `claude` | 122B | Entry point shell script |
| `_set_title.js` | 118B | Process title maintenance utility |
| `claude-code/` | - | Claude Code Node.js package |
| `@modelcontextprotocol/` | - | MCP protocol servers |

#### 2. Python SDK (`/claude_agent_sdk`)

Full-featured Python SDK for agent development:

```
claude_agent_sdk/
├── client.py              # Main SDK client
├── types.py               # Type definitions
├── query.py               # Query utilities
├── config/                # Configuration system
├── tools/                 # Built-in tools
│   ├── browser_tool.py   # Playwright browser automation
│   ├── file_tool.py      # Safe file operations
│   └── bash_tool.py      # Shell command execution
├── _internal/            # Internal implementation
│   ├── client.py
│   ├── query.py
│   ├── message_parser.py
│   └── transport/
└── examples/             # Usage examples
```

#### 3. Backend API (`/backend`)

FastAPI-based backend service:

```
backend/
├── main.py               # FastAPI application
├── routers/              # API endpoints
├── models/               # Data models
└── services/             # Business logic
```

#### 4. Frontend (`/frontend`)

React-based web interface:

```
frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/           # Page components
│   └── App.tsx          # Main application
└── package.json
```

### Running Principles

#### LLM Interaction Flow

```
User Input
    │
    ▼
┌─────────────────┐
│   Frontend UI   │  User types message
└────────┬────────┘
         │
         ▼ (HTTP/WebSocket)
┌─────────────────┐
│   Backend API   │  Session management, routing
└────────┬────────┘
         │
         ▼ (STDIN to Agent Runner)
┌─────────────────┐
│  Agent Runner   │  Claude Code 2.0.33 engine
│ (Claude SDK)    │  LLM inference, tool planning
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  LLM Gateway    │  │   Tool System   │
│ 10.138.255.202  │  │Browser/File/Bash│
└─────────────────┘  └─────────────────┘
         │                  │
         └────────┬─────────┘
                  │
                  ▼ (STDOUT from Agent Runner)
         ┌─────────────────┐
         │   Backend API   │  Response formatting
         └────────┬────────┘
                  │
                  ▼ (HTTP/WebSocket)
         ┌─────────────────┐
         │   Frontend UI   │  Display response
         └─────────────────┘
```

#### Tool Execution Model

```
┌──────────────┐     Tool Call      ┌──────────────┐
│              │ ──────────────────▶│              │
│ Claude Code  │                    │ Python SDK   │
│   Engine     │                    │   Tools      │
│              │ ◀──────────────────│              │
└──────────────┘     Tool Result    └──────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │         Tool Types          │
              ├──────────────────────────────┤
              │  BrowserTool  │  Headless   │
              │               │  Playwright  │
              ├───────────────┼──────────────┤
              │  FileTool     │  Safe file  │
              │               │  operations  │
              ├───────────────┼──────────────┤
              │  BashTool     │  Shell exec  │
              │               │  in workspace│
              ├───────────────┼──────────────┤
              │  MCP Servers  │  Extensible  │
              │               │  via MCP     │
              └───────────────┴──────────────┘
```

### Installation

#### Prerequisites

- Python 3.12.0+
- Node.js 18.0.0+
- Docker & Docker Compose (for deployment)
- Xvfb (for headless browser)

#### Python SDK Installation

```bash
# Clone repository
git clone https://github.com/ctz168/mmagent.git
cd mmagent

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

#### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Manual Deployment

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run build
# Serve dist/ with nginx or any static server
```

### Quick Start

#### Basic Python Usage

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def main():
    # Simple query
    result = await ClaudeSDKClient.query("Hello, how are you?")
    print(result)

asyncio.run(main())
```

#### With Browser Automation

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, tool
from claude_agent_sdk.tools import BrowserTool

@tool(name="browse", description="Browse webpage", input_schema={"url": str})
async def browse(args: dict) -> dict:
    async with BrowserTool() as browser:
        await browser.navigate(args["url"])
        title = await browser.get_text("title")
        return {"content": [{"type": "text", "text": f"Title: {title}"}]}

async with ClaudeSDKClient(options={"mcp_servers": {"browser": browse}}) as client:
    await client.query("Visit example.com and tell me the title")
```

#### Streaming Conversation

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def main():
    async with ClaudeSDKClient() as client:
        await client.query("Explain Python asyncio")
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_GATEWAY_BASE_URL` | Custom LLM gateway URL | `http://10.138.255.202:8080` |
| `ANTHROPIC_BASE_URL` | Anthropic API base URL | `http://127.0.0.1:8765` |
| `CLAUDE_CODE_ENTRYPOINT` | Claude Code entry point | `sdk-py-client` |
| `WORKSPACE_DIR` | Agent workspace directory | `/workspace` |
| `DISPLAY` | X display for browser | `:99` |

### Project Structure

```
mmagent/
├── engine/                      # Agent Runner Engine (Claude Code)
│   ├── agent-runner            # Main engine (9.7MB)
│   ├── claude                   # Entry point
│   ├── claude-code/            # Node.js package
│   └── @modelcontextprotocol/  # MCP servers
├── claude_agent_sdk/           # Python SDK
│   ├── client.py
│   ├── tools/
│   └── examples/
├── backend/                    # FastAPI Backend
│   ├── main.py
│   └── routers/
├── frontend/                   # React Frontend
│   └── src/
├── docker/                     # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── examples/                   # Example scripts
├── tests/                      # Test suite
└── README.md                   # This file
```

### License

MIT License

---

## 中文

### 概述

MMAgent 是一个全面的 AI Agent 开发框架，提供基于大语言模型的智能代理开发完整解决方案。基于 Claude Code 技术构建，提供无缝的 LLM 集成、浏览器自动化和可扩展的工具系统。

### 核心特性

| 特性 | 描述 |
|------|------|
| **Claude SDK 集成** | 完整的 Python SDK 用于与 Claude Code 交互 |
| **多 LLM 支持** | Anthropic Claude API、自定义 LLM 网关等 |
| **浏览器自动化** | 基于 Playwright 的网页浏览和抓取 |
| **MCP 协议** | Model Context Protocol 标准化工具系统 |
| **工具框架** | 内置文件操作、Shell 执行、浏览器控制 |
| **流式响应** | 异步实时响应流 |
| **Docker 支持** | 完整的容器化部署方案 |

### 系统架构

```
┌────────────────────────────────────────────────────────────────────┐
│                         MMAgent 系统架构                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      前端 (React)                            │   │
│  │              Web UI - 聊天界面 - 管理面板                    │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      后端 (FastAPI)                          │   │
│  │            REST API - WebSocket - 会话管理                   │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Python SDK 层                             │   │
│  │         ClaudeSDKClient - 工具系统 - MCP 服务器              │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Agent Runner 引擎                          │   │
│  │                   (Claude Code 2.0.33)                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │   │
│  │  │ Claude SDK   │  │ 工具执行器   │  │ MCP 协议     │        │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                │                                     │
│                                ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       LLM 网关                                │   │
│  │            10.138.255.202:8080 / Anthropic API              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### 运行原理

#### LLM 交互流程

```
用户输入
    │
    ▼
┌─────────────────┐
│   前端界面      │  用户输入消息
└────────┬────────┘
         │
         ▼ (HTTP/WebSocket)
┌─────────────────┐
│   后端 API      │  会话管理、路由
└────────┬────────┘
         │
         ▼ (STDIN 发送给 Agent Runner)
┌─────────────────┐
│  Agent Runner   │  Claude Code 2.0.33 引擎
│ (Claude SDK)    │  LLM 推理、工具规划
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  LLM 网关       │  │   工具系统      │
│ 10.138.255.202  │  │浏览器/文件/终端 │
└─────────────────┘  └─────────────────┘
         │                  │
         └────────┬─────────┘
                  │
                  ▼ (STDOUT 从 Agent Runner 输出)
         ┌─────────────────┐
         │   后端 API      │  响应格式化
         └────────┬────────┘
                  │
                  ▼ (HTTP/WebSocket)
         ┌─────────────────┐
         │   前端界面      │  显示响应
         └─────────────────┘
```

#### 工具执行模型

```
┌──────────────┐     工具调用      ┌──────────────┐
│              │ ───────────────▶│              │
│ Claude Code  │                  │ Python SDK   │
│   引擎       │                  │   工具集     │
│              │ ◀───────────────│              │
└──────────────┘     工具结果     └──────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │         工具类型              │
              ├──────────────────────────────┤
              │  BrowserTool │  无头浏览器    │
              │              │  Playwright    │
              ├───────────────┼───────────────┤
              │  FileTool    │  安全文件操作  │
              ├───────────────┼───────────────┤
              │  BashTool    │  Shell 执行    │
              │              │  工作区内执行  │
              ├───────────────┼───────────────┤
              │  MCP 服务器  │  可扩展工具    │
              └───────────────┴───────────────┘
```

### 系统组件详解

#### 1. Agent Runner 引擎 (`/engine`)

基于 Claude Code 2.0.33 的核心 AI 引擎：

| 组件 | 大小 | 描述 |
|------|------|------|
| `agent-runner` | 9.7MB | Claude Code 主引擎（压缩的 Node.js） |
| `claude` | 122B | 入口 Shell 脚本 |
| `_set_title.js` | 118B | 进程标题维护工具 |
| `claude-code/` | - | Claude Code Node.js 包 |
| `@modelcontextprotocol/` | - | MCP 协议服务器 |

**入口点脚本 (claude):**

```bash
#!/bin/sh
export NODE_OPTIONS="${NODE_OPTIONS:-} -r /tmp/matrix/bin/_set_title.js"
exec /tmp/matrix/bin/agent-runner "$@"
```

#### 2. Python SDK (`/claude_agent_sdk`)

完整的 Python SDK 用于 Agent 开发：

```
claude_agent_sdk/
├── client.py              # 主 SDK 客户端
├── types.py               # 类型定义
├── query.py               # 查询工具
├── config/                # 配置系统
├── tools/                 # 内置工具
│   ├── browser_tool.py   # Playwright 浏览器自动化
│   ├── file_tool.py      # 安全文件操作
│   └── bash_tool.py      # Shell 命令执行
├── _internal/            # 内部实现
│   ├── client.py
│   ├── query.py
│   ├── message_parser.py
│   └── transport/
└── examples/             # 使用示例
```

#### 3. 后端 API (`/backend`)

基于 FastAPI 的后端服务：

```
backend/
├── main.py               # FastAPI 应用
├── routers/              # API 端点
├── models/               # 数据模型
└── services/             # 业务逻辑
```

#### 4. 前端 (`/frontend`)

基于 React 的 Web 界面：

```
frontend/
├── src/
│   ├── components/       # React 组件
│   ├── pages/           # 页面组件
│   └── App.tsx          # 主应用
└── package.json
```

### 部署指南

#### 环境要求

- Python 3.12.0+
- Node.js 18.0.0+
- Docker & Docker Compose（容器部署）
- Xvfb（无头浏览器）

#### Docker 部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/ctz168/mmagent.git
cd mmagent

# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 手动部署

**后端部署：**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**前端部署：**

```bash
cd frontend
npm install
npm run build
# 使用 nginx 或任何静态服务器托管 dist/ 目录
```

**Python SDK 安装：**

```bash
# 使用 uv 安装（推荐）
uv pip install -e .

# 或使用 pip
pip install -e .
```

### 快速开始

#### 基础 Python 使用

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def main():
    # 简单查询
    result = await ClaudeSDKClient.query("你好，世界！")
    print(result)

asyncio.run(main())
```

#### 浏览器自动化

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, tool
from claude_agent_sdk.tools import BrowserTool

@tool(name="browse", description="浏览网页", input_schema={"url": str})
async def browse(args: dict) -> dict:
    async with BrowserTool() as browser:
        await browser.navigate(args["url"])
        title = await browser.get_text("title")
        return {"content": [{"type": "text", "text": f"标题: {title}"}]}

async with ClaudeSDKClient(options={"mcp_servers": {"browser": browse}}) as client:
    await client.query("访问 example.com 并告诉我标题")
```

#### 流式对话

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient

async def main():
    async with ClaudeSDKClient() as client:
        await client.query("解释 Python 异步编程")
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

### 环境变量配置

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `LLM_GATEWAY_BASE_URL` | 自定义 LLM 网关地址 | `http://10.138.255.202:8080` |
| `ANTHROPIC_BASE_URL` | Anthropic API 地址 | `http://127.0.0.1:8765` |
| `CLAUDE_CODE_ENTRYPOINT` | Claude Code 入口点 | `sdk-py-client` |
| `WORKSPACE_DIR` | Agent 工作目录 | `/workspace` |
| `DISPLAY` | 浏览器 X 显示 | `:99` |
| `PYTHONPATH` | Python 模块搜索路径 | `/workspace:/app` |

### 项目结构

```
mmagent/
├── engine/                      # Agent Runner 引擎 (Claude Code)
│   ├── agent-runner            # 主引擎 (9.7MB)
│   ├── claude                   # 入口脚本
│   ├── claude-code/            # Node.js 包
│   └── @modelcontextprotocol/  # MCP 服务器
├── claude_agent_sdk/           # Python SDK
│   ├── client.py
│   ├── tools/
│   └── examples/
├── backend/                    # FastAPI 后端
│   ├── main.py
│   └── routers/
├── frontend/                   # React 前端
│   └── src/
├── docker/                     # Docker 配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── examples/                   # 示例脚本
├── tests/                      # 测试套件
└── README.md                   # 本文件
```

### 技术栈

| 类别 | 技术 |
|------|------|
| AI 引擎 | Claude Code 2.0.33 |
| Python SDK | aiohttp, httpx, pydantic, playwright |
| 后端框架 | FastAPI, uvicorn |
| 前端框架 | React, TypeScript, Vite |
| 协议 | MCP (Model Context Protocol) |
| 容器化 | Docker, Docker Compose, Nginx |
| LLM 网关 | Anthropic API, 自定义网关 |

### 许可证

MIT License

---

**作者**: MiniMax Agent
**版本**: 1.0.0
**最后更新**: 2026-04-03
