# Nova Music - Bot Squad

Nova Music es una aplicación web de análisis musical desarrollada con Python y Streamlit.

La aplicación permite visualizar canciones, artistas, géneros, estadísticas, gráficos y favoritos musicales de forma interactiva.

---

## Objetivo del proyecto

El objetivo de Nova Music es analizar datos musicales reales para identificar tendencias y preferencias musicales.

Esta información puede ser útil para:

- Productores musicales
- Estudios de música
- Empresas publicitarias

---

## Integrantes

- Sanaz Amanmohammadi
- Maria Fernanda Pérez García
- Juan Diego Soto Galvan
- Leoncio Mbomio Mbuña

---

## Estructura del proyecto

El proyecto está organizado en varias carpetas y archivos:

- `web/`: contiene la aplicación web principal de Nova Music.
- `src/`: contiene scripts para descargar y preparar datos.
- `data/`: contiene los archivos de datos musicales usados por la aplicación.
- `notebooks/`: contiene pruebas y análisis realizados durante el desarrollo.
- `requirements.txt`: lista de librerías necesarias para ejecutar el proyecto.
- `Dockerfile`: archivo principal para crear el contenedor Docker de la aplicación.
- `Dockerfile.data`: archivo Docker relacionado con los datos.
- `Dockerfile.download`: archivo Docker relacionado con la descarga de datos.
- `usuarios.db`: base de datos local donde se guardan los usuarios.
- `favoritos.json`: archivo usado para guardar información de favoritos.
- `README.md`: documentación del proyecto.

---

## Arquitectura Docker

La aplicación se ejecuta en un único contenedor Docker.

Este contenedor incluye:

- La aplicación web hecha con Streamlit.
- El código fuente del proyecto.
- Los archivos de datos necesarios.
- Las librerías indicadas en `requirements.txt`.

---

## Contenedor principal

**Nombre de la imagen:** `bot-squad`  
**Aplicación:** Nova Music  
**Tecnología:** Python y Streamlit  
**Puerto local:** `8503`  
**Puerto interno del contenedor:** `8501`  
**Comando de ejecución:** `streamlit run web/app.py`

El contenedor se encarga de:

- Ejecutar la aplicación web.
- Leer los archivos CSV almacenados en `data/clean/`.
- Mostrar las páginas de análisis musical.
- Permitir el uso de canciones, artistas, géneros, favoritos y usuarios.

---
### Ejecución

#### Opción 1 – Ejecución con Docker

Con Docker instalado (https://www.docker.com/products/docker-desktop), abre una terminal en la carpeta del proyecto y ejecuta:

1. Construir la imagen principal de la aplicación: `docker build -t bot-squad .`
2. Iniciar la aplicación: `docker run -p 8503:8501 bot-squad`
3. Abrir el navegador y entrar en: `http://localhost:8503`

Si además quieres ejecutar los pasos de descarga de datos, ejecuta estos comandos en orden antes de iniciar la aplicación:

- Para descargar los datos musicales desde Last.fm:
  `docker build -f Dockerfile.download -t bot-squad-download .`
  `docker run bot-squad-download`

- Para buscar previews de audio en iTunes:
  `docker build -f Dockerfile.data -t bot-squad-data .`
  `docker run bot-squad-data`

---

#### Opción 2 – Ejecución manual (sin Docker)

Abre una terminal en la carpeta raíz del proyecto y sigue estos pasos:

1. Instalar las librerías necesarias: `pip install -r requirements.txt`
2. Descargar los datos musicales desde Last.fm: `python src/download.py`
3. (Opcional) Buscar previews de audio en iTunes: `python src/buscar_audios.py`
4. Lanzar la aplicación: `streamlit run web/app.py`
5. Abrir el navegador y entrar en: `http://localhost:8501`