from fastapi import Depends, HTTPException, Cookie, status
from app.core.security import decode_access_token

async def get_current_user_id(
    session_token: str | None = Cookie(default=None)
) -> str:

    if session_token:
        print("token encontrado")
        token_decodificado = decode_access_token(session_token)
        return token_decodificado
        
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado. Cookie de sessão ausente."
        )
  