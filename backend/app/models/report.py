"""Report generation models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum


class ReportFormat(str, Enum):
    """Report output format."""
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"


@dataclass
class ReportSection:
    """A section in the report."""
    title: str
    content: str
    subsections: List["ReportSection"] = field(default_factory=list)


@dataclass
class Report:
    """Generated report."""
    keyword: str
    title: str
    summary: str
    sections: List[ReportSection]
    generated_at: datetime = field(default_factory=datetime.now)
    format: ReportFormat = ReportFormat.MARKDOWN
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Convert report to Markdown format."""
        lines = [
            f"# {self.title}",
            "",
            f"*Generated at: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            f"## Summary",
            "",
            self.summary,
            "",
        ]

        for section in self.sections:
            lines.extend(self._section_to_markdown(section, level=2))

        return "\n".join(lines)

    def _section_to_markdown(self, section: ReportSection, level: int) -> List[str]:
        """Convert a section to markdown lines."""
        lines = [
            f"{'#' * level} {section.title}",
            "",
            section.content,
            "",
        ]

        for subsection in section.subsections:
            lines.extend(self._section_to_markdown(subsection, level + 1))

        return lines

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "keyword": self.keyword,
            "title": self.title,
            "summary": self.summary,
            "sections": [
                {
                    "title": s.title,
                    "content": s.content,
                    "subsections": [
                        {"title": ss.title, "content": ss.content}
                        for ss in s.subsections
                    ],
                }
                for s in self.sections
            ],
            "generated_at": self.generated_at.isoformat(),
            "format": self.format.value,
            "metadata": self.metadata,
        }