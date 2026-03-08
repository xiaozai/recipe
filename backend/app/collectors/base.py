"""Base collector interface for data sources."""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.content import ContentItem, SearchResult


class BaseCollector(ABC):
    """Abstract base class for all data collectors."""

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this collector."""
        pass

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return the source type identifier."""
        pass

    @abstractmethod
    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """
        Search for content related to the keyword.

        Args:
            keyword: Search keyword/phrase
            limit: Maximum number of results to return

        Returns:
            SearchResult containing found items
        """
        pass

    @abstractmethod
    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """
        Get trending content from this source.

        Args:
            timeframe: Time period (day, week, month)

        Returns:
            List of trending content items
        """
        pass

    async def health_check(self) -> bool:
        """
        Check if the collector is properly configured and accessible.

        Returns:
            True if healthy, False otherwise
        """
        try:
            results = await self.search("test", limit=1)
            return results.total_count >= 0
        except Exception:
            return False

    def _truncate_content(self, content: str, max_length: int = 2000) -> str:
        """Truncate content to max length."""
        if len(content) > max_length:
            return content[:max_length] + "..."
        return content