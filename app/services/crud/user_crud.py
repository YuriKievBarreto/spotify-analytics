from app.schemas.schema_usuario import UsuarioCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario  
from datetime import datetime
from app.core.database import async_engine

async def criar_usuario(db: AsyncSession, user_data_dict):

    print("iniciandi criacao de usuaroi")


    try:
        db_user = Usuario(**user_data_dict)
        db.add(db_user)
        await db.commit()

        return db_user

    except Exception as e:

        print("erro ao tenta adicionar usuario:" , e)



async def atualizar_credenciais_usuario(db: AsyncSession, 
                                        user_id: str,
                                        new_access_token: str,
                                        new_refresh_token: str,
                                        new_expires_at: datetime):
    

    print("iniciando atualização de credenciais do usuario")
    try:
        db_user = await db.get(Usuario, user_id)

        if db_user is None:
            print("Usuario de id {user_id} não encontrado para atualização de credenciais")
            return None
        
        db_user.access_token = new_access_token
        db_user.refresh_token = new_refresh_token
        db_user.token_expires_at = new_expires_at

        db.add(db_user)

        await db.commit()

        print("credenciais do usuario atualizadas com sucesso")

        return db_user

    except Exception as e:
        print("erro ao atualizar credenciais do usuario: ", e)
        raise e
    

async def ler_usuario(user_id:str):
   async with AsyncSession(async_engine) as db:
        try:
            db_user = await db.get(Usuario, user_id)

            if db_user is None:
                print("Usuario de id {user_id} não encontrado")
                return None
            
            print("usuario encontrado")
            return db_user
    
        except Exception as e:
            raise e 


