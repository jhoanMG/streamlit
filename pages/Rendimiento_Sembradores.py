import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar la página
st.set_page_config(page_title="Análisis de Siembras", layout="wide")

# Sidebar
st.sidebar.title("Página de seguimiento")
logo = "https://i.ibb.co/tpDf97v/logo-sky.jpg"  # Enlace directo a la imagen
st.sidebar.image(logo)

# Cargar el CSV
f = pd.read_csv('datasets/sembradores.csv', sep=';', encoding='utf-8')

# Asegurarse de que 'Rendimiento' es numérico
f['Rendimiento'] = pd.to_numeric(f['Rendimiento'], errors='coerce')

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

# Agrupar por sembrador y calcular la media, ignorando NaNs
grouped_df = filtered_df.groupby('Sembrador', as_index=False).agg({'Rendimiento': 'mean'})

# Eliminar filas donde 'Rendimiento' sea NaN después del agrupamiento
grouped_df = grouped_df.dropna()

# Configurar la figura de las gráficas
fig, axs = plt.subplots(2, 1, figsize=(14, 12))  # Aumenté el tamaño de la figura para mayor claridad
fig.tight_layout(pad=5.0)

# Gráfica de "barras" para "Suma de Plantas_sembradas"
sns.barplot(data=filtered_df, x='Suma de Plantas_sembradas', y='Sembrador', ax=axs[0], palette='Blues_d', ci=None)
axs[0].set_title('Distribución de la Suma de Plantas Sembradas por Sembrador', fontsize=16)
axs[0].set_xlabel('Suma de Plantas Sembradas', fontsize=12)
axs[0].set_ylabel('Sembrador', fontsize=12)

# Rotar las etiquetas de los números en el eje X a 45 grados
axs[0].tick_params(axis='x', rotation=45)

# Gráfica de "barras" para "Rendimiento"
sns.barplot(data=grouped_df, x='Sembrador', y='Rendimiento', ax=axs[1], palette='Blues_d', ci=None)

# Ajustar los nombres de los sembradores
axs[1].set_title('Rendimiento por Sembrador', fontsize=16)
axs[1].set_xlabel('Sembrador', fontsize=12)
axs[1].set_ylabel('Rendimiento', fontsize=12)

# Aumentar el espacio entre los nombres y los valores
axs[1].set_xticks(range(len(grouped_df['Sembrador'])))
axs[1].set_xticklabels(grouped_df['Sembrador'], rotation=60, ha='right')

# Aumentar el espaciado entre los números en el eje Y
for i in range(len(grouped_df)):
    axs[1].text(i, grouped_df['Rendimiento'].iloc[i] + 0.5, round(grouped_df['Rendimiento'].iloc[i], 2), ha='center', va='bottom')

axs[1].tick_params(axis='y', rotation=0)

# Ajustar el espaciado entre las gráficas
plt.subplots_adjust(hspace=0.4)

# Mostrar las gráficas en Streamlit
st.pyplot(fig)

# Mostrar los primeros registros del DataFrame
#st.subheader("Datos del CSV")
#st.write(filtered_df.head())
