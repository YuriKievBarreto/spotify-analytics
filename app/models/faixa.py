from sqlalchemy import String, JSON, Integer
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from typing import List

from app.core.database import Base


class Faixa(Base):
    __tablename__ = "faixa"

    id_faixa: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome_faixa: Mapped[str] = mapped_column(String(255), nullable=False)
    emocoes: Mapped[str] = mapped_column(JSON, nullable= True)
    duracao_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    popularidade: Mapped[int] =  mapped_column(Integer, nullable=False)
    album: Mapped[str] = mapped_column(String(255), nullable= False)
    link_imagem: Mapped[str] = mapped_column(String(255), nullable=False)

    top_usuarios_rel: Mapped[List["UsuarioTopFaixa"]] = relationship(
        back_populates="faixa"
    )