import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import re

def check_song(song_name, artist_name, sp):
    flag = False
    #first try - search track by name and artist
    query = f'track:{song_name} artist:{artist_name}'
    results = sp.search(q=query, type='track', limit=1) 
    if len(results['tracks']['items']) > 0:
        return results
    # second try - search track only by name and try to find the artist in the result
    query = f'track:{song_name}'
    results = sp.search(q=query, type='track', limit=1)       
    if len(results['tracks']['items']) > 0:
        track_artists = [artist['name'] for artist in results['tracks']['items'][0]['artists']]
        if artist_name in track_artists:
            return results
    #third try - remove ' - and parenthesis
    song_name = re.sub(r'\([^)]*\)', '', song_name).replace("'","").replace("-","")
    query = f'track:{song_name} artist:{artist_name}'
    results = sp.search(q=query, type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        return results
    #if nothing worked
    return None

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv(".env")
    SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
    SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']
    SPOTIFY_USERNAME = os.environ['SPOTIFY_USERNAME']

    # Set up Spotipy client credentials

    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Example usage
    song_list = [
        ( 'DOG EAT DOG II (feat. Cruel Santino & Bella Shmurda)','ODUMODUBLVCK'),
        ( 'Highlife Interlude (feat. Phyno)','Seyi Vibez'),
        ( "i'm a mess",'Omah Lay'),
        ('Leave The Door Open', 'Silk Sonic'),
        ('invalid song', 'invalid artist'),
    ]

    # Check if each song is found on Spotify
    for song in song_list:
        song_name, artist_name = song
        if check_song(song_name, artist_name):
            print(f"Spotify found '{song_name}' by '{artist_name}'")
        else:
            print(f"Spotify could not find '{song_name}' by '{artist_name}'")