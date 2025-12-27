from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class UsuarioSchema(BaseModel):
    id_usuario: str
    nome_exibicao: str
    pais: str

    access_token: str
    refresh_token: str
    token_expires_at: datetime 

    ultima_atualizacao: datetime
    status_processamento: str

    perfil_emocional: str
    

    top_artistas_rel: List["UsuarioTopArtistaSchema"]
    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    id_usuario: str
    nome_exibicao: str
    pais: str
    
  
    access_token: str
    refresh_token: str
    token_expires_at: datetime 

    ultima_atualizacao: datetime
    status_processamento: str

    perfil_emocional: Optional[Any] = None
