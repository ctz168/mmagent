#!/usr/bin/env python3
"""Example: Streaming Chat Interface."""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, PermissionMode


async def main():
    """Streaming chat example with more control."""
    print("=== Streaming Chat Example ===\n")

    # Configure options
    options = ClaudeAgentOptions(
        permission_mode=PermissionMode.BYPASS,  # Auto-approve dangerous operations
        max_tokens=4096,
        temperature=0.7,
    )

    async with ClaudeSDKClient(options=options) as client:
        # Start conversation
        print("User: Hello, what can you help me with?")
        await client.query("Hello! I'm working on a Python project.")

        # Get streaming responses
        async for message in client.receive_response():
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(f"Claude: {block.text}")

        # Change model mid-conversation
        print("\nSwitching to Sonnet model...")
        await client.set_model("claude-sonnet-4-5")
        await client.query("Now please explain Python decorators.")


if __name__ == "__main__":
    asyncio.run(main())
