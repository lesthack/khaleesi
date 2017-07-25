#DROP VIEW vProyectos
CREATE OR REPLACE VIEW vProyectos AS
SELECT 
	track_proyecto.id,
	track_proyecto.proyecto as nombre_proyecto,
    track_proyecto.descripcion,
    track_proyecto.link,
    track_proyecto.archived,
    modulos.totales as modulos_totales,
    issues.abiertos as issues_abiertos,
    issues.resueltos as issues_resueltos,
    issues.abandonados as issues_abandonados,
    issues.cancelados as issues_cancelados
FROM track_proyecto
	INNER JOIN (
		SELECT 
			track_modulo.proyecto_id,     
			count(*) as totales
		FROM track_modulo
		WHERE track_modulo.deleted = False
		GROUP BY proyecto_id
    ) modulos ON modulos.proyecto_id = track_proyecto.id
    INNER JOIN (
		SELECT 
			track_modulo.proyecto_id,    
			SUM(CASE WHEN track_issue.status = 0 THEN 1 ELSE 0 END) as abiertos,
			SUM(CASE WHEN track_issue.status = 1 THEN 1 ELSE 0 END) as resueltos,
			SUM(CASE WHEN track_issue.status = 2 THEN 1 ELSE 0 END) as abandonados,
			SUM(CASE WHEN track_issue.status = 3 THEN 1 ELSE 0 END) as cancelados
		FROM track_issue
			INNER JOIN track_modulo ON track_modulo.id = track_issue.modulo_id
		GROUP BY
			track_modulo.proyecto_id
    ) issues ON issues.proyecto_id = track_proyecto.id
WHERE deleted = False;
 
SELECT * FROM vProyectos;
SELECT * FROM vReporteTareas;
SELECT * FROM track_pizarron;
SELECT * FROM vStatusTarea