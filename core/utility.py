import spotipy
from datetime import datetime

from spotipy.oauth2 import SpotifyOAuth
from spotify import settings


def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID, 
        client_secret=settings.SPOTIFY_CLIENT_SECRET, 
        redirect_uri=settings.SPOTIFY_REDIRECT_URI, 
        scope='user-library-read user-top-read'))
    
    return sp

def convert_str_to_date(date_str, format):
    try:
        date_obj = datetime.strptime(date_str, format)
        print(f"date_obj: {date_obj}")
        return datetime.strptime(date_str, format)
    except ValueError as e:
        print(f'failed: {e}')
        return date_str
