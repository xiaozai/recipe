"""Reddit data collector."""
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx

from .base import BaseCollector
from ..models.content import ContentItem, ContentType, SearchResult
from ..core.config import get_settings


class RedditCollector(BaseCollector):
    """Collector for Reddit posts and comments."""

    BASE_URL = "https://oauth.reddit.com"
    AUTH_URL = "https://www.reddit.com/api/v1/access_token"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        settings = get_settings()
        self.client_id = client_id or settings.reddit_client_id
        self.client_secret = client_secret or settings.reddit_client_secret
        self._access_token: Optional[str] = None

    @property
    def name(self) -> str:
        return "Reddit"

    @property
    def source_type(self) -> str:
        return "reddit"

    async def _get_access_token(self) -> str:
        """Get OAuth access token for Reddit API."""
        if self._access_token:
            return self._access_token

        if not self.client_id or not self.client_secret:
            raise ValueError("Reddit credentials not configured")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            auth = (self.client_id, self.client_secret)
            data = {"grant_type": "client_credentials"}
            response = await client.post(self.AUTH_URL, auth=auth, data=data)
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
            return self._access_token

    async def _make_request(
        self, client: httpx.AsyncClient, endpoint: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to Reddit API."""
        token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "TechTrendAnalyzer/1.0",
        }
        url = f"{self.BASE_URL}{endpoint}"
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _parse_post(self, post_data: Dict[str, Any]) -> ContentItem:
        """Parse a Reddit post into a ContentItem."""
        post = post_data["data"]
        created_at = None
        if post.get("created_utc"):
            created_at = datetime.fromtimestamp(post["created_utc"])

        return ContentItem(
            id=f"reddit_post_{post['id']}",
            title=post["title"],
            content=self._truncate_content(post.get("selftext") or post["title"]),
            source_type=ContentType.REDDIT_POST,
            url=f"https://reddit.com{post['permalink']}",
            author=post.get("author"),
            created_at=created_at,
            score=post.get("score", 0),
            tags=post.get("link_flair_richtext", []),
            metadata={
                "subreddit": post.get("subreddit"),
                "upvote_ratio": post.get("upvote_ratio"),
                "num_comments": post.get("num_comments", 0),
                "awards": post.get("total_awards_received", 0),
            },
        )

    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """Search Reddit for posts."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {
                "q": keyword,
                "limit": limit,
                "sort": "relevance",
                "type": "link,self",
            }

            try:
                data = await self._make_request(client, "/search", params)
                items = []

                for child in data.get("data", {}).get("children", []):
                    try:
                        item = self._parse_post(child)
                        items.append(item)
                    except (KeyError, TypeError):
                        continue

                return SearchResult(
                    keyword=keyword,
                    items=items,
                    total_count=len(items),
                    source=self.name,
                )
            except Exception as e:
                # Return empty result on error
                return SearchResult(
                    keyword=keyword,
                    items=[],
                    total_count=0,
                    source=self.name,
                )

    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """Get trending posts from tech subreddits."""
        subreddits = ["programming", "technology", "MachineLearning", "artificial"]

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = []
            for subreddit in subreddits:
                params = {"limit": 25, "t": timeframe}
                tasks.append(
                    self._make_request(client, f"/r/{subreddit}/hot", params)
                )

            results = await asyncio.gather(*tasks, return_exceptions=True)

            items = []
            for result in results:
                if isinstance(result, dict):
                    for child in result.get("data", {}).get("children", []):
                        try:
                            item = self._parse_post(child)
                            items.append(item)
                        except (KeyError, TypeError):
                            continue

            # Sort by score
            items.sort(key=lambda x: x.score or 0, reverse=True)
            return items[:30]