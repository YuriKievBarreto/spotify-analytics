from sqlalchemy import  String  , DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[str] = mapped_column(String(50), primary_key=True)
    nome_exibicao: Mapped[str] = mapped_column(String(50), nullable=False)
    pais: Mapped[str] = mapped_column(String(50), nullable=False)

    access_token: Mapped[str] = mapped_column(String(512), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(1024))
    token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ultima_atualizacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status_processamento: Mapped[str] = mapped_column(String(512), nullable=True)

    top_artistas_rel: Mapped[List["UsuarioTopArtista"]] = relationship(
        back_populates="usuario"
    )

    top_faixas_rel: Mapped[List["UsuarioTopFaixa"]] = relationship(
        back_populates="usuario"
    )