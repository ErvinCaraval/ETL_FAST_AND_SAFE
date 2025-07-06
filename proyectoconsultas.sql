------- DIMENCIONES Y HECHOS

SELECT * FROM "dim_tiempo" ;

SELECT * FROM "dim_cliente" ;

SELECT * FROM "dim_mensajero" ;
SELECT * FROM "dim_sede";

SELECT * FROM "fact_servicios";

SELECT * FROM "fact_novedades";

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
