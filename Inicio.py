import streamlit as st

# Configuración de la página
st.set_page_config(layout="wide", page_title="Seguimiento Sky")

# Sidebar
st.sidebar.title("Pagina de seguimiento")
logo = "https://i.ibb.co/tpDf97v/logo-sky.jpg"  # Enlace directo a la imagen
st.sidebar.image(logo)

# Título principal con estilo
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>PAGINA DE INFORMACION</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'></h2>", unsafe_allow_html=True)

# Imagen principal
main_image = "https://i.ibb.co/tpDf97v/logo-sky.jpg"  # Enlace directo a la imagen principal
st.markdown(f"<div style='text-align: center;'><img src='{main_image}' alt='Servidor de tecnología avanzada' style='width:50%; height:auto;'/></div>", unsafe_allow_html=True)


