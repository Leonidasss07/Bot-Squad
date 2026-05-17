import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
import os
import json
from matplotlib.ticker import ScalarFormatter

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Canciones - Nova Music", layout="wide")

# --- PERSISTENCIA DE FAVORITOS ---
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

.search-section {{ text-align:center; margin-top:-150px; }}

.stTextInput input {{
    background:#000 !important; color:white !important;
    border:2px solid white !important; border-radius:999px;
    padding:8px 24px !important; text-align: center;
}}
div[data-testid="stTextInput"] {{ width: 30% !important; margin: 20px auto !important; }}

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

# --- BUSCADOR ---
st.markdown("""
<div class="search-section">
    <h2>Tus canciones favoritas</h2>
    <p>Escucha y guarda lo mejor de Nova Music</p>
</div>
""", unsafe_allow_html=True)

busqueda = st.text_input("Buscar", placeholder="¿Qué quieres escuchar hoy?", label_visibility="collapsed")

# --- CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/clean/canciones_populares.csv")
    df["reproducciones"] = pd.to_numeric(df["reproducciones"], errors="coerce")
    return df

df_canciones = cargar_datos()

if busqueda:
    df_mostrar = df_canciones[
        df_canciones["nombre"].str.contains(busqueda, case=False, na=False) |
        df_canciones["artista"].str.contains(busqueda, case=False, na=False)
    ].copy()
else:
    df_mostrar = df_canciones.sort_values(by="reproducciones", ascending=False).head(10).copy()

st.write("<br>", unsafe_allow_html=True)

# --- DISEÑO DE DOS COLUMNAS ---
col_lista, col_grafico = st.columns([1.2, 0.8], gap="large")

with col_lista:
    st.markdown("<div class='stats-title'>Top Canciones</div>", unsafe_allow_html=True)
    
    if df_mostrar.empty:
        st.warning("No se encontraron resultados.")
    else:
        for index, row in df_mostrar.iterrows():
            # Crear la fila interactiva
            c_img, c_info, c_audio, c_fav = st.columns([1, 2.5, 3, 0.7])
            
            with c_img:
                if pd.notna(row.get("imagen_url")):
                    st.image(row["imagen_url"], use_container_width=True)
            
            with c_info:
                st.markdown(f"**{row['nombre']}**")
                st.caption(f"{row['artista']}")
            
            with c_audio:
                enlace = str(row.get("audio_url", "")).strip()
                if enlace.startswith("http"):
                    st.audio(enlace, format="audio/mp4")
                else:
                    st.caption("🎵 No disponible")
            
            with c_fav:
                es_fav = any(f['nombre'] == row['nombre'] and f['artista'] == row['artista'] for f in st.session_state.favoritos)
                if st.button("❤️" if es_fav else "🤍", key=f"fav_btn_{index}"):
                    if not es_fav:
                        st.session_state.favoritos.append({
                            "nombre": row['nombre'], "artista": row['artista'],
                            "audio_url": row.get("audio_url", ""), "imagen_url": row.get("imagen_url", "")
                        })
                    else:
                        st.session_state.favoritos = [f for f in st.session_state.favoritos if not (f['nombre'] == row['nombre'] and f['artista'] == row['artista'])]
                    guardar_favoritos(st.session_state.favoritos)
                    st.rerun()
            st.markdown("<div class='song-row'></div>", unsafe_allow_html=True)

with col_grafico:
    st.markdown("<div class='stats-title'>Gráfico de Popularidad</div>", unsafe_allow_html=True)
    
    if not df_mostrar.empty:
        top_plot = df_mostrar.head(10).sort_values(by="reproducciones", ascending=True)
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(7, 8))
        fig.patch.set_facecolor('#000')
        ax.set_facecolor('#000')
        
        ax.barh(top_plot["nombre"], top_plot["reproducciones"], color="#48deec")
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='x')
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        plt.tight_layout()
        st.pyplot(fig)
