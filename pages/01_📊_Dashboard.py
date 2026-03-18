import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de página
st.set_page_config(page_title="Dashboard General", layout="wide")

# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)



# Título y Descripción
st.title("📊 Dashboard General de Inversión")

with st.expander("ℹ️ Acerca de esta página", expanded=True):
    st.markdown("""
    En este módulo encontrará una **visión global** de los recursos destinados a la gestión ambiental. 
    * **Propósito:** Identificar cuáles son los sectores económicos que más invierten en protección del medio ambiente.
    * **Variables clave:** Gastos totales y Gasto en gestión ambiental (EAS).
    * **Visualización:** El gráfico de rectángulos (*Treemap*) permite ver la proporción de inversión de cada sector de forma jerárquica.
    """)

# Función de carga
def cargar_datos(anio):
    ruta = f"datos/procesados/datos_{anio}_final.csv"
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return None

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    anio_sel = st.selectbox("Seleccionar Año:", [2023, 2022, 2021, 2020, 2019], index=0)

df = cargar_datos(anio_sel)

if df is not None:
    # Métricas Rápidas
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Inversión Ambiental Total", f"${df['gasto_gestion_amb'].sum():,.0f}")
    with m2:
        st.metric("Empresas Registradas", f"{len(df):,}")

    st.divider()

    # Gráfico Treemap
    st.subheader(f"Distribución de Inversión por Sector - Año {anio_sel}")
    fig_tree = px.treemap(
        df[df['gasto_gestion_amb'] > 0], 
        path=['seccion_economica'], 
        values='gasto_gestion_amb',
        color='gasto_gestion_amb',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig_tree, use_container_width=True)
else:
    st.error("No se encontraron datos procesados para este año.")