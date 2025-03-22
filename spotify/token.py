import base64
from . import settings
import json
from requests import post

def get_token():
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET
    }
    result = post(url, data=data)
    if result.status_code != 200:
        print(f"Error: {result.status_code}, Response: {result.text}")
    token = result.json().get('access_token')
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}