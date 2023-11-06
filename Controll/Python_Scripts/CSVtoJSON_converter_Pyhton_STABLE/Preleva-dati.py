from pytz import timezone
from datetime import datetime
import pandas as pd
import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import configparser

if __name__=="__main__":
    # Setta la current dir
    mainfolder=pathlib.Path(__file__).parent.resolve()
    config = configparser.ConfigParser()
    config.read("{0}/config.ini".format(mainfolder))
    log_level=logging.ERROR
    stampa_stack=False
    if log_level < logging.ERROR:
        stampa_stack=True
    dt_naive = datetime.now()
    tz= timezone("Europe/Rome")
    dt= tz.localize(dt_naive)
    # setta il nome del log
    log_file = ('{0}/logger.log'.format(config['cartelle']['LOG_FOLDER']))
    # crea il demone del log
    logger = logging.getLogger("Rotating Log")
    # imposta il livello di log (vedere "importanza" livelli)
    logger.setLevel(log_level)
    # handler fa una cosa ogni tot, in questo caso crea un "log_file" ogni "d (giorno), fino ad un massimo di backupCount=5(files)"
    try:
        handler = TimedRotatingFileHandler(log_file, when="d", interval=1, backupCount=5)
    except FileNotFoundError as err:
        # se non trova la folder remota DI LOG, scrive nella folder corrente (e a prossima volta se se sveia...)
        log_file = ('{0}/logger.log'.format(mainfolder))
        logger = logging.getLogger("Rotating Log")
        logger.setLevel(log_level)
        handler = TimedRotatingFileHandler(log_file, when="d", interval=1, backupCount=5)
        logger.addHandler(handler)
        logger.error("{0} {1:30s}\t".format(dt.strftime("%Y-%m-%d %H:%M:%S %z"),"Directory di logger non esistente"),exc_info=stampa_stack)
    # assegno l'handler al demone
    logger.addHandler(handler)
    try:
        uscita= pd.read_csv(config['cartelle']['FILENAME1'], delimiter=";",usecols=["NUM_SPEDIZIONE","NUMERO_COLLO","CODICE_CLIENTE","PESO_NETTO","PESO_LORDO","BASE_MAGGIORE","BASE_MINORE","ALTEZZA","FLAG_PALETTIZZABILE","FLAG_SOVRAPPONIBILE","FLAG_RUOTABILE"])
        uscita= uscita.fillna("")
        uscita.to_json(config['cartelle']['OUT'])
        logger.debug("{0} {1:30s}\t".format(dt.strftime("%Y-%m-%d %H:%M:%S %z"),"Eseguito trasferimento correttamente."))
        # gestisco l'errore di filenotfound riguardante il csv
    except FileNotFoundError as err:
        logger.error("{0} {1:30s}\t".format(dt.strftime("%Y-%m-%d %H:%M:%S %z"),"File csv non esistente o folder sbagliata"),exc_info=stampa_stack)