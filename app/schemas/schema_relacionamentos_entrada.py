from pydantic import BaseModel
from typing import List, Optional


class UsuarioTopArtistaCreate(BaseModel):
   
    id_usuario: str 
    id_artista: str  
    
    time_range: str
    rank: int




class UsuarioTopFaixaCreate(BaseModel):
   
    id_usuario: str  
    id_faixa: str   
    short_time_rank: int
    medium_time_rank: int
    long_time_rank: int
    

class GeneroArtistaCreate(BaseModel):
   
    id_artista: str
    nome_genero: str
    
   