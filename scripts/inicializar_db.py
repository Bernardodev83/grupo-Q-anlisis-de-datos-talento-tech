import sys
import os
from pathlib import Path

# --- LOCALIZACIÓN DE LA RAÍZ ---
# Esto permite que el script encuentre la carpeta 'utils'
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

try:
    # Importamos la nueva función 'get_connection' que creamos en el Paso 1
    from utils.conexion import get_connection
    print("✅ Módulo 'utils' y función 'get_connection' detectados.")
except ImportError as e:
    print(f"❌ Error al importar: {e}")
    sys.exit(1)

def crear_estructura_tablas():
    # Obtenemos la conexión directa de mysql-connector
    conn = get_connection()
    
    if not conn:
        print("❌ No se pudo establecer la conexión con Aiven.")
        return

    # Definición de la tabla principal
    # Mantenemos tus columnas: periodo, seccion, energia, gasto y agua
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
        cursor = conn.cursor()
        print("⏳ Verificando estructura en la nube de Aiven...")
        
        # Ejecutamos la creación
        cursor.execute(query_crear_tabla)
        
        # En MySQL es buena práctica asegurar el commit
        conn.commit()
        
        print("✅ ¡Estructura de la base de datos creada exitosamente en Aiven!")
        
    except Exception as e:
        print(f"❌ Error al crear la tabla: {e}")
    finally:
        # Cerramos siempre el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        conn.close()
        print("🔌 Conexión cerrada.")

if __name__ == "__main__":
    crear_estructura_tablas()