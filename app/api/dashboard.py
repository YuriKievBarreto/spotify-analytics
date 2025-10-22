from fastapi import APIRouter, Request, Depends
from app.core.spotipy_auth import sp_oauth_manager
from starlette.responses import RedirectResponse
from spotipy import Spotify

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@dashboard_router.get("/?user_id")
async def dashboard(request: Request):
    user_id = request.query_params.get("user_id")
    return {"id do usuario: ", }