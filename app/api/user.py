from fastapi import APIRouter, Request, Depends, status
from app.core.spotipy_auth import sp_oauth_manager
from starlette.responses import  JSONResponse
from app.core.dependencies import get_current_user_id
from app.services.data_ingestion_service import refresh_and_get_access_token
from app.services.crud_service import atualizar_credenciais_usuario, ler_usuario
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from datetime import datetime, timezone


SESSION_TOKEN_COOKIE_NAME = "session_token"

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.get("/me")
async def me(
     spotify_user_id: str = Depends(get_current_user_id),
     db: AsyncSession = Depends(get_session)
):  
    await valida_credenciais(spotify_user_id, db)
    
    

    return {"message": "logado",
            "detail": "Sessão JWT validada e ativa."}


@user_router.post("/logout")
async def logout(): 
    response = JSONResponse(content={"message": "Logout bem sucedido"})

    response.set_cookie(
        key="session_token",
        httponly=True,
        secure=False,  # só porque é localhost
        samesite="Lax",
        max_age=43200 * 60,
        path="/"
    )

    return response





async def valida_credenciais(spotify_user_id: str, db: AsyncSession):
    usuario = await ler_usuario(user_id=spotify_user_id, db=db)
    current_time = datetime.now(timezone.utc)

    if current_time >= usuario.token_expires_at:
        print("token do usuario expirado, atualizando credenciais")

        credenciais = await refresh_and_get_access_token(db=db, user_id=usuario.id_usuario, refresh_token=usuario.refresh_token)
        
        await atualizar_credenciais_usuario(db, usuario.id_usuario,
                                        credenciais["new_access_token"],
                                        credenciais["new_refresh_token"],
                                        credenciais["new_expires_at"])

    print("token não expirado")
