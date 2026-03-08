"""Report generation service."""
from typing import Dict, Any, Optional
from datetime import datetime

from ..models.report import Report, ReportSection, ReportFormat
from ..models.analysis import AnalysisResult


class ReportService:
    """Service for generating formatted reports."""

    async def generate_report(
        self,
        keyword: str,
        analysis_result: Dict[str, Any],
        format: ReportFormat = ReportFormat.MARKDOWN,
        include_items: bool = False,
    ) -> Report:
        """Generate a comprehensive report from analysis results."""
        analysis = analysis_result.get("analysis", analysis_result)

        # Build sections
        sections = []

        # Executive Summary
        summary_section = ReportSection(
            title="Executive Summary",
            content=self._format_summary(analysis),
        )
        sections.append(summary_section)

        # Use Cases
        use_cases = analysis.get("use_cases", [])
        if use_cases:
            use_case_section = ReportSection(
                title="Popular Use Cases",
                content=self._format_use_cases(use_cases),
            )
            sections.append(use_case_section)

        # Trends
        trends = analysis.get("trends", [])
        if trends:
            trend_section = ReportSection(
                title="Trend Analysis",
                content=self._format_trends(trends),
            )
            sections.append(trend_section)

        # Innovation Cases
        innovation_cases = analysis.get("innovation_cases", [])
        if innovation_cases:
            innovation_section = ReportSection(
                title="Innovative Applications",
                content=self._format_innovation_cases(innovation_cases),
            )
            sections.append(innovation_section)

        # Opportunities
        opportunities = analysis.get("opportunities", [])
        if opportunities:
            opportunity_section = ReportSection(
                title="Opportunities & Recommendations",
                content=self._format_opportunities(opportunities),
            )
            sections.append(opportunity_section)

        # Sentiment
        sentiment = analysis.get("sentiment", {})
        if sentiment:
            sentiment_section = ReportSection(
                title="Community Sentiment",
                content=self._format_sentiment(sentiment),
            )
            sections.append(sentiment_section)

        # Collected Items (optional)
        if include_items:
            items = analysis_result.get("items", [])
            if items:
                items_section = ReportSection(
                    title="Collected Resources",
                    content=self._format_items(items[:50]),
                )
                sections.append(items_section)

        # Create report
        report = Report(
            keyword=keyword,
            title=f"{keyword} Technology Trend Analysis Report",
            summary=analysis.get("summary", "No summary available."),
            sections=sections,
            format=format,
            metadata={
                "content_count": analysis.get("content_count", 0),
                "generated_by": "Tech Trend Analyzer",
            },
        )

        return report

    def _format_summary(self, analysis: Dict[str, Any]) -> str:
        """Format the executive summary."""
        summary = analysis.get("summary", "")
        key_insights = analysis.get("key_insights", [])
        content_count = analysis.get("content_count", 0)

        lines = [
            summary,
            "",
            f"**Analyzed {content_count} content items.**",
            "",
        ]

        if key_insights:
            lines.append("**Key Insights:**")
            for insight in key_insights:
                lines.append(f"- {insight}")

        return "\n".join(lines)

    def _format_use_cases(self, use_cases: list) -> str:
        """Format use cases section."""
        lines = ["| Use Case | Description | Heat Level |", "|----------|-------------|------------|"]

        for uc in use_cases:
            name = uc.get("name", "Unknown")
            desc = uc.get("description", "")[:50]
            heat = uc.get("heat_level", "medium")
            lines.append(f"| {name} | {desc}... | {heat} |")

        return "\n".join(lines)

    def _format_trends(self, trends: list) -> str:
        """Format trends section."""
        lines = []

        for trend in trends:
            name = trend.get("name", "Unknown")
            direction = trend.get("direction", "stable")
            desc = trend.get("description", "")
            confidence = trend.get("confidence", 0)

            # Direction emoji
            direction_emoji = {"rising": "📈", "stable": "➡️", "declining": "📉"}.get(
                direction, "➡️"
            )

            lines.append(f"### {direction_emoji} {name}")
            lines.append(f"- **Direction**: {direction}")
            lines.append(f"- **Confidence**: {confidence:.0%}")
            lines.append(f"- **Description**: {desc}")
            lines.append("")

        return "\n".join(lines)

    def _format_innovation_cases(self, cases: list) -> str:
        """Format innovation cases section."""
        lines = []

        for i, case in enumerate(cases, 1):
            title = case.get("title", f"Case {i}")
            desc = case.get("description", "")
            url = case.get("source_url", "")

            lines.append(f"### {i}. {title}")
            lines.append(desc)
            if url:
                lines.append(f"[Source]({url})")
            lines.append("")

        return "\n".join(lines)

    def _format_opportunities(self, opportunities: list) -> str:
        """Format opportunities section."""
        lines = ["### Blue Ocean Areas", ""]

        for opp in opportunities:
            title = opp.get("title", "Unknown")
            desc = opp.get("description", "")
            potential = opp.get("potential", "medium")
            difficulty = opp.get("difficulty", "medium")

            lines.append(f"#### {title}")
            lines.append(f"- **Potential**: {potential}")
            lines.append(f"- **Difficulty**: {difficulty}")
            lines.append(f"- **Description**: {desc}")
            lines.append("")

        return "\n".join(lines)

    def _format_sentiment(self, sentiment: Dict[str, Any]) -> str:
        """Format sentiment section."""
        positive = sentiment.get("positive", 0)
        negative = sentiment.get("negative", 0)
        neutral = sentiment.get("neutral", 0)

        lines = [
            f"- **Positive**: {positive}%",
            f"- **Neutral**: {neutral}%",
            f"- **Negative**: {negative}%",
            "",
        ]

        # Overall assessment
        if positive > 50:
            lines.append("**Overall**: The community sentiment is predominantly positive.")
        elif negative > 50:
            lines.append("**Overall**: There are significant concerns in the community.")
        else:
            lines.append("**Overall**: The community sentiment is balanced.")

        return "\n".join(lines)

    def _format_items(self, items: list) -> str:
        """Format collected items section."""
        lines = ["### Resources", ""]

        for item in items:
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            source = item.get("source_type", "unknown")

            if url:
                lines.append(f"- [{title}]({url}) ({source})")
            else:
                lines.append(f"- {title} ({source})")

        return "\n".join(lines)