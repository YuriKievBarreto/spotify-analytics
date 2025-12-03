from app.schemas.schema_faixa import FaixaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_engine
from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
from app.models.faixa import Faixa  
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Type, List, Dict

async def ler_usuario_top_faixas(id_usuario: str):
   async with AsyncSession(async_engine) as db:
      print("iniciando busca de relacionamentos")
      stmt = select(UsuarioTopFaixa).where(
         UsuarioTopFaixa.id_usuario == id_usuario
      ).options(
         joinedload(UsuarioTopFaixa.faixa) 
      ).order_by(
        UsuarioTopFaixa.short_time_rank.asc()
    )
      
   result =  await db.execute(stmt)
   return result.scalars().all()




