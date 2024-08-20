import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide", page_title="Filtros de Siembras")

# Título y logo en la barra lateral
st.sidebar.title("Filtros de Siembras")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Título en la aplicación
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Análisis de Siembras</h1>", unsafe_allow_html=True)

# Leer el CSV
df = pd.read_csv('datasets/AppSheet.ViewData.2024-06-20.csv', sep=';', encoding='utf-8')

# Verificar que la columna existe y limpiar nombres de columnas
df.columns = [col.strip('"') for col in df.columns]  # Eliminar comillas de los nombres de columnas

if 'Nombre de la variedad' not in df.columns:
    st.error("La columna 'Nombre de la variedad' no se encuentra en el CSV.")
else:
    # Convertir 'Fecha_siembra' a datetime si no lo está
    df['Fecha_siembra'] = pd.to_datetime(df['Fecha_siembra'], errors='coerce', dayfirst=True)

    # Convertir 'Total sembrado' a float después de limpiar comas
    df['Total sembrado'] = df['Total sembrado'].replace(',', '', regex=True).astype(float)

    # Creación de los filtros
    st.sidebar.header("Filtrar por:")

    # Filtro por Nombre de la variedad
    nombre_variedad_seleccionado = st.sidebar.multiselect('Nombre de la variedad', sorted(df['Nombre de la variedad'].dropna().unique()))

    # Filtro por Fecha de siembra
    fecha_min = st.sidebar.date_input('Fecha mínima de siembra', df['Fecha_siembra'].min().date())
    fecha_max = st.sidebar.date_input('Fecha máxima de siembra', df['Fecha_siembra'].max().date())

    # Función para filtrar datos
    def filter_data(df, nombre_variedad_seleccionado, fecha_min, fecha_max):
        df_filtered = df.copy()

        if nombre_variedad_seleccionado:
            df_filtered = df_filtered[df_filtered['Nombre de la variedad'].isin(nombre_variedad_seleccionado)]

        df_filtered = df_filtered[
            (df_filtered['Fecha_siembra'] >= pd.to_datetime(fecha_min)) &
            (df_filtered['Fecha_siembra'] <= pd.to_datetime(fecha_max))
        ]

        return df_filtered

    # Aplicar filtros
    df_filtered = filter_data(df, nombre_variedad_seleccionado, fecha_min, fecha_max)

    # Métricas
    col1, col2 = st.columns(2)
    total_sembres = df_filtered['Total sembrado'].sum()
    num_variedades = df_filtered['Nombre de la variedad'].nunique()

    col1.metric("Total Sembrado", f"{total_sembres:,.0f}")
    col2.metric("Número de Variedades", f"{num_variedades:,.0f}")

    # Gráfico 1: Total sembrado por variedad
    if not df_filtered.empty:
        total_por_variedad = df_filtered.groupby('Nombre de la variedad')['Total sembrado'].sum().reset_index()
        fig_variedad = px.bar(total_por_variedad, x='Total sembrado', y='Nombre de la variedad', orientation='h',
                              title='Total Sembrado por Variedad', labels={'Total sembrado': 'Total Sembrado', 'Nombre de la variedad': 'Variedad'})
        st.plotly_chart(fig_variedad)

    # Gráfico 2: Evolución del sembrado a lo largo del tiempo
    if not df_filtered.empty:
        total_por_fecha = df_filtered.groupby('Fecha_siembra')['Total sembrado'].sum().reset_index()
        fig_fecha = px.line(total_por_fecha, x='Fecha_siembra', y='Total sembrado',
                            title='Evolución del Total Sembrado a lo Largo del Tiempo', labels={'Total sembrado': 'Total Sembrado', 'Fecha_siembra': 'Fecha de Siembra'})
        st.plotly_chart(fig_fecha)

    # Gráfico 3: Total sembrado acumulado por variedad
    if not df_filtered.empty:
        total_acumulado = df_filtered.groupby(['Nombre de la variedad', 'Fecha_siembra'])['Total sembrado'].sum().groupby(level=0).cumsum().reset_index()
        fig_acumulado = px.line(total_acumulado, x='Fecha_siembra', y='Total sembrado', color='Nombre de la variedad',
                                title='Total Sembrado Acumulado por Variedad', labels={'Total sembrado': 'Total Sembrado Acumulado', 'Fecha_siembra': 'Fecha de Siembra'})
        st.plotly_chart(fig_acumulado)

    # Mostrar el DataFrame filtrado
    st.dataframe(df_filtered)
