from app.schemas.schema_usuario import UsuarioCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario  
from datetime import datetime
from app.core.database import async_engine
from app.services.crud.relacionamentos_crud import ler_usuario_top_faixas, ler_usuario_top_artistas
from app.utils.general import contar_elementos

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
        


async def get_basic_data(spotify_user_id: str, user_db):
    print("usuario encontrado, tentando puxar dados direto do banco de dados")
    try:
        nome_exibicao = user_db.nome_exibicao

        response_top_faixa = await ler_usuario_top_faixas(spotify_user_id, quantidade=1)
        top_faixa = response_top_faixa[0].faixa

        top_artista = await ler_usuario_top_artistas(spotify_user_id, quantidade=1)

        response_top_artistas = await ler_usuario_top_artistas(spotify_user_id, quantidade=20)
        top_generos = [gen for art in response_top_artistas for gen in art.artista.generos]
        top_generos = await contar_elementos(top_generos)


        return {
        "nome_exibicao": nome_exibicao,
        "top_faixa": top_faixa,
        "top_artista": top_artista[0].artista,
        "top_generos": top_generos
    }
    
    except Exception as e:
        print(e)
        raise e
      

async def atualizar_status(spotify_user_id: str, status: str):
    async with AsyncSession(async_engine) as db:
        print(f"atualizando status do usuario para : {status}")

    consulta = select(Usuario).where(Usuario.id_usuario == spotify_user_id)
    resultado = await db.execute(consulta)
    
    
    usuario_db = resultado.scalar_one_or_none() 

    if usuario_db:
        usuario_db.status_processamento = status
        db.add(usuario_db)
        await db.commit()
        
        return usuario_db
    else:
        print(f"Usuário {spotify_user_id} não encontrado.")
        return None

