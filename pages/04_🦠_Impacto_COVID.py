import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

try:
    # Usamos nuestra conexión estandarizada
    from utils.conexion import get_connection
except ImportError:
    st.error("❌ No se encontró el módulo de conexión en utils.")

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Impacto COVID-19 Colombia", layout="wide", page_icon="🦠")

# 2. CARGA DE DATOS INDUSTRIALES (SQL con caché)
@st.cache_data
def cargar_datos_industriales_sql():
    conn = get_connection()
    if conn:
        try:
            # Traemos sectores para el mapa (Limitamos para optimizar)
            query = "SELECT seccion_economica, periodo FROM indicadores_ambientales LIMIT 1000"
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error SQL: {e}")
    return None

# --- DISEÑO DE LA PÁGINA ---

# Encabezado estilo DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"
st.image(url_logo_dane, width=200)
st.title("🇨🇴 Análisis Integral: Impacto de la Pandemia")
st.markdown("---")

# 3. CARGA DEL ARCHIVO EXCEL (Datos de respaldo en carpeta originales)
ruta_covid = ruta_raiz / "data" / "originales" / "COVID.xlsx"

if ruta_covid.exists():
    try:
        df_covid = pd.read_excel(ruta_covid)
        # Limpieza de nombres de columnas
        df_covid.columns = [str(c).strip().upper() for c in df_covid.columns]
        
        # Identificación dinámica de columnas (asumiendo que la primera es Casos y la última Fecha)
        col_casos = df_covid.columns[0] 
        col_fecha = df_covid.columns[-1] 
        
        total_nacional = df_covid[col_casos].sum()

        # --- INDICADORES CLAVE ---
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Contagios (Nacional)", f"{total_nacional:,.0f}")
        with m2:
            max_casos = df_covid[col_casos].max()
            st.metric("Pico de Crisis", f"{max_casos:,.0f}")
        with m3:
            # Verificación de estado en tiempo real
            test_conn = get_connection()
            estado_db = "✅ Online (Aiven)" if test_conn else "⚠️ Offline (Local)"
            if test_conn: test_conn.close()
            st.metric("Estado Base de Datos", estado_db)

        st.markdown("---")

        # --- SECCIÓN 1: MAPA GEOGRÁFICO ---
        st.subheader("📍 1. Distribución Territorial del Riesgo Industrial")
        
        df_emp = cargar_datos_industriales_sql()
        
        if df_emp is not None and not df_emp.empty:
            # Procesamos datos para el mapa basado en sectores de la DB
            df_geo = df_emp.groupby('seccion_economica').size().reset_index(name='puntos')
            df_geo['CASOS_ESTIMADOS'] = (df_geo['puntos'] / df_geo['puntos'].sum()) * total_nacional
            
            # Coordenadas base de Colombia para dispersión visual
            df_geo['LAT'] = [4.57 + (i * 0.2) for i in range(len(df_geo))]
            df_geo['LON'] = [-74.29 + (i * 0.04) for i in range(len(df_geo))]

            fig_mapa = px.scatter_geo(
                df_geo, lat='LAT', lon='LON', size='CASOS_ESTIMADOS',
                hover_name='seccion_economica', color='CASOS_ESTIMADOS',
                color_continuous_scale="Reds", size_max=35,
                template="plotly_white", projection="natural earth"
            )
            fig_mapa.update_geos(
                showcountries=True, countrycolor="Silver",
                lataxis_range=[-4, 13], lonaxis_range=[-82, -67],
                visible=False, resolution=50, showcoastlines=True,
                showland=True, landcolor="GhostWhite"
            )
            fig_mapa.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_mapa, use_container_width=True)
        else:
            st.warning("⚠️ El mapa requiere datos de la nube para mostrar los sectores industriales.")

        st.divider()

        # --- SECCIÓN 2: LÍNEA DE TIEMPO ---
        st.subheader("📈 2. Evolución de Contagios y Curva de Pandemia")
        
        df_covid[col_fecha] = pd.to_datetime(df_covid[col_fecha])
        fig_linea = px.line(df_covid, x=col_fecha, y=col_casos, 
                            labels={col_casos: 'Contagios Diarios', col_fecha: 'Línea de Tiempo'},
                            color_discrete_sequence=['#E63946'],
                            title="Curva Epidemiológica en Sectores Industriales")
        st.plotly_chart(fig_linea, use_container_width=True)

        # --- SECCIÓN 3: CONCLUSIONES ---
        st.subheader("🧐 3. Hallazgos Estratégicos")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Análisis de Datos:** La integración de datos en la nube permite cruzar la actividad industrial con los picos de contagio reportados.")
        with c2:
            st.warning("**Resiliencia:** El sistema híbrido asegura que el análisis de crisis sea visible incluso si la base de datos está en mantenimiento.")

    except Exception as e:
        st.error(f"❌ Error al procesar los datos: {e}")
else:
    st.error(f"⚠️ No se encontró el archivo Excel en: {ruta_covid}")
    st.info("Asegúrate de que el archivo 'COVID.xlsx' esté en la carpeta 'data/originales/'.")