DROP FUNCTION IF EXISTS fnMinutosTarea;
CREATE FUNCTION fnMinutosTarea(in_tarea_id INT, ini datetime, fin datetime)
RETURNS FLOAT
BEGIN
    /*
        Obtiene las horas reales de una tarea
        entre una rango de fechas especificadas  
    */
	DECLARE done INT DEFAULT FALSE;
    DECLARE sts INT;
    DECLARE last_sts INT;
    DECLARE fecha datetime;
    DECLARE fecha_ini datetime;
    DECLARE fecha_fin datetime;
    DECLARE segundos_totales FLOAT;
    
    DECLARE curs_tareas CURSOR FOR 
        SELECT status, convert_tz(track_pizarron.created_at, '+00:00', '-06:00') AS fecha 
        FROM track_pizarron 
        WHERE 
            track_pizarron.tarea_id = in_tarea_id
            AND convert_tz(track_pizarron.created_at, '+00:00', '-06:00') BETWEEN ini AND fin -- Se consideran 6 horas de diferencia
        ORDER BY track_pizarron.created_at;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN curs_tareas;
    
    SET @segundos_totales := 0;
    SET @last_sts := -1;
    
    tareas: LOOP
        FETCH curs_tareas INTO sts, fecha;
        
        IF done THEN
            LEAVE tareas;
        END IF;
        
        IF sts = 2 and @last_sts != 2 THEN
            SET @fecha_ini := fecha;
        END IF;
        
        IF sts != 2 THEN
            SET @fecha_fin := fecha;
            IF @fecha_fin > @fecha_ini THEN
                SET @segundos_totales = @segundos_totales + TIMESTAMPDIFF(SECOND, @fecha_ini, @fecha_fin);
                SET @fecha_ini = Null;
            END IF;
        END IF;
        
        SET @last_sts := sts;
    END LOOP;   
    
    -- Agregando opcion para tareas no finalizadas
    -- Se considera límite a las 6 pm
    IF @last_sts = 2 AND TIME(@fecha_ini) <= '18:00:00' THEN
        -- Si el ultimo estatus es pausado
        SET @segundos_totales = @segundos_totales + TIMESTAMPDIFF(SECOND, @fecha_ini, DATE_ADD(CAST(DATE(@fecha_ini) AS datetime), INTERVAL 1080 minute));
    END IF;

    CLOSE curs_tareas;
    
    RETURN ceil(@segundos_totales/60);
END;
