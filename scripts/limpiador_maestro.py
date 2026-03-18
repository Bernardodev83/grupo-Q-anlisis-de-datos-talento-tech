import pandas as pd
import os

def limpiador_maestro_final():
    # Variables que queremos en el archivo final
    variables_objetivo = [
        'periodo', 'id_empresa', 'seccion_economica', 'actividad_nombre',
        'gastos_totales', 'gasto_gestion_amb', 'consumo_agua_m3', 'consumo_energia_kwh'
    ]

    print("🚀 Iniciando Limpieza Maestra con Rescate de Datos (2019-2021)...")

    for anio in [2019, 2020, 2021, 2022, 2023]:
        ruta = f"datos/originales/EAS_{anio}.xlsx"
        
        if os.path.exists(ruta):
            print(f"⏳ Procesando año {anio}...")
            df_ori = pd.read_excel(ruta)
            df_final = pd.DataFrame()

            # --- 1. IDENTIFICACIÓN DE COLUMNAS BÁSICAS ---
            df_final['periodo'] = [anio] * len(df_ori)
            
            # ID Empresa
            for c in ['idnoremp', 'id_empresa', 'idnorempan']:
                if c in df_ori.columns:
                    df_final['id_empresa'] = df_ori[c]
                    break
            
            # Sección Económica (Sectores)
            for c in ['SECTOR_DESC', 'seccion_desc', 'SECCION_DESC', 'SECCION']:
                if c in df_ori.columns:
                    df_final['seccion_economica'] = df_ori[c].astype(str).str.title()
                    break

            # Gastos Totales e Inversión Ambiental
            for c in ['gastos_tot', 'gastos_totales']:
                if c in df_ori.columns:
                    df_final['gastos_totales'] = pd.to_numeric(df_ori[c], errors='coerce').fillna(0)
                    break
            
            for c in ['GASPROGESAMB', 'gasto_gestion_amb']:
                if c in df_ori.columns:
                    df_final['gasto_gestion_amb'] = pd.to_numeric(df_ori[c], errors='coerce').fillna(0)
                    break

            # --- 2. LÓGICA DE RESCATE PARA AGUA Y ENERGÍA ---
            if anio == 2023:
                # 2023 usa nombres directos
                if 'FUEN_AG_TOT' in df_ori.columns:
                    df_final['consumo_agua_m3'] = pd.to_numeric(df_ori['FUEN_AG_TOT'], errors='coerce').fillna(0)
                if 'WTOTECONSUM' in df_ori.columns:
                    df_final['consumo_energia_kwh'] = pd.to_numeric(df_ori['WTOTECONSUM'], errors='coerce').fillna(0)
            
            elif anio in [2020, 2022]:
                # 2020/2022 usan nombres descriptivos de inversión
                if 'gasto_ahorro_agua' in df_ori.columns:
                    df_final['consumo_agua_m3'] = pd.to_numeric(df_ori['gasto_ahorro_agua'], errors='coerce').fillna(0)
                if 'gasto_energia_limp' in df_ori.columns:
                    df_final['consumo_energia_kwh'] = pd.to_numeric(df_ori['gasto_energia_limp'], errors='coerce').fillna(0)
            
            elif anio in [2019, 2021]:
                # 2019/2021 usan códigos ACTGAST (2=Agua, 7=Energía)
                if 'ACTGAST2' in df_ori.columns:
                    df_final['consumo_agua_m3'] = pd.to_numeric(df_ori['ACTGAST2'], errors='coerce').fillna(0)
                if 'ACTGAST7' in df_ori.columns:
                    df_final['consumo_energia_kwh'] = pd.to_numeric(df_ori['ACTGAST7'], errors='coerce').fillna(0)

            # Rellenar cualquier columna faltante con 0
            for col in variables_objetivo:
                if col not in df_final.columns:
                    df_final[col] = 0

            # --- 3. GUARDADO ---
            os.makedirs("datos/procesados", exist_ok=True)
            df_final.to_csv(f"datos/procesados/datos_{anio}_final.csv", index=False)
            print(f"✅ Año {anio} procesado con éxito.")
        else:
            print(f"❌ No se encontró el archivo: {ruta}")

# --- se debe copiar el limpiador_maestro.py en la carpeta raiz ---
if __name__ == "__main__":
    limpiador_maestro_final()