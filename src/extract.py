import os
import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Lee la fuente de datos en su estado puro (Raw Data) asegurando 
    la preservación del archivo original y documentando su adquisición.
    """
    # 1. Verificación de existencia del archivo original inalterado (Preserve raw data)
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"❌ ERROR CRÍTICO EN EXTRACTION: No se encontró el dataset crudo en: {file_path}\n"
            "Asegúrate de que el archivo 'Registro_Nacional_de_Turismo_-_RNT_20260915.csv' esté en 'data/raw/'."
        )
    
    # 2. Documentación y lectura del archivo sin transformaciones de negocio
    print(f"[EXTRACT] Adquiriendo dataset crudo desde: {file_path}")
    
    # Se utiliza low_memory=False únicamente para asegurar lectura continua por el volumen de filas,
    # manteniendo los datos exactamente como están en la fuente original.
    raw_df = pd.read_csv(file_path, low_memory=False)
    
    # 3. Registro y verificación básica de adquisición
    print(f"[EXTRACT] Documentación de Adquisición:")
    print(f"  - Filas leídas (Raw): {len(raw_df):,}")
    print(f"  - Columnas leídas (Raw): {len(raw_df.columns)}")
    print("✔ [EXTRACT] Extracción pura finalizada sin transformaciones aplicadas.\n")
    
    return raw_df

if __name__ == "__main__":
    # Prueba de ejecución individual de la capa de Extracción
    RAW_FILE_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    extracted_df = extract_data(RAW_FILE_PATH)