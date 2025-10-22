from pydantic import BaseModel
from typing import List

class UsuarioSchema(BaseModel):
    id_usuario: str
    nome_exibicao: str
    pais: str

    top_artistas_rel: List["UsuarioTopArtistaSchema"]
    top_faixas_rel: List["UsuarioTopFaixaSchema"]

    class Config:
        from_attributes = True


