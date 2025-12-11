
import sys
import asyncio
from functools import partial
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.services.crud.user_crud import ler_usuario
import math
from app.core.aws_config import aws_bedrock_client
import json
from botocore.exceptions import ClientError
import time

MODEL_ID = "amazon.nova-lite-v1:0"
MODEL_ID_2 = "amazon.nova-pro-v1:0"





async def get_perfil_emocional(emocoes: dict) -> str:
    print("analisando perfil emocional...")
    prompt =  f"""
    Você é um analista especializado em comportamento musical e perfil emocional.

A seguir está um JSON com a média das intensidades emocionais (0 a 1) identificadas nas músicas mais ouvidas do usuário:

{json.dumps(emocoes)}

Com base nesses valores, escreva um texto curto (OBRIGATORIAMENTE no máximo 3 linhas) descrevendo:
1. O perfil musical do usuário.
2. Como essa preferência musical se conecta com a visão de mundo dele.

- Seja intuitivo, direto e humano.
- Escreva um texto direcionado para o usuário (usando "Você" e/ou palavras que direcionem o texto ao usuário)
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
        print("perfil emocional analisado com sucesso!")
        return raw_output
    except Exception as e:
        print(f"Erro ao chamar Bedrock: {e}")
        return {"erro": str(e)}
    


async def get_analise_musica(EMOCAO: str, LETRA):
    print("analisando musica...")
    prompt = f"""

    Instruções:
Você receberá:

Uma emoção predominante, já identificada por outro modelo.

A letra completa de uma música.

Sua tarefa é:

Identificar qual verso ou estrofe da letra tem maior relação direta com a emoção fornecida.

A resposta deve trazer apenas um trecho (o mais relevante).

Explique brevemente por que esse trecho se conecta com a emoção.

Regras:
    - Retorne SOMENTE o JSON.
    - Seja intuitivo, direto e humano.
    - Faça questão de embelezar a explicação, evidenciando um lado poético.

Formato exato da resposta:

{{
  "citacao": "<TRECHO DA LETRA>",
  "explicacao": "<EXPLICAÇÃO CURTA>"
}}


Dados fornecidos:
Emoção predominante: '{EMOCAO}'
Letra da música:
'{LETRA}'

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
        print(f"musica de emocao {EMOCAO} analisada com sucesso!")
        return raw_output
    except Exception as e:
        print(f"Erro ao chamar Bedrock: {e}")
        return {"erro": str(e)}
    

async def get_media_emocoes(emocoes: list):
        print("extraindo media de emocoes...")
        dict_media_emocoes = {}
       
        for item in emocoes:
            for a, b in item.items():
                if a not in dict_media_emocoes:
                    dict_media_emocoes[a] = b
                else:
                    dict_media_emocoes[a] += b
                   

        for chave, valor in dict_media_emocoes.items():
            dict_media_emocoes[chave] = round(valor/len(emocoes), 2)


        return dict_media_emocoes


def montar_prompt_batch(lista_de_letras):
    itens = []
    for i, letra in enumerate(lista_de_letras):
        itens.append(f'"letra_{i}": "{letra}"')

    letras_json = "{\n" + ",\n".join(itens) + "\n}"

    return f"""
Você é um analisador emocional especializado.

Sua tarefa é analisar cada letra e identificar a intensidade de cada emoção listada abaixo.

IMPORTANTE:
- O raciocínio deve acontecer INTERNAMENTE.
- NÃO revele explicações, etapas, análises, divisão por seções ou qualquer texto fora do JSON final.
- A saída final deve conter APENAS um ARRAY JSON, na mesma ordem das letras recebidas.

Processo interno que você DEVE seguir (sem mostrar):
1. Leia cada letra inteira.
2. Resuma internamente a letra.
3. Identifique os temas principais internamente.
4. Separe a letra internamente em seções (verso/refrão/ponte).
5. Avalie emoções SOMENTE quando houver elementos explícitos ou diretamente sugeridos pelo texto.
6. Evite interpretações subjetivas ou simbólicas.
7. Gere as pontuações emocionais baseando-se apenas no texto.

REGRAS:
- A saída deve ser SOMENTE um ARRAY JSON.
- Não explique nada.
- Não descreva nada fora do JSON.
- Não infira nada que não esteja explícito na letra.
- Não interprete símbolos, metáforas ou contexto cultural.
- Não adivinhe sentimentos implícitos.
- Não altere nomes das chaves.
- Todos os itens devem conter TODAS as emoções.
- Valores entre 0.0 e 1.0.
- Use 0.0 quando a emoção não estiver presente de forma clara.

FORMATO DE CADA ITEM DO ARRAY:
{{
  "alegria": 0.0, "otimismo": 0.0, "esperanca": 0.0,
  "introspeccao": 0.0, "paz": 0.0, "amor": 0.0,
  "tristeza": 0.0, "raiva": 0.0, "medo": 0.0,
  "nostalgia": 0.0, "melancolia": 0.0, "desilusao_amorosa": 0.0,
  "desespero": 0.0, "rebeldia": 0.0, "anseio": 0.0,
  "autoafirmacao": 0.0, "sensualidade": 0.0, "sexual_explicit": 0.0
}}

LETRAS:
{letras_json}

Retorne agora SOMENTE o ARRAY JSON.
"""


async def extrair_emocoes_batch_bedrock(lista_de_letras: list[str], chunk_size=1):
    resultados_finais = []

    print(f"\n⚙️ Iniciando batch com {len(lista_de_letras)} letras, chunk_size = {chunk_size}")

    for idx, chunk in enumerate(chunk_list(lista_de_letras, chunk_size)):
        print(f"\n📦 --- Chunk {idx+1} ---")
        print(f"Contém {len(chunk)} letras")

        # medir tempo de geração do prompt
        t0 = time.time()
        prompt = montar_prompt_batch(chunk)
        t1 = time.time()
        print(f"⏱️ Tempo para montar prompt: {t1 - t0:.2f}s")
        print(f"📄 Prompt tem {len(prompt)} caracteres")

        # chamada à API
        print("🚀 Enviando chunk para o Bedrock...")
        t2 = time.time()

        call = partial(
            aws_bedrock_client.converse,
            modelId=MODEL_ID_2,
            messages=[{"role": "user", "content": [{"text": prompt}]}]
        )

        try:
            response = await asyncio.to_thread(call)
        except Exception as e:
            print(f"❌ Erro no chunk {idx+1}: {e}")
            resultados_finais.extend([None] * len(chunk))
            continue

        t3 = time.time()
        print(f"✅ Resposta recebida em {t3 - t2:.2f}s")

        # processamento do retorno
        raw = response["output"]["message"]["content"][0]["text"]
        raw = raw.replace("```json", "").replace("```", "").strip()

        print("📥 JSON bruto retornado:")
        print(raw[:500] + ("..." if len(raw) > 500 else ""))  

        try:
            parsed = json.loads(raw)
            print(f"🟢 JSON válido. Foram retornados {len(parsed)} itens.")
        except json.JSONDecodeError as e:
            print("❌ Erro ao converter JSON:", e)
            parsed = [None] * len(chunk)

        resultados_finais.extend(parsed)

    print("\n🎉 Batch finalizado!")
    print(f"Total de resultados: {len(resultados_finais)}\n")

    return resultados_finais


def chunk_list(lista, tamanho):
    for i in range(0, len(lista), tamanho):
        yield lista[i:i + tamanho]

