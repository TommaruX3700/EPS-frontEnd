from tkinter import *
import tkinter as tk
import time
import pathlib
from tkinter import filedialog
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
log = ""
input = ""
uscita = ""
cfg = ""
nomefile = ""

mainfolder=pathlib.Path(__file__).parent.resolve()

def diruscita():
    global uscita
    uscita = filedialog.askdirectory()

def dirinput():
    global input
    input = filedialog.askopenfilename(filetypes=[("CSV files", ".csv .txt")])


def dirlog():
    global log
    log = filedialog.askdirectory()


def stop():
    global nomefile
    nomefile = simpledialog.askstring(title="Nome file di uscita",prompt="Inserire il nome del file di optput:")
    if(nomefile==""):
        messagebox.showerror ("Attenzione", "nessun nome file applicato")
        nomefile = simpledialog.askstring(title="Nome file di uscita",prompt="Inserire il nome del file di optput:")
    global uscita
    if(uscita==""):
        messagebox.showerror ("Attenzione", "nessuna cartella di uscita selezionata")
        uscita= filedialog.askdirectory()
    global input
    if(input==""):
        messagebox.showerror ("Attenzione", "nessun file CSV specificato")
        input = filedialog.askopenfilename(filetypes=[("CSV files", ".csv .txt")])
    global log
    if(log==""):
        messagebox.showerror ("Attenzione", "nessuna cartella di log selezionata")
        log = filedialog.askdirectory()
    global cfg
    if(cfg==""):
        messagebox.showerror ("Attenzione", "nessun file di configurazione selezionato")
        cfg = filedialog.askopenfilename(filetypes=[(".ini Files", ".ini .txt")])
    time.sleep(1)
    messagebox.showinfo("Info","Impostazioni Applicate")
    finestra.destroy()
    

def aprifile():
    global cfg
    cfg = filedialog.askopenfilename(filetypes=[(".ini Files", ".ini .txt")])
    

def annulla():
    risposta=messagebox.askyesno(title="Chiudere il menù di selezione?",message="Chiudere il programma?")
    if (risposta==True):
        finestra.destroy()
    else:
        pass


finestra = Tk()
finestra.title("menù di selezione")
finestra.geometry("383x170")
finestra.resizable(width=False, height=False)
try:
    sfondo= tk.PhotoImage(file="{0}/ITSMres.png".format(mainfolder))
except TclError as err:
    messagebox.showerror ("ATTENZIONE", "Non è stato possibile trovare il percorso contenente lo sfondo del menù")
    finestra.destroy()

immagine=Label(finestra, i=sfondo)
selezione1 = Button(text="Seleziona file di configurazione...",height= 1, width=30,command=aprifile)

selezione2 = Button(text="Seleziona directory di uscita...",height= 1, width=30,command=diruscita)

selezione3 = Button(text="Seleziona file di input...",height= 1, width=30,command=dirinput)

selezione4 = Button(text="Seleziona directory file di log...",height= 1, width=30,command=dirlog)


arresta = Button(text="Annulla",command=annulla)
chiudi = Button(text="Applica",command=stop)


selezione1.place(x=100,y=70)
selezione4.place(x=100,y=40)
selezione3.place(x=100,y=9)
selezione2.place(x=100,y=100)
arresta.place(x=320,y=140)
chiudi.place(x=10,y=140)
immagine.pack()

finestra.mainloop()

linee = ['[cartelle]','\n','FILENAME1 = ',input,'\n','OUT = ', uscita,'/',nomefile,'.json','\n','LOG_FOLDER = ',log]
try:
    with open (cfg, "w+")as f:
        for line in linee:
            f.write(line)
except FileNotFoundError as err:
    messagebox.showerror ("ATTENZIONE", "Nessun file di configurazione selezionato o file inesistenti, il file rimarrà invariato")


