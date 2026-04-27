import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Semanales", layout="wide")

st.title("📅 Canciones semanales")

genero = st.selectbox("Elige un género", ["Jazz", "Pop", "Rock"])

df = pd.DataFrame({
    "nombre": ["Like a Tattoo", "Take Five", "My Way"],
    "artista": ["Sade", "Dave Brubeck", "Frank Sinatra"],
    "oyentes": [1200, 950, 740]
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tabla semanal")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Gráfico semanal")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df["nombre"], df["oyentes"])
    ax.set_xlabel("Oyentes")
    ax.set_ylabel("Canción")
    ax.set_title(f"Top canciones semanales - {genero}")
    plt.tight_layout()
    st.pyplot(fig)