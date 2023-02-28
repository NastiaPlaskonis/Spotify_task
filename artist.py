'''
Information about the artist
'''
from dotenv import load_dotenv
import base64
import requests
import json
import os


load_dotenv()
BASE_URL = "https://api.spotify.com/v1"

def to_get_token():
    '''
    Returns token from request
    '''
    auth_string = f"{os.getenv('CLIENT_ID')}:{os.getenv('CLIENT_SECRET')}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': f'Basic {auth_base64}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    token =  response.json()['access_token']

    return token


def get_auth_header(token):
    '''
    Creates header for a request
    '''
    return {'Authorization': f'Bearer {token}'}


def get_artist_by_name(name, token):
    '''
    Gets artist id
    '''
    url = f"{BASE_URL}/search?q={name}&type=artist&limit=1"
    response = requests.get(url, headers = get_auth_header(token))
    result = response.json()['artists']['items']
    if result:
        return result[0]['id'], result[0]['name']
    raise ValueError(f'No artist with name {name}')


def info(name_id, token, reques):
    """
    Finds some information about artist
    """
    header = get_auth_header(token)
    url = f"{BASE_URL}/artists/{name_id}"
    response = requests.get(url ,headers = header)
    result =  json.loads(response.content)
    if reques == "followers":
        return result["followers"]['total']
    else:
        return result[reques]


def album(name_id, token):
    """
    Gets artist's albums
    """
    header = get_auth_header(token)
    url = f'{BASE_URL}/artists/{name_id}/albums'
    response = requests.get(url, headers = header)
    result =  json.loads(response.content)
    res_my = []
    for i in range(len(result[0]['items'])):
        res_my.append(tuple([result['items'][i]['name'], result['items'][i]["release_date"]]))
    return res_my


def top(name_id, token):
    """
    Finds top artist's songs 
    """
    header = get_auth_header(token)
    url = f'{BASE_URL}/artists/{name_id}/top-tracks?country=UA&limit=1'
    response = requests.get(url, headers = header)
    result =  json.loads(response.content)
    res_my = []
    for i in range(len(result[0]['tracks'])):
        res_my.append(result['tracks'][i]['name'])
    return res_my


if __name__ == "__main__":
    name = input("Enter name of artist: ")
    token = to_get_token()
    name_id = get_artist_by_name(name, token)[0]
    answers = ['genres', 'popularity', 'followers', 'id', 'top-tracks', 'albums']
    print(['genres' , 'popularity' , 'followers', 'id' , 'top-tracks' , 'albums'])
    reques = input("Choose what would you like to know about this artist ")
    while reques not in answers:
        print(['genres' , 'popularity' , 'followers', 'id' , 'top-tracks' , 'albums'])
        reques = input("Choose what would you like to know about this artist ")
    if reques in ['genres', 'popularity', 'followers', 'id']:
        print(info(name_id, token, reques))
    elif reques == 'albums':
        for i in album(name_id, token):
            print(f'Album is {i[0]}, date-released of the album: {i[1]}')
    elif reques == 'top-tracks':
        for i in range(len(top(name_id, token))):
            print(f"{i+1}. {top(name_id, token)[i]}")