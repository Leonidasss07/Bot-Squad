import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Proyecto Musical", layout="wide")

st.title("Proyecto musical con Last.fm")
st.subheader("Análisis de canciones, artistas y géneros")

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

st.header("Vista previa de los datos")

opcion = st.selectbox(
    "Selecciona una tabla",
    ["Canciones populares", "Artistas populares", "Géneros", "Canciones de julio"]
)

if opcion == "Canciones populares":
    st.dataframe(canciones.head(20))

elif opcion == "Artistas populares":
    st.dataframe(artistas.head(20))

elif opcion == "Géneros":
    st.dataframe(generos.head(20))

else:
    st.dataframe(julio.head(20))

conteo_generos = generos["generos"].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(conteo_generos.index, conteo_generos.values)
ax2.set_title("Géneros más populares")
ax2.set_xlabel("Género")
ax2.set_ylabel("Cantidad")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig2)

canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
top_canciones = canciones.sort_values(by="reproducciones", ascending=False).head(10)
