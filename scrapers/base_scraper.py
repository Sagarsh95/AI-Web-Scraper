from abc import ABC, abstractmethod
from typing import Optional, Dict

class BaseScraper(ABC):
    """
    Abstract base class for all scrapers (Playwright, Selenium, etc.).
    Enforces a consistent interface for the Orchestrator.
    """

    @abstractmethod
    async def setup(self):
        """Initialize the browser/driver."""
        pass

    @abstractmethod
    async def scrape(self, url: str) -> Dict[str, any]:
        """
        Scrape a single URL.
        Returns a dictionary containing raw HTML, screenshots, metadata, etc.
        """
        pass

    @abstractmethod
    async def close(self):
        """Clean up resources."""
        pass
