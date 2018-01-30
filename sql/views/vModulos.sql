CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `khaleesi`@`%` 
    SQL SECURITY DEFINER
VIEW `vModulos` AS
    SELECT 
        `track_modulo`.`id` AS `modulo_id`,
        `track_proyecto`.`id` AS `proyecto_id`,
        `track_proyecto`.`proyecto` AS `proyecto`,
        `track_modulo`.`modulo` AS `modulo`,
        `track_modulo`.`descripcion` AS `descripcion`
    FROM
        (`track_modulo`
        JOIN `track_proyecto` ON ((`track_proyecto`.`id` = `track_modulo`.`proyecto_id`)))
    WHERE
        ((`track_modulo`.`deleted` = 0)
            AND (`track_proyecto`.`deleted` = 0))
    ORDER BY `track_modulo`.`id`