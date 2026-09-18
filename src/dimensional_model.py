import pandas as pd
import numpy as np

def build_dimensional_model(df_clean: pd.DataFrame) -> dict:
    """
    Construye las tablas del modelo dimensional a partir del dataset limpio.
    Garantiza la asignación de PKs, Surrogate Keys y FKs relacionales.
    """
    print("[TRANSFORM - DIMENSIONAL] Generando dimensiones y tabla de hechos...")

    # ------------------------------------------------------------------
    # 1. DIMENSIÓN UBICACIÓN (dim_ubicacion)
    # PK Natural: codigo_municipio (DIVIPOLA)
    # ------------------------------------------------------------------
    dim_ubicacion = df_clean[
        ['CODIGO_MUNICIPIO', 'MUNICIPIO', 'CODIGO_DEPARTAMENTO', 'DEPARTAMENTO']
    ].drop_duplicates(subset=['CODIGO_MUNICIPIO']).copy()
    
    dim_ubicacion.rename(columns={
        'CODIGO_MUNICIPIO': 'codigo_municipio',
        'MUNICIPIO': 'municipio',
        'CODIGO_DEPARTAMENTO': 'codigo_departamento',
        'DEPARTAMENTO': 'departamento'
    }, inplace=True)
    
    # ------------------------------------------------------------------
    # 2. DIMENSIÓN CATEGORÍA (dim_categoria)
    # PK Subrogada (Surrogate Key): id_categoria
    # ------------------------------------------------------------------
    dim_categoria = df_clean[
        ['CATEGORIA', 'SUB_CATEGORIA']
    ].drop_duplicates().reset_index(drop=True).copy()
    
    # Creación explícita de Surrogate Key
    dim_categoria['id_categoria'] = dim_categoria.index + 1
    
    dim_categoria.rename(columns={
        'CATEGORIA': 'categoria',
        'SUB_CATEGORIA': 'sub_categoria'
    }, inplace=True)
    
    # Reordenar columnas para dejar la PK al inicio
    dim_categoria = dim_categoria[['id_categoria', 'categoria', 'sub_categoria']]

    # ------------------------------------------------------------------
    # 3. DIMENSIÓN PRESTADOR (dim_prestador)
    # PK Natural: codigo_rnt
    # ------------------------------------------------------------------
    dim_prestador = df_clean[
        ['CODIGO_RNT', 'RAZON_SOCIAL_ESTABLECIMIENTO', 'NIT', 'ESTADO_RNT']
    ].drop_duplicates(subset=['CODIGO_RNT']).copy()
    
    dim_prestador.rename(columns={
        'CODIGO_RNT': 'codigo_rnt',
        'RAZON_SOCIAL_ESTABLECIMIENTO': 'razon_social',
        'NIT': 'nit',
        'ESTADO_RNT': 'estado_rnt'
    }, inplace=True)

    # ------------------------------------------------------------------
    # 4. DIMENSIÓN TIEMPO (dim_tiempo)
    # PK Natural: anio
    # ------------------------------------------------------------------
    dim_tiempo = pd.DataFrame({
        'anio': sorted(df_clean['AÑO'].unique())
    })

    # ------------------------------------------------------------------
    # 5. TABLA DE HECHOS (fact_turismo_anual)
    # PK Subrogada: id_fact | FKs: codigo_rnt, codigo_municipio, id_categoria, anio
    # ------------------------------------------------------------------
    fact = df_clean.copy()
    
    # Mapeo de Surrogate Key de Categoría
    fact = fact.merge(
        dim_categoria,
        left_on=['CATEGORIA', 'SUB_CATEGORIA'],
        right_on=['categoria', 'sub_categoria'],
        how='left'
    )
    
    # Selección y renombrado de columnas para la Fact Table
    fact_turismo_anual = pd.DataFrame({
        'id_fact': np.arange(1, len(fact) + 1),
        'codigo_rnt': fact['CODIGO_RNT'],
        'codigo_municipio': fact['CODIGO_MUNICIPIO'],
        'id_categoria': fact['id_categoria'],
        'anio': fact['AÑO'],
        'numero_de_habitaciones': fact['NUMERO_DE_HABITACIONES'],
        'numero_de_camas': fact['NUMERO_DE_CAMAS'],
        'numero_de_empleados': fact['NUMERO_DE_EMPLEADOS']
    })

    print(f"  - Dimensión Ubicación: {len(dim_ubicacion):,} municipios únicos (PK garantizada).")
    print(f"  - Dimensión Categoría: {len(dim_categoria):,} miembros únicos con Surrogate Key.")
    print(f"  - Dimensión Prestador: {len(dim_prestador):,} miembros únicos.")
    print(f"  - Dimensión Tiempo: {len(dim_tiempo):,} miembros únicos.")
    print(f"  - Tabla de Hechos (Fact): {len(fact_turismo_anual):,} registros a grano atómico.")
    print("✔ [TRANSFORM - DIMENSIONAL] Modelo dimensional generado exitosamente.\n")

    return {
        'dim_ubicacion': dim_ubicacion,
        'dim_categoria': dim_categoria,
        'dim_prestador': dim_prestador,
        'dim_tiempo': dim_tiempo,
        'fact_turismo_anual': fact_turismo_anual
    }

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data_preparation

    RAW_FILE_PATH = "data/raw/Registro_Nacional_de_Turismo_-_RNT_20260915.csv"
    raw_df = extract_data(RAW_FILE_PATH)
    clean_df = transform_data_preparation(raw_df)
    tables = build_dimensional_model(clean_df)