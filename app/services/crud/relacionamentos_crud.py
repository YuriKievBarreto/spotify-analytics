from app.schemas.schema_faixa import FaixaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
from app.models.faixa import Faixa  
from sqlalchemy import select
from typing import Type


async def salvar_relacionamentos_em_lote(db: AsyncSession,
                                         modelo_orm: Type[Base],
                                         lista_de_dados: list[dict]):
    
    print(f"Iniciando inserção direta em lote na tabela {modelo_orm.__tablename__}...")

    if not lista_de_dados:
        print("Lista de dados vazia. Nenhuma ação realizada.")
        return []
    
    try:
        # 1. Converte a lista de dicionários (input) em objetos ORM
        objetos_a_inserir = [modelo_orm(**dados) for dados in lista_de_dados]
        
        # 2. Adiciona TODOS os objetos de uma vez na sessão (Bulk Insert)
        db.add_all(objetos_a_inserir)
        
        # 3. Confirma a transação no DB
        await db.commit()
        
        print(f"✅ Inseridas {len(objetos_a_inserir)} linhas na tabela {modelo_orm.__tablename__}.")
        return objetos_a_inserir

    except Exception as e:
        await db.rollback() 
        print(f"❌ ERRO FATAL ao inserir em lote na tabela {modelo_orm.__tablename__}:", e)
        raise