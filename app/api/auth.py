from fastapi import APIRouter, Request, Depends, status, HTTPException
from app.core.spotipy_auth import sp_oauth_manager  
from starlette.responses import RedirectResponse
from spotipy import Spotify
from fastapi import BackgroundTasks
from app.services.data_ingestion_service import salvar_dados_iniciais_do_usuario, salvar_top_faixas
from app.core.security import create_access_token   
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.crud_service import ler_usuario
from app.core.database import get_session
from app.api.user import valida_credenciais


auth_router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@auth_router.get("/login")
async def login_spotify():
    auth_url = sp_oauth_manager.get_authorize_url()
    return RedirectResponse(auth_url)

@auth_router.get("/callback")
async def spotify_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_session)
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Código de autorização ausente")

   
    token_info = sp_oauth_manager.get_access_token(code)
    user_id = await get_user_id(token_info)

  
    usuario_bd = await ler_usuario(user_id=user_id, db=db)

    if usuario_bd is None:
        print("Usuário novo — criando dados iniciais...")
        
        await salvar_dados_iniciais_do_usuario(token_info)

        session_token = create_access_token(subject=user_id)

        # salva top faixas de forma assíncrona
        background_tasks.add_task(
            salvar_top_faixas,
            user_id,
            code
        )

    
    else:
        print("Usuário já existe — gerando novo JWT")
        session_token = create_access_token(subject=usuario_bd.id_usuario)

        print("Validando credenciais do usuário...")
        await valida_credenciais(usuario_bd.id_usuario, db)

  
    response = RedirectResponse(
        "http://127.0.0.1:8000/static/dashboard.html",
        status_code=status.HTTP_302_FOUND
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,  # Localhost
        samesite="Lax",
        max_age=43200 * 60,
        path="/"
    )

    return response




async def get_user_id(token_info):
    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')

    sp_autenticado = Spotify(auth=access_token)
    user_info = sp_autenticado.current_user()
    user_id = user_info['id']


    return user_id




