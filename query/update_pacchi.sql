-- UPDATE PACCHI
-- Da eseguire per ogni singolo pacco processato, aggiornare le variabili soltanto ed eseguire

-- VARIABILE_1: CODICE PALLET A CUI ASSEGNARE I PACCHI
SET @PALLET_ID = 125;

INSERT INTO pallet (CODICE_PALLET_ASSEGNATO)
SELECT @PALLET_ID
WHERE NOT EXISTS (SELECT 1 FROM pallet WHERE CODICE_PALLET_ASSEGNATO = @PALLET_ID);

UPDATE pacchi 
SET CODICE_PALLET_ASSEGNATO = @PALLET_ID 
-- VARIABILE_2: CODICI DEI PACCHI DA ASSEGNARE AL PALLET
WHERE ID_PACCO IN (1, 2, 3);

-- TESTS
-- OK 1. pacco assegnato a un nuovo pallet id, pallet esistente
-- OK 2. pacco assegnato a un nuovo palelt id, pallet non esistente
--  NEED TO FIX MY DATABASE SCHEMA
-- OK 3. pacco assegnato allo stesso pallet id, pallet esistente
