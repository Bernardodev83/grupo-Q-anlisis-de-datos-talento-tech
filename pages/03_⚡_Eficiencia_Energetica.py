import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Eficiencia Energética - DANE", layout="wide")

# Encabezado con Logo
st.image("https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png", width=200)
st.caption("Fuente Oficial: DANE Colombia")
st.markdown("<h1 style='text-align: center; color: #E67E22;'>⚡ Eficiencia Energética e Índice ICA</h1>", unsafe_allow_html=True)
st.divider()

# 2. SELECTOR DE AÑO
col_f, _ = st.columns([1, 2])
with col_f:
    anio_sel = st.selectbox("📅 Seleccione el Año de Análisis:", [2023, 2022, 2021, 2020, 2019], index=0)

# 3. CARGA DE DATOS
df = pd.DataFrame()
ruta_data = "data"

if os.path.exists(ruta_data):
    for raiz, dirs, archivos in os.walk(ruta_data):
        for f in archivos:
            if str(anio_sel) in f and f.lower().endswith(".csv"):
                df = pd.read_csv(os.path.join(raiz, f))
                break

# 4. PROCESAMIENTO Y GRÁFICOS
if not df.empty:
    df.columns = df.columns.str.strip().str.lower()
    
    col_ener = "consumo_energia_kwh"
    col_sec = "seccion_economica"
    col_gast_amb = "gasto_gestion_amb"
    col_gast_tot = "gastos_totales"

    df[col_ener] = pd.to_numeric(df[col_ener], errors='coerce').fillna(0)
    df[col_gast_amb] = pd.to_numeric(df[col_gast_amb], errors='coerce').fillna(0)
    df[col_gast_tot] = pd.to_numeric(df[col_gast_tot], errors='coerce').fillna(1)

    # --- A. VELOCÍMETRO ICA ---
    st.subheader(f"🚀 Indicador de Desempeño Ambiental (ICA) - {anio_sel}")
    
    # Cálculo con multiplicador de visibilidad (50.000)
    indice_calculado = (df[col_gast_amb].sum() / df[col_gast_tot].sum()) * 50000
    valor_gauge = min(indice_calculado, 100)

    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valor_gauge,
        number = {'suffix': " pts", 'valueformat': '.1f', 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#E67E22"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 30], 'color': "#FFB3B3"},
                {'range': [30, 70], 'color': "#FFF3B3"},
                {'range': [70, 100], 'color': "#B3FFB3"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': valor_gauge
            }
        }
    ))
    fig_gauge.update_layout(height=350, margin=dict(t=50, b=0))
    st.plotly_chart(fig_gauge, width='stretch')

    # --- NOTA EXPLICATIVA DE LOS PUNTOS (PTS) ---
    st.info("""
        **💡 Nota sobre el Indicador (pts):**
        El puntaje en el velocímetro representa el **Índice de Inversión Ambiental**. 
        Se calcula comparando el gasto en gestión ambiental frente al gasto total de los sectores industriales. 
        Un mayor puntaje indica una industria más comprometida con la sostenibilidad y la protección del entorno.
    """)

    st.divider()

    # --- B. TOP 10 CONSUMO ---
    st.subheader(f"🔝 Top 10 Sectores con Mayor Consumo ({anio_sel})")
    df_top10 = df.groupby(col_sec)[col_ener].sum().reset_index().sort_values(by=col_ener, ascending=True).tail(10)
    
    fig_bar = px.bar(
        df_top10, x=col_ener, y=col_sec, orientation='h',
        color=col_ener, color_continuous_scale='Oranges',
        labels={col_ener: 'Consumo (kWh)', col_sec: 'Sector'}
    )
    fig_bar.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_bar, width='stretch')

    st.divider()

    # --- C. DISTRIBUCIÓN (TREEMAP) ---
    st.subheader(f"🗺️ Distribución del Consumo por Sector ({anio_sel})")
    df_tree = df.groupby(col_sec)[col_ener].sum().reset_index()
    df_tree = df_tree[df_tree[col_ener] > 0]
    
    fig_tree = px.treemap(
        df_tree, path=[col_sec], values=col_ener,
        color=col_ener, color_continuous_scale='RdYlGn_r'
    )
    fig_tree.update_traces(textinfo="label+percent root")
    st.plotly_chart(fig_tree, width='stretch')

else:
    st.warning(f"⚠️ No se encontró el archivo de datos para el año {anio_sel}.")