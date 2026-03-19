import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from pathlib import Path

# 1. CONFIGURACIÓN DE RUTAS
script_path = Path(__file__).resolve()
proyecto_raiz = script_path.parent.parent
# Apuntamos directamente a procesados donde están tus archivos
ruta_data = proyecto_raiz / "data" / "procesados"

print(f"--- INICIANDO PROCESO DE CARGA ---")

# 2. CARGAR VARIABLES DE ENTORNO
load_dotenv(proyecto_raiz / ".env")

def conectar_db():
    try:
        url_object = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME"),
        )
        engine = create_engine(url_object)
        return engine
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def ejecutar_carga():
    if not ruta_data.exists():
        print(f"❌ ERROR: No existe la ruta {ruta_data}")
        return

    engine = conectar_db()
    if not engine: return

    archivos_procesados = 0
    
    # Buscamos archivos .csv
    for archivo_path in ruta_data.glob("*.csv"):
        print(f"🚀 Procesando: {archivo_path.name}...")
        
        try:
            df = pd.read_csv(archivo_path)
            
            if df.empty:
                continue

            # INSERTAR EN LA BASE DE DATOS
            # Usamos 'append' para acumular 2022, 2023, etc.
            df.to_sql('indicadores_ambientales', con=engine, if_exists='append', index=False)
            
            print(f"✅ {archivo_path.name} -> {len(df)} filas insertadas.")
            archivos_procesados += 1
            
        except Exception as e:
            print(f"❌ Error con {archivo_path.name}: {e}")

    if archivos_procesados > 0:
        print(f"\n✨ ¡ÉXITO! Datos cargados correctamente.")
    else:
        print("\n🔎 No se encontraron archivos para procesar.")

if __name__ == "__main__":
    ejecutar_carga()