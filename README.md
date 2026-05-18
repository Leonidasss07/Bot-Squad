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
**Tecnología:** Python + Streamlit  
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
1. Primero se genera la imagen Docker a partir del `Dockerfile`: `docker build -t bot-squad .`
2. Docker instala las dependencias indicadas en `requirements.txt`.
3. Se copia el código del proyecto dentro del contenedor.
4. Al iniciar el contenedor, se ejecuta la aplicación Streamlit: `docker run -p 8503:8501 bot-squad`
5. La web queda disponible en `http://localhost:8503`.