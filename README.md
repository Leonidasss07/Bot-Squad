# Bot Squad
Grupo de trabajo para proyecto de software

### Estructura

- src: código
- data: ficheros crudos y trabajados
- notebooks: ficheros de prueba

### Integrantes: 
-Sanaz Amanmohammadi
-Maria Fernanda Pérez García 
-Juan Diego Soto Galvan
-Leoncio Mbomio Mbuña

### Arquitectura Docker
La aplicación se ejecuta en un único contenedor Docker que contiene la aplicación Streamlit, el código fuente y los archivos de datos necesarios para visualizar el proyecto.

### Contenedor principal
**Nombre:** nova music  
**Tecnología:** Python + Streamlit  
**Puerto:** 8503
**Comando de ejecución:** `streamlit run web/app.py`

El contenedor se encarga de:
- Ejecutar la aplicación web desarrollada con Streamlit.
- Leer los archivos CSV almacenados en `data/clean/`.
- Mostrar las páginas de análisis musical, dashboard, canciones, artistas y géneros.

### Ejecución
1. Primero se genera la imagen Docker a partir del `Dockerfile`: `docker build -t bot-squad .`
2. Docker instala las dependencias indicadas en `requirements.txt`.
3. Se copia el código del proyecto dentro del contenedor.
4. Al iniciar el contenedor, se ejecuta la aplicación Streamlit: `docker run -p 8503:8501 bot-squad`
5. La web queda disponible en `http://localhost:8503`.
