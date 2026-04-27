import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Favoritos · Proyecto Musical",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none !important; }

[data-testid="stSidebar"] { background-color: #f3f6fb; }

.sidebar-title { font-size: 24px; font-weight: 800; color: #1f2a44; margin-bottom: 10px; }
.sidebar-section { font-size: 12px; font-weight: 800; color: #8a8f98; letter-spacing: 1px; margin-top: 18px; margin-bottom: 4px; }

div[data-testid="stSidebar"] div.stButton > button {
    width: 100%; height: auto; padding: 6px 8px; border-radius: 8px;
    border: none; background-color: transparent; color: #1f2a44;
    font-size: 15px; font-weight: 500; text-align: left;
    box-shadow: none; transition: color 0.15s ease;
}
div[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: transparent; color: #4f6ef7; border: none; box-shadow: none;
}

/* Botones de añadir favorito */
div[data-testid="stMain"] div.stButton > button {
    height: 36px; border-radius: 8px; border: 1px solid #e5e7eb;
    background-color: white; color: #1f2a44; font-size: 13px;
    font-weight: 500; transition: all 0.15s ease;
}
div[data-testid="stMain"] div.stButton > button:hover {
    background-color: #fefce8; border-color: #fbbf24; color: #92400e;
}

.fav-card {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 16px; border-radius: 12px;
    border: 1px solid #e5e7eb; background: white;
    margin-bottom: 8px;
}
.fav-num { font-size: 18px; font-weight: 800; color: #d1d5db; min-width: 28px; }
.fav-title { font-size: 15px; font-weight: 600; color: #1f2a44; }
.fav-artist { font-size: 13px; color: #6b7280; }
.fav-repro { font-size: 13px; color: #4f6ef7; font-weight: 600; margin-left: auto; }
.empty-state { text-align: center; padding: 60px 20px; color: #9ca3af; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">Analisis Musical Stats</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">HOME</div>', unsafe_allow_html=True)
    if st.button("🏠 Página principal"):
        st.switch_page("app.py")

    st.markdown('<div class="sidebar-section">DASHBOARD</div>', unsafe_allow_html=True)
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")

    st.markdown('<div class="sidebar-section">EXPLORAR</div>', unsafe_allow_html=True)
    if st.button("🎵 Canciones"):
        st.switch_page("pages/1_Semanales.py")
    if st.button("🎤 Artistas"):
        st.switch_page("pages/artistas.py")
    if st.button("🎼 Géneros"):
        st.switch_page("pages/2_Generos.py")

    st.markdown('<div class="sidebar-section">PRODUCTOR</div>', unsafe_allow_html=True)
    if st.button("⭐ Favoritos"):
        st.switch_page("pages/4_Favoritos.py")
    if st.button("📈 Tendencias"):
        st.switch_page("pages/3_Tendencias.py")
    if st.button("🕘 Historial"):
        pass

    st.markdown('<div class="sidebar-section">USUARIO</div>', unsafe_allow_html=True)
    if st.button("👤 Perfil"):
        pass

# ── Inicializa favoritos en session_state ──
if "favoritos" not in st.session_state:
    st.session_state["favoritos"] = []  # lista de dicts {nombre, artista, reproducciones}

# ── Carga canciones populares ──
@st.cache_data
def cargar_canciones():
    path = "data/clean/canciones_populares.csv"
    if os.path.exists(path):
        df = pd.read_csv(path)
        df["reproducciones"] = pd.to_numeric(df["reproducciones"], errors="coerce")
        return df.dropna(subset=["reproducciones"]).sort_values("reproducciones", ascending=False)
    return pd.DataFrame()

canciones_df = cargar_canciones()

# ── HEADER ──
st.title("⭐ Favoritos")
st.markdown("Marca tus canciones favoritas y tenlas siempre a mano.")
st.markdown("---")

# ── DOS COLUMNAS: Buscar + Mis favoritos ──
col_buscar, col_favs = st.columns([1.2, 1], gap="large")

with col_buscar:
    st.subheader("Buscar canciones")

    busqueda = st.text_input("🔍 Busca por nombre o artista", placeholder="Ej: Radiohead, Creep...")

    if not canciones_df.empty:
        if busqueda:
            mask = (
                canciones_df["nombre"].str.contains(busqueda, case=False, na=False) |
                canciones_df["artista"].str.contains(busqueda, case=False, na=False)
            )
            resultados = canciones_df[mask].head(10)
        else:
            resultados = canciones_df.head(20)

        if resultados.empty:
            st.info("No se encontraron canciones.")
        else:
            for _, row in resultados.iterrows():
                nombre   = row.get("nombre", "—")
                artista  = row.get("artista", "—")
                repros   = row.get("reproducciones", 0)
                ya_fav   = any(f["nombre"] == nombre for f in st.session_state["favoritos"])

                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(
                        f'<div style="padding:6px 0;border-bottom:1px solid #f3f4f6;">'
                        f'<div style="font-weight:600;font-size:14px;color:#1f2a44;">{nombre}</div>'
                        f'<div style="font-size:12px;color:#6b7280;">{artista} · {int(repros/1_000_000):.0f}M reproducciones</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                with c2:
                    label = "⭐ Añadida" if ya_fav else "☆ Añadir"
                    if not ya_fav:
                        if st.button(label, key=f"add_{nombre}"):
                            st.session_state["favoritos"].append({
                                "nombre": nombre,
                                "artista": artista,
                                "reproducciones": int(repros)
                            })
                            st.rerun()
                    else:
                        st.markdown(
                            '<span style="color:#fbbf24;font-size:13px;padding:6px 0;display:block;">⭐ En favoritos</span>',
                            unsafe_allow_html=True
                        )
    else:
        st.info("Ejecuta `download.py` para cargar canciones.")

with col_favs:
    st.subheader(f"Mis favoritos ({len(st.session_state['favoritos'])})")

    if not st.session_state["favoritos"]:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-icon">⭐</div>'
            '<div style="font-size:16px;font-weight:600;color:#6b7280;">Aún no tienes favoritos</div>'
            '<div style="font-size:13px;margin-top:6px;">Busca canciones y pulsa ☆ Añadir</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # Botón limpiar todo
        if st.button("🗑️ Limpiar todos"):
            st.session_state["favoritos"] = []
            st.rerun()

        st.markdown("")

        for i, fav in enumerate(st.session_state["favoritos"], 1):
            repros_m = fav['reproducciones'] / 1_000_000
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(
                    f'<div class="fav-card">'
                    f'<div class="fav-num">{i}</div>'
                    f'<div>'
                    f'<div class="fav-title">{fav["nombre"]}</div>'
                    f'<div class="fav-artist">{fav["artista"]} · {repros_m:.1f}M reprod.</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with c2:
                if st.button("✕", key=f"del_{i}_{fav['nombre']}"):
                    st.session_state["favoritos"].pop(i - 1)
                    st.rerun()