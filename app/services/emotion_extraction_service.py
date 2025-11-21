
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.core.aws_config import aws_bedrock_client



def extrair_emocoes(letra_musica: str):
        
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
    "empoderamento": 0.20
    }}


    Letra da música:
    "{letra_musica}"

    """

    response = aws_bedrock_client.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[
            {"role": "user", "content": [{"text": prompt}]}
        ]
    )

    
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


