from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class UsuarioSchema(BaseModel):
    id_usuario: str
    nome_exibicao: str
    pais: str

    top_artistas_rel: List["UsuarioTopArtistaSchema"]
    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
   class UsuarioCreate(BaseModel):
   
    id_usuario: str
    nome_exibicao: str
    pais: str
    
  
    access_token: str
    refresh_token: str
    token_expires_at: datetime 
