-- UPDATE PACCHI
-- Query che registra tutti i pacchi per un singolo pallet.
-- Eseguire per un pallet alla volta.

-- VARIABILE_1: CODICE PALLET A CUI ASSEGNARE I PACCHI
SET @PALLET_ID = 125;
SET @X_DIM_PALLET = 100;
SET @Y_DIM_PALLET = 100;
SET @Z_DIM_PALLET = 100;

INSERT INTO pallet (CODICE_PALLET, DIM_X_PALLET, DIM_Y_PALLET, DIM_Z_PALLET)
SELECT @PALLET_ID, @X_DIM_PALLET, @Y_DIM_PALLET, @Z_DIM_PALLET
WHERE NOT EXISTS (SELECT 1 FROM pallet WHERE CODICE_PALLET = @PALLET_ID);

INSERT INTO pacchi (ID_PACCO, NUM_SPEDIZIONE, CODICE_CLIENTE, PESO_NETTO, PESO_LORDO, BASE_MAGGIORE, BASE_MINORE, ALTEZZA, FLAG_PALLETTIZZABILE,  FLAG_SOVRAPPONIBILE, FLAG_RUOTABILE)
SELECT 101010, 1, 1, 1, 1, 1, 1, 1, 'N', 'N', 'N'
WHERE NOT EXISTS (SELECT 1 FROM pacchi WHERE ID_PACCO = 101010);

UPDATE pacchi 
SET CODICE_PALLET = @PALLET_ID 
-- VARIABILE_2: CODICI DEI PACCHI DA ASSEGNARE AL PALLET
WHERE ID_PACCO IN (1, 2, 3);
