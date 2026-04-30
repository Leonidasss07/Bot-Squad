import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Géneros · Proyecto Musical",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none !important; }

[data-testid="stSidebar"] {
    background-color: #f3f6fb;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #1f2a44;
    margin-bottom: 10px;
}

.sidebar-section {
    font-size: 12px;
    font-weight: 800;
    color: #8a8f98;
    letter-spacing: 1px;
    margin-top: 18px;
    margin-bottom: 4px;
}

/* Botones sidebar como texto simple */
div[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    height: auto;
    padding: 6px 8px;
    border-radius: 8px;
    border: none;
    background-color: transparent;
    color: #1f2a44;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    box-shadow: none;
    transition: color 0.15s ease;
}
div[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: transparent;
    color: #4f6ef7;
    border: none;
    box-shadow: none;
}

""", unsafe_allow_html=True)

# Menu
with st.sidebar:
    st.markdown('<div class="sidebar-title">Analisis Musical Stats</div>', unsafe_allow_html=True)

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

COLORS = ["#4f6ef7","#6c82f8","#8997f9","#a6acfa","#c3c1fb",
          "#3a5bd9","#5570f0","#7088f5","#99a9f9","#bbc3fc"]



gen_path = "data/clean/generos_canciones.csv"
if os.path.exists(gen_path):
    gen_df = pd.read_csv(gen_path)
    conteo_generos = gen_df["generos"].value_counts().head(10).reset_index()
    conteo_generos.columns = ["género", "cantidad"]
else:
    conteo_generos = pd.DataFrame({
        "género":   ["pop","rock","alternative","rnb","indie","dance","rap","hip-hop","electronic","synthpop"],
        "cantidad": [352, 220, 144, 139, 134, 82, 74, 71, 58, 53]
    })

total = conteo_generos["cantidad"].sum()
conteo_generos["porcentaje"] = (conteo_generos["cantidad"] / total * 100).round(1).astype(str) + "%"
genero_top = conteo_generos.iloc[0]["género"].capitalize()
total_generos = len(conteo_generos)

st.title("🎼 Géneros")
st.markdown("Distribución de géneros musicales extraída de **Last.fm**.")
st.markdown("---")

m1, m2, m3 = st.columns(3)
m1.metric("🎼 Géneros analizados", total_generos)
m2.metric("🏆 Género dominante", genero_top)
m3.metric("🎵 Total canciones", f"{total:,}")

st.markdown("---")

col_izq, col_der = st.columns([1, 1.4], gap="large")

with col_izq:
    st.subheader("Tabla de géneros")
    tabla_display = conteo_generos[["género", "cantidad", "porcentaje"]].copy()
    st.dataframe(
        tabla_display.style.bar(subset=["cantidad"], color="#c7d3fc"),
        use_container_width=True,
        hide_index=True
    )

with col_der:
    st.subheader("Gráfica de géneros")
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bar_colors = COLORS[:len(conteo_generos)]
    bars = ax.barh(
        conteo_generos["género"][::-1],
        conteo_generos["cantidad"][::-1],
        color=bar_colors[::-1],
        height=0.6, edgecolor="none"
    )
    ax.set_xlabel("Cantidad de canciones", fontsize=10, color="#555")
    ax.tick_params(axis="y", labelsize=11)
    ax.tick_params(axis="x", labelsize=9, colors="#888")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, conteo_generos["cantidad"].max() * 1.2)
    for bar, val in zip(bars, conteo_generos["cantidad"][::-1]):
        ax.text(
            bar.get_width() + conteo_generos["cantidad"].max() * 0.02,
            bar.get_y() + bar.get_height() / 2,
            str(val), va="center", color="#555", fontsize=9, fontweight="bold"
        )
    ax.set_facecolor("#fafbff")
    fig.patch.set_facecolor("#fafbff")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

st.subheader("Reparto por género")
col_pie, col_info = st.columns([1, 1], gap="large")

with col_pie:
    plt.rcdefaults()
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax2.pie(
        conteo_generos["cantidad"],
        labels=conteo_generos["género"],
        colors=COLORS[:len(conteo_generos)],
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.82,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2)
    )
    for t in texts:
        t.set_fontsize(9)
        t.set_color("#333")
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("#333")
    ax2.set_facecolor("#fafbff")
    fig2.patch.set_facecolor("#fafbff")
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

with col_info:
    st.markdown("#### Top géneros")
    for i, row in conteo_generos.iterrows():
        color = COLORS[i % len(COLORS)]
        pct = row["porcentaje"]
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;'
            f'border-bottom:1px solid #eee;">'
            f'<div style="width:12px;height:12px;border-radius:50%;'
            f'background:{color};flex-shrink:0;"></div>'
            f'<span style="flex:1;font-size:14px;color:#1f2a44;font-weight:500;">'
            f'{row["género"].capitalize()}</span>'
            f'<span style="font-size:13px;color:#888;">{row["cantidad"]:,}</span>'
            f'<span style="font-size:12px;color:{color};font-weight:700;'
            f'min-width:42px;text-align:right;">{pct}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

st.subheader("🔍 Canciones más populares por género")
st.markdown("Selecciona un género para ver sus canciones más escuchadas.")

TAGS_TODOS = ["disco", "rock", "pop", "jazz", "hip-hop", "k-pop"]
TAGS_DISPONIBLES = [t for t in TAGS_TODOS if os.path.exists(f"data/clean/canciones_{t}.csv")]

if not TAGS_DISPONIBLES:
    st.info("No se encontraron archivos de géneros. Ejecuta `download.py` primero.")
else:
    genero_elegido = st.selectbox(
        "Elige un género:",
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

  
    pop_path = "data/clean/canciones_populares.csv"
    if os.path.exists(pop_path):
        pop_df = pd.read_csv(pop_path)
        pop_df["reproducciones"] = pd.to_numeric(pop_df["reproducciones"], errors="coerce")
        pop_df["nombre_lower"] = pop_df["nombre"].astype(str).str.lower().str.strip()
        tag_df["nombre_lower"] = tag_df[nombre_col].astype(str).str.lower().str.strip()
        tag_df = tag_df.merge(
            pop_df[["nombre_lower", "reproducciones"]],
            on="nombre_lower", how="left"
        ).drop(columns=["nombre_lower"])


    valor_col = None
    for col in ["reproducciones", "oyentes", "listeners", "playcount"]:
        if col in tag_df.columns:
            tag_df[col] = pd.to_numeric(tag_df[col], errors="coerce")
            if tag_df[col].notna().sum() > 0:
                tag_df = tag_df.sort_values(col, ascending=False).head(10)
                valor_col = col
                usar_ranking = False
                break

  
    if valor_col is None:
        tag_df = tag_df.head(10).reset_index(drop=True)
        tag_df["posición"] = range(1, len(tag_df) + 1)
        valor_col = "posición"
        usar_ranking = True

    col_t, col_g = st.columns([1, 1.4], gap="large")

    with col_t:
        st.markdown(f"#### Top canciones · {genero_elegido.upper()}")
        cols_show = [c for c in [nombre_col, "artista", "artist"] if c and c in tag_df.columns]
        tabla_show = tag_df[cols_show].reset_index(drop=True)
        tabla_show.insert(0, "#", range(1, len(tabla_show) + 1))
        st.dataframe(tabla_show, use_container_width=True, hide_index=True)

    with col_g:
        if valor_col and len(tag_df) > 0:
            titulo_grafica = "Ranking de canciones" if usar_ranking else "Reproducciones por canción"
            st.markdown(f"#### {titulo_grafica}")
            plt.rcdefaults()
            fig3, ax3 = plt.subplots(figsize=(7, 4.5))

            nombres = tag_df[nombre_col].astype(str).str[:28].tolist()
            valores_raw = tag_df[valor_col].tolist()

            # Divide entre millones para que el eje no use notacion cientifica
            if not usar_ranking:
                valores_plot = [v / 1_000_000 for v in valores_raw]
                xlabel = "Reproducciones (millones)"
            else:
                valores_plot = valores_raw
                xlabel = "Posición"

            bar_colors = COLORS[:len(tag_df)]
            bars3 = ax3.barh(
                nombres[::-1],
                valores_plot[::-1],
                color=bar_colors,
                height=0.6, edgecolor="none"
            )
            ax3.set_xlabel(xlabel, fontsize=10, color="#555")
            ax3.tick_params(axis="y", labelsize=10)
            ax3.tick_params(axis="x", labelsize=8, colors="#888")
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            ax3.spines["left"].set_visible(False)
            ax3.set_xlim(0, max(valores_plot) * 1.3)
            for i, (bar, vplot, vraw) in enumerate(zip(bars3, valores_plot[::-1], valores_raw[::-1])):
                label = f"#{len(valores_raw) - i}" if usar_ranking else f"{vraw/1_000_000:.1f}M"
                ax3.text(
                    bar.get_width() + max(valores_plot) * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    label, va="center", color="#555", fontsize=9, fontweight="bold"
                )

            ax3.set_facecolor("#fafbff")
            fig3.patch.set_facecolor("#fafbff")
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()