from .playwright_scraper import PlaywrightScraper
import logging

logger = logging.getLogger(__name__)

class ScraperOrchestrator:
    def __init__(self):
        self.scraper = PlaywrightScraper(headless=True)
        self.is_running = False

    async def start_scraping(self, url: str, mode: str = "single_page"):
        """
        Main entry point for scraping tasks. 
        Mode can be: 'single_page', 'website' (crawl), 'search'.
        """
        self.is_running = True
        try:
            await self.scraper.setup()
            
            if mode == "single_page":
                result = await self.scraper.scrape(url)
                return [result] # Return list for consistency
                
            elif mode == "website":
                return await self._crawl_website(url)
                
            elif mode == "search":
                return await self._search_and_scrape(url) # url here is the query
                
            else:
                return {"error": f"Mode '{mode}' not yet implemented"}
                
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Orchestrator error: {e}\n{tb}")
            return {"error": f"{str(e)} | Traceback: {tb}"}
        finally:
            await self.scraper.close()
            self.is_running = False

    async def _crawl_website(self, start_url: str, max_pages: int = 5):
        """
        BFS Crawler to visit pages within the same domain.
        """
        from urllib.parse import urlparse
        
        domain = urlparse(start_url).netloc
        visited = set()
        queue = [start_url]
        results = []
        
        logger.info(f"Starting crawl for {start_url} (Max: {max_pages})")
        
        while queue and len(visited) < max_pages:
            current_url = queue.pop(0)
            
            if current_url in visited:
                continue
                
            # Skip if leaving domain (basic check)
            if urlparse(current_url).netloc != domain:
                continue
                
            visited.add(current_url)
            
            data = await self.scraper.scrape(current_url)
            if "error" in data:
                continue
                
            results.append(data)
            
            # Add new links to queue
            for link in data.get("links", []):
                # Basic clean up
                if link and link.startswith("http") and link not in visited:
                    queue.append(link)
                    
        return results

    async def _search_and_scrape(self, query: str, limit: int = 3):
        """
        Performs a search (via DuckDuckGo) and scrapes the top results.
        """
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://search.brave.com/search?q={encoded_query}&source=web"
        
        logger.info(f"Searching for: {query} via Brave")
        
        # 1. Scrape Search Page
        search_data = await self.scraper.scrape(search_url)
        if "error" in search_data:
            return search_data
            
        # 2. Extract Result Links (Brave)
        candidate_links = []
        
        for link in search_data.get("links", []):
            # Brave results are usually direct
            if "brave.com" in link:
                continue
            # Basic filters
            if not link.startswith("http"):
                continue
                
            candidate_links.append(link)
        
        # Deduplicate and limit
        unique_links = list(dict.fromkeys(candidate_links))[:limit]
        
        results = []
        logger.info(f"Found {len(unique_links)} links to scrape: {unique_links}")
        
        # 3. Scrape Each Result
        for link in unique_links:
            data = await self.scraper.scrape(link)
            if "error" not in data:
                results.append(data)
                
        return results
