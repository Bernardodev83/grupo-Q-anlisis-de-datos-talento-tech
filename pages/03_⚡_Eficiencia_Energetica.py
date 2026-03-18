import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Configuración de la página
st.set_page_config(page_title="Eficiencia Energética", layout="wide")


# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)
    

# 2. Título y Sección de Información
st.title("⚡ Eficiencia Energética e Índice ICA")

with st.expander("ℹ️ Acerca de esta página"):
    st.markdown("""
    Este módulo analiza el **consumo de energía** y calcula un **Índice de Desempeño (ICA)**.
    * **Velocímetro ICA:** Relación entre inversión ambiental y consumo.
    * **Top 10 Barras:** Comparativa directa de los mayores consumidores.
    * **Mapa de Distribución:** Visualización proporcional del peso de cada sector.
    """)

# 3. Selector de Año
anio = st.sidebar.selectbox("Seleccionar Año:", [2023, 2022, 2021, 2020, 2019], key="ener_final_v3")
ruta = f"datos/procesados/datos_{anio}_final.csv"

if os.path.exists(ruta):
    df = pd.read_csv(ruta)
    
    # Agrupamos por sector
    df_agrupado = df.groupby('seccion_economica').agg({
        'consumo_energia_kwh': 'sum',
        'gasto_gestion_amb': 'sum'
    }).reset_index()
    
    df_agrupado = df_agrupado[df_agrupado['consumo_energia_kwh'] > 0]

    if not df_agrupado.empty:
        # --- 1. VELOCÍMETRO (GAUGE) COMPACTO ---
        inv_total = df_agrupado['gasto_gestion_amb'].sum()
        cons_total = df_agrupado['consumo_energia_kwh'].sum()
        ica_score = min(100, (inv_total / (cons_total * 0.05)) * 100) if cons_total > 0 else 0

        st.subheader("🚀 Indicador de Desempeño Ambiental (ICA)")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = ica_score,
            number = {'suffix': "%", 'font': {'size': 35}},
            title = {'text': f"Eficiencia - {anio}", 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 40], 'color': '#ff4b4b'},
                    {'range': [40, 70], 'color': '#ffa421'},
                    {'range': [70, 100], 'color': '#21c354'}
                ]
            }
        ))
        fig_gauge.update_layout(height=220, margin=dict(t=20, b=0, l=40, r=40))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.divider()

        # --- 2. TOP 10 BARRAS ---
        top_10_ener = df_agrupado.nlargest(10, 'consumo_energia_kwh')
        
        st.subheader(f"🔝 Top 10 Sectores con Mayor Consumo ({anio})")
        fig_bar = px.bar(
            top_10_ener, 
            x='consumo_energia_kwh', 
            y='seccion_economica', 
            orientation='h', 
            color='consumo_energia_kwh',
            color_continuous_scale='YlOrRd',
            text_auto='.2s'
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=450, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # --- 3. MAPA DE DISTRIBUCIÓN (TREEMAP) - REEMPLAZA BURBUJAS ---
        st.subheader(f"🗺️ Distribución del Consumo por Sector ({anio})")
        st.write("Este mapa permite ver proporcionalmente qué sectores dominan el consumo sin saturar la pantalla del celular.")
        
        fig_tree = px.treemap(
            top_10_ener, 
            path=['seccion_economica'], 
            values='consumo_energia_kwh',
            color='consumo_energia_kwh',
            color_continuous_scale='YlOrRd',
            labels={'consumo_energia_kwh': 'Consumo Total'}
        )
        # Ajustamos para que se vea bien en cualquier dispositivo
        fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=400)
        st.plotly_chart(fig_tree, use_container_width=True)
            
    else:
        st.warning(f"No hay datos de energía para mostrar en {anio}.")
else:
    st.error(f"❌ No se encontró el archivo: {ruta}")