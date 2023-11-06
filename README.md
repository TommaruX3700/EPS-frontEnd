# EPS-frontEnd
FrontEnd EPS 

NB: 
    Dentro View/Eps_Interface_Demo è presente "WindFormsApp1.exe" per avere uno spunto x interfaccia.

---
DeadLines:
NOVEMBRE - DICEMBRE INIZIO:
- avere antemprima interfaccia con 2 test case del cazzo.

---
Note su comunicazione I/O Model:

INPUT | model.exe: 
- STRINGA: posizione del file json, dimPalletX[cm], dimPalletY[cm] 

OUTPUT | model.exe:
- STRINGA: organizzata così
    nPallet, #codicePacco1, posX, posY, flagRuotato;
    nPallet, #codicePacco2, posX, posY, flagRuotato;
    ...