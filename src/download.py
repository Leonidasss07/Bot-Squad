import requests
import json
import os
import time
import csv
import math

API_KEY = '2486bf623744f4f6f8e4b2a60720a504'

MAX_CANCIONES_POPULARES = 10000
LIMITE_POR_PAGINA = 1000

# buscar portada usando iTunes
def buscar_url_imagen_itunes(nombre, artista):
    url = "https://itunes.apple.com/search"

    params = {
        "term": f"{artista} {nombre}",
        "media": "music",
        "entity": "song",
        "limit": 1
    }

    try:
        respuesta = requests.get(url, params=params, timeout=10)
        datos = respuesta.json()

        resultados = datos.get("results", [])

        if resultados:
            imagen = resultados[0].get("artworkUrl100", "")

            if imagen:
                return imagen.replace("100x100bb", "600x600bb")

    except Exception:
        pass

    return ""

# obtener portada
def obtener_portada(nombre, artista):
    return buscar_url_imagen_itunes(nombre, artista)


# canciones populares
def obtener_canciones_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'
    canciones = []

    total_paginas = math.ceil(MAX_CANCIONES_POPULARES / LIMITE_POR_PAGINA)

    for pagina in range(1, total_paginas + 1):
        params = {
            'method': 'chart.gettoptracks',
            'api_key': API_KEY,
            'format': 'json',
            'limit': LIMITE_POR_PAGINA,
            'page': pagina
        }

        try:
            respuesta = requests.get(url, params=params, timeout=15)
            datos = respuesta.json()

            if 'error' in datos or 'tracks' not in datos:
                print(f"Aviso: Error o fin de datos en la página {pagina}.")
                break

            for track in datos['tracks']['track']:
                if len(canciones) >= MAX_CANCIONES_POPULARES:
                    break

                nombre = track.get('name', 'N/A')
                artista = track.get('artist', {}).get('name', 'N/A')
                imagen = obtener_portada(nombre, artista)

                cancion = {
                    'nombre': nombre,
                    'artista': artista,
                    'reproducciones': track.get('playcount', 'N/A'),
                    'url': track.get('url', ''),
                    'imagen': imagen
                }

                canciones.append(cancion)

                time.sleep(0.12)

            print(f"Página {pagina} procesada. Canciones en total: {len(canciones)}")
            time.sleep(1)

        except Exception as e:
            print(f"Ocurrió un error en la página {pagina}: {e}")
            break

    return canciones


# artistas populares
def obtener_artistas_populares():
    url = 'http://ws.audioscrobbler.com/2.0/'

    params = {
        'method': 'chart.gettopartists',
        'format': 'json',
        'page': 1,
        'limit': 1000,
        'api_key': API_KEY
    }

    respuesta = requests.get(url, params=params, timeout=15)
    datos = respuesta.json()
    artistas = []

    for artista in datos['artists']['artist']:
        musico = {
            'nombre': artista.get('name', 'N/A'),
            'reproducciones': artista.get('playcount', 'N/A'),
            'oyentes': artista.get('listeners', 'N/A'),
            'url': artista.get('url', ''),
            'imagen': ''
        }

        artistas.append(musico)

    return artistas


# canciones populares del mes
def obtener_canciones_populares_julio():
    url = 'http://ws.audioscrobbler.com/2.0/'

    params = {
        'method': 'album.getinfo',
        'artist': 'KY Noraebang',
        'album': "July 2021's popular song Vol.2",
        'api_key': API_KEY,
        'format': 'json'
    }

    respuesta = requests.get(url, params=params, timeout=15)
    datos = respuesta.json()
    canciones_populares_julio = []

    album = datos.get('album', {})
    tracks = album.get('tracks', {}).get('track', [])

    if isinstance(tracks, dict):
        tracks = [tracks]

    for track in tracks:
        nombre = track.get('name', 'N/A')
        artista = track.get('artist', {}).get('name', 'N/A')
        imagen = obtener_portada(nombre, artista)

        cancion_julio = {
            'nombre': nombre,
            'artista': artista,
            'duracion': track.get('duration', 'N/A'),
            'imagen': imagen
        }

        canciones_populares_julio.append(cancion_julio)

        time.sleep(0.12)

    return canciones_populares_julio

# géneros válidos
GENEROS_VALIDOS = {
    'pop', 'rock', 'hip-hop', 'hip hop', 'rap', 'r&b', 'rnb', 'soul', 'jazz',
    'blues', 'classical', 'electronic', 'dance', 'house', 'techno', 'trance',
    'metal', 'heavy metal', 'punk', 'indie', 'alternative', 'folk', 'country',
    'reggae', 'latin', 'reggaeton', 'k-pop', 'j-pop', 'edm', 'trap', 'funk',
    'disco', 'ambient', 'lo-fi', 'synthpop', 'synthwave', 'grunge', 'emo',
    'gospel', 'opera', 'soundtrack', 'new wave', 'post-rock', 'experimental'
}

# géneros de canciones populares
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

        respuesta = requests.get(url, params=params, timeout=15)
        datos = respuesta.json()

        if 'error' in datos or 'tracks' not in datos:
            print(f"Aviso: error en la página {pagina}")
            break

        for track in datos['tracks']['track']:
            nombre = track.get('name', 'N/A')
            artista = track.get('artist', {}).get('name', 'N/A')

            params_info = {
                'method': 'track.getInfo',
                'api_key': API_KEY,
                'format': 'json',
                'artist': artista,
                'track': nombre
            }

            respuesta_info = requests.get(url, params=params_info, timeout=15)
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

# canciones semanales por género
def obtener_canciones_semanales_tag(tag):
    url = 'http://ws.audioscrobbler.com/2.0/'
    canciones = []

    params_chartlist = {
        'method': 'tag.getweeklychartlist',
        'tag': tag,
        'api_key': API_KEY,
        'format': 'json'
    }

    respuesta_chartlist = requests.get(url, params=params_chartlist, timeout=15)
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

        respuesta = requests.get(url, params=params, timeout=15)
        datos = respuesta.json()

        for track in datos['tracks']['track']:
            nombre = track.get('name', 'N/A')
            artista = track.get('artist', {}).get('name', 'N/A')
            imagen = obtener_portada(nombre, artista)

            cancion = {
                'tag': tag,
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'nombre': nombre,
                'artista': artista,
                'oyentes': track.get('listeners', 'N/A'),
                'url': track.get('url', ''),
                'imagen': imagen
            }

            canciones.append(cancion)

            time.sleep(0.12)

        print(f"Se obtuvieron {len(canciones)} canciones para el tag {tag}")

    except Exception as e:
        print(f"Error al obtener canciones del tag {tag}: {e}")

    return canciones

# guardar archivos json
def guardar_json_lineas(datos, file_path):
    with open(file_path, 'w', encoding='utf-8') as archivo:
        for item in datos:
            archivo.write(json.dumps(item, ensure_ascii=False) + '\n')


def guardar_json_lista(datos, file_path):
    with open(file_path, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


# guardar canciones populares
def guardar_canciones(canciones):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/canciones_populares.json'
    guardar_json_lineas(canciones, file_path)
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

# guardar artistas
def guardar_artistas(artistas):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/artistas_populares.json'
    guardar_json_lineas(artistas, file_path)
    print(f'Se han guardado {len(artistas)} artistas en {file_path}')

# guardar canciones de julio
def guardar_canciones_julio(canciones_populares_julio):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/canciones_populares_julio.json'
    guardar_json_lineas(canciones_populares_julio, file_path)
    print(f'Se han guardado {len(canciones_populares_julio)} canciones en {file_path}')

# guardar géneros
def guardar_generos_canciones(canciones_con_generos):
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/generos_canciones_populares.json'
    guardar_json_lineas(canciones_con_generos, file_path)
    print(f'Se han guardado {len(canciones_con_generos)} géneros en {file_path}')

# guardar canciones por tag
def guardar_canciones_tag(canciones, tag):
    os.makedirs('data/raw', exist_ok=True)
    file_path = f'data/raw/canciones_{tag}.json'
    guardar_json_lista(canciones, file_path)
    print(f'Se han guardado {len(canciones)} canciones en {file_path}')

# guardar archivos csv
def guardar_csv(datos, file_path, columnas):
    os.makedirs('data/clean', exist_ok=True)

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columnas, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for item in datos:
            writer.writerow({columna: item.get(columna, '') for columna in columnas})

    print(f'CSV guardado en {file_path}')

# canciones populares
def guardar_canciones_csv(canciones):
    guardar_csv(
        canciones,
        'data/clean/canciones_populares.csv',
        ['nombre', 'artista', 'reproducciones', 'url', 'imagen']
    )

# artistas populares
def guardar_artistas_csv(artistas):
    guardar_csv(
        artistas,
        'data/clean/artistas_populares.csv',
        ['nombre', 'reproducciones', 'oyentes', 'url', 'imagen']
    )

# canciones de julio
def guardar_canciones_julio_csv(canciones_julio):
    guardar_csv(
        canciones_julio,
        'data/clean/canciones_julio.csv',
        ['nombre', 'artista', 'duracion', 'imagen']
    )

# géneros
def guardar_generos_csv(canciones_con_generos):
    guardar_csv(
        canciones_con_generos,
        'data/clean/generos_canciones.csv',
        ['generos']
    )

# canciones por género
def guardar_canciones_tag_csv(canciones, tag):
    guardar_csv(
        canciones,
        f'data/clean/canciones_{tag}.csv',
        ['tag', 'fecha_desde', 'fecha_hasta', 'nombre', 'artista', 'oyentes', 'url', 'imagen']
    )

# ejecutar
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