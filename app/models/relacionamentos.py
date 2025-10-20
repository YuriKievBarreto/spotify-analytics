from sqlalchemy import  Integer, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship


from app.core.database import Base


class UsuarioTopArtista(Base):
    __tablename__ = "usuario_top_artista"

    id_usuario: Mapped[str] = mapped_column(ForeignKey("usuario.id_usuario"), primary_key=True)
    id_artista: Mapped[str] = mapped_column(ForeignKey("artista.id_artista"))
    time_range: Mapped[str] = mapped_column(String(10), primary_key=True)

    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="top_artistas_rel")
    artista: Mapped["Artista"] = relationship(back_populates="top_usuarios_rel")


class UsuarioTopFaixa(Base):
    __tablename__ = "usuario_top_faixa"

    id_usuario: Mapped[str] = mapped_column(ForeignKey('usuario.id_usuario'), primary_key=True)
    id_faixa: Mapped[str] = mapped_column(ForeignKey('faixa.id_faixa'), primary_key=True)
    time_range: Mapped[str] = mapped_column(String(10), primary_key=True)

    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="top_faixas_rel")
    faixa: Mapped["Faixa"] = relationship(back_populates="top_usuarios_rel")


class GeneroArtista(Base):
    __tablename__ = "genero_artista"

    id_artista: Mapped[str] = mapped_column(ForeignKey("artista.id_artista"))
    nome_genero: Mapped[str] = mapped_column(String(100), primary_key=True)

    artista: Mapped["Artista"] = relationship(back_populates="generos_rel")

