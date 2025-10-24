from app.schemas.schema_usuario import UsuarioCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario  
from datetime import datetime

async def criar_usuario(db: AsyncSession , user_data_dict):

    print("iniciandi criacao de usuaroi")
    print("dicionario do usuario: ")
    print(user_data_dict)


    try:
       
        db_user = Usuario(**user_data_dict)
        db.add(db_user)

        await db.commit()

        return db_user

    except Exception as e:

        print("erro ao tenta adicionar usuario:" , e)
        return 



async def atualizar_usuario(db: AsyncSession, user_data: UsuarioCreate):
    return "a"
