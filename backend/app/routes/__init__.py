"""Routes package – collects all API routers."""

from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.dashboard import router as dashboard_router
from app.routes.transactions import router as transactions_router
from app.routes.invoices import router as invoices_router
from app.routes.assistant import router as assistant_router
from app.routes.reports import router as reports_router
from app.routes.knowledge import router as knowledge_router
from app.routes.settings import router as settings_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(dashboard_router)
api_router.include_router(transactions_router)
api_router.include_router(invoices_router)
api_router.include_router(assistant_router)
api_router.include_router(reports_router)
api_router.include_router(knowledge_router)
api_router.include_router(settings_router)
