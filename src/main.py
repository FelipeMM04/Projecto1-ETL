import sys
import os

# Garantizar la resolución de importaciones dentro de src/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract_data
from transform import transform_data_preparation, save_processed_data
from dimensional_model import build_dimensional_model
from validate import validate_requirements
from load import load_to_mysql

def run_etl_pipeline():
    print("\n========================================================")
    print("🚀 INICIANDO EJECUCIÓN DEL PIPELINE ETL COMPLETO (ODS 8)")
    print("========================================================\n")
    
    RAW_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    PROCESSED_PATH = "data/processed/Registro_Turismo_Procesado.csv"
    
    # 1. EXTRACT
    print("--- ETAPA 1: EXTRACTION ---")
    raw_df = extract_data(RAW_PATH)
    
    # 2. TRANSFORM - DATA PREPARATION
    print("--- ETAPA 2: TRANSFORM (DATA PREPARATION) ---")
    clean_df = transform_data_preparation(raw_df)
    save_processed_data(clean_df, PROCESSED_PATH)
    
    # 3. TRANSFORM - DIMENSIONAL TRANSFORMATION
    print("--- ETAPA 3: TRANSFORM (DIMENSIONAL TRANSFORMATION) ---")
    model_tables = build_dimensional_model(clean_df)
    
    # 4. VALIDATE
    print("--- ETAPA 4: VALIDATE ---")
    is_valid = validate_requirements(model_tables)
    if not is_valid:
        print("❌ El pipeline se detuvo por fallas de validación.")
        return
        
    # 5. LOAD (PERSISTENCIA EN MYSQL)
    print("--- ETAPA 5: LOAD (MYSQL DATA WAREHOUSE) ---")
    load_to_mysql(model_tables, db_user="root", db_pass="ADsemestre2025")
    
    print("========================================================")
    print("✔ PIPELINE ETL EJECUTADO Y PERSISTIDO CON ÉXITO AL 100%")
    print("========================================================\n")

if __name__ == "__main__":
    run_etl_pipeline()