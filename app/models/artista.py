from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from core.database import Base

class Artista(Base):
    __tablename__ = "artista" 
    id_artista: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome_artista: Mapped[str] = mapped_column(String(50), nullable=True)
    popularidade: Mapped[int] = mapped_column(Integer, nullable=True)

    top_usuarios_rel: Mapped[List["UsuarioTopArtista"]] = relationship(
        back_populates="artista"
    )

    top_usuarios_rel: Mapped[List["UsuarioTopArtista"]] = relationship(
        back_populates="artista"
    )