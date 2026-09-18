import pandas as pd
from sqlalchemy import create_engine, text

def run_analytical_queries(db_user: str = "root", db_pass: str = "ADsemestre2025", db_host: str = "localhost", db_port: str = "3306"):
    """
    Conecta a MySQL DW y ejecuta las 5 consultas analíticas obligatorias.
    """
    print("[ANALYTICAL QUERIES] Conectando a MySQL dw_turismo_ods8...")
    db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/dw_turismo_ods8"
    engine = create_engine(db_url)

    queries = {
        "R1": {
            "title": "R1: Empleo por Territorio (Top 5 Departamentos con mayor empleo formal turistico)",
            "kpi": "Total Empleos Turísticos por Departamento",
            "tables": "fact_turismo_anual, dim_ubicacion",
            "sql": """
                SELECT 
                    u.departamento,
                    COUNT(DISTINCT u.codigo_municipio) AS municipios_cobertura,
                    SUM(f.numero_de_empleados) AS total_empleos
                FROM fact_turismo_anual f
                JOIN dim_ubicacion u ON f.codigo_municipio = u.codigo_municipio
                GROUP BY u.departamento
                ORDER BY total_empleos DESC
                LIMIT 5;
            """
        },
        "R2": {
            "title": "R2: Capacidad Hotelera (Top 5 Municipios con mayor oferta de Hospedaje)",
            "kpi": "Promedio de Camas por Habitación & Oferta Total",
            "tables": "fact_turismo_anual, dim_ubicacion",
            "sql": """
                SELECT 
                    u.municipio,
                    u.departamento,
                    SUM(f.numero_de_habitaciones) AS total_habitaciones,
                    SUM(f.numero_de_camas) AS total_camas,
                    ROUND(SUM(f.numero_de_camas) / NULLIF(SUM(f.numero_de_habitaciones), 0), 2) AS promedio_camas_por_habitacion
                FROM fact_turismo_anual f
                JOIN dim_ubicacion u ON f.codigo_municipio = u.codigo_municipio
                GROUP BY u.codigo_municipio, u.municipio, u.departamento
                HAVING total_habitaciones > 0
                ORDER BY total_habitaciones DESC
                LIMIT 5;
            """
        },
        "R3": {
            "title": "R3: Empleo por Categoria Turistica (Participacion relativa de empleo)",
            "kpi": "Generación de Empleo Directo por Categoría Comercial",
            "tables": "fact_turismo_anual, dim_categoria",
            "sql": """
                SELECT 
                    c.categoria,
                    COUNT(DISTINCT c.sub_categoria) AS subcategorias_asociadas,
                    SUM(f.numero_de_empleados) AS total_empleados,
                    ROUND((SUM(f.numero_de_empleados) * 100.0) / (SELECT SUM(numero_de_empleados) FROM fact_turismo_anual), 2) AS porcentaje_participacion
                FROM fact_turismo_anual f
                JOIN dim_categoria c ON f.id_categoria = c.id_categoria
                GROUP BY c.categoria
                ORDER BY total_empleados DESC;
            """
        },
        "R4": {
            "title": "R4: Promedio por Prestador de Servicios Turisticos (PST)",
            "kpi": "Densidad Promedio de Empleo por Establecimiento",
            "tables": "fact_turismo_anual, dim_categoria",
            "sql": """
                SELECT 
                    c.categoria,
                    COUNT(DISTINCT f.codigo_rnt) AS total_pst_registrados,
                    SUM(f.numero_de_empleados) AS total_empleos,
                    ROUND(AVG(f.numero_de_empleados), 2) AS promedio_empleados_por_pst
                FROM fact_turismo_anual f
                JOIN dim_categoria c ON f.id_categoria = c.id_categoria
                GROUP BY c.categoria
                ORDER BY promedio_empleados_por_pst DESC;
            """
        },
        "R5": {
            "title": "R5: Evolucion Temporal y Tendencia Historica (2019-2026)",
            "kpi": "Tasa de Crecimiento Anual de Empleo y Capacidad",
            "tables": "fact_turismo_anual, dim_tiempo",
            "sql": """
                SELECT 
                    t.anio,
                    COUNT(f.id_fact) AS total_registros_anuales,
                    SUM(f.numero_de_empleados) AS empleo_anual,
                    SUM(f.numero_de_habitaciones) AS habitaciones_anuales,
                    SUM(f.numero_de_camas) AS camas_anuales
                FROM fact_turismo_anual f
                JOIN dim_tiempo t ON f.anio = t.anio
                GROUP BY t.anio
                ORDER BY t.anio ASC;
            """
        }
    }

    results_summary = {}

    with engine.connect() as conn:
        for r_code, q in queries.items():
            print(f"\n====================================================")
            print(f"📊 EJECUTANDO {q['title']}")
            print(f"====================================================")
            df_res = pd.read_sql_query(text(q['sql']), conn)
            print(df_res.to_string(index=False))
            results_summary[r_code] = df_res

    print("\n✔ [ANALYTICAL QUERIES] Consultas SQL ejecutadas exitosamente sobre MySQL DW.\n")
    return results_summary

if __name__ == "__main__":
    run_analytical_queries()