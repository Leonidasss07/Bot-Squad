import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
import os
import json
import html
from matplotlib.ticker import ScalarFormatter

from db_favoritos import (
    agregar_cancion_favorita,
    eliminar_cancion_favorita,
    es_cancion_favorita,
)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Canciones - Nova Music", layout="wide")

# --- PERSISTENCIA DE FAVORITOS ---
FAVORITOS_FILE = "favoritos.json"

def cargar_favoritos():
    if os.path.exists(FAVORITOS_FILE):
        try:
            with open(FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_favoritos(lista):
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

if 'favoritos' not in st.session_state:
    st.session_state.favoritos = cargar_favoritos()

# --- SESIÓN DE USUARIO ---
def obtener_usuario_activo():
    usuario = st.session_state.get("usuario")

    if usuario:
        return usuario

    if os.path.exists("usuario_activo.txt"):
        with open("usuario_activo.txt", "r", encoding="utf-8") as f:
            usuario_guardado = f.read().strip()

        if usuario_guardado:
            st.session_state["usuario"] = usuario_guardado
            return usuario_guardado

    return None

usuario_activo = obtener_usuario_activo()

# --- ASSETS Y BASE64 ---
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "..", "assets", "canciones.jpeg")
img_base64 = get_base64_image(img_path)

# --- FUNCIONES DE APOYO ---
def texto_seguro(valor):
    if pd.isna(valor):
        return ""
    return html.escape(str(valor))

def formatear_numero(valor):
    try:
        valor = float(valor)

        if valor >= 1_000_000_000:
            return f"{valor / 1_000_000_000:.1f}B"
        if valor >= 1_000_000:
            return f"{valor / 1_000_000:.1f}M"
        if valor >= 1_000:
            return f"{valor / 1_000:.1f}K"

        return f"{valor:.0f}"
    except Exception:
        return str(valor)

def obtener_imagen_fila(row):
    posibles = ["imagen_url", "imagen", "image", "image_url", "cover_url", "cover", "artwork"]

    for col in posibles:
        if col in row.index and pd.notna(row[col]):
            url = str(row[col]).strip().strip('"').strip("'")
            if url.startswith("http"):
                return url

    return ""

def obtener_audio_fila(row):
    posibles = ["audio_url", "preview", "preview_url", "mp3", "audio"]

    for col in posibles:
        if col in row.index and pd.notna(row[col]):
            url = str(row[col]).strip().strip('"').strip("'")
            if url.startswith("http"):
                return url

    return ""

def obtener_url_fila(row):
    if "url" in row.index and pd.notna(row["url"]):
        url = str(row["url"]).strip().strip('"').strip("'")
        if url.startswith("http"):
            return url

    return ""

# --- CARGAR DATOS ---
try:
    canciones = pd.read_csv("data/clean/canciones_populares.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo data/clean/canciones_populares.csv")
    st.stop()

if "reproducciones" in canciones.columns:
    canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
else:
    canciones["reproducciones"] = 0

if "imagen_url" not in canciones.columns:
    canciones["imagen_url"] = ""

if "audio_url" not in canciones.columns:
    canciones["audio_url"] = ""

canciones_ordenadas = canciones.sort_values(
    by="reproducciones",
    ascending=False
).reset_index(drop=True)

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
header {{ visibility: hidden; }}
.stApp {{ background:#000; color:white; }}
[data-testid="stSidebar"] {{ display:none; }}
[data-testid="collapsedControl"] {{ display:none; }}
[data-testid="stToolbar"] {{ display:none; }}
[data-testid="stDecoration"] {{ display:none; }}
footer {{ display:none; }}

.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

.top-menu {{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:42px;

    background-image:
        linear-gradient(to bottom, rgba(0,0,0,0) 25%, rgba(0,0,0,0.95) 100%),
        url("data:image/jpeg;base64,{img_base64}");

    background-size:cover;
    background-position:center top;
    background-repeat:no-repeat;

    height:500px;
    margin-top:-11px;
    position:relative;
}}

.top-menu a {{
    color:white;
    text-decoration:none;
    letter-spacing:2px;
    z-index:2;
    font-weight:bold;
    font-family:"Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
}}

.top-menu a:hover {{
    color:#AFCFCF;
}}

.search-section {{
    text-align:center;
    margin-top:-150px;
    position:relative;
    z-index:3;
}}

.search-section h2 {{
    color:white;
    font-size:38px;
    font-weight:400;
    margin-bottom:8px;
}}

.search-section p {{
    color:rgba(255,255,255,0.72);
    font-size:15px;
}}

.stTextInput input {{
    background:#000 !important;
    color:white !important;
    border:2px solid white !important;
    border-radius:999px;
    padding:8px 24px !important;
    text-align:center;
}}

div[data-testid="stTextInput"] {{
    width:30% !important;
    margin:20px auto 70px auto !important;
}}

.song-row {{
    border-bottom:1px solid #1f2937;
    padding:10px 0;
}}

.stats-title {{
    font-size:22px;
    margin-bottom:20px;
    font-weight:bold;
    color:#ffffff;
    text-align:center;
}}

.song-card {{
    background:#0d0d0d;
    border:1px solid rgba(59,130,246,0.35);
    border-radius:20px;
    padding:14px;
    margin-bottom:16px;
    box-shadow:0 12px 28px rgba(0,0,0,0.25);
}}

.song-layout {{
    display:grid;
    grid-template-columns:72px 1fr;
    gap:14px;
    align-items:center;
}}

.song-cover {{
    width:72px;
    height:72px;
    border-radius:14px;
    overflow:hidden;
    background:#111827;
    display:flex;
    align-items:center;
    justify-content:center;
}}

.song-cover img {{
    width:100%;
    height:100%;
    object-fit:cover;
}}

.song-placeholder {{
    color:#3b82f6;
    font-size:28px;
    font-weight:800;
}}

.song-rank {{
    color:#3b82f6;
    font-size:13px;
    font-weight:800;
    margin-bottom:5px;
}}

.song-name {{
    color:white;
    font-size:16px;
    font-weight:700;
    margin-bottom:5px;
}}

.song-artist {{
    color:rgba(255,255,255,0.65);
    font-size:13px;
}}

.song-meta {{
    color:rgba(255,255,255,0.42);
    font-size:12px;
    margin-top:5px;
}}

.song-link {{
    display:inline-block;
    color:#93c5fd !important;
    text-decoration:none !important;
    font-size:12px;
    font-weight:700;
    margin-top:6px;
}}

[data-testid="stAudio"] {{
    background:transparent !important;
    border:none !important;
    padding:0 !important;
    margin-top:4px;
    margin-bottom:4px;
    box-shadow:none !important;
}}

[data-testid="stAudio"] audio {{
    width:100%;
    height:36px;
    border-radius:20px;
    filter:grayscale(1) brightness(0.85);
}}

div[data-testid="stButton"] > button {{
    background:rgba(255,255,255,0.08) !important;
    color:#ffffff !important;
    border:1px solid rgba(59,130,246,0.60) !important;
    border-radius:14px !important;
    font-weight:800 !important;
    min-height:42px !important;
}}

div[data-testid="stButton"] > button:hover {{
    background:rgba(59,130,246,0.22) !important;
    border:1px solid rgba(59,130,246,0.85) !important;
}}

.login-link {{
    display:inline-block;
    color:#93c5fd !important;
    text-decoration:none !important;
    font-size:12px;
    font-weight:700;
    text-align:center;
}}

@media (max-width:900px) {{
    .top-menu {{
        height:260px;
        gap:18px;
        flex-wrap:wrap;
    }}

    .top-menu a {{
        font-size:12px;
    }}

    div[data-testid="stTextInput"] {{
        width:90% !important;
    }}

    .search-section {{
        margin-top:-90px;
    }}
}}
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

if busqueda:
    canciones_mostrar = canciones_ordenadas[
        canciones_ordenadas["nombre"].str.contains(busqueda, case=False, na=False) |
        canciones_ordenadas["artista"].str.contains(busqueda, case=False, na=False)
    ].copy()
else:
    canciones_mostrar = canciones_ordenadas.head(10).copy()

# --- DISEÑO DE DOS COLUMNAS ---
col1, col2 = st.columns([1.15, 0.85], gap="large")

with col1:
    st.markdown("<div class='stats-title'>Top canciones</div>", unsafe_allow_html=True)

    if canciones_mostrar.empty:
        st.warning("No se encontró ninguna canción.")
    else:
        for i, row in canciones_mostrar.head(10).iterrows():
            nombre = str(row.get("nombre", "")).strip()
            artista = str(row.get("artista", "")).strip()
            imagen = obtener_imagen_fila(row)
            audio = obtener_audio_fila(row)
            url = obtener_url_fila(row)
            reproducciones = row.get("reproducciones", "")

            if imagen:
                cover_html = f'<img src="{html.escape(imagen)}">'
            else:
                inicial = texto_seguro(nombre[:1].upper() if nombre else "♪")
                cover_html = f'<div class="song-placeholder">{inicial}</div>'

            enlace_html = ""
            if url:
                enlace_html = f'<a class="song-link" href="{html.escape(url)}" target="_blank">Ver en Last.fm</a>'

            c_info, c_audio, c_fav = st.columns([3.2, 2.5, 0.65])

            with c_info:
                st.markdown(
                    f"""
                    <div class="song-card">
                        <div class="song-layout" style="grid-template-columns:72px 1fr;">
                            <div class="song-cover">{cover_html}</div>
                            <div>
                                <div class="song-rank">#{i + 1}</div>
                                <div class="song-name">{texto_seguro(nombre)}</div>
                                <div class="song-artist">{texto_seguro(artista)}</div>
                                <div class="song-meta">{formatear_numero(reproducciones)} reproducciones</div>
                                {enlace_html}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c_audio:
                if audio:
                    st.audio(audio, format="audio/mp3")
                else:
                    st.caption("Audio no disponible")

            with c_fav:
                if usuario_activo:
                    ya_es_fav = es_cancion_favorita(usuario_activo, nombre, artista)

                    btn_label = "★" if ya_es_fav else "☆"
                    btn_key = f"fav_cancion_{usuario_activo}_{i}_{nombre}_{artista}"

                    if st.button(btn_label, key=btn_key):
                        if ya_es_fav:
                            eliminar_cancion_favorita(usuario_activo, nombre, artista)
                            st.toast("Eliminado de favoritos")
                        else:
                            agregar_cancion_favorita(
                                usuario=usuario_activo,
                                nombre=nombre,
                                artista=artista,
                                imagen_url=imagen,
                                url=url,
                                audio_url=audio,
                                reproducciones=reproducciones,
                                genero="canciones",
                            )
                            st.toast("¡Añadido a favoritos! ★")

                        st.rerun()
                else:
                    st.markdown(
                        '<a class="login-link" href="/sesion" target="_self">☆ Inicia sesión</a>',
                        unsafe_allow_html=True
                    )

with col2:
    st.markdown("<div class='stats-title'>Gráfico de popularidad</div>", unsafe_allow_html=True)

    if not canciones_mostrar.empty:
        top_plot = canciones_mostrar.head(10).copy()
        top_plot = top_plot.sort_values(by="reproducciones", ascending=True)

        top_plot["reproducciones_millones"] = top_plot["reproducciones"] / 1_000_000

        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor("#000000")
        ax.set_facecolor("#000000")

        bars = ax.barh(
            top_plot["nombre"],
            top_plot["reproducciones_millones"],
            color="#48deec",
            height=0.62
        )

        ax.set_xlabel("Reproducciones en millones", color="#ffffff", fontsize=10)

        ax.tick_params(axis="x", colors="#d1d5db", labelsize=9)
        ax.tick_params(axis="y", colors="#ffffff", labelsize=9)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="x", color="#ffffff", alpha=0.15, linewidth=0.6)

        max_val = top_plot["reproducciones_millones"].max()
        max_val = max_val if max_val > 0 else 1
        ax.set_xlim(0, max_val * 1.22)

        for bar, valor in zip(bars, top_plot["reproducciones_millones"]):
            ax.text(
                bar.get_width() + max_val * 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{valor:.1f}M",
                va="center",
                color="#93c5fd",
                fontsize=8,
                fontweight="bold"
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()