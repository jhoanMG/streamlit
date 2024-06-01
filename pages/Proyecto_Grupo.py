import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Filtros")

st.sidebar.title("Nuevas Tecnologias")

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)
st.title("Intoxicaciones por sustancias psicoactivas")
df = pd.read_csv('datasets/intoxicacion_por_sustancias_psicoactivas.csv')

col1, col2 = st.columns(2)

nombre_barrio = col1.multiselect('Nombre del Barrio', sorted(df['nombre_barrio'].unique()))

with col2:
    solo_mujeres = st.checkbox('Num Mujeres')
    solo_hombres = st.checkbox('Num hombres')

def filter_data(df, nombre_barrio, solo_mujeres, solo_hombres):
    df_copy = df.copy()

    if len(nombre_barrio) > 0:
        df_copy = df_copy[df_copy['nombre_barrio'].isin(nombre_barrio)]

    if solo_mujeres and solo_hombres:
        # No filtrar por sexo si ambos están seleccionados
        pass
    elif solo_mujeres:
        df_copy = df_copy[df_copy['sexo_'].str.upper() == 'F']
    elif solo_hombres:
        df_copy = df_copy[df_copy['sexo_'].str.upper() == 'M']

    return df_copy

df_filtered = filter_data(df, nombre_barrio, solo_mujeres, solo_hombres)

total_casos = len(df_filtered)
barrio_mas_intoxicaciones = df_filtered['nombre_barrio'].mode()[0] if not df_filtered.empty else 'N/A'

col1, col2, col3 = st.columns(3)
col1.metric("# Casos", f"{total_casos:,.0f}")
col3.metric("Barrio con Intoxicaciones", barrio_mas_intoxicaciones)

st.dataframe(df_filtered)
