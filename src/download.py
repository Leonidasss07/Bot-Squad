import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '44a679c4d0a34b09b0b6534fa5c2d300'
CLIENT_SECRET = '2ee21c22a3fb4ea5bf7b0963bab7cb78'
REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope='playlist-read-public'
))

def obtener_canciones_populares():
    # Top 50 Global
    resultados = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=50)
    canciones = []

    for item in resultados['items']:
        track = item['track']
        cancion = {
            'id': track['id'],
            'nombre': track['name'],
            'artista': track['artists'][0]['name']
        }
        canciones.append(cancion)

    return canciones