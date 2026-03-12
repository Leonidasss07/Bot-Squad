import requests
import json
import os

API_KEY = '2486bf623744f4f6f8e4b2a60720a504' 
def obtener_canciones_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 50
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    canciones = []

    for track in datos['tracks']['track']:
        cancion = {
            'nombre': track['name'],
            'artista': track['artist']['name'],
            'reproducciones': track['playcount']
        }
        canciones.append(cancion)

    return canciones

def obetener_artistas_populares():
    url =  'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettopartists',
        'format': 'json',
        'page': 1,
        'limit': 50,
        'api_key': API_KEY
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    artistas = []

    for artista in datos['artists']['artist']:
        musico = {
            'nombre': artista['name'],
            'reproducciones': artista['playcount'],
            'oyentes': artista['listeners']
        }
        artistas.append(musico)
        
    return artistas

def guardar_artistas(artistas):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/artistas_populares.json'
    with open(file_path, 'w') as archivo:
        for musico in artistas:
            archivo.write(json.dumps(musico, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(artistas)} artisatas en {file_path}')




def guardar_canciones(canciones):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares.json'
    with open(file_path, 'w') as archivo:
        for cancion in canciones:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')


if __name__ == '__main__':
    canciones = obtener_canciones_populares()
    guardar_canciones(canciones)
    artistas = obetener_artistas_populares()
    guardar_artistas(artistas)