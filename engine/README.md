# Agent Engine - MiniMax Agent Runner

This directory contains the core Agent Engine that powers the MiniMax AI Agent platform.

## Contents

```
engine/
├── agent-runner              # Main Claude Code engine (9.7MB minified Node.js)
├── claude                    # Entry point script
├── _set_title.js            # Process title utility
├── claude-code/             # Claude Code Node.js package
│   ├── cli.js               # CLI implementation
│   ├── api.js               # API handlers
│   ├── transport/            # Transport layer
│   └── vendor/               # Vendor dependencies
└── @modelcontextprotocol/    # MCP Protocol implementation
```

## Main Components

### 1. agent-runner (9.7MB)
- **Type**: Minified Node.js script
- **Version**: Claude Code 2.0.33
- **Purpose**: Core AI Agent execution engine
- **Features**:
  - Claude SDK integration
  - Tool execution system
  - MCP protocol support
  - Streaming responses

### 2. Entry Point (claude)
```bash
#!/bin/sh
export NODE_OPTIONS="${NODE_OPTIONS:-} -r /tmp/matrix/bin/_set_title.js"
exec /tmp/matrix/bin/agent-runner "$@"
```

### 3. Process Title (_set_title.js)
Maintains the process title for monitoring.

## Architecture

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

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_CODE_ENTRYPOINT` | sdk-py-client | Entry point mode |
| `ANTHROPIC_BASE_URL` | http://127.0.0.1:8765 | Anthropic API proxy |
| `LLM_GATEWAY_BASE_URL` | http://10.138.255.202:8080 | LLM Gateway |
| `DISPLAY` | :99 | X11 display for browser |

## Usage

```bash
# Direct execution
./engine/agent-runner

# Via entry point
./engine/claude

# With arguments
./engine/claude --help
```

## Notes

- This is the **actual runtime engine** from the container environment
- The agent-runner file is **minified and obfuscated** (Claude Code proprietary)
- All components are copied directly from the running container
- Source code is not included (proprietary)

## Related

- Frontend: `/frontend` - Web UI
- Backend: `/backend` - API service
- SDK: `/claude_agent_sdk` - Python SDK
