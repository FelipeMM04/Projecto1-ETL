-- ESQUEMA DEL DATA WAREHOUSE (ODS 8 - TURISMO COLOMBIA)
-- MOTOR: MySQL

CREATE DATABASE IF NOT EXISTS dw_turismo_ods8 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE dw_turismo_ods8;

-- 1. TABLA DIMENSIÓN UBICACIÓN
DROP TABLE IF EXISTS fact_turismo_anual;
DROP TABLE IF EXISTS dim_ubicacion;

CREATE TABLE dim_ubicacion (
    codigo_municipio INT PRIMARY KEY,
    municipio VARCHAR(150) NOT NULL,
    codigo_departamento INT NOT NULL,
    departamento VARCHAR(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. TABLA DIMENSIÓN CATEGORÍA
DROP TABLE IF EXISTS dim_categoria;

CREATE TABLE dim_categoria (
    id_categoria INT PRIMARY KEY,
    categoria VARCHAR(150) NOT NULL,
    sub_categoria VARCHAR(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. TABLA DIMENSIÓN PRESTADOR
DROP TABLE IF EXISTS dim_prestador;

CREATE TABLE dim_prestador (
    codigo_rnt INT PRIMARY KEY,
    razon_social VARCHAR(255) NOT NULL,
    nit VARCHAR(50) NOT NULL,
    estado_rnt VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. TABLA DIMENSIÓN TIEMPO
DROP TABLE IF EXISTS dim_tiempo;

CREATE TABLE dim_tiempo (
    anio INT PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. TABLA DE HECHOS (FACT TABLE)
CREATE TABLE fact_turismo_anual (
    id_fact INT PRIMARY KEY,
    codigo_rnt INT NOT NULL,
    codigo_municipio INT NOT NULL,
    id_categoria INT NOT NULL,
    anio INT NOT NULL,
    numero_de_habitaciones INT NOT NULL DEFAULT 0,
    numero_de_camas INT NOT NULL DEFAULT 0,
    numero_de_empleados INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_fact_prestador FOREIGN KEY (codigo_rnt) REFERENCES dim_prestador(codigo_rnt),
    CONSTRAINT fk_fact_ubicacion FOREIGN KEY (codigo_municipio) REFERENCES dim_ubicacion(codigo_municipio),
    CONSTRAINT fk_fact_categoria FOREIGN KEY (id_categoria) REFERENCES dim_categoria(id_categoria),
    CONSTRAINT fk_fact_tiempo FOREIGN KEY (anio) REFERENCES dim_tiempo(anio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;