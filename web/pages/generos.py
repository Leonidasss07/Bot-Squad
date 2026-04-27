import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Géneros · AEM",
    page_icon="🎼",
    layout="wide"
)

# 🎨 ESTILO MODO DÍA
st.markdown("""
<style>

:root {
    --bg:        #f8fafc;
    --surface:   #ffffff;
    --surface2:  #f1f5f9;
    --accent:    #6366f1;
    --accent2:   #ec4899;
    --text:      #1e293b;
    --muted:     #64748b;
    --border:    #e2e8f0;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

.sidebar-logo {
    font-size: 22px;
    font-weight: 700;
    color: var(--accent) !important;
}

.sidebar-section {
    font-size: 11px;
    font-weight: 700;
    color: var(--muted) !important;
    letter-spacing: 1px;
    margin-top: 15px;
}

[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
}

h1, h2, h3 {
    color: var(--text) !important;
}

.accent-line {
    height: 3px;
    width: 48px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 2px;
    margin: 10px 0 20px 0;
}

</style>
""", unsafe_allow_html=True)


# 📂 DATOS
@st.cache_data
def cargar_generos():
    try:
        return pd.read_csv("data/clean/generos_canciones.csv")
    except:
        return pd.DataFrame()

generos_df = cargar_generos()


# 📊 PROCESAMIENTO
if not generos_df.empty and "generos" in generos_df.columns:
    conteo = generos_df["generos"].value_counts().head(8)
else:
    conteo = pd.Series({
        "pop": 320, "rock": 280, "hip-hop": 200,
        "jazz": 150, "electronic": 130
    })


# 📈 GRÁFICO
def grafico_generos(conteo):
    fig, ax = plt.subplots()

    ax.barh(conteo.index[::-1], conteo.values[::-1])

    ax.set_xlabel("Canciones")
    ax.set_ylabel("Género")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig


# 🎯 UI
st.title("🎼 Géneros musicales")
st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

st.write("Análisis de los géneros más escuchados.")

col1, col2, col3 = st.columns(3)

col1.metric("Géneros únicos", len(conteo))
col2.metric("Canciones", len(generos_df))
col3.metric("Top género", conteo.idxmax())

st.markdown("---")

colA, colB = st.columns(2)

with colA:
    st.subheader("Géneros más populares")
    st.pyplot(grafico_generos(conteo))

with colB:
    st.subheader("Tabla")
    tabla = conteo.reset_index()
    tabla.columns = ["género", "canciones"]
    st.dataframe(tabla, use_container_width=True)