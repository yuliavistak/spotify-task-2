"""
"""
import os
import base64
import json
import pycountry
import folium
from dotenv import load_dotenv
from requests import post, get
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from flask import Flask, render_template, request, redirect

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

def get_songs_by_artist(artist_id):
    """
    Gets top of the 10 most popular artist's songs in USA
    """
    token = get_token()
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result2 = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result2.content)["tracks"]
    with open('g.json', 'w', encoding = 'utf-8') as file:
        json.dump(json_result, file, ensure_ascii = False, indent = 2)
    return json_result


def get_available_markets_of_song(token, song_name):
    """
    """
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
    headers = get_auth_header(token)
    result2 = get(url, headers = headers, timeout = 10)
    json_result = json.loads(result2.content)["tracks"]
    countries = json_result["items"][0]['available_markets']
    return countries

def convert_countries(countries_list: list) -> dict:
    """
    Decodes names of countries from the abbreviation
    """
    res = []
    geolocator = Nominatim(user_agent="song_map")
    for count in countries_list[:10] :
        if count == 'XC':
            count = 'CZ'
        country = pycountry.countries.get(alpha_2=count)
        try:
            country_name = country.official_name
        except AttributeError:
            if count == 'XK':
                country_name = 'Kosovo'
            else:
                country_name = country.name
        # print(country_name)
        # print(country.official_name)
        try:
            location = geolocator.geocode(country_name)
            res.append([country_name, (location.latitude, location.longitude)])
        except GeocoderUnavailable:
            continue

    return res


def create_map(points: list):
    """
    """
    final_map = folium.Map(zoom_start = 2)
    song_map_1 = folium.FeatureGroup(name="Song map")
    html = """<h4>Country:</h4>
    <br>{}</br>"""
    for country in points[:10]:
        iframe = folium.IFrame(html=html.format(country[0]),
                          width=300,
                          height=100)
        song_map_1.add_child(folium.Marker(location=country[1],\
        popup=folium.Popup(iframe), icon=folium.Icon(color="red", icon="info-sign"), zoom_start = 5))

    final_map.add_child(song_map_1)
    final_map.add_child(folium.LayerControl())
    final_map.save('c.html')
    return final_map


def main(artist_name):
    """
    """
    token = get_token()
    artist_id = search_for_artist(token, artist_name)['id']
    song = get_songs_by_artist(artist_id)[0]["name"]
    lst = get_available_markets_of_song(token, song)
    converted = convert_countries(lst)
    map1 = create_map(converted)
    return map1, song
