from app.core.database import async_engine
from app.core.spotipy_auth import sp_oauth_manager
import spotipy
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token


async def process_initial_data(user_id: str, refresh_token: str):
    async with AsyncSession(async_engine) as db:

        print("iniciando ingestao de dados no banco")
       
        # Processo de salvamento no banco de dados #
    #   |                                          |   #
    #   |                                          |   #
        # Processo de salvamento no banco de dados #
        

        token_info = await asyncio.to_thread(
        sp_oauth_manager.refresh_access_token, refresh_token
    )
        
        new_access_token = token_info['access_token']
       


        pass