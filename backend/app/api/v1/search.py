"""Search API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks

from ...models.content import SearchResult, ContentItem
from ...collectors import (
    GitHubCollector,
    HackerNewsCollector,
    RedditCollector,
    WebSearchCollector,
)

router = APIRouter(prefix="/search", tags=["search"])

# Collector instances
collectors = {
    "github": GitHubCollector(),
    "hackernews": HackerNewsCollector(),
    "reddit": RedditCollector(),
    "web": WebSearchCollector(),
}


@router.get("/{keyword}", response_model=dict)
async def search_keyword(
    keyword: str,
    sources: Optional[str] = Query(None, description="Comma-separated list of sources"),
    limit: int = Query(50, ge=1, le=100, description="Max results per source"),
):
    """
    Search for content across multiple sources.

    - **keyword**: Search term
    - **sources**: Optional comma-separated list (github, hackernews, reddit, web)
    - **limit**: Maximum results per source (1-100)
    """
    import asyncio

    # Determine which sources to use
    if sources:
        source_list = [s.strip().lower() for s in sources.split(",")]
        active_collectors = {
            name: collector
            for name, collector in collectors.items()
            if name in source_list
        }
    else:
        active_collectors = collectors

    if not active_collectors:
        raise HTTPException(status_code=400, detail="No valid sources specified")

    # Run searches in parallel
    tasks = [
        collector.search(keyword, limit) for collector in active_collectors.values()
    ]

    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    # Combine results
    all_items: List[ContentItem] = []
    source_counts = {}
    errors = []

    for name, result in zip(active_collectors.keys(), results):
        if isinstance(result, Exception):
            errors.append({name: str(result)})
            source_counts[name] = 0
        elif isinstance(result, SearchResult):
            all_items.extend(result.items)
            source_counts[name] = result.total_count

    return {
        "keyword": keyword,
        "total_count": len(all_items),
        "source_counts": source_counts,
        "errors": errors if errors else None,
        "items": [item.to_dict() for item in all_items[:100]],
    }


@router.get("/{source}/trending", response_model=dict)
async def get_trending(
    source: str,
    timeframe: str = Query("week", regex="^(day|week|month)$"),
    limit: int = Query(30, ge=1, le=100),
):
    """
    Get trending content from a specific source.

    - **source**: One of github, hackernews, reddit
    - **timeframe**: day, week, or month
    - **limit**: Maximum results (1-100)
    """
    if source not in collectors:
        raise HTTPException(status_code=400, detail=f"Unknown source: {source}")

    collector = collectors[source]

    try:
        items = await collector.get_trending(timeframe)
        return {
            "source": source,
            "timeframe": timeframe,
            "total_count": len(items),
            "items": [item.to_dict() for item in items[:limit]],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending: {str(e)}")


@router.get("/sources/list", response_model=dict)
async def list_sources():
    """List all available data sources."""
    return {
        "sources": [
            {
                "name": "github",
                "description": "GitHub repositories, issues, and discussions",
                "requires_auth": False,
                "supports_trending": True,
            },
            {
                "name": "hackernews",
                "description": "Hacker News stories and comments",
                "requires_auth": False,
                "supports_trending": True,
            },
            {
                "name": "reddit",
                "description": "Reddit posts and comments",
                "requires_auth": True,
                "supports_trending": True,
            },
            {
                "name": "web",
                "description": "Web search results",
                "requires_auth": False,
                "supports_trending": False,
            },
        ]
    }