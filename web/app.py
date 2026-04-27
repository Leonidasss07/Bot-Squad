import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Proyecto Musical",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none !important; }

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
    margin-bottom: 4px;
}

.metric-card {
    background-color: white;
    padding: 10px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
}

/* Radio como texto simple */
div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] > div { gap: 2px !important; }
div[data-testid="stRadio"] > div > label {
    display: block !important;
    padding: 6px 8px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #1f2a44 !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stRadio"] > div > label:hover { color: #4f6ef7 !important; }
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }
div[data-testid="stRadio"] > div > label > p {
    font-size: 15px !important;
    font-weight: 500 !important;
    margin: 0 !important;
}

/* Botones sidebar como texto simple */
div[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    height: auto;
    padding: 6px 8px;
    border-radius: 8px;
    border: none;
    background-color: transparent;
    color: #1f2a44;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    box-shadow: none;
    transition: color 0.15s ease;
}
div[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: transparent;
    color: #4f6ef7;
    border: none;
    box-shadow: none;
}

/* Botones de explorar en página principal */
div[data-testid="stMain"] div.stButton > button {
    width: 100%;
    height: 54px;
    border-radius: 12px;
    border: 1px solid #d6dbe4;
    background-color: white;
    color: #1f2a44;
    font-size: 15px;
    font-weight: 500;
    transition: background-color 0.15s ease, border-color 0.15s ease;
}
div[data-testid="stMain"] div.stButton > button:hover {
    background-color: #f0f4ff;
    border-color: #b8c4ea;
}
</style>
""", unsafe_allow_html=True)

# Inicializa la página activa solo la primera vez
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "🏠 Página principal"

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">Analisis Musical Stats</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">HOME</div>', unsafe_allow_html=True)
    if st.button("🏠 Página principal", key="btn_home"):
        st.session_state["pagina"] = "🏠 Página principal"

    st.markdown('<div class="sidebar-section">DASHBOARD</div>', unsafe_allow_html=True)
    if st.button("📊 Dashboard", key="btn_dash"):
        st.session_state["pagina"] = "📊 Dashboard"

    st.markdown('<div class="sidebar-section">EXPLORAR</div>', unsafe_allow_html=True)
    if st.button("🎵 Canciones", key="btn_canciones"):
        st.session_state["pagina"] = "🎵 Canciones"
    if st.button("🎤 Artistas", key="btn_artistas"):
        st.session_state["pagina"] = "🎤 Artistas"
    if st.button("🎼 Géneros", key="btn_generos"):
        st.session_state["pagina"] = "🎼 Géneros"

    st.markdown('<div class="sidebar-section">PRODUCTOR</div>', unsafe_allow_html=True)
    if st.button("⭐ Favoritos", key="btn_favoritos"):
        st.session_state["pagina"] = "⭐ Favoritos"
    if st.button("📈 Tendencias", key="btn_tendencias"):
        st.session_state["pagina"] = "📈 Tendencias"
    if st.button("🕘 Historial", key="btn_historial"):
        st.session_state["pagina"] = "🕘 Historial"

    st.markdown('<div class="sidebar-section">USUARIO</div>', unsafe_allow_html=True)
    if st.button("👤 Perfil", key="btn_perfil"):
        st.session_state["pagina"] = "👤 Perfil"

opcion = st.session_state["pagina"]

# ── Datos temporales ──
canciones = pd.DataFrame({
    "nombre": ["Dato pendiente", "Dato pendiente", "Dato pendiente"],
    "reproducciones": [0, 0, 0]
})
artistas = pd.DataFrame({"nombre": ["Dato pendiente", "Dato pendiente", "Dato pendiente"]})
generos  = pd.DataFrame({"generos": ["Pendiente", "Pendiente", "Pendiente"]})
julio    = pd.DataFrame({"nombre": ["Dato pendiente", "Dato pendiente", "Dato pendiente"]})

# ── Página principal ──
if opcion == "🏠 Página principal":
    st.title("𝄞 ÁNALISIS ESTADISTICO MUSICAL")

    st.markdown("""
    <p style='font-size:16px; max-width:800px; color:#374151;'>
    En un mercado saturado, la diferencia entre un track que pasa desapercibido y un éxito global
    suele estar en los detalles que el oído humano no siempre detecta a la primera.
    En Análisis Estadístico Musical, transformamos el audio en métricas accionables
    para que lleves tu sonido al siguiente nivel competitivo.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size:17px; font-weight:700; color:#1f2a44; margin-top:8px; margin-bottom:32px;'>
    NO SOMOS CRÍTICOS MUSICALES, SOMOS ANALISTAS DE DATOS
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Explora")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Dashboard", key="exp_dash"):
            st.session_state["pagina"] = "📊 Dashboard"
            st.rerun()
    with col2:
        if st.button("Canciones", key="exp_canciones"):
            st.session_state["pagina"] = "🎵 Canciones"
            st.rerun()
    with col3:
        if st.button("Artistas", key="exp_artistas"):
            st.session_state["pagina"] = "🎤 Artistas"
            st.rerun()
    with col4:
        if st.button("Géneros", key="exp_generos"):
            st.session_state["pagina"] = "🎼 Géneros"
            st.rerun()

# ── Dashboard ──
elif opcion == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Canciones", len(canciones))
    col2.metric("Artistas", len(artistas))
    col3.metric("Géneros", len(generos))
    col4.metric("Canciones del mes", len(julio))

    st.subheader("Vista general")
    col_a, col_b = st.columns([1.4, 1])
    with col_a:
        st.write("Desde el menú lateral podrás acceder a las demás secciones del sistema.")
    with col_b:
        conteo_generos = generos["generos"].value_counts().head(10)
        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(conteo_generos.index, conteo_generos.values, color="#4f6ef7")
        ax.set_title("Resumen de géneros")
        ax.set_xlabel("Género")
        ax.set_ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

elif opcion == "🎵 Canciones":
    st.title("🎵 Canciones")
    st.dataframe(canciones, use_container_width=True)

elif opcion == "🎤 Artistas":
    st.title("🎤 Artistas")
    st.dataframe(artistas, use_container_width=True)

elif opcion == "🎼 Géneros":
    st.title("🎼 Géneros")
    st.markdown("Distribución de géneros musicales extraída de Last.fm.")
    st.markdown("---")

    # Carga real del CSV
    import os
    gen_path = "data/clean/generos_canciones.csv"
    if os.path.exists(gen_path):
        gen_df = pd.read_csv(gen_path)
        conteo_generos = gen_df["generos"].value_counts().head(10).reset_index()
        conteo_generos.columns = ["género", "cantidad"]
    else:
        conteo_generos = pd.DataFrame({
            "género":   ["Jazz", "Pop", "Rock", "Soul", "Hip-Hop"],
            "cantidad": [15, 12, 10, 8, 6]
        })

    col_izq, col_der = st.columns([1, 1.4], gap="large")

    with col_izq:
        st.subheader("Tabla de géneros")
        st.dataframe(
            conteo_generos.style.bar(subset=["cantidad"], color="#c7d3fc"),
            use_container_width=True,
            hide_index=True
        )

    with col_der:
        st.subheader("Gráfica de géneros")
        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(7, 4.5))
        colors = ["#4f6ef7", "#6c82f8", "#8997f9", "#a6acfa", "#c3c1fb",
                  "#4f6ef7", "#6c82f8", "#8997f9", "#a6acfa", "#c3c1fb"]
        bars = ax.barh(
            conteo_generos["género"][::-1],
            conteo_generos["cantidad"][::-1],
            color=colors[:len(conteo_generos)],
            height=0.6, edgecolor="none"
        )
        ax.set_xlabel("Cantidad de canciones", fontsize=10, color="#555")
        ax.tick_params(axis="y", labelsize=11)
        ax.tick_params(axis="x", labelsize=9, colors="#888")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_xlim(0, conteo_generos["cantidad"].max() * 1.18)
        for bar, val in zip(bars, conteo_generos["cantidad"][::-1]):
            ax.text(
                bar.get_width() + conteo_generos["cantidad"].max() * 0.02,
                bar.get_y() + bar.get_height() / 2,
                str(val), va="center", color="#555", fontsize=9
            )
        ax.set_facecolor("#fafbff")
        fig.patch.set_facecolor("#fafbff")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

elif opcion == "⭐ Favoritos":
    st.switch_page("pages/4_Favoritos.py")

elif opcion == "📈 Tendencias":
    st.title("📈 Tendencias")
    st.info("Aquí irán las tendencias musicales.")

elif opcion == "🕘 Historial":
    st.title("🕘 Historial")
    st.info("Aquí irá el historial del usuario o productor.")

elif opcion == "👤 Perfil":
    st.title("👤 Usuario")
    st.info("Aquí irá la información del usuario.")