
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
import os

from utils_loader import mostrar_loader

#tablas
def tabla_negra(df):
    html = """
    <table style='width:60%; 
    margin:auto; border-collapse:collapse; 
    background:#000; color:white; 
    border-radius:10px; overflow:hidden; 
    margin-top:20px; border:1px solid #ec4899; 
    font-size:13px;'>
        <thead>
            <tr style='background:#111827;'>
    """
    for col in df.columns:
        html += f"<th style='padding:10px; text-align:left; border-bottom:1px solid #ec4899; color:#e5e7eb; font-weight:400;'>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr style='border-bottom:1px solid #1f2937;'>"
        for val in row:
            html += f"<td style='padding:10px; color:#d1d5db; font-weight:300;'>{val}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html


def tabla_top(df):
    html = """
    <table style='width:82%; margin:auto; 
    border-collapse:collapse; background:#000; 
    color:white; border-radius:10px; 
    overflow:hidden; 
    margin-top:20px; 
    border:1px solid #ec4899; 
    font-size:13px;'>
        <thead>
            <tr style='background:#111827;'>
    """
    for col in df.columns:
        html += f"<th style='padding:10px; text-align:left; border-bottom:1px solid #ec4899; color:#e5e7eb; font-weight:400;'>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr style='border-bottom:1px solid #1f2937;'>"
        for val in row:
            html += f"<td style='padding:10px; color:#d1d5db; font-weight:300;'>{val}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html


st.set_page_config(page_title="Proyecto Musical", layout="wide")

loader = mostrar_loader(1)

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "..", "assets", "populares.jpg")
img_base64 = get_base64_image(img_path)

st.markdown(f"""
<style>
html, body {{
    margin: 0;
    padding: 0;
}}

header {{
    visibility: hidden;
}}

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:#000;
    color:white;
}}
            
.block-container {{
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}}

[data-testid="stSidebar"] {{
    display:none;
}}

.top-menu {{
    display:flex;
    justify-content:center;
    align-items:center;
    gap:110px;
    background-image:url("data:image/jpg;base64,{img_base64}");
    background-size:cover;
    height:190px;
    margin-top: -11px;
    position:relative;
    overflow:hidden;
}}

.top-menu::before {{
    content:"";
    position:absolute;
    inset:0;
    background:linear-gradient(
        to bottom,
        rgba(0,0,0,0.00) 0%,
        rgba(0,0,0,0.15) 40%,
        rgba(0,0,0,0.60) 70%,
        rgba(0,0,0,0.95) 100%
    );
    z-index:1;
    pointer-events: none;
}}

.top-menu a {{
    color:white;
    text-decoration:none;
    letter-spacing:2px;
}}

.search-section {{
    text-align:center;
    margin-top:40px;
}}

.stTextInput input {{
    background:#000 !important;
    color:white !important;
    border:2px solid white !important;
    border-radius:999px;

    padding:8px 14px !important;
    font-size:13px !important;
}}
div[data-testid="stTextInput"] {{
    width: 28% !important;
    margin: 25px auto !important;
}}

div[data-testid="stTextInput"] > div {{
    width: 100% !important;
}}

div[data-baseweb="input"] {{
    width: 100% !important;
}}

.stTextInput input:focus {{
    border:2px solid #ec4899 !important;
}}

.stats-title {{
    text-align:center;
    font-size:22px;
    margin-bottom:10px;
}}
</style>
""", unsafe_allow_html=True)

#menu
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

@st.cache_data
def cargar_artistas():
    return pd.read_csv("data/clean/artistas_populares.csv")

artistas = cargar_artistas()
artistas["reproducciones"] = pd.to_numeric(artistas["reproducciones"], errors="coerce")

artistas_ordenados = artistas.sort_values(by="reproducciones", ascending=False).reset_index(drop=True)

#buscador de artistas
st.markdown("""
<div class="search-section">
    <h2>Descubre tu artista favorito</h2>
    <p>Explora los artistas más escuchados</p>
</div>
""", unsafe_allow_html=True)

busqueda = st.text_input("Buscar artista", placeholder="Buscar artista...", label_visibility="collapsed")

if busqueda:
    resultados = artistas_ordenados[
        artistas_ordenados["nombre"].str.contains(busqueda, case=False, na=False)
    ].copy()

    if resultados.empty:
        st.warning("No se encontró ningún artista.")
    else:
        resultados["posición"] = resultados.index + 1
        resultados["reproducciones"] = resultados["reproducciones"].map("{:,.0f}".format)

        st.markdown(
            tabla_negra(resultados[["posición", "nombre", "reproducciones", "oyentes"]]),
            unsafe_allow_html=True
        )

st.divider()

loader.empty()

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='stats-title'>Top 10 Artistas</div>", unsafe_allow_html=True)

    top10 = artistas_ordenados.head(10).copy()
    top10["reproducciones"] = top10["reproducciones"].map("{:,.0f}".format)

    st.markdown(
        tabla_top(top10[["nombre", "reproducciones", "oyentes"]]),
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<div class='stats-title'>Gráfico de Popularidad</div>", unsafe_allow_html=True)

    top = artistas_ordenados.head(10)

    fig, ax = plt.subplots(figsize=(6,4))

    ax.barh(
        top["nombre"],
        top["reproducciones"],
        color="#ff2d95"
    )

    ax.invert_yaxis()

    fig.patch.set_facecolor("#000")
    ax.set_facecolor("#000")

    ax.tick_params(colors="#d1d5db", labelsize=8)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="x", color="#1f2937", linewidth=0.5)

    plt.tight_layout()

    st.pyplot(fig)
