from spotify import token, settings
from requests import get
import json

def search_for_artist(artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = settings.SPOTIFY_AUTH_HEADER
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']

    return json_result
    

def get_playlist_data(playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/'
    headers = settings.SPOTIFY_AUTH_HEADER
    query = f'tracks?market=US&limit=1000'

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_artist_data(artist_id):
    url = f'https://api.spotify.com/v1/artists/'
    headers = settings.SPOTIFY_AUTH_HEADER
    query_url = url + artist_id
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_album_data(album_id):
    url = f'https://api.spotify.com/v1/albums/'
    headers = settings.SPOTIFY_AUTH_HEADER

    query_url = url + album_id + '?market=US'
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_users_playlists(user_id):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = settings.SPOTIFY_AUTH_HEADER
    query_url = url + '?limit=50'
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

# Time range: short_term, medium_term, long_term
# Limit: Int for returned tracks
def get_users_top_songs(user_id, time_range='short_term', limit=6):
    # url = f"https://api.spotify.com/v1/{user_id}/top/tracks?time_range={time_range}&limit={limit}&offset=0"
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=6&offset=0"
    print(f"URL: {url}")
    headers = settings.SPOTIFY_AUTH_HEADER
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


