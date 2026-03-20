import mysql.connector
import os
from dotenv import load_dotenv

# 1. Localizamos las rutas subiendo un nivel (..) desde la carpeta utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
CA_PATH = os.path.join(BASE_DIR, 'ca.pem')

# 2. Cargamos las variables de entorno
load_dotenv(ENV_PATH)

def get_connection():
    """Establece la conexión con la base de datos MySQL en Aiven."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_ca=CA_PATH,
            ssl_verify_cert=True
        )
        return conn
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")
        return None

# Prueba de funcionamiento autónoma
if __name__ == "__main__":
    conexion = get_connection()
    if conexion:
        print("✅ ¡CONEXIÓN EXITOSA! El puente hacia Aiven está activo.")
        conexion.close()
    else:
        print("❌ No se pudo conectar. Revisa el archivo .env y el ca.pem.")