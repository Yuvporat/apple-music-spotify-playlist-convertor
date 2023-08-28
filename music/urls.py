# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),

    path('login/', views.spotify_login, name='spotify_login'),
    path('logout/', views.logout_view, name='logout'),

    path('scrape/',views.scrape_apple_playlist, name='apple_scrape_playlist'),
    path('create/', views.spotify_create_playlist, name='spotify_create_playlist'),
]
