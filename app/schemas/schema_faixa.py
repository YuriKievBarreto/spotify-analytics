from pydantic import BaseModel, Field
from typing import List

class FaixaSchema(BaseModel):
    id_faixa: str
    nome_faixa: str


    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


class FaixaCreate(BaseModel):
    
    id_faixa: str = Field(..., alias='id') 
    
    nome_faixa: str = Field(..., alias='name')
    

    class Config:
        populate_by_name = True 
        extra = 'ignore'