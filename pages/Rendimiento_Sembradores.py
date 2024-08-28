import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar la página
st.set_page_config(page_title="Análisis de Siembras", layout="wide")

# Sidebar
st.sidebar.title("Pagina de seguimiento")
logo = "https://i.ibb.co/tpDf97v/logo-sky.jpg"  # Enlace directo a la imagen
st.sidebar.image(logo)

# Cargar el CSV
f = pd.read_csv('datasets/AppSheet.ViewData.2024-08-26.csv', sep=';', encoding='utf-8')

# Título de la aplicación
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>RENDIMIENTO SEMBRADORES</h1>", unsafe_allow_html=True)

# Filtros
sembradores = f['Sembrador'].unique()
selected_sembradores = st.sidebar.multiselect('Selecciona Sembradores', sembradores, default=sembradores)

# Filtros adicionales
fechas = f['Fecha_siembra'].unique()
selected_fechas = st.sidebar.multiselect('Selecciona Fechas de Siembra', fechas, default=fechas)

suma_min = f['Suma de Plantas_sembradas'].min()
suma_max = f['Suma de Plantas_sembradas'].max()
selected_suma = st.sidebar.slider('Selecciona Rango de Suma de Plantas Sembradas', 
                                  min_value=suma_min, 
                                  max_value=suma_max, 
                                  value=(suma_min, suma_max))

# Filtrar los datos
filtered_df = f[(f['Sembrador'].isin(selected_sembradores)) &
                (f['Fecha_siembra'].isin(selected_fechas)) &
                (f['Suma de Plantas_sembradas'].between(selected_suma[0], selected_suma[1]))]

# Configurar la figura de las gráficas
fig, axs = plt.subplots(2, 1, figsize=(14, 10))
fig.tight_layout(pad=5.0)

# Gráfica de "Suma de Plantas_sembradas"
sns.barplot(data=filtered_df, x='Sembrador', y='Suma de Plantas_sembradas', ax=axs[0], palette='Blues_d')
axs[0].set_title('Suma de Plantas Sembradas por Sembrador')
axs[0].set_xlabel('Sembrador')
axs[0].set_ylabel('Suma de Plantas Sembradas')

# Gráfica de "Rendimiento"
sns.barplot(data=filtered_df, x='Sembrador', y='Rendimiento', ax=axs[1], palette='Blues_d')
axs[1].set_title('Rendimiento por Sembrador')
axs[1].set_xlabel('Sembrador')
axs[1].set_ylabel('Rendimiento')

# Mostrar las gráficas en Streamlit
st.pyplot(fig)

# Mostrar los primeros registros del DataFrame
st.subheader("Datos del CSV")
st.write(filtered_df.head())
