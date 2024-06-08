import streamlit as st

# Configuración de la página
st.set_page_config(layout="wide", page_title="Nuevas tecnologías")

st.sidebar.title("Nuevas Tecnologias")

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Definir el título y el encabezado de la página
st.title("Nuevas Tecnologías")
st.header("Aquí encontrarás una variedad de datos")

# Agregar imagen principal
main_image = "https://st4.depositphotos.com/10325396/25177/i/450/depositphotos_251775510-stock-photo-corridor-of-server-room-with.jpg"
st.image(main_image, caption='Servidor de tecnología avanzada')

st.subheader("Proyecto Integrador")
st.write("- Musica")

st.subheader("Simulador Cesde")
st.write("- Info Cesde Sede Bello")

st.subheader("Proyecto Individual")
st.write("- Intoxicacion por Sustancias Psicoactivas - Medellin")

st.subheader("Elaborado Por:")
st.write("- Clara Eliana Ramirez Lopez")
st.write("- Jhoan Andres Monsalve Garcia")
