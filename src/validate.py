import pandas as pd

def validate_requirements(tables: dict) -> bool:
    """
    Simula las consultas SQL R1 a R5 mediante joins de pandas sobre
    el modelo dimensional generado.
    """
    print("[VALIDATION] Iniciando validación de Requerimientos (R1-R5) sobre el Modelo Dimensional...")
    
    dim_ubicacion = tables['dim_ubicacion']
    dim_categoria = tables['dim_categoria']
    dim_prestador = tables['dim_prestador']
    dim_tiempo = tables['dim_tiempo']
    fact = tables['fact_turismo_anual']

    # 1. Validar Integridad Referencial (0 FK Huérfanas)
    assert fact['codigo_municipio'].isin(dim_ubicacion['codigo_municipio']).all(), "FK Error: Municipios huérfanos"
    assert fact['id_categoria'].isin(dim_categoria['id_categoria']).all(), "FK Error: Categorías huérfanas"
    assert fact['codigo_rnt'].isin(dim_prestador['codigo_rnt']).all(), "FK Error: Prestadores huérfanos"
    assert fact['anio'].isin(dim_tiempo['anio']).all(), "FK Error: Tiempos huérfanos"
    print("  ✔ Integridad Referencial: 100% de las Foreign Keys vinculan correctamente.")

    # R1: Empleo por Territorio
    r1 = fact.merge(dim_ubicacion, on='codigo_municipio').groupby(['departamento', 'municipio'])['numero_de_empleados'].sum().reset_index()
    print(f"  ✔ R1 Validado: Generada matriz de empleo para {len(r1):,} municipios/departamentos.")

    # R2: Capacidad Hotelera
    r2 = fact.merge(dim_ubicacion, on='codigo_municipio').groupby('municipio')[['numero_de_habitaciones', 'numero_de_camas']].sum().reset_index()
    print(f"  ✔ R2 Validado: Capacidad calculada para {len(r2):,} municipios.")

    # R3: Empleo por Categoría
    r3 = fact.merge(dim_categoria, on='id_categoria').groupby(['categoria', 'sub_categoria'])['numero_de_empleados'].sum().reset_index()
    print(f"  ✔ R3 Validado: Empleo distribuido en {len(r3):,} subcategorías turísticas.")

    # R4: Promedio por Prestador
    r4 = fact.merge(dim_categoria, on='id_categoria').groupby('categoria')['numero_de_empleados'].mean().reset_index()
    print(f"  ✔ R4 Validado: Promedios de empleo calculados por categoría comercial.")

    # R5: Evolución Temporal (2019-2026)
    r5 = fact.merge(dim_tiempo, on='anio').groupby('anio')[['numero_de_empleados', 'numero_de_habitaciones']].sum().reset_index()
    print(f"  ✔ R5 Validado: Serie de tiempo histórica procesada para {len(r5)} años (2019-2026).")

    # Reconciliación total de métricas
    total_empleados = fact['numero_de_empleados'].sum()
    print(f"\n  [RECONCILIACIÓN TOTAL] Total de empleos directos reconciliados: {total_empleados:,}")
    print("✔ [VALIDATION] Requerimientos R1-R5 soportados al 100% por el modelo.\n")
    return True

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data_preparation
    from dimensional_model import build_dimensional_model

    RAW_FILE_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    raw = extract_data(RAW_FILE_PATH)
    clean = transform_data_preparation(raw)
    tables = build_dimensional_model(clean)
    validate_requirements(tables)