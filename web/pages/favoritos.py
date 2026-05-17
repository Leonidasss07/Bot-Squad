import streamlit as st
import base64
import os
import html as html_lib

from db_favoritos import (
    obtener_canciones_favoritas,
    obtener_artistas_favoritos,
    eliminar_cancion_favorita,
    eliminar_artista_favorito,
)

st.set_page_config(
    page_title="Mis Favoritos – Nova Music",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Redirigir si no hay sesión
if not st.session_state.get("usuario"):
    st.markdown("""
    <style>
    html, body, .stApp { background: #000 !important; color: #fff !important; }
    header, footer, #MainMenu, [data-testid="stToolbar"],
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 0 !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-top:120px;">
        <div style="font-size:48px; margin-bottom:18px;">★</div>
        <p style="font-size:22px; color:#ffffff; font-weight:800; letter-spacing:2px; margin-bottom:8px;">
            Inicia sesión para ver tus favoritos
        </p>
        <p style="color:rgba(255,255,255,0.45); font-size:14px; letter-spacing:1px;">
            Guarda tus canciones y artistas preferidos
        </p>
    </div>
    """, unsafe_allow_html=True)
    _, col_btn, _ = st.columns([2, 1, 2])
    with col_btn:
        if st.button("Iniciar sesión →", use_container_width=True):
            st.switch_page("pages/sesion.py")
    st.stop()

usuario = st.session_state["usuario"]

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))   # pages/
ROOT_DIR  = os.path.dirname(BASE_DIR)                    # raíz
HERO_PATH = os.path.join(ROOT_DIR, "web", "assets", "generos_bg.jpeg")

def image_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

HERO_B64 = image_to_base64(HERO_PATH)

def texto_seguro(valor):
    if valor is None or str(valor).strip() in ("", "nan"):
        return ""
    return html_lib.escape(str(valor))

# CSS y menú 
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: #000000 !important; color: #ffffff !important;
}}
header, footer, #MainMenu,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="collapsedControl"],
[data-testid="stSidebar"], [data-testid="stSidebarNav"] {{ display: none !important; }}
[data-testid="stAppViewContainer"] > .main {{ background: #000000 !important; }}
.block-container {{
    max-width: 100% !important; padding-top: 0 !important;
    padding-bottom: 2rem !important; padding-left: 2rem !important; padding-right: 2rem !important;
}}
hr {{ border: none !important; border-top: 1px solid rgba(255,255,255,0.08) !important; margin: 1.8rem 0 !important; }}

.menu-superior {{
    display: flex; justify-content: center; align-items: center;
    gap: 42px; height: 240px; width: 100vw; margin-left: calc(50% - 50vw);
    background-image:
        linear-gradient(to right, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to left,  rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.95)),
        url("data:image/jpeg;base64,{HERO_B64}");
    background-size: cover; background-position: center top;
    position: relative; z-index: 10;
}}
.menu-superior a {{
    color: white; text-decoration: none; font-size: 16px; font-weight: 800;
    letter-spacing: 3px; font-family: "Century Gothic","Montserrat","Segoe UI",Arial,sans-serif;
    text-transform: uppercase; transform: translateY(42px);
    text-shadow: 0 3px 12px rgba(0,0,0,0.85);
}}
.menu-superior a:hover {{ color: #AFCFCF; }}

.fav-hero {{ text-align: center; padding: 40px 48px 24px; }}
.fav-hero-title {{ font-size: 44px; font-weight: 900; color: #ffffff; letter-spacing: -1px; }}
.fav-hero-sub {{ color: rgba(255,255,255,0.55); font-size: 15px; margin-top: 8px; letter-spacing: 1px; }}
.fav-user-badge {{
    display: inline-block; margin-top: 14px;
    background: rgba(175,207,207,0.12); border: 1px solid rgba(175,207,207,0.35);
    border-radius: 30px; padding: 7px 22px; font-size: 13px; font-weight: 700;
    color: #AFCFCF; letter-spacing: 1px;
}}

.fav-song-card {{
    background: #0d0d0d; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px; padding: 14px; margin-bottom: 14px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.10); transition: transform 0.16s ease;
}}
.fav-song-card:hover {{ transform: translateY(-2px); box-shadow: 0 16px 34px rgba(0,0,0,0.18); }}
.fav-song-layout {{ display: flex; justify-content: space-between; align-items: center; gap: 14px; }}
.fav-song-content {{ flex: 1; min-width: 0; }}
.fav-song-name {{ font-weight: 800; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #ffffff; }}
.fav-song-artist {{ color: #b5b9c2; font-size: 14px; margin-top: 4px; }}
.fav-song-meta {{ color: #9ca3af; font-size: 12px; margin-top: 6px; }}
.fav-song-cover {{
    width: 88px; height: 88px; border-radius: 16px; overflow: hidden; flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.08); background: #111;
    display: flex; align-items: center; justify-content: center;
}}
.fav-song-cover img {{ width:100%; height:100%; object-fit:cover; }}
.fav-cover-placeholder {{ font-size:22px; font-weight:800; color:#475569; }}
.fav-link-btn {{
    display: inline-block; margin-top: 10px;
    background: linear-gradient(135deg,#DCE8D8 0%,#AFCFCF 100%);
    color: #111827 !important; text-decoration: none !important;
    border-radius: 10px; padding: 6px 12px; font-size: 12px; font-weight: 760;
    border: 1px solid #AFCFCF;
}}

.fav-artist-card {{
    background: #0d0d0d; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px; padding: 18px 20px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 16px; transition: transform 0.16s ease;
}}
.fav-artist-card:hover {{ transform: translateY(-2px); box-shadow: 0 16px 34px rgba(0,0,0,0.18); }}
.fav-artist-avatar {{
    width: 68px; height: 68px; border-radius: 50%; overflow: hidden; flex-shrink: 0;
    border: 2px solid rgba(255,255,255,0.12); background: #111;
    display: flex; align-items: center; justify-content: center;
}}
.fav-artist-avatar img {{ width:100%; height:100%; object-fit:cover; }}
.fav-artist-initial {{ font-size:22px; font-weight:800; color:#475569; }}
.fav-artist-info {{ flex:1; min-width:0; }}
.fav-artist-name {{ font-size:17px; font-weight:800; color:#ffffff; }}
.fav-artist-meta {{ color:#9ca3af; font-size:13px; margin-top:3px; }}

.empty-state {{ text-align:center; padding:70px 20px; color:rgba(255,255,255,0.28); }}
.empty-state-icon {{ font-size:52px; margin-bottom:14px; }}
.empty-state-text {{ font-size:15px; font-weight:600; letter-spacing:1px; line-height:1.6; }}

[data-testid="stAudio"] {{
    background: transparent !important; border: none !important;
    padding: 0 !important; margin-top: 6px; margin-bottom: 6px;
}}
[data-testid="stAudio"] audio {{ width:100%; height:36px; border-radius:20px; filter:grayscale(1) brightness(0.85); }}
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

st.markdown(f"""
<div class="fav-hero">
    <div class="fav-hero-title">Mis Favoritos</div>
    <div class="fav-hero-sub">Tu colección personal de música guardada</div>
    <div class="fav-user-badge">★ {html_lib.escape(usuario)}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

canciones_fav = obtener_canciones_favoritas(usuario)
artistas_fav  = obtener_artistas_favoritos(usuario)

tab_c, tab_a = st.tabs([
    f"Canciones  ({len(canciones_fav)})",
    f"Artistas  ({len(artistas_fav)})",
])

# Canciones
with tab_c:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if not canciones_fav:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">♪</div>
            <div class="empty-state-text">
                Aún no tienes canciones guardadas.<br>
                Ve a <strong style="color:#AFCFCF">Géneros</strong> y pulsa ☆ en las que te gusten.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(2, gap="large")
        for i, cancion in enumerate(canciones_fav):
            nombre  = texto_seguro(cancion.get("nombre", ""))
            artista = texto_seguro(cancion.get("artista", ""))
            imagen  = cancion.get("imagen_url", "") or ""
            url     = cancion.get("url", "") or ""
            audio   = cancion.get("audio_url", "") or ""
            genero  = texto_seguro(cancion.get("genero", ""))
            repro   = cancion.get("reproducciones", "") or ""

            cover_html = (
                f'<div class="fav-song-cover"><img src="{html_lib.escape(imagen)}"></div>'
                if imagen.startswith("http") else
                f'<div class="fav-song-cover"><div class="fav-cover-placeholder">{nombre[:1].upper() or "♪"}</div></div>'
            )
            link_btn = (
                f'<a class="fav-link-btn" href="{html_lib.escape(url)}" target="_blank">Ver en Last.fm</a>'
                if url.startswith("http") else ""
            )
            meta_parts = []
            if genero:
                meta_parts.append(genero.upper())
            if repro and repro not in ("nan", ""):
                try:
                    v = float(repro)
                    meta_parts.append(f"{v/1_000_000:.1f}M reprod." if v >= 1_000_000 else f"{int(v):,} reprod.")
                except Exception:
                    pass

            with cols[i % 2]:
                st.markdown(f"""
                <div class="fav-song-card">
                    <div class="fav-song-layout">
                        <div class="fav-song-content">
                            <div class="fav-song-name">{nombre}</div>
                            <div class="fav-song-artist">{artista}</div>
                            <div class="fav-song-meta">{" · ".join(meta_parts)}</div>
                            {link_btn}
                        </div>
                        {cover_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if audio.startswith("http"):
                    st.audio(audio, format="audio/mp3")

                if st.button("🗑 Quitar", key=f"del_c_{i}", help="Eliminar de favoritos"):
                    eliminar_cancion_favorita(usuario, cancion["nombre"], cancion.get("artista", ""))
                    st.rerun()

# Artistas
with tab_a:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if not artistas_fav:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🎤</div>
            <div class="empty-state-text">
                Aún no tienes artistas guardados.<br>
                Ve a <strong style="color:#AFCFCF">Artistas</strong> y guarda tus favoritos.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols2 = st.columns(2, gap="large")
        for i, artista in enumerate(artistas_fav):
            nombre  = texto_seguro(artista.get("nombre", ""))
            imagen  = artista.get("imagen_url", "") or ""
            url     = artista.get("url", "") or ""
            oyentes = artista.get("oyentes", "") or ""

            avatar_html = (
                f'<div class="fav-artist-avatar"><img src="{html_lib.escape(imagen)}"></div>'
                if imagen.startswith("http") else
                f'<div class="fav-artist-avatar"><div class="fav-artist-initial">{nombre[:1].upper() or "?"}</div></div>'
            )
            link_btn = (
                f'<a class="fav-link-btn" href="{html_lib.escape(url)}" target="_blank">Ver en Last.fm</a>'
                if url.startswith("http") else ""
            )
            meta_oyentes = ""
            if oyentes and oyentes not in ("nan", ""):
                try:
                    v = float(oyentes)
                    meta_oyentes = f"{v/1_000_000:.1f}M oyentes" if v >= 1_000_000 else f"{int(v):,} oyentes"
                except Exception:
                    meta_oyentes = str(oyentes)

            with cols2[i % 2]:
                st.markdown(f"""
                <div class="fav-artist-card">
                    {avatar_html}
                    <div class="fav-artist-info">
                        <div class="fav-artist-name">{nombre}</div>
                        <div class="fav-artist-meta">{meta_oyentes}</div>
                        {link_btn}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🗑 Quitar", key=f"del_a_{i}", help="Eliminar de favoritos"):
                    eliminar_artista_favorito(usuario, artista["nombre"])
                    st.rerun()

st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:12px 0 8px;">
    <span style="color:rgba(255,255,255,0.25); font-size:13px; letter-spacing:2px;">
        NOVA MUSIC★ · {html_lib.escape(usuario)}
    </span>
</div>
""", unsafe_allow_html=True)