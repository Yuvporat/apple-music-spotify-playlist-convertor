import requests
from bs4 import BeautifulSoup
import json

def scrape_apple_music_playlist(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    #get the javascript object from the <script> tag
    script_tag = soup.find('script', id='serialized-server-data')
    script_content = script_tag.string
    json_data = json.loads(script_content)

    #extract the data
    playlist_name = json_data[0]['data']['sections'][0]['items'][0]['modalPresentationDescriptor']['headerTitle']
    playlist_description = json_data[0]['data']['sections'][0]['items'][0]['modalPresentationDescriptor']['paragraphText']

    song_list = []
    songs = json_data[0]['data']['sections'][1]['items']
    for song in songs:
         name = song['title']
         artist = song['subtitleLinks'][0]['title']
         album = song['tertiaryLinks'][0]['title']
         song_list.append({'name': name, 'artist': artist, 'album': album})

    return {'name':playlist_name, 'description': playlist_description, 'songs': song_list}