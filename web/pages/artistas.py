import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64
import os
import html
import streamlit.components.v1 as components

from utils_loader import mostrar_loader

# CONFIGURACIÓN
st.set_page_config(
    page_title="Artistas - Nova Music",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

loader = mostrar_loader(1)


# FUNCIONES
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""


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


def tabla_artistas(df):
    html_tabla = """
    <table style="width:95%; margin:auto; border-collapse:collapse;
    background:#000; color:white; border-radius:14px; overflow:hidden;
    margin-top:20px; border:1px solid #ec4899; font-size:17px;">
        <thead>
            <tr style="background:#111827;">
    """

    for col in df.columns:
        html_tabla += f"""
        <th style="padding:16px; text-align:left; border-bottom:1px solid #ec4899;
        color:#e5e7eb; font-weight:400;">{texto_seguro(col)}</th>
        """

    html_tabla += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html_tabla += '<tr style="border-bottom:1px solid #1f2937;">'
        for val in row:
            html_tabla += f'<td style="padding:16px; color:#d1d5db; font-weight:300;">{texto_seguro(val)}</td>'
        html_tabla += "</tr>"

    html_tabla += "</tbody></table>"
    return html_tabla


def tabla_top(df):
    html_tabla = """
    <table style="width:95%; margin:auto; border-collapse:collapse;
    background:#000; color:white; border-radius:14px; overflow:hidden;
    margin-top:20px; border:1px solid #ec4899; font-size:17px;">
        <thead>
            <tr style="background:#111827;">
    """

    for col in df.columns:
        html_tabla += f"""
        <th style="padding:16px; text-align:left; border-bottom:1px solid #ec4899;
        color:#e5e7eb; font-weight:400;">{texto_seguro(col)}</th>
        """

    html_tabla += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html_tabla += '<tr style="border-bottom:1px solid #1f2937;">'
        for val in row:
            html_tabla += f'<td style="padding:16px; color:#d1d5db; font-weight:300;">{texto_seguro(val)}</td>'
        html_tabla += "</tr>"

    html_tabla += "</tbody></table>"
    return html_tabla


def cargar_artistas():
    return pd.read_csv("data/clean/artistas_populares.csv")


# IMAGEN DE FONDO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE_DIR, "..", "assets", "populares.jpg")
img_base64 = get_base64_image(img_path)


# CSS
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: #000000 !important;
    color: #ffffff !important;
    margin: 0;
    padding: 0;
}}

header, footer, #MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

* {{
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}}

.block-container {{
    max-width: 100% !important;
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

hr {{
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}}

.menu-superior {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 32px;

    height: 400px;
    padding-bottom: 58px;
    margin-top: 0;

    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);

    background-image:
        linear-gradient(to right, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to left, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(
            to bottom,
            rgba(0,0,0,0) 0%,
            rgba(0,0,0,0) 78%,
            rgba(0,0,0,0.35) 88%,
            rgba(0,0,0,0.75) 95%,
            rgba(0,0,0,1) 100%
        ),
        url("data:image/jpg;base64,{img_base64}");

    background-size: cover;
    background-position: center top;
    background-repeat: no-repeat;

    position: relative;
    z-index: 10;
}}

.menu-superior a {{
    color: white;
    text-decoration: none;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 3px;
    font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
    text-transform: uppercase;
    transform: none;
    text-shadow: 0 3px 12px rgba(0,0,0,0.85);
}}

.menu-superior a:hover {{
    color: #ec4899;
}}

.search-section {{
    text-align: center;
    margin-top: 36px;
}}

.search-section h2 {{
    color: white;
    font-size: 38px;
    font-weight: 400;
    margin-bottom: 8px;
    text-shadow: 0 4px 18px rgba(0,0,0,0.75);
}}

.search-section p {{
    color: rgba(255,255,255,0.72);
    font-size: 15px;
    font-weight: 400;
}}

.stTextInput input {{
    background: #0d0d0d !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    border-radius: 999px;
    padding: 10px 18px !important;
    font-size: 13px !important;
    text-align: center;
}}

.stTextInput input:focus {{
    border: 1px solid #ec4899 !important;
}}

div[data-testid="stTextInput"] {{
    width: 32% !important;
    margin: 25px auto !important;
}}

.stats-title {{
    text-align: center;
    font-size: 24px;
    margin-bottom: 10px;
    font-weight: 400;
    color: white;
}}

@media (max-width: 900px) {{
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    .menu-superior {{
        height: 240px;
        gap: 18px;
        flex-wrap: wrap;
        padding-bottom: 42px;
    }}

    .menu-superior a {{
        font-size: 12px;
        letter-spacing: 2px;
    }}

    div[data-testid="stTextInput"] {{
        width: 90% !important;
    }}

    .search-section h2 {{
        font-size: 30px;
    }}
}}
</style>

<div class="menu-superior">
    <a href="/" target="_self">Inicio</a>
    <a href="/dashboard" target="_self">Dashboard</a>
    <a href="/canciones" target="_self">Canciones</a>
    <a href="/artistas" target="_self">Artistas</a>
    <a href="/generos" target="_self">Géneros</a>
    <a href="/favoritos" target="_self">Favoritos</a>
</div>
""", unsafe_allow_html=True)


# DATOS
artistas = cargar_artistas()

artistas["reproducciones"] = pd.to_numeric(artistas["reproducciones"], errors="coerce")
artistas["oyentes"] = pd.to_numeric(artistas["oyentes"], errors="coerce")

if "imagen_url" not in artistas.columns:
    artistas["imagen_url"] = ""

artistas_ordenados = artistas.sort_values(
    by="reproducciones",
    ascending=False
).reset_index(drop=True)

loader.empty()


# BUSCADOR
st.markdown("""
<div class="search-section">
    <h2>Descubre tu artista favorito</h2>
    <p>Explora los artistas más escuchados</p>
</div>
""", unsafe_allow_html=True)

busqueda = st.text_input(
    "Buscar artista",
    placeholder="Buscar artista...",
    label_visibility="collapsed"
)

if busqueda:
    resultados = artistas_ordenados[
        artistas_ordenados["nombre"].str.contains(busqueda, case=False, na=False)
    ].copy()

    if resultados.empty:
        st.warning("No se encontró ningún artista.")
    else:
        resultados["posición"] = resultados.index + 1
        resultados["reproducciones"] = resultados["reproducciones"].apply(formatear_numero)
        resultados["oyentes"] = resultados["oyentes"].apply(formatear_numero)

        components.html(
            tabla_artistas(resultados[["posición", "nombre", "reproducciones", "oyentes"]]),
            height=600,
            scrolling=True
        )

st.divider()


# TABLA Y GRÁFICA
col1, col2 = st.columns([1.08, 0.92], gap="large")

with col1:
    st.markdown("<div class='stats-title'>Top 10 Artistas</div>", unsafe_allow_html=True)

    top10 = artistas_ordenados.head(10).copy()
    top10["reproducciones"] = top10["reproducciones"].apply(formatear_numero)
    top10["oyentes"] = top10["oyentes"].apply(formatear_numero)

    components.html(
        tabla_top(top10[["nombre", "reproducciones", "oyentes"]]),
        height=560,
        scrolling=False
    )

with col2:
    st.markdown("<div class='stats-title'>Gráfico de Popularidad</div>", unsafe_allow_html=True)

    top = artistas_ordenados.head(10).copy()
    top = top.sort_values(by="reproducciones", ascending=True)

    top["reproducciones_millones"] = top["reproducciones"] / 1_000_000

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    bars = ax.barh(
        top["nombre"],
        top["reproducciones_millones"],
        color="#ff2d95",
        height=0.62
    )

    ax.set_xlabel("Reproducciones en millones", color="#ffffff", fontsize=10)

    ax.tick_params(axis="x", colors="#d1d5db", labelsize=9)
    ax.tick_params(axis="y", colors="#ffffff", labelsize=9)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="x", color="#ffffff", alpha=0.15, linewidth=0.6)

    max_val = top["reproducciones_millones"].max()
    max_val = max_val if max_val > 0 else 1
    ax.set_xlim(0, max_val * 1.22)

    for bar, valor in zip(bars, top["reproducciones_millones"]):
        ax.text(
            bar.get_width() + max_val * 0.02,
            bar.get_y() + bar.get_height() / 2,
            f"{valor:.1f}M",
            va="center",
            color="#ffb3dc",
            fontsize=8,
            fontweight="bold"
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()



# FOTOS DE ARTISTAS
st.markdown("---")
st.markdown("<div class='stats-title'>Top 10 artistas destacados</div>", unsafe_allow_html=True)

top_cards = artistas_ordenados.head(10).copy()

cards_html = """
<style>
body {
    background: #000000;
}

.artist-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 22px;
    max-width: 1180px;
    margin: 35px auto;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

.artist-card {
    background: #0d0d0d;
    border: 1px solid rgba(236,72,153,0.35);
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 14px 34px rgba(0,0,0,0.28);
}

.artist-img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
}

.artist-placeholder {
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111827;
    color: #ec4899;
    font-size: 42px;
    font-weight: 800;
}

.artist-info {
    padding: 16px;
}

.artist-rank {
    color: #ec4899;
    font-size: 13px;
    font-weight: 800;
}

.artist-name {
    color: white;
    font-size: 17px;
    font-weight: 700;
    margin-top: 6px;
}

.artist-meta {
    color: rgba(255,255,255,0.58);
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.5;
}

.artist-link {
    display: inline-block;
    margin-top: 10px;
    color: #ffb3dc;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
}

@media (max-width: 900px) {
    .artist-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>

<div class="artist-grid">
"""

for i, row in top_cards.iterrows():
    nombre = texto_seguro(row["nombre"])
    reproducciones = formatear_numero(row["reproducciones"])
    oyentes = formatear_numero(row["oyentes"])
    imagen = str(row.get("imagen_url", "")).strip().strip('"').strip("'")
    url = str(row.get("url", "")).strip().strip('"').strip("'")

    if imagen.startswith("http"):
        imagen_html = f'<img class="artist-img" src="{html.escape(imagen)}">'
    else:
        inicial = str(nombre)[:1].upper()
        imagen_html = f'<div class="artist-placeholder">{inicial}</div>'

    if url.startswith("http"):
        enlace_html = f'<a class="artist-link" href="{html.escape(url)}" target="_blank">Ver en Last.fm</a>'
    else:
        enlace_html = ""

    cards_html += f"""
    <div class="artist-card">
        {imagen_html}
        <div class="artist-info">
            <div class="artist-rank">#{i + 1}</div>
            <div class="artist-name">{nombre}</div>
            <div class="artist-meta">
                {reproducciones} reproducciones<br>
                {oyentes} oyentes
            </div>
            {enlace_html}
        </div>
    </div>
    """

cards_html += """
</div>
"""
components.html(
    cards_html,
    height=950,
    scrolling=False
)