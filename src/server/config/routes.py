from fastapi import APIRouter

from server.apps.auth.routes import router as auth_router
from .broker import broker_router

# FastAPI Routes
router = APIRouter(prefix="/api")

# Broker Routes
router.include_router(broker_router)
router.include_router(auth_router, prefix="/auth", tags=["auth"])
