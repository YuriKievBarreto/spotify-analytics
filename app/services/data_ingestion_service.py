from app.core.database import async_engine
from app.core.spotipy_auth import sp_oauth_manager
import spotipy
import asyncio
from spotipy import Spotify
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema_usuario import UsuarioCreate
from datetime import datetime, timedelta, timezone
from app.services.crud_service import criar_usuario


async def refresh_and_get_access_token(db: AsyncSession, user_id: str, refresh_token: str) -> str:
    new_token_info = await asyncio.to_thread(
    sp_oauth_manager.refresh_access_token, refresh_token
    )

    new_access_token = new_token_info['access_token']
   # access_token=new_token_info['access_token']
    new_refresh_token=new_token_info.get('refresh_token', refresh_token)
    expires_in=new_token_info['expires_in']

    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)



    return {
        "new_access_token":new_access_token,
        "new_refresh_token":new_refresh_token,
        "new_expires_at":token_expires_at
    }
     
    

async def busca_informacoes_do_usuario(sp_client: spotipy.Spotify):
    return sp_client.current_user()


async def salvar_dados_iniciais_do_usuario(token_info):
    async with AsyncSession(async_engine) as db:

        access_token = token_info['access_token']
        refresh_token = token_info.get('refresh_token')

        sp_autenticado = Spotify(auth=access_token)
        user_info = sp_autenticado.current_user()

        id_usuario = user_info['id']
        nome_exibicao = user_info["display_name"]
        pais = user_info["country"]
        
        expires_in_seconds = token_info['expires_in']
        

        token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

        user_create_data = UsuarioCreate(
            id_usuario = id_usuario,
            nome_exibicao =  nome_exibicao,
            pais = pais,
            access_token = access_token,
            refresh_token = refresh_token,
            token_expires_at = token_expires_at
        )

       
        user_data_dict = user_create_data.model_dump()
        db_user = await criar_usuario(db, user_data_dict)

        print("ususario criado: ", db_user)

        pass


