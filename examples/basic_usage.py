#!/usr/bin/env python3
"""Example: Basic Claude SDK Usage."""

import asyncio
from claude_agent_sdk import ClaudeSDKClient


async def main():
    """Basic usage example with Claude SDK."""
    print("=== Claude SDK Basic Example ===\n")

    # Simple query mode
    print("1. Simple Query Mode:")
    result = await ClaudeSDKClient.query("What is 2 + 2?")
    print(f"   Result: {result}\n")

    # Streaming mode with conversation
    print("2. Streaming Conversation Mode:")
    async with ClaudeSDKClient() as client:
        # Initial query
        await client.query("Explain what a container is in Docker.")

        # Follow-up query
        await client.query("Give me an example of creating one.")

        # Get all responses
        async for message in client.receive_response():
            print(f"   Message: {message}\n")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
