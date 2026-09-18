-- R1: Generación de empleo por departamento (Top 10)
SELECT 
    u.departamento,
    SUM(f.numero_de_empleados) AS total_empleados
FROM fact_turismo_anual f
JOIN dim_ubicacion u ON f.codigo_municipio = u.codigo_municipio
GROUP BY u.departamento
ORDER BY total_empleados DESC
LIMIT 10;

-- R2: Capacidad hotelera instalada por municipio (Top 10)
SELECT 
    u.municipio,
    u.departamento,
    SUM(f.numero_de_habitaciones) AS total_habitaciones,
    SUM(f.numero_de_camas) AS total_camas
FROM fact_turismo_anual f
JOIN dim_ubicacion u ON f.codigo_municipio = u.codigo_municipio
GROUP BY u.municipio, u.departamento
ORDER BY total_camas DESC
LIMIT 10;

-- R3: Distribución del empleo e infraestructura por categoría comercial
SELECT 
    c.categoria,
    COUNT(f.id_fact) AS total_prestadores,
    SUM(f.numero_de_empleados) AS total_empleados,
    SUM(f.numero_de_habitaciones) AS total_habitaciones
FROM fact_turismo_anual f
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
GROUP BY c.categoria
ORDER BY total_empleados DESC;

-- R4: Concentración y promedio de empleo por establecimiento según categoría
SELECT 
    c.categoria,
    ROUND(AVG(f.numero_de_empleados), 2) AS promedio_empleados_por_est,
    MAX(f.numero_de_empleados) AS max_empleados
FROM fact_turismo_anual f
JOIN dim_categoria c ON f.id_categoria = c.id_categoria
GROUP BY c.categoria
ORDER BY promedio_empleados_por_est DESC;

-- R5: Evolución temporal de la oferta y capacidad instalada
SELECT 
    t.anio,
    COUNT(f.id_fact) AS total_registros_activos,
    SUM(f.numero_de_empleados) AS total_empleados,
    SUM(f.numero_de_habitaciones) AS total_habitaciones
FROM fact_turismo_anual f
JOIN dim_tiempo t ON f.anio = t.anio
GROUP BY t.anio
ORDER BY t.anio ASC;