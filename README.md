# MMAgent

MiniMax AI Agent Runner - A powerful Node.js-based agent execution framework.

## Overview

MMAgent is the core agent runner that powers the MiniMax AI platform. It provides a robust execution environment for AI agents with integrated support for:

- Python environment management via uv
- Playwright browser automation
- Multi-language support (Node.js, Python, Go, etc.)
- Secure privilege management
- Virtual display support (Xvfb, X11VNC)

## Features

- **Agent Execution**: Run AI agents in isolated environments
- **Environment Management**: Automatic Python dependency installation via `pyproject.toml`
- **Browser Automation**: Integrated Playwright support
- **Virtual Display**: Xvfb + X11VNC for headless browser operations
- **Privilege Management**: Secure privilege escalation daemon
- **Multi-Language Support**: Node.js, Python, Go, and more

## Installation

```bash
# Clone the repository
git clone https://github.com/ctz168/mmagent.git
cd mmagent

# Make the agent runner executable
chmod +x bin/agent-runner

# Run the agent
./bin/agent-runner
```

## Project Structure

```
mmagent/
├── bin/
│   └── agent-runner    # Main executable Node.js script
├── README.md           # This file
└── package.json        # Node.js package configuration
```

## Requirements

- Node.js (for agent-runner)
- Python 3.12.5+ (for workspace environment)
- uv (Python package manager)
- Xvfb (for virtual display)
- Playwright (for browser automation)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `UV_INDEX_URL` | Python package index URL |
| `UV_PROJECT_ENVIRONMENT` | Python virtual environment path |
| `PLAYWRIGHT_BROWSERS_PATH` | Playwright browsers cache path |
| `PYTHONPATH` | Python module search path |

## License

MIT License
