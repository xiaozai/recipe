"""Analysis result models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class UseCase:
    """A detected use case."""
    name: str
    description: str
    heat_level: str  # high, medium, low
    examples: List[str]
    source_count: int = 0


@dataclass
class Trend:
    """A detected trend."""
    name: str
    direction: str  # rising, stable, declining
    description: str
    confidence: float  # 0.0 - 1.0
    supporting_evidence: List[str]


@dataclass
class Opportunity:
    """An identified opportunity."""
    title: str
    description: str
    potential: str  # high, medium, low
    difficulty: str  # easy, medium, hard
    reasons: List[str]


@dataclass
class InnovationCase:
    """An innovative application case."""
    title: str
    description: str
    source_url: str
    author: Optional[str]
    key_features: List[str]


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    keyword: str
    summary: str
    key_insights: List[str]
    use_cases: List[UseCase]
    trends: List[Trend]
    opportunities: List[Opportunity]
    innovation_cases: List[InnovationCase]
    sentiment: Dict[str, Any]  # positive, negative, neutral ratios
    analyzed_at: datetime = field(default_factory=datetime.now)
    content_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "keyword": self.keyword,
            "summary": self.summary,
            "key_insights": self.key_insights,
            "use_cases": [
                {
                    "name": uc.name,
                    "description": uc.description,
                    "heat_level": uc.heat_level,
                    "examples": uc.examples,
                    "source_count": uc.source_count,
                }
                for uc in self.use_cases
            ],
            "trends": [
                {
                    "name": t.name,
                    "direction": t.direction,
                    "description": t.description,
                    "confidence": t.confidence,
                    "supporting_evidence": t.supporting_evidence,
                }
                for t in self.trends
            ],
            "opportunities": [
                {
                    "title": o.title,
                    "description": o.description,
                    "potential": o.potential,
                    "difficulty": o.difficulty,
                    "reasons": o.reasons,
                }
                for o in self.opportunities
            ],
            "innovation_cases": [
                {
                    "title": ic.title,
                    "description": ic.description,
                    "source_url": ic.source_url,
                    "author": ic.author,
                    "key_features": ic.key_features,
                }
                for ic in self.innovation_cases
            ],
            "sentiment": self.sentiment,
            "analyzed_at": self.analyzed_at.isoformat(),
            "content_count": self.content_count,
        }