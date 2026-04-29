import requests
import json
import os
import time
import csv

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

# géneros de las canciones más populares
# creamos un conjunto de géneros válidos
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
    canciones_con_generos = []

    for pagina in range(1, 11):
        params = {
            'method': 'chart.gettoptracks',
            'api_key': API_KEY,
            'format': 'json',
            'limit': 100,
            'page': pagina
        }

        respuesta = requests.get(url, params=params)
        datos = respuesta.json()

        if 'error' in datos or 'tracks' not in datos:
            print(f"Aviso: error en la página {pagina}")
            break

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

            try:
                tags = datos_info['track']['toptags']['tag']

                for tag in tags:
                    genero = tag['name'].lower()

                    if genero in GENEROS_VALIDOS:
                        canciones_con_generos.append({'generos': genero})

            except (KeyError, TypeError):
                pass

            time.sleep(0.2)

        print(f"Página {pagina} procesada")

    return canciones_con_generos

#canciones semanales
def obtener_canciones_semanales_tag(tag):
    url = 'http://ws.audioscrobbler.com/2.0/'
    canciones = []

    params_chartlist = {
        'method': 'tag.getweeklychartlist',
        'tag': tag,
        'api_key': API_KEY,
        'format': 'json'
    }

    respuesta_chartlist = requests.get(url, params=params_chartlist)
    datos_chartlist = respuesta_chartlist.json()

    try:
        semanas = datos_chartlist['weeklychartlist']['chart']

        if not semanas:
            print(f"No hay semanas disponibles para este tag: {tag}")
            return canciones

        ultima_semana = semanas[-1]
        fecha_desde = ultima_semana['from']
        fecha_hasta = ultima_semana['to']

        params = {
            'method': 'tag.gettoptracks',
            'tag': tag,
            'api_key': API_KEY,
            'format': 'json',
            'limit': 100
        }

        respuesta = requests.get(url, params=params)
        datos = respuesta.json()

        for track in datos['tracks']['track']:
            cancion = {
                'tag': tag,
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'nombre': track.get('name', 'N/A'),
                'artista': track.get('artist', {}).get('name', 'N/A'),
                'oyentes': track.get('listeners', 'N/A'),
                'url': track.get('url', 'N/A')
            }
            canciones.append(cancion)

        print(f"Se obtuvieron {len(canciones)} canciones para el tag {tag}")

    except Exception as e:
        print(f"Error al obtener canciones del tag {tag}: {e}")

    return canciones


#guardar los archivos
def guardar_canciones(canciones):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/canciones_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion in canciones:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

def guardar_artistas(artistas):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/artistas_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for musico in artistas:
            archivo.write(json.dumps(musico, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(artistas)} artistas en {file_path}')

def guardar_canciones_julio(canciones_populares_julio):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/canciones_populares_julio.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion_julio in canciones_populares_julio:
            archivo.write(json.dumps(cancion_julio, ensure_ascii=False) + '\n')
    print(f'Se han guardado {len(canciones_populares_julio)} canciones en {file_path}')

def guardar_generos_canciones(canciones_con_generos):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/generos_canciones_populares.json'
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for cancion in canciones_con_generos:
            archivo.write(json.dumps(cancion, ensure_ascii=False) + '\n')
    total_generos = len(canciones_con_generos)
    print(f'Se han guardado {total_generos} géneros en {file_path}')

def guardar_canciones_tag(canciones, tag):
    os.makedirs('data/raw', exist_ok=True)
    file_path = f'data/raw/canciones_{tag}.json'

    with open(file_path, 'w', encoding='utf-8') as archivo:
        json.dump(canciones, archivo, ensure_ascii=False, indent=4)

    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

#archivos csv
def guardar_canciones_csv(canciones):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['nombre', 'artista', 'reproducciones', 'url'])
        for cancion in canciones:
            writer.writerow([cancion['nombre'], cancion['artista'], cancion['reproducciones'], cancion['url']])
    print(f'CSV guardado en {file_path}')

def guardar_artistas_csv(artistas):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/artistas_populares.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['nombre', 'reproducciones', 'oyentes', 'url'])
        for artista in artistas:
            writer.writerow([artista['nombre'], artista['reproducciones'], artista['oyentes'], artista['url']])
    print(f'CSV guardado en {file_path}')

def guardar_canciones_julio_csv(canciones_julio):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_julio.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['nombre', 'artista', 'duracion'])
        for cancion in canciones_julio:
            writer.writerow([cancion['nombre'], cancion['artista'], cancion['duracion']])
    print(f'CSV guardado en {file_path}')

def guardar_generos_csv(canciones_con_generos):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/generos_canciones.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['generos'])
        for cancion in canciones_con_generos:
            writer.writerow([cancion['generos']])
    print(f'CSV guardado en {file_path}')

def guardar_canciones_tag_csv(canciones, tag):
    os.makedirs('data/clean', exist_ok=True)
    file_path = f'data/clean/canciones_{tag}.csv'

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['tag', 'fecha_desde', 'fecha_hasta', 'nombre', 'artista', 'oyentes', 'url'])

        for cancion in canciones:
            writer.writerow([
                cancion['tag'],
                cancion['fecha_desde'],
                cancion['fecha_hasta'],
                cancion['nombre'],
                cancion['artista'],
                cancion['oyentes'],
                cancion['url']
            ])

    print(f'CSV guardado en {file_path}')


if __name__ == '__main__':
    canciones = obtener_canciones_populares()
    guardar_canciones(canciones)
    guardar_canciones_csv(canciones)

    artistas = obtener_artistas_populares()
    guardar_artistas(artistas)
    guardar_artistas_csv(artistas)

    canciones_julio = obtener_canciones_populares_julio()
    guardar_canciones_julio(canciones_julio)
    guardar_canciones_julio_csv(canciones_julio)

    canciones_generos = obtener_generos_canciones_populares()
    guardar_generos_canciones(canciones_generos)
    guardar_generos_csv(canciones_generos)

    tags = ["disco", "rock", "pop", "jazz", "hip-hop", "k-pop"]

    for tag in tags:
        canciones_tag = obtener_canciones_semanales_tag(tag)
        guardar_canciones_tag(canciones_tag, tag)
        guardar_canciones_tag_csv(canciones_tag, tag)