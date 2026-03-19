import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import streamlit as st

# Cargar variables de entorno
load_dotenv()

def obtener_conexion():
    """Establece la conexión con la base de datos."""
    try:
        # Intenta sacar las credenciales de los Secrets de Streamlit (para la nube)
        # O de las variables de entorno (para local)
        user = st.secrets.get("DB_USER") or os.getenv("DB_USER")
        password = st.secrets.get("DB_PASSWORD") or os.getenv("DB_PASSWORD")
        host = st.secrets.get("DB_HOST") or os.getenv("DB_HOST")
        port = st.secrets.get("DB_PORT") or os.getenv("DB_PORT")
        database = st.secrets.get("DB_NAME") or os.getenv("DB_NAME")

        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)
        return engine
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None