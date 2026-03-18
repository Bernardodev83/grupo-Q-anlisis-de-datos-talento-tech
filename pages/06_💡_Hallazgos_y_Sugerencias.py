import streamlit as st
import pandas as pd
import os

# 1. Configuración de la página
st.set_page_config(page_title="Hallazgos y Sugerencias", layout="wide")

# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)




st.title("💡 Hallazgos Estratégicos y Sugerencias")
st.markdown("""
Esta sección consolida la inteligencia del sistema **EcoAnalytics Pro**. 
Filtre por periodo para entender la evolución de los indicadores industriales.
""")
st.markdown("---")

# 2. El Filtro Maestro (Selector de Periodo)
periodo = st.selectbox(
    "📅 Seleccione el periodo de análisis:",
    ["2019: Estabilidad Pre-Pandemia", 
     "2020-2021: Crisis y Parálisis", 
     "2022-2023: Recuperación y Eficiencia"]
)

# 3. Contenedor Dinámico de Hallazgos
st.subheader(f"🔍 Análisis del Periodo: {periodo}")

col_info, col_img = st.columns([2, 1])

with col_info:
    if "2019" in periodo:
        st.info("✅ **Diagnóstico de Normalidad**")
        st.write("""
        * **Consumo Base:** Los niveles de energía y agua muestran una operación industrial al 100%. 
        * **Inversión:** Las empresas mantenían un presupuesto activo para la protección del medio ambiente sin interrupciones.
        * **Hallazgo:** Fue el último año de predictibilidad total antes del choque externo.
        """)
        
    elif "2020-2021" in periodo:
        st.error("🚨 **Diagnóstico de Crisis**")
        st.write("""
        * **Efecto COVID:** La curva de contagios (ver Pág 04) forzó cierres que desplomaron el consumo energético.
        * **Desabastecimiento Operativo:** Se observa que la inversión ambiental se detuvo para priorizar la nómina y la bioseguridad.
        * **Hallazgo:** El sector industrial sufrió una contracción operativa del 15% al 20% en sus indicadores de sostenibilidad.
        """)
        
    else:
        st.success("📈 **Diagnóstico de Recuperación**")
        st.write("""
        * **Eficiencia Energética:** Las empresas regresaron a producir, pero con un consumo de agua más controlado (Aprendizaje de crisis).
        * **Reactivación de Proyectos:** Se detecta un aumento en la compra de maquinaria más limpia para recuperar el tiempo perdido.
        * **Hallazgo:** La industria es más resiliente y utiliza los datos del DANE para optimizar costos.
        """)

with col_img:
    # Espacio para una métrica visual rápida según el periodo
    if "Crisis" in periodo:
        st.metric("Riesgo Industrial", "Alto", delta="Crítico")
    elif "Recuperación" in periodo:
        st.metric("Tendencia", "Positiva", delta="Crecimiento")
    else:
        st.metric("Estabilidad", "Óptima")

st.divider()

# 4. Sugerencias Permanentes (Saber qué hacer)
st.header("🚀 Sugerencias y Hoja de Ruta")

tab1, tab2 = st.tabs(["🔧 Operativas (Técnicas)", "📊 Gerenciales (Estratégicas)"])

with tab1:
    st.markdown("""
    * **Optimización de Agua:** Implementar sistemas de recirculación en plantas que mostraron consumos altos durante la inactividad de 2020.
    * **Sensores Inteligentes:** Instalar medidores de energía IoT que alerten sobre picos de consumo innecesarios fuera de horas laborales.
    * **Auditoría Ambiental:** Realizar un balance de emisiones ahora que la producción volvió a niveles de 2019.
    """)

with tab2:
    st.markdown("""
    * **Fondo de Reserva Ambiental:** Crear un rubro financiero que proteja los proyectos de sostenibilidad ante futuras pandemias o crisis.
    * **Cultura de Datos:** Integrar los microdatos del DANE mensualmente en las juntas directivas para tomar decisiones basadas en evidencia.
    * **Capacitación:** Entrenar al personal en el uso del Dashboard para que cada área vigile sus propios indicadores.
    """)

st.markdown("---")
st.caption("EcoAnalytics Pro - Análisis desarrollado por Bernardo para la toma de decisiones basada en microdatos.")