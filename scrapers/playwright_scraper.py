import asyncio
from playwright.async_api import async_playwright
from .base_scraper import BaseScraper
from .utils import get_random_user_agent
import logging

logger = logging.getLogger(__name__)

class PlaywrightScraper(BaseScraper):
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None

    async def setup(self):
        """Starts the Playwright engine."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        
        # Create a context with a random user agent or modern one
        # user_agent = get_random_user_agent() # Sometimes returns old stuff
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.context = await self.browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Referer": "https://www.google.com/"
            }
        )
        logger.info(f"Playwright initialized with UA: {user_agent}")

    async def scrape(self, url: str):
        if not self.context:
            await self.setup()
            
        page = await self.context.new_page()
        try:
            logger.info(f"Navigating to {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Basic anti-bot: Wait a bit
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            title = await page.title()
            
            # Extract Links
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a')).map(a => a.href)
            """)
            
            # Take screenshot for debugging/audit
            screenshot = await page.screenshot(full_page=True)
            
            return {
                "url": url,
                "title": title,
                "content": content,
                "links": links,
                "screenshot": screenshot
            }
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Error scraping {url}: {e}\n{tb}")
            return {"error": f"{str(e)} | Traceback: {tb}", "url": url}
        finally:
            await page.close()

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
