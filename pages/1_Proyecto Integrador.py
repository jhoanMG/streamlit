import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Proyecto Integrador")

# Título del sidebar y de la página
st.sidebar.title("Base de datos")
st.title("Proyecto Integrador")

# Carga de datos
try:
    df = pd.read_csv('datasets/integrador.csv')
except FileNotFoundError:
    st.error("El archivo 'integrador.csv' no se encuentra en el directorio especificado.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("El archivo 'integrador.csv' está vacío.")
    st.stop()
except Exception as e:
    st.error(f"Error al leer el archivo CSV: {e}")
    st.stop()

# Validar las columnas esperadas
expected_columns = ['Puntuacion', 'Categoria', 'DuracionMinutos', 'Actores']
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Falta la columna '{col}' en el archivo CSV.")
        st.stop()

# Asegurarse de que DuracionMinutos sea numérico
try:
    df['DuracionMinutos'] = pd.to_numeric(df['DuracionMinutos'])
except ValueError:
    st.error("La columna 'DuracionMinutos' contiene valores no numéricos.")
    st.stop()

# Variables únicas para los selectboxes
PuntuacionU = sorted(df['Puntuacion'].unique())
CategoriaU = sorted(df['Categoria'].astype(str).unique())

# Extraer lista de actores únicos
todos_actores = set()
for actores in df['Actores'].dropna().str.split(','):
    todos_actores.update([actor.strip() for actor in actores])
ActoresU = sorted(todos_actores)

# Valores mínimo y máximo para el slider de duración
duracion_min, duracion_max = int(df['DuracionMinutos'].min()), int(df['DuracionMinutos'].max())

# Función de filtrado
def filtro1():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        Puntuacion = st.selectbox("Puntuacion", PuntuacionU + ['Todas'])
    with col2:
        Categoria = st.selectbox("Categoria", CategoriaU + ['Todas'])
    with col3:
        Duracion = st.slider("Duración (min)", duracion_min, duracion_max, (duracion_min, duracion_max))
    with col4:
        Actor = st.selectbox("Actor", ['Todos'] + ActoresU)

    # Filtrado de datos
    filtered_df = df
    if Puntuacion != 'Todas':
        filtered_df = filtered_df[filtered_df['Puntuacion'] == Puntuacion]
    if Categoria != 'Todas':
        filtered_df = filtered_df[filtered_df['Categoria'] == Categoria]
    if Actor != 'Todos':
        filtered_df = filtered_df[filtered_df['Actores'].str.contains(Actor, na=False)]
    filtered_df = filtered_df[
        (filtered_df['DuracionMinutos'] >= Duracion[0]) & (filtered_df['DuracionMinutos'] <= Duracion[1])
    ]
    
    return filtered_df, Categoria if Categoria != 'Todas' else None

# Aplicar el filtro y mostrar la tabla
filtered_df, selected_categoria = filtro1()
st.write(filtered_df)

# Gráfico avanzado
st.subheader("Distribución de Puntuaciones por Categoría")

# Crear una agregación para la media de puntuación por categoría
df_avg = df.groupby('Categoria', as_index=False)['Puntuacion'].mean()

# Crear una lista de colores: rojo para la categoría seleccionada, azul para las demás
colors = ['red' if cat == selected_categoria else 'blue' for cat in df_avg['Categoria']]

# Crear el gráfico de barras con Plotly
fig = go.Figure(
    data=[
        go.Bar(
            x=df_avg['Categoria'],
            y=df_avg['Puntuacion'],
            marker=dict(color=colors),
            text=df_avg['Puntuacion'],
            textposition='auto'
        )
    ]
)

# Configuración del gráfico
fig.update_layout(
    title="Distribución de Puntuaciones por Categoría",
    xaxis_title="Categoría",
    yaxis_title="Puntuación Promedio",
    height=500
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Footer con miembros del equipo y contacto
st.subheader("Equipo y Contacto")
st.markdown("""
**Miembros del equipo:**
- Clara Ramirez
- Jhoan Monsalve G.
""")
