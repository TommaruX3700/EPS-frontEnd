## EPS - Model v1.0 
Eseguire l'exe fornendo come unico argomento una stringa contenente il percorso di sistema del file .json di input.
Il file .json di input deve avere un formato come il file input di esempio fornito "inputPackListSample.json".
L'output verrà salvato successivamente nella stessa posizione dove si trova il file exe del modello, in formato json come "output.json".

---

### EPS_MODEL error codes:
- 3: senza pacchi //error code 3, nessun pacco in input // error code 3
- 2: con un pallet minuscolo (che non riesce a tenere nulla) //error code 2, pallet dimensione troppo piccola
- 11: info pallet corrotte 
- 10: RILEVATO PACCO SENZA ID REGISTRATO A SISTEMA 