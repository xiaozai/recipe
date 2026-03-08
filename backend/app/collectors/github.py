"""GitHub data collector."""
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx

from .base import BaseCollector
from ..models.content import ContentItem, ContentType, SearchResult
from ..core.config import get_settings


class GitHubCollector(BaseCollector):
    """Collector for GitHub repositories, issues, and discussions."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.token = token or get_settings().github_token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    @property
    def name(self) -> str:
        return "GitHub"

    @property
    def source_type(self) -> str:
        return "github"

    async def _make_request(
        self, client: httpx.AsyncClient, endpoint: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to GitHub API."""
        url = f"{self.BASE_URL}{endpoint}"
        response = await client.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    async def search_repositories(
        self, keyword: str, limit: int = 30
    ) -> List[ContentItem]:
        """Search for repositories."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {
                "q": keyword,
                "sort": "stars",
                "order": "desc",
                "per_page": min(limit, 100),
            }
            data = await self._make_request(client, "/search/repositories", params)

            items = []
            for repo in data.get("items", []):
                item = ContentItem(
                    id=f"github_repo_{repo['id']}",
                    title=repo["full_name"],
                    content=self._truncate_content(
                        repo.get("description") or "No description"
                    ),
                    source_type=ContentType.GITHUB_REPO,
                    url=repo["html_url"],
                    author=repo["owner"]["login"],
                    created_at=datetime.fromisoformat(
                        repo["created_at"].replace("Z", "+00:00")
                    ),
                    updated_at=datetime.fromisoformat(
                        repo["updated_at"].replace("Z", "+00:00")
                    ),
                    score=repo.get("stargazers_count", 0),
                    tags=repo.get("topics", []),
                    metadata={
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "language": repo.get("language"),
                        "open_issues": repo.get("open_issues_count", 0),
                    },
                )
                items.append(item)
            return items

    async def search_issues(
        self, keyword: str, limit: int = 20
    ) -> List[ContentItem]:
        """Search for issues and discussions."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {
                "q": f"{keyword} is:issue OR is:discussion",
                "sort": "updated",
                "order": "desc",
                "per_page": min(limit, 100),
            }
            data = await self._make_request(client, "/search/issues", params)

            items = []
            for issue in data.get("items", []):
                # Determine if it's an issue or discussion
                is_discussion = "discussions" in issue.get("html_url", "")
                content_type = (
                    ContentType.GITHUB_DISCUSSION
                    if is_discussion
                    else ContentType.GITHUB_ISSUE
                )

                item = ContentItem(
                    id=f"github_issue_{issue['id']}",
                    title=issue["title"],
                    content=self._truncate_content(issue.get("body") or issue["title"]),
                    source_type=content_type,
                    url=issue["html_url"],
                    author=issue["user"]["login"],
                    created_at=datetime.fromisoformat(
                        issue["created_at"].replace("Z", "+00:00")
                    ),
                    updated_at=datetime.fromisoformat(
                        issue["updated_at"].replace("Z", "+00:00")
                    ),
                    score=issue.get("comments", 0) + issue.get("reactions", {}).get(
                        "total_count", 0
                    ),
                    tags=issue.get("labels", []),
                    metadata={
                        "state": issue.get("state"),
                        "comments": issue.get("comments", 0),
                        "reactions": issue.get("reactions", {}).get("total_count", 0),
                    },
                )
                items.append(item)
            return items

    async def search(self, keyword: str, limit: int = 50) -> SearchResult:
        """Search GitHub for repositories and issues."""
        repo_limit = limit // 2
        issue_limit = limit - repo_limit

        # Run searches in parallel
        repos_task = self.search_repositories(keyword, repo_limit)
        issues_task = self.search_issues(keyword, issue_limit)

        repos, issues = await asyncio.gather(
            repos_task, issues_task, return_exceptions=True
        )

        items = []
        if isinstance(repos, list):
            items.extend(repos)
        if isinstance(issues, list):
            items.extend(issues)

        return SearchResult(
            keyword=keyword,
            items=items,
            total_count=len(items),
            source=self.name,
        )

    async def get_trending(self, timeframe: str = "week") -> List[ContentItem]:
        """Get trending repositories (using search with created filter)."""
        from datetime import datetime, timedelta

        # Map timeframe to days
        days_map = {"day": 1, "week": 7, "month": 30}
        days = days_map.get(timeframe, 7)

        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {
                "q": f"created:>{since}",
                "sort": "stars",
                "order": "desc",
                "per_page": 30,
            }
            data = await self._make_request(client, "/search/repositories", params)

            items = []
            for repo in data.get("items", []):
                item = ContentItem(
                    id=f"github_repo_{repo['id']}",
                    title=repo["full_name"],
                    content=self._truncate_content(
                        repo.get("description") or "No description"
                    ),
                    source_type=ContentType.GITHUB_REPO,
                    url=repo["html_url"],
                    author=repo["owner"]["login"],
                    created_at=datetime.fromisoformat(
                        repo["created_at"].replace("Z", "+00:00")
                    ),
                    score=repo.get("stargazers_count", 0),
                    tags=repo.get("topics", []),
                    metadata={
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language"),
                    },
                )
                items.append(item)
            return items