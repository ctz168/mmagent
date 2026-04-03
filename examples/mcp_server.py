#!/usr/bin/env python3
"""Example: Creating Custom MCP Servers."""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, tool, create_sdk_mcp_server


# Define custom tools
@tool(name="calculator", description="Perform arithmetic calculations", input_schema={"a": float, "b": float, "operation": str})
async def calculator(args: dict) -> dict:
    """Simple calculator tool."""
    a, b = args["a"], args["b"]
    op = args["operation"]

    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }

    result = operations.get(op, "Unknown operation")
    return {"content": [{"type": "text", "text": f"Result: {result}"}]}


@tool(name="weather", description="Get weather for a city", input_schema={"city": str, "unit": str})
async def weather(args: dict) -> dict:
    """Mock weather lookup."""
    city = args["city"]
    unit = args.get("unit", "celsius")

    # Mock weather data
    conditions = ["sunny", "cloudy", "rainy", "snowy"]
    temp = 22 if unit == "celsius" else 72

    return {
        "content": [{
            "type": "text",
            "text": f"Weather in {city}: {conditions[0]}, {temp}°{'C' if unit == 'celsius' else 'F'}"
        }]
    }


async def main():
    """MCP Server creation example."""
    print("=== MCP Server Example ===\n")

    # Create MCP server with custom tools
    tools_server = create_sdk_mcp_server(
        name="utilities",
        version="1.0.0",
        tools=[calculator, weather]
    )

    # Use with Claude SDK
    options = {
        "mcp_servers": {"utilities": tools_server},
        "allowed_tools": ["calculator", "weather"]
    }

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Calculate 15 + 27 using the calculator")
        await client.query("What's the weather in Tokyo?")


if __name__ == "__main__":
    asyncio.run(main())
