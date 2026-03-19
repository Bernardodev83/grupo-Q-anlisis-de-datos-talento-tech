import sys
import os
from pathlib import Path

# --- ESTO ES LO QUE SOLUCIONA EL ERROR ---
# Obtenemos la ruta de la carpeta raíz (proyecto ambiental DANE)
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))
# -----------------------------------------

try:
    from utils.conexion import obtener_conexion
    from sqlalchemy import text
    print("✅ Módulo 'utils' detectado correctamente.")
except ImportError as e:
    print(f"❌ Error al importar: {e}")
    sys.exit(1)

def crear_estructura_tablas():
    engine = obtener_conexion()
    if not engine:
        print("❌ No se pudo obtener la conexión.")
        return

    # Definición de la tabla (Ajustada a tus requerimientos)
    query_crear_tabla = """
    CREATE TABLE IF NOT EXISTS indicadores_ambientales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        periodo INT NOT NULL,
        seccion_economica VARCHAR(255) NOT NULL,
        consumo_energia_kwh DECIMAL(15, 2),
        gasto_gestion_amb DECIMAL(15, 2),
        ahorro_agua_m3 DECIMAL(15, 2),
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    try:
        with engine.connect() as con:
            # SQLAlchemy 2.0 requiere que las ejecuciones de texto sean explícitas
            con.execute(text(query_crear_tabla))
            # Importante: algunas versiones requieren con.commit() si no es autocommit
            print("✅ Estructura de MariaDB verificada/creada exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear la tabla: {e}")

if __name__ == "__main__":
    crear_estructura_tablas()