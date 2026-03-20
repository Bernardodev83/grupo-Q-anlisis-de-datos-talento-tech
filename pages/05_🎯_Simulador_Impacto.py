import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from pathlib import Path

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Esto permite que el script encuentre la carpeta 'utils' desde la carpeta 'pages'
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

try:
    from utils.conexion import get_connection
except ImportError:
    st.error("❌ No se encontró el módulo de conexión en utils/conexion.py")

# --- 2. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Simulador Ambiental - DANE", 
    layout="wide", 
    page_icon="🧮"
)

# Estética DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"
st.image(url_logo_dane, width=200)
st.title("🧮 Simulador de Impacto Ambiental")
st.info("Proyecta el ahorro y la eficiencia basándote en los datos reales de la industria colombiana cargados en la nube.")
st.divider()

# --- 3. MOTOR DE SIMULACIÓN (OBTENER PROMEDIOS) ---
@st.cache_data(ttl=600)
def obtener_promedios_reales():
    """Consulta la DB para obtener promedios históricos y alimentar el simulador"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT AVG(consumo_energia_kwh), AVG(ahorro_agua_m3) FROM indicadores_ambientales"
            cursor.execute(query)
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            
            # Si la DB tiene datos, los usamos. Si no, devolvemos valores base.
            avg_e = float(res[0]) if res and res[0] else 8500.0
            avg_a = float(res[1]) if res and res[1] else 450.0
            return avg_e, avg_a, "✅ Datos basados en promedios reales de la nube (Aiven)"
        except Exception as e:
            return 5000.0, 200.0, f"⚠️ Error en consulta: Usando valores de referencia manuales."
    return 5000.0, 200.0, "⚠️ Modo Offline: Usando valores de referencia (Sin conexión a la nube)"

# Ejecutamos la carga de promedios
avg_energia_db, avg_agua_db, mensaje_estado = obtener_promedios_reales()
st.caption(mensaje_estado)

# --- 4. INTERFAZ DE USUARIO (COLUMNAS) ---
col_config, col_metas = st.columns(2)

with col_config:
    st.subheader("⚙️ Configuración de la Empresa")
    sector = st.selectbox("Seleccione el Sector Industrial:", [
        "Manufactura", "Servicios", "Comercio", "Minería", "Alimentos", "Químicos", "Textiles"
    ])
    consumo_actual_e = st.number_input(
        "Consumo de Energía Actual (kWh):", 
        value=avg_energia_db, 
        step=100.0,
        help="Este valor inicia con el promedio histórico de la base de datos."
    )
    consumo_actual_a = st.number_input(
        "Consumo de Agua Actual (m³):", 
        value=avg_agua_db, 
        step=10.0
    )

with col_metas:
    st.subheader("🎯 Metas de Reducción")
    meta_e = st.slider("% Reducción de Energía deseada:", 0, 50, 15)
    meta_a = st.slider("% Reducción de Agua deseada:", 0, 50, 10)
    costo_kwh = st.number_input("Costo promedio por kWh ($COP):", value=650, step=10)

# --- 5. LÓGICA DE CÁLCULO ---
ahorro_e_anual = (consumo_actual_e * (meta_e / 100)) * 12
ahorro_a_anual = (consumo_actual_a * (meta_a / 100)) * 12
dinero_ahorrado_anual = ahorro_e_anual * costo_kwh

st.divider()

# --- 6. RENDERIZADO DE RESULTADOS ---
st.subheader("🚀 Proyección de Impacto Anual")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Energía a Ahorrar (Año)", f"{ahorro_e_anual:,.1f} kWh", f"-{meta_e}%")
with m2:
    st.metric("Agua a Ahorrar (Año)", f"{ahorro_a_anual:,.1f} m³", f"-{meta_a}%")
with m3:
    st.metric("Ahorro Económico Est.", f"$ {dinero_ahorrado_anual:,.0f}", help="Cálculo basado en ahorro de energía")

# --- 7. GRÁFICO COMPARATIVO (PLOTLY) ---
st.write("### 📊 Comparativa Visual: Situación Actual vs. Meta")

# Creamos un DataFrame para graficar
df_plot = pd.DataFrame({
    'Indicador': ['Energía (kWh)', 'Agua (m³)'],
    'Actual': [consumo_actual_e, consumo_actual_a],
    'Meta': [consumo_actual_e * (1 - meta_e/100), consumo_actual_a * (1 - meta_a/100)]
})

# Reorganizamos los datos para que Plotly los entienda bien (Melt)
df_melted = df_plot.melt(id_vars='Indicador', var_name='Escenario', value_name='Valor')

fig_sim = px.bar(
    df_melted, 
    x='Indicador', 
    y='Valor', 
    color='Escenario', 
    barmode='group',
    color_discrete_map={'Actual': '#BDC3C7', 'Meta': '#27AE60'}, # Gris vs Verde
    text_auto='.2s',
    template="plotly_white"
)

fig_sim.update_layout(
    height=400, 
    margin=dict(t=20, b=20, l=20, r=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_sim, use_container_width=True)

# Conclusión dinámica final
st.success(f"""
    💡 **Conclusión del Simulador:** Si el sector de **{sector}** implementa estas metas, lograría un ahorro económico de 
    **$ {dinero_ahorrado_anual:,.0f} COP** al año, mejorando significativamente su Índice de Desempeño Ambiental (ICA).
""")