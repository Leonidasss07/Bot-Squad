import pandas as pd
import requests
import time
import os

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
            print(f"Bloqueo o error {respuesta.status_code} en {cancion}.")
            return ""
            
        datos = respuesta.json()
        
        if datos.get("resultCount", 0) > 0:
            return datos["results"][0].get("previewUrl", "")
            
    except Exception as e:
        print(f"Error procesando '{cancion}': {e}")
    return ""

print("Cargando tu base de datos...")

ruta_archivo = "data/clean/canciones_populares.csv"
ruta_backup = "data/clean/canciones_populares_backup.csv"

canciones = pd.read_csv(ruta_archivo)

# crear copia de seguridad antes de modificar
if not os.path.exists(ruta_backup):
    canciones.to_csv(ruta_backup, index=False)
    print(f"Copia de seguridad creada en {ruta_backup}")

# crear columna si no existe
if "audio_url" not in canciones.columns:
    canciones["audio_url"] = ""

# ordenar por reproducciones
canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
canciones = canciones.sort_values(by="reproducciones", ascending=False).reset_index(drop=True)

print("Buscando audios en iTunes...")

limite = min(10000, len(canciones))

for index in range(limite):
    nombre_artista = canciones.at[index, "artista"]
    nombre_cancion = canciones.at[index, "nombre"]

    # saltar canciones que ya tienen audio
    audio_actual = canciones.at[index, "audio_url"]

    if pd.notna(audio_actual) and str(audio_actual).strip() != "":
        print(f"Ya tenía audio: {nombre_cancion}")
        continue

    enlace_audio = obtener_preview_itunes(nombre_artista, nombre_cancion)
    
    if enlace_audio:
        print(f"{index + 1}/{limite} Audio encontrado para: {nombre_cancion}")
    else:
        print(f"{index + 1}/{limite} Sin audio para: {nombre_cancion}")
        
    canciones.at[index, "audio_url"] = enlace_audio

    # guardar progreso cada 100 canciones
    if (index + 1) % 100 == 0:
        canciones.to_csv(ruta_archivo, index=False)
        print(f"Progreso guardado hasta la canción {index + 1}")

    time.sleep(1)

canciones.to_csv(ruta_archivo, index=False)

print("Tu archivo CSV ahora tiene los enlaces de audio de iTunes.")