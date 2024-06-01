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

    if solo_mujeres:
        df_copy = df_copy[df_copy['sexo_'] == 'F']
    elif solo_hombres:
        df_copy = df_copy[df_copy['sexo_'] == 'M']

    return df_copy

df_filtered = filter_data(df, nombre_barrio, solo_mujeres, solo_hombres)

total_casos = len(df_filtered)
total_mujeres = len(df_filtered[df_filtered['sexo_'] == 'F'])
total_hombres = len(df_filtered[df_filtered['sexo_'] == 'M'])
barrio_mas_intoxicaciones = df_filtered['nombre_barrio'].mode()[0] if not df_filtered.empty else 'N/A'

col1, col2, col3 = st.columns(3)
col1.metric("# Casos", f"{total_casos:,.0f}")
col2.metric("# Mujeres", f"{total_mujeres:,.0f}")
col3.metric("# Hombres", f"{total_hombres:,.0f}")
col3.metric("Barrio con Intoxicaciones", barrio_mas_intoxicaciones)

# Crear un gráfico de barras que muestre las comunas con más casos de intoxicación
if not df_filtered.empty:
    casos_por_comuna = df_filtered['comuna'].value_counts().reset_index()
    casos_por_comuna.columns = ['comuna', 'num_casos']
    casos_por_comuna = casos_por_comuna.sort_values(by='num_casos', ascending=True)

    fig_comuna = px.bar(casos_por_comuna, x='num_casos', y='comuna', orientation='h',
                        title='Casos de Intoxicación por Comuna', labels={'num_casos': 'Número de Casos', 'comuna': 'Nombre de la Comuna'})
    st.plotly_chart(fig_comuna)

# Crear un gráfico comparando hombres y mujeres
if not df_filtered.empty:
    casos_por_sexo = df_filtered['sexo_'].value_counts().reset_index()
    casos_por_sexo.columns = ['sexo_', 'num_casos']

    fig_sexo = px.bar(casos_por_sexo, x='sexo_', y='num_casos', 
                      title='Comparación de Casos por Sexo', labels={'sexo_': 'Sexo', 'num_casos': 'Número de Casos'},
                      color='sexo_', color_discrete_map={'F': 'pink', 'M': 'blue'})

    st.plotly_chart(fig_sexo)

# Crear un gráfico de barras que muestre los casos por rangos de edad
if not df_filtered.empty:
    # Suponiendo que hay una columna 'edad_' en el DataFrame
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    df_filtered['edad_'] = pd.cut(df_filtered['edad_'], bins=bins, labels=labels, right=False)

    casos_por_edad = df_filtered['edad_'].value_counts().reset_index()
    casos_por_edad.columns = ['edad_', 'num_casos']
    casos_por_edad = casos_por_edad.sort_values(by='num_casos', ascending=True)

    fig_edad = px.bar(casos_por_edad, x='num_casos', y='edad_', orientation='h',
                      title='Casos de Intoxicación por Rango de Edad', labels={'num_casos': 'Número de Casos', 'edad_': 'Rango de Edad'})
    st.plotly_chart(fig_edad)

st.dataframe(df_filtered)