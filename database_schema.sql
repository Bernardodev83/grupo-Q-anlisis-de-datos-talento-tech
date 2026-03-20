-- ======================================================
-- PROYECTO: EcoAnalytics Pro - Nivel Integrador
-- AUTOR: Bernardo & Equipo
-- DESCRIPCIÓN: Estructura de la Base de Datos en MySQL
-- ======================================================

-- 1. CREACIÓN DE LA ESTRUCTURA (DDL)
-- Esta tabla almacena los microdatos procesados del DANE 2019-2023
CREATE TABLE IF NOT EXISTS indicadores_ambientales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    periodo INT NOT NULL,
    id_empresa VARCHAR(50),
    seccion_economica VARCHAR(200),
    gastos_totales DECIMAL(20, 2),
    gasto_gestion_amb DECIMAL(20, 2),
    consumo_agua_m3 DECIMAL(20, 2),
    consumo_energia_kwh DECIMAL(20, 2),
    actividad_nombre TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CONSULTAS ANALÍTICAS (DML) - Requisito Punto 3 del Proyecto
-- Estas consultas demuestran el análisis profundo de los datos

-- A. Ranking de Sectores con Mayor Inversión Ambiental en Post-Pandemia (2022-2023)
SELECT 
    seccion_economica, 
    SUM(gasto_gestion_amb) AS total_inversion,
    AVG(consumo_energia_kwh) AS promedio_consumo_energia
FROM 
    indicadores_ambientales
WHERE 
    periodo >= 2022
GROUP BY 
    seccion_economica
ORDER BY 
    total_inversion DESC;

-- B. Análisis de Eficiencia Hídrica: Gasto Ambiental vs Consumo de Agua
SELECT 
    periodo,
    SUM(consumo_agua_m3) AS consumo_total_agua,
    SUM(gasto_gestion_amb) AS inversion_ambiental,
    (SUM(gasto_gestion_amb) / SUM(consumo_agua_m3)) AS indice_eficiencia_costo_agua
FROM 
    indicadores_ambientales
GROUP BY 
    periodo
ORDER BY 
    periodo ASC;