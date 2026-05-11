import pandas as pd
import requests
import time

#guardar preview de canciones
def obtener_preview_itunes(artista, cancion):
    url = "https://itunes.apple.com/search"
    
    parametros = {
        "term": f"{artista} {cancion}",
        "entity": "song",
        "limit": 1
    }
    
    # 1. Somos honestos con Apple. No fingimos ser Chrome.
    headers = {
        "User-Agent": "ProyectoMusical/1.0"
    }
    
    try:
        # Añadimos un 'timeout' por si la conexión se queda colgada
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

print("Buscando audios en iTunes (iremos más lento para no activar las alarmas)...")

for index in range(10000):
    if index < len(canciones):
        nombre_artista = canciones.at[index, 'artista']
        nombre_cancion = canciones.at[index, 'nombre']
        
        enlace_audio = obtener_preview_itunes(nombre_artista, nombre_cancion)
        
        # Solo imprimimos un mensajito si la encontró para ver que todo va bien
        if enlace_audio:
            print(f"✅ Audio encontrado para: {nombre_cancion}")
            
        canciones.at[index, 'audio_url'] = enlace_audio
        
        # 2. AUMENTAMOS LA PAUSA A 1.5 SEGUNDOS
        # Este es el secreto para que no nos den el Error 403
        time.sleep(1)

canciones.to_csv(ruta_archivo, index=False)
print("¡Listo! Tu archivo CSV ahora tiene los enlaces de audio de iTunes.")