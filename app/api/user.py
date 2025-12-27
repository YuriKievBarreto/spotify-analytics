from fastapi import APIRouter, Request, Depends
from starlette.responses import  JSONResponse
from app.core.dependencies import get_current_user_id
from app.services.data_ingestion_service import refresh_and_get_access_token
from app.services.crud.user_crud import atualizar_credenciais_usuario, ler_usuario
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from datetime import datetime, timezone
from app.services.crud.user_crud import ler_usuario
from app.services.spotipy_service import get_top_faixas, get_top_artistas, get_user_top_genres
from app.services.crud.relacionamentos_crud import ler_usuario_top_faixas, ler_usuario_top_artistas
from app.services.emotion_extraction_service import get_media_emocoes, get_perfil_emocional, get_analise_musica
from app.services.crud.user_crud import ler_usuario, get_basic_data, atualizar_perfil_emocional
from app.services.crud.relacionamentos_crud import ler_usuario_top_faixas, ler_usuario_top_artistas

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
    
    
    user_db = await ler_usuario(spotify_user_id)

    if user_db.status_processamento == "PROCESSANDO":
        print("puxando basic data da api do spotify")
        usuario = await ler_usuario(spotify_user_id)
        nome_exibicao = usuario.nome_exibicao
        top_faixa = await get_top_faixas(usuario.access_token, quantitade=1)
        top_artista = await get_top_artistas(usuario.access_token, quantitade=1)
        top_generos = await get_user_top_genres(usuario.access_token, quantidade=50)

        top_artista = list(top_artista.values())[0]
        top_faixa = list(top_faixa.values())[0]



        return {
            "nome_exibicao": nome_exibicao,
            "top_faixa": top_faixa,
            "top_artista": top_artista,
            "top_generos": top_generos

        }
       

        
    else:
        response_dict = await get_basic_data(spotify_user_id, user_db)
        return response_dict
        
    
    



async def valida_credenciais(spotify_user_id: str, db: AsyncSession):
    usuario = await ler_usuario(user_id=spotify_user_id)
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

    relacoinamentos = await ler_usuario_top_faixas(user_id)
    

    lista_emocoes = [rel.faixa.emocoes for rel in relacoinamentos]
    lista_faixas = np.array([rel.faixa.duracao_ms for rel in relacoinamentos])
    popularidade_media =  np.array([rel.faixa.popularidade for rel in relacoinamentos])
    pop_media = int(np.round(popularidade_media.mean(), 0))
    

 

    df_emocoes = pd.DataFrame(lista_emocoes)
    df_emocoes.describe()
    df_emocoes.info()
    matriz_emocoes = df_emocoes.values
    resultado_np = np.mean(matriz_emocoes, axis=0)
    resultado_np = np.round(resultado_np, 2)
   



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

@user_router.get("/top-artistas")
async def user_top_artistas( user_id: str = Depends(get_current_user_id)):

    relacoinamentos = await ler_usuario_top_artistas(user_id)
    print("rodando top artistas")

    
    dict_resposta =  [converter_artista_e_relacionamento_para_dict(rel) for rel in relacoinamentos]
    
    return dict_resposta



def converter_artista_e_relacionamento_para_dict(rel):
    return {
        "nome_artista": rel.artista.nome_artista,
        "link_imagem": rel.artista.link_imagem,
        "short_rank": rel.short_time_rank,
        "medium_rank": rel.medium_time_rank,
        "long_rank": rel.long_time_rank,
        "popularidade_artista": rel.artista.popularidade_artista,
        "generos": rel.artista.generos
    }


@user_router.get("/perfil-musical")
async def get_perfil_musical( user_id: str = Depends(get_current_user_id)):

    usuario_banco = await ler_usuario(user_id)
    if usuario_banco.perfil_emocional:
        print(type(usuario_banco.perfil_emocional))
        print(usuario_banco.perfil_emocional)
        return usuario_banco.perfil_emocional


    else:
        usuario_top_faixas = await ler_usuario_top_faixas(user_id)
        lista_emocoes = [rel.faixa.emocoes for rel in usuario_top_faixas]
        lista_faixas = [rel.faixa for rel in usuario_top_faixas]


        dict_media_emocoes = await get_media_emocoes(lista_emocoes)
        copia_media_emocoes = dict_media_emocoes.copy()


        texto_perfil_emocional = await get_perfil_emocional(dict_media_emocoes)

        media_top1_chave_max = max(copia_media_emocoes, key=copia_media_emocoes.get)
        media_top1_valor_max = copia_media_emocoes[media_top1_chave_max]

        del copia_media_emocoes[media_top1_chave_max]

        top2chave_max = max(copia_media_emocoes, key=copia_media_emocoes.get)
        top2_valor_max = copia_media_emocoes[top2chave_max]


        faixa_top1 = max(lista_faixas, key=lambda faixa: faixa.emocoes[media_top1_chave_max])
        valor_top1 = faixa_top1.emocoes[media_top1_chave_max]



        analise_top1 = await get_analise_musica(LETRA=faixa_top1.letra_faixa, EMOCAO=media_top1_chave_max)
        dict_analise_faixa_top1 = json.loads(analise_top1)



        dict_faixa_top1 = to_dict(faixa_top1)
        del dict_faixa_top1["emocoes"]
        dict_faixa_top1["emocao_mais_alta"] = valor_top1
        dict_faixa_top1["analise"] = dict_analise_faixa_top1

        faixa_top2 = max(lista_faixas, key=lambda faixa: faixa.emocoes[top2chave_max])
        valor_top2 = faixa_top2.emocoes[top2chave_max]

    


        analise_top2 = await get_analise_musica(LETRA=faixa_top2.letra_faixa, EMOCAO=top2chave_max)
        dict_analise_faixa_top2 = json.loads(analise_top2)
        dict_faixa_top2 = to_dict(faixa_top2)
        del dict_faixa_top2["emocoes"]
        dict_faixa_top2["emocao_mais_alta"] = valor_top2
        dict_faixa_top2["analise"] = dict_analise_faixa_top2

    

        dict_resposta = {
        "top1_sentimento": {
            "nome": media_top1_chave_max,
            "intensidade": media_top1_valor_max,
            "faixa": dict_faixa_top1
        },
        "top2_sentimento": {
            "nome": top2chave_max,
            "intensidade": top2_valor_max,
            "faixa": dict_faixa_top2
        },
        "texto_perfil_emocional": texto_perfil_emocional
        }


        print("atualizando perifl emocional no banco de dados")
        await atualizar_perfil_emocional(user_id, dict_resposta)


        return dict_resposta

    


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}