from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('home/', views.homepage, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('get-top-songs/', views.get_top_songs, name='get-top-songs'),
    path('get-top-artists/', views.get_top_artists, name='get-top-artists'),
    path('get-album-details/<str:album_id>/', views.get_album_details, name='get-album-details'),
]