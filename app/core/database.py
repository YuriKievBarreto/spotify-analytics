from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text


class Base(DeclarativeBase):
    pass

# para rodar em conteiner:
##DATABASE_URL = "postgresql+asyncpg://yuri:yuri@db_spotify_analytics:5432/db_spotify_analytics"


# para rodar localmente:
DATABASE_URL ="postgresql+asyncpg://yuri:yuri@localhost:5432/db_spotify_analytics"



async_engine = create_async_engine(DATABASE_URL)


async def init_db():
    
    from app.models.usuario import Usuario 
    from app.models.artista import  Artista 
    from app.models.faixa import Faixa 
    from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
    
    try:
         async with async_engine.begin() as conn:
            print("iniciando tentativa de conexao com o banco de dados")
            print("apagando todas as tabelas")
            await conn.run_sync(Base.metadata.drop_all)
            print("criando todas as tabelas")
            await conn.run_sync(Base.metadata.create_all)
            print("conexao bem sucedida")

            print("query de teste:")
            query = text(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
                """
            )

            result = await conn.execute(query)
            table_names = [row[0] for row in result.all()]

            print("Conexao bem sucedida e tabelas verificadas/criadas.")
            print("tabelas encontradas: ", len(table_names))


            
    
    except Exception as e:
        print("erro de conexao: ", e)
        raise e
    






def get_session() -> AsyncSession:

    return AsyncSession(async_engine)





