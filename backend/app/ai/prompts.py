"""Prompt templates for Claude analysis."""

SYSTEM_PROMPT = """You are an expert technology analyst specializing in trend analysis and opportunity identification.
Your role is to analyze technology-related content and provide structured, actionable insights.

When analyzing content:
1. Focus on practical applications and real-world use cases
2. Identify emerging trends and patterns
3. Spot opportunities that others might miss
4. Provide specific, actionable recommendations

Always respond in a structured format that can be easily parsed."""


SUMMARY_PROMPT = """Analyze the following content about "{keyword}" and provide a comprehensive summary.

Focus on:
1. What is the main purpose and value proposition?
2. Who is using it and for what?
3. What are the key benefits and challenges?
4. What makes it unique or interesting?

Content:
{contents}

Provide a 2-3 paragraph summary followed by 3-5 key insights as bullet points."""


USE_CASE_PROMPT = """Based on the following content about "{keyword}", identify and classify the main use cases.

For each use case, provide:
1. Name of the use case
2. Brief description
3. Estimated heat level (high/medium/low based on frequency and engagement)

Content:
{contents}

Format your response as numbered items with the format:
1. Use Case Name: Description (Heat: level)"""


TREND_PROMPT = """Analyze the following content about "{keyword}" and identify key trends.

For each trend, indicate:
1. Trend name
2. Direction (rising/stable/declining)
3. Supporting evidence from the content

Content:
{contents}

Format as numbered items:
1. Trend Name: Description [Direction]"""


OPPORTUNITY_PROMPT = """Based on the following content about "{keyword}", identify untapped opportunities and potential blue ocean areas.

Look for:
1. Gaps in current offerings
2. Underserved user segments
3. Novel combinations with other technologies
4. Problems that haven't been adequately solved

Content:
{contents}

Format as numbered items:
1. Opportunity: Description [Potential: high/medium/low] [Difficulty: easy/medium/hard]"""


INNOVATION_PROMPT = """From the following content about "{keyword}", identify the most innovative and interesting application cases.

Focus on:
1. Novel uses of the technology
2. Impressive projects or implementations
3. Creative approaches

Content:
{contents}

Format as numbered items:
1. Case Title: Brief description of the innovation"""


SENTIMENT_PROMPT = """Analyze the overall sentiment toward "{keyword}" in the following content.

Determine:
1. Percentage of positive sentiment (enthusiasm, praise, success stories)
2. Percentage of negative sentiment (criticism, problems, complaints)
3. Percentage of neutral sentiment (factual reporting, balanced views)

Content:
{contents}

Format your response as:
Positive: X%
Negative: X%
Neutral: X%

Followed by a brief explanation of the overall sentiment."""


# Additional prompts for specific analyses
PROJECT_IDEA_PROMPT = """Based on the analysis of "{keyword}", suggest 3-5 concrete project ideas that:
1. Address identified opportunities
2. Leverage current trends
3. Are feasible for an individual developer or small team

For each idea, provide:
- Title
- Description
- Key features
- Target users
- Monetization potential (if applicable)
- Technical complexity estimate

Previous analysis:
{analysis_summary}

Format each idea as a structured description."""