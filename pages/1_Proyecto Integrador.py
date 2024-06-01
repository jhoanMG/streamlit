import streamlit as st
import pandas as pd


st.set_page_config(page_title="Filtros")


st.sidebar.title("Base de datos")


st.title("Proyecto Integrador")


df = pd.read_csv('datasets/integrador.csv')


PuntuacionU = sorted(df['Puntuacion'].unique())
CategoriaU = sorted(df['Categoria'].astype(str).unique())


def filtro1():    
    col1, col2 = st.columns(2)
    with col1:
        Puntuacion = st.selectbox("Puntuacion", PuntuacionU + ['Todas']) 
    with col2:
        Categoria = st.selectbox("Categoria", CategoriaU + ['Todas']) 

    if Puntuacion != 'Todas' and Categoria != 'Todas':
        filtered_df = df[(df['Puntuacion'] == Puntuacion) & (df['Categoria'] == Categoria)]
    elif Puntuacion != 'Todas':
        filtered_df = df[df['Puntuacion'] == Puntuacion]
    elif Categoria != 'Todas':
        filtered_df = df[df['Categoria'] == Categoria]
    else:
        filtered_df = df 
    
  
    st.write(filtered_df)


filtro1()
