import base64
from . import settings
import json
from requests import post

def get_token():
    auth_string = f'{settings.CLIENT_ID} : {settings.CLIENT_SECRET}'
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
    result = post(url, data=data)
    token = result.json().get('access_token')
    return token

def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}