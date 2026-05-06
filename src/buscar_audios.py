import pandas as pd
import requests
import time

def obtener_preview_itunes(artista, cancion):
    url = "https://itunes.apple.com/search"
    
    parametros = {
        "term": f"{artista} {cancion}",
        "entity": "song",
        "limit": 1
    }
    
    headers = {
        "User-Agent": "ProyectoMusical/1.0"
    }
    
    try:
        respuesta = requests.get(url, params=parametros, headers=headers, timeout=10)
        
        if respuesta.status_code != 200:
            print(f"Bloqueo (Error {respuesta.status_code}) en {cancion}.")
            return ""
            
        datos = respuesta.json()
        
        if 'resultCount' in datos and datos['resultCount'] > 0:
            return datos['results'][0].get('previewUrl', '')
            
    except Exception as e:
        print(f"Error procesando '{cancion}': {e}")
        
    return ""

print("Cargando tu base de datos...")
ruta_archivo = "data/clean/canciones_populares.csv"
canciones = pd.read_csv(ruta_archivo)

canciones['audio_url'] = ""

canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
canciones = canciones.sort_values(by="reproducciones", ascending=False).reset_index(drop=True)

print("Buscando audios en iTunes...")

for index in range(10000):
    if index < len(canciones):
        nombre_artista = canciones.at[index, 'artista']
        nombre_cancion = canciones.at[index, 'nombre']
        
        enlace_audio = obtener_preview_itunes(nombre_artista, nombre_cancion)
        
        if enlace_audio:
            print(f"Audio encontrado para: {nombre_cancion}")
            
        canciones.at[index, 'audio_url'] = enlace_audio
        
        time.sleep(1)

canciones.to_csv(ruta_archivo, index=False)
print("Tu archivo CSV ahora tiene los enlaces de audio de iTunes.")