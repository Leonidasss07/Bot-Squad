import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import ScalarFormatter
import os

st.set_page_config(page_title="Proyecto Musical", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
        .header-section {
            background: linear-gradient(135deg, #FFD9B3 0%, #FFB3D9 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .search-section {
            background-color: #B3D9FF;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .results-section {
            background-color: #D4F1D4;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .stats-section {
            background-color: #FFFFCC;
            padding: 15px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-section"><h1>🎵 Artistas Populares</h1></div>', unsafe_allow_html=True)


@st.cache_data
def cargar_artistas():
    ruta = os.path.join(os.path.dirname(__file__), "../data/clean/artistas_populares.csv")
    return pd.read_csv(ruta)

artistas = cargar_artistas()

artistas["reproducciones"] = pd.to_numeric(artistas["reproducciones"], errors="coerce")

artistas_ordenados = artistas.sort_values(by="reproducciones", ascending=False).reset_index(drop=True)

# SECCIÓN DE BÚSQUEDA
st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown("### 🔍 Buscar Artista")
busqueda = st.text_input("Escribe el nombre del artista que buscas:", placeholder="Ej. Kanye West")
st.markdown('</div>', unsafe_allow_html=True)

# SECCIÓN DE RESULTADOS DE BÚSQUEDA
if busqueda:
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    resultados = artistas_ordenados[artistas_ordenados["nombre"].str.contains(busqueda, case=False, na=False)].copy()
    if resultados.empty:
        st.warning("⚠️ No se encontró ningún artista con ese nombre. Prueba otra búsqueda.")
    else:
        st.markdown("#### 📊 Resultados de la Búsqueda")
        resultados["posición"] = resultados.index + 1
        resultados["reproducciones"] = resultados["reproducciones"].map('{:,.0f}'.format)
        st.dataframe(resultados[["posición", "nombre", "reproducciones", "oyentes"]], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# SECCIÓN DE ESTADÍSTICAS
st.markdown('<div class="stats-section">', unsafe_allow_html=True)

col1, col_tabla = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 10 Artistas")
    df_mostrar = artistas_ordenados.head(10).copy()
    df_mostrar["reproducciones"] = df_mostrar["reproducciones"].map('{:,.0f}'.format)
    st.dataframe(df_mostrar, use_container_width=True)

with col_tabla:
    st.markdown("### 📈 Gráfico de Popularidad")
    top_artistas = artistas_ordenados.head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colores_pastel = ['#FFB3D9', '#B3D9FF', '#D4F1D4', '#FFFFCC', '#FFD9B3', '#D9D9FF', '#FFD9E8', '#CCFFCC', '#FFFACD', '#FFE4B5']
    ax2.barh(top_artistas["nombre"], top_artistas["reproducciones"], color=colores_pastel)
    ax2.invert_yaxis()
    ax2.set_title("Artistas más populares", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Reproducciones", fontsize=12)
    ax2.set_ylabel("Nombre", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    ax2.xaxis.set_major_formatter(ScalarFormatter())
    ax2.ticklabel_format(style='plain', axis='x')
    fig2.patch.set_facecolor('#FFFFCC')
    st.pyplot(fig2)

st.markdown('</div>', unsafe_allow_html=True)

