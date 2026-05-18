import streamlit as st
import os

_ARCHIVO_SESION = "usuario_activo.txt"


def recuperar_sesion():
    """
    Recupera la sesion activa. Comprueba session_state primero,
    luego el archivo de respaldo. Llamar al inicio de cada pagina.
    """
    if st.session_state.get("usuario"):
        return st.session_state["usuario"]

    if os.path.exists(_ARCHIVO_SESION):
        with open(_ARCHIVO_SESION, "r", encoding="utf-8") as f:
            usuario = f.read().strip()
        if usuario:
            st.session_state["usuario"] = usuario
            return usuario

    return None


def guardar_sesion(correo):
    """Guarda la sesion en session_state y en archivo de respaldo."""
    st.session_state["usuario"] = correo
    with open(_ARCHIVO_SESION, "w", encoding="utf-8") as f:
        f.write(correo)


def cerrar_sesion():
    """Cierra la sesion limpiando session_state y el archivo."""
    if "usuario" in st.session_state:
        del st.session_state["usuario"]
    if os.path.exists(_ARCHIVO_SESION):
        os.remove(_ARCHIVO_SESION)