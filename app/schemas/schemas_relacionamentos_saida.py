from pydantic import BaseModel
from typing import List

class UsuarioTopArtistaSchema(BaseModel):
    id_artista: str
    time_range: str
    rank: int

    class Config:
        from_attributes: True


class UsuarioTopFaixaSchema(BaseModel):
    time_range: str
    rank: int

    class Config:
        from_attributes: True


class GeneroArtistaSchema(BaseModel):
    nome_genero: str

    class Config:
        from_attributes: True
