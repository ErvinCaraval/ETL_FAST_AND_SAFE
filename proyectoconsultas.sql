------- DIMENCIONES Y HECHOS

SELECT * FROM "dim_tiempo" ;

SELECT * FROM "dim_cliente" ;

SELECT * FROM "dim_mensajero" ;
SELECT * FROM "dim_sede";

SELECT * FROM "fact_servicios";

SELECT * FROM "fact_novedades";

-------CONSULTAS DIRECTAS A LA BODEGA DE DATOS 

"1"
SELECT 
    "Año",
    "Mes",
    COUNT(*) AS total_servicios
FROM fact_servicios
GROUP BY "Año", "Mes"
ORDER BY total_servicios DESC



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


"4"
SELECT 
    fs."ClienteKey",
    dc."nombre",
    fs."Año",
    fs."Mes",
    COUNT(*) AS total_servicios
FROM fact_servicios fs
INNER JOIN dim_cliente dc
    ON fs."ClienteKey" = dc."ClienteKey"
GROUP BY fs."ClienteKey", dc."nombre", fs."Año", fs."Mes"
ORDER BY total_servicios DESC;



"5"
SELECT 
    "MensajeroKey",
    COUNT(*) AS servicios_realizados,
    AVG("Duracion_Total_Min") AS duracion_promedio_min,
    AVG("Eficiencia_Mensajero") AS eficiencia_promedio
FROM fact_servicios
GROUP BY "MensajeroKey"
ORDER BY servicios_realizados DESC, eficiencia_promedio ASC


"6"
SELECT 
    fs."ClienteKey",
    dc."nombre" AS nombre_cliente,
    ds."nombre" AS nombre_sede_origen,
    COUNT(*) AS total_servicios
FROM fact_servicios fs
INNER JOIN dim_cliente dc
    ON fs."ClienteKey" = dc."ClienteKey"
INNER JOIN dim_sede ds
    ON fs."SedeOrigenKey" = ds."SedeKey"
GROUP BY fs."ClienteKey", dc."nombre", fs."SedeOrigenKey", ds."nombre"
ORDER BY total_servicios DESC;




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

-------CONSULTAS DATAMART ANALITICO 
"1"	
SELECT * FROM "resumen_servicios_por_mes"

"2"
SELECT * FROM "resumen_servicios_por_dia_semana"


"3"
SELECT * FROM "resumen_actividad_por_hora"

"4"
SELECT * FROM "servicios_por_cliente_mes"


"5"
SELECT * FROM  "eficiencia_mensajeros"

"6"
SELECT * FROM  "actividad_por_sede_cliente"

"7"
SELECT * FROM "duracion_promedio_servicio"

"8"
SELECT * FROM "duracion_promedio_por_fase"

"9"
SELECT * FROM "novedades_por_tipo"
