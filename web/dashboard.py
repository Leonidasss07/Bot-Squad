
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# st.set_page_config SIEMPRE debe ir una sola vez y al principio
st.set_page_config(page_title="Proyecto Musical", layout="wide")

st.title("📊 Dashboard")

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
mes_actual = meses[datetime.now().month]

st.caption(f"Última sincronización con Last.fm: {mes_actual}")

# Carga de datos (Añadí try-except por buenas prácticas, igual que en el otro archivo)
try:
    canciones = pd.read_csv("data/clean/canciones_populares.csv")
    artistas = pd.read_csv("data/clean/artistas_populares.csv")
    generos = pd.read_csv("data/clean/generos_canciones.csv")
    julio = pd.read_csv("data/clean/canciones_julio.csv")
except FileNotFoundError:
    st.error("Error al cargar los datos. Revisa que los archivos CSV existan en la ruta.")
    st.stop()

st.header("Resumen general")

# Métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Canciones", len(canciones))
col2.metric("Artistas", len(artistas))
col3.metric("Géneros", len(generos))
col4.metric("Canciones de julio", len(julio))

st.write("---")

# Añadimos gap="large" para separar mejor el gráfico de la tabla
col_tabla, col_artistas = st.columns(2, gap="large")

with col_tabla:
    st.subheader("🎸 Géneros más populares")
    conteo_generos = generos["generos"].value_counts().head(10)

    # --- INICIO MAGIA MATPLOTLIB MODO OSCURO ---
    plt.style.use('dark_background')
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    # Fondos transparentes
    fig2.patch.set_alpha(0.0)
    ax2.patch.set_alpha(0.0)

    # Color de barras azul moderno
    ax2.barh(conteo_generos.index, conteo_generos.values, color="#3b82f6")
    
    ax2.invert_yaxis()
    ax2.set_xlabel("Cantidad")
    ax2.set_ylabel("") # Limpiamos la etiqueta del eje Y
    
    plt.xticks(rotation=45, ha="right")
    
    # Quitamos bordes innecesarios
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_alpha(0.3)
    ax2.spines['left'].set_alpha(0.3)
    
    plt.tight_layout()
    # --- FIN MAGIA MATPLOTLIB ---
    
    st.pyplot(fig2)


# Ordenamos los artistas de mayor a menor usando los oyentes
artistas_ordenadas = artistas.sort_values(by="oyentes", ascending=False)

with col_artistas:
    st.subheader("🎤 Top Artistas")
    
    # 1. Tomamos los 10 primeros
    df_artistas_mostrar = artistas_ordenadas.head(10).copy()
    
    # 2. Reiniciamos el índice
    df_artistas_mostrar = df_artistas_mostrar.reset_index(drop=True)
    
    # 3. Sumamos 1 para que empiece en 1
    df_artistas_mostrar.index = df_artistas_mostrar.index + 1
    
    # 4. Eliminamos la columna "reproducciones" si existe
    if "reproducciones" in df_artistas_mostrar.columns:
        df_artistas_mostrar = df_artistas_mostrar.drop(columns=["reproducciones"])
        
    # 5. Mostramos la tabla
    st.dataframe(
        df_artistas_mostrar, 
        use_container_width=True,
        column_config={
            "_index": st.column_config.NumberColumn("Puesto", format="%d"),
            "url": st.column_config.LinkColumn(
                "Enlace",
                display_text="Ir a Last.fm"
            )
        }
    )

st.write("---")

# --- SECCIÓN: Canción de la semana ---
st.subheader("🎧 Canción más escuchada")

# 1. Aseguramos que reproducciones sea número y ordenamos
canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
canciones_top = canciones.sort_values(by="reproducciones", ascending=False)

# 2. Obtenemos el primer lugar
top_1 = canciones_top.iloc[0]

# 3. Lo mostramos bonito
col_img, col_info = st.columns([1, 3])

with col_img:
    if "imagen_url" in top_1 and pd.notna(top_1["imagen_url"]) and top_1["imagen_url"] != "":
        st.image(top_1["imagen_url"], width=200)
    else:
        st.info("🎵 Sin portada")

with col_info:
    st.markdown(f"### {top_1['nombre']}")
    st.markdown(f"**Artista:** {top_1['artista']}")
    
    reproducciones_formato = f"{top_1['reproducciones']:,.0f}"
    st.markdown(f"**Reproducciones:** {reproducciones_formato}")
    
    if "url" in top_1:
        st.link_button("Escuchar en Last.fm", top_1["url"])