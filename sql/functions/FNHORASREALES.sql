CREATE FUNCTION `khaleesi`.`FNHORASREALES`(in_tarea_id INT) RETURNS float
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE sts INT;
    DECLARE last_sts INT;
    DECLARE fecha datetime;
    DECLARE fecha_ini datetime;
    DECLARE fecha_fin datetime;
    DECLARE segundos_totales FLOAT;
    DECLARE curs_tareas CURSOR FOR SELECT status, created_at 
        FROM track_pizarron 
        WHERE track_pizarron.tarea_id = in_tarea_id 
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
    
    CLOSE curs_tareas;
    
    RETURN @segundos_totales/3600;
END
