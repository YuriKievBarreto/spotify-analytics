from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class FaixaSchema(BaseModel):
    id_faixa: str
    nome_faixa: str
    emocoes: Optional[Dict[str, float]] = None
    duracao_ms: int
    popularidade: int
    album: str


    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


class FaixaCreate(BaseModel):
    
    id_faixa: str = Field(..., alias='id') 
    nome_faixa: str = Field(..., alias='name')
    emocoes: Optional[Dict[str, float]] = None
    album: str = Field(..., alias='album') 
    popularidade: int 
    duracao_ms: int 
    

    class Config:
        populate_by_name = True 
        extra = 'ignore'