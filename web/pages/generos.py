import os
import html
import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Géneros",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ruta de la imagen
HERO_IMAGE_PATH = "web/assets/generos_bg.jpeg"


def image_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


HERO_IMAGE_BASE64 = image_to_base64(HERO_IMAGE_PATH)

st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: #000000 !important;
    color: #ffffff !important;
}}

header, footer, #MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

[data-testid="stAppViewContainer"] > .main {{
    background: #000000 !important;
}}

.block-container {{
    max-width: 100% !important;
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

hr {{
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin-top: 1.8rem !important;
    margin-bottom: 1.8rem !important;
}}

h1, h2, h3, h4, p, label, div {{
    color: inherit;
}}

.menu-superior {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 42px;

    height: 240px;
    margin-top: 0;

    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);

    background-image:
        linear-gradient(to right, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to left, rgba(0,0,0,0.75), rgba(0,0,0,0) 25%),
        linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.95)),
        url("data:image/jpeg;base64,{HERO_IMAGE_BASE64}");

    background-size: cover;
    background-position: center top;
    background-repeat: no-repeat;

    position: relative;
    z-index: 10;
}}

.menu-superior a {{
    color: white;
    text-decoration: none;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 3px;
    font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
    text-transform: uppercase;
    transform: translateY(42px);
    text-shadow: 0 3px 12px rgba(0,0,0,0.85);
}}

.menu-superior a:hover {{
    color: #AFCFCF;
}}

.hero-card {{
    position: relative;
    overflow: hidden;
    border: none;
    border-radius: 0;
    margin-top: 0;
    margin-bottom: 24px;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    width: 100vw;
    min-height: 350px;
    background: #000000;
    display: flex;
    align-items: center;
}}

.hero-content {{
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    padding: 20px 48px 38px 48px;
    text-align: center;
}}

.hero-title {{
    font-size: 44px;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
    line-height: 1.05;
    color: #ffffff !important;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.75);
}}

.hero-text {{
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 650;
    line-height: 1.7;
    max-width: 760px;
    margin: 14px auto 0 auto;
    text-shadow: 0 3px 14px rgba(0, 0, 0, 0.75);
    text-align: center;
}}

.hero-metrics {{
    display: flex;
    justify-content: center;
    gap: 16px;
    margin: 20px auto 0 auto;
    flex-wrap: wrap;
    max-width: 980px;
}}

.hero-metric-box {{
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 18px 26px;
    flex: 1;
    min-width: 180px;
    max-width: 280px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
    text-align: left;
}}

.hm-label {{
    color: #ffffff;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.5px;
}}

.hm-value {{
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    margin-top: 4px;
}}

h3 {{
    color: #ffffff !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    margin-top: 0.5rem !important;
}}

h4 {{
    color: #ffffff !important;
}}

.legend-card {{
    background: #0d0d0d;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 22px 24px;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
    margin-top: 8px;
}}

.legend-title {{
    font-size: 22px;
    font-weight: 850;
    margin-bottom: 20px;
    color: #ffffff;
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
    color: #ffffff;
}}

.legend-info {{
    text-align: right;
    min-width: 92px;
}}

.legend-percent {{
    color: #d4d4d4;
    font-size: 12px;
    line-height: 1.35;
    margin-bottom: 2px;
    display: block;
    font-weight: 700;
}}

.legend-count {{
    color: #9ca3af;
    font-size: 12px;
    line-height: 1.35;
    display: block;
}}

.song-card {{
    background: #0d0d0d;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    padding: 14px;
    margin-bottom: 14px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.10);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
    min-height: 155px;
}}

.song-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
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
    background: #111111;
    border: 1px solid rgba(255, 255, 255, 0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #AFCFCF;
    font-size: 13px;
    font-weight: 800;
}}

.song-name {{
    font-weight: 800;
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #ffffff;
}}

.song-artist {{
    color: #b5b9c2;
    font-size: 14px;
    margin-top: 4px;
}}

.song-meta {{
    color: #9ca3af;
    font-size: 12px;
    margin-top: 9px;
}}

.song-button {{
    display: inline-block;
    margin-top: 12px;
    background: linear-gradient(135deg, #DCE8D8 0%, #AFCFCF 100%);
    color: #111827 !important;
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
    background: #111111;
    color: #94a3b8 !important;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 650;
    border: 1px solid rgba(255, 255, 255, 0.08);
}}

.song-cover {{
    width: 100px;
    height: 100px;
    border-radius: 18px;
    overflow: hidden;
    flex-shrink: 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
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

.stSelectbox label {{
    color: #ffffff !important;
    font-weight: 700 !important;
}}

div[data-baseweb="select"] > div {{
    background-color: #0d0d0d !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    color: #ffffff !important;
}}

@media (max-width: 900px) {{
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    .menu-superior {{
        height: 220px;
        gap: 18px;
        flex-wrap: wrap;
    }}

    .menu-superior a {{
        font-size: 12px;
        letter-spacing: 2px;
    }}

    .hero-card {{
        min-height: 400px;
    }}

    .hero-content {{
        padding: 0 22px 26px 22px;
    }}

    .hero-title {{
        font-size: 34px;
    }}

    .hero-metric-box {{
        max-width: none;
        min-width: 100%;
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

<div class="menu-superior">
    <a href="/" target="_self">INICIO</a>
    <a href="/dashboard" target="_self">DASHBOARD</a>
    <a href="/canciones" target="_self">CANCIONES</a>
    <a href="/artistas" target="_self">ARTISTAS</a>
    <a href="/generos" target="_self">GENEROS</a>
    <a href="/favoritos" target="_self">FAVORITOS</a>
</div>
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


def texto_seguro(valor):
    if pd.isna(valor):
        return ""
    return html.escape(str(valor))


def html_block(texto):
    lineas = texto.splitlines()
    lineas_limpias = [linea.strip() for linea in lineas if linea.strip()]
    return "\n".join(lineas_limpias)

def obtener_imagen_fila(row):
    posibles = ["imagen url", "imagen_url"]
    
    for col in posibles:
        if col in row.index and pd.notna(row[col]):
            url = str(row[col]).strip()
            if url.startswith("http"):
                return url
    return ""

def obtener_url_fila(row):

    if "url" in row.index and pd.notna(row["url"]):
        return str(row["url"]).strip()
    return ""


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

total = conteo_generos["cantidad"].sum()
conteo_generos["porcentaje"] = (conteo_generos["cantidad"] / total * 100).round(1).astype(str) + "%"
genero_top = conteo_generos.iloc[0]["género"].capitalize()
total_generos = len(conteo_generos)


st.markdown(
    html_block(f"""
    <div class="hero-card">
        <div class="hero-content">
            <h1 class="hero-title">Explorador de géneros</h1>
            <p class="hero-subtitle">
                Descubre qué estilos aparecen con más frecuencia y explora canciones destacadas por género.
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

st.subheader("Composición del catálogo")

col_pie, col_legend = st.columns([0.95, 1.05], gap="large")

with col_pie:
    plt.rcdefaults()
    fig2, ax2 = plt.subplots(figsize=(4.6, 4.0))
    fig2.patch.set_facecolor("#000000")
    ax2.set_facecolor("#000000")

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

        for extra_col in [
            "reproducciones",
            "url",
            "audio_url",
            "imagen_url",
            "imagen",
            "image",
            "image_url",
            "cover_url",
            "cover",
            "artwork"
        ]:
            if extra_col in pop_df.columns and extra_col not in columnas_merge:
                columnas_merge.append(extra_col)

        tag_df = tag_df.merge(
            pop_df[columnas_merge],
            on="nombre_lower",
            how="left",
            suffixes=("", "_popular")
        ).drop(columns=["nombre_lower"])

        for col in ["reproducciones", "url", "audio_url", "imagen_url"]:
            pop_col = f"{col}_popular"

            if pop_col in tag_df.columns:
                if col not in tag_df.columns:
                    tag_df[col] = tag_df[pop_col]
                else:
                    tag_df[col] = tag_df[col].fillna(tag_df[pop_col])

        for img_col in ["imagen", "image", "image_url", "cover_url", "cover", "artwork"]:
            pop_col = f"{img_col}_popular"

            if pop_col in tag_df.columns and img_col not in tag_df.columns:
                tag_df[img_col] = tag_df[pop_col]

        tag_df = tag_df.loc[:, ~tag_df.columns.duplicated()]

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
        audio = str(row.get("audio_url", "")).strip()
        meta = texto_seguro(obtener_valor_formateado(row, valor_col, usar_ranking))
        rank = i + 1

        if imagen:
            cover_html = f'<div class="song-cover"><img src="{imagen}" style="width:100%; height:100%; object-fit:cover;"></div>'
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

        if audio.startswith("http"):
            st.audio(audio, format="audio/mp3")
        else:
            st.caption("Audio no disponible")

    st.markdown("---")

    st.subheader("Análisis en gráficas")

    col_graf_generos, col_graf_repro = st.columns(2, gap="large")

    with col_graf_generos:
        st.markdown("#### Gráfica de géneros")

        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(6.5, 4.5))
        fig.patch.set_facecolor("#000000")
        ax.set_facecolor("#000000")
        bar_colors = COLORS[:len(conteo_generos)]

        bars = ax.barh(
            conteo_generos["género"][::-1],
            conteo_generos["cantidad"][::-1],
            color=bar_colors[::-1],
            height=0.62,
            edgecolor="none"
        )

        ax.set_xlabel("Cantidad de canciones", fontsize=10, color="#ffffff")
        ax.tick_params(axis="y", labelsize=11, colors="#ffffff")
        ax.tick_params(axis="x", labelsize=9, colors="#ffffff")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_alpha(0.3)
        ax.spines["bottom"].set_color("#ffffff")
        ax.grid(axis="x", alpha=0.2, color="#ffffff")

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
                fontweight="bold",
                color="#ffffff"
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_graf_repro:
        if valor_col and len(tag_df) > 0:
            titulo_grafica = "Ranking de canciones" if usar_ranking else "Reproducciones por canción"
            st.markdown(f"#### {titulo_grafica}")

            plt.rcdefaults()
            fig3, ax3 = plt.subplots(figsize=(6.5, 4.5))
            fig3.patch.set_facecolor("#000000")
            ax3.set_facecolor("#000000")

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

            ax3.set_xlabel(xlabel, fontsize=10, color="#ffffff")
            ax3.tick_params(axis="y", labelsize=10, colors="#ffffff")
            ax3.tick_params(axis="x", labelsize=8, colors="#ffffff")
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            ax3.spines["left"].set_visible(False)
            ax3.spines["bottom"].set_alpha(0.3)
            ax3.spines["bottom"].set_color("#ffffff")
            ax3.grid(axis="x", alpha=0.2, color="#ffffff")

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
                    fontweight="bold",
                    color="#ffffff"
                )

            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()