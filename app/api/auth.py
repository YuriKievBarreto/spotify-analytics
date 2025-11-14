from fastapi import APIRouter, Request, Depends, status, HTTPException, Response
from app.core.spotipy_auth import sp_oauth_manager  
from starlette.responses import RedirectResponse
from spotipy import Spotify
from fastapi import BackgroundTasks
from app.services.data_ingestion_service import salvar_dados_iniciais_do_usuario
from app.core.security import create_access_token
from fastapi.responses import JSONResponse


auth_router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@auth_router.get("/login")
async def login_spotify():
    auth_url = sp_oauth_manager.get_authorize_url()
    return RedirectResponse(auth_url)

@auth_router.get("/callback")
async def spotify_callback(request: Request, background_tasks: BackgroundTasks):
    code = request.query_params.get("code")
    if code:
        token_info = sp_oauth_manager.get_access_token(code)
        user_id = await get_user_id(token_info)

        await salvar_dados_iniciais_do_usuario(token_info)
        session_token = create_access_token(subject=user_id)

        response = RedirectResponse("/static/dashboard.html", status_code=status.HTTP_302_FOUND)

        """
        background_tasks.add_task(
        process_initial_data, 
        user_id, 
        refresh_token,
        
        )
        """

       ## response = JSONResponse({"redirect_url": "http://localhost:5500/frontend_teste/dashboard.html"})

    
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # só porque é localhost
            samesite="Lax",
            max_age=43200 * 60,
            path="/"
        )


        return response

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro de autenticação")



async def get_user_id(token_info):
    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')

    sp_autenticado = Spotify(auth=access_token)
    user_info = sp_autenticado.current_user()
    user_id = user_info['id']


    return user_id




