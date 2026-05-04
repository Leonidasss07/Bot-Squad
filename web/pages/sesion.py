import streamlit as st
from db import (
    crear_usuario,
    iniciar_sesion,
    guardar_codigo_recuperacion,
    verificar_codigo,
    cambiar_password
)
from email_utils import enviar_codigo

st.set_page_config(
    page_title="Sesión - Nova music",
    layout="centered"
)

st.markdown("""
<style>
html, body, .stApp {
    background-color: black !important;
    color: white !important;
}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stAppViewContainer"],
[data-testid="stSidebar"] {
    background: black !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3, p, label, span, div {
    color: white !important;
}

input {
    background-color: #1e1e1e !important;
    color: white !important;
    border: 1px solid white !important;
}

button {
    background-color: #111 !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #555 !important;
}

button:hover {
    background-color: #222 !important;
}

/* Radio buttons bien blancos */
div[role="radiogroup"] label,
div[role="radiogroup"] label span,
div[role="radiogroup"] div,
.stRadio label,
.stRadio span {
    color: white !important;
    opacity: 1 !important;
}

.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario:
    st.switch_page("app.py")

st.markdown("## Cuenta de usuario")

opcion = st.radio(
    "Elige una opción",
    ["Iniciar sesión", "Crear cuenta", "Olvidé mi contraseña"],
    horizontal=True
)

if opcion in ["Iniciar sesión", "Crear cuenta"]:
    correo = st.text_input("Correo")
    password = st.text_input("Contraseña", type="password")

    if opcion == "Crear cuenta":
        if st.button("Crear cuenta"):
            if crear_usuario(correo, password):
                st.session_state.usuario = correo
                st.success("Cuenta creada correctamente")
                st.switch_page("app.py")
            else:
                st.error("Ese correo ya existe")

    if opcion == "Iniciar sesión":
        if st.button("Iniciar sesión"):
            usuario = iniciar_sesion(correo, password)

            if usuario:
                st.session_state.usuario = correo
                st.success(f"Bienvenido, {correo}")
                st.switch_page("app.py")
            else:
                st.error("Correo o contraseña incorrectos")

if opcion == "Olvidé mi contraseña":
    st.markdown("### Restablecer contraseña")

    correo_recuperacion = st.text_input("Correo de tu cuenta")

    if st.button("Enviar código"):
        codigo = guardar_codigo_recuperacion(correo_recuperacion)

        if codigo:
            st.session_state.correo_recuperacion = correo_recuperacion

            try:
                enviar_codigo(correo_recuperacion, codigo)
                st.success("Te enviamos un código a tu correo.")
            except Exception as e:
                st.error(f"No se pudo enviar el correo: {e}")
        else:
            st.error("No existe una cuenta con ese correo")

    codigo_usuario = st.text_input("Código recibido")
    nueva_password = st.text_input("Nueva contraseña", type="password")
    repetir_password = st.text_input("Repite la nueva contraseña", type="password")

    if st.button("Cambiar contraseña"):
        if "correo_recuperacion" not in st.session_state:
            st.error("Primero debes enviar un código")
        elif nueva_password != repetir_password:
            st.error("Las contraseñas no coinciden")
        elif verificar_codigo(st.session_state.correo_recuperacion, codigo_usuario):
            cambiar_password(st.session_state.correo_recuperacion, nueva_password)
            st.success("Contraseña cambiada correctamente. Ya puedes iniciar sesión.")
        else:
            st.error("Código incorrecto o expirado")