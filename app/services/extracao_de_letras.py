import httpx
from bs4 import BeautifulSoup
import asyncio
import re
import unicodedata



def normalizar_nome(nome: str) -> str:
    nome = nome.lower().strip()
    nome = unicodedata.normalize('NFD', nome)
    nome = nome.encode('ascii', 'ignore').decode('utf-8')
    nome = re.sub(r'[^a-z0-9 ]', '', nome)
    nome = nome.replace(" ", "-")
    return nome


async def buscar_letra(artista: str, musica: str) -> dict:
    artista_fmt = normalizar_nome(artista)
    musica_fmt  = normalizar_nome(musica)

    url = f"https://www.letras.mus.br/{artista_fmt}/{musica_fmt}/"

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(url)

        if resp.status_code != 200:
            return {
                "artista": artista,
                "musica": musica,
                "erro": f"HTTP {resp.status_code}",
                "letra": None
            }

        soup = BeautifulSoup(resp.text, "html.parser")
        lyrics_div = soup.find("div", {"class": "lyric-original"})

        if not lyrics_div:
            return {
                "artista": artista,
                "musica": musica,
                "erro": "Letra não encontrada",
                "letra": None
            }

        letra = lyrics_div.get_text("\n", strip=True)

        return {
            "artista": artista,
            "musica": musica,
            "erro": None,
            "letra": letra
        }

    except Exception as e:
        return {
            "artista": artista,
            "musica": musica,
            "erro": str(e),
            "letra": None
        }



async def buscar_letras_em_batch(lista_musicas: list):
    tasks = [
        buscar_letra(artista, musica)
        for artista, musica in lista_musicas
    ]

    resultados = await asyncio.gather(*tasks)
    return resultados







