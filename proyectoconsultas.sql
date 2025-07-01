SELECT * FROM "dim_tiempo" ;

SELECT * FROM "dim_cliente" ;

SELECT * FROM "dim_mensajero" ;
SELECT * FROM "dim_sede";

SELECT * FROM "fact_servicios";

SELECT * FROM "fact_novedades";

SELECT * FROM "stg_servicios"


"1"
SELECT 
    "Año",
    "Mes",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "Año", "Mes"
ORDER BY total_servicios DESC
LIMIT 5;


"2"

SELECT 
    "DiaSemana",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "DiaSemana"
ORDER BY total_servicios DESC;

"3"
SELECT 
    "Hora",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "Hora"
ORDER BY total_servicios DESC
LIMIT 5;

"4"
SELECT 
    "ClienteKey",
    "Año",
    "Mes",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "ClienteKey", "Año", "Mes"
ORDER BY total_servicios DESC
LIMIT 10;

"5"
SELECT 
    "MensajeroKey",
    COUNT(*) AS servicios_realizados,
    AVG("Duracion_Total_Min") AS duracion_promedio_min,
    AVG("Eficiencia_Mensajero") AS eficiencia_promedio
FROM fact_servicios
GROUP BY "MensajeroKey"
ORDER BY servicios_realizados DESC, eficiencia_promedio ASC
LIMIT 10;

"6"
SELECT 
    "ClienteKey",
    "SedeOrigenKey",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "ClienteKey", "SedeOrigenKey"
ORDER BY total_servicios DESC

"7"
SELECT 
    AVG("Duracion_Total_Min") AS tiempo_promedio_total_min
FROM fact_servicios;

"8"
SELECT 
    AVG("Duracion_Asignacion_Min") AS asignacion_promedio_min,
    AVG("Duracion_Recogida_Min") AS recogida_promedio_min,
    AVG("Duracion_Entrega_Min") AS entrega_promedio_min,
    AVG("Duracion_Cierre_Min") AS cierre_promedio_min
FROM fact_servicios;

"9"
SELECT 
    "TipoNovedad" AS "Tipo de Novedad",
    COUNT(*) AS "Total de Ocurrencias"
FROM 
    fact_novedades
GROUP BY 
    "TipoNovedad"
ORDER BY 
    "Total de Ocurrencias" DESC;

