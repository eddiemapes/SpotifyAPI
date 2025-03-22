from spotify import token, settings
from requests import get
import json

def search_for_artist(artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = settings.AUTH_HEADER
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']

    return json_result
    

def get_playlist_data(playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/'
    headers = settings.AUTH_HEADER
    query = f'tracks?market=US&limit=1000'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_artist_data(artist_id):
    url = f'https://api.spotify.com/v1/artists/'
    headers = settings.AUTH_HEADER
    query_url = url + artist_id
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_album_data(album_id):
    url = f'https://api.spotify.com/v1/albums/'
    headers = settings.AUTH_HEADER

    query_url = url + album_id + '?market=US'
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_users_playlists(user_id):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = settings.AUTH_HEADER
    query_url = url + '?limit=50'
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result
