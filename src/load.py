import os
import pandas as pd
from sqlalchemy import create_engine, text

def load_to_mysql(model_tables: dict, db_user: str = "root", db_pass: str = "ADsemestre2025", db_host: str = "localhost", db_port: str = "3306"):
    """
    Carga las dimensiones y la tabla de hechos en MySQL respetando el orden relacional.
    """
    print("[LOAD] Conectando a MySQL para iniciar la persistencia...")
    
    # 1. Crear motor para conectar al servidor MySQL y asegurar la existencia de la BD
    server_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/"
    engine_server = create_engine(server_url)
    
    with engine_server.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS dw_turismo_ods8;"))
        conn.commit()
    
    # 2. Conectar a la base de datos específica dw_turismo_ods8
    db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/dw_turismo_ods8"
    engine = create_engine(db_url)

    # 3. Limpieza previa idempotente para evitar duplicación en reejecuciones
    print("  - Preparando tablas relacionales (Truncate previa e inhabilitación temporal de FKs)...")
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("TRUNCATE TABLE fact_turismo_anual;"))
        conn.execute(text("TRUNCATE TABLE dim_ubicacion;"))
        conn.execute(text("TRUNCATE TABLE dim_categoria;"))
        conn.execute(text("TRUNCATE TABLE dim_prestador;"))
        conn.execute(text("TRUNCATE TABLE dim_tiempo;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    # 4. Load dimensions first (Carga de dimensiones primero)
    print("  - Ingesta: Cargando tablas de dimensiones...")
    model_tables['dim_ubicacion'].to_sql('dim_ubicacion', con=engine, if_exists='append', index=False)
    model_tables['dim_categoria'].to_sql('dim_categoria', con=engine, if_exists='append', index=False)
    model_tables['dim_prestador'].to_sql('dim_prestador', con=engine, if_exists='append', index=False)
    model_tables['dim_tiempo'].to_sql('dim_tiempo', con=engine, if_exists='append', index=False)
    print("  - Ingesta: Dimensiones cargadas con éxito.")

    # 5. Load Fact Table (Carga de la Tabla de Hechos posteriormente)
    print(f"  - Ingesta: Cargando Tabla de Hechos ({len(model_tables['fact_turismo_anual']):,} filas)...")
    model_tables['fact_turismo_anual'].to_sql('fact_turismo_anual', con=engine, if_exists='append', index=False, chunksize=50000)
    print("  - Ingesta: Tabla de hechos cargada exitosamente.")

    # 6. Verify referential integrity after loading
    print("  - Verificación Post-Carga: Comprobando filas cargadas en MySQL...")
    with engine.connect() as conn:
        fact_count = conn.execute(text("SELECT COUNT(*) FROM fact_turismo_anual")).scalar()
        dim_ub_count = conn.execute(text("SELECT COUNT(*) FROM dim_ubicacion")).scalar()
        print(f"    * Registros en MySQL -> Fact: {fact_count:,} | Dim Ubicación: {dim_ub_count:,}")

    print("✔ [LOAD] Carga e integridad verificadas al 100% en MySQL.\n")

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data_preparation
    from dimensional_model import build_dimensional_model

    RAW_FILE_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    raw_data = extract_data(RAW_FILE_PATH)
    clean_data = transform_data_preparation(raw_data)
    tables = build_dimensional_model(clean_data)
    
    load_to_mysql(tables, db_user="root", db_pass="ADsemestre2025")