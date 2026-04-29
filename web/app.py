import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Proyecto Musical", layout="wide")


def cargar_csv_seguro(ruta):
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return pd.DataFrame()

def convertir_fechas_unix(df, col_desde="fecha_desde", col_hasta="fecha_hasta"):
    if col_desde in df.columns:
        df[col_desde] = pd.to_datetime(df[col_desde], unit="s", errors="coerce")
        df[col_desde] = df[col_desde].dt.strftime("%d/%m/%Y")
    if col_hasta in df.columns:
        df[col_hasta] = pd.to_datetime(df[col_hasta], unit="s", errors="coerce")
        df[col_hasta] = df[col_hasta].dt.strftime("%d/%m/%Y")
    return df

def limpiar_numeros(df, columna):
    if columna in df.columns:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")
    return df


canciones = cargar_csv_seguro("data/clean/canciones_populares.csv")
artistas = cargar_csv_seguro("data/clean/artistas_populares.csv")
generos = cargar_csv_seguro("data/clean/generos_canciones.csv")
julio = cargar_csv_seguro("data/clean/canciones_julio.csv")
artistas_semanales = cargar_csv_seguro("data/clean/artistas_semanales.csv")

if not artistas_semanales.empty:
    artistas_semanales = convertir_fechas_unix(artistas_semanales, "fecha_desde", "fecha_hasta")
    artistas_semanales = limpiar_numeros(artistas_semanales, "reproducciones")

if not canciones.empty:
    canciones = limpiar_numeros(canciones, "reproducciones")

if not artistas.empty:
    artistas = limpiar_numeros(artistas, "reproducciones")


st.title("🎧 Proyecto musical con Last.fm")
st.subheader("Análisis de canciones, artistas, géneros y rankings semanales")

st.divider()


st.header("📊 Resumen general")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Canciones", len(canciones))
col2.metric("Artistas", len(artistas))
col3.metric("Géneros", len(generos))
col4.metric("Julio", len(julio))
col5.metric("Semanales", len(artistas_semanales))

st.divider()


st.header("📁 Vista previa de los datos")

opcion = st.selectbox(
    "Selecciona una tabla",
    [
        "Canciones populares",
        "Artistas populares",
        "Géneros",
        "Canciones de julio",
        "Artistas semanales"
    ]
)

if opcion == "Canciones populares":
    if canciones.empty:
        st.warning("No se encontró el archivo de canciones populares.")
    else:
        st.dataframe(canciones.head(20), use_container_width=True)

elif opcion == "Artistas populares":
    if artistas.empty:
        st.warning("No se encontró el archivo de artistas populares.")
    else:
        st.dataframe(artistas.head(20), use_container_width=True)

elif opcion == "Géneros":
    if generos.empty:
        st.warning("No se encontró el archivo de géneros.")
    else:
        st.dataframe(generos.head(20), use_container_width=True)

elif opcion == "Canciones de julio":
    if julio.empty:
        st.warning("No se encontró el archivo de canciones de julio.")
    else:
        st.dataframe(julio.head(20), use_container_width=True)

elif opcion == "Artistas semanales":
    if artistas_semanales.empty:
        st.warning("No se encontró el archivo de artistas semanales.")
    else:
        st.dataframe(artistas_semanales.head(20), use_container_width=True)

st.divider()

st.header("🗓️ Canciones semanales")

tag_usuario = st.selectbox(
    "Elige un género",
    ["disco", "rock", "pop", "jazz", "hip-hop", "k-pop"]
)

ruta_csv_tag = f"data/clean/canciones_{tag_usuario}.csv"
canciones_tag = cargar_csv_seguro(ruta_csv_tag)

if not canciones_tag.empty:
    canciones_tag = convertir_fechas_unix(canciones_tag, "fecha_desde", "fecha_hasta")


    if not canciones_tag.empty:
        semana_desde = canciones_tag["fecha_desde"].iloc[0] if "fecha_desde" in canciones_tag.columns else "N/A"
        semana_hasta = canciones_tag["fecha_hasta"].iloc[0] if "fecha_hasta" in canciones_tag.columns else "N/A"

        st.markdown(f"**Semana:** {semana_desde} - {semana_hasta}")
        st.markdown(f"**Tag seleccionado:** {tag_usuario}")

        col_izq, col_der = st.columns(2)

        with col_izq:
            st.subheader("Tabla semanal")
            columnas_tabla = [col for col in ["nombre", "artista"] if col in canciones_tag.columns]
            st.dataframe(canciones_tag[columnas_tabla].head(10), use_container_width=True)

        with col_der:
            st.subheader("Gráfico semanal")
            top10 = canciones_tag.sort_values(by="oyentes", ascending=False).head(10).copy()
            top10 = top10.sort_values(by="oyentes", ascending=True)
            top10["etiqueta"] = top10["nombre"].astype(str).str.slice(0, 30)

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(top10["etiqueta"], top10["oyentes"])
            ax.set_title(f"Top canciones semanales - {tag_usuario}")
            ax.set_xlabel("Oyentes")
            ax.set_ylabel("Canción")
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.warning(f"El archivo {ruta_csv_tag} existe, pero no tiene valores numéricos válidos en 'oyentes'.")
else:
    st.warning(f"No existe el archivo {ruta_csv_tag}. Ejecuta antes tu script de descarga.")

st.divider()



st.header("📈 Gráficos generales")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Géneros más populares")
    if not generos.empty and "generos" in generos.columns:
        conteo_generos = generos["generos"].value_counts().head(10)

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.bar(conteo_generos.index, conteo_generos.values)
        ax2.set_title("Top géneros")
        ax2.set_xlabel("Género")
        ax2.set_ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig2)
    else:
        st.warning("No hay datos de géneros disponibles.")

with col_g2:
    st.subheader("Top artistas globales")
    if not artistas.empty and "reproducciones" in artistas.columns and "nombre" in artistas.columns:
        top_artistas = artistas.dropna(subset=["reproducciones"]).sort_values(
            by="reproducciones", ascending=False
        ).head(10).copy()

        top_artistas = top_artistas.sort_values(by="reproducciones", ascending=True)
        top_artistas["etiqueta"] = top_artistas["nombre"].astype(str).str.slice(0, 30)

        fig3, ax3 = plt.subplots(figsize=(8, 5))
        ax3.barh(top_artistas["etiqueta"], top_artistas["reproducciones"])
        ax3.set_title("Top artistas")
        ax3.set_xlabel("Reproducciones")
        ax3.set_ylabel("Artista")
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.warning("No hay datos de artistas disponibles.")

st.divider()

st.header("⚡ Comparación entre tags")

tags_comparacion = ["disco", "rock"]
col_a, col_b = st.columns(2)

for i, tag in enumerate(tags_comparacion):
    ruta = f"data/clean/canciones_{tag}.csv"
    df = cargar_csv_seguro(ruta)

    if not df.empty:
        df = convertir_fechas_unix(df, "fecha_desde", "fecha_hasta")
        df = limpiar_numeros(df, "oyentes")
        df = df.dropna(subset=["oyentes"])
        df = df[df["oyentes"] > 0]

        if not df.empty:
            top5 = df.sort_values(by="oyentes", ascending=False).head(5).copy()
            top5["etiqueta"] = top5["nombre"].astype(str).str.slice(0, 20)

            if i == 0:
                with col_a:
                    st.subheader(f"Tag: {tag}")
                    st.dataframe(top5[["nombre", "artista", "oyentes"]], use_container_width=True)

                    fig, ax = plt.subplots(figsize=(7, 4))
                    ax.bar(top5["etiqueta"], top5["oyentes"])
                    ax.set_title(f"Top 5 - {tag}")
                    ax.set_ylabel("Oyentes")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig)
            else:
                with col_b:
                    st.subheader(f"Tag: {tag}")
                    st.dataframe(top5[["nombre", "artista", "oyentes"]], use_container_width=True)

                    fig, ax = plt.subplots(figsize=(7, 4))
                    ax.bar(top5["etiqueta"], top5["oyentes"])
                    ax.set_title(f"Top 5 - {tag}")
                    ax.set_ylabel("Oyentes")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig)
        else:
            if i == 0:
                with col_a:
                    st.warning(f"El archivo de {tag} no tiene oyentes válidos.")
            else:
                with col_b:
                    st.warning(f"El archivo de {tag} no tiene oyentes válidos.")
    else:
        if i == 0:
            with col_a:
                st.warning(f"No existe el archivo canciones_{tag}.csv")
        else:
            with col_b:
                st.warning(f"No existe el archivo canciones_{tag}.csv")