
import sys
import asyncio
from functools import partial
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.aws_config import aws_bedrock_client
import json



async def extrair_emocoes(letra_musica: str):
        
    prompt =  f"""
        Você é um analisador emocional especializado. 
    Sua tarefa é identificar a intensidade de cada emoção presente na letra da música abaixo.

    Regras:
    - Retorne SOMENTE o JSON.
    - Cada emoção deve ser um número entre 0 e 1.
    - Se a emoção não estiver presente, use 0.
    - Não adicione comentários, explicações ou texto fora do JSON.
    - Não altere os nomes das chaves.
    - A letra pode estar em qualquer idioma, não só português.

    Formato exato de saída:
    {{
    "alegria": 0.75,
    "otimismo": 0.70,
    "esperanca": 0.65,
    "introspeccao": 0.20,
    "paz": 0.50,
    "amor": 0.20,
    "tristeza": 0.05,
    "raiva": 0.03,
    "medo": 0.02,
    "nostalgia": 0.10,
    "melancolia": 0.05,
    "desilusao_amorosa": 0.03,
    "desespero": 0.02,
    "rebeldia": 0.01,
    "anseio": 0.15,
    "autoafirmacao": 0.20,
    "sensualidade: 0.50",
    "sexual_explicit: 0.20"
    }}

    observação: Use sensualidade apenas para conteúdo sexual explícito ou muito direto. Letras apenas românticas ou sedutoras NÃO devem receber esse rótulo

    Letra da música:
    "{letra_musica}"

    """

    call = partial(
        aws_bedrock_client.converse,
        modelId="amazon.nova-pro-v1:0", #"amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )


    try:
        response = await asyncio.to_thread(call)
    except Exception as e:
        print(f"Erro ao chamar Bedrock: {e}")
        return {"erro": str(e)}
    
    raw_output = response["output"]["message"]["content"][0]["text"]
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()
    
    import json

    try:
        emotion_data = json.loads(raw_output)
        return emotion_data
    except json.JSONDecodeError as e:
        print("erro ao converter JSON:", e)
        print("conteúdo retornado pelo Bedrock:")
        print(raw_output)
    return None


async def extrair_emocoes_em_batch(lista_de_letras: list[str]) -> list[dict]:

    tasks = [
        extrair_emocoes(letra)
        for letra in lista_de_letras
    ]

    resultados = await asyncio.gather(*tasks)
    
    return resultados


async def get_perfil_emocional(emocoes: dict) -> str:
    prompt =  f"""
    Você é um analista especializado em comportamento musical e perfil emocional.

A seguir está um JSON com a média das intensidades emocionais (0 a 1) identificadas nas músicas mais ouvidas do usuário:

{json.dumps(emocoes)}

Com base nesses valores, escreva um texto curto (OBRIGATORIAMENTE no máximo 4 linhas) descrevendo:
1. O perfil musical do usuário.
2. Como essa preferência musical se conecta com a visão de mundo dele.

- Seja intuitivo, direto e humano.
- Não cite números ou valores do JSON.
- Não repita o JSON.
- Não use linguagem técnica de análise; apenas interpretação natural.
- Dê ênfase nas duas emoções com pontuação mais alta, mas sem citar valores
    

"""
    
    call = partial(
        aws_bedrock_client.converse,
        modelId="amazon.nova-lite-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}]
    )

    try:
        response = await asyncio.to_thread(call)
        raw_output = response["output"]["message"]["content"][0]["text"]
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()
        return raw_output
    except Exception as e:
        print(f"Erro ao chamar Bedrock: {e}")
        return {"erro": str(e)}
    


