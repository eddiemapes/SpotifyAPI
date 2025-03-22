from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('dashboard/', views.homepage, name='dashboard'),
]