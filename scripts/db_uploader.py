import pandas as pd
import sys
from pathlib import Path

# Configurar rutas para que encuentre 'utils'
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

from utils.conexion import obtener_conexion

def ejecutar_carga():
    engine = obtener_conexion()
    if not engine: return

    folder_proc = ruta_raiz / "data" / "procesados"
    archivos = list(folder_proc.glob("*.csv"))

    if not archivos:
        print(f"❌ No hay archivos en {folder_proc}")
        return

    # Usamos el primer CSV que encuentre el limpiador
    ruta_csv = archivos[0]
    print(f"📖 Procesando: {ruta_csv.name}")

    try:
        df = pd.read_csv(ruta_csv)
        # Limpiar nombres de columnas para SQL (quitar espacios)
        df.columns = [c.replace(' ', '_').lower() for c in df.columns]
        
        # Carga masiva
        df.to_sql('indicadores_ambientales', con=engine, if_exists='replace', index=False, chunksize=500)
        print(f"✅ ¡ÉXITO! {len(df)} filas cargadas en MariaDB.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_carga()