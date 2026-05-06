import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import ScalarFormatter

# Configuración inicial de la página
st.set_page_config(page_title="Proyecto Musical", page_icon="🎵", layout="wide")

st.title("🎧 Canciones Populares")

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
mes_actual = meses[datetime.now().month]

st.caption(f"Última sincronización con Last.fm: {mes_actual}")

# 1. Cargamos todos los datos originales
try:
    canciones = pd.read_csv("data/clean/canciones_populares.csv")
    canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
except FileNotFoundError:
    st.error("No se encontró el archivo de datos. Revisa la ruta.")
    st.stop()

# 2. Buscador
st.write("---") 
termino_busqueda = st.text_input("🔍 Buscar canción o artista:", placeholder="Escribe tu búsqueda aquí...")

if termino_busqueda:
    filtro = canciones["nombre"].str.contains(termino_busqueda, case=False, na=False) | \
             canciones["artista"].str.contains(termino_busqueda, case=False, na=False)
    canciones = canciones[filtro]

if canciones.empty:
    st.warning(f"No encontramos resultados para '{termino_busqueda}'. Intenta con otra palabra.")
else:
    canciones_ordenadas = canciones.sort_values(by="reproducciones", ascending=False)

    # Añadimos gap="large" para separar las columnas
    col1, col_tabla = st.columns(2, gap="large")

    with col1:
        st.subheader("🏆 Top Canciones")
        
        df_mostrar = canciones_ordenadas.head(10).copy()
        
        for puesto, (index, row) in enumerate(df_mostrar.iterrows(), start=1):
            
            col_num, col_img, col_info, col_audio = st.columns([0.5, 1, 3.5, 2])
            
            with col_num:
                st.markdown(f"### #{puesto}")

            with col_img:
                if "imagen_url" in row and pd.notna(row["imagen_url"]):
                    st.image(row["imagen_url"], use_container_width=True)
            
            with col_info:
                st.markdown(f"*{row['nombre']}* \n\n*{row['artista']}*")
                
            with col_audio:
                enlace = str(row.get("audio_url", "")).strip()
                if enlace.startswith("http"):
                    st.audio(enlace, format="audio/mp3")    
                else:
                    st.caption("🎵 No disponible")
            
            st.divider()

    with col_tabla:
        st.subheader("📊 Gráfico de reproducciones")

        top_canciones = canciones.sort_values(by="reproducciones", ascending=False).head(10)

        # --- AQUÍ ESTÁ LA MAGIA DE MATPLOTLIB PARA MODO OSCURO ---
        
        # 1. Le decimos a matplotlib que use su estilo oscuro por defecto
        plt.style.use('dark_background')
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        # 2. Hacemos que el fondo de la figura y el área del gráfico sean transparentes
        fig2.patch.set_alpha(0.0)
        ax2.patch.set_alpha(0.0)

        # 3. Dibujamos las barras con un color azul moderno
        ax2.barh(top_canciones["nombre"], top_canciones["reproducciones"], color="#3b82f6")
        
        ax2.invert_yaxis()
        ax2.set_xlabel("Cantidad de Reproducciones")
        ax2.set_ylabel("") # Dejamos el eje Y sin título para limpiar el diseño
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        ax2.ticklabel_format(style='plain', axis='x')
        
        # 4. Quitamos los bordes superior y derecho para que se vea más minimalista
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        # Hacemos los bordes restantes un poco más tenues
        ax2.spines['bottom'].set_alpha(0.3)
        ax2.spines['left'].set_alpha(0.3)
        
        st.pyplot(fig2)