"""Web/blog data collector using RSS feeds and web scraping."""
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx
from bs4 import BeautifulSoup
import feedparser

from .base import BaseCollector
from ..models.content import ContentItem, ContentType, SearchResult


class BlogCollector(BaseCollector):
    """Collector for tech blogs and RSS feeds."""

    # Predefined tech blog RSS feeds
    TECH_FEEDS = [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://www.infoq.com/feed",
        "https://hnrss.org/frontpage",
        "https://feeds.feedburner.com/PythonInsider",
        "https://blog.rust-lang.org/feed.xml",
        "https://go.dev/blog/feed.atom",
        "https://dev.to/feed",
        "https://medium.com/feed/topic/technology",
    ]

    def __init__(self, custom_feeds: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        self.feeds = custom_feeds or self.TECH_FEEDS

    @property
    def name(self) -> str:
        return "Tech Blogs"

    @property
    def source_type(self) -> str:
        return "blog"

    async def _fetch_feed(
        self, client: httpx.AsyncClient, feed_url: str
    ) -> List[ContentItem]:
        """Fetch and parse a single RSS feed."""
        items = []
        try:
            response = await client.get(feed_url, timeout=self.timeout)
            response.raise_for_status()

            feed = feedparser.parse(response.text)

            for entry in feed.entries[:20]:  # Limit per feed
                # Parse published date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                # Get content
                content = ""
                if hasattr(entry, "content"):
                    content = entry.content[0].value if entry.content else ""
                elif hasattr(entry, "summary"):
                    content = entry.summary

                # Clean HTML
                if content:
                    soup = BeautifulSoup(content, "html.parser")
                    content = soup.get_text(separator=" ", strip=True)

                item = ContentItem(
                    id=f"blog_{hash(entry.get('link', ''))}",
                    title=entry.get("title", "Untitled"),
                    content=self._truncate_content(content or entry.get("title", "")),
                    source_type=ContentType.BLOG,
                    url=entry.get("link", ""),
                    author=entry.get("author", None),
                    created_at=published,
                    tags=[tag.term for tag in entry.get("tags", [])],
                    metadata={
                        "feed_source": feed_url,
                        "summary": entry.get("summary", ""),
                    },
                )
                items.append(item)

        except Exception:
            pass  # Skip failed feeds silently

        return items

    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """Search blogs by fetching feeds and filtering by keyword."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = [self._fetch_feed(client, feed) for feed in self.feeds[:5]]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_items = []
            for result in results:
                if isinstance(result, list):
                    all_items.extend(result)

            # Filter by keyword
            keyword_lower = keyword.lower()
            filtered = [
                item
                for item in all_items
                if keyword_lower in item.title.lower()
                or keyword_lower in item.content.lower()
            ]

            # Sort by date (newest first)
            filtered.sort(key=lambda x: x.created_at or datetime.min, reverse=True)

            return SearchResult(
                keyword=keyword,
                items=filtered[:limit],
                total_count=len(filtered),
                source=self.name,
            )

    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """Get trending blog posts."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            tasks = [self._fetch_feed(client, feed) for feed in self.feeds]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_items = []
            for result in results:
                if isinstance(result, list):
                    all_items.extend(result)

            # Filter by timeframe
            from datetime import timedelta

            days_map = {"day": 1, "week": 7, "month": 30}
            cutoff = datetime.now() - timedelta(days=days_map.get(timeframe, 7))

            recent = [
                item
                for item in all_items
                if item.created_at and item.created_at > cutoff
            ]

            recent.sort(key=lambda x: x.created_at or datetime.min, reverse=True)
            return recent[:30]


class WebSearchCollector(BaseCollector):
    """Web search collector using DuckDuckGo."""

    SEARCH_URL = "https://html.duckduckgo.com/html/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self) -> str:
        return "Web Search"

    @property
    def source_type(self) -> str:
        return "blog"

    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """Search the web for keyword."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {"q": keyword, "kl": "wt-wt"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            try:
                response = await client.post(
                    self.SEARCH_URL, data=params, headers=headers
                )
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                items = []

                results = soup.select(".result")[:limit]

                for result in results:
                    title_elem = result.select_one(".result__title")
                    snippet_elem = result.select_one(".result__snippet")
                    link_elem = result.select_one(".result__url")

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get("href", "")

                        # Clean up DuckDuckGo redirect URLs
                        if "uddg=" in link:
                            import urllib.parse

                            parsed = urllib.parse.parse_qs(
                                urllib.parse.urlparse(link).query
                            )
                            if "uddg" in parsed:
                                link = parsed["uddg"][0]

                        content = snippet_elem.get_text(strip=True) if snippet_elem else ""

                        item = ContentItem(
                            id=f"web_{hash(link)}",
                            title=title,
                            content=self._truncate_content(content or title),
                            source_type=ContentType.BLOG,
                            url=link,
                            metadata={"source": "DuckDuckGo"},
                        )
                        items.append(item)

                return SearchResult(
                    keyword=keyword,
                    items=items,
                    total_count=len(items),
                    source=self.name,
                )

            except Exception as e:
                return SearchResult(
                    keyword=keyword,
                    items=[],
                    total_count=0,
                    source=self.name,
                )

    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """Web search doesn't support trending."""
        return []