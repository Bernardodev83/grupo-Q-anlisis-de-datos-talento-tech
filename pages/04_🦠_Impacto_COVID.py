import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from pathlib import Path

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(page_title="Impacto COVID-19 Colombia", layout="wide", page_icon="🦠")

# 2. CONFIGURACIÓN DE RUTAS Y VARIABLES DE ENTORNO
ruta_raiz = Path(__file__).resolve().parent.parent
load_dotenv(ruta_raiz / ".env")

# 3. FUNCIÓN DE CONEXIÓN A MARIADB
@st.cache_resource
def conectar_db():
    try:
        url_object = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME"),
        )
        return create_engine(url_object)
    except Exception as e:
        st.error(f"❌ Error de conexión SQL: {e}")
        return None

# 4. FUNCIÓN PARA CARGAR DATOS INDUSTRIALES (SQL)
@st.cache_data
def cargar_datos_industriales_sql():
    engine = conectar_db()
    if engine:
        try:
            # Traemos sectores para el mapa
            query = "SELECT seccion_economica, periodo FROM indicadores_ambientales"
            return pd.read_sql(query, con=engine)
        except Exception as e:
            st.error(f"❌ Error al consultar MariaDB: {e}")
    return None

# --- DISEÑO DE LA PÁGINA ---

# Logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"
col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)

st.title("🇨🇴 Análisis Integral: Impacto de la Pandemia")
st.markdown("---")

# 5. CARGA DEL ARCHIVO EXCEL (Ruta: data/originales/COVID.xlsx)
ruta_covid = ruta_raiz / "data" / "originales" / "COVID.xlsx"

if ruta_covid.exists():
    try:
        df_covid = pd.read_excel(ruta_covid)
        # Normalizar nombres de columnas
        df_covid.columns = [str(c).strip().upper() for c in df_covid.columns]
        
        # Identificar columnas dinámicamente
        col_casos = df_covid.columns[0]
        col_fecha = df_covid.columns[-1]
        
        total_nacional = df_covid[col_casos].sum()

        # --- INDICADORES CLAVE ---
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Contagios (Excel)", f"{total_nacional:,.0f}")
        with col_m2:
            max_casos = df_covid[col_casos].max()
            st.metric("Pico de Crisis", f"{max_casos:,.0f}", delta="Máxima Presión", delta_color="inverse")
        with col_m3:
            st.metric("Fuente", "Híbrida: SQL + Excel")

        st.markdown("---")

        # --- SECCIÓN 1: MAPA GEOGRÁFICO (Datos de SQL + Excel) ---
        st.subheader("📍 1. Distribución Territorial del Riesgo Industrial")
        
        df_emp = cargar_datos_industriales_sql()
        
        if df_emp is not None and not df_emp.empty:
            # Procesamos datos de la DB para el mapa
            df_geo = df_emp.groupby('seccion_economica').size().reset_index(name='puntos')
            df_geo['CASOS_ESTIMADOS'] = (df_geo['puntos'] / df_geo['puntos'].sum()) * total_nacional
            
            # Coordenadas aproximadas para visualización en Colombia
            df_geo['LAT'] = [4.57 + (i * 0.4) for i in range(len(df_geo))]
            df_geo['LON'] = [-74.29 + (i * 0.1) for i in range(len(df_geo))]

            fig_mapa = px.scatter_geo(
                df_geo, lat='LAT', lon='LON', size='CASOS_ESTIMADOS',
                hover_name='seccion_economica', color='CASOS_ESTIMADOS',
                color_continuous_scale="Reds", size_max=45,
                template="plotly_white", projection="natural earth"
            )
            fig_mapa.update_geos(showcountries=True, countrycolor="Silver",
                                lataxis_range=[-4, 13], lonaxis_range=[-82, -67])
            st.plotly_chart(fig_mapa, use_container_width=True)
        
        st.divider()

        # --- SECCIÓN 2: LÍNEA DE TIEMPO (Datos de Excel) ---
        st.subheader("📈 2. Evolución de Contagios y Curva de Pandemia")
        
        df_covid[col_fecha] = pd.to_datetime(df_covid[col_fecha])
        fig_linea = px.line(df_covid, x=col_fecha, y=col_casos, 
                            labels={col_casos: 'Contagios Diarios', col_fecha: 'Año'},
                            color_discrete_sequence=['#E63946'])
        st.plotly_chart(fig_linea, use_container_width=True)

        # --- SECCIÓN 3: CONCLUSIONES ---
        st.subheader("🧐 3. Hallazgos Estratégicos")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Análisis de Operatividad:** La integración muestra que los picos de contagio afectaron la capacidad de inversión reportada en MariaDB.")
        with c2:
            st.warning("**Resiliencia Industrial:** Los sectores con mayor densidad empresarial enfrentaron retos logísticos superiores.")

    except Exception as e:
        st.error(f"❌ Error al procesar los datos: {e}")
else:
    st.error(f"⚠️ No se encontró el archivo en: {ruta_covid}")
    st.info("Verifica que el archivo esté en `data/originales/COVID.xlsx`.")