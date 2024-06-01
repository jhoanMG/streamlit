import streamlit as st
import pandas as pd

st.header("Simulador CESDE")

df = pd.read_csv('datasets/cesde.csv')

#------------------------------------------------------------------------------
def notas_estudiante():
    gruposU = sorted(df['GRUPO'].unique()) 
    momentoU = sorted(df['MOMENTO'].unique()) 
    col1, col2 = st.columns(2)
    with col1:
        grupo_seleccionado = st.selectbox("Grupos", gruposU)
    with col2:
        momento_seleccionado = st.selectbox("Momentos", momentoU)
    estudiantes = df[(df['GRUPO'] == grupo_seleccionado) & (df['MOMENTO'] == momento_seleccionado)]
    
    estudiante_seleccionado = st.selectbox("Estudiante", estudiantes['NOMBRE'])

    notas_estudiante = estudiantes[estudiantes['NOMBRE'] == estudiante_seleccionado]
    st.table(notas_estudiante[['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']])

    # Crear un DataFrame para el gráfico de barras
    data = {
        'Tipo': ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO'],
        'Cantidad': [notas_estudiante['CONOCIMIENTO'].values[0],
                     notas_estudiante['DESEMPEÑO'].values[0],
                     notas_estudiante['PRODUCTO'].values[0]]
    }

    df_grafico = pd.DataFrame(data)
   
    # Graficar el DataFrame con un gráfico de barras
    st.bar_chart(df_grafico.set_index('Tipo'))

#------------------------------------------------------------------------------
def notas_grupo():
    gruposU = sorted(df['GRUPO'].unique()) 
    opcion = st.selectbox("Grupos", gruposU)
    estudiantes = df[df['GRUPO'] == opcion]
    st.table(estudiantes)

#------------------------------------------------------------------------------
def estudiantes_becado():
    promedio_minimo = 4.5
    becados = df[(df['CONOCIMIENTO'] >= promedio_minimo) & 
                 (df['DESEMPEÑO'] >= promedio_minimo) & 
                 (df['PRODUCTO'] >= promedio_minimo)]
    
    st.table(becados[['NOMBRE', 'GRUPO', 'CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']])

#------------------------------------------------------------------------------
filtros = [
    'Notas por estudiante',
    'Notas por grupo',
    'Estudiantes becados'
]

seleccion_filtro = st.selectbox("Filtro", filtros)

if seleccion_filtro:
    index = filtros.index(seleccion_filtro)
    if index == 0:
        notas_estudiante()
    elif index == 1:
        notas_grupo()
    elif index == 2:
        estudiantes_becado()
