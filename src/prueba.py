import os
import json
import requests
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
    response = requests.get(f"https://api.spotify.com/v1/playlists/{id_playlist}", headers=headers)
    return response.json()
    

def data_writing(file_path, data,mode="w"):
    
    os.makedirs("data/raw", exist_ok=True)

    with open(file_path, mode,  encoding="utf-8") as f:
        for element in data:
            f.write(json.dumps(element) + "\n")

#Playlist
headers = {"Authorization": f"Bearer {access_token}"}
id_playlist = id_url(headers)
playlist_data = api_request(id_playlist)
playlist_file_path = "data/raw/playlist.json"
data_writing(playlist_file_path, playlist_data["results"], "w")
