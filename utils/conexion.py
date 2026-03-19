import streamlit as st
from sqlalchemy import create_engine
import os

def obtener_conexion():
    """Conexión robusta para Talento Tech"""
    try:
        # 1. Intentar leer de Secrets (Streamlit Cloud) o Variables de Entorno (Local)
        user = st.secrets.get("DB_USER") or os.getenv("DB_USER")
        password = st.secrets.get("DB_PASSWORD") or os.getenv("DB_PASSWORD")
        host = st.secrets.get("DB_HOST") or os.getenv("DB_HOST")
        port = st.secrets.get("DB_PORT") or os.getenv("DB_PORT")
        database = st.secrets.get("DB_NAME") or os.getenv("DB_NAME")

        # 2. VALIDACIÓN CRÍTICA: Si algo es None, poner valores por defecto o avisar
        if not all([user, password, host, database]):
            st.warning("⚠️ Configuración incompleta. Revisa los Secrets en Streamlit Cloud.")
            return None
        
        # Forzar el puerto a ser un entero, si falla usa 3306
        try:
            port_int = int(port)
        except (ValueError, TypeError):
            port_int = 3306

        # 3. CREAR EL ENGINE
        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port_int}/{database}"
        engine = create_engine(url)
        return engine

    except Exception as e:
        st.error(f"❌ Error crítico de conexión: {e}")
        return None