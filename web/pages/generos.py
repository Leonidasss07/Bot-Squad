import os
import html
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Géneros · Proyecto Musical",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# imagen del fondo
HERO_IMAGE_URL = "https://i.pinimg.com/736x/44/2c/ce/442cce422c3c8177ae22de9b1028a6b5.jpg"


# estilo de la página
st.markdown(f"""
<style>
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

.sidebar-title {{
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 10px;
}}

.sidebar-section {{
    font-size: 12px;
    font-weight: 800;
    color: #64748b;
    letter-spacing: 1px;
    margin-top: 18px;
    margin-bottom: 4px;
}}

div[data-testid="stSidebar"] div.stButton > button {{
    width: 100%;
    height: auto;
    padding: 8px 10px;
    border-radius: 10px;
    border: none;
    background-color: transparent;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    box-shadow: none;
    transition: all 0.18s ease;
}}

div[data-testid="stSidebar"] div.stButton > button:hover {{
    background-color: var(--secondary-background-color);
    color: #3f5fa8;
}}

.block-container {{
    padding-top: 2rem;
}}

.hero-card {{
    position: relative;
    overflow: hidden;
    border-radius: 30px;
    padding: 36px 36px;
    margin-bottom: 26px;
    border: 1px solid #d9dee8;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.10);
    background-image: url("{HERO_IMAGE_URL}");
    background-size: cover;
    background-position: center 38%;
    background-repeat: no-repeat;
    min-height: 360px;
    display: flex;
    align-items: flex-end;
}}

.hero-content {{
    width: 100%;
    max-width: 850px;
}}

.hero-title {{
    font-size: 44px;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
    line-height: 1.05;
    color: #AFCFCF !important;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.75);
}}

.hero-text {{
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 650;
    line-height: 1.7;
    max-width: 760px;
    margin-top: 14px;
    margin-bottom: 0;
    text-shadow: 0 3px 14px rgba(0, 0, 0, 0.75);
}}

.hero-metrics {{
    display: flex;
    gap: 16px;
    margin-top: 24px;
    flex-wrap: wrap;
}}

.hero-metric-box {{
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 18px;
    padding: 16px 24px;
    flex: 1;
    min-width: 150px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
}}

.hm-label {{
    color: #111827;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.5px;
}}

.hm-value {{
    color: #111827;
    font-size: 28px;
    font-weight: 600;
    margin-top: 4px;
}}


.legend-card {{
    background: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.18);
    border-radius: 24px;
    padding: 22px 24px;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.06);
    margin-top: 8px;
}}

.legend-title {{
    font-size: 22px;
    font-weight: 850;
    margin-bottom: 20px;
}}

.legend-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px 34px;
}}

.legend-item {{
    display: grid;
    grid-template-columns: 18px 1fr auto;
    align-items: start;
    column-gap: 10px;
    min-width: 0;
}}

.legend-color {{
    width: 14px;
    height: 14px;
    border-radius: 5px;
    margin-top: 4px;
    flex-shrink: 0;
}}

.legend-name {{
    font-weight: 800;
    font-size: 14px;
    line-height: 1.2;
}}

.legend-info {{
    text-align: right;
    min-width: 92px;
}}

.legend-percent {{
    color: #52627b;
    font-size: 12px;
    line-height: 1.35;
    margin-bottom: 2px;
    display: block;
    font-weight: 700;
}}

.legend-count {{
    color: #8a97aa;
    font-size: 12px;
    line-height: 1.35;
    display: block;
}}

.song-card {{
    background: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 22px;
    padding: 14px;
    margin-bottom: 14px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.05);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
    min-height: 155px;
}}

.song-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.1);
}}

.song-layout {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
}}

.song-content {{
    flex: 1;
    min-width: 0;
}}

.song-topline {{
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 8px;
}}

.song-rank {{
    min-width: 30px;
    height: 30px;
    border-radius: 10px;
    background: var(--background-color);
    border: 1px solid rgba(128, 128, 128, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3d5f99;
    font-size: 13px;
    font-weight: 800;
}}

.song-name {{
    font-weight: 800;
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.song-artist {{
    color: #7b8798;
    font-size: 14px;
    margin-top: 4px;
}}

.song-meta {{
    color: #64748b;
    font-size: 12px;
    margin-top: 9px;
}}

.song-button {{
    display: inline-block;
    margin-top: 12px;
    background: linear-gradient(135deg, #DCE8D8 0%, #AFCFCF 100%);
    color: #1f2937 !important;
    text-decoration: none !important;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 760;
    border: 1px solid #AFCFCF;
}}

.song-button:hover {{
    color: #111827 !important;
    background: linear-gradient(135deg, #AFCFCF 0%, #78AFC4 100%);
    border: 1px solid #78AFC4;
}}

.song-button-disabled {{
    display: inline-block;
    margin-top: 12px;
    background: var(--background-color);
    color: #475569 !important;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 650;
    border: 1px solid rgba(128, 128, 128, 0.2);
}}

.song-cover {{
    width: 100px;
    height: 100px;
    border-radius: 18px;
    overflow: hidden;
    flex-shrink: 0;
    border: 1px solid rgba(128, 128, 128, 0.2);
    background: linear-gradient(135deg, #222831 0%, #101418 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.song-cover img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.song-cover-placeholder {{
    font-size: 24px;
    font-weight: 800;
    color: #475569;
}}

@media (max-width: 900px) {{
    .hero-card {{
        padding: 24px 20px;
        min-height: 420px;
        background-position: center;
    }}

    .hero-title {{
        font-size: 34px;
    }}

    .song-layout {{
        flex-direction: column-reverse;
        align-items: flex-start;
    }}

    .song-cover {{
        width: 100px;
        height: 100px;
    }}

    .legend-grid {{
        grid-template-columns: 1fr;
    }}
}}
</style>
""", unsafe_allow_html=True)


COLORS = [
    "#7C002F",
    "#A6294B",
    "#C85A69",
    "#E08A72",
    "#F0D2B2",
    "#DCE8D8",
    "#AFCFCF",
    "#78AFC4",
    "#477EAE",
    "#1A2E78"
]


# limpiar texto
def texto_seguro(valor):
    if pd.isna(valor):
        return ""
    return html.escape(str(valor))


# limpiar html
def html_block(texto):
    lineas = texto.splitlines()
    lineas_limpias = [linea.strip() for linea in lineas if linea.strip()]
    return "\n".join(lineas_limpias)


# obtener enlace
def obtener_url_fila(row):
    for col in ["url", "url_popular"]:
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip() != "":
            return str(row[col]).strip()
    return ""


# obtener imagen
def obtener_imagen_fila(row):
    posibles = ["imagen", "image", "image_url", "cover_url", "cover", "artwork"]

    imagenes_genericas = [
        "2a96cbd8b46e442fc41c2b86b821562f",
        "c6f59c1e5e7240a4c0d427abd71f3dbb"
    ]

    for col in posibles:
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip() != "":
            url = str(row[col]).strip()

            if any(generica in url for generica in imagenes_genericas):
                continue

            return url

    return ""


# formatear reproducciones
def obtener_valor_formateado(row, valor_col, usar_ranking):
    if usar_ranking:
        return f"Posición {row.get('posición', '')}"

    if valor_col in row.index and pd.notna(row[valor_col]):
        try:
            valor = float(row[valor_col])
            if valor >= 1_000_000:
                return f"{valor / 1_000_000:.1f}M reproducciones"
            return f"{int(valor):,} reproducciones"
        except Exception:
            return str(row[valor_col])

    return ""


# menú
with st.sidebar:
    st.markdown('<div class="sidebar-title">Music Stats</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">HOME</div>', unsafe_allow_html=True)
    if st.button("Página principal"):
        st.switch_page("app.py")

    st.markdown('<div class="sidebar-section">DASHBOARD</div>', unsafe_allow_html=True)
    if st.button("Dashboard"):
        st.switch_page("pages/dashboard.py")

    st.markdown('<div class="sidebar-section">EXPLORAR</div>', unsafe_allow_html=True)
    if st.button("Canciones"):
        st.switch_page("pages/1_Semanales.py")
    if st.button("Artistas"):
        st.switch_page("pages/artistas.py")
    if st.button("Géneros"):
        st.switch_page("pages/2_Generos.py")

    st.markdown('<div class="sidebar-section">PRODUCTOR</div>', unsafe_allow_html=True)
    if st.button("Mi catálogo"):
        pass
    if st.button("Tendencias"):
        st.switch_page("pages/3_Tendencias.py")
    if st.button("Historial"):
        pass

    st.markdown('<div class="sidebar-section">USUARIO</div>', unsafe_allow_html=True)
    if st.button("Perfil"):
        pass


# cargar datos de géneros
gen_path = "data/clean/generos_canciones.csv"

if os.path.exists(gen_path):
    gen_df = pd.read_csv(gen_path)
    conteo_generos = gen_df["generos"].value_counts().head(10).reset_index()
    conteo_generos.columns = ["género", "cantidad"]
else:
    conteo_generos = pd.DataFrame({
        "género": ["pop", "rock", "alternative", "rnb", "indie", "dance", "rap", "hip-hop", "electronic", "synthpop"],
        "cantidad": [352, 220, 144, 139, 134, 82, 74, 71, 58, 53]
    })


# calcular métricas
total = conteo_generos["cantidad"].sum()
conteo_generos["porcentaje"] = (conteo_generos["cantidad"] / total * 100).round(1).astype(str) + "%"
genero_top = conteo_generos.iloc[0]["género"].capitalize()
total_generos = len(conteo_generos)


# cabecera principal
st.markdown(
    html_block(f"""
    <div class="hero-card">
        <div class="hero-content">
            <h1 class="hero-title">Explorador de géneros</h1>
            <p class="hero-text">
                Descubre qué estilos aparecen con más frecuencia explora canciones destacadas por género.
            </p>
            <div class="hero-metrics">
                <div class="hero-metric-box">
                    <div class="hm-label">GÉNEROS ENCONTRADOS</div>
                    <div class="hm-value">{total_generos}</div>
                </div>
                <div class="hero-metric-box">
                    <div class="hm-label">GÉNERO MÁS POPULAR</div>
                    <div class="hm-value">{genero_top}</div>
                </div>
                <div class="hero-metric-box">
                    <div class="hm-label">CANCIONES REVISADAS</div>
                    <div class="hm-value">{total:,}</div>
                </div>
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True
)

st.markdown("---")


# composición del catálogo
st.subheader("Composición del catálogo")

col_pie, col_legend = st.columns([0.95, 1.05], gap="large")

with col_pie:
    plt.rcdefaults()
    fig2, ax2 = plt.subplots(figsize=(4.6, 4.0))

    wedges, texts, autotexts = ax2.pie(
        conteo_generos["cantidad"],
        labels=None,
        colors=COLORS[:len(conteo_generos)],
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.48, edgecolor="none")
    )

    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#1a1a1a")
        at.set_fontweight("bold")

    ax2.set_facecolor("none")
    fig2.patch.set_facecolor("none")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

with col_legend:
    legend_html = """
    <div class="legend-card">
        <div class="legend-title">Estilos Musicales</div>
        <div class="legend-grid">
    """

    for i, row in conteo_generos.iterrows():
        color = COLORS[i % len(COLORS)]
        legend_html += f"""
        <div class="legend-item">
            <div class="legend-color" style="background-color:{color};"></div>
            <div class="legend-name">{texto_seguro(row['género']).capitalize()}</div>
            <div class="legend-info">
                <div class="legend-percent">{row['porcentaje']}</div>
                <div class="legend-count">{row['cantidad']:,} canciones</div>
            </div>
        </div>
        """

    legend_html += """
        </div>
    </div>
    """

    st.markdown(html_block(legend_html), unsafe_allow_html=True)

st.markdown("---")


# canciones destacadas por género
st.subheader("Canciones destacadas por género")

TAGS_TODOS = ["disco", "rock", "pop", "jazz", "hip-hop", "k-pop"]
TAGS_DISPONIBLES = [t for t in TAGS_TODOS if os.path.exists(f"data/clean/canciones_{t}.csv")]

if not TAGS_DISPONIBLES:
    st.info("No se encontraron archivos de géneros. Ejecuta `download.py` primero.")
else:
    genero_elegido = st.selectbox(
        "Elige un género para explorar canciones populares:",
        options=TAGS_DISPONIBLES,
        format_func=lambda x: x.upper()
    )

    tag_path = f"data/clean/canciones_{genero_elegido}.csv"
    tag_df = pd.read_csv(tag_path)

    for col in ["nombre", "name", "track", "cancion"]:
        if col in tag_df.columns:
            nombre_col = col
            break
    else:
        nombre_col = tag_df.columns[0]

    artista_col = None
    for col in ["artista", "artist"]:
        if col in tag_df.columns:
            artista_col = col
            break

    pop_path = "data/clean/canciones_populares.csv"

    if os.path.exists(pop_path):
        pop_df = pd.read_csv(pop_path)

        if "reproducciones" in pop_df.columns:
            pop_df["reproducciones"] = pd.to_numeric(pop_df["reproducciones"], errors="coerce")

        if "nombre" in pop_df.columns:
            pop_df["nombre_lower"] = pop_df["nombre"].astype(str).str.lower().str.strip()
            tag_df["nombre_lower"] = tag_df[nombre_col].astype(str).str.lower().str.strip()

            columnas_merge = ["nombre_lower"]

            for extra_col in ["reproducciones", "url", "imagen", "image", "image_url", "cover_url", "cover", "artwork"]:
                if extra_col in pop_df.columns:
                    columnas_merge.append(extra_col)

            tag_df = tag_df.merge(
                pop_df[columnas_merge],
                on="nombre_lower",
                how="left",
                suffixes=("", "_popular")
            ).drop(columns=["nombre_lower"])

            for img_col in ["imagen", "image", "image_url", "cover_url", "cover", "artwork"]:
                pop_col = f"{img_col}_popular"
                if pop_col in tag_df.columns and img_col not in tag_df.columns:
                    tag_df[img_col] = tag_df[pop_col]

            if "url_popular" in tag_df.columns and "url" not in tag_df.columns:
                tag_df["url"] = tag_df["url_popular"]

    valor_col = None

    for col in ["reproducciones", "oyentes", "listeners", "playcount"]:
        if col in tag_df.columns:
            tag_df[col] = pd.to_numeric(tag_df[col], errors="coerce")

            if tag_df[col].notna().sum() > 0:
                tag_df = tag_df.sort_values(col, ascending=False).head(10).reset_index(drop=True)
                valor_col = col
                usar_ranking = False
                break

    if valor_col is None:
        tag_df = tag_df.head(10).reset_index(drop=True)
        tag_df["posición"] = range(1, len(tag_df) + 1)
        valor_col = "posición"
        usar_ranking = True

    st.markdown(f"#### Canciones de {genero_elegido.upper()}")

    columnas_canciones = st.columns(2)

    for i, row in tag_df.iterrows():
        nombre = texto_seguro(row[nombre_col])
        artista = texto_seguro(row[artista_col]) if artista_col else "Artista no disponible"
        url = obtener_url_fila(row)
        imagen = obtener_imagen_fila(row)
        meta = texto_seguro(obtener_valor_formateado(row, valor_col, usar_ranking))
        rank = i + 1

        if imagen:
            cover_html = f'<div class="song-cover"><img src="{html.escape(imagen)}" alt="{nombre}"></div>'
        else:
            initial = nombre[:1].upper() if nombre else "♪"
            cover_html = f'<div class="song-cover"><div class="song-cover-placeholder">{initial}</div></div>'

        if url:
            boton = f'<a class="song-button" href="{html.escape(url)}" target="_blank">Ver en Last.fm</a>'
        else:
            boton = '<span class="song-button-disabled">Sin enlace</span>'

        with columnas_canciones[i % 2]:
            st.markdown(
                html_block(f"""
                <div class="song-card">
                    <div class="song-layout">
                        <div class="song-content">
                            <div class="song-topline">
                                <div class="song-rank">{rank}</div>
                                <div class="song-name">{nombre}</div>
                            </div>
                            <div class="song-artist">{artista}</div>
                            <div class="song-meta">{meta}</div>
                            {boton}
                        </div>
                        {cover_html}
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

    st.markdown("---")

    # gráficas
    st.subheader("Análisis en gráficas")

    col_graf_generos, col_graf_repro = st.columns(2, gap="large")

    with col_graf_generos:
        st.markdown("#### Gráfica de géneros")

        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        bar_colors = COLORS[:len(conteo_generos)]

        bars = ax.barh(
            conteo_generos["género"][::-1],
            conteo_generos["cantidad"][::-1],
            color=bar_colors[::-1],
            height=0.62,
            edgecolor="none"
        )

        ax.set_xlabel("Cantidad de canciones", fontsize=10)
        ax.tick_params(axis="y", labelsize=11)
        ax.tick_params(axis="x", labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_alpha(0.3)
        ax.grid(axis="x", alpha=0.3)

        max_val = conteo_generos["cantidad"].max()
        max_val = max_val if max_val > 0 else 1
        ax.set_xlim(0, max_val * 1.22)

        for bar, val in zip(bars, conteo_generos["cantidad"][::-1]):
            ax.text(
                bar.get_width() + max_val * 0.02,
                bar.get_y() + bar.get_height() / 2,
                str(val),
                va="center",
                fontsize=9,
                fontweight="bold"
            )

        ax.set_facecolor("none")
        fig.patch.set_facecolor("none")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_graf_repro:
        if valor_col and len(tag_df) > 0:
            titulo_grafica = "Ranking de canciones" if usar_ranking else "Reproducciones por canción"
            st.markdown(f"#### {titulo_grafica}")

            plt.rcdefaults()
            fig3, ax3 = plt.subplots(figsize=(6.5, 4.5))

            nombres = tag_df[nombre_col].astype(str).str[:28].tolist()
            valores_raw = tag_df[valor_col].tolist()

            if not usar_ranking:
                valores_plot = [v / 1_000_000 for v in valores_raw]
                xlabel = "Reproducciones en millones"
            else:
                valores_plot = valores_raw
                xlabel = "Posición"

            bar_colors = COLORS[:len(tag_df)]

            bars3 = ax3.barh(
                nombres[::-1],
                valores_plot[::-1],
                color=bar_colors[::-1],
                height=0.62,
                edgecolor="none"
            )

            ax3.set_xlabel(xlabel, fontsize=10)
            ax3.tick_params(axis="y", labelsize=10)
            ax3.tick_params(axis="x", labelsize=8)
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            ax3.spines["left"].set_visible(False)
            ax3.spines["bottom"].set_alpha(0.3)
            ax3.grid(axis="x", alpha=0.3)

            max_val = max(valores_plot) if valores_plot and max(valores_plot) > 0 else 1
            ax3.set_xlim(0, max_val * 1.3)

            for i, (bar, vplot, vraw) in enumerate(zip(bars3, valores_plot[::-1], valores_raw[::-1])):
                label = f"#{len(valores_raw) - i}" if usar_ranking else f"{vraw / 1_000_000:.1f}M"

                ax3.text(
                    bar.get_width() + max_val * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    label,
                    va="center",
                    fontsize=9,
                    fontweight="bold"
                )

            ax3.set_facecolor("none")
            fig3.patch.set_facecolor("none")
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()