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