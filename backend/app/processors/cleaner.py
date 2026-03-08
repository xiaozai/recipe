"""Content cleaner for data preprocessing."""
import re
import html
from typing import Optional
from ..models.content import ContentItem


class ContentCleaner:
    """Cleans and normalizes content items."""

    # Patterns to remove
    HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
    URL_PATTERN = re.compile(r"https?://\S+")
    MENTION_PATTERN = re.compile(r"@\w+")
    HASHTAG_PATTERN = re.compile(r"#\w+")
    WHITESPACE_PATTERN = re.compile(r"\s+")
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )

    def __init__(
        self,
        remove_urls: bool = False,
        remove_mentions: bool = True,
        remove_hashtags: bool = False,
        remove_emojis: bool = False,
        min_content_length: int = 10,
    ):
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_emojis = remove_emojis
        self.min_content_length = min_content_length

    def clean(self, item: ContentItem) -> ContentItem:
        """Clean a content item in place."""
        # Clean title
        item.title = self._clean_text(item.title)

        # Clean content
        item.content = self._clean_text(item.content)

        # Clean author
        if item.author:
            item.author = self._clean_text(item.author, remove_emojis=True)

        # Clean tags
        item.tags = [self._clean_text(tag, remove_emojis=True) for tag in item.tags]
        item.tags = [tag for tag in item.tags if tag]  # Remove empty tags

        return item

    def _clean_text(self, text: str, remove_emojis: bool = False) -> str:
        """Clean a text string."""
        if not text:
            return ""

        # Decode HTML entities
        text = html.unescape(text)

        # Remove HTML tags
        text = self.HTML_TAG_PATTERN.sub(" ", text)

        # Optional removals
        if self.remove_urls:
            text = self.URL_PATTERN.sub("", text)

        if self.remove_mentions:
            text = self.MENTION_PATTERN.sub("", text)

        if self.remove_hashtags:
            text = self.HASHTAG_PATTERN.sub("", text)

        if self.remove_emojis or remove_emojis:
            text = self.EMOJI_PATTERN.sub("", text)

        # Normalize whitespace
        text = self.WHITESPACE_PATTERN.sub(" ", text)

        # Strip
        text = text.strip()

        return text

    def is_valid(self, item: ContentItem) -> bool:
        """Check if an item is valid after cleaning."""
        if not item.title or len(item.title) < 3:
            return False

        if not item.content or len(item.content) < self.min_content_length:
            return False

        return True