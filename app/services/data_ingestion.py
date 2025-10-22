from app.core.database import async_engine
from app.core.spotipy_auth import sp_oauth_manager
import spotipy
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession


async def process_initial_data(user_id: str, refresh_token: str):
    async with AsyncSession(async_engine) as db: 
       
        pass