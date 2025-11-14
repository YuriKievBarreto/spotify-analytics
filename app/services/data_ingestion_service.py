from app.core.database import async_engine
from app.core.spotipy_auth import sp_oauth_manager
import spotipy
import asyncio
from spotipy import Spotify
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema_usuario import UsuarioCreate
from app.schemas.schema_relacionamentos_entrada import UsuarioTopFaixaCreate
from datetime import datetime, timedelta, timezone
from app.services.crud_service import criar_usuario
from app.services.spotipy_service import get_current_user_details


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

        user_dict = await get_current_user_details(token_info)


        user_create_data = UsuarioCreate(
            id_usuario = user_dict["id_usuario"],
            nome_exibicao =  user_dict["nome_exibicao"],
            pais = user_dict["pais"],
            access_token = user_dict["access_token"],
            refresh_token = user_dict["refresh_token"],
            token_expires_at = user_dict["token_expires_at"]
        )

       
        user_data_dict = user_create_data.model_dump()
        db_user = await criar_usuario(db, user_data_dict)

        

        pass

async def salvar_top_faixas(user_id:str, code:str):

    async with AsyncSession(async_engine) as db:
        """
        top_faixa_data = UsuarioTopFaixaCreate(
            id_usuario=user_id
        )
        """
        

        print("inserindo faixas no bd")
        
       

        



