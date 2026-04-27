import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Proyecto Musical", layout="wide")

st.title("Dashboard")

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

mes_actual = meses[datetime.now().month]
st.caption(f"Última sincronización con Last.fm: {mes_actual}")

canciones = pd.read_csv("data/clean/canciones_populares.csv")
artistas = pd.read_csv("data/clean/artistas_populares.csv")
generos = pd.read_csv("data/clean/generos_canciones.csv")
julio = pd.read_csv("data/clean/canciones_julio.csv")

st.header("Resumen general")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Canciones", len(canciones))
col2.metric("Artistas", len(artistas))
col3.metric("Géneros", len(generos))
col4.metric("Canciones de julio", len(julio))

col_tabla, col_artistas = st.columns(2)

with col_tabla:
    st.subheader("Géneros más populares")

    conteo_generos = generos["generos"].value_counts().head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.barh(conteo_generos.index, conteo_generos.values)
    ax2.invert_yaxis()
    ax2.set_title("Géneros más populares")
    ax2.set_xlabel("Cantidad")
    ax2.set_ylabel("Género")
    plt.tight_layout()

    st.pyplot(fig2)

artistas_ordenadas = artistas.sort_values(by="oyentes", ascending=False)

with col_artistas:
    st.subheader("Top Artistas")
    st.dataframe(artistas_ordenadas.head(10), use_container_width=True)

st.subheader("Canción más escuchada de la semana")