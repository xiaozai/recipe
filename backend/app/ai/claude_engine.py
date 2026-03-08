"""AI API integration for content analysis. Supports Anthropic and OpenAI formats."""
import asyncio
from typing import List, Optional, Dict, Any
import httpx

from ..models.content import ContentItem
from ..models.analysis import (
    AnalysisResult,
    UseCase,
    Trend,
    Opportunity,
    InnovationCase,
)
from ..core.config import get_settings
from . import prompts


class AIEngine:
    """AI-based analysis engine supporting both Anthropic and OpenAI formats."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        api_type: Optional[str] = None,
    ):
        settings = get_settings()
        self.api_key = api_key or settings.get_effective_api_key()
        self.base_url = base_url or settings.get_effective_base_url()
        self.model = model or settings.get_effective_model()
        self.api_type = api_type or settings.api_type
        self.max_tokens = settings.max_tokens

        # 确保 base_url 不以斜杠结尾
        if self.base_url and self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]

    async def _call_api(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make a call to AI API (supports both Anthropic and OpenAI formats)."""
        if not self.api_key:
            raise ValueError("API key not configured. Please set API_KEY in .env file.")

        if self.api_type == "anthropic":
            return await self._call_anthropic(prompt, system_prompt, max_tokens)
        else:
            return await self._call_openai(prompt, system_prompt, max_tokens)

    async def _call_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Call Anthropic API format."""
        url = f"{self.base_url}/v1/messages"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]

    async def _call_openai(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Call OpenAI API format."""
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": messages,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def summarize_contents(
        self, contents: List[ContentItem], keyword: str
    ) -> str:
        """Generate a summary of collected contents."""
        content_text = self._format_contents_for_prompt(contents[:20])
        prompt = prompts.SUMMARY_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        return await self._call_api(prompt, prompts.SYSTEM_PROMPT)

    async def classify_use_cases(
        self, contents: List[ContentItem], keyword: str
    ) -> List[UseCase]:
        """Identify and classify use cases."""
        content_text = self._format_contents_for_prompt(contents[:30])
        prompt = prompts.USE_CASE_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        response = await self._call_api(prompt, prompts.SYSTEM_PROMPT)

        # Parse structured response
        use_cases = self._parse_use_cases(response)
        return use_cases

    async def identify_trends(
        self, contents: List[ContentItem], keyword: str
    ) -> List[Trend]:
        """Identify trends in the content."""
        content_text = self._format_contents_for_prompt(contents[:30])
        prompt = prompts.TREND_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        response = await self._call_api(prompt, prompts.SYSTEM_PROMPT)

        trends = self._parse_trends(response)
        return trends

    async def find_opportunities(
        self, contents: List[ContentItem], keyword: str
    ) -> List[Opportunity]:
        """Find potential opportunities."""
        content_text = self._format_contents_for_prompt(contents[:20])
        prompt = prompts.OPPORTUNITY_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        response = await self._call_api(prompt, prompts.SYSTEM_PROMPT)

        opportunities = self._parse_opportunities(response)
        return opportunities

    async def find_innovation_cases(
        self, contents: List[ContentItem], keyword: str
    ) -> List[InnovationCase]:
        """Find innovative application cases."""
        content_text = self._format_contents_for_prompt(contents[:15])
        prompt = prompts.INNOVATION_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        response = await self._call_api(prompt, prompts.SYSTEM_PROMPT)

        cases = self._parse_innovation_cases(response)
        return cases

    async def analyze_sentiment(
        self, contents: List[ContentItem], keyword: str
    ) -> Dict[str, Any]:
        """Analyze overall sentiment."""
        content_text = self._format_contents_for_prompt(contents[:20])
        prompt = prompts.SENTIMENT_PROMPT.format(
            keyword=keyword, contents=content_text
        )

        response = await self._call_api(prompt, prompts.SYSTEM_PROMPT)

        # Parse sentiment response
        sentiment = self._parse_sentiment(response)
        return sentiment

    async def analyze_all(
        self, contents: List[ContentItem], keyword: str
    ) -> AnalysisResult:
        """Run full analysis pipeline."""
        if not contents:
            return AnalysisResult(
                keyword=keyword,
                summary="No content found for analysis.",
                key_insights=[],
                use_cases=[],
                trends=[],
                opportunities=[],
                innovation_cases=[],
                sentiment={"positive": 0, "negative": 0, "neutral": 100},
                content_count=0,
            )

        # Run all analyses in parallel
        tasks = [
            self.summarize_contents(contents, keyword),
            self.classify_use_cases(contents, keyword),
            self.identify_trends(contents, keyword),
            self.find_opportunities(contents, keyword),
            self.find_innovation_cases(contents, keyword),
            self.analyze_sentiment(contents, keyword),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        summary = results[0] if not isinstance(results[0], Exception) else ""
        use_cases = results[1] if not isinstance(results[1], Exception) else []
        trends = results[2] if not isinstance(results[2], Exception) else []
        opportunities = results[3] if not isinstance(results[3], Exception) else []
        innovation_cases = results[4] if not isinstance(results[4], Exception) else []
        sentiment = (
            results[5]
            if not isinstance(results[5], Exception)
            else {"positive": 0, "negative": 0, "neutral": 100}
        )

        # Extract key insights from summary
        key_insights = self._extract_key_insights(summary)

        return AnalysisResult(
            keyword=keyword,
            summary=summary,
            key_insights=key_insights,
            use_cases=use_cases,
            trends=trends,
            opportunities=opportunities,
            innovation_cases=innovation_cases,
            sentiment=sentiment,
            content_count=len(contents),
        )

    def _format_contents_for_prompt(
        self, contents: List[ContentItem], max_items: int = 30
    ) -> str:
        """Format contents for prompt inclusion."""
        formatted = []
        for i, item in enumerate(contents[:max_items], 1):
            formatted.append(
                f"{i}. [{item.source_type.value}] {item.title}\n"
                f"   URL: {item.url}\n"
                f"   Content: {item.content[:500]}...\n"
            )
        return "\n".join(formatted)

    def _parse_use_cases(self, response: str) -> List[UseCase]:
        """Parse use cases from AI response."""
        use_cases = []
        lines = response.split("\n")

        current_case = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for numbered items or bullet points
            if line[0].isdigit() or line.startswith("-") or line.startswith("*"):
                if current_case:
                    use_cases.append(current_case)

                # Parse the line
                parts = line.split(":", 1)
                name = parts[0].lstrip("0123456789.-* ")
                description = parts[1].strip() if len(parts) > 1 else ""

                current_case = UseCase(
                    name=name,
                    description=description,
                    heat_level="medium",
                    examples=[],
                    source_count=0,
                )

        if current_case:
            use_cases.append(current_case)

        return use_cases[:10]

    def _parse_trends(self, response: str) -> List[Trend]:
        """Parse trends from AI response."""
        trends = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Simple parsing
            if line[0].isdigit() or line.startswith("-") or line.startswith("*"):
                parts = line.split(":", 1)
                name = parts[0].lstrip("0123456789.-* ")
                description = parts[1].strip() if len(parts) > 1 else ""

                # Determine direction from keywords
                direction = "stable"
                if any(kw in line.lower() for kw in ["rising", "growing", "increasing"]):
                    direction = "rising"
                elif any(kw in line.lower() for kw in ["declining", "decreasing", "falling"]):
                    direction = "declining"

                trends.append(
                    Trend(
                        name=name,
                        direction=direction,
                        description=description,
                        confidence=0.7,
                        supporting_evidence=[],
                    )
                )

        return trends[:10]

    def _parse_opportunities(self, response: str) -> List[Opportunity]:
        """Parse opportunities from AI response."""
        opportunities = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit() or line.startswith("-") or line.startswith("*"):
                parts = line.split(":", 1)
                title = parts[0].lstrip("0123456789.-* ")
                description = parts[1].strip() if len(parts) > 1 else ""

                opportunities.append(
                    Opportunity(
                        title=title,
                        description=description,
                        potential="medium",
                        difficulty="medium",
                        reasons=[],
                    )
                )

        return opportunities[:5]

    def _parse_innovation_cases(self, response: str) -> List[InnovationCase]:
        """Parse innovation cases from AI response."""
        cases = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit() or line.startswith("-") or line.startswith("*"):
                parts = line.split(":", 1)
                title = parts[0].lstrip("0123456789.-* ")
                description = parts[1].strip() if len(parts) > 1 else ""

                cases.append(
                    InnovationCase(
                        title=title,
                        description=description,
                        source_url="",
                        author=None,
                        key_features=[],
                    )
                )

        return cases[:5]

    def _parse_sentiment(self, response: str) -> Dict[str, Any]:
        """Parse sentiment analysis from AI response."""
        sentiment = {"positive": 33, "negative": 33, "neutral": 34}

        response_lower = response.lower()

        # Try to extract percentages
        import re

        for sentiment_type in ["positive", "negative", "neutral"]:
            pattern = rf"{sentiment_type}[:\s]+(\d+)%?"
            match = re.search(pattern, response_lower)
            if match:
                sentiment[sentiment_type] = int(match.group(1))

        return sentiment

    def _extract_key_insights(self, summary: str) -> List[str]:
        """Extract key insights from summary."""
        insights = []

        # Simple extraction based on bullet points or numbered items
        lines = summary.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                insights.append(line.lstrip("-* "))
            elif line and line[0].isdigit() and "." in line[:3]:
                insights.append(line.split(".", 1)[1].strip())

        return insights[:5]

    async def analyze_project(
        self, item: ContentItem, keyword: str
    ) -> Dict[str, Any]:
        """Analyze a single project to understand what it does."""
        try:
            prompt = f"""Analyze this project and explain what it does in detail.

Keyword/Topic: {keyword}

Project Title: {item.title}
Project URL: {item.url}
Project Content: {item.content[:500] if item.content else 'No detailed content available'}

Please provide:
1. A clear explanation of what this project does (2-3 sentences)
2. Key features or capabilities (as a list)
3. How it relates to "{keyword}"
4. A relevance score from 0-100

Format your response as JSON:
{{
    "what_it_does": "explanation",
    "key_features": ["feature1", "feature2"],
    "relation_to_keyword": "explanation",
    "relevance_score": 85
}}"""

            response = await self._call_api(prompt)

            # Parse JSON response
            import json
            import re

            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = {
                    "what_it_does": response[:200],
                    "key_features": [],
                    "relation_to_keyword": "Related to " + keyword,
                    "relevance_score": 50,
                }

            return {
                "title": item.title,
                "url": item.url,
                "source_type": item.source_type.value if item.source_type else "unknown",
                "what_it_does": parsed.get("what_it_does", "No description available"),
                "key_features": parsed.get("key_features", []),
                "relevance_score": parsed.get("relevance_score", 50),
            }
        except Exception as e:
            print(f"Error analyzing project: {e}")
            return None

    async def generate_trend_summary(
        self,
        items: List[ContentItem],
        keyword: str,
        analyzed_projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate overall trend summary from analyzed projects."""
        try:
            # Prepare content for analysis
            projects_text = "\n\n".join([
                f"- {p['title']}: {p['what_it_does']}\n  Features: {', '.join(p['key_features']) if p['key_features'] else 'N/A'}"
                for p in analyzed_projects[:10]
            ])

            prompt = f"""Based on the analysis of projects related to "{keyword}", provide a comprehensive trend summary.

Analyzed Projects:
{projects_text}

Please provide:
1. Main themes or patterns you observe
2. Common technology stack or tools mentioned
3. Emerging trends or innovations
4. Overall market sentiment (positive/neutral/negative)
5. A recommendation for someone interested in this space

Format your response as JSON:
{{
    "main_themes": ["theme1", "theme2"],
    "technology_stack": ["tech1", "tech2"],
    "common_patterns": ["pattern1", "pattern2"],
    "emerging_trends": ["trend1", "trend2"],
    "market_sentiment": "positive|neutral|negative",
    "recommendation": "your recommendation here"
}}"""

            response = await self._call_api(prompt)

            # Parse JSON response
            import json
            import re

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = {
                    "main_themes": [keyword],
                    "technology_stack": [],
                    "common_patterns": [],
                    "emerging_trends": [],
                    "market_sentiment": "neutral",
                    "recommendation": "Continue monitoring and exploring this technology.",
                }

            return parsed
        except Exception as e:
            print(f"Error generating trend summary: {e}")
            return {
                "main_themes": [keyword],
                "technology_stack": [],
                "common_patterns": [],
                "emerging_trends": [],
                "market_sentiment": "neutral",
                "recommendation": "Continue monitoring this technology space.",
            }


# Backward compatibility alias
ClaudeEngine = AIEngine