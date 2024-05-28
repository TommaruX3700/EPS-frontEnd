-- SELEZIONE PACCHI A SISTEMA BY PALLET_ID
-- OK, tested
-- NB: fillare le parentesi con gli id dei pallet di cui si vuole recuperare i pacchi collegati

SELECT *
FROM `pacchi`
WHERE pacchi.CODICE_PALLET_ASSEGNATO IN (0)