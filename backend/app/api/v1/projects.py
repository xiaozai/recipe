"""Project analysis API endpoints."""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...models.content import ContentItem, ContentType
from ...ai import TrendAnalyzer

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectAnalysisRequest(BaseModel):
    """Request model for project analysis."""
    items: List[Dict[str, Any]]
    keyword: str


def dict_to_content_item(item_data: Dict[str, Any]) -> Optional[ContentItem]:
    """Convert a dictionary to ContentItem object."""
    try:
        # Generate an ID if not present
        item_id = item_data.get("id", f"item_{hash(item_data.get('title', '')) % 100000}")

        # Handle source_type conversion
        source_type_str = item_data.get("source_type", "unknown")
        if isinstance(source_type_str, str):
            try:
                source_type = ContentType(source_type_str)
            except ValueError:
                # Map common string values to ContentType
                type_mapping = {
                    "github": ContentType.GITHUB_REPO,
                    "github_repo": ContentType.GITHUB_REPO,
                    "hackernews": ContentType.HACKERNEWS,
                    "reddit": ContentType.REDDIT_POST,
                    "blog": ContentType.BLOG,
                    "web": ContentType.UNKNOWN,
                }
                source_type = type_mapping.get(source_type_str.lower(), ContentType.UNKNOWN)

        # Parse datetime strings if present
        from datetime import datetime

        created_at = item_data.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError:
                created_at = None

        updated_at = item_data.get("updated_at")
        if isinstance(updated_at, str):
            try:
                updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            except ValueError:
                updated_at = None

        return ContentItem(
            id=str(item_id),
            title=str(item_data.get("title", "Untitled")),
            content=str(item_data.get("content", "")),
            source_type=source_type,
            url=str(item_data.get("url", "")),
            author=item_data.get("author"),
            created_at=created_at,
            updated_at=updated_at,
            score=item_data.get("score"),
            tags=item_data.get("tags", []),
            metadata=item_data.get("metadata", {}),
        )
    except Exception as e:
        print(f"Error converting item: {e}")
        return None


@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_projects(request: ProjectAnalysisRequest):
    """
    Analyze search results to understand what each project does and summarize trends.

    - **items**: List of content items from search results
    - **keyword**: The search keyword/topic

    Returns detailed analysis of each project and overall trend summary.
    """
    try:
        # Convert dict items to ContentItem objects using helper function
        content_items = []
        for item_data in request.items:
            item = dict_to_content_item(item_data)
            if item:
                content_items.append(item)

        if not content_items:
            raise HTTPException(status_code=400, detail="No valid content items provided")

        # Use TrendAnalyzer to analyze projects
        analyzer = TrendAnalyzer()

        # Analyze each project individually
        analyzed_projects = []
        for item in content_items[:15]:  # Limit to 15 projects for detailed analysis
            project_analysis = await analyzer.analyze_single_project(item, request.keyword)
            if project_analysis:
                analyzed_projects.append(project_analysis)

        # Generate overall trend summary
        trend_summary = await analyzer.generate_trend_summary(
            content_items,
            request.keyword,
            analyzed_projects
        )

        return {
            "keyword": request.keyword,
            "total_projects": len(content_items),
            "analyzed_projects": analyzed_projects,
            "trend_summary": trend_summary,
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/quick-summary", response_model=Dict[str, Any])
async def quick_project_summary(request: ProjectAnalysisRequest):
    """
    Quick summary of projects without detailed AI analysis.
    Uses heuristics and keyword matching for faster results.
    """
    try:
        # Convert dict items to ContentItem objects
        content_items = []
        for item_data in request.items:
            item = dict_to_content_item(item_data)
            if item:
                content_items.append(item)

        if not content_items:
            raise HTTPException(status_code=400, detail="No valid content items provided")

        # Quick analysis without LLM
        analyzer = TrendAnalyzer()
        quick_summary = await analyzer.quick_project_summary(content_items, request.keyword)

        return quick_summary

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Summary failed: {str(e)}")
