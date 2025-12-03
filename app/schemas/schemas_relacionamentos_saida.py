from pydantic import BaseModel
from typing import List

class UsuarioTopArtistaSchema(BaseModel):
    id_artista: str
    time_range: str
    rank: int

    class Config:
        from_attributes: True


class UsuarioTopFaixaSchema(BaseModel):
    short_time_rank: str
    medium_time_rank: str
    long_time_rank: str

    class Config:
        from_attributes: True


"""
class GeneroArtistaSchema(BaseModel):
    nome_genero: str

    class Config:
        from_attributes: True
"""