# Agent Engine - MMAgent 核心引擎

> Claude Code 2.0.33 运行时引擎

[English](#english) | [中文](#中文)

---

## English

### Overview

This directory contains the core Agent Runner engine that powers the MMAgent AI Agent platform. Based on Claude Code 2.0.33, it provides the fundamental AI inference and tool execution capabilities.

### Components

```
engine/
├── agent-runner              # Main Claude Code engine (9.7MB minified Node.js)
├── claude                    # Entry point shell script
├── _set_title.js            # Process title maintenance utility
├── claude-code/             # Claude Code Node.js package
│   ├── cli.js               # CLI implementation
│   ├── api.js               # API handlers
│   ├── transport/            # Transport layer
│   └── vendor/               # Vendor dependencies
├── @modelcontextprotocol/    # MCP Protocol implementation
│   ├── github/              # GitHub MCP server
│   ├── gitlab/              # GitLab MCP server
│   ├── slack/               # Slack MCP server
│   └── google-maps/         # Google Maps MCP server
├── core/                    # Core utilities
├── mcp/                     # MCP related modules
├── smith/                   # Smith toolkit
└── tools/                   # Tool definitions
```

### Main Components

#### 1. agent-runner (9.7MB)

| Property | Value |
|----------|-------|
| **Type** | Minified Node.js script |
| **Version** | Claude Code 2.0.33 |
| **Size** | 9.7 MB |
| **Purpose** | Core AI Agent execution engine |

**Features:**
- Claude SDK integration
- Tool execution system
- MCP protocol support
- Streaming responses
- Async tool calls

#### 2. Entry Point (claude)

```bash
#!/bin/sh
export NODE_OPTIONS="${NODE_OPTIONS:-} -r /tmp/matrix/bin/_set_title.js"
exec /tmp/matrix/bin/agent-runner "$@"
```

Sets up Node.js options and delegates to agent-runner.

#### 3. Process Title (_set_title.js)

Maintains the process title for monitoring and identification:

```javascript
process.title='agent-runner';
var _t=setInterval(function(){process.title='agent-runner'},500);
if(_t.unref)_t.unref();
```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Runner Process                      │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Claude     │───▶│    Tool      │───▶│     MCP      │ │
│  │    SDK      │    │   System     │    │   Protocol   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   LLM API    │    │   Python/JS  │    │    Remote    │ │
│  │   Gateway    │    │   Tools      │    │   Servers    │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_CODE_ENTRYPOINT` | sdk-py-client | Entry point mode |
| `ANTHROPIC_BASE_URL` | http://127.0.0.1:8765 | Anthropic API proxy |
| `LLM_GATEWAY_BASE_URL` | http://10.138.255.202:8080 | LLM Gateway |
| `DISPLAY` | :99 | X11 display for browser |
| `WORKSPACE_DIR` | /workspace | Agent workspace |

### Usage

```bash
# Direct execution
./engine/agent-runner

# Via entry point
./engine/claude

# With arguments
./engine/claude --help
```

### Claude Code Package Structure

```
claude-code/
├── cli.js                  # Main CLI implementation
├── api.js                  # API handlers
├── package.json            # Package configuration
├── transport/              # Transport layer
│   └── ...
└── vendor/                 # Vendor dependencies
    ├── claude-code-jetbrains-plugin/  # IDE plugins
    │   ├── plugin/
    │   └── resources/
    └── ripgrep/            # ripgrep binaries
        ├── ripgrep-*-x86_64-unknown-linux-gnu/
        ├── ripgrep-*-x86_64-apple-darwin/
        └── ripgrep-*-x86_64-pc-windows-gnu/
```

### MCP Servers

Pre-configured MCP protocol servers:

| Server | Description |
|--------|-------------|
| github | GitHub repository and issue management |
| gitlab | GitLab project and merge request handling |
| slack | Slack messaging integration |
| google-maps | Google Maps API integration |

### Notes

- This is the **actual runtime engine** from the container environment
- The agent-runner file is **minified and obfuscated** (Claude Code proprietary)
- All components are copied directly from the running container
- Source code is not included (proprietary)

### Related

- Main README: `/README.md`
- Frontend: `/frontend` - Web UI
- Backend: `/backend` - API service
- SDK: `/claude_agent_sdk` - Python SDK

---

## 中文

### 概述

本目录包含驱动 MMAgent AI Agent 平台的核心 Agent Runner 引擎。基于 Claude Code 2.0.33 构建，提供基础的 AI 推理和工具执行能力。

### 组件结构

```
engine/
├── agent-runner              # Claude Code 主引擎 (9.7MB 压缩的 Node.js)
├── claude                    # 入口 Shell 脚本
├── _set_title.js            # 进程标题维护工具
├── claude-code/             # Claude Code Node.js 包
│   ├── cli.js               # CLI 实现
│   ├── api.js               # API 处理器
│   ├── transport/            # 传输层
│   └── vendor/               # 供应商依赖
├── @modelcontextprotocol/    # MCP 协议实现
│   ├── github/              # GitHub MCP 服务器
│   ├── gitlab/              # GitLab MCP 服务器
│   ├── slack/               # Slack MCP 服务器
│   └── google-maps/         # Google Maps MCP 服务器
├── core/                    # 核心工具
├── mcp/                     # MCP 相关模块
├── smith/                   # Smith 工具包
└── tools/                   # 工具定义
```

### 主要组件

#### 1. agent-runner (9.7MB)

| 属性 | 值 |
|------|------|
| **类型** | 压缩的 Node.js 脚本 |
| **版本** | Claude Code 2.0.33 |
| **大小** | 9.7 MB |
| **用途** | 核心 AI Agent 执行引擎 |

**功能特性：**
- Claude SDK 集成
- 工具执行系统
- MCP 协议支持
- 流式响应
- 异步工具调用

#### 2. 入口点 (claude)

```bash
#!/bin/sh
export NODE_OPTIONS="${NODE_OPTIONS:-} -r /tmp/matrix/bin/_set_title.js"
exec /tmp/matrix/bin/agent-runner "$@"
```

设置 Node.js 选项并委托给 agent-runner。

#### 3. 进程标题 (_set_title.js)

维护进程标题以便监控和识别：

```javascript
process.title='agent-runner';
var _t=setInterval(function(){process.title='agent-runner'},500);
if(_t.unref)_t.unref();
```

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Runner 进程                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Claude     │───▶│    工具      │───▶│     MCP      │ │
│  │    SDK       │    │   执行器     │    │   协议       │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   LLM API     │    │   Python/JS  │    │    远程      │ │
│  │   网关        │    │   工具       │    │   服务器     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 运行原理

#### 1. 初始化阶段

```
Agent Runner 启动
    │
    ├── 加载 Claude SDK
    ├── 初始化 MCP 协议栈
    ├── 注册内置工具 (BrowserTool, FileTool, BashTool)
    └── 连接 LLM 网关
```

#### 2. 请求处理流程

```
收到用户输入 (STDIN)
    │
    ├── 解析用户消息
    ├── 构建提示词上下文
    └── 调用 LLM 推理
            │
            ├── LLM 返回文本/工具调用
            │
            └── 如果是工具调用
                    │
                    ├── 解析工具名称和参数
                    ├── 调用对应工具
                    └── 返回结果给 LLM
```

#### 3. 流式响应

```
LLM 推理 (流式输出)
    │
    ├── 实时发送 token 到 STDOUT
    ├── 后端捕获并转发给前端
    └── 前端实时显示响应
```

### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `CLAUDE_CODE_ENTRYPOINT` | sdk-py-client | 入口点模式 |
| `ANTHROPIC_BASE_URL` | http://127.0.0.1:8765 | Anthropic API 代理 |
| `LLM_GATEWAY_BASE_URL` | http://10.138.255.202:8080 | LLM 网关 |
| `DISPLAY` | :99 | 浏览器 X11 显示 |
| `WORKSPACE_DIR` | /workspace | Agent 工作目录 |

### 使用方法

```bash
# 直接执行
./engine/agent-runner

# 通过入口脚本
./engine/claude

# 带参数执行
./engine/claude --help
```

### Claude Code 包结构

```
claude-code/
├── cli.js                  # 主 CLI 实现
├── api.js                  # API 处理器
├── package.json            # 包配置
├── transport/              # 传输层
│   └── ...
└── vendor/                 # 供应商依赖
    ├── claude-code-jetbrains-plugin/  # IDE 插件
    │   ├── plugin/
    │   └── resources/
    └── ripgrep/            # ripgrep 二进制文件
        ├── ripgrep-*-x86_64-unknown-linux-gnu/
        ├── ripgrep-*-x86_64-apple-darwin/
        └── ripgrep-*-x86_64-pc-windows-gnu/
```

### MCP 服务器

预配置的 MCP 协议服务器：

| 服务器 | 描述 |
|--------|------|
| github | GitHub 仓库和 Issue 管理 |
| gitlab | GitLab 项目和合并请求处理 |
| slack | Slack 消息集成 |
| google-maps | Google Maps API 集成 |

### 工具系统

#### 内置工具

| 工具 | 描述 | 实现 |
|------|------|------|
| BrowserTool | 无头浏览器自动化 | Python/Playwright |
| FileTool | 安全文件操作 | Python |
| BashTool | Shell 命令执行 | Python |

#### MCP 扩展

通过 MCP (Model Context Protocol) 可以扩展更多工具：

```python
# 自定义 MCP 工具示例
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(name="custom_tool", description="自定义工具", input_schema={"input": str})
async def custom_tool(args: dict) -> dict:
    return {"content": [{"type": "text", "text": f"结果: {args['input']}"}]}

server = create_sdk_mcp_server("my_server", tools=[custom_tool])
```

### 技术细节

#### STDIN/STDOUT 通信

Agent Runner 通过标准输入输出与后端通信：

```
后端 ──STDIN──▶ Agent Runner  (发送用户消息)
后端 ◀─STDOUT── Agent Runner  (接收响应)
```

#### 进程管理

- 主进程：`agent-runner`
- 进程标题：`agent-runner`
- 定期更新标题以保持活跃

### 注意事项

- 这是容器环境中的**实际运行时引擎**
- agent-runner 文件是**压缩和混淆的**（Claude Code 专有）
- 所有组件直接从运行中的容器复制
- 不包含源代码（专有）

### 相关文档

- 主 README: `/README.md`
- 前端: `/frontend` - Web UI
- 后端: `/backend` - API 服务
- SDK: `/claude_agent_sdk` - Python SDK

---

**版本**: 2.0.33
**最后更新**: 2026-04-03
