from spotipy.oauth2 import SpotifyOAuth
from spotify import settings
import spotipy

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID, 
        client_secret=settings.SPOTIFY_CLIENT_SECRET, 
        redirect_uri=settings.SPOTIFY_REDIRECT_URI, 
        scope='user-library-read user-top-read'))
    
    return sp