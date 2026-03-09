import requests
import json
import os
from config import access_token


def id_url(headers):
    r = requests.get(
    "https://api.spotify.com/v1/search",
    headers=headers,
    params={
        "q": 'Top 50 - España',
        "type": "playlist",
        "limit": 10
    },
    timeout=30,
    )
    r.raise_for_status()

    playlists = r.json()["playlists"]["items"]

    for i, p in enumerate(playlists, 1):
        # 1. Si la playlist viene vacía (None), saltamos al siguiente ciclo
        if not p:
            continue

        # 2. Extraemos el dueño de forma segura
        owner_data = p.get("owner") or {} 
        owner = owner_data.get("display_name", "Sin nombre")
        
        # 3. Extraemos el nombre y el ID también con .get() por si acaso
        nombre = p.get("name", "Sin título")
        id_playlist = p.get("id", "Sin ID")
        return id_playlist


def api_request(id_playlist):
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # OJO: Dependiendo de tu proxy, puede que necesites una barra "/" antes del ID.
    # Si sigue fallando, prueba a cambiar el "4" por "4/"
    url = f"https://api.spotify.com/v1/playlists//{id_playlist}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status() # ¡Vital! Detendrá el código si la URL está mal o el token falla
    return response.json()
    

def data_writing(file_path, data,mode="w"):
    
    os.makedirs("data/raw", exist_ok=True)

    with open(file_path, mode,  encoding="utf-8") as f:
        for element in data:
            f.write(json.dumps(element) + "\n")

#Playlist
headers = {"Authorization": f"Bearer {access_token}"}
id_playlist = id_url(headers)

if id_playlist:
    try:
        playlist_data = api_request(id_playlist)
        playlist_file_path = "data/raw/playlist.json"
        
        # --- NUEVA LÓGICA DE EXTRACCIÓN MÁS ROBUSTA ---
        canciones = []
        
        # Opción A: Estructura de "Playlist Completa" (Spotify Original)
        if "tracks" in playlist_data and "items" in playlist_data["tracks"]:
            canciones = playlist_data["tracks"]["items"]
            
        # Opción B: Estructura de "Solo Tracks" 
        elif "items" in playlist_data:
            canciones = playlist_data["items"]
            
        # Opción C: Tu plan B original (por si el proxy usa "results")
        elif "results" in playlist_data:
            canciones = playlist_data["results"]

        # --- GUARDADO ---
        if canciones:
            data_writing(playlist_file_path, canciones, "w")
            print(f"¡Éxito! Se han guardado {len(canciones)} canciones en {playlist_file_path}.")
        else:
            print("La solicitud fue exitosa, pero no se encontraron canciones bajo las claves conocidas.")
            print("--- INICIO DEL JSON DE RESPUESTA ---")
            print(json.dumps(playlist_data, indent=2)[:800]) # Aumenté un poco el límite para ver mejor
            print("--- FIN DEL JSON DE RESPUESTA ---")

    except requests.exceptions.HTTPError as e:
        print(f"Error al conectar con la API para sacar las canciones: {e}")
else:
    print("No se encontró ninguna playlist en la búsqueda inicial.")

