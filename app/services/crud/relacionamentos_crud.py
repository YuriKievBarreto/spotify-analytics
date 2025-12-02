from app.schemas.schema_faixa import FaixaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
from app.models.faixa import Faixa  
from sqlalchemy import select
from typing import Type, List, Dict




async def salvar_UsuarioTopFaixa_em_lote(
    db: AsyncSession, 
    lista_de_relacoes: List[Dict]
):
    
    if not lista_de_relacoes:
        return []

    try:
        # 1. Converte a lista de dicionários em objetos ORM
        objetos_a_inserir = [UsuarioTopFaixa(**dados) for dados in lista_de_relacoes]
        
        # 2. Inserção em massa: Adiciona todos de uma vez
        db.add_all(objetos_a_inserir)
        
        # 3. Confirma a transação
        await db.commit()
        
        print(f"✅ Inseridas {len(objetos_a_inserir)} novas relações UsuarioTopFaixa.")
        return objetos_a_inserir

    except Exception as e:
        # Em caso de erro (ex: duplicata de PK), o rollback desfaz tudo
        await db.rollback() 
        print("❌ ERRO ao inserir relações em lote:", e)
        raise