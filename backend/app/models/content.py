"""Content data models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class ContentType(str, Enum):
    """Type of content source."""
    GITHUB_REPO = "github_repo"
    GITHUB_ISSUE = "github_issue"
    GITHUB_DISCUSSION = "github_discussion"
    REDDIT_POST = "reddit_post"
    REDDIT_COMMENT = "reddit_comment"
    HACKERNEWS = "hackernews"
    TWITTER = "twitter"
    BLOG = "blog"
    VIDEO = "video"
    UNKNOWN = "unknown"


@dataclass
class ContentItem:
    """A single content item from any source."""
    id: str
    title: str
    content: str
    source_type: ContentType
    url: str
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    score: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "source_type": self.source_type.value,
            "url": self.url,
            "author": self.author,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "score": self.score,
            "tags": self.tags,
            "metadata": self.metadata,
        }


@dataclass
class SearchResult:
    """Result from a search operation."""
    keyword: str
    items: List[ContentItem]
    total_count: int
    source: str
    collected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "keyword": self.keyword,
            "items": [item.to_dict() for item in self.items],
            "total_count": self.total_count,
            "source": self.source,
            "collected_at": self.collected_at.isoformat(),
        }