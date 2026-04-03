"""API routes for Agent."""

import time
from typing import AsyncIterator
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from sse_starlette.sse import EventSourceResponse

from .schemas import (
    ChatRequest, ChatResponse, HealthResponse, ConfigResponse,
    StreamChunk
)
from agent.client import get_agent_client, close_agent_client
from config import settings

# Create router
router = APIRouter()

# Startup time for uptime calculation
_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime=time.time() - _start_time,
        models=[settings.default_model]
    )


@router.get("/config", response_model=ConfigResponse)
async def get_config():
    """Get current configuration."""
    return ConfigResponse(
        model=settings.default_model,
        max_tokens=4096,
        temperature=0.7,
        available_tools=["bash", "browser", "file", "search", "code", "git"]
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for agent interaction.

    Send a message and receive an agent response.
    """
    try:
        client = await get_agent_client()

        # Convert history to dict format
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.history
        ]

        # Get response
        result = await client.chat(
            message=request.message,
            history=history
        )

        return ChatResponse(
            response=result["response"],
            tools=result.get("tools", []),
            model=result.get("model", settings.default_model),
            usage=result.get("usage")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/stream")
async def stream_chat(message: str, history: str = "{}"):
    """
    Streaming chat endpoint.

    Use Server-Sent Events to stream agent responses.
    """
    import json

    async def generate() -> AsyncIterator[dict]:
        try:
            client = await get_agent_client()

            # Parse history
            history_list = json.loads(history) if history else []

            # Stream response
            async for chunk in client.stream_chat(
                message=message,
                history=history_list
            ):
                if chunk["type"] == "text":
                    yield {
                        "event": "message",
                        "data": chunk["content"]
                    }
                elif chunk["type"] == "done":
                    yield {
                        "event": "done",
                        "data": ""
                    }

        except Exception as e:
            yield {
                "event": "error",
                "data": str(e)
            }

    return EventSourceResponse(generate())


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket chat endpoint for real-time interaction.
    """
    await websocket.accept()

    try:
        client = await get_agent_client()

        while True:
            # Receive message
            data = await websocket.receive_json()

            message = data.get("message", "")
            history = data.get("history", [])

            # Stream response
            async for chunk in client.stream_chat(
                message=message,
                history=history
            ):
                if chunk["type"] == "text":
                    await websocket.send_json({
                        "type": "text",
                        "content": chunk["content"]
                    })
                elif chunk["type"] == "done":
                    await websocket.send_json({
                        "type": "done",
                        "content": ""
                    })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "content": str(e)
        })
    finally:
        await websocket.close()


@router.post("/tools/execute")
async def execute_tool(tool_name: str, tool_input: dict):
    """
    Execute a specific tool.

    This endpoint allows direct tool execution.
    """
    # Placeholder for tool execution
    # In production, this would integrate with actual tool implementations

    tools = {
        "bash": {
            "description": "Execute shell command",
            "input_schema": {"command": str}
        },
        "browser": {
            "description": "Browser automation",
            "input_schema": {"url": str, "action": str}
        },
        "file": {
            "description": "File operations",
            "input_schema": {"path": str, "operation": str}
        }
    }

    if tool_name not in tools:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    return {
        "tool": tool_name,
        "input": tool_input,
        "output": f"Tool '{tool_name}' execution placeholder",
        "status": "completed"
    }


@router.get("/tools/list")
async def list_tools():
    """List available tools."""
    return {
        "tools": [
            {
                "name": "bash",
                "description": "Execute shell commands",
                "input_schema": {"command": str}
            },
            {
                "name": "browser",
                "description": "Browser automation with Playwright",
                "input_schema": {"url": str, "action": str, "selector": str}
            },
            {
                "name": "file_read",
                "description": "Read file contents",
                "input_schema": {"path": str, "binary": bool}
            },
            {
                "name": "file_write",
                "description": "Write file contents",
                "input_schema": {"path": str, "content": str}
            },
            {
                "name": "file_list",
                "description": "List directory contents",
                "input_schema": {"path": str, "recursive": bool}
            },
            {
                "name": "search",
                "description": "Web search",
                "input_schema": {"query": str, "num_results": int}
            }
        ]
    }
