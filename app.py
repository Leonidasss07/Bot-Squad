import streamlit as st
import pandas as pd

st.title("Musica")

st.subheader("Resumen - datos")

df = pd.read_csv("..data/clean/generos_canciones.csv")

st.write(df.head(3))

st.write(df["title"].count())