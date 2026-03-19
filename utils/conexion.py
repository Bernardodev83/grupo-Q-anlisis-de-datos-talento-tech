import os
import streamlit as st
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
from pathlib import Path

# Localizar el .env en la raíz
ruta_raiz = Path(__file__).resolve().parent.parent
load_dotenv(ruta_raiz / ".env")

@st.cache_resource
def obtener_conexion():
    """Conexión centralizada y segura a MariaDB."""
    try:
        url_object = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME"),
        )
        # pool_recycle evita que la conexión se caiga por inactividad
        return create_engine(url_object, pool_recycle=3600, pool_pre_ping=True)
    except Exception as e:
        st.error(f"❌ Error de Conexión: {e}")
        return None