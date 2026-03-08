"""Content deduplicator for removing duplicates."""
from typing import List, Dict, Set
import hashlib
from ..models.content import ContentItem


class ContentDeduplicator:
    """Removes duplicate content items."""

    def __init__(
        self,
        use_url: bool = True,
        use_content_hash: bool = True,
        use_title_similarity: bool = True,
        similarity_threshold: float = 0.9,
    ):
        self.use_url = use_url
        self.use_content_hash = use_content_hash
        self.use_title_similarity = use_title_similarity
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, items: List[ContentItem]) -> List[ContentItem]:
        """Remove duplicate items from a list."""
        if not items:
            return items

        seen_urls: Set[str] = set()
        seen_hashes: Set[str] = set()
        seen_titles: List[str] = []

        unique_items = []

        for item in items:
            # Check URL
            if self.use_url and item.url:
                if item.url in seen_urls:
                    continue
                seen_urls.add(item.url)

            # Check content hash
            if self.use_content_hash:
                content_hash = self._hash_content(item.content)
                if content_hash in seen_hashes:
                    continue
                seen_hashes.add(content_hash)

            # Check title similarity
            if self.use_title_similarity:
                if self._is_similar_title(item.title, seen_titles):
                    continue
                seen_titles.append(item.title.lower())

            unique_items.append(item)

        return unique_items

    def _hash_content(self, content: str) -> str:
        """Generate a hash for content."""
        # Normalize content for hashing
        normalized = content.lower().strip()
        normalized = "".join(normalized.split())  # Remove all whitespace

        return hashlib.md5(normalized.encode()).hexdigest()

    def _is_similar_title(self, title: str, seen_titles: List[str]) -> bool:
        """Check if a title is similar to any seen titles."""
        if not seen_titles:
            return False

        title_lower = title.lower()

        for seen in seen_titles:
            similarity = self._calculate_similarity(title_lower, seen)
            if similarity >= self.similarity_threshold:
                return True

        return False

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using Jaccard similarity."""
        if not text1 or not text2:
            return 0.0

        # Split into words
        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0