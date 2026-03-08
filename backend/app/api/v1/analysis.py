"""Analysis API endpoints."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel

from ...ai import TrendAnalyzer
from ...models.content import ContentItem

router = APIRouter(prefix="/analyze", tags=["analysis"])

# Store for background task results
analysis_results = {}


class AnalysisRequest(BaseModel):
    keyword: str
    sources: Optional[List[str]] = None
    limit: int = 50
    quick: bool = False


class AnalysisResponse(BaseModel):
    task_id: str
    status: str
    message: str


@router.post("/", response_model=dict)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start a full analysis of a keyword.

    This runs as a background task. Use the returned task_id to check status.
    """
    import uuid

    task_id = str(uuid.uuid4())
    analysis_results[task_id] = {
        "status": "pending",
        "progress": 0,
        "progress_message": "Starting analysis...",
        "result": None,
        "error": None
    }

    # Add to background tasks
    background_tasks.add_task(
        run_analysis,
        task_id,
        request.keyword,
        request.sources,
        request.limit,
        request.quick
    )

    return {
        "task_id": task_id,
        "status": "pending",
        "message": f"Analysis started for '{request.keyword}'",
        "check_status_url": f"/api/v1/analyze/status/{task_id}",
    }


async def run_analysis(
    task_id: str,
    keyword: str,
    sources: Optional[List[str]],
    limit: int,
    quick: bool
):
    """Background task to run analysis."""
    try:
        analyzer = TrendAnalyzer()

        # Update progress
        analysis_results[task_id]["progress"] = 10
        analysis_results[task_id]["progress_message"] = "Collecting data from sources..."

        if quick:
            result = await analyzer.quick_analysis(keyword)
        else:
            result = await analyzer.analyze(keyword, sources, limit)

        analysis_results[task_id] = {
            "status": "completed",
            "progress": 100,
            "progress_message": "Analysis complete!",
            "result": result,
            "error": None,
        }
    except Exception as e:
        analysis_results[task_id] = {
            "status": "failed",
            "progress": 0,
            "progress_message": f"Error: {str(e)}",
            "result": None,
            "error": str(e),
        }


@router.get("/status/{task_id}", response_model=dict)
async def get_analysis_status(task_id: str):
    """
    Get the status of an analysis task.

    Returns the result if completed, or the current status.
    """
    if task_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = analysis_results[task_id]

    response = {
        "task_id": task_id,
        "status": task_data["status"],
        "progress": task_data.get("progress", 0),
        "progress_message": task_data.get("progress_message", ""),
    }

    if task_data["status"] == "completed":
        response["result"] = task_data["result"]
    elif task_data["status"] == "failed":
        response["error"] = task_data["error"]

    return response


@router.post("/quick", response_model=dict)
async def quick_analysis(request: AnalysisRequest):
    """
    Run a quick analysis (synchronous, limited sources).

    This returns immediately with a summary.
    """
    try:
        analyzer = TrendAnalyzer()
        result = await analyzer.quick_analysis(request.keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/sync", response_model=dict)
async def sync_analysis(request: AnalysisRequest):
    """
    Run a synchronous full analysis.

    Warning: This may take 30-60 seconds. Use the async endpoint for better UX.
    """
    try:
        analyzer = TrendAnalyzer()
        result = await analyzer.analyze(request.keyword, request.sources, request.limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.delete("/{task_id}", response_model=dict)
async def delete_analysis(task_id: str):
    """Delete an analysis result."""
    if task_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Task not found")

    del analysis_results[task_id]
    return {"message": "Analysis deleted", "task_id": task_id}