-- SELEZIONE PALLET A SISTEMA
-- OK, tested

SELECT 
	CODICE_PALLET_ASSEGNATO AS CODICE_PALLET,
    DIM_X AS X,
    DIM_Y AS Y,
    DIM_Z AS ALTEZZA,
    (SELECT COUNT(pacchi.ID_PACCO) FROM pacchi WHERE pacchi.CODICE_PALLET_ASSEGNATO = pallet.CODICE_PALLET_ASSEGNATO) AS N_PACCHI
FROM `pallet` 
WHERE 1