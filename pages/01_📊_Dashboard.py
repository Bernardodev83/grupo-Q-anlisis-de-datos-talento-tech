import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from pathlib import Path

# --- AJUSTE DE RUTAS PARA IMPORTAR UTILS ---
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

try:
    # Importamos la nueva conexión que creamos juntos
    from utils.conexion import get_connection
    print("✅ Conexión vinculada al Dashboard.")
except ImportError as e:
    st.error(f"Error de configuración: {e}")

# 1. CONFIGURACIÓN DE PÁGINA (Mantenemos tu diseño original)
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
    # He puesto el index en 0 para que por defecto muestre el más reciente (2023)
    anio_sel = st.selectbox("📅 Seleccione el Año de Análisis:", [2023, 2022, 2021, 2020, 2019], index=0)

# 3. MOTOR DE CARGA (Primero Nube, luego Local)
df = pd.DataFrame()
conn = get_connection()

# --- INTENTO 1: CARGA DESDE AIVEN (SQL) ---
if conn:
    try:
        # Usamos pandas para leer directamente con la conexión de mysql-connector
        query = f"SELECT * FROM indicadores_ambientales WHERE periodo = {anio_sel}"
        df = pd.read_sql(query, conn)
        conn.close()
    except Exception as e:
        print(f"DEBUG: Error leyendo SQL: {e}")

# --- INTENTO 2: BÚSQUEDA LOCAL (Respaldo si falla la nube) ---
if df.empty:
    ruta_base = os.path.join(ruta_raiz, "data", "procesados")
    # Buscamos archivos que contengan el año (ej: datos_2023_final.csv)
    if os.path.exists(ruta_base):
        archivos = os.listdir(ruta_base)
        coincidencia = [f for f in archivos if str(anio_sel) in f and f.endswith(".csv")]
        if coincidencia:
            df = pd.read_csv(os.path.join(ruta_base, coincidencia[0]))

# 4. RENDERIZADO DE DATOS (Interfaz Visual Intacta)
if not df.empty:
    # Estandarización de columnas (Tu lógica original)
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Identificar columnas críticas
    col_inv = 'gasto_gestion_amb' if 'gasto_gestion_amb' in df.columns else df.columns[-1]
    col_sec = 'seccion_economica' if 'seccion_economica' in df.columns else df.columns[1]

    # MÉTRICAS PRINCIPALES
    m1, m2 = st.columns(2)
    with m1:
        total_inv = df[col_inv].sum()
        st.metric(f"Inversión Total {anio_sel}", f"$ {total_inv:,.0f}")
    with m2:
        # Usamos id_empresa si existe en el CSV o en la DB
        conteo = df['id_empresa'].nunique() if 'id_empresa' in df.columns else len(df)
        st.metric("Registros Analizados", f"{conteo:,}")

    st.divider()

    # GRÁFICO TREEMAP (Tu diseño de visualización)
    st.subheader(f"🌳 Distribución de Inversión por Sector ({anio_sel})")
    
    # Agrupamos para el gráfico
    df_tree = df.groupby(col_sec)[col_inv].sum().reset_index()
    df_tree = df_tree[df_tree[col_inv] > 0] # Solo sectores con inversión
    
    if not df_tree.empty:
        fig = px.treemap(
            df_tree, 
            path=[col_sec], 
            values=col_inv, 
            color=col_inv, 
            color_continuous_scale='RdYlGn_r',
            labels={col_inv: 'Inversión ($)', col_sec: 'Sector'}
        )
        fig.update_layout(margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de inversión para graficar en este periodo.")

else:
    st.warning(f"⚠️ No se encontró información para el año {anio_sel} ni en la nube ni en local.")