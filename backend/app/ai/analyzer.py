"""Main analyzer module that orchestrates the analysis pipeline."""
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from collections import Counter

from ..models.content import ContentItem, SearchResult
from ..models.analysis import AnalysisResult
from ..collectors import (
    GitHubCollector,
    HackerNewsCollector,
    RedditCollector,
    WebSearchCollector,
)
from ..processors.cleaner import ContentCleaner
from ..processors.deduplicator import ContentDeduplicator
from .claude_engine import ClaudeEngine


class TrendAnalyzer:
    """Main analyzer that orchestrates data collection and analysis."""

    def __init__(self, api_key: Optional[str] = None):
        self.claude_engine = ClaudeEngine(api_key)
        self.cleaner = ContentCleaner()
        self.deduplicator = ContentDeduplicator()

        # Initialize collectors - all available collectors
        self.collectors = {
            "github": GitHubCollector(),
            "hackernews": HackerNewsCollector(),
            "web": WebSearchCollector(),
            # Reddit requires credentials, add conditionally
            # "reddit": RedditCollector(),
        }

    async def collect_data(
        self, keyword: str, sources: Optional[List[str]] = None, limit: int = 50
    ) -> tuple[List[ContentItem], Dict[str, int]]:
        """Collect data from multiple sources.

        Returns:
            Tuple of (items, source_counts)
        """
        # Determine which collectors to use
        if sources:
            active_collectors = {
                name: collector for name, collector in self.collectors.items()
                if name in sources
            }
        else:
            active_collectors = self.collectors

        if not active_collectors:
            return [], {}

        # Run all collectors in parallel
        tasks = [collector.search(keyword, limit) for collector in active_collectors.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine all items and count by source
        all_items = []
        source_counts = {}

        for (name, result) in zip(active_collectors.keys(), results):
            if isinstance(result, SearchResult):
                all_items.extend(result.items)
                source_counts[name] = len(result.items)
            elif isinstance(result, Exception):
                source_counts[name] = 0
                print(f"Error collecting from {name}: {result}")

        return all_items, source_counts

    async def analyze(
        self,
        keyword: str,
        sources: Optional[List[str]] = None,
        limit: int = 50,
        skip_collection: bool = False,
        existing_items: Optional[List[ContentItem]] = None,
    ) -> Dict[str, Any]:
        """Run complete analysis pipeline."""
        start_time = datetime.now()

        # Step 1: Collect data
        if skip_collection and existing_items:
            items = existing_items
            source_counts = {}
        else:
            items, source_counts = await self.collect_data(keyword, sources, limit)

        collection_time = datetime.now()

        # Step 2: Clean data
        items = [self.cleaner.clean(item) for item in items]

        # Step 3: Deduplicate
        items = self.deduplicator.deduplicate(items)

        processing_time = datetime.now()

        # Step 4: Analyze with Claude
        analysis_result = await self.claude_engine.analyze_all(items, keyword)

        analysis_time = datetime.now()

        # Build result with source_counts
        result = {
            "keyword": keyword,
            "analysis": analysis_result.to_dict(),
            "source_counts": source_counts,  # Add source counts for charts
            "metadata": {
                "total_items_collected": len(items),
                "sources_used": list(source_counts.keys()),
                "timings": {
                    "collection_seconds": (collection_time - start_time).total_seconds(),
                    "processing_seconds": (processing_time - collection_time).total_seconds(),
                    "analysis_seconds": (analysis_time - processing_time).total_seconds(),
                    "total_seconds": (analysis_time - start_time).total_seconds(),
                },
            },
            "items": [item.to_dict() for item in items[:100]],  # Limit stored items
        }

        return result

    async def quick_analysis(self, keyword: str) -> Dict[str, Any]:
        """Run a quick analysis with limited sources."""
        # Use only the fastest collectors
        quick_collectors = {
            "hackernews": HackerNewsCollector(),
            "web": WebSearchCollector(),
        }

        tasks = [collector.search(keyword, limit=20) for collector in quick_collectors.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        items = []
        source_counts = {}
        for (name, result) in zip(quick_collectors.keys(), results):
            if isinstance(result, SearchResult):
                items.extend(result.items)
                source_counts[name] = len(result.items)
            elif isinstance(result, Exception):
                source_counts[name] = 0

        # Quick clean
        items = [self.cleaner.clean(item) for item in items]
        items = self.deduplicator.deduplicate(items)

        # Get summary only
        summary = await self.claude_engine.summarize_contents(items, keyword)

        return {
            "keyword": keyword,
            "summary": summary,
            "item_count": len(items),
            "source_counts": source_counts,
            "items": [item.to_dict() for item in items[:20]],
        }

    def add_collector(self, name: str, collector):
        """Add a custom collector."""
        self.collectors[name] = collector

    def remove_collector(self, collector_name: str):
        """Remove a collector by name."""
        if collector_name in self.collectors:
            del self.collectors[collector_name]

    async def analyze_single_project(
        self, item: ContentItem, keyword: str
    ) -> Dict[str, Any]:
        """Analyze a single project/item to understand what it does."""
        try:
            result = await self.claude_engine.analyze_project(item, keyword)
            return result
        except Exception:
            # Fallback to basic extraction if AI analysis fails
            return {
                "title": item.title,
                "url": item.url,
                "source_type": item.source_type.value if item.source_type else "unknown",
                "what_it_does": item.content[:200] if item.content else item.title,
                "key_features": [],
                "relevance_score": 50.0,
            }

    async def generate_trend_summary(
        self,
        items: List[ContentItem],
        keyword: str,
        analyzed_projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate overall trend summary from analyzed projects."""
        try:
            result = await self.claude_engine.generate_trend_summary(
                items, keyword, analyzed_projects
            )
            return result
        except Exception:
            # Fallback to basic summary
            return {
                "main_themes": [keyword],
                "technology_stack": [],
                "common_patterns": [],
                "emerging_trends": [],
                "market_sentiment": "neutral",
                "recommendation": "Continue monitoring this technology space.",
            }

    async def quick_project_summary(
        self, items: List[ContentItem], keyword: str
    ) -> Dict[str, Any]:
        """Quick summary without LLM analysis."""
        # Extract keywords and patterns heuristically
        all_content = " ".join([
            f"{item.title} {item.content or ''}"
            for item in items[:50]
        ]).lower()

        # Common tech keywords to look for
        tech_keywords = [
            "api", "sdk", "library", "framework", "tool", "platform",
            "machine learning", "ai", "llm", "nlp", "vector", "database",
            "react", "vue", "angular", "python", "javascript", "typescript",
            "docker", "kubernetes", "cloud", "serverless", "microservice"
        ]

        found_tech = []
        for tech in tech_keywords:
            if tech in all_content:
                found_tech.append(tech)

        return {
            "keyword": keyword,
            "total_items": len(items),
            "detected_technologies": found_tech,
            "sample_projects": [
                {
                    "title": item.title,
                    "url": item.url,
                    "source_type": item.source_type.value if item.source_type else "unknown",
                }
                for item in items[:10]
            ],
        }