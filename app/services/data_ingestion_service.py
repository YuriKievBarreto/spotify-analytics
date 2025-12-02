from app.core.database import async_engine
from app.core.spotipy_auth import sp_oauth_manager
import spotipy
import asyncio
from spotipy import Spotify
from app.services.spotipy_service import get_top_faixas
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema_usuario import UsuarioCreate
from app.models.relacionamentos import UsuarioTopFaixa
from datetime import datetime, timedelta, timezone
from app.services.crud.user_crud import criar_usuario
from app.services.crud.faixa_crud import salvar_faixas_em_batch
from app.services.crud.relacionamentos_crud import salvar_UsuarioTopFaixa_em_lote
from app.services.spotipy_service import get_current_user_details
from app.services.extracao_de_letras import buscar_letras_em_batch
from app.services.emotion_extraction_service import extrair_emocoes_em_batch



async def refresh_and_get_access_token(db: AsyncSession, user_id: str, refresh_token: str) -> str:
    new_token_info = await asyncio.to_thread(
    sp_oauth_manager.refresh_access_token, refresh_token
    )

    new_access_token = new_token_info['access_token']
   # access_token=new_token_info['access_token']
    new_refresh_token=new_token_info.get('refresh_token', refresh_token)
    expires_in=new_token_info['expires_in']

    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)



    return {
        "new_access_token":new_access_token,
        "new_refresh_token":new_refresh_token,
        "new_expires_at":token_expires_at
    }
     
    

async def busca_informacoes_do_usuario(sp_client: spotipy.Spotify):
    return sp_client.current_user()


async def salvar_dados_iniciais_do_usuario(token_info):
    async with AsyncSession(async_engine) as db:

        user_dict = await get_current_user_details(token_info)


        user_create_data = UsuarioCreate(
            id_usuario = user_dict["id_usuario"],
            nome_exibicao =  user_dict["nome_exibicao"],
            pais = user_dict["pais"],
            access_token = user_dict["access_token"],
            refresh_token = user_dict["refresh_token"],
            token_expires_at = user_dict["token_expires_at"]
        )

       
        user_data_dict = user_create_data.model_dump()
        db_user = await criar_usuario(db, user_data_dict)

        

        pass

async def salvar_top_faixas(user_id:str, access_token:str):
    print("iniciando salvamento de top faixas do usuario no bancon de dados")

    async with AsyncSession(async_engine) as db:
        ## 1. Obter as 25 top faixas do usuario
        print("puxando top 25 faixas do short term")
        top_faixas = await get_top_faixas(access_token, quantitade=5, time_ranges=["short_term", "medium_term", "long_term"])
        
        top_faixas_unicas = {}
        tuplas_vistas = set()

        for id_faixa, faixa_dados in top_faixas.items():
            chave_de_unicidade = (faixa_dados["artista_principal"], faixa_dados["nome_faixa"])
    
            if chave_de_unicidade not in tuplas_vistas:
                tuplas_vistas.add(chave_de_unicidade)
                top_faixas_unicas[id_faixa] = faixa_dados

        


       
        print("--------------------------")
        lista_musicas = [(faixa["artista_principal"], faixa["nome_faixa"]) 
        for faixa in top_faixas_unicas.values()]
        

       
        
        ## 2 realizar a estracao de letra de cada uma delas
        print("extraindo letras de musicas")
        letras_musicas = await buscar_letras_em_batch(lista_musicas)

        for i, (chave, dados_faixa) in enumerate(top_faixas_unicas.items()):
            dados_faixa["letra"] = letras_musicas[i]["letra"]

        
        
        print("extraindo emocoes")
        lista_letras = [faixa["letra"] for faixa in top_faixas_unicas.values()]

        lista_emocoes = await extrair_emocoes_em_batch(lista_letras)

        for i, (chave, dados_faixa) in enumerate(top_faixas_unicas.items()):
            dados_faixa["emocoes"] = lista_emocoes[i]

        
      

        
        ## 4 salvar cada faixa no banc de dados
        lista_faixas_para_adicionar = []
        for chave, valor_faixa in top_faixas_unicas.items():
            faixa = {
                "id_faixa": valor_faixa["id_faixa"],
                "nome_faixa": valor_faixa["nome_faixa"],
                "emocoes": valor_faixa["emocoes"],
                "duracao_ms": valor_faixa["duracao_ms"],
                "popularidade": valor_faixa["popularidade"],
                "album": valor_faixa["album"],
                "link_imagem": valor_faixa["link_imagem"],
                "letra_faixa": valor_faixa["letra"]
            }

            lista_faixas_para_adicionar.append(faixa)
            
        print("salvando faixas no banco de dados")
        response = await salvar_faixas_em_batch(db, lista_faixas_para_adicionar)

        

        


        ## 5 salvar o relacoinamento usuarioTopFaixas
        """
            id-usuari
            id_faixa
            _short_time_rank
            long_time_rank
            usuario
            faixa
       
     
        await salvar_UsuarioTopFaixa_em_lote(
                db, 
                
                
            )

             """



        print("inserindo faixas no bd")
        
       

        



