import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análisis de Siembras - LAURA CRISTINA RAMIREZ GAVIRIA", layout="wide")
st.sidebar.title("Página de seguimiento")
logo = "https://i.ibb.co/tpDf97v/logo-sky.jpg"
st.sidebar.image(logo)

f = pd.read_csv('datasets/sembradores.csv', sep=';', encoding='utf-8')
f['Rendimiento'] = pd.to_numeric(f['Rendimiento'], errors='coerce')

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>RENDIMIENTO SEMBRADORES - LAURA CRISTINA RAMIREZ GAVIRIA</h1>", unsafe_allow_html=True)

selected_sembradores = st.sidebar.multiselect('Selecciona Sembradores', ['LAURA CRISTINA RAMIREZ GAVIRIA'])

fechas = f['Fecha_siembra'].unique()
selected_fechas = st.sidebar.multiselect('Selecciona Fechas de Siembra', fechas, default=fechas)

suma_min = f['Suma de Plantas_sembradas'].min()
suma_max = f['Suma de Plantas_sembradas'].max()
selected_suma = st.sidebar.slider('Selecciona Rango de Suma de Plantas Sembradas', 
                                  min_value=suma_min, 
                                  max_value=suma_max, 
                                  value=(suma_min, suma_max))

filtered_df = f[(f['Sembrador'].isin(selected_sembradores)) &
                (f['Fecha_siembra'].isin(selected_fechas)) &
                (f['Suma de Plantas_sembradas'].between(selected_suma[0], selected_suma[1]))]

grouped_df = filtered_df.groupby('Sembrador', as_index=False).agg({'Rendimiento': 'mean'})
grouped_df = grouped_df.dropna()

fig, axs = plt.subplots(2, 1, figsize=(14, 12))
fig.tight_layout(pad=5.0)

sns.barplot(data=filtered_df, x='Suma de Plantas_sembradas', y='Sembrador', ax=axs[0], palette='Blues_d', ci=None)
axs[0].set_title('Distribución de la Suma de Plantas Sembradas por Sembrador', fontsize=16)
axs[0].set_xlabel('Suma de Plantas Sembradas', fontsize=12)
axs[0].set_ylabel('Sembrador', fontsize=12)
axs[0].tick_params(axis='x', rotation=45)

sns.barplot(data=grouped_df, x='Sembrador', y='Rendimiento', ax=axs[1], palette='Blues_d', ci=None)
axs[1].set_title('Rendimiento por Sembrador', fontsize=16)
axs[1].set_xlabel('Sembrador', fontsize=12)
axs[1].set_ylabel('Rendimiento', fontsize=12)
axs[1].set_xticks(range(len(grouped_df['Sembrador'])))
axs[1].set_xticklabels(grouped_df['Sembrador'], rotation=60, ha='right')

for i in range(len(grouped_df)):
    axs[1].text(i, grouped_df['Rendimiento'].iloc[i] + 0.5, round(grouped_df['Rendimiento'].iloc[i], 2), ha='center', va='bottom')

plt.subplots_adjust(hspace=0.4)
st.pyplot(fig)
