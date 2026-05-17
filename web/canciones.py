import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import ScalarFormatter
import base64
import os
import json

# --- CONFIGURACIÓN DE PERSISTENCIA ---
FAVORITOS_FILE = "favoritos.json"

def cargar_favoritos():
    """Carga los favoritos desde el archivo físico JSON."""
    if os.path.exists(FAVORITOS_FILE):
        try:
            with open(FAVORITOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_favoritos(lista_favoritos):
    """Guarda la lista actual de favoritos en el archivo JSON."""
    with open(FAVORITOS_FILE, "w", encoding="utf-8") as f:
        json.dump(lista_favoritos, f, ensure_ascii=False, indent=4)

# --- CONFIGURACIÓN INICIAL DE STREAMLIT ---
st.set_page_config(page_title="Proyecto Musical", page_icon="🎵", layout="wide")

# Inicializar el estado global de favoritos
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = cargar_favoritos()

# --- DISEÑO: FONDO Y ESTILOS ---
def set_background():
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "nova_music_background.jpeg")
    
    if not os.path.exists(image_path):
        image_path = os.path.join(current_dir, "nova_music_background.jpg")

    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode()
            
            mime = "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"

            st.markdown(
                f"""
                <style>
                .stApp {{
                    background: 
                        linear-gradient(to bottom, rgba(14, 17, 23, 0) 25%, rgba(14, 17, 23, 1) 50%), 
                        url("data:{mime};base64,{base64_image}");
                    background-size: cover;
                    background-position: center center;
                    background-attachment: fixed;
                }}
                h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
                    color: white !important;
                }}
                .stTextInput>div>div>input {{
                    background-color: rgba(0, 0, 0, 0.5) !important;
                    color: white !important;
                    border: 1px solid rgba(255,255,255,0.2) !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error al procesar la imagen: {e}")

set_background()

# --- LÓGICA DE PÁGINA: EXPLORAR ---
def pagina_explorar():
    st.title("Canciones Populares")
    
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 
             7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    mes_actual = meses[datetime.now().month]
    st.caption(f"Última sincronización con Last.fm: {mes_actual}")

    try:
        canciones = pd.read_csv("data/clean/canciones_populares.csv")
        canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")
    except FileNotFoundError:
        st.error("No se encontró el archivo 'data/clean/canciones_populares.csv'.")
        return

    st.write("---") 
    termino_busqueda = st.text_input("Buscar canción o artista:", placeholder="Escribe tu búsqueda aquí...")

    if termino_busqueda:
        filtro = canciones["nombre"].str.contains(termino_busqueda, case=False, na=False) | \
                 canciones["artista"].str.contains(termino_busqueda, case=False, na=False)
        canciones = canciones[filtro]

    if canciones.empty:
        st.warning("No se encontraron resultados.")
    else:
        canciones_ordenadas = canciones.sort_values(by="reproducciones", ascending=False)
        col1, col_tabla = st.columns(2, gap="large")

        with col1:
            st.subheader("Top Canciones")
            df_mostrar = canciones_ordenadas.head(10).copy()
            
            for puesto, (index, row) in enumerate(df_mostrar.iterrows(), start=1):
                col_num, col_img, col_info, col_audio, col_fav = st.columns([0.5, 1, 2.5, 3, 0.7])
                
                with col_num:
                    st.markdown(f"### #{puesto}")
                with col_img:
                    if "imagen_url" in row and pd.notna(row["imagen_url"]):
                        st.image(row["imagen_url"], use_container_width=True)
                with col_info:
                    st.markdown(f"**{row['nombre']}** \n\n*{row['artista']}*")
                with col_audio:
                    enlace = str(row.get("audio_url", "")).strip()
                    if enlace.startswith("http"):
                        st.audio(enlace, format="audio/mp4")
                    else:
                        st.caption("🎵 No disponible")
                
                with col_fav:
                    # Lógica de favorito
                    es_fav = any(f['nombre'] == row['nombre'] and f['artista'] == row['artista'] for f in st.session_state.favoritos)
                    if st.button("❤️" if es_fav else "🤍", key=f"btn_{index}"):
                        if not es_fav:
                            nueva_cancion = {
                                "nombre": row['nombre'], 
                                "artista": row['artista'], 
                                "audio_url": row.get("audio_url", ""),
                                "imagen_url": row.get("imagen_url", "")
                            }
                            st.session_state.favoritos.append(nueva_cancion)
                        else:
                            st.session_state.favoritos = [f for f in st.session_state.favoritos if not (f['nombre'] == row['nombre'] and f['artista'] == row['artista'])]
                        
                        guardar_favoritos(st.session_state.favoritos)
                        st.rerun()
                st.divider()

        with col_tabla:
            st.subheader("Gráfico de reproducciones")
            top_canciones = canciones_ordenadas.head(10)
            plt.style.use('dark_background')
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            fig2.patch.set_alpha(0.0)
            ax2.patch.set_alpha(0.0)
            ax2.barh(top_canciones["nombre"], top_canciones["reproducciones"], color="#3b82f6")
            ax2.invert_yaxis()
            ax2.xaxis.set_major_formatter(ScalarFormatter())
            ax2.ticklabel_format(style='plain', axis='x')
            st.pyplot(fig2)

# --- LÓGICA DE PÁGINA: FAVORITOS ---
def pagina_favoritos():
    st.title("❤️ Mis Canciones Favoritas")
    st.write("Aquí guardamos tus temas preferidos para que no se pierdan.")
    
    if not st.session_state.favoritos:
        st.info("Aún no tienes canciones favoritas. ¡Explora el catálogo y añade algunas!")
    else:
        if st.button("Limpiar toda la lista"):
            st.session_state.favoritos = []
            guardar_favoritos([])
            st.rerun()
            
        st.write("---")
        
        # Mostrar favoritos guardados
        for i, fav in enumerate(st.session_state.favoritos):
            c_img, c_txt, c_aud, c_del = st.columns([1, 3, 3, 1])
            
            with c_img:
                if fav.get("imagen_url"):
                    st.image(fav["imagen_url"], width=80)
            with c_txt:
                st.markdown(f"**{fav['nombre']}**")
                st.caption(fav['artista'])
            with c_aud:
                if fav.get("audio_url") and str(fav["audio_url"]).startswith("http"):
                    st.audio(fav["audio_url"], format="audio/mp4")
            with c_del:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.favoritos.pop(i)
                    guardar_favoritos(st.session_state.favoritos)
                    st.rerun()
            st.divider()

# --- NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.title("Nova Music 🎵")
    opcion = st.radio("Navegación", ["Explorar", "Mis Favoritos"])
    st.write("---")


# Renderizar la página seleccionada
if opcion == "Explorar":
    pagina_explorar()
else:
    pagina_favoritos()
