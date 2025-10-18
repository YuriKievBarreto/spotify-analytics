import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost/'

SCOPE = "user-read-private user-read-email user-top-read"

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)

results = sp.search(q='artist:filipe ret', type='artist', limit=1,)

print("--- Resultado da Pesquisa Pública ---")
pprint(results['artists']['items'][0]['name'])
# print(results)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=SCOPE, 
    # Se não usar variáveis de ambiente, descomente e preencha:
    # client_id=CLIENT_ID,
    # client_secret=CLIENT_SECRET,
    # redirect_uri=REDIRECT_URI,
    show_dialog=True # Força o pop-up de login a cada vez (útil para testes)
))



print("--- Informações do Usuário Autenticado (/me) ---")
pprint()