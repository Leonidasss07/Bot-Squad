import os
import pandas as pd


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