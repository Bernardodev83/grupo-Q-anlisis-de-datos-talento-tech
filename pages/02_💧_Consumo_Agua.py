import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.conexion import obtener_conexion
from sqlalchemy import text

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Análisis Hídrico - DANE", layout="wide")

# Logo y Título
st.image("https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png", width=200)
st.markdown("<h1 style='color: #003366;'>💧 Gestión de Recursos Hídricos (Top 10)</h1>", unsafe_allow_html=True)
st.caption("Fuente Oficial: DANE Colombia - Análisis de Huella Hídrica")

# 2. SECCIÓN INFORMATIVA
with st.expander("ℹ️ Información del Análisis"):
    st.write("Esta página identifica los 10 sectores industriales con mayor demanda de agua y los compara con su inversión ambiental.")

st.divider()

# 3. FILTRO DE AÑO (Motor inteligente)
col_f, _ = st.columns([1, 3])
with col_f:
    anio_sel = st.selectbox("📅 Seleccione el Año de Análisis:", [2023, 2022, 2021, 2020, 2019], index=4)

# 4. CARGA DE DATOS (SQL o Carpetas)
df = pd.DataFrame()
engine = obtener_conexion()

if engine:
    try:
        query = text("SELECT * FROM indicadores_ambientales WHERE CAST(periodo AS CHAR) = :anio")
        df = pd.read_sql(query, engine, params={"anio": str(anio_sel)})
    except: pass

if df.empty:
    ruta_base = "data"
    if os.path.exists(ruta_base):
        for raiz, dirs, archivos in os.walk(ruta_base):
            coincidencias = [f for f in archivos if str(anio_sel) in f and f.lower().endswith(".csv")]
            if coincidencias:
                df = pd.read_csv(os.path.join(raiz, coincidencias[0]))
                break

# 5. RENDERIZADO DE GRÁFICOS
if not df.empty:
    # Limpieza de columnas
    df.columns = [c.lower().strip() for c in df.columns]
    col_agua = next((c for c in df.columns if 'agua' in c), df.columns[-1])
    col_inv = 'gasto_gestion_amb' if 'gasto_gestion_amb' in df.columns else df.columns[-2]
    col_sec = 'seccion_economica' if 'seccion_economica' in df.columns else df.columns[1]

    # --- PREPARACIÓN TOP 10 ---
    df_top10 = df.groupby(col_sec)[[col_agua, col_inv]].sum().reset_index()
    df_top10 = df_top10.sort_values(by=col_agua, ascending=False).head(10)

    # --- GRÁFICO 1: BARRAS HORIZONTALES ---
    st.subheader(f"📊 Ranking: Los 10 Mayores Consumidores ({anio_sel})")
    fig_barras = px.bar(
        df_top10.sort_values(by=col_agua, ascending=True),
        x=col_agua,
        y=col_sec,
        orientation='h',
        color=col_agua,
        color_continuous_scale='Blues',
        text_auto='.2s',
        labels={col_agua: 'Consumo (m³)', col_sec: 'Sector'}
    )
    fig_barras.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_barras, use_container_width=True)

    st.divider()

    # --- GRÁFICO 2: BURBUJAS (Inversión vs Consumo) ---
    st.subheader(f"🔵 Relación: Consumo vs. Inversión Ambiental ({anio_sel})")
    st.markdown("*El tamaño de la burbuja indica el volumen de agua consumida.*")
    
    fig_burbujas = px.scatter(
        df_top10,
        x=col_inv,
        y=col_agua,
        size=col_agua,
        color=col_sec,
        hover_name=col_sec,
        size_max=60,
        labels={col_inv: 'Inversión en Protección ($)', col_agua: 'Consumo de Agua (m³)'}
    )
    fig_burbujas.update_layout(height=500)
    st.plotly_chart(fig_burbujas, use_container_width=True)

    # Mensaje de conclusión dinámica
    st.info(f"💡 En {anio_sel}, el sector **{df_top10.iloc[0][col_sec]}** es el mayor consumidor, mientras que el tamaño de las burbujas ayuda a visualizar qué tan proporcional es su inversión.")

else:
    st.warning(f"⚠️ No se encontró el archivo del año {anio_sel} en la carpeta 'data'.")