"""
get_token
get_auth_header
search_for_artist
get_songs_by_artist
get_albums_by_artist
search_song_in_album
choice_1
choice_2
choice_3
get_name
check_input1
check_input2
main
"""
import os
import base64
import json
from dotenv import load_dotenv
from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token():
    """
    Gets token for developers
    """
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result0 = post(url, headers = headers, data = data, timeout = 10)
    json_result = json.loads(result0.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    """
    Gets the auth header
    """
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """
    Looks for information abot the artist
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'
    query_url = url + query
    result1 = get(query_url, headers = headers, timeout = 10)
    json_result = json.loads(result1.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    """
    Gets top of the 10 most popular artist's songs in USA
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result2 = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result2.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    """
    Gets list of artist's albums
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result2 = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result2.content)
    return json_result

def search_song_in_album(token, album_id):
    """
    Gets a list of songs of a particular album
    """
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result2 = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result2.content)
    return json_result

def choice_1(token, result):
    """
    Finds top-10 the most popular artist's songs in USA
    Is triggered when the user selects option №1
    """
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

def choice_2(token, result):
    """
    Displays a list of the artist's albums to the use
    Is triggered when the user selects option №2
    """
    artist_id = result["id"]
    albums = get_songs_by_artist(token, artist_id)
    for idx, album in enumerate(albums):
        print(f"{idx + 1}. {album['name']}")

def choice_3(token, result):
    """
    Displays a list of the songs of the album
    Is triggered when the user selects option №3
    """
    while True:
        artist_id = result["id"]
        albums = get_albums_by_artist(token, artist_id)['items']
        print(''.join(album['name']+'\n' for album in albums))
        print('Enter an album name')
        name = input('>>> ')
        album_id = ''
        for album in albums:
            if name == album['name']:
                album_id = album['id']
        if not album_id:
            print("Wrong input")
            res = check_input2()
            if not res:
                return False
            if res:
                continue
        necessary_album = search_song_in_album(token, album_id)['items']
        for idx, song in enumerate(necessary_album):
            print(f"{idx + 1}. {song['name']}")
        break
    return True

def get_name():
    """
    Receives the name of the group or the singer
    entered by the user
    """
    step1 = 'What the name of the singer/group? (Enter a name)'
    print(step1)
    name_artist = input(">>> ")
    token = get_token()
    result = search_for_artist(token, name_artist)
    return token, result

def check_input1(result):
    """
    Checks if the artist is on Spotify
    """
    while not result:
        print("The input is wrong.")
        print("Would you like to continue?(yes/no)")
        choice = input(">>> ")
        if choice in {'yes', 'YES', 'Yes'}:
            result = get_name()[2]
        if choice in {'no', 'NO', 'No'}:
            print('End of the game. See you soon in Spotify:)')
            return False
        check_input1(result)
    return True

def check_input2():
    """
    Check user's answers to yes/no questions
    """
    while True:
        print("Would you like to continue?(yes/no)")
        choice = input(">>> ")
        if choice in {'yes', 'YES', 'Yes'}:
            return True
        if choice in {'no', 'NO', 'No'}:
            print('End of the game. See you soon in Spotify:)')
            return False
        print("Wrong input")
        check_input2()

def main():
    """
    The main function of the program
    Unites all parts of program and makes it work
    """
    start_message = "Hey! Would you like to find out some information about\
 your favourite singer?"
    print(start_message)
    token, result = get_name()
    if not check_input1(result):
        return None
    while True:
        step2 = '''
What information would you like to know? (Enter a number)

    1) Top-10 songs in USA
    2) Artist's albums
    3) Songs from an album
    4) Another artist
    5) Exit
    '''
        print(step2)
        options = input(">>> ")
        if options == '1':
            choice_1(token, result)
        elif options == '2':
            choice_2(token, result)
        elif options == '3':
            if not choice_3(token, result):
                break
        elif options == '4':
            result = get_name()[2]
            check_input1(result)
            continue
        elif options == '5':
            print('End of the game. See you soon in Spotify:)')
            break
        else:
            print("Wrong input")
        if not check_input2():
            break
        continue

if __name__ == '__main__':
    main()
