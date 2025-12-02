from app.schemas.schema_faixa import FaixaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.relacionamentos import UsuarioTopArtista, UsuarioTopFaixa, GeneroArtista
from app.models.faixa import Faixa  
from sqlalchemy import select
from typing import Type, List, Dict




