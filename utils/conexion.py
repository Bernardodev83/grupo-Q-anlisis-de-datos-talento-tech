import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st

# Cargar variables de entorno
load_dotenv()

def obtener_conexion():
    try:
        # Usamos .get() y definimos un puerto por defecto (3306) para que no sea 'None'
        user = st.secrets.get("DB_USER")
        password = st.secrets.get("DB_PASSWORD")
        host = st.secrets.get("DB_HOST")
        port = st.secrets.get("DB_PORT", "3306") # Si no existe, usa 3306
        database = st.secrets.get("DB_NAME")

        # Verificamos que los datos esenciales existan
        if not all([user, password, host, database]):
            st.warning("⚠️ Faltan credenciales en los Secrets de Streamlit.")
            return None

        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)
        return engine
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None