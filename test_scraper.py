import asyncio
import sys
import os

# Ensure we can import from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from scrapers.orchestrator import ScraperOrchestrator

async def main():
    print("Starting Scraper Test...")
    orchestrator = ScraperOrchestrator()
    
    url = "http://example.com"
    print(f"Scraping {url}...")
    
    result = await orchestrator.start_scraping(url, mode="single_page")
    
    if "error" in result:
        print(f"❌ Failed: {result['error']}")
    else:
        print(f"✅ Success!")
        print(f"Title: {result.get('title')}")
        content_len = len(result.get('content', ''))
        print(f"Content Length: {content_len}")
        if result.get('screenshot'):
            print("✅ Screenshot captured")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
