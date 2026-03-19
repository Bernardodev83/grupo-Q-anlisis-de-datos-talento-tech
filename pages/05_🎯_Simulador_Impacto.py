import streamlit as st
import pandas as pd
from utils.conexion import obtener_conexion
from sqlalchemy import text

st.set_page_config(page_title="Simulador Ambiental", layout="wide")

st.title("🧮 Simulador de Impacto Ambiental")
st.info("Proyecta el ahorro y la eficiencia basándote en los datos reales de MariaDB.")

# 1. CONEXIÓN
engine = obtener_conexion()

if engine:
    try:
        # 2. OBTENER PROMEDIOS REALES DE LA DB (Para que la simulación sea realista)
        with engine.connect() as con:
            query_avg = text("""
                SELECT AVG(consumo_energia_kwh) as avg_energia, 
                       AVG(consumo_agua_m3) as avg_agua 
                FROM indicadores_ambientales
            """)
            res = con.execute(query_avg).fetchone()
            # Si la DB está vacía, usamos valores por defecto
            avg_energia_db = float(res[0]) if res[0] else 5000.0
            avg_agua_db = float(res[1]) if res[1] else 200.0

        st.success(f"📈 Base de simulación actualizada según el promedio histórico de la base de datos.")

        # --- INTERFAZ DEL SIMULADOR ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚙️ Configuración de la Empresa")
            sector = st.selectbox("Sector Industrial:", ["Manufactura", "Servicios", "Comercio", "Minería"])
            consumo_actual_e = st.number_input("Consumo Energía Actual (kWh):", value=avg_energia_db)
            consumo_actual_a = st.number_input("Consumo Agua Actual (m3):", value=avg_agua_db)

        with col2:
            st.subheader("🎯 Metas de Reducción")
            meta_e = st.slider("% Reducción Energía:", 0, 50, 15)
            meta_a = st.slider("% Reducción Agua:", 0, 50, 10)

        # --- CÁLCULOS ---
        ahorro_e = consumo_actual_e * (meta_e / 100)
        ahorro_a = consumo_actual_a * (meta_a / 100)
        
        # Supongamos un costo promedio (puedes ajustarlo)
        costo_kwh = 650 
        dinero_ahorrado = ahorro_e * costo_kwh

        st.divider()

        # --- RESULTADOS ---
        st.subheader("🚀 Proyección de Resultados")
        res1, res2, res3 = st.columns(3)
        
        res1.metric("Energía a Ahorrar", f"{ahorro_e:,.2f} kWh", f"-{meta_e}%", delta_color="normal")
        res2.metric("Agua a Ahorrar", f"{ahorro_a:,.2f} m3", f"-{meta_a}%", delta_color="normal")
        res3.metric("Ahorro Estimado ($)", f"$ {dinero_ahorrado:,.0f}", help="Basado en costo promedio de kWh")

        # Gráfico comparativo
        st.write("### Comparativa: Actual vs Meta")
        data_sim = pd.DataFrame({
            'Concepto': ['Energía (kWh)', 'Agua (m3)'],
            'Actual': [consumo_actual_e, consumo_actual_a],
            'Meta': [consumo_actual_e - ahorro_e, consumo_actual_a - ahorro_a]
        })
        st.bar_chart(data_sim.set_index('Concepto'))

    except Exception as e:
        st.error(f"❌ Error al cargar datos para el simulador: {e}")
else:
    st.error("❌ No hay conexión con MariaDB para obtener los promedios.")