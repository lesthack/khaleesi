CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `khaleesi`@`%` 
    SQL SECURITY DEFINER
VIEW `vReporteTareas` AS
    SELECT 
        `track_tarea`.`id` AS `id`,
        `track_tarea`.`nombre` AS `nombre`,
        YEAR(`track_tarea`.`fecha_inicial`) AS `año`,
        MONTH(`track_tarea`.`fecha_inicial`) AS `mes`,
        `track_tarea`.`fecha_inicial` AS `fecha_inicial_estimada`,
        `track_tarea`.`fecha_final` AS `fecha_final_estimada`,
        TIMESTAMPDIFF(DAY,
            `track_tarea`.`fecha_inicial`,
            `track_tarea`.`fecha_final`) AS `diff_estimada`,
        (SELECT 
                MIN(`track_pizarron`.`created_at`)
            FROM
                `track_pizarron`
            WHERE
                (`track_pizarron`.`tarea_id` = `track_tarea`.`id`)) AS `fecha_inicial_real`,
        (SELECT 
                MAX(`track_pizarron`.`created_at`)
            FROM
                `track_pizarron`
            WHERE
                (`track_pizarron`.`tarea_id` = `track_tarea`.`id`)) AS `fecha_final_real`,
        TIMESTAMPDIFF(DAY,
            (SELECT 
                    MIN(`track_pizarron`.`created_at`)
                FROM
                    `track_pizarron`
                WHERE
                    (`track_pizarron`.`tarea_id` = `track_tarea`.`id`)),
            (SELECT 
                    MAX(`track_pizarron`.`created_at`)
                FROM
                    `track_pizarron`
                WHERE
                    (`track_pizarron`.`tarea_id` = `track_tarea`.`id`))) AS `diff_real`,
        `track_tarea`.`horas_estimadas` AS `horas_estimadas`,
        FORMAT(FNHORASREALES(`track_tarea`.`id`),
            2) AS `horas_reales`,
        (`track_tarea`.`horas_estimadas` - FORMAT(FNHORASREALES(`track_tarea`.`id`),
            2)) AS `diff_horas`,
        (CASE
            WHEN (`track_tarea`.`status` = 1) THEN 1
            ELSE 0
        END) AS `terminada`,
        `track_proyecto`.`proyecto` AS `proyecto`,
        `track_modulo`.`modulo` AS `modulo`,
        `auth_user`.`username` AS `responsable`,
        (CASE
            WHEN (`vStatusTarea`.`status` = 0) THEN 'Asignado'
            WHEN (`vStatusTarea`.`status` = 1) THEN 'Pendiente'
            WHEN (`vStatusTarea`.`status` = 2) THEN 'En Proceso'
            WHEN (`vStatusTarea`.`status` = 3) THEN 'Pausado'
            WHEN (`vStatusTarea`.`status` = 4) THEN 'Terminado'
            WHEN (`vStatusTarea`.`status` = 5) THEN 'Bloqueado'
            WHEN (`vStatusTarea`.`status` = 6) THEN 'Reasignado'
            WHEN (`vStatusTarea`.`status` = 7) THEN 'Abandonada'
            ELSE 'Desconocido'
        END) AS `status`,
        `track_proyecto`.`id` AS `proyecto_id`,
        `track_modulo`.`id` AS `modulo_id`
    FROM
        ((((`track_tarea`
        JOIN `vStatusTarea` ON ((`vStatusTarea`.`tarea_id` = `track_tarea`.`id`)))
        JOIN `auth_user` ON ((`auth_user`.`id` = `track_tarea`.`responsable_id`)))
        JOIN `track_modulo` ON ((`track_modulo`.`id` = `track_tarea`.`modulo_id`)))
        JOIN `track_proyecto` ON ((`track_proyecto`.`id` = `track_modulo`.`proyecto_id`)))
    ORDER BY `track_tarea`.`id`