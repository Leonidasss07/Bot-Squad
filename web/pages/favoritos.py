import streamlit as st
import base64
import os
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Favoritos - Nova Music", layout="wide")

# --- FUNCIONES PARA FAVORITOS ---
FAVORITOS_FILE = "favoritos.json"

def cargar_favoritos():
    if os.path.exists(FAVORITOS_FILE):
        try:
            with open(FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []
    return []

def guardar_favoritos(lista):
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

if 'favoritos' not in st.session_state:
    st.session_state.favoritos = cargar_favoritos()

# --- ASSETS Y BASE64 ---
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""

# Ajusta la ruta de la imagen según la estructura de tus carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "..", "assets", "canciones.jpeg") 
img_base64 = get_base64_image(img_path)

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
header {{ visibility: hidden; }}
.stApp {{ background:#000; color:white; }}
[data-testid="stSidebar"] {{ display:none; }}
.block-container {{ padding: 0 !important; }}

.top-menu {{
    display:flex; justify-content:center; align-items:center; gap:110px;
    background-image:url("data:image/jpg;base64,{img_base64}");
    background-size:cover; height:500px; margin-top: -11px; position:relative;
}}
.top-menu::before {{
    content:""; position:absolute; inset:0;
    background:linear-gradient(to bottom, rgba(0,0,0,0) 25%, rgba(0,0,0,0.95) 100%);
}}
.top-menu a {{ color:white; text-decoration:none; letter-spacing:2px; z-index:2; font-weight: bold; }}

.header-section {{ text-align:center; margin-top:-150px; margin-bottom: 50px; }}

.song-row {{ border-bottom: 1px solid #1f2937; padding: 10px 0; }}
.stats-title {{ font-size:22px; margin-bottom:20px; font-weight: bold; color: #ffffff; }}
</style>
""", unsafe_allow_html=True)

# --- MENÚ SUPERIOR ---
st.markdown("""
<div class="top-menu">
    <a href="/" target="_self">INICIO</a>
    <a href="/dashboard" target="_self">DASHBOARD</a>
    <a href="/canciones" target="_self">CANCIONES</a>
    <a href="/artistas" target="_self">ARTISTAS</a>
    <a href="/generos" target="_self">GÉNEROS</a>
    <a href="/favoritos" target="_self">FAVORITOS</a>
</div>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("""
<div class="header-section">
    <h2>Tu Biblioteca</h2>
    <p>Tus canciones guardadas en un solo lugar</p>
</div>
""", unsafe_allow_html=True)

# --- LISTA DE FAVORITOS ---
col_vacia1, col_centro, col_vacia2 = st.columns([1, 2, 1]) # Centramos el contenido para que se vea mejor

with col_centro:
    st.markdown("<div class='stats-title'>Canciones Favoritas</div>", unsafe_allow_html=True)
    
    favoritos_actuales = st.session_state.favoritos
    
    if not favoritos_actuales:
        st.info("Aún no tienes canciones favoritas guardadas. ¡Ve a la sección de canciones y agrega algunas!")
    else:
        for index, cancion in enumerate(favoritos_actuales):
            # Crear la fila para cada canción favorita
            c_img, c_info, c_audio, c_quitar = st.columns([1, 2.5, 3, 1])
            
            with c_img:
                if cancion.get("imagen_url"):
                    st.image(cancion["imagen_url"], use_container_width=True)
            
            with c_info:
                st.markdown(f"**{cancion['nombre']}**")
                st.caption(f"{cancion['artista']}")
            
            with c_audio:
                enlace = str(cancion.get("audio_url", "")).strip()
                if enlace.startswith("http"):
                    st.audio(enlace, format="audio/mp4")
                else:
                    st.caption("🎵 No disponible")
            
            with c_quitar:
                # Botón para quitar de favoritos
                if st.button("Quitar 🤍", key=f"remove_btn_{index}"):
                    # Filtramos la lista para remover la canción seleccionada
                    st.session_state.favoritos = [f for f in st.session_state.favoritos if not (f['nombre'] == cancion['nombre'] and f['artista'] == cancion['artista'])]
                    guardar_favoritos(st.session_state.favoritos)
                    st.rerun() # Recargamos para actualizar la vista
                    
            st.markdown("<div class='song-row'></div>", unsafe_allow_html=True)