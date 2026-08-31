
import sys
import os
import asyncio
import requests
import time

# Function to run the uvicorn server in a subprocess would be ideal, 
# but for simplicity we assume the user might need to run it.
# However, we can also test the logic by importing main directly and running it, 
# but integrating with the scraper requires the async event loop handling.

# Let's perform a direct unit test of the endpoint function logic first 
# to avoid needing a running server for this specific verification step.

# Hack to add parent path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/app'))
sys.path.append(os.path.dirname(__file__))

from backend.app.main import trigger_scrape, ScrapePayload

async def test_api_logic():
    print("Starting API Logic Test...")
    
    payload = ScrapePayload(url="http://example.com", mode="single_page")
    
    print(f"Triggering scrape for {payload.url}...")
    
    # We need to ensure the event loop is capable of running playwright
    # On Windows, this is tricky within another loop if not handled right.
    # ScraperOrchestrator uses async_playwright.
    
    try:
        result = await trigger_scrape(payload)
        
        if result.get("status") == "success":
            print("✅ API Scrape Success")
            print(f"Doc ID: {result.get('doc_id')}")
            print(f"Title: {result.get('title')}")
            print(f"Preview: {result.get('preview')}")
        else:
            print(f"❌ API Scrape Failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Exception during test: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_api_logic())
