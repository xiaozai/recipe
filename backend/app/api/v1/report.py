"""Report generation API endpoints."""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse

from ...ai import TrendAnalyzer
from ...models.report import Report, ReportFormat
from ...services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["reports"])

report_service = ReportService()


@router.post("/generate/{keyword}", response_model=dict)
async def generate_report(
    keyword: str,
    format: ReportFormat = Query(ReportFormat.MARKDOWN, description="Output format"),
    include_items: bool = Query(False, description="Include collected items in report"),
):
    """
    Generate a comprehensive report for a keyword.

    - **keyword**: Technology/term to analyze
    - **format**: Output format (markdown, json, html)
    - **include_items**: Include raw collected items in the report
    """
    try:
        analyzer = TrendAnalyzer()

        # Run analysis
        analysis_result = await analyzer.analyze(keyword)

        # Generate report
        report = await report_service.generate_report(
            keyword=keyword,
            analysis_result=analysis_result,
            format=format,
            include_items=include_items,
        )

        return {
            "keyword": keyword,
            "format": format.value,
            "report": report.to_markdown() if format == ReportFormat.MARKDOWN else report.to_dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/download/{keyword}", response_class=PlainTextResponse)
async def download_report(
    keyword: str,
    format: str = Query("markdown", regex="^(markdown|md|txt)$"),
):
    """
    Download a report as a file.

    Returns plain text markdown suitable for download.
    """
    try:
        analyzer = TrendAnalyzer()

        # Run analysis
        analysis_result = await analyzer.analyze(keyword)

        # Generate report
        report = await report_service.generate_report(
            keyword=keyword,
            analysis_result=analysis_result,
            format=ReportFormat.MARKDOWN,
            include_items=False,
        )

        return report.to_markdown()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.post("/from-analysis/{task_id}", response_model=dict)
async def report_from_analysis(
    task_id: str,
    format: ReportFormat = Query(ReportFormat.MARKDOWN),
):
    """
    Generate a report from a previously completed analysis.

    Use this when you already have an analysis task completed.
    """
    from .analysis import analysis_results

    if task_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis task not found")

    task_data = analysis_results[task_id]

    if task_data["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis not completed. Current status: {task_data['status']}",
        )

    try:
        report = await report_service.generate_report(
            keyword=task_data["result"]["keyword"],
            analysis_result=task_data["result"],
            format=format,
            include_items=False,
        )

        return {
            "keyword": task_data["result"]["keyword"],
            "format": format.value,
            "report": report.to_markdown() if format == ReportFormat.MARKDOWN else report.to_dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")