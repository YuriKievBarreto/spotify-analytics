from fastapi import APIRouter
from .auth import auth_router
from .dashboard import dashboard_router


mainRouter = APIRouter(
    prefix="/api/v1",
    tags=["API geral"]
)

mainRouter.include_router(auth_router)
mainRouter.include_router(dashboard_router)
