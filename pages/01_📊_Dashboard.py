import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.conexion import obtener_conexion
from sqlalchemy import text

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Dashboard General de Inversión", layout="wide")

# Logo DANE Centrado
col_logo_a, col_logo_b, col_logo_c = st.columns([1, 2, 1])
with col_logo_b:
    st.image("https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png", 
             use_container_width=True)

st.markdown("<h1 style='text-align: center;'>📊 Dashboard General de Inversión</h1>", unsafe_allow_html=True)
st.divider()

# 2. SELECTOR DE AÑO
col_f, _ = st.columns([1, 3])
with col_f:
    anio_sel = st.selectbox("📅 Seleccione el Año de Análisis:", [2023, 2022, 2021, 2020, 2019], index=4)

# 3. MOTOR DE CARGA SILENCIOSO
df = pd.DataFrame()
engine = obtener_conexion()

# Intento 1: SQL
if engine:
    try:
        query = text("SELECT * FROM indicadores_ambientales WHERE CAST(periodo AS CHAR) = :anio")
        df = pd.read_sql(query, engine, params={"anio": str(anio_sel)})
    except: pass

# Intento 2: Búsqueda Recursiva en Carpetas (data/procesados/etc)
if df.empty:
    ruta_base = "data"
    if os.path.exists(ruta_base):
        for raiz, carpetas, archivos in os.walk(ruta_base):
            coincidencias = [f for f in archivos if str(anio_sel) in f and f.lower().endswith(".csv")]
            if coincidencias:
                df = pd.read_csv(os.path.join(raiz, coincidencias[0]))
                break

# 4. RENDERIZADO DE DATOS (Sin mensajes técnicos)
if not df.empty:
    # Estandarización de columnas
    df.columns = [c.lower().strip() for c in df.columns]
    col_inv = 'gasto_gestion_amb' if 'gasto_gestion_amb' in df.columns else df.columns[-1]
    col_sec = 'seccion_economica' if 'seccion_economica' in df.columns else df.columns[1]

    # MÉTRICAS
    m1, m2 = st.columns(2)
    m1.metric(f"Inversión Total {anio_sel}", f"$ {df[col_inv].sum():,.0f}")
    m2.metric("Empresas Registradas", f"{df['id_empresa'].nunique() if 'id_empresa' in df.columns else len(df):,}")

    st.divider()

    # GRÁFICO TREEMAP
    st.subheader(f"🌳 Distribución por Sector ({anio_sel})")
    df_tree = df.groupby(col_sec)[col_inv].sum().reset_index()
    df_tree = df_tree[df_tree[col_inv] > 0]
    
    fig = px.treemap(
        df_tree, 
        path=[col_sec], 
        values=col_inv, 
        color=col_inv, 
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning(f"⚠️ No se encontró información para el año {anio_sel}.")