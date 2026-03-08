"""API v1 package initialization."""
from fastapi import APIRouter

from .search import router as search_router
from .analysis import router as analysis_router
from .report import router as report_router
from .projects import router as projects_router
from .settings import router as settings_router

router = APIRouter(prefix="/v1")

router.include_router(search_router)
router.include_router(analysis_router)
router.include_router(report_router)
router.include_router(projects_router)
router.include_router(settings_router)

__all__ = ["router"]