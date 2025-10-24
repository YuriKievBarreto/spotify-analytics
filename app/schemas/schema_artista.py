from pydantic import BaseModel, Field
from typing import List


class ArtistaSchema(BaseModel):
    id_artista: str
    nome_artista: str
    popularidade: int
    
    
    generos_rel: List["GeneroArtistaSchema"]

    class Config:
        from_attributes = True


class ArtistaCreate(BaseModel):
    id_artista: str = Field(..., alias='id') 
    nome_artista: str = Field(..., alias='name') 
    
    popularidade: int

    class Config:
        populate_by_name = True 
        extra = 'ignore'
