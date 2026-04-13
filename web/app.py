import pandas as pd
import streamlit as st 

st.title("Analisis Bot Squad")
st.subheader("Resumen - datos")

df= pd.read_csv("../data/clean/generos_canciones.csv")

st.write(df.head(3))

st.write(df["generos"].count())
