-- UPDATE_PACCHI

-- eseguire la query solo per un pallet alla volta 

-- 2: se non esiste, lo creo
-- 3: modifico il valore "codice_pallet_assegnato" dei pacchi da caricare con il valore di pallet correlato

SET @ID = 1;
SET @PALLET_EXISTS = (SELECT COUNT(1) FROM pallet WHERE pallet.CODICE_PALLET_ASSEGNATO = @ID);

-- DELIMITER //
-- CREATE PROCEDURE procedura1 (param1 INT, param2 CHAR(3),
--        OUT param3 INT)
-- BEGIN
--        DECLARE finito INT default 0;
--        DECLARE a INT;
--        DECLARE b CHAR(50);
-- END; //
-- DELIMITER ;

SELECT 1
    CASE 
        WHEN @PALLET_EXISTS = 0 THEN -- query 1
        ELSE ()
    END
    INSERT INTO PA
FROM pacchi;

SELECT @PALLET_EXISTS;

