import os
import pandas as pd

def transform_data_preparation(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta la preparacion y limpieza estandarizada de datos.
    """
    print("[TRANSFORM - DATA PREPARATION] Iniciando limpieza y estandarización...")
    df = raw_df.copy()

    # 1. Clean and standardize: Imputación de nulos
    nulls_before = df['RAZON_SOCIAL_ESTABLECIMIENTO'].isnull().sum()
    df['RAZON_SOCIAL_ESTABLECIMIENTO'] = df['RAZON_SOCIAL_ESTABLECIMIENTO'].fillna('NO REGISTRA')
    print(f"  - Clean: Imputados {nulls_before} valores nulos en RAZON_SOCIAL_ESTABLECIMIENTO.")

    # 2. Prepare categories and text identifiers: Normalización de cadenas
    text_cols = [
        'RAZON_SOCIAL_ESTABLECIMIENTO', 'DEPARTAMENTO', 
        'MUNICIPIO', 'CATEGORIA', 'SUB_CATEGORIA', 'ESTADO_RNT'
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
    print("  - Standardize: Cadenas de texto normalizadas (UPPERCASE y STRIP).")

    # 3. Correct data types: Conversión explícita a enteros
    int_cols = [
        'NUMERO_DE_HABITACIONES', 'NUMERO_DE_CAMAS', 'NUMERO_DE_EMPLEADOS', 
        'CODIGO_RNT', 'AÑO', 'CODIGO_MUNICIPIO', 'CODIGO_DEPARTAMENTO'
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')
    print("  - Correct Data Types: Tipos numéricos e identificadores casteados a int64.")

    print("✔ [TRANSFORM - DATA PREPARATION] Preparación de datos finalizada exitosamente.\n")
    return df

def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """Guarda el archivo procesado en data/processed/"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✔ Dataset procesado guardado en: {output_path}\n")

if __name__ == "__main__":
    from extract import extract_data
    RAW_FILE_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    PROCESSED_FILE_PATH = "data/processed/Registro_Turismo_Procesado.csv"
    
    raw_data = extract_data(RAW_FILE_PATH)
    clean_data = transform_data_preparation(raw_data)
    save_processed_data(clean_data, PROCESSED_FILE_PATH)