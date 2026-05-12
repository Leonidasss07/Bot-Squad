import requests
import json
import os
import time
import csv
import math


API_KEY = "2486bf623744f4f6f8e4b2a60720a504"      
MAX_CANCIONES_POPULARES = 10000      
LIMITE_POR_PAGINA = 1000           
MAX_PORTADAS = 10000            

# obtener portadas
def obtener_imagen_cancion(artista, cancion, api_key=API_KEY):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'track.getInfo',
        'api_key': api_key,
        'artist': artista,
        'track': cancion,
        'format': 'json'
    }
    try:
        respuesta = requests.get(url, params=params)
        datos = respuesta.json()
        
        if 'track' in datos and 'album' in datos['track'] and 'image' in datos['track']['album']:
            imagenes = datos['track']['album']['image']
            if len(imagenes) > 0:
                return imagenes[-1]['#text']
    except Exception as e:
        print(f"Error obteniendo imagen para {cancion}: {e}")
        
    return ""

def obtener_canciones_populares():
    url = "http://ws.audioscrobbler.com/2.0/"
    canciones = []

    total_paginas = math.ceil(MAX_CANCIONES_POPULARES / LIMITE_POR_PAGINA)

    for pagina in range(1, total_paginas + 1):
        params = {
            "method": "chart.gettoptracks",
            "api_key": API_KEY,
            "format": "json",
            "limit": LIMITE_POR_PAGINA,
            "page": pagina
        }

        try:
            respuesta = requests.get(url, params=params, timeout=15)
            datos = respuesta.json()

            if "error" in datos or "tracks" not in datos:
                print(f"Aviso: error o fin de datos en la página {pagina}.")
                break

            for track in datos["tracks"]["track"]:
                if len(canciones) >= MAX_CANCIONES_POPULARES:
                    break

                nombre = track.get("name", "N/A")
                artista = track.get("artist", {}).get("name", "N/A")
                imagen_url = ""

                if len(canciones) < MAX_PORTADAS:
                    imagen_url = obtener_imagen_cancion(artista, nombre)
                    time.sleep(0.1)

                cancion = {
                    "nombre": nombre,
                    "artista": artista,
                    "reproducciones": track.get("playcount", "N/A"),
                    "url": track.get("url", ""),
                    "imagen_url": imagen_url
                }

                canciones.append(cancion)

            print(f"Página {pagina} procesada. Canciones en total: {len(canciones)}")
            time.sleep(1)

        except Exception as e:
            print(f"Ocurrió un error en la página {pagina}: {e}")
            break

    return canciones

# artistas populares
def obtener_artistas_populares():
    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "chart.gettopartists",
        "api_key": API_KEY,
        "format": "json",
        "page": 1,
        "limit": 1000
    }

    artistas = []

    try:
        respuesta = requests.get(url, params=params, timeout=15)
        datos = respuesta.json()

        for artista in datos["artists"]["artist"]:
            musico = {
                "nombre": artista.get("name", "N/A"),
                "reproducciones": artista.get("playcount", "N/A"),
                "oyentes": artista.get("listeners", "N/A"),
                "url": artista.get("url", "")
            }

            artistas.append(musico)

    except Exception as e:
        print(f"Error al obtener artistas: {e}")

    return artistas

# canciones populares del mes
def obtener_canciones_populares_julio():
    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "album.getinfo",
        "artist": "KY Noraebang",
        "album": "July 2021's popular song Vol.2",
        "api_key": API_KEY,
        "format": "json"
    }

    canciones_populares_julio = []

    try:
        respuesta = requests.get(url, params=params, timeout=15)
        datos = respuesta.json()

        tracks = datos.get("album", {}).get("tracks", {}).get("track", [])

        if isinstance(tracks, dict):
            tracks = [tracks]

        for track in tracks:
            cancion_julio = {
                "nombre": track.get("name", "N/A"),
                "artista": track.get("artist", {}).get("name", "N/A"),
                "duracion": track.get("duration", "N/A")
            }

            canciones_populares_julio.append(cancion_julio)

    except Exception as e:
        print(f"Error al obtener canciones de julio: {e}")

    return canciones_populares_julio

# géneros válidos
GENEROS_VALIDOS = {
    "pop", "rock", "hip-hop", "hip hop", "rap", "r&b", "rnb", "soul", "jazz",
    "blues", "classical", "electronic", "dance", "house", "techno", "trance",
    "metal", "heavy metal", "punk", "indie", "alternative", "folk", "country",
    "reggae", "latin", "reggaeton", "k-pop", "j-pop", "edm", "trap", "funk",
    "disco", "ambient", "lo-fi", "synthpop", "synthwave", "grunge", "emo",
    "gospel", "opera", "soundtrack", "new wave", "post-rock", "experimental"
}

# géneros de canciones populares
def obtener_generos_canciones_populares():
    url = "http://ws.audioscrobbler.com/2.0/"
    canciones_con_generos = []

    for pagina in range(1, 11):
        params = {
            "method": "chart.gettoptracks",
            "api_key": API_KEY,
            "format": "json",
            "limit": 100,
            "page": pagina
        }

        try:
            respuesta = requests.get(url, params=params, timeout=15)
            datos = respuesta.json()

            if "error" in datos or "tracks" not in datos:
                print(f"Aviso: error en la página {pagina}")
                break

            for track in datos["tracks"]["track"]:
                nombre = track.get("name", "N/A")
                artista = track.get("artist", {}).get("name", "N/A")

                params_info = {
                    "method": "track.getInfo",
                    "api_key": API_KEY,
                    "format": "json",
                    "artist": artista,
                    "track": nombre
                }

                respuesta_info = requests.get(url, params=params_info, timeout=15)
                datos_info = respuesta_info.json()

                try:
                    tags = datos_info["track"]["toptags"]["tag"]

                    for tag in tags:
                        genero = tag["name"].lower()

                        if genero in GENEROS_VALIDOS:
                            canciones_con_generos.append({"generos": genero})

                except (KeyError, TypeError):
                    pass

                time.sleep(0.2)

            print(f"Página {pagina} procesada")

        except Exception as e:
            print(f"Error al obtener géneros en la página {pagina}: {e}")
            break

    return canciones_con_generos

# canciones por género
def obtener_canciones_semanales_tag(tag):
    url = "http://ws.audioscrobbler.com/2.0/"
    canciones = []

    params_chartlist = {
        "method": "tag.getweeklychartlist",
        "tag": tag,
        "api_key": API_KEY,
        "format": "json"
    }

    try:
        respuesta_chartlist = requests.get(url, params=params_chartlist, timeout=15)
        datos_chartlist = respuesta_chartlist.json()

        semanas = datos_chartlist["weeklychartlist"]["chart"]

        if not semanas:
            print(f"No hay semanas disponibles para este tag: {tag}")
            return canciones

        ultima_semana = semanas[-1]
        fecha_desde = ultima_semana["from"]
        fecha_hasta = ultima_semana["to"]

        params = {
            "method": "tag.gettoptracks",
            "tag": tag,
            "api_key": API_KEY,
            "format": "json",
            "limit": 100
        }

        respuesta = requests.get(url, params=params, timeout=15)
        datos = respuesta.json()

        for track in datos["tracks"]["track"]:
            nombre = track.get("name", "N/A")
            artista = track.get("artist", {}).get("name", "N/A")

            imagen_url = obtener_imagen_cancion(artista, nombre)
            time.sleep(0.1)

            cancion = {
                "tag": tag,
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
                "nombre": nombre,
                "artista": artista,
                "oyentes": track.get("listeners", "N/A"),
                "url": track.get("url", ""),
                "imagen_url": imagen_url
            }

            canciones.append(cancion)
        print(f"Se obtuvieron {len(canciones)} canciones para el tag {tag}")

    except Exception as e:
        print(f"Error al obtener canciones del tag {tag}: {e}")

    return canciones

def guardar_json_lineas(datos, file_path):
    with open(file_path, "w", encoding="utf-8") as archivo:
        for item in datos:
            archivo.write(json.dumps(item, ensure_ascii=False) + "\n")

def guardar_json_lista(datos, file_path):
    with open(file_path, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

# guardar csv
def guardar_csv(datos, file_path, columnas):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for item in datos:
            writer.writerow({columna: item.get(columna, "") for columna in columnas})

    print(f"CSV guardado en {file_path}")

# guardar canciones populares
def guardar_canciones(canciones):
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/canciones_populares.json"
    guardar_json_lineas(canciones, file_path)
    print(f"Se han guardado {len(canciones)} canciones en {file_path}")

def guardar_canciones_csv(canciones):
    os.makedirs('data/clean', exist_ok=True)
    file_path = 'data/clean/canciones_populares.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['nombre', 'artista', 'reproducciones', 'url', 'imagen_url'])
        
        for cancion in canciones:
            writer.writerow([
                cancion['nombre'], 
                cancion['artista'], 
                cancion['reproducciones'], 
                cancion['url'], 
                cancion.get('imagen_url', '')
            ])
    print(f'CSV guardado en {file_path}')

# NUEVA FUNCIÓN AÑADIDA PARA EVITAR ERROR
def guardar_artistas(artistas):
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/artistas_populares.json"
    guardar_json_lineas(artistas, file_path)
    print(f"Se han guardado {len(artistas)} artistas en {file_path}")

def guardar_artistas_csv(artistas):
    guardar_csv(
        artistas,
        "data/clean/artistas_populares.csv",
        ["nombre", "reproducciones", "oyentes", "url"]
    )

# guardar canciones de julio
def guardar_canciones_julio(canciones_julio):
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/canciones_populares_julio.json"
    guardar_json_lineas(canciones_julio, file_path)
    print(f"Se han guardado {len(canciones_julio)} canciones en {file_path}")

def guardar_canciones_julio_csv(canciones_julio):
    guardar_csv(
        canciones_julio,
        "data/clean/canciones_julio.csv",
        ["nombre", "artista", "duracion"]
    )

# guardar géneros
def guardar_generos_canciones(canciones_con_generos):
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/generos_canciones_populares.json"
    guardar_json_lineas(canciones_con_generos, file_path)
    print(f"Se han guardado {len(canciones_con_generos)} géneros en {file_path}")

def guardar_generos_csv(canciones_con_generos):
    guardar_csv(
        canciones_con_generos,
        "data/clean/generos_canciones.csv",
        ["generos"]
    )

# guardar canciones por género
def guardar_canciones_tag(canciones, tag):
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/canciones_{tag}.json"
    guardar_json_lista(canciones, file_path)
    print(f"Se han guardado {len(canciones)} canciones en {file_path}")

def guardar_canciones_tag_csv(canciones, tag):
    guardar_csv(
        canciones,
        f"data/clean/canciones_{tag}.csv",
        ["tag", "fecha_desde", "fecha_hasta", "nombre", "artista", "oyentes", "url", "imagen_url"]
    )

# ejecutar
if __name__ == "__main__":
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