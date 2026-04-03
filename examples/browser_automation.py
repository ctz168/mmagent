#!/usr/bin/env python3
"""Example: Browser Automation with Claude SDK."""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, tool, create_sdk_mcp_server
from claude_agent_sdk.tools import BrowserTool, PlaywrightConfig


# Create browser MCP tool
@tool(
    name="browse_url",
    description="Navigate to a URL and get page content or take screenshot",
    input_schema={
        "url": str,
        "action": str  # "content", "title", "screenshot"
    }
)
async def browse(args: dict) -> dict:
    """Browse a webpage and extract information."""
    config = PlaywrightConfig(headless=True)
    async with BrowserTool(config) as browser:
        await browser.navigate(args["url"])

        if args["action"] == "content":
            html = await browser.get_html()
            return {"content": [{"type": "text", "text": html}]}

        elif args["action"] == "title":
            title = await browser.get_text("title")
            return {"content": [{"type": "text", "text": f"Title: {title}"}]}

        elif args["action"] == "screenshot":
            await browser.screenshot("/tmp/screenshot.png")
            return {"content": [{"type": "text", "text": "Screenshot saved to /tmp/screenshot.png"}]}

        return {"content": [{"type": "text", "text": "Unknown action"}]}


async def main():
    """Browser automation example."""
    print("=== Browser Automation Example ===\n")

    # Create MCP server with browser tool
    browser_server = create_sdk_mcp_server("browser", tools=[browse])

    # Use with Claude SDK
    options = {
        "mcp_servers": {"browser": browser_server},
        "allowed_tools": ["browse_url"]
    }

    async with ClaudeSDKClient(options=options) as client:
        # Ask Claude to browse a website
        await client.query("Please visit example.com and tell me the page title")
        await client.query("Take a screenshot of github.com")


if __name__ == "__main__":
    asyncio.run(main())
