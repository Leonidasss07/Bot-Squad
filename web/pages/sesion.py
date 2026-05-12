import streamlit as st
import base64
import os

from db import crear_usuario, iniciar_sesion, guardar_codigo_recuperacion, verificar_codigo, cambiar_password
from email_utils import enviar_codigo
from utils_loader import mostrar_loader

st.set_page_config(page_title="Sesión - Nova music", layout="wide")
loader = mostrar_loader(1)

def get_base64_image(path):
    if not os.path.exists(path): return ""
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

path_bg = os.path.join(BASE_DIR, "..", "assets", "sesion_bg.jpeg")
path_banner = os.path.join(BASE_DIR, "..", "assets", "image_3857d6.jpg") 

img_bg = get_base64_image(path_bg)
img_banner = get_base64_image(path_banner)

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.85)), url("data:image/jpeg;base64,{img_bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

header {{ visibility: hidden; }}
[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ padding: 0 !important; }}

.top-menu {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 40px;
    height: 80px;
    padding-bottom: 20px;
    background-image: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.9)), url("data:image/jpeg;base64,{img_banner}");
    background-size: cover;
    background-position: center;
    width: 100%;
    margin-bottom: 5px;
}}

.logo-text {{
    position: absolute; left: 40px; bottom: 20px;
    font-size: 22px; font-weight: bold; color: rgba(255,255,255,0.7); letter-spacing: 3px;
}}

.top-menu a {{
    color: white; text-decoration: none; font-weight: bold; font-size: 16px; text-transform: uppercase;
}}

/* Contenedor Principal */
.main-center-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}}

/* Forzar ancho unificado en el bloque de formulario */
[data-testid="stForm"] {{
    border: none !important;
    width: 450px !important;
    background-color: transparent !important;
    padding: 0 !important;
}}

/* Alineación de Radio Buttons */
div[data-testid="stRadio"] {{
    background-color: transparent !important;
    margin-bottom: 20px;
}}

div[role="radiogroup"] {{
    flex-direction: row !important;
    justify-content: space-between !important;
    gap: 10px !important;
}}

/* Estilo de Inputs */
input {{
    background-color: #1e1e1e !important;
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 8px !important;
}}

/* Botón de envío */
[data-testid="stFormSubmitButton"] button {{
    width: 100% !important;
    background-color: #111 !important;
    border: 1px solid #555 !important;
    color: white !important;
    border-radius: 8px !important;
    height: 45px;
    font-weight: bold;
    margin-top: 10px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="top-menu">
    <div class="logo-text">NOVA MUSIC ★</div>
    <a href="/" target="_self">INICIO</a>
    <a href="/dashboard" target="_self">DASHBOARD</a>
    <a href="/canciones" target="_self">CANCIONES</a>
    <a href="/artistas" target="_self">ARTISTAS</a>
    <a href="/generos" target="_self">GÉNEROS</a>
</div>
""", unsafe_allow_html=True)

loader.empty()

st.markdown('<div class="main-center-wrapper">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<h2 style='text-align: center-wrapper;'>Cuenta de usuario</h2>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        opcion = st.radio(
            "Elige una opción", 
            ["Iniciar sesión", "Crear cuenta", "Olvidé mi contraseña"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("")
        
        correo = st.text_input("Correo", placeholder="ejemplo@correo.com")
        password = st.text_input("Contraseña", type="password")
        
        submit = st.form_submit_button("Confirmar")
        
        if submit:
            if opcion == "Iniciar sesión":
                usuario = iniciar_sesion(correo, password)
                if usuario:
                    st.session_state.usuario = correo
                    st.switch_page("app.py")
                else:
                    st.error("Credenciales incorrectas")
            elif opcion == "Crear cuenta":
                if crear_usuario(correo, password):
                    st.success("Cuenta creada")
                else:
                    st.error("Error al crear cuenta")

st.markdown('</div>', unsafe_allow_html=True)