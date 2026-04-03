"""FastAPI application for MiniMax Agent."""

import os
import sys
from contextlib import asynccontextmanager

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from agent.client import close_agent_client
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print(f"🚀 Starting MiniMax Agent API...")
    print(f"   Host: {settings.api_host}:{settings.api_port}")
    print(f"   LLM Gateway: {settings.llm_gateway_url}")
    print(f"   Workspace: {settings.workspace_dir}")

    yield

    # Shutdown
    print("👋 Shutting down MiniMax Agent API...")
    await close_agent_client()


# Create FastAPI app
app = FastAPI(
    title="MiniMax Agent API",
    description="AI Agent Platform API powered by Claude Code",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MiniMax Agent",
        "version": "1.0.0",
        "description": "AI Agent Platform powered by Claude Code",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "stream": "/api/chat/stream",
            "websocket": "/ws/chat",
            "tools": "/api/tools/list",
            "docs": "/docs"
        }
    }


@app.get("/favicon.ico")
async def favicon():
    """Favicon."""
    return FileResponse("static/favicon.ico")


# Serve static files in production
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    )
