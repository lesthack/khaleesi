-- DROP VIEW vTrabajoDia
CREATE VIEW vTrabajoDia AS
SELECT
  tmp_trabajo.*
  , CAST(fecha AS datetime) AS ini
  , DATE_ADD(CAST(fecha AS datetime), INTERVAL 1439 minute) AS fin
  , fnMinutosTarea(tarea_id, CAST(fecha AS datetime), DATE_ADD(CAST(fecha AS datetime), INTERVAL 1439 minute)) AS minutos
FROM (
    SELECT
        track_tarea.id AS tarea_id
        , DATE(track_pizarron.created_at) AS fecha
        , track_tarea.nombre
        , auth_user.username AS responsable
        , vModulos.proyecto
        , vModulos.modulo         
    FROM track_pizarron
        INNER JOIN track_tarea ON track_tarea.id = track_pizarron.tarea_id
        INNER JOIN auth_user ON auth_user.id = track_tarea.responsable_id
        INNER JOIN vModulos ON vModulos.modulo_id = track_tarea.modulo_id
    GROUP BY
        track_pizarron.tarea_id    
        , fecha
        , track_tarea.nombre
        , auth_user.username
        , vModulos.proyecto
        , vModulos.modulo
        -- minutos
    ORDER BY 
        fecha DESC
) tmp_trabajo;


-- SELECT * FROM vTrabajoDia WHERE tarea_id = 421 AND fecha = DATE(NOW())
