from app.core.spotipy_auth import sp_oauth_manager
from spotipy import Spotify
from datetime import datetime, timezone, timedelta

async def autenticar_sp(token_info):
    access_token = token_info['access_token']
    sp_autenticado = Spotify(auth=access_token)

    
    return sp_autenticado




async def get_current_user_details(token_info):

    sp_autenticado =  autenticar_sp(token_info)
    user_info = sp_autenticado.current_user()

    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')
    
    expires_in_seconds = token_info['expires_in']
    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

    
    
    return {
          
        "id_usuario": user_info['id'],
        "nome_exibicao": user_info["display_name"],
        "pais": user_info["country"],
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_expires_at": token_expires_at
    }




async def get_top_faixas(token_info):
    sp = autenticar_sp(token_info)

    TIME_RANGES = ["short_term", "medium_term", "long_term"]

    final_unified_tracks = {} 

    for term in TIME_RANGES:
        
    
        resultados = sp.current_user_top_tracks(time_range=term)
        
        rank_key = f"{term}_rank" 
        
    
        for rank_index, item in enumerate(resultados.get("items", [])):
            track_id = item["id"]
            rank_value = rank_index + 1
            
            
            if track_id not in final_unified_tracks:
                
            
                track_data = {
                    "id_faixa": track_id,
                    "nome_faixa": item["name"],
                }
                
                
                for other_term in TIME_RANGES:
                    track_data[f"{other_term}_rank"] = None
                    
                final_unified_tracks[track_id] = track_data
            
        
            final_unified_tracks[track_id][rank_key] = rank_value

        final_unified_tracks

    return
    