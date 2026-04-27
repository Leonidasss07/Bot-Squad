import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tendencias", layout="wide")

st.title("📈 Tendencias")

tab1, tab2 = st.tabs(["Semana 1", "Semana 2"])

with tab1:
    df1 = pd.DataFrame({
        "nombre": ["Like a Tattoo", "Take Five"],
        "artista": ["Sade", "Brubeck"]
    })
    st.dataframe(df1, use_container_width=True)

with tab2:
    df2 = pd.DataFrame({
        "nombre": ["Back to Black", "Paradise"],
        "artista": ["Amy", "Sade"]
    })
    st.dataframe(df2, use_container_width=True)