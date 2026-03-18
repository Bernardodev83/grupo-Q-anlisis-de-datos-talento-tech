import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuración de la página
st.set_page_config(page_title="Consumo de Agua", layout="wide")

# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)

# 2. Título y Sección de Información
st.title("💧 Análisis de Recursos Hídricos")

with st.expander("ℹ️ Acerca de esta página"):
    st.markdown("""
    Esta sección analiza la **huella hídrica** de la industria capturada por la encuesta del DANE.
    * **Propósito:** Comparar el consumo de agua en metros cúbicos (m³) frente a la inversión que hacen las empresas para ahorrar o tratar el recurso.
    * **Variables clave:** `consumo_agua_m3` y `gasto_gestion_amb`.
    * **Análisis:** Permite identificar sectores con alto consumo pero baja inversión en ahorro.
    """)

# 3. Selector de Año en la barra lateral
# Usamos un 'key' único para evitar conflictos con otras páginas
anio = st.sidebar.selectbox("Seleccionar Año:", [2023, 2022, 2021, 2020, 2019], key="agua_year_selector")
ruta = f"datos/procesados/datos_{anio}_final.csv"

# 4. Carga y Visualización
if os.path.exists(ruta):
    # Cargamos los datos del año seleccionado
    df = pd.read_csv(ruta)
    
    # Limpieza rápida: asegurar que no haya valores negativos y quitar textos vacíos
    df = df[df['seccion_economica'].notna()]
    
    # --- GRÁFICO 1: TOP CONSUMIDORES (ARRIBA) ---
    st.subheader(f"🔝 Top 10 Sectores con Mayor Consumo de Agua ({anio})")
    
    # Agrupamos por sector para que el gráfico sea estable en todos los años
    resumen_sectores = df.groupby('seccion_economica').agg({
        'consumo_agua_m3': 'sum',
        'gasto_gestion_amb': 'sum'
    }).reset_index()
    
    top_10_agua = resumen_sectores.nlargest(10, 'consumo_agua_m3')
    
    fig_bar = px.bar(
        top_10_agua, 
        x='consumo_agua_m3', 
        y='seccion_economica', 
        orientation='h', 
        color='consumo_agua_m3',
        color_continuous_scale='Blues',
        labels={'consumo_agua_m3': 'Metros Cúbicos (m³)', 'seccion_economica': 'Sector Económico'},
        text_auto='.2s'
    )
    # Ordenar de mayor a menor
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider() 

    # --- GRÁFICO 2: RELACIÓN INVERSIÓN VS CONSUMO (ABAJO) ---
    st.subheader("📊 Relación Sectorial: Inversión vs. Consumo")
    st.write(f"Comparativa de cuánto consume cada sector frente a cuánto invierte en el año {anio}.")
    
    # Usamos el resumen agrupado para asegurar que siempre haya datos visibles
    fig_scat = px.scatter(
        resumen_sectores[resumen_sectores['consumo_agua_m3'] > 0], 
        x='consumo_agua_m3', 
        y='gasto_gestion_amb', 
        color='seccion_economica',
        hover_name='seccion_economica',
        size='consumo_agua_m3', # El tamaño del punto depende del consumo
        labels={
            'consumo_agua_m3': 'Consumo Total (m³)', 
            'gasto_gestion_amb': 'Inversión Total ($)'
        },
        template="plotly_white"
    )
    
    # Ajustamos para que se vea bien si hay valores muy distantes
    fig_scat.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    st.plotly_chart(fig_scat, use_container_width=True)

else:
    st.error(f"❌ No se encontró el archivo: {ruta}")
    st.info("Asegúrate de haber ejecutado el Limpiador Maestro para generar los archivos procesados.")