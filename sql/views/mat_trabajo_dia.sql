-- DROP TABLE mat_trabajo_dia
CREATE TABLE mat_trabajo_dia
SELECT
  tmp_trabajo.*
  -- , CAST(fecha AS datetime) AS ini
  -- , DATE_ADD(CAST(fecha AS datetime), INTERVAL 1439 minute) AS fin
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

-- Creamos un indice para mejorar busquedas
ALTER TABLE mat_trabajo_dia DROP INDEX index_mat_trabajo_dia_main;
CREATE INDEX index_mat_trabajo_dia_main ON mat_trabajo_dia (tarea_id, fecha) USING BTREE;
    
-- Trigger para actualizar la tabla tam_trabajo_dia
DROP TRIGGER IF EXISTS trigger_pizarron_insert;
CREATE TRIGGER trigger_pizarron_insert
AFTER INSERT ON track_pizarron
FOR EACH ROW BEGIN
    -- Eliminamos registros anteriores 
	DELETE FROM mat_trabajo_dia WHERE tarea_id = NEW.tarea_id AND fecha = DATE(NEW.created_at);
	-- Insertamos nuevos valores
	INSERT INTO mat_trabajo_dia
	SELECT tarea_id, fecha, nombre, responsable, proyecto, modulo, minutos
	FROM vTrabajoDia WHERE tarea_id = NEW.tarea_id AND fecha = DATE(NEW.created_at);
END
