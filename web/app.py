import streamlit as st

st.set_page_config(
    page_title="Proyecto Musical",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #f3f6fb;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #1f2a44;
    margin-bottom: 10px;
}

.sidebar-section {
    font-size: 12px;
    font-weight: 800;
    color: #8a8f98;
    letter-spacing: 1px;
    margin-top: 18px;
    margin-bottom: 8px;
}

section[data-testid="stSidebar"] div.stButton > button {
    background-color: transparent !important;
    border: none !important;
    color: #1f2a44 !important;
    font-weight: 600;
    text-align: left;
    padding-left: 4px;
    font-size: 16px;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #e9eefc !important;
    border-radius: 6px;
}

.main-buttons button {
    height: 90px !important;
    border-radius: 18px !important;
    border: none !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #1f2a44 !important;
}

.main-buttons.btn1 button { background-color: #d7e3fc !important; }
.main-buttons.btn2 button { background-color: #f7d6e0 !important; }
.main-buttons.btn3 button { background-color: #fff4b8 !important; }
.main-buttons.btn4 button { background-color: #d9f2d9 !important; }

.main-buttons button:hover {
    filter: brightness(0.96) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08) !important;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="sidebar-title">Analisis Musical Stats</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">HOME</div>', unsafe_allow_html=True)
    if st.button("Página principal"):
        st.session_state.menu = "Inicio"

    st.markdown('<div class="sidebar-section">DASHBOARD</div>', unsafe_allow_html=True)
    if st.button("Dashboard"):
        st.switch_page("pages/dashboard.py")

    st.markdown('<div class="sidebar-section">EXPLORAR</div>', unsafe_allow_html=True)

    if st.button("Canciones"):
        st.switch_page("pages/canciones.py")

    if st.button("Géneros"):
        st.switch_page("pages/generos.py")

    if st.button("Artistas"):
        st.session_state.menu = "Artistas"

    st.markdown('<div class="sidebar-section">PRODUCTOR</div>', unsafe_allow_html=True)
    if st.button("Tendencias"):
        st.session_state.menu = "Tendencias"

    st.markdown('<div class="sidebar-section">USUARIO</div>', unsafe_allow_html=True)
    if st.button("Perfil"):
        st.session_state.menu = "Perfil"


opcion = st.session_state.get("menu", "Inicio")


if opcion == "Inicio":
    st.title("𝄞 ÁNALISIS ESTADISTICO MUSICAL")

    st.markdown("""
    <p style='font-size:16px; max-width:800px;'>
    En un mercado saturado, la diferencia entre un track que pasa desapercibido y un éxito global
    suele estar en los detalles que el oído humano no siempre detecta a la primera.
    En Análisis Estadístico Musical, transformamos el audio en métricas accionables
    para que lleves tu sonido al siguiente nivel competitivo.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size:22px; font-weight:bold; color:#3d2b1f; margin-top:10px;'>
    NO SOMOS CRÍTICOS MUSICALES, SOMOS ANALISTAS DE DATOS
    </p>
    """, unsafe_allow_html=True)

    st.markdown("### Explora")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="main-buttons btn1">', unsafe_allow_html=True)
        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="main-buttons btn2">', unsafe_allow_html=True)
        if st.button("Canciones", use_container_width=True):
            st.switch_page("pages/canciones.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="main-buttons btn3">', unsafe_allow_html=True)
        if st.button("Artistas", use_container_width=True):
            st.session_state.menu = "Artistas"
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="main-buttons btn4">', unsafe_allow_html=True)
        if st.button("Géneros", use_container_width=True):
            st.switch_page("pages/generos.py")
        st.markdown('</div>', unsafe_allow_html=True)


elif opcion == "Artistas":
    st.title("Artistas")
    st.info("Aquí irán los artistas.")

elif opcion == "Tendencias":
    st.title("Tendencias")
    st.info("Aquí irán las tendencias musicales.")

elif opcion == "Perfil":
    st.title("Usuario")
    st.info("Aquí irá la información")
