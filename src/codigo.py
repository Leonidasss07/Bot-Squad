import os 
import requests

def api():

    url_spoty = "https://developer.spotify.com/documentation/web-api"
    url_apple = "https://developer.apple.com/documentation/applemusicapi"

    response_spotify = requests.get(url_spoty)
    response_apple = requests.get(url_apple)
    