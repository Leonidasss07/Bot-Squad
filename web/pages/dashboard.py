import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import base64
from pathlib import Path

def imagen_local(nombre):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ruta = BASE_DIR / "assets" / nombre
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()

imagen_dashboard_bg = imagen_local("dashboard.jpg")

# CONFIG
st.set_page_config(page_title="Proyecto Musical", layout="wide")

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
    align-items: center;
    gap: 40px;

    height: 240px;
    margin-top: -55px;

    width: 100vw;
    margin-left: calc(-50vw + 50%);

    background-image:
        linear-gradient(to right, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to left, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.95)),
        url("data:image/jpeg;base64,{imagen_dashboard_bg}");

    background-size: cover;
    background-position: center;
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
    transform: translateY(40px);
}}

.menu-superior a:hover {{
    color: #3b82f6;
}}

h1 {{
    display: none !important;
}}

h2 {{
    font-size: 24px !important;
    color: white !important;
    font-weight: 800 !important;
    letter-spacing: 1.5px;
    text-align: center;
    border: none !important;
    padding: 4px 0;
    width: fit-content;
    margin: 20px auto 20px auto !important;
    text-shadow: 0 0 12px rgba(255,255,255,0.25);
}}

[data-testid="stCaptionContainer"] {{
    color: rgba(255,255,255,0.75) !important;
    text-align: center;
    font-size: 12px !important;
    margin-top: 10px !important;
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
    width: 92%;
    margin: 20px auto 45px auto;
    padding: 28px 34px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(2,6,23,0.95));
    border: 1px solid rgba(37,99,235,0.45);
    box-shadow: 0 0 35px rgba(37,99,235,0.12);
}}

.cancion-card h2 {{
    margin: 0 0 24px 0 !important;
    font-size: 25px !important;
    text-align: left !important;
    width: 100%;
}}

.cancion-content {{
    display: flex;
    align-items: center;
    gap: 28px;
}}

.portada-fake {{
    width: 210px;
    height: 210px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(37,99,235,0.35), rgba(15,23,42,0.95));
    border: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.75);
    font-weight: 700;
    letter-spacing: 1px;
}}

.cancion-info h3 {{
    color: white;
    font-size: 30px;
    margin: 0 0 14px 0;
}}

.cancion-info p {{
    color: rgba(255,255,255,0.88);
    font-size: 16px;
    margin: 10px 0;
}}

.cancion-boton {{
    display: inline-block;
    margin-top: 18px;
    padding: 11px 18px;
    border-radius: 12px;
    background: #1e3a8a;
    color: white !important;
    text-decoration: none;
    font-weight: 700;
}}

.cancion-boton:hover {{
    background: #2563eb;
}}

html, body, .stApp {{
    background-color: black;
    color: white;
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

    plt.style.use('dark_background')
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

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_alpha(0.25)
    ax.spines['left'].set_alpha(0.25)

    plt.tight_layout()
    st.pyplot(fig)

artistas_ordenadas = artistas.sort_values(by="oyentes", ascending=False)

with col_artistas:
    st.subheader("Top 10 Artistas")

    df = artistas_ordenadas.head(10).copy()
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    if "reproducciones" in df.columns:
        df = df.drop(columns=["reproducciones"])

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

portada_html = ""
if "imagen_url" in top_1 and pd.notna(top_1["imagen_url"]) and top_1["imagen_url"] != "":
    portada_html = f'<img src="{top_1["imagen_url"]}" style="width:210px;height:210px;object-fit:cover;border-radius:18px;">'
else:
    portada_html = '<div class="portada-fake">SIN PORTADA</div>'

url_boton = ""
if "url" in top_1:
    url_boton = f'<a class="cancion-boton" href="{top_1["url"]}" target="_blank">Escuchar en Last.fm</a>'

reproducciones_formato = f"{top_1['reproducciones']:,.0f}"

st.markdown(f"""
<div class="cancion-card">
    <h2>Canción más escuchada</h2>
    <div class="cancion-content">
        {portada_html}
        <div class="cancion-info">
            <h3>{top_1['nombre']}</h3>
            <p><strong>Artista:</strong> {top_1['artista']}</p>
            <p><strong>Reproducciones:</strong> {reproducciones_formato}</p>
            {url_boton}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)