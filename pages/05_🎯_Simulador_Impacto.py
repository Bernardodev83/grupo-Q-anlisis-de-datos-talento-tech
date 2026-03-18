import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 1. Configuración de la página
st.set_page_config(page_title="Simulador de Impacto", layout="wide")

# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)




# 2. Título e Instrucciones
st.title("🎯 Simulador de Eco-Eficiencia")
st.markdown("""
Esta herramienta permite proyectar el **ahorro económico** potencial si los sectores industriales implementan estrategias de optimización de recursos.
""")

# 3. Sidebar: Configuración del Escenario
st.sidebar.header("⚙️ Configuración del Escenario")
anio = st.sidebar.selectbox("Año de Referencia:", [2023, 2022, 2021, 2020, 2019], key="sim_year")

st.sidebar.subheader("📉 Metas de Ahorro")
ahorro_agua = st.sidebar.slider("Ahorro en Agua (%)", 0, 50, 10)
ahorro_ener = st.sidebar.slider("Ahorro en Energía (%)", 0, 50, 15)

# Costos estimados (puedes ajustarlos según la realidad del mercado)
costo_m3 = st.sidebar.number_input("Costo promedio m³ Agua ($)", value=4500)
costo_kwh = st.sidebar.number_input("Costo promedio kWh Energía ($)", value=800)

# 4. Carga de Datos
ruta = f"datos/procesados/datos_{anio}_final.csv"

if os.path.exists(ruta):
    df = pd.read_csv(ruta)
    
    # Cálculos actuales
    total_agua_act = df['consumo_agua_m3'].sum()
    total_ener_act = df['consumo_energia_kwh'].sum()
    
    # Proyecciones
    m3_ahorrados = total_agua_act * (ahorro_agua / 100)
    kwh_ahorrados = total_ener_act * (ahorro_ener / 100)
    
    dinero_ahorro_agua = m3_ahorrados * costo_m3
    dinero_ahorro_ener = kwh_ahorrados * costo_kwh
    ahorro_total = dinero_ahorro_agua + dinero_ahorro_ener

    # --- KPI'S DE IMPACTO ---
    st.subheader(f"📊 Resultados del Simulador - Año {anio}")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Agua Recuperable", f"{m3_ahorrados:,.0f} m³", f"-{ahorro_agua}%", delta_color="normal")
    with c2:
        st.metric("Energía Optimizada", f"{kwh_ahorrados:,.0f} kWh", f"-{ahorro_ener}%", delta_color="normal")
    with c3:
        st.metric("Ahorro Económico Estimado", f"$ {ahorro_total:,.0f}", "Potencial", delta_color="off")

    st.divider()

    # --- GRÁFICO DE IMPACTO ECONÓMICO ---
    st.subheader("💰 Impacto en la Estructura de Costos")
    
    # Datos para el gráfico comparativo
    categorias = ['Situación Actual', 'Con Optimización']
    costo_actual = (total_agua_act * costo_m3) + (total_ener_act * costo_kwh)
    costo_proyectado = costo_actual - ahorro_total
    
    fig_impacto = go.Figure()
    fig_impacto.add_trace(go.Bar(
        name='Gasto Proyectado',
        x=categorias,
        y=[costo_actual, costo_proyectado],
        marker_color=['#95a5a6', '#27ae60'],
        text=[f"$ {costo_actual:,.0f}", f"$ {costo_proyectado:,.0f}"],
        textposition='auto'
    ))

    fig_impacto.update_layout(
        title="Reducción de Gastos Operativos (Agua + Energía)",
        yaxis_title="Pesos Colombianos ($)",
        template="plotly_white",
        height=500
    )
    
    st.plotly_chart(fig_impacto, use_container_width=True)

    # --- TABLA POR SECTORES ---
    with st.expander("🔍 Ver detalle de ahorro por Sector Económico"):
        df_sectores = df.groupby('seccion_economica').agg({
            'consumo_agua_m3': 'sum',
            'consumo_energia_kwh': 'sum'
        }).reset_index()
        
        df_sectores['Ahorro $ Agua'] = df_sectores['consumo_agua_m3'] * (ahorro_agua/100) * costo_m3
        df_sectores['Ahorro $ Energía'] = df_sectores['consumo_energia_kwh'] * (ahorro_ener/100) * costo_kwh
        df_sectores['Ahorro Total Potencial'] = df_sectores['Ahorro $ Agua'] + df_sectores['Ahorro $ Energía']
        
        st.dataframe(df_sectores.sort_values('Ahorro Total Potencial', ascending=False), use_container_width=True)

else:
    st.error(f"No se encontraron datos para el año {anio}. Por favor, procesa los archivos primero.")