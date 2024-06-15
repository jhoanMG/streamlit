import streamlit as st

# Configuración de la página
st.set_page_config(layout="wide", page_title="Nuevas tecnologías de Programación")

# Sidebar
st.sidebar.title("Nuevas Tecnologías")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Título principal con estilo
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Nuevas Tecnologías</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Aquí encontrarás una variedad de datos </h2>", unsafe_allow_html=True)

# Sección de Elaborado Por
st.markdown("<h3 style='color: #4A90E2;'>Elaborado Por:</h3>", unsafe_allow_html=True)
st.write("- Clara Eliana Ramírez López")
st.write("- Jhoan Andrés Monsalve García")

# Imagen principal
main_image = "https://st4.depositphotos.com/10325396/25177/i/450/depositphotos_251775510-stock-photo-corridor-of-server-room-with.jpg"
st.markdown(f"<div style='text-align: center;'><img src='{main_image}' alt='Servidor de tecnología avanzada' style='width:70%;'/></div>", unsafe_allow_html=True)

# Sección de Proyecto Integrador
st.markdown("<h3 style='color: #4A90E2;'>Proyecto Integrador</h3>", unsafe_allow_html=True)
st.write("- Películas")
st.write("- Aquí se podrán explorar diferentes filtros para visualizar información sobre películas, actores, etc. Esto significa que los usuarios tendrán la capacidad de utilizar una variedad de filtros, como género de la película, año de lanzamiento, calificación, entre otros, para personalizar su búsqueda y encontrar la información específica que están buscando. Además de la información sobre las películas en sí, también podrán explorar detalles sobre los actores, directores, y cualquier otra información relevante relacionada con la industria cinematográfica. Este enfoque interactivo y personalizable permite a los usuarios navegar a través de una amplia gama de datos cinematográficos de una manera eficiente y adaptada a sus intereses particulares.")

# Sección de Simulador Cesde
st.markdown("<h3 style='color: #4A90E2;'>Simulador Cesde</h3>", unsafe_allow_html=True)
st.write("- Información sobre Cesde Sede Bello")
st.write("En esta sección, los usuarios podrán acceder a una variedad de filtros relacionados con la información académica de la institución Cesde Sede Bello. Estos filtros permitirán a los usuarios explorar datos específicos sobre notas, grupos y docentes, lo que les brindará una comprensión más detallada y personalizada de la dinámica académica dentro de la institución. Desde la evaluación del rendimiento académico hasta la organización de grupos y la identificación de docentes relevantes, estos filtros ofrecen una herramienta integral para explorar y comprender la experiencia educativa en Cesde Sede Bello.")

# Sección de Proyecto Individual
st.markdown("<h3 style='color: #4A90E2;'>Proyecto Individual</h3>", unsafe_allow_html=True)
st.write("- Intoxicación por Sustancias Psicoactivas - Medellín")
st.write("En esta sección, se lleva a cabo un análisis exhaustivo del índice de intoxicaciones por sustancias psicoactivas en el área de Medellín. Los usuarios podrán explorar datos detallados relacionados con la incidencia de intoxicaciones, incluyendo estadísticas sobre la frecuencia, tendencias temporales, áreas geográficas afectadas, grupos de población más afectados, entre otros aspectos relevantes. Este análisis proporciona una visión profunda de la problemática de las sustancias psicoactivas en Medellín, permitiendo una comprensión más completa de los factores que contribuyen a esta situación y ayudando a identificar posibles áreas de intervención y prevención.")