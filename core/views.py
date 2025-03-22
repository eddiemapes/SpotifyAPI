import logging
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from spotipy.oauth2 import SpotifyOAuth
from . import query
from .models import Profile
import spotipy
from spotify import settings
import pandas as pd


logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='spotify.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'core/login.html')

@require_http_methods(['GET'])
def logout_view(request):
    print("Logging out")
    logout(request)
    return redirect('core:login')

def spotify_login():
    # Initialize SpotifyOAuth with client credentials and requested scope
    spotify_oath = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID, 
        client_secret=settings.SPOTIFY_CLIENT_SECRET, 
        redirect_uri=settings.SPOTIFY_REDIRECT_URI, 
        scope='user-library-read')
    
    # Get the Spotify authorization URL that user will be redirected to
    auth_url = spotify_oath.get_authorize_url()
    # Redirect user to Spotify login page
    return redirect(auth_url)


def spotify_callback(request):
    # Initialize SpotifyOAuth again with same credentials
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope='user-library-read'
    )

    # Get authorization code from callback request parameters
    code = request.GET.get("code")
    if code:
        # Exchange authorization code for access and refresh tokens
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]

        # Create Spotify client with access token
        sp = spotipy.Spotify(auth=access_token)
        # Get current user's profile data
        user_data = sp.current_user()
        logging.debug(f"user_data: {user_data}")
        # Extract user ID and email from profile
        spotify_id = user_data["id"]

        # Create or get existing user in Django database
        user, created = User.objects.get_or_create(username=spotify_id)
        profile, created = Profile.objects.get_or_create(user=user)
        print(f"user: {user}, created: {created}")
        check_for_profile_changes(profile, user_data)


        # Store Spotify tokens in session for future API calls
        request.session["spotify_access_token"] = access_token
        request.session["spotify_refresh_token"] = refresh_token

        # Log the user into Django
        login(request, user)
        return redirect("core:home")  # Redirect to dashboard after successful login
    else:
        return redirect("core:home")  # Redirect to home if authorization failed

def get_playlist_details():
    # Query for all the songs in the playlist 
    api_query = query.get_playlist_data('5oUK8DDz1pRG4Tiks11H4p')['items']

    # Extract specific data for songs in playlist
    song_and_artist_list = extract_song_and_artist(api_query)

    # Query for artist data using the Artist ID 
    for entry in song_and_artist_list:
        if entry['Artist_ID']:
            artist_data = query.get_artist_data(entry['Artist_ID'])
            entry['Genres'] = artist_data['genres']
    
    return song_and_artist_list

# This takes in profile object and user data to see if any changes need to be made
def check_for_profile_changes(profile, user_data):
    modified = False

    profile_url = user_data['external_urls']['spotify']
    profile_img_1 = user_data['images'][0]['url']
    profile_img_2 = user_data['images'][1]['url']

    if any([
        profile.profile_url != profile_url,
        profile.profile_img_1 != profile_img_1,
        profile.profile_img_2 != profile_img_2
    ]):
        modified = True

    if modified:
        profile.profile_url = profile_url
        profile.profile_img_1 = profile_img_1
        profile.profile_img_2 = profile_img_2
        profile.save()

    print(f"Profile updated: {modified}")

@login_required
def homepage(request):
    # song_and_artist_list = get_playlist_details()

    context = {

    }
    return render(request, 'core/index.html', context)

def extract_song_and_artist(item):
    song_details_list = []
    for i in item:
        song_details_list.append({'Song_Name': i['track']['name'],
        'Song_ID': i['track']['id'],
        'Album_Name': i['track']['album']['name'],
        'Album_ID': i['track']['album']['id'],
        'Artist_Name': i['track']['artists'][0]['name'],
        'Artist_ID': i['track']['artists'][0]['id']})
    return song_details_list

def extract_genre_from_artist_data(item):
    return item['genres']

