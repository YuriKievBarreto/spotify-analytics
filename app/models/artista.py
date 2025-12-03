from sqlalchemy import  Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.core.database import Base

class Artista(Base):
    __tablename__ = "artista" 
    id_artista: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome_artista: Mapped[str] = mapped_column(String(50), nullable=False)
    popularidade_artista: Mapped[int] = mapped_column(Integer, nullable=False)
    link_imagem: Mapped[str] = mapped_column(String(250), nullable=False)
    generos: Mapped[List[str]] = mapped_column(postgresql.ARRAY(String))

    top_usuarios_rel: Mapped[List["UsuarioTopArtista"]] = relationship(
        back_populates="artista"
    )

    """
    generos_rel: Mapped[List["GeneroArtista"]] = relationship(
        back_populates="artista"
    )"""