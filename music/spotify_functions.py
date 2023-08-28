import spotipy
from .search import check_song

def create_spotify_playlist(access_token, playlist):
    playlist_name = playlist['name']
    songs = playlist['songs']
    
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.me()['id']

    missing_songs = []
  
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlist['id']

    # Search for each song and add it to the playlist
    for song in songs:
        results = check_song(song['name'],song['artist'], sp)
        if results:
            track = results['tracks']['items'][0]
            track_uri = track['uri']
            # Add the track to the playlist
            sp.playlist_add_items(playlist_id, [track_uri])
        else:
            missing_songs.append(song)
            print('could not find "{}" by "{}"'.format(song['name'],song['artist']))

    print('Playlist created successfully!')
    msg = "{} of {}".format(len(songs) - len(missing_songs),len(songs))
    return { 'missing_songs': missing_songs, "msg" : msg}