CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `khaleesi`@`%` 
    SQL SECURITY DEFINER
VIEW `vStatusTarea` AS
    SELECT 
        `track_pizarron`.`id` AS `id`,
        `track_pizarron`.`log` AS `log`,
        `track_pizarron`.`created_at` AS `created_at`,
        `track_pizarron`.`updated_at` AS `updated_at`,
        `track_pizarron`.`created_by_id` AS `created_by_id`,
        `track_pizarron`.`tarea_id` AS `tarea_id`,
        `track_pizarron`.`status` AS `status`
    FROM
        (`track_pizarron`
        JOIN `vUltimoPizarron` ON (((`vUltimoPizarron`.`id` = `track_pizarron`.`id`)
            AND (`vUltimoPizarron`.`tarea_id` = `track_pizarron`.`tarea_id`))))