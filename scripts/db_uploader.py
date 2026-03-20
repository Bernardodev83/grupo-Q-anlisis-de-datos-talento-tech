import pandas as pd
import os
import sys
from pathlib import Path

# --- LOCALIZACIÓN DE LA RAÍZ ---
ruta_raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta_raiz))

try:
    from utils.conexion import get_connection
    print("✅ Conexión con Aiven preparada.")
except ImportError:
    print("❌ No se encontró utils/conexion.py")
    sys.exit(1)

def subir_datos_csv():
    ruta_procesados = os.path.join(ruta_raiz, 'data', 'procesados')
    archivos = [
        'datos_2019_final.csv', 'datos_2020_final.csv', 
        'datos_2021_final.csv', 'datos_2022_final.csv', 
        'datos_2023_final.csv'
    ]
    
    conn = get_connection()
    if not conn: return

    cursor = conn.cursor()
    
    try:
        for archivo in archivos:
            ruta_full = os.path.join(ruta_procesados, archivo)
            
            if os.path.exists(ruta_full):
                print(f"⏳ Procesando {archivo}...")
                df = pd.read_csv(ruta_full).fillna(0)
                
                print(f"🚀 Subiendo {len(df)} filas...")
                
                # Ajustamos el INSERT para que use los nombres exactos de tus columnas
                query = """
                INSERT INTO indicadores_ambientales 
                (periodo, seccion_economica, consumo_energia_kwh, gasto_gestion_amb, ahorro_agua_m3)
                VALUES (%s, %s, %s, %s, %s)
                """
                
                for _, row in df.iterrows():
                    # MAPEANDO TUS COLUMNAS REALES:
                    valores = (
                        row['periodo'], 
                        row['seccion_economica'], 
                        row['consumo_energia_kwh'],
                        row['gasto_gestion_amb'],
                        row['consumo_agua_m3']  # <-- Aquí estaba el error, ya está corregido
                    )
                    cursor.execute(query, valores)
                
                conn.commit()
                print(f"✅ {archivo} guardado con éxito.")
            else:
                print(f"⚠️ No se encontró: {archivo}")

        print("\n🏆 ¡DATOS CARGADOS! Bernardo, el DANE ya está en tu nube.")

    except Exception as e:
        print(f"❌ Error durante la subida: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals(): cursor.close()
        conn.close()
        print("🔌 Conexión cerrada.")

if __name__ == "__main__":
    subir_datos_csv()