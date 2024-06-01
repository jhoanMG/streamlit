import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(layout="wide")

st.sidebar.title("Nuevas Tecnologias")

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)
st.title("Simulador CESDE Bello")

df = pd.read_csv('datasets/cesde.csv')

gruposU = sorted(df['GRUPO'].unique())
nivelesU = sorted(df['NIVEL'].unique())
jornadasU = sorted(df['JORNADA'].unique())
horarioU = sorted(df['HORARIO'].unique())
submodulosU = sorted(df['SUBMODULO'].unique())
docentesU = sorted(df['DOCENTE'].unique())
momentosU = sorted(df['MOMENTO'].unique())

# -----------------------------------------------------------------------------------
def filtro1():    
    col1, col2 = st.columns(2)
    with col1:
        grupo = st.selectbox("Grupo", gruposU)
    with col2:
        momento = st.selectbox("Momento", momentosU)
    resultado = df[(df['GRUPO'] == grupo) & (df['MOMENTO'] == momento)]
    resultado = resultado.reset_index(drop=True)
    estudiante = resultado['NOMBRE']
    fig = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=estudiante, y=resultado['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=estudiante, y=resultado['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=estudiante, y=resultado['PRODUCTO'])
    ])   
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.table(resultado[["NOMBRE", "CONOCIMIENTO", "DESEMPEÑO", "PRODUCTO"]])
    
# -----------------------------------------------------------------------------------
def filtro2():
    col1, col2, col3 = st.columns(3)
    with col1:
        grupo = st.selectbox("Grupo", gruposU)
    with col2:
        nombres = df[df['GRUPO'] == grupo]
        nombre = st.selectbox("Estudiante", nombres["NOMBRE"])
    with col3:
        momentosU.append("Todos")
        momento = st.selectbox("Momento", momentosU)   
    if momento == "Todos":
        resultado = df[(df['GRUPO'] == grupo) & (df['NOMBRE'] == nombre)]
        momentos = sorted(df['MOMENTO'].unique())
        fig = go.Figure(data=[
            go.Bar(name='CONOCIMIENTO', x=momentos, y=resultado['CONOCIMIENTO']),
            go.Bar(name='DESEMPEÑO', x=momentos, y=resultado['DESEMPEÑO']),
            go.Bar(name='PRODUCTO', x=momentos, y=resultado['PRODUCTO'])
        ])   
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        resultado = resultado.reset_index(drop=True)
        m1 = resultado.loc[0, ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']]
        m2 = resultado.loc[1, ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']]
        m3 = resultado.loc[2, ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']]
        tm = pd.Series([m1.mean(), m2.mean(), m3.mean()])       
        st.subheader("Promedio")
        st.subheader(round(tm.mean(), 1))
    else:
        resultado = df[(df['GRUPO'] == grupo) & (df['MOMENTO'] == momento) & (df['NOMBRE'] == nombre)]
        estudiante = resultado['NOMBRE']
        fig = go.Figure(data=[
            go.Bar(name='CONOCIMIENTO', x=estudiante, y=resultado['CONOCIMIENTO']),
            go.Bar(name='DESEMPEÑO', x=estudiante, y=resultado['DESEMPEÑO']),
            go.Bar(name='PRODUCTO', x=estudiante, y=resultado['PRODUCTO'])
        ])   
        fig.update_layout(barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        resultado = resultado.reset_index(drop=True)
        conocimiento = resultado.loc[0, ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']]
        st.subheader("Promedio")
        st.subheader(round(conocimiento.mean(), 1)) 

# -----------------------------------------------------------------------------------
def filtro3():
    col1, col2 = st.columns(2)
    with col1:
        docente = st.selectbox("Docente", docentesU)
    with col2:
        momento = st.selectbox("Momento", momentosU)
    resultado = df[(df['DOCENTE'] == docente) & (df['MOMENTO'] == momento)]
    resultado = resultado.reset_index(drop=True)
    estudiante = resultado['NOMBRE']
    fig = go.Figure(data=[
        go.Bar(name='CONOCIMIENTO', x=estudiante, y=resultado['CONOCIMIENTO']),
        go.Bar(name='DESEMPEÑO', x=estudiante, y=resultado['DESEMPEÑO']),
        go.Bar(name='PRODUCTO', x=estudiante, y=resultado['PRODUCTO'])
    ])   
    fig.update_layout(barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.table(resultado[["NOMBRE", "CONOCIMIENTO", "DESEMPEÑO", "PRODUCTO"]])



def estudiantes_becado():
    promedio_minimo = 4.5
    becados = df[(df['CONOCIMIENTO'] >= promedio_minimo) & 
                 (df['DESEMPEÑO'] >= promedio_minimo) & 
                 (df['PRODUCTO'] >= promedio_minimo)]
    
    # Filtrar los mejores becados
    becados_mejores = becados.nlargest(10, ['CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO'])
    
    # Crear un select box para seleccionar al estudiante
    estudiante_seleccionado = st.selectbox('Selecciona un estudiante:', becados_mejores['NOMBRE'])
    
    # Filtrar el DataFrame para mostrar solo la información del estudiante seleccionado
    info_estudiante = becados_mejores[becados_mejores['NOMBRE'] == estudiante_seleccionado]
    
    st.table(info_estudiante[['NOMBRE', 'GRUPO', 'CONOCIMIENTO', 'DESEMPEÑO', 'PRODUCTO']])
    
    # Crear la figura de la gráfica de barras
    fig = go.Figure()
    
    # Iterar sobre cada estudiante y agregar una barra a la gráfica
    for index, row in becados_mejores.iterrows():
        # Si el estudiante es el seleccionado, la barra es azul, de lo contrario, es roja
        color = 'blue' if row['NOMBRE'] == estudiante_seleccionado else 'red'
        fig.add_trace(go.Bar(x=[row['NOMBRE']], 
                             y=[row['CONOCIMIENTO'], row['DESEMPEÑO'], row['PRODUCTO']], 
                             name=row['NOMBRE'],
                             marker_color=color))
    
    # Ajustar diseño de la gráfica
    fig.update_layout(
        barmode='group',
        xaxis_title='Estudiantes',
        yaxis_title='Puntaje',
        title='Puntajes de Estudiantes Becados'
    )
    
    st.plotly_chart(fig)



# -----------------------------------------------------------------------------------
filtros = [
    "Notas por grupo",
    "Notas por estudiante",
    "Notas por docente",
    "Estudiantes becados"
]

filtro = st.selectbox("Filtros", filtros)

if filtro:
    filtro_index = filtros.index(filtro)
    if filtro_index == 0:
        filtro1()
    elif filtro_index == 1:
        filtro2()
    elif filtro_index == 2:
        filtro3()
    elif filtro_index == 3:
        estudiantes_becado()
