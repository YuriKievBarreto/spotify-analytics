from fastapi import APIRouter, Request, Depends, status
from starlette.responses import  JSONResponse
from app.core.dependencies import get_current_user_id
from app.services.data_ingestion_service import refresh_and_get_access_token
from app.services.crud.user_crud import atualizar_credenciais_usuario, ler_usuario
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from datetime import datetime, timezone
from app.services.crud.user_crud import ler_usuario
from app.services.spotipy_service import get_top_faixas, get_top_artistas, get_user_top_genres
from app.services.crud.faixa_crud import ler_faixa
from app.services.crud.relacionamentos_crud import ler_usuario_top_faixas
import numpy as np
import json
import pandas as pd

SESSION_TOKEN_COOKIE_NAME = "session_token"

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.get("/me")
async def me(
     spotify_user_id: str = Depends(get_current_user_id),
     db: AsyncSession = Depends(get_session)
):  
    await valida_credenciais(spotify_user_id, db)

    return {"message": "logado",
            "detail": "Sessão JWT validada e ativa."}


@user_router.post("/logout")
async def logout(): 
    response = JSONResponse(content={"message": "Logout bem sucedido"})

    response.set_cookie(
        key="session_token",
        httponly=True,
        secure=False,  # só porque é localhost
        samesite="Lax",
        max_age=43200 * 60,
        path="/"
    )

    return response

@user_router.get("/current_session_user_id")
async def get_user_id(
    spotify_user_id: str = Depends(get_current_user_id),
     db: AsyncSession = Depends(get_session)):
    
    return spotify_user_id


@user_router.get("/get_user_basic_data")
async def get_user_basic_data(spotify_user_id: str = Depends(get_current_user_id),
     db: AsyncSession = Depends(get_session)):

    usuario = await ler_usuario(spotify_user_id, db)
    nome_exibicao = usuario.nome_exibicao
    top_faixas = await get_top_faixas(usuario.access_token, quantitade=1)
    top_artistas = await get_top_artistas(usuario.access_token, quantitade=1)
    top_generos = await get_user_top_genres(usuario.access_token, quantidade=50)

    return {
        "nome_exibicao": nome_exibicao,
        "top_faixas": top_faixas,
        "top_artistas": top_artistas,
        "top_generos": top_generos
    }




async def valida_credenciais(spotify_user_id: str, db: AsyncSession):
    usuario = await ler_usuario(user_id=spotify_user_id, db=db)
    current_time = datetime.now(timezone.utc)

    if current_time >= usuario.token_expires_at:
        print("token do usuario expirado, atualizando credenciais")

        credenciais = await refresh_and_get_access_token(db=db, user_id=usuario.id_usuario, refresh_token=usuario.refresh_token)
        
        await atualizar_credenciais_usuario(db, usuario.id_usuario,
                                        credenciais["new_access_token"],
                                        credenciais["new_refresh_token"],
                                        credenciais["new_expires_at"])

    print("token não expirado")



@user_router.get("/top-musicas")
async def user_top_musicas( user_id: str = Depends(get_current_user_id)):

    """
    o que preciso retornar em top_musicas:

    nome_musica ok
    album_musica ok
    short_time_rank
    medium_time_rank
    long_time_rank
    popularidade_musica 
    sentimento predominante ok
    pontuacao_sentimento_predominante(0 a 1)
    duracao_ms ok
    duracao+media ok

    """
    relacoinamentos = await ler_usuario_top_faixas(user_id)
    

    lista_emocoes = [rel.faixa.emocoes for rel in relacoinamentos]
    lista_faixas = np.array([rel.faixa.duracao_ms for rel in relacoinamentos])
    media_duracao_ms =  int(np.round(lista_faixas.mean(), 0))
    popularidade_media =  np.array([rel.faixa.popularidade for rel in relacoinamentos])
    pop_media = int(np.round(popularidade_media.mean(), 0))
    

 

    df_emocoes = pd.DataFrame(lista_emocoes)
    df_emocoes.describe()
    df_emocoes.info()
    matriz_emocoes = df_emocoes.values
    resultado_np = np.mean(matriz_emocoes, axis=0)
    resultado_np = np.round(resultado_np, 2)
   

    resultado_python_list = resultado_np.tolist()
    resultado_agregado = dict(zip(df_emocoes.columns, resultado_python_list))    


    dict_resposta = {
    "sentimento_predominante": str(df_emocoes.columns[resultado_np.argmax()]),
    "pontuacao_sentimento_predominante": float(resultado_np.max()),
    "duracao_media_ms": int(np.round(lista_faixas.mean(), 0)),
    "faixas": [converter_faixa_e_relacionamento_para_dict(rel) for rel in relacoinamentos],
    "popularidade_media": float(pop_media)
}
                    
    
   

    return dict_resposta




def converter_faixa_e_relacionamento_para_dict(rel):
    return {
        "nome_faixa": rel.faixa.nome_faixa,
        "album": rel.faixa.album,
        "link_imagem": rel.faixa.link_imagem,
        "emocoes": rel.faixa.emocoes,
        "duracao_ms": rel.faixa.duracao_ms,
        "short_rank": rel.short_time_rank,
        "medium_rank": rel.medium_time_rank,
        "long_rank": rel.long_time_rank,
        "popularidade": rel.faixa.popularidade,
        "artista_principal": rel.faixa.artista_principal
    }



