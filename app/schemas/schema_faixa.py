from pydantic import BaseModel
from typing import List

class FaixaSchema(BaseModel):
    id_faixa: str
    nome_faixa: str


    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


