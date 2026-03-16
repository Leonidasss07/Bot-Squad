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


##Creamos el codigo para descargar canciones mas populares de un mes
def obtener_canciones_julio():
    # Spotify API permite un límite máximo de 50; usar 10 para evitar errores.
    resultados = sp.search(q='lo mas escuchado en julio 2025', type='track', limit=10)
    canciones_populares_julio = []

    for track in resultados['tracks']['items']:
        cancion_julio = {
            'id': track['id'],
            'nombre': track['name'],
            'artista': track['artists'][0]['name']
        }
        canciones_populares_julio.append(cancion_julio)

    return canciones_populares_julio   

def guardar_canciones_julio(canciones_populares_julio):
    with open('data/clean/canciones_populares_julio.json', 'w') as archivo:
        json.dump(canciones_populares_julio, archivo, indent=4)
    print(f'Se han guardado {len(canciones_populares_julio)} canciones.')


if __name__ == '__main__':
    canciones_populares = obtener_canciones_populares()
    guardar_canciones(canciones_populares)

    canciones_populares_julio = obtener_canciones_julio()
    guardar_canciones_julio(canciones_populares_julio)
