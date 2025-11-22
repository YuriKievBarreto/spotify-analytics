from app.schemas.schema_artista import ArtistaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.artista import Artista  


async def ler_artista(id_artista:str, db: AsyncSession):
    try:
        db_artista = await db.get(Artista, id_artista)

        if db_artista is None:
            print(f"Artista de id {id_artista} não encontrada")
            return None
        
        print("artista_encontrada encontrado")
        return db_artista
    
    except Exception as e:
        raise e
    


async def criar_artista(db: AsyncSession, artista_data_dict):

    print("iniciandi criacao de faiax==x")


    try:
        db_artista = Artista(**artista_data_dict)
        db.add(db_artista)
        await db.commit()

        return db_artista

    except Exception as e:

        print("erro ao tenta adicionar artista:" , e)


