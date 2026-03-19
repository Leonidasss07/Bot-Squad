import requests
import json
import os

API_KEY = '2486bf623744f4f6f8e4b2a60720a504' 

#canciones populares
def obtener_canciones_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 1000,
        'page': i+1
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    canciones = []

    for track in datos['tracks']['track']:
        cancion = {
            'nombre': track['name'],
            'artista': track['artist']['name'],
            'reproducciones': track['playcount'],
            'url': track['url']
        }
        canciones.append(cancion)

    return canciones

#artistas populares
def obetener_artistas_populares():
    
    url =  'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettopartists',
        'format': 'json',
        'page': 1,
        'limit': 1000,
        'api_key': API_KEY
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    artistas = []

    for artista in datos['artists']['artist']:
        musico = {
            'nombre': artista['name'],
            'reproducciones': artista['playcount'],
            'oyentes': artista['listeners'],
            'url': artista['url']
        }
        artistas.append(musico)
            
    return artistas

#canciones populares del mes
def obtener_canciones_populares_julio():
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
    'method': 'album.getinfo',
    'artist': 'KY Noraebang',
    'album': 'July 2021\'s popular song Vol.2',
    'api_key': API_KEY,
    'format': 'json'
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    canciones_populares_julio = []

    for track in datos['album']['tracks']['track']:
        cancion_julio = {
            'nombre': track['name'],
            'artista': track['artist']['name'],
            'duracion': track.get('duration', 'N/A')
        }
        canciones_populares_julio.append(cancion_julio)

    return canciones_populares_julio


def guardar_artistas(artistas):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/artistas_populares.json'
    with open(file_path, 'w') as archivo:
        for musico in artistas:
            archivo.write(json.dumps(musico, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(artistas)} artistas en {file_path}')


def guardar_canciones(canciones):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares.json'
    with open(file_path, 'w') as archivo:
        for cancion in canciones:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

def obtener_canciones_populares_julio():
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'album.getinfo',
        'artist': 'KY Noraebang',
        'album': 'July 2021\'s popular song Vol.2',
        'api_key': API_KEY,
        'format': 'json'
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    canciones_populares_julio = []

    for track in datos['album']['tracks']['track']:
        cancion_julio = {
            'nombre': track['name'],
            'artista': track['artist']['name'],
            'duracion': track.get('duration', 'N/A')
        }
        canciones_populares_julio.append(cancion_julio)

    return canciones_populares_julio

def guardar_canciones_julio(canciones_populares_julio):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares_julio.json'
    with open(file_path, 'w') as archivo:
        for cancion_julio in canciones_populares_julio:
            archivo.write(json.dumps(cancion_julio, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones_populares_julio)} canciones en {file_path}')



def guardar_canciones_julio(canciones_populares_julio):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares_julio.json'
    with open(file_path, 'w') as archivo:
        for cancion_julio in canciones_populares_julio:
            archivo.write(json.dumps(cancion_julio, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones_populares_julio)} canciones en {file_path}')


if __name__ == '__main__':
    canciones = obtener_canciones_populares()
    guardar_canciones(canciones)

    artistas = obetener_artistas_populares()
    guardar_artistas(artistas)
    canciones_populares_julio = obtener_canciones_populares_julio()
    guardar_canciones_julio(canciones_populares_julio)
