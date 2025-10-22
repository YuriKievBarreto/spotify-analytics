import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

todos_os_escopos = "user-read-private user-read-email user-top-read user-read-recently-played user-read-playback-position user-library-read user-library-modify playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-follow-read user-follow-modify user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control ugc-image-upload"

sp_oauth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=todos_os_escopos,
    show_dialog=True 
)





    
    
        

