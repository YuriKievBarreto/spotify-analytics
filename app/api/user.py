from fastapi import APIRouter, Request, Depends
from app.core.spotipy_auth import sp_oauth_manager
from starlette.responses import RedirectResponse
from spotipy import Spotify
from app.core.dependencies import get_current_user_id


user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.get("/me")
async def me(
     spotify_user_id: str = Depends(get_current_user_id)
):
   print(spotify_user_id)


