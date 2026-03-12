import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '44a679c4d0a34b09b0b6534fa5c2d300'
CLIENT_SECRET = '2ee21c22a3fb4ea5bf7b0963bab7cb78'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def obtener_canciones_populares():
    resultados = sp.search(q='pop 2024', type='track', limit=10)
    canciones = []

    for track in resultados['tracks']['items']:
        cancion = {
            'id': track['id'],
            'nombre': track['name'],
            'artista': track['artists'][0]['name']
        }
        canciones.append(cancion)

    return canciones


def guardar_canciones(canciones):
    with open('data/clean/canciones_populares.json', 'w') as archivo:
        json.dump(canciones, archivo, indent=4)
    print(f'Se han guardado {len(canciones)} canciones.')


if __name__ == '__main__':
    canciones_populares = obtener_canciones_populares()
    guardar_canciones(canciones_populares)
