from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass



DATABASE_URL = "postgresql+asyncpg://yuri:yuri@localhost:5432/db_spotify_analytics"

async_engine = create_async_engine(DATABASE_URL)


async def init_db():
    
    from app.models.usuario import Usuario 
    from app.models.artista import  Artista 
    from app.models.faixa import Faixa 
    from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



def get_session() -> AsyncSession:

    return AsyncSession(async_engine)





