from pydantic import BaseModel
from typing import List


class ArtistaSchema(BaseModel):
    id_artista: str
    nome_artista: str
    popularidade: int
    
    
    generos_rel: List["GeneroArtistaSchema"]

    class Config:
        from_attributes = True