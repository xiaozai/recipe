"""Hacker News data collector."""
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx

from .base import BaseCollector
from ..models.content import ContentItem, ContentType, SearchResult


class HackerNewsCollector(BaseCollector):
    """Collector for Hacker News stories and comments."""

    BASE_URL = "https://hn.algolia.com/api/v1"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self) -> str:
        return "Hacker News"

    @property
    def source_type(self) -> str:
        return "hackernews"

    async def _make_request(
        self, client: httpx.AsyncClient, endpoint: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make a request to HN Algolia API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _parse_item(self, hit: Dict[str, Any]) -> Optional[ContentItem]:
        """Parse a single HN hit into a ContentItem."""
        if not hit.get("title"):
            return None

        created_at = None
        if hit.get("created_at"):
            try:
                created_at = datetime.fromisoformat(
                    hit["created_at"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass

        return ContentItem(
            id=f"hn_{hit.get('objectID', '')}",
            title=hit["title"],
            content=self._truncate_content(
                hit.get("story_text") or hit.get("comment_text") or hit["title"]
            ),
            source_type=ContentType.HACKERNEWS,
            url=hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            author=hit.get("author"),
            created_at=created_at,
            score=hit.get("points", 0),
            tags=[],
            metadata={
                "points": hit.get("points", 0),
                "num_comments": hit.get("num_comments", 0),
                "story_id": hit.get("story_id"),
                "type": hit.get("type"),
            },
        )

    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """Search Hacker News for stories and comments."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Search stories
            stories_params = {
                "query": keyword,
                "tags": "story",
                "hitsPerPage": limit // 2,
            }
            # Search comments
            comments_params = {
                "query": keyword,
                "tags": "comment",
                "hitsPerPage": limit // 2,
            }

            stories_task = self._make_request(client, "/search", stories_params)
            comments_task = self._make_request(client, "/search", comments_params)

            stories_data, comments_data = await asyncio.gather(
                stories_task, comments_task, return_exceptions=True
            )

            items = []

            if isinstance(stories_data, dict):
                for hit in stories_data.get("hits", []):
                    item = self._parse_item(hit)
                    if item:
                        items.append(item)

            if isinstance(comments_data, dict):
                for hit in comments_data.get("hits", []):
                    item = self._parse_item(hit)
                    if item:
                        items.append(item)

            return SearchResult(
                keyword=keyword,
                items=items,
                total_count=len(items),
                source=self.name,
            )

    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """Get trending stories on HN."""
        # Map timeframe to seconds
        seconds_map = {"day": 86400, "week": 604800, "month": 2592000}
        seconds = seconds_map.get(timeframe, 604800)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {
                "tags": "story",
                "hitsPerPage": 30,
                "numericFilters": f"points>50,created_at_i>{int(datetime.now().timestamp()) - seconds}",
            }
            data = await self._make_request(client, "/search", params)

            items = []
            for hit in data.get("hits", []):
                item = self._parse_item(hit)
                if item:
                    items.append(item)

            # Sort by points
            items.sort(key=lambda x: x.score or 0, reverse=True)
            return items