from django.shortcuts import render
from django.http import HttpResponse
from . import query
from spotify import settings

def homepage(request):
    # Query for all the songs in the playlist 
    api_query = query.get_playlist_data('5oUK8DDz1pRG4Tiks11H4p')['items']
    # Take the song name and artist 
    print(api_query[0])
    first_song_and_artist = extract_song_and_artist(api_query[0])
    # print(first_song_and_artist)
    artist_data = query.get_artist_data(first_song_and_artist['Artist_ID'])
    # print(artist_data)

    return render(request, 'core/index.html', {'results': first_song_and_artist})

def extract_song_and_artist(item):
    return {
        'Song_Name': item['track']['name'],
        'Artist': item['track']['artists'][0]['name'],
        'Artist_ID': item['track']['artists'][0]['id']
    }