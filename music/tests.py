from django.test import TestCase
import requests

url = 'http://127.0.0.1:8000'

# Create your tests here.
def scrape():
    playlist_url = 'https://music.apple.com/us/playlist/top-100-usa/pl.606afcbb70264d2eb2b51d8dbcfa6a12'
    scrape_url = url + '/scrape/'
    scrape_data = {
        'url' : playlist_url
    }
    response = requests.post(scrape_url, data=scrape_data)
    data = response.json()
    print('status:', response.status_code)
    print(data)
    return data
def create(playlist):
    create_url = url + '/create/'
    headers = {
        'Access-token': 'BQAiKNESt6hUioaausI6yFjZWtqy7LBbYCjtaO0EoPek8QMvSh4w1SjanthBtYL_7ESaUjl56qa6oGsLH0tLh7rNOZsg1ExKjr23NTG0tV1bw-f6RpLdZEM8UGPUCucuxNNo2Mp7g5894eeDOodU4dD1wEbVkOThlgW7uk8tqIV9IiaS9FD7UfAD1mRdx7_2fWjiJDz1X6jHLm7wXQ07iBD9nPnFuyPvDYpZbcXMPPSK7x632Bzm7y8oXd60xQPnVTGe44ss3B3Vcn2NBbeZ2A0yqY4-G3g', #a user access token,
    }
    create_data = {
        'playlist' : playlist
    }
    response = requests.post(create_url, headers=headers, json=create_data)
    print('status:', response.status_code)
    print(response.text)
    return response.text
if __name__ == '__main__':
    playlist = scrape()
    create(playlist)
  