from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from .applemusic_functions import scrape_apple_music_playlist
from .spotify_functions import create_spotify_playlist
import spotipy
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import spotipy
from django.conf import settings

def index(request):
    spotify_authenticated = False
    access_token = ''
    username = request.user

    # Check if the user is_authenticated and not admin
    if request.user.is_authenticated and not request.user.is_superuser:
        try:

    # Check if the user is authenticated with Spotify using UserSocialAuth
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='spotify')
            extra_data = social_auth.extra_data
            #get the access token
            if 'access_token' in extra_data:
                try:# for access token out of date- log out if expired
                    spotify_authenticated = True
                    access_token = extra_data['access_token']
                    #get username
                    sp = spotipy.Spotify(auth=access_token)
                    username = sp.me()['display_name']
                except:
                    logout(request)
                    return redirect('/')
        except UserSocialAuth.DoesNotExist:
            pass
    # You can pass the flag and data to the template
    context = {
        'data': 'my-data',
        'spotify_authenticated': spotify_authenticated,
        # 'access_token' : access_token,
        'username' : username,
    }
    # print('access token:', access_token)
    return render(request, 'vue_app.html',context)

def spotify_login(request):
    return redirect('social:begin', backend='spotify')

def logout_view(request):
    logout(request)
    return redirect('/')

# request must be in this format:
# {
#     "url": "https://music.apple.com/us/playlist/red-hot-chili-peppers-essentials/pl.9055e2e325314c72812d147573977e01"
# }
@api_view(['POST'])
def scrape_apple_playlist(request):
    if request.method == 'POST':
        print('request.user:',request.user)
        playlist_url = request.data['url']
        playlist = scrape_apple_music_playlist(playlist_url)
        return Response(playlist, status=status.HTTP_200_OK)
@api_view(['POST'])
def spotify_create_playlist(request):
    if request.method == 'POST':

            #get user's access token
            print('request.user:',request.user)

            #get access token and user id from request user and not from request headers
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='spotify')
            access_token = social_auth.extra_data.get('access_token')
            #get access token and user id from request headers
            # access_token =  request.META.get('HTTP_ACCESS_TOKEN')
            # print('access_token:',access_token)
            playlist = request.data['playlist']
            result = create_spotify_playlist(access_token,playlist)
    return Response(result, status=status.HTTP_200_OK)