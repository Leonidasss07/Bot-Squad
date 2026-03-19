import requests
import json
import os
import time

API_KEY = '2486bf623744f4f6f8e4b2a60720a504' 

#canciones populares
def obtener_canciones_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'
    canciones = []
    for pagina in range(1,11):
        params = {
            'method': 'chart.gettoptracks',
            'api_key': API_KEY,
            'format': 'json',
            'limit': 1000,
            'page': pagina
        }
        try:    
            respuesta = requests.get(url, params=params)
            datos = respuesta.json()

            if 'error' in datos or 'tracks' not in datos:
                print(f"Aviso: Error o fin de datos en la página {pagina}.")
                break

            for track in datos['tracks']['track']:
                cancion = {
                    'nombre': track['name'],
                    'artista': track['artist']['name'],
                    'reproducciones': track['playcount'],
                    'url': track['url']
                }
                canciones.append(cancion)

            print(f"Página {pagina} procesada. Canciones en total: {len(canciones)}")
            
            # Pausa de 1 segundo para no saturar la API
            time.sleep(1)
            
        except Exception as e:
            print(f"Ocurrió un error en la página {pagina}: {e}")
            break

    return canciones

#artistas populares
def obtener_artistas_populares():
    
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

#generos de los canciones mas populares
#creamos un set de los generos validos 
GENEROS_VALIDOS = {
    'pop', 'rock', 'hip-hop', 'hip hop', 'rap', 'r&b', 'rnb', 'soul', 'jazz',
    'blues', 'classical', 'electronic', 'dance', 'house', 'techno', 'trance',
    'metal', 'heavy metal', 'punk', 'indie', 'alternative', 'folk', 'country',
    'reggae', 'latin', 'reggaeton', 'k-pop', 'j-pop', 'edm', 'trap', 'funk',
    'disco', 'ambient', 'lo-fi', 'synthpop', 'synthwave', 'grunge', 'emo',
    'gospel', 'opera', 'soundtrack', 'new wave', 'post-rock', 'experimental'
}

def obtener_generos_canciones_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 50
    }
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()

    canciones_con_generos = []

    for track in datos['tracks']['track']:
        nombre = track['name']
        artista = track['artist']['name']

        params_info = {
            'method': 'track.getInfo',
            'api_key': API_KEY,
            'format': 'json',
            'artist': artista,
            'track': nombre
        }
        respuesta_info = requests.get(url, params=params_info)
        datos_info = respuesta_info.json()

        generos = []
        try:
            tags = datos_info['track']['toptags']['tag']
            #solo guardamos los tags que esten en nuestra lista de generos validos
            generos = [
                tag['name'] for tag in tags
                if tag['name'].lower() in GENEROS_VALIDOS
            ]
        except (KeyError, TypeError):
            pass

        #solo se guarda la cancion si tiene al menos un genero valido
        if generos:
            cancion = {'generos': generos}
            canciones_con_generos.append(cancion)

    return canciones_con_generos

#guardar los archivos
def guardar_canciones(canciones):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion in canciones:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

def guardar_artistas(artistas):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/artistas_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for musico in artistas:
            archivo.write(json.dumps(musico, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(artistas)} artistas en {file_path}')

def guardar_canciones_julio(canciones_populares_julio):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares_julio.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion_julio in canciones_populares_julio:
            archivo.write(json.dumps(cancion_julio, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones_populares_julio)} canciones en {file_path}')

def guardar_generos_canciones(canciones_con_generos):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/generos_canciones_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion in canciones_con_generos:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones_con_generos)} canciones con géneros en {file_path}')


if __name__ == '__main__':
    canciones = obtener_canciones_populares()
    guardar_canciones(canciones)

    artistas = obtener_artistas_populares()
    guardar_artistas(artistas)
    
    canciones_julio = obtener_canciones_populares_julio()
    guardar_canciones_julio(canciones_julio)

    canciones_generos = obtener_generos_canciones_populares()
    guardar_generos_canciones(canciones_generos)
