"""Browser Automation Tool using Playwright."""

import asyncio
import os
from dataclasses import dataclass, field
from typing import Any, Optional

try:
    from playwright.async_api import async_playwright, Browser, Page, Playwright
except ImportError:
    raise ImportError("playwright is required. Install with: pip install playwright")


@dataclass
class PlaywrightConfig:
    """Configuration for Playwright browser automation."""

    browser_type: str = "chromium"
    headless: bool = True
    viewport_width: int = 1280
    viewport_height: int = 720
    user_agent: Optional[str] = None
    slow_mo: int = 0
    timeout: int = 30000
    ignore_https_errors: bool = True
    downloads_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "PlaywrightConfig":
        """Create config from environment variables."""
        return cls(
            headless=os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true",
            browser_type=os.getenv("PLAYWRIGHT_BROWSER", "chromium"),
        )


class BrowserTool:
    """
    Browser automation tool using Playwright.

    Provides methods for:
    - Page navigation
    - Element interaction
    - Screenshot capture
    - Content extraction
    - Form filling
    - File downloads
    """

    def __init__(self, config: Optional[PlaywrightConfig] = None):
        """Initialize browser tool with configuration."""
        self.config = config or PlaywrightConfig.from_env()
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None

    async def __aenter__(self) -> "BrowserTool":
        """Async context manager entry."""
        await self.launch()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Async context manager exit."""
        await self.close()
        return False

    async def launch(self) -> None:
        """Launch browser instance."""
        self._playwright = await async_playwright().start()

        browser_kwargs = {
            "headless": self.config.headless,
            "slow_mo": self.config.slow_mo,
        }

        if self.config.browser_type == "chromium":
            self._browser = await self._playwright.chromium.launch(**browser_kwargs)
        elif self.config.browser_type == "firefox":
            self._browser = await self._playwright.firefox.launch(**browser_kwargs)
        elif self.config.config.browser_type == "webkit":
            self._browser = await self._playwright.webkit.launch(**browser_kwargs)
        else:
            raise ValueError(f"Unknown browser type: {self.config.browser_type}")

        context_kwargs: dict[str, Any] = {
            "viewport": {"width": self.config.viewport_width, "height": self.config.viewport_height},
            "ignore_https_errors": self.config.ignore_https_errors,
        }

        if self.config.user_agent:
            context_kwargs["user_agent"] = self.config.user_agent

        if self.config.downloads_path:
            context_kwargs["accept_downloads"] = True
            os.makedirs(self.config.downloads_path, exist_ok=True)

        context = await self._browser.new_context(**context_kwargs)
        self._page = await context.new_page()

    async def close(self) -> None:
        """Close browser and cleanup resources."""
        if self._page:
            await self._page.close()
            self._page = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    async def navigate(self, url: str, wait_until: str = "networkidle") -> dict[str, Any]:
        """
        Navigate to a URL.

        Args:
            url: Target URL
            wait_until: Wait condition ('load', 'domcontentloaded', 'networkidle', 'commit')

        Returns:
            Navigation result with URL and status
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        response = await self._page.goto(url, wait_until=wait_until, timeout=self.config.timeout)
        return {
            "url": self._page.url,
            "status": response.status if response else None,
            "ok": response.ok if response else False,
        }

    async def screenshot(self, path: str, full_page: bool = False) -> dict[str, Any]:
        """
        Take screenshot of current page.

        Args:
            path: Output file path
            full_page: Capture full scrollable page

        Returns:
            Screenshot result with file path and size
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        await self._page.screenshot(path=path, full_page=full_page)
        file_size = os.path.getsize(path)

        return {
            "path": path,
            "size": file_size,
            "url": self._page.url,
        }

    async def get_text(self, selector: str) -> Optional[str]:
        """Get text content from element."""
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        try:
            element = await self._page.query_selector(selector)
            return await element.inner_text() if element else None
        except Exception:
            return None

    async def get_html(self, selector: Optional[str] = None) -> str:
        """
        Get HTML content.

        Args:
            selector: Optional element selector. If None, gets full page HTML.

        Returns:
            HTML content string
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        if selector:
            element = await self._page.query_selector(selector)
            return await element.inner_html() if element else ""
        return await self._page.content()

    async def click(self, selector: str, timeout: Optional[int] = None) -> dict[str, Any]:
        """
        Click element by selector.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds

        Returns:
            Click result with success status
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        try:
            await self._page.click(selector, timeout=timeout or self.config.timeout)
            return {"success": True, "selector": selector}
        except Exception as e:
            return {"success": False, "selector": selector, "error": str(e)}

    async def fill(self, selector: str, value: str) -> dict[str, Any]:
        """
        Fill input element.

        Args:
            selector: Input element selector
            value: Value to fill

        Returns:
            Fill result with success status
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        try:
            await self._page.fill(selector, value)
            return {"success": True, "selector": selector}
        except Exception as e:
            return {"success": False, "selector": selector, "error": str(e)}

    async def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> bool:
        """
        Wait for element to appear.

        Args:
            selector: Element selector
            state: Wait state ('attached', 'detached', 'visible', 'hidden')
            timeout: Optional timeout in milliseconds

        Returns:
            True if element found, False otherwise
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        try:
            await self._page.wait_for_selector(selector, state=state, timeout=timeout or self.config.timeout)
            return True
        except Exception:
            return False

    async def evaluate(self, expression: str) -> Any:
        """
        Execute JavaScript expression.

        Args:
            expression: JavaScript expression to evaluate

        Returns:
            Result of expression evaluation
        """
        if not self._page:
            raise RuntimeError("Browser not launched. Call launch() first.")

        return await self._page.evaluate(expression)


# Example usage with Claude SDK
async def example_browser_usage():
    """Example of using browser tool with Claude SDK."""
    from claude_agent_sdk import ClaudeSDKClient, tool, create_sdk_mcp_server

    # Create browser tool
    @tool(name="browse", description="Browse a webpage and extract information", input_schema={"url": str, "action": str})
    async def browse(args: dict) -> dict:
        async with BrowserTool() as browser:
            await browser.navigate(args["url"])

            if args.get("action") == "screenshot":
                await browser.screenshot("screenshot.png")
                return {"content": [{"type": "text", "text": "Screenshot saved"}]}
            elif args.get("action") == "content":
                html = await browser.get_html()
                return {"content": [{"type": "text", "text": html}]}
            else:
                title = await browser.get_text("title")
                return {"content": [{"type": "text", "text": f"Title: {title}"}]}

    # Create MCP server with browser tool
    server = create_sdk_mcp_server("browser", tools=[browse])

    # Use with Claude SDK
    async with ClaudeSDKClient(options={"mcp_servers": {"browser": server}}) as client:
        await client.query("Browse example.com and tell me the title")
