from app.core.spotipy_auth import sp_oauth_manager
from spotipy import Spotify
from datetime import datetime, timezone, timedelta

async def get_current_user_details(token_info):
    token_info = token_info

    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')

    sp_autenticado = Spotify(auth=access_token)
    user_info = sp_autenticado.current_user()

    id_usuario = user_info['id']
    nome_exibicao = user_info["display_name"]
    pais = user_info["country"]
    
    expires_in_seconds = token_info['expires_in']
    
    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

    return {
          
        "id_usuario": id_usuario,
        "nome_exibicao": nome_exibicao,
        "pais": pais,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_expires_at": token_expires_at
    }
    