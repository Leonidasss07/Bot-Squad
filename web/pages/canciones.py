import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import ScalarFormatter

st.set_page_config(page_title="Proyecto Musical", layout="wide")

st.title("Canciones Populares")

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
mes_actual = meses[datetime.now().month]

st.caption(f"Última sincronización con Last.fm: {mes_actual}")

canciones = pd.read_csv("data/clean/canciones_populares.csv")

canciones["reproducciones"] = pd.to_numeric(canciones["reproducciones"], errors="coerce")

canciones_ordenadas = canciones.sort_values(by="reproducciones", ascending=False)

col1, col_tabla = st.columns(2)


with col1:
    st.subheader("Top Artistas")
    df_mostrar = canciones_ordenadas.head(10).copy()
    df_mostrar["reproducciones"] = df_mostrar["reproducciones"].map('{:,.0f}'.format)
    st.dataframe(df_mostrar, use_container_width=True)



with col_tabla:
    st.subheader("Canciones más populares")


    top_canciones = canciones.sort_values(by="reproducciones", ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.barh(top_canciones["nombre"], top_canciones["reproducciones"])
    ax2.invert_yaxis()
    ax2.set_title("Canciones más populares")
    ax2.set_xlabel("Cantidad")
    ax2.set_ylabel("Nombre")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    ax2.xaxis.set_major_formatter(ScalarFormatter())
    ax2.ticklabel_format(style='plain', axis='x')
    st.pyplot(fig2)

    plt.show()