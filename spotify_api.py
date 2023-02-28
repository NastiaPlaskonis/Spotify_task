from dotenv import load_dotenv
import os
import base64
import requests



BASE_URL = "https://api.spotify.com/v1"


# AUTHORIZATION
load_dotenv()
auth_string = f"{os.getenv('CLIENT_ID')}:{os.getenv('CLIENT_SECRET')}"
auth_bytes = auth_string.encode('utf-8')
auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
url = 'https://accounts.spotify.com/api/token'
headers = {'Authorization': f'Basic {auth_base64}'}
data = {'grant_type': 'client_credentials'}
response = requests.post(url, headers=headers, data=data)
token =  response.json().get('access_token')


def get_auth_header():
    return {'Authorization': f'Bearer {token}'}


def get_artist_by_name(name):
    url = f"{BASE_URL}/search?q={name}&type=artist&limit=1"
    response = requests.get(url, headers=get_auth_header())
    result = response.json().get('artists').get('items')
    if result:
        return result[0].get('id'), result[0].get('name')        
    raise ValueError(f'No artist with name {name}')


def get_most_popular_track(artist_id, country='US'):
    url = f"{BASE_URL}/artists/{artist_id}/top-tracks?country={country}"
    headers = get_auth_header()
    response = requests.get(url, headers=get_auth_header())
    try:
        result = response.json().get('tracks')[0]
        return result.get('id'), result.get('name')
    except:
        raise ValueError(f"No results for country {country}")
    

def get_available_markets(track_id):
    url = f"{BASE_URL}/tracks/{track_id}"
    response = requests.get(url, headers=get_auth_header())
    return response.json().get('available_markets')

# print(get_available_markets('7tFiyTwD0nx5a1eklYtX2J'))
