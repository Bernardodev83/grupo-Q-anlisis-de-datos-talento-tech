import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="EcoAnalytics Pro | DANE EAS",
    page_icon="🌿",
    layout="wide"
)

# 2. Barra Lateral
st.sidebar.title("🌿 EcoAnalytics Pro")
st.sidebar.markdown("---")
st.sidebar.info("Análisis de Microdatos DANE (2019-2023)")

# 3. CUERPO PRINCIPAL (Portada)

# --- LOGO DESDE DIRECCIÓN WEB ---
# Usamos una URL directa del logo del DANE
url_logo_dane = "https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png"

col_izq, col_centro, col_der = st.columns([1, 2, 1])
with col_centro:
    # Aquí cargamos la imagen directamente con la URL
    st.image(url_logo_dane, caption="Fuente Oficial: DANE Colombia", use_container_width=True)

# --- TÍTULO Y DESCRIPCIÓN ---
st.markdown("---")
st.title("📊 Inteligencia Ambiental Industrial: DANE EAS")
st.write("""
Este Dashboard transforma microdatos complejos en indicadores visuales estratégicos 
para entender la sostenibilidad industrial en Colombia.
""")

# Panel de instrucciones
with st.expander("🚀 ¿Cómo empezar?", expanded=True):
    st.markdown("""
    - Use el menú de la izquierda para ver **Agua** o **Energía**.
    - Revise el impacto del **COVID-19** en la sección dedicada.
    - Consulte los **Hallazgos** para recomendaciones finales.
    """)

st.info("👈 Seleccione una página en el menú lateral para comenzar.")