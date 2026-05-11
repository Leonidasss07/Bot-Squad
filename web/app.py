import streamlit as st
import base64
from pathlib import Path
import streamlit.components.v1 as components
import random 

st.set_page_config(
    page_title="Nova music",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

def imagen_local(nombre):
    archivo = ASSETS_DIR / nombre

    if not archivo.exists():
        st.error(f"No encontré la imagen: {archivo}")
        st.stop()

    with open(archivo, "rb") as img:
        return base64.b64encode(img.read()).decode()

if not ASSETS_DIR.exists():
    st.error(f"No existe la carpeta assets en: {ASSETS_DIR}")
    st.stop()


imagen_lema = imagen_local("lema.jpg")
imagen_grafica = imagen_local("grafica.jpg")
imagen_nueva = imagen_local("angeles.jpg")
imagen_nueva2 = imagen_local("favoritos.jpg")
imagen_nueva3 = imagen_local("audifonos.jpg")
imagen_nueva4 = imagen_local("corazon.jpg")
imagen_nueva5 = imagen_local("flecha.jpg")
imagen_anuncio = imagen_local("anuncio.jpg")
imagen_dashboard = imagen_local("bts.jpg")
imagen_canciones = imagen_local("peso.jpg")
imagen_artistas = imagen_local("kanye.jpg")
imagen_generos = imagen_local("un_verano_sin_ti.jpg")

if "menu" not in st.session_state:
    st.session_state.menu = "Inicio"

st.markdown("""
<style>
html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: black !important;
    overflow-x: hidden;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.block-container,
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stElementContainer"] {
    background: black !important;
}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer,
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

section.main > div {
    padding-top: 0 !important;
}

.hero {
    width: 110vw;
    height: 105vh;
    margin-top: -120px;
    margin-left: -5vw;
    position: relative;
    overflow: hidden;
}

.hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    position: absolute;
    inset: 0;
    filter: brightness(1) !important;
    opacity: 0;
    animation: cambiarHero 20s infinite;
}

.hero img:nth-child(1) {
    animation-delay: 0s;
}

.hero img:nth-child(2) {
    animation-delay: 4s;
}

.hero img:nth-child(3) {
    animation-delay: 8s;
}
            
.hero img:nth-child(4) {
    animation-delay: 12s;
}

.hero img:nth-child(5) {
    animation-delay: 16s;
}

@keyframes cambiarHero {
    0% { opacity: 0; }
    10% { opacity: 1; }
    45% { opacity: 1; }
    55% { opacity: 0; }
    100% { opacity: 0; }
}

.logo-hero {
    position: absolute;
    top: 40px;
    left: 40px;
    z-index: 5;
    color: white;
    font-size: 14px;
    font-weight: 300;
    letter-spacing: 6px;
    font-family: "Century Gothic", "Montserrat", "Avenir Next", "Segoe UI", Arial, sans-serif;
    text-transform: uppercase;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.logo-hero .star {
    font-size: 18px;
    margin-left: 6px;
    vertical-align: -1px;
}

.texto-hero {
    position: absolute;
    bottom: 80px;
    left: 60px;
    z-index: 5;
    color: white;
    font-size: 45px;
    font-weight: 900;
    font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
    text-shadow: 0 4px 18px rgba(0,0,0,0.8);
}

.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0) 70%,
        rgba(0,0,0,0.4) 80%,
        rgba(0,0,0,0.9) 100%
    );
}

.explora {
    padding: 50px;
}

.explora h3 {
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.album-generos {
    width: 170px;
    height: 170px;
    border-radius: 22px;
    overflow: hidden;
    display: block;
    margin: auto;
    box-shadow: 0 14px 32px rgba(0,0,0,0.6);
    transition: 0.3s ease;
}

.album-generos:hover {
    transform: scale(1.08);
}

.album-generos img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.boton-texto {
    text-align: center;
    color: white;
    font-size: 18px;
    font-weight: 700;
    margin-top: 10px;
}

.banner-anuncio {
    width: 92%;
    height: 260px;
    border-radius: 20px;
    overflow: hidden;
    margin: 40px auto;
}

.banner-anuncio img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.boton-login {
    position: fixed;
    top: 35px;
    right: 45px;
    z-index: 9999;
}

.boton-login a {
    color: white;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 3px;
    font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
    text-transform: uppercase;
    padding: 10px 18px;
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 30px;
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(8px);
}

.boton-login a:hover {
    background: white;
    color: black;
}
</style>

<div class="boton-login">
    <a href="/sesion" target="_self">INICIA SESIÓN</a>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="hero">
    <img src="data:image/jpeg;base64,{imagen_nueva}">
    <img src="data:image/jpeg;base64,{imagen_nueva2}">
    <img src="data:image/jpeg;base64,{imagen_nueva3}">
    <img src="data:image/jpeg;base64,{imagen_nueva4}">
    <img src="data:image/jpeg;base64,{imagen_nueva5}">
    <div class="logo-hero">NOVA MUSIC<span class="star">★</span></div>
    <div class="texto-hero"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div style="margin: 55px">
        <img src="data:image/jpg;base64,{imagen_lema}" 
             style="width:60%; border-radius:15px;">
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="margin-top:90px; text-align:center;">
        <p style="
            color:white; 
            font-weight:800; 
            font-size:20px;
            margin-bottom:15px;">
            Recomendaciones
        </p>
    </div>
    """, unsafe_allow_html=True)

    playlists = [
        "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI",  # Top global
        "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj",  # Pop
        "PLS_oEMUyvA728O0r3rW0U2Y9d2z6kQ6Jt",  # Latino
        "PL4fGSI1pDJn5kI81J1fYWK5eZRl1zJ5kM"   # Variado
    ]

    playlist = random.choice(playlists)

    components.html(f"""
    <iframe width="100%" height="300"
        src="https://www.youtube.com/embed/videoseries?list={playlist}"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        style="border-radius:25px;">
    </iframe>
    """, height=320)

st.markdown("""
<div class="explora" style="margin-top:-80px;">
    <h3>Explora</h3>
</div>
""", unsafe_allow_html=True)

columnas = st.columns(4)

with columnas[0]:
    st.markdown(f"""
    <a href="/dashboard" target="_self" class="album-generos">
        <img src="data:image/jpg;base64,{imagen_dashboard}">
    </a>
    <div class="boton-texto">Dashboard</div>
    """, unsafe_allow_html=True)

with columnas[1]:
    st.markdown(f"""
    <a href="/canciones" target="_self" class="album-generos">
        <img src="data:image/jpg;base64,{imagen_canciones}">
    </a>
    <div class="boton-texto">Canciones</div>
    """, unsafe_allow_html=True)

with columnas[2]:
    st.markdown(f"""
    <a href="/artistas" target="_self" class="album-generos">
        <img src="data:image/jpg;base64,{imagen_artistas}">
    </a>
    <div class="boton-texto">Artistas</div>
    """, unsafe_allow_html=True)
    
with columnas[3]:
    st.markdown(f"""
    <a href="/generos" target="_self" class="album-generos">
        <img src="data:image/jpg;base64,{imagen_generos}">
    </a>
    <div class="boton-texto">Géneros</div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="banner-anuncio">
    <img src="data:image/jpeg;base64,{imagen_anuncio}">
</div>
""", unsafe_allow_html=True)