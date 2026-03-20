import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Hallazgos y Sugerencias - EcoAnalytics", layout="wide", page_icon="💡")

# Logo del DANE centrado (Consistente con tu diseño)
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)

st.title("💡 Hallazgos Estratégicos y Sugerencias")
st.markdown("""
Esta sección consolida la inteligencia del sistema **EcoAnalytics Pro**. 
Aquí interpretamos los microdatos para entender la evolución de la industria frente a los desafíos ambientales y globales.
""")
st.markdown("---")

# 2. SELECTOR DE PERIODO (El Filtro Maestro)
periodo = st.selectbox(
    "📅 Seleccione el periodo de análisis para ver el diagnóstico:",
    ["2019: Estabilidad Pre-Pandemia", 
     "2020-2021: Crisis y Parálisis", 
     "2022-2023: Recuperación y Eficiencia"],
    index=0
)

# 3. CONTENEDOR DINÁMICO DE HALLAZGOS
st.subheader(f"🔍 Análisis del Periodo: {periodo}")

col_info, col_metrica = st.columns([3, 1])

with col_info:
    if "2019" in periodo:
        st.info("✅ **Diagnóstico de Normalidad Operativa**")
        st.markdown("""
        * **Consumo Base:** Los niveles de energía y agua muestran una operación industrial estable y al 100% de capacidad. 
        * **Inversión Constante:** Las empresas mantenían presupuestos activos para protección ambiental sin interrupciones externas.
        * **Hallazgo Clave:** Este periodo sirve como la 'Línea Base' ideal para comparar cualquier métrica de eficiencia futura.
        """)
        
    elif "2020-2021" in periodo:
        st.error("🚨 **Diagnóstico de Crisis y Contingencia**")
        st.markdown("""
        * **Efecto Pandemia:** Los cierres sectoriales provocaron una caída drástica en el consumo energético, pero no proporcional en el gasto fijo.
        * **Priorización de Recursos:** La inversión ambiental se estancó para priorizar la bioseguridad y la estabilidad de la nómina.
        * **Hallazgo Clave:** La resiliencia industrial se puso a prueba; los sectores con mejor gestión previa de datos sobrevivieron con menores costos fijos.
        """)
        
    else:
        st.success("📈 **Diagnóstico de Recuperación y Nueva Eficiencia**")
        st.markdown("""
        * **Aprendizaje Post-Crisis:** Se observa un regreso a la producción con indicadores de agua más optimizados, reflejando una mayor conciencia del recurso.
        * **Modernización:** El aumento en el gasto ambiental sugiere una renovación de maquinaria hacia tecnologías más limpias y eficientes.
        * **Hallazgo Clave:** La industria post-pandemia es más consciente y utiliza herramientas como **EcoAnalytics** para vigilar sus costos operativos.
        """)

with col_metrica:
    # Métrica visual rápida basada en el contexto
    st.markdown("### Estado General")
    if "Crisis" in periodo:
        st.metric("Riesgo Industrial", "Crítico", delta="-18% Actividad", delta_color="inverse")
    elif "Recuperación" in periodo:
        st.metric("Tendencia Actual", "Positiva", delta="+12% Eficiencia")
    else:
        st.metric("Estabilidad", "Óptima", delta="Base")

st.divider()

# 4. HOJA DE RUTA (Sugerencias Permanentes)
st.header("🚀 Sugerencias y Hoja de Ruta para la Industria")

tab_tec, tab_est = st.tabs(["🔧 Sugerencias Operativas", "📊 Sugerencias Estratégicas"])

with tab_tec:
    st.markdown("""
    1. **Optimización Hídrica:** Implementar sistemas de circuito cerrado en sectores de manufactura para reducir la dependencia de fuentes externas.
    2. **Monitoreo IoT:** Instalar telemetría en tiempo real para detectar picos de consumo eléctrico fuera de los turnos de producción.
    3. **Auditoría de Emisiones:** Aprovechar la recuperación económica para certificar procesos bajo normas internacionales de sostenibilidad.
    """)

with tab_est:
    st.markdown("""
    1. **Fondo de Resiliencia:** Crear una reserva financiera específica para proyectos ambientales que no se vea afectada por crisis externas.
    2. **Gobernanza de Datos:** Integrar los reportes del DANE en el tablero de control (KPIs) mensual de la gerencia general.
    3. **Capacitación Continua:** Fomentar una cultura donde cada operario entienda cómo su labor impacta el consumo de agua y energía de la planta.
    """)

# Pie de página final de la aplicación
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "EcoAnalytics Pro v1.0 | Desarrollado por Bernardo | Análisis basado en Microdatos DANE Colombia"
    "</div>", 
    unsafe_allow_html=True
)