import requests
import json
import os
import time
import csv

API_KEY = '2486bf623744f4f6f8e4b2a60720a504' 


def guardar_top_semanal_json():
    url = 'http://ws.audioscrobbler.com/2.0/'
    
    # Parámetros corregidos
    params = {
        'method': 'tag.getweeklytrackchart', # Método para obtener las canciones
        'tag': 'rock',
        'api_key': API_KEY, # Reemplaza con tu clave
        'format': 'json'
    }
    
    try:
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status() # Verifica si hubo errores en la petición
        datos = respuesta.json()
        
        # Guardar como archivo JSON
        nombre_archivo = 'top_canciones_semana.json'
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Archivo '{nombre_archivo}' guardado con éxito.")
        return datos

    except Exception as e:
        print(f"❌ Error: {e}")

# Ejecutar la función
guardar_top_semanal_json()