import requests
import json
import os
import csv

API_KEY = '2486bf623744f4f6f8e4b2a60720a504' 
BASE_URL = "https://ws.audioscrobbler.com/2.0/"


def obtener_artistas_populares(limit=50):
    params = {
        "method": "chart.gettopartists",
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    respuesta = requests.get(BASE_URL, params=params, timeout=15)
    respuesta.raise_for_status()

    datos = respuesta.json()

    if "error" in datos:
        raise Exception(datos.get("message", "Error desconocido de la API"))

    artistas = []

    for artist in datos["artists"]["artist"]:
        artistas.append({
            "nombre": artist.get("name", ""),
            "oyentes": int(artist.get("listeners", 0)),
            "reproducciones": int(artist.get("playcount", 0)),
            "url": artist.get("url", "")
        })

    return artistas

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




def guardar_artistas_json(artistas):
    os.makedirs("data/clean", exist_ok=True)

    ruta = "data/clean/artistas_populares.json"

    with open(ruta, "w", encoding="utf-8") as archivo:
        for artista in artistas:
            archivo.write(json.dumps(artista, ensure_ascii=False) + "\n")


def guardar_artistas_csv(artistas):
    os.makedirs("data/clean", exist_ok=True)

    ruta = "data/clean/artistas_populares.csv"

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(
            archivo,
            fieldnames=["nombre", "oyentes", "reproducciones", "url"]
        )
        writer.writeheader()
        writer.writerows(artistas)


def main():
    try:
        artistas = obtener_artistas_populares(50)
        guardar_artistas_json(artistas)
        guardar_artistas_csv(artistas)

        print("Datos guardados correctamente.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
