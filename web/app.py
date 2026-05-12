import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Proyecto Musical", layout="wide")

col1, col2 = st.columns([5, 1])

col_logo, col_titulo = st.columns([0.6, 6])


with col_titulo:
    st.markdown("<h1 style='margin-top: 16px;'>  𝄞 ANÁLISIS ESTADISTICO MUSICAL</h1>", unsafe_allow_html=True)
   
st.markdown("""
<p style='font-size:16px; max-width:800px;'>
En un mercado saturado la diferencia entre un track que pasa desapercibido y un exito global
suele estar en los detalles que el oido humano no siempre detecta a la primera.
En Análisis Estadistico Musical, transformamos el audio en métricas accionables
para que lleves tu sonido al siguiente nivel competitivo.
</p>
""", unsafe_allow_html=True)
st.markdown("""
<p style='font-size:22px; font-weight:bold; color:#3d2b1f; margin-top:20px;'>
NO SOMOS CRÍTICOS MUSICALES, SOMOS ANALISTAS DE DATOS
</p>
""", unsafe_allow_html=True)

st.markdown("## Explora los análisis")

col1, col2 = st.columns(2)

with col1:
    if st.button("Canciones populares"):
        st.switch_page("pages/canciones_populares.py")

    if st.button("Artistas"):
        st.switch_page("pages/artistas.py")

with col2:
    if st.button("Canciones del mes"):
        st.switch_page("pages/canciones_del_mes.py")

    if st.button("🎧 Géneros"):
        st.switch_page("pages/Géneros.py")

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
