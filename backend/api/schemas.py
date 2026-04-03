"""Pydantic schemas for API."""

from typing import Optional, Any, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., description="User message")
    history: list[Message] = Field(default_factory=list, description="Conversation history")
    model: Optional[str] = Field(None, description="Model to use")
    temperature: Optional[float] = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(4096, gt=0)


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    tools: list[dict[str, Any]] = Field(default_factory=list)
    model: str
    usage: Optional[dict[str, int]] = None


class ToolCall(BaseModel):
    """Tool call information."""
    name: str
    input: dict[str, Any]
    output: Optional[str] = None
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    error: Optional[str] = None


class StreamChunk(BaseModel):
    """Streaming chunk."""
    type: Literal["text", "tool", "error", "done"]
    content: str
    tool_name: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    uptime: float
    models: list[str]


class ConfigResponse(BaseModel):
    """Configuration response."""
    model: str
    max_tokens: int
    temperature: float
    available_tools: list[str]
