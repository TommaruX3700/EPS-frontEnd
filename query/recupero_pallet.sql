-- SELEZIONE PALLET A SISTEMA
-- non è necessario modificare ulteriormente la query, restituisce tutti i pallet registrati a sistema

SELECT 
	CODICE_PALLET AS CODICE_PALLET,
    DIM_X_PALLET AS X,
    DIM_Y_PALLET AS Y,    
    DIM_Z_PALLET AS ALTEZZA,
-- "N_PACCHI" rappresenta il numero di pacchi che sono attualmente registrati al suddetto Pallet
    (SELECT COUNT(pacchi.ID_PACCO) FROM pacchi WHERE pacchi.CODICE_PALLET = pallet.CODICE_PALLET) AS N_PACCHI
FROM `pallet` 
WHERE 1