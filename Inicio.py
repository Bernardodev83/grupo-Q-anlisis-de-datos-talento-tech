import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="EcoAnalytics Pro - DANE",
    layout="wide",
    page_icon="🌿"
)

# 2. BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.image("https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png", use_container_width=True)
    st.divider()
    st.success("🌿 **EcoAnalytics Pro**")
    st.info("Análisis de Microdatos DANE (2019-2023)")

# 3. CUERPO PRINCIPAL (DISEÑO CENTRADO)

# Logo Principal centrado
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    st.image("https://www.valoraanalitik.com/wp-content/uploads/2018/10/1200px-Colombia_Dane_logo.svg_-696x264.png", 
             caption="Fuente Oficial: DANE Colombia", use_container_width=True)

# Título Principal centrado
st.markdown("<h1 style='text-align: center;'>📊 Inteligencia Ambiental Industrial: DANE EAS</h1>", unsafe_allow_html=True)

# Descripción centrada
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Este Dashboard transforma microdatos complejos en indicadores visuales estratégicos para entender la sostenibilidad industrial en Colombia.</p>", unsafe_allow_html=True)

st.divider()

# --- SECCIÓN CENTRAL: ¿CÓMO EMPEZAR? ---
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    st.markdown("<h2 style='text-align: center;'>🚀 ¿Cómo empezar?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>👈 Seleccione una página en el menú lateral para comenzar.</p>", unsafe_allow_html=True)