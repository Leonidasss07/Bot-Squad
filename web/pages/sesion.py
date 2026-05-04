import streamlit as st
from pages.db import crear_usuario, iniciar_sesion

st.set_page_config(
    page_title="Sesión - Nova music",
    layout="centered"
)

if "usuario" not in st.session_state:
    st.session_state.usuario = None

st.markdown("## Cuenta de usuario")

opcion = st.radio(
    "Elige una opción",
    ["Iniciar sesión", "Crear cuenta"],
    horizontal=True
)

correo = st.text_input("Correo")
password = st.text_input("Contraseña", type="password")

if opcion == "Crear cuenta":
    if st.button("Crear cuenta"):
        if crear_usuario(correo, password):
            st.success("Cuenta creada correctamente")
            st.session_state.usuario = correo
        else:
            st.error("Ese correo ya existe")

if opcion == "Iniciar sesión":
    if st.button("Iniciar sesión"):
        usuario = iniciar_sesion(correo, password)

        if usuario:
            st.success(f"Bienvenido, {correo}")
            st.session_state.usuario = correo
        else:
            st.error("Correo o contraseña incorrectos")