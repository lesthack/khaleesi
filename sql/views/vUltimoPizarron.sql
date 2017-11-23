CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `khaleesi`@`%` 
    SQL SECURITY DEFINER
VIEW `vUltimoPizarron` AS
    SELECT 
        `track_pizarron`.`tarea_id` AS `tarea_id`,
        MAX(`track_pizarron`.`id`) AS `id`
    FROM
        `track_pizarron`
    GROUP BY `track_pizarron`.`tarea_id`