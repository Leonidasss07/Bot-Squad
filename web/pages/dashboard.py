import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import base64

from pathlib import Path
from utils_loader import mostrar_loader


def imagen_local(nombre):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ruta = BASE_DIR / "assets" / nombre
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()


imagen_dashboard_bg = imagen_local("dashboard.jpg")

# CONFIG
st.set_page_config(page_title="Proyecto Musical", layout="wide")
loader = mostrar_loader(1)

# =========================
# MENÚ SUPERIOR
# =========================
st.markdown(f"""
<style>
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer {{
    display: none !important;
}}

header[data-testid="stHeader"] {{
    display: none !important;
}}

.block-container {{
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    padding-top: 0rem !important;
}}

.menu-superior {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 40px;

    height: 400px;
    padding-bottom: 58px;
    margin-top: 0;

    width: 100vw;
    margin-left: calc(-50vw + 50%);

    background-image:
        linear-gradient(to right, rgba(0,0,0,0.70), rgba(0,0,0,0) 22%),
        linear-gradient(to left, rgba(0,0,0,0.70), rgba(0,0,0,0) 22%),
        linear-gradient(
            to bottom,
            rgba(0,0,0,0) 0%,
            rgba(0,0,0,0) 78%,
            rgba(0,0,0,0.35) 88%,
            rgba(0,0,0,0.75) 95%,
            rgba(0,0,0,1) 100%
        ),
        url("data:image/jpeg;base64,{imagen_dashboard_bg}");

    background-size: 100% auto;
    background-position: absolute;
    background-repeat: no-repeat;

    position: relative;
    z-index: 9999;
}}

.menu-superior a {{
    color: white;
    text-decoration: none;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 3px;
    font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
    text-transform: uppercase;
    transform: none;
    text-shadow: 0 3px 12px rgba(0,0,0,0.85);
}}

.menu-superior a:hover {{
    color: #AFCFCF;
}}

h1 {{
    display: none !important;
}}

h2 {{
    font-size: 28px !important;
    color: white !important;
    font-weight: 900 !important;
    letter-spacing: 1.5px;
    text-align: center;
    border: none !important;
    padding: 4px 0;
    width: fit-content;
    margin: 34px auto 20px auto !important;
    text-shadow: 0 0 12px rgba(255,255,255,0.25);
}}

[data-testid="stCaptionContainer"] {{
    color: rgba(255,255,255,0.72) !important;
    text-align: center;
    font-size: 12px !important;
    margin-top: 8px !important;
    margin-bottom: 24px !important;
}}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {{
    max-width: 900px;
    margin: 0 auto 25px auto !important;
    gap: 18px !important;
}}

[data-testid="stMetric"] {{
    text-align: center;
    border: 1.5px solid rgba(37, 99, 235, 0.75);
    border-radius: 14px;
    padding: 12px 8px;
    background: rgba(15, 23, 42, 0.35);
}}

[data-testid="stMetricLabel"] {{
    color: rgba(255,255,255,0.88) !important;
    font-size: 11px !important;
    justify-content: center !important;
}}

[data-testid="stMetricValue"] {{
    color: white !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}}

.tabla-artistas {{
    width: 82%;
    margin: 0 auto;
    border-collapse: collapse;
    color: white;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 14px;
}}

.tabla-artistas th {{
    background: #111827;
    color: white;
    padding: 13px 14px;
    text-align: left;
    border-bottom: 1px solid #2563eb;
}}

.tabla-artistas td {{
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}

.tabla-artistas tr:hover {{
    background: rgba(37,99,235,0.12);
}}

.tabla-artistas th:first-child {{
    border-top-left-radius: 8px;
}}

.tabla-artistas th:last-child {{
    border-top-right-radius: 8px;
}}

.cancion-card {{
    width: 100%;
    margin: 10px 0 6px 0;
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    background: #1a1a2e;
    box-shadow: 0 8px 32px rgba(0,0,0,0.55);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.cancion-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.7);
}}

.cancion-bg {{
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    filter: blur(18px) brightness(0.55) saturate(1.4);
    transform: scale(1.08);
    z-index: 0;
}}

.cancion-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(
        135deg,
        rgba(0,0,0,0.15) 0%,
        rgba(0,0,0,0.45) 100%
    );
    z-index: 1;
}}

.cancion-card h2 {{
    position: relative;
    z-index: 2;
    margin: 0 !important;
    font-size: 16px !important;
    text-align: right !important;
    width: 100%;
    color: rgba(255,255,255,0.55) !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    text-shadow: none !important;
    padding: 14px 16px 0 16px;
}}

.cancion-content {{
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 0;
    padding: 0;
    min-height: 155px;
}}

.cancion-cover-wrap {{
    flex-shrink: 0;
    width: 155px;
    align-self: stretch;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.cancion-cover-wrap img {{
    width: 155px;
    height: 155px;
    object-fit: cover;
    display: block;
    border-radius: 0;
    margin: auto;
}}

.portada-fake {{
    width: 155px;
    height: 155px;
    background: linear-gradient(135deg, rgba(37,99,235,0.5), rgba(15,23,42,0.95));
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.6);
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 1px;
}}

.cancion-info {{
    flex: 1;
    padding: 18px 18px 18px 18px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.cancion-label {{
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.5);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.cancion-info h3 {{
    color: white;
    font-size: 22px;
    font-weight: 900;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
    line-height: 1.1;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}}

.cancion-info .artista {{
    color: rgba(255,255,255,0.65);
    font-size: 13px;
    font-weight: 600;
    margin: 0 0 8px 0;
}}

.cancion-info .repro {{
    color: rgba(255,255,255,0.4);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
}}

.cancion-boton {{
    display: none;
}}

html, body, .stApp {{
    background-color: black;
    color: white;
}}

[data-testid="stAudio"] {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 10px 0 4px 0 !important;
}}

[data-testid="stAudio"] audio {{
    width: 100%;
    height: 38px;
    border-radius: 20px;
    filter: grayscale(1) brightness(0.75);
}}
</style>

<div class="menu-superior">
    <a href="/" target="_self">INICIO</a>
    <a href="/dashboard" target="_self">DASHBOARD</a>
    <a href="/canciones" target="_self">CANCIONES</a>
    <a href="/artistas" target="_self">ARTISTAS</a>
    <a href="/generos" target="_self">GENEROS</a>
    <a href="/favoritos" target="_self">FAVORITOS</a>
</div>
""", unsafe_allow_html=True)


st.title("Dashboard")

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

mes_actual = meses[datetime.now().month]

st.caption(f"Última sincronización con Last.fm: {mes_actual}")

loader.empty()

try:
    canciones = pd.read_csv("data/clean/canciones_populares.csv")
    artistas = pd.read_csv("data/clean/artistas_populares.csv")
    generos = pd.read_csv("data/clean/generos_canciones.csv")
    julio = pd.read_csv("data/clean/canciones_julio.csv")
except FileNotFoundError:
    st.error("Error al cargar los datos. Revisa que los CSV existan.")
    st.stop()

st.header("Resumen general")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Canciones", len(canciones))
col2.metric("Artistas", len(artistas))
col3.metric("Géneros", len(generos))
col4.metric("Canciones de julio", len(julio))

st.write("---")

col_tabla, col_artistas = st.columns(2, gap="large")

with col_tabla:
    st.subheader("Top 10 Géneros")

    conteo_generos = generos["generos"].value_counts().head(10)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6))

    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    ax.barh(conteo_generos.index, conteo_generos.values, color="#3b82f6")
    ax.invert_yaxis()

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    ax.grid(axis="x", color="white", alpha=0.15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_alpha(0.25)
    ax.spines["left"].set_alpha(0.25)

    plt.tight_layout()
    st.pyplot(fig)

artistas_ordenadas = artistas.sort_values(by="oyentes", ascending=False)

with col_artistas:
    st.subheader("Top 10 Artistas")

    df = artistas_ordenadas.head(10).copy()
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    columnas_ocultar = ["reproducciones", "imagen_url"]

    for columna in columnas_ocultar:
        if columna in df.columns:
            df = df.drop(columns=[columna])

    tabla_html = df.to_html(
        classes="tabla-artistas",
        escape=False,
        index=False
    )

    st.markdown(tabla_html, unsafe_allow_html=True)

st.write("---")

canciones["reproducciones"] = pd.to_numeric(
    canciones["reproducciones"], errors="coerce"
)

canciones_top = canciones.sort_values(by="reproducciones", ascending=False)
top_1 = canciones_top.iloc[0]
top_2 = canciones_top.iloc[1] if len(canciones_top) > 1 else None

# Formato de reproducciones
reproducciones_formato = f"{top_1['reproducciones']:,.0f}"
reproducciones_formato_2 = f"{top_2['reproducciones']:,.0f}" if top_2 is not None else ""

# Dos cards en columnas
col_c1, col_c2 = st.columns(2, gap="large")

with col_c1:
    if "imagen_url" in top_1 and pd.notna(top_1["imagen_url"]) and top_1["imagen_url"] != "":
        img1 = top_1["imagen_url"]
        cover1 = f'<div class="cancion-cover-wrap"><img src="{img1}" style="width:155px;height:155px;object-fit:cover;display:block;"></div>'
        bg1 = f'<div class="cancion-bg" style="background-image:url({img1});"></div>'
    else:
        cover1 = '<div class="cancion-cover-wrap"><div class="portada-fake">SIN PORTADA</div></div>'
        bg1 = '<div class="cancion-bg" style="background:#0f172a;"></div>'

    st.markdown(f"""
    <div class="cancion-card">
        {bg1}
        <div class="cancion-overlay"></div>
        <h2>Más escuchada</h2>
        <div class="cancion-content">
            {cover1}
            <div class="cancion-info">
                <div class="cancion-label">Artista</div>
                <div style="color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;margin-bottom:6px;">{top_1['artista']}</div>
                <h3>{top_1['nombre']}</h3>
                <div class="repro">{reproducciones_formato} reproducciones</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    audio_top1 = str(top_1.get("audio_url", "")).strip()

    if audio_top1.startswith("http"):
        st.audio(audio_top1, format="audio/mp3")
    else:
        st.caption("Audio no disponible")

with col_c2:
    if top_2 is not None:
        if "imagen_url" in top_2 and pd.notna(top_2["imagen_url"]) and top_2["imagen_url"] != "":
            img2 = top_2["imagen_url"]
            cover2 = f'<div class="cancion-cover-wrap"><img src="{img2}" style="width:155px;height:155px;object-fit:cover;display:block;"></div>'
            bg2 = f'<div class="cancion-bg" style="background-image:url({img2});"></div>'
        else:
            cover2 = '<div class="cancion-cover-wrap"><div class="portada-fake">SIN PORTADA</div></div>'
            bg2 = '<div class="cancion-bg" style="background:#0f172a;"></div>'

        st.markdown(f"""
        <div class="cancion-card">
            {bg2}
            <div class="cancion-overlay"></div>
            <h2>Trending</h2>
            <div class="cancion-content">
                {cover2}
                <div class="cancion-info">
                    <div class="cancion-label">Artista</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:13px;font-weight:600;margin-bottom:6px;">{top_2['artista']}</div>
                    <h3>{top_2['nombre']}</h3>
                    <div class="repro">{reproducciones_formato_2} reproducciones</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        audio_top2 = str(top_2.get("audio_url", "")).strip()

        if audio_top2.startswith("http"):
            st.audio(audio_top2, format="audio/mp3")
        else:
            st.caption("Audio no disponible")