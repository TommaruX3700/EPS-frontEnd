import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QDialog, QFormLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QGroupBox, QHeaderView, QTableWidgetItem,QTableWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd
import mysql.connector
import json
import configparser 
import os
import json
import pdfkit
import jinja2
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import QApplication,QMessageBox
import copy
import fitz

file_path = ''

def mainfolderFinder():
    '''Trova la cartella attuale'''
    mainfolder = ''
    mainfolder_buff=__file__
    mainfolder_buff = mainfolder_buff.split(sep='\\')
    mainfolder_buff.pop(-1)
    for name in mainfolder_buff:
        mainfolder += name
        mainfolder += '\\' 
    
    return(mainfolder)

def json_updater(json_path,Lenght,Width,Height,MXWeight,Shipment_type):
    if Lenght is None or Width is None or Height is None:
        new_data ={"Shipment_type":"NA",
        "Lenght": 120,
        "Width": 120,
        "Height": 120,
        "MXWeight" : 20
        }
        with open(json_path,'r+') as j:
            file_data = json.load(j)
            file_data["user_settings"] = (new_data)
            j.seek(0)
            json.dump(file_data, j, indent = 4)
    else:
        if Shipment_type is None:
            Shipment_type = "NA"
        new_data = new_data ={"Shipment_type":Shipment_type,
        "Lenght":Lenght,
        "Width": Width,
        "Height": Height,
        "Max Weight" : MXWeight
        }
        with open(json_path,'r+') as j:
            file_data = json.load(j)
            file_data["user_settings"] = (new_data)
            j.seek(0)
        with open(json_path,'w') as j:
            json.dump(file_data, j, indent = 4)


def create_pdf(mainfolder,data):
    '''funzione che crea il pdf partendo da un file html'''
    built_pallets={}
    temp_pallet = {}
    firstRound = True
    chiavi = []
    chiaviJson = []
    n_p=0
    try:
        html_path = mainfolder
        html_path += 'template_bolla.html'
        or_html = mainfolder
        or_html += 'default'
        json_path = mainfolder
        json_path += '\EPS_MODEL\input_for_model.json'
        my_data = load_json(json_path)
        for Jchiave in my_data:
            if Jchiave == 'user_settings':
                pass
            else:
                chiaviJson.append(Jchiave)
        t = 0        
        for pallet in (data['Pallets']):
            i=0
            for pacco in pallet['Packs']:
                idx = pallet['Packs'][i]['id']
                temp_pallet[idx] = pacco
                try:
                    for indice in my_data:
                        if my_data[indice]['NUMERO_COLLO'] == idx:
                            break
                        else:
                            continue
                    built_pallets[idx] = my_data[indice]
                    built_pallets[idx]['CODICE_PALLET'] = int(pallet['Pallet'])
                    built_pallets[idx]['COLORE_GRUPPO'] = int(pallet['Pallet']) *4
                    built_pallets[idx]['COLORE_GRUPPO'] = hex(built_pallets[idx]['COLORE_GRUPPO'])
                except Exception as err:
                    if firstRound is True:
                        for chiave in my_data:
                            if chiave == 'user_settings':
                                pass
                            else:
                                chiavi.append(int(chiave))
                    firstRound = False
                    built_pallets[idx] = my_data[str(chiavi[t])]
                    built_pallets[idx]['CODICE_PALLET'] = int(pallet['Pallet'])
                    built_pallets[idx]['COLORE_GRUPPO'] = int(pallet['Pallet']) *4
                    built_pallets[idx]['COLORE_GRUPPO'] = hex(built_pallets[idx]['COLORE_GRUPPO'])
                    t +=1
                i=i+1
            n_p = n_p+1

        with open(or_html, 'r') as h:
            orBuff = h.readlines()
        with open(html_path, 'w') as h:
            h.writelines(orBuff)

        with open(html_path, 'r') as h:
            buffer = h.readlines()
        strt_line = []
        for linea in buffer:
            if "tabella_dinamica" in linea:
                strt_line.append(buffer.index(linea))
                if "'id=\"end_of_tabella_dinamica\">'" in linea:
                    tt_lines = strt_line[0] - strt_line[1]
                    break
        tt_lines = strt_line[1] - strt_line[0]
        j = 0
        indici = []
        for pallet in built_pallets:
                
            htmlColor1 = ((built_pallets[int(pallet)]['COLORE_GRUPPO']).replace('0x','#'))
            i=0
            idx = tt_lines -2
            k = strt_line[1]
            stringhe = []
            if j % 2 == 0:
                stringhe.append('''<tr id="colonna_dinamica" style="background-color:{0};">\n'''.format(htmlColor1)) # 
            else:
                stringhe.append('''<tr id="colonna_dinamica" style="background-color:{0};">\n'''.format(htmlColor1))
                
            stringhe.append('''<th scope="row" style="font-family:\'Serif\'">{0}</th>\n'''.format(built_pallets[int(pallet)]['CODICE_PALLET']))
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(str(pallet)))
            dimensioni = str(built_pallets[int(pallet)]['BASE_MAGGIORE'])
            dimensioni += 'x'
            dimensioni += str(built_pallets[int(pallet)]['BASE_MINORE'])
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(dimensioni))
            fr = built_pallets[int(pallet)]['FLAG_RUOTABILE']
            if fr == '':
                fr = 'No'
            else:
                fr = 'Yes'
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(fr))   
            fs = built_pallets[int(pallet)]['FLAG_SOVRAPPONIBILE']
            if fs == '':
                fs = 'No'
            else:
                fs = 'Yes'
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(fs))
            stringhe.append('''</tr id="end_of_colonna_dinamica">\n''')
            for stringa in stringhe:
                buffer.insert(k,stringa)
                k = k + 1
                i=i+1
            
            j = j+1           

        with open(html_path,'w') as h:
            h.writelines(buffer)

        template_loader = jinja2.FileSystemLoader(mainfolder)
        template_env = jinja2.Environment(loader=template_loader)
        bollaPathOut = mainfolder
        bollaPathOut += 'bolla.pdf'
        cssPath = mainfolder
        cssPath += 'Bootstrap\\bootstrap-5.0.2-dist\\css\\bootstrap.css'
        config_path = mainfolder
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        jsPath = mainfolder
        jsPath += 'Bootstrap\\bootstrap-5.0.2-dist\\js\\bootstrap.js'
        photoPath = mainfolder
        photoPath += 'EPS_LOGO_rsz.png'
        template = template_env.get_template('template_bolla.html')
        dt_naive = datetime.now()
        context={"bootstrap_5_PATH":cssPath,"bootstrapScript_5_PATH":jsPath,"EPS_logo_PATH":photoPath,"nome_cliente":str(config.get('RECAPITI','nome')),"via_cliente": str(config.get('RECAPITI','via')),"citt_cliente":str(config.get('RECAPITI','citta')),"naz_cliente":str(config.get('RECAPITI','nazione')),"cap_cliente":int(config.get('RECAPITI','cap')),"plt_idx":1,"art_cdx":2,"dim":"24x60 Cm","RT_flag":True,"SV_flag":False,"n_delivery":4,"date_of_delivery":dt_naive.strftime("%d/%m/%Y %H:%M"),"shipm_type":my_data['user_settings']['Shipment_type']}
        output_text = template.render(context)
        wkhtmltopdf = mainfolder
        wkhtmltopdf += 'wkhtmltox\\bin\\wkhtmltopdf.exe'
        pdfConfig = pdfkit.configuration(wkhtmltopdf= wkhtmltopdf)
        pdfkit.from_string(output_text,options={"enable-local-file-access": ""}, output_path=bollaPathOut, configuration=pdfConfig,css=cssPath)
    except TypeError as err:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Attenzione")
        msg.setInformativeText("\nL'algoritmo di nesting non è stato in grado di creare il file PDF, in quanto non c'è abbastanza spazio sul pallet\n\nNessun pacco inserito nel file\n")
        msg.setWindowTitle("Attenzione")
        msg.exec_()
    except Exception as err:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Errore durante a creazione del PDF")
        msg.setInformativeText("\nSi è verificata un'eccezione durante la creazione del file PDF\n\nAllegare il codice errore agli sviluppatori per correggere l'anomalia\n\nErrore: {0}\n".format(err))
        msg.setWindowTitle("Errore durante a creazione del PDF")
        msg.exec_()

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menù Principale')
        self.setGeometry(100, 100, 320, 210)

        upload_button = QPushButton('Recupera collo da CSV', self)
        upload_button.clicked.connect(self.show_settings_window)
        upload_button.setFixedSize(320, 70)

        searchDB_button = QPushButton('Recupera collo da DataBase', self)
        searchDB_button.clicked.connect(self.show_DB_window_collo)
        searchDB_button.setFixedSize(320, 70)

        searchPLT_DB_button = QPushButton('Recupera pallet da DataBase', self)
        searchPLT_DB_button.clicked.connect(self.show_DB_window_pallet)
        searchPLT_DB_button.setFixedSize(320, 70)
        
        changeUserSettings_button = QPushButton('Impostazioni Utente',self)
        changeUserSettings_button.clicked.connect(self.changeUsrSettings)
        changeUserSettings_button.setFixedSize(320, 70)
        
        kill_btn = QPushButton('Esci',self)
        kill_btn.clicked.connect(self.suicide)
        kill_btn.setFixedSize(130,30)

        layout = QVBoxLayout()
        layout.addWidget(upload_button)
        layout.addWidget(searchDB_button)
        layout.addWidget(searchPLT_DB_button)
        layout.addWidget(changeUserSettings_button)
        layout.addWidget(kill_btn)

        self.setLayout(layout)
        
        
    def show_DB_window_pallet(self):
        mainfolder = mainfolderFinder()
        config_path = mainfolder
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)        
        try:
            mydb = mysql.connector.connect(
            host= str(config.get('DB_SETTINGS','db_host')),
            user=str(config.get('DB_SETTINGS','db_username')),
            password=str(config.get('DB_SETTINGS','db_password')),
            database=str(config.get('DB_SETTINGS','db_name')),
            )
            buffer_json = {}
            mycursor = mydb.cursor()
            query = '''SELECT 
	CODICE_PALLET AS CODICE_PALLET,
    DIM_X_PALLET AS X,
    DIM_Y_PALLET AS Y,    
    DIM_Z_PALLET AS ALTEZZA,
    (SELECT COUNT(pacchi.ID_PACCO) FROM pacchi WHERE pacchi.CODICE_PALLET = pallet.CODICE_PALLET) AS N_PACCHI
FROM `pallet` 
WHERE 1'''
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            for risultato in myresult:
                index = str(risultato[0])
                buffer_json[index] = ''
                risultato = list(risultato)
                risultato.remove(risultato[0])
                buffer_json[index] = risultato
                
            self.palletSelection = palletSelection(buffer_json)
            self.palletSelection.show()
            self.close()
        except mysql.connector.errors.DatabaseError as err:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Errore durante il collegamento al DB")
            msg.setInformativeText("\nSi è verificata un'eccezione durante il collegamento al database\n\nControllare che l'indirizzo del DataBase sia corretto e che sia raggiungibile\n")
            msg.setWindowTitle("Errore durante il collegamento al DB")
            msg.exec_()
             
        
    def show_DB_window_collo(self):
        mainfolder = mainfolderFinder()
        config_path = mainfolder
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)    
        x = str(config.get('DB_SETTINGS','db_password'))    
        try:
            mydb = mysql.connector.connect(
            host= str(config.get('DB_SETTINGS','db_host')),
            user= str(config.get('DB_SETTINGS','db_username')),
            password= str(config.get('DB_SETTINGS','db_password')),
            database= str(config.get('DB_SETTINGS','db_name')),
            )
            buffer_json = {}
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM `pacchi` WHERE 1")
            myresult = mycursor.fetchall()
            for risultato in myresult:
                index = str(risultato[0])
                buffer_json[index] = ''
                risultato = list(risultato)
                risultato.remove(risultato[0])
                buffer_json[index] = risultato
                
            self.db_window = databasePage(buffer_json)
            self.db_window.show()
            self.close()
        except mysql.connector.errors.DatabaseError as err:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Errore durante il collegamento al DB")
            msg.setInformativeText("\nSi è verificata un'eccezione durante il collegamento al database\n\nControllare che l'indirizzo del DataBase sia corretto e che sia raggiungibile\n")
            msg.setWindowTitle("Errore durante il collegamento al DB")
            msg.exec_()

    def printPDF(self):

        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path += '\\bolla.pdf'
        subprocess.Popen([path], shell=True)


    def show_settings_window(self, *args, **kwargs):
        askForCSV = kwargs.get('askForCSV')
        if askForCSV is not False:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, 'Open CSV File', '', 'CSV files (*.csv)')
            if file_path:
                mainfolder = mainfolderFinder()
                config_path = ''
                config_path += mainfolder
                config_path += 'config.ini'
                config = configparser.ConfigParser()
                config.read(config_path)
                uscita= pd.read_csv(file_path, delimiter=";",usecols=["NUM_SPEDIZIONE","NUMERO_COLLO","CODICE_CLIENTE","PESO_NETTO","PESO_LORDO","BASE_MAGGIORE","BASE_MINORE","ALTEZZA","FLAG_PALETTIZZABILE","FLAG_SOVRAPPONIBILE","FLAG_RUOTABILE"])
                uscita= uscita.fillna("")
                uscita.to_json(config['DEFAULT']['nome_json'],orient='index', indent=4)
            if (kwargs.get('width_edit') is None or kwargs.get('weight_edit') is None or kwargs.get('height_edit') is None or kwargs.get('length_edit') is None ):
                try:
                    json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=None,Width=None,Height=None,MXWeight=None,Shipment_type=None)
                except UnboundLocalError as err:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Errore")
                    msg.setInformativeText('Nessun file CSV selezionato')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    self.show_settings_window()
            else:
                json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=kwargs.get('length_edit'),Width=kwargs.get('width_edit'),Height=kwargs.get('height_edit'),MXWeight=40,Shipment_type=kwargs.get('shipment_type'))
            mainfolder = mainfolderFinder()
            config_path = ''
            config_path += mainfolder
            config_path += 'config.ini'
            config = configparser.ConfigParser()
            config.read(config_path)
            json_path = mainfolder
            json_path += config['DEFAULT']['nome_json']
            checkForErrorPath = mainfolder
            checkForErrorPath += 'EPS_MODEL\\EPS_MODEL.exe'
            try:
                checkForError = (subprocess.check_output([checkForErrorPath, str(json_path)]))
            except UnboundLocalError as err:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Errore")
                msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nRiferire il codice sottostante agli sviluppatori per correggere l'errore.\n\nErrore: {0}\n".format(err.returncode))
                msg.setWindowTitle("Errore Critico")
                msg.exec_()
                exit(1)
            except Exception as err:
                if err.returncode == 10:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Errore")
                    msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nNessun pacco selezionato o i pacchi selezionati sono corrotti\n\nErrore: {0}\n".format(err.returncode))
                    msg.setWindowTitle("Errore Critico")
                    msg.exec_()
                    self.goBack()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Errore")
                    msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nRiferire il codice sottostante agli sviluppatori per correggere l'errore.\n\nErrore: {0}\n".format(err.returncode))
                    msg.setWindowTitle("Errore Critico")
                    msg.exec_()
                    exit(1)
            
            json_path = mainfolder
            json_path += 'output.json'
            with open(json_path) as json_file:
                data = json.load(json_file)
            if data['UnNestedPacks'] is not None:
                notNestet = ''
                for pacco in data['UnNestedPacks']:
                    notNestet += str(pacco)
                    notNestet += ','
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Attenzione")
                msg.setInformativeText("\nDurante la creazione del pallet alcuni pacchi non sono stati inseriti\n\nQuando dei pacchi non vengono inseriti nel pallet, vuol dire che il pallet è troppo piccolo o già pieno.\n\nPacchi non inseriti: {0}\n".format(notNestet))
                msg.setWindowTitle("Attenzione")
                msg.exec_()
            create_pdf(mainfolder,data)
            self.settings_window = SettingsWindow(file_path)
            self.settings_window.show()
            self.close()
        else:
            mainfolder = mainfolderFinder()
            config_path = ''
            config_path += mainfolder
            config_path += 'config.ini'
            config = configparser.ConfigParser()
            config.read(config_path)
            if (kwargs.get('width_edit') is None or kwargs.get('weight_edit') is None or kwargs.get('height_edit') is None or kwargs.get('length_edit') is None ):
                json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=None,Width=None,Height=None,MXWeight=None,Shipment_type=None) 
            else:
                try:
                    Lenght = int((kwargs.get('length_edit')).displayText())
                    Width = int((kwargs.get('width_edit')).displayText()) 
                    Height = int((kwargs.get('height_edit')).displayText())
                except AttributeError:
                    Lenght = int((kwargs.get('length_edit')))
                    Width = int((kwargs.get('width_edit')))
                    Height = int((kwargs.get('height_edit')))
                try:
                    if kwargs['DBSelection']:
                        pass
                    else:
                        json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=Lenght,Width=Width,Height=Height,MXWeight=40,Shipment_type=kwargs.get('shipment_type'))
                except KeyError:
                    json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=Lenght,Width=Width,Height=Height,MXWeight=40,Shipment_type=kwargs.get('shipment_type'))
            json_path = mainfolder
            json_path += config['DEFAULT']['nome_json']
            checkForErrorPath = mainfolder
            checkForErrorPath += 'EPS_MODEL\\EPS_MODEL.exe'
            try:
                checkForError = (subprocess.check_output([checkForErrorPath, str(json_path)]))
            except UnboundLocalError as err:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Errore")
                msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nRiferire il codice sottostante agli sviluppatori per correggere l'errore.\n\nErrore: {0}\n".format(err.returncode))
                msg.setWindowTitle("Errore Critico")
                msg.exec_()
                exit(1)
            except Exception as err:
                if err.returncode == 10:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Errore")
                    msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nNessun pacco selezionato o i pacchi selezionati sono corrotti\n\nErrore: {0}\n".format(err.returncode))
                    msg.setWindowTitle("Errore Critico")
                    msg.exec_()
                    self.goBack()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Errore")
                    msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nRiferire il codice sottostante agli sviluppatori per correggere l'errore.\n\nErrore: {0}\n".format(err.returncode))
                    msg.setWindowTitle("Errore Critico")
                    msg.exec_()
                    exit(1)
            
            json_path = mainfolder
            json_path += 'output.json'
            with open(json_path) as json_file:
                data = json.load(json_file)
            if data['UnNestedPacks'] is not None:
                notNestet = ''
                for pacco in data['UnNestedPacks']:
                    notNestet += str(pacco)
                    notNestet += ','
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Attenzione")
                msg.setInformativeText("\nDurante la creazione del pallet alcuni pacchi non sono stati inseriti\n\nQuando dei pacchi non vengono inseriti nel pallet, vuol dire che il pallet è troppo piccolo o già pieno.\n\nPacchi non inseriti: {0}\n".format(notNestet))
                msg.setWindowTitle("Attenzione")
                msg.exec_()
            create_pdf(mainfolder,data)
            self.settings_window = SettingsWindow(csv_file_path=None)
            self.settings_window.show()
            self.close()

    def upload_bubble(self,single:bool, *args, **kwargs):
        print("Spedisce la bolla sul db")
        
    
    def changeUsrSettings(self, *args, **kwargs):
        self.usrSettings_window = UserSettings()
        self.usrSettings_window.show()
        self.close()
        
    def suicide(self):
        self.destroy()
        self.close()
        exit(0)
        
    def goBack(self):
        self.close()
        main_window.show()
        
class SettingsWindow(QDialog):
    def __init__(self, csv_file_path):
        super().__init__()  
        self.setWindowTitle('Menù Impostazioni')

        self.csv_file_path = csv_file_path
        global file_path
        if csv_file_path is not None:
            file_path = csv_file_path
        self.root = os.path.dirname(os.path.abspath(__file__))

        self.image_settings = {
            "type": "aereo",
            "Length": 800,
            "Width": 1200,
            "Height": 800,
            "MXWeight":40
        }


        layout = QHBoxLayout()       
        settings_groupbox = QGroupBox('Settings')

        form_layout = QFormLayout()

        type_combobox1 = QComboBox(self)
        type_combobox1.setObjectName('trasporto')
        type_combobox1.addItems(['Aereo', 'Treno', 'Nave', 'Furgone'])
        type_combobox1.setCurrentText(self.image_settings['type'])
        form_layout.addRow('Shipment Type:', type_combobox1)

        length_edit = QLineEdit(str(self.image_settings['Length']))
        form_layout.addRow('Length:', length_edit)
        length_edit.setObjectName('Length')

        width_edit = QLineEdit(str(self.image_settings['Width']))
        form_layout.addRow('Width:', width_edit)
        width_edit.setObjectName('Width')

        height_edit = QLineEdit(str(self.image_settings['Height']))
        form_layout.addRow('Height:', height_edit)
        height_edit.setObjectName('Height')

        weight_edit = QLineEdit(str(self.image_settings['MXWeight']))
        form_layout.addRow('Max Weight:', weight_edit)
        weight_edit.setObjectName('MXWeight')

        settings_groupbox.setLayout(form_layout)

        image_preview_groupbox = QGroupBox('PDF Preview')
        self.image_label = QLabel(self)
        self.update_image_preview()
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)
        image_preview_groupbox.setLayout(image_layout)
        layout.addWidget(settings_groupbox)
        layout.addWidget(image_preview_groupbox)

        self.setLayout(layout)

        apply_button = QPushButton('Rigenera il  PDF', self)
        apply_button.clicked.connect(lambda: main_window.show_settings_window(width_edit = width_edit,weight_edit = weight_edit,height_edit = height_edit,length_edit = length_edit,askForCSV = False,shipment_type=type_combobox1.currentText()))
        form_layout.addRow(apply_button)


        print_button = QPushButton('Stampa il documento e mostra anteprima', self)
        print_button.clicked.connect(main_window.printPDF)
        form_layout.addRow(print_button)

        writeDB_button = QPushButton('Carica la bolla nel DataBase', self)
        writeDB_button.clicked.connect(main_window.upload_bubble)
        form_layout.addRow(writeDB_button)
        
        kill_btn = QPushButton('Indietro',self)
        kill_btn.clicked.connect(self.goBack)
        kill_btn.setFixedSize(130,30)
        form_layout.addRow(kill_btn)
        

    def apply_settings_and_show_image(self):
        mainfolder = mainfolderFinder()
        config_path = ''
        config_path += mainfolder
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)

        try:
            self.image_settings['type'] = self.findChild(QComboBox, 'trasporto').currentText()
        except AttributeError as err:
            pass
        try:
            self.image_settings['Length'] = float(self.findChild(QLineEdit, 'Length').text())
        except AttributeError as err:
            pass
        try:
            self.image_settings['Width'] = float(self.findChild(QLineEdit, 'Width').text())
        except AttributeError as err:
            pass
        try:
            self.image_settings['Height'] = float(self.findChild(QLineEdit, 'Height').text())
        except AttributeError as err:
            pass
        try:
            self.image_settings['MXWeight'] = float(self.findChild(QLineEdit, 'MXWeight').text())
        except AttributeError as err:
            pass
        try:
            self.selezione_pallet = int((self.findChild(QComboBox, 'selezione_pallet')).currentText())
        except AttributeError as err:
            pass
        json_updater(Lenght=self.image_settings['Length'],Width=self.image_settings['Width'],Height=self.image_settings['Height'],MXWeight = self.image_settings['MXWeight'],json_path=config['DEFAULT']['nome_json'],Shipment_type=self.image_settings['type'])
        self.update_image_preview()

    def update_image_preview(self):
        pdf = (self.root).replace("\\","/")
        super().__init__()
        pdf += '/bolla.pdf'
        doc = fitz.open(pdf)
        for i, page in enumerate(doc):
            image = (self.root).replace("\\","/")
            pix = page.get_pixmap()
            image += "/bolla"
            image += str(i)
            image += ".png"
            pix.save(image)
        image = (self.root).replace("\\","/")
        image += "/bolla"
        image += str(0)
        image += ".png"
        self.im = QPixmap(image)
        self.label = QLabel()
        self.image_label.setPixmap(self.im)

    def goBack(self):
        self.close()
        main_window.show()


class palletSelection(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()  
        self.setWindowTitle('Selezione pallet da DataBase')
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 930
   
        self.setGeometry(self.left, self.top, self.width, self.height) 
   
        self.createTable(dbResult=args[0]) 
        self.layout = QVBoxLayout() 
        
        self.l2 = QLabel()
        self.l2.setText("Per selezionare più colonne tenere premuto il tasto Maiusc e allo stesso tempo selezionare le colonne con il mouse")
        self.l2.move(100,70)
        self.l2.setAlignment(Qt.AlignCenter)
        self.l3 = QLabel()
        self.l3.setText("La selezione a mano di colonne non consecutive verranno considerate consecutive ES[da 1 a 4 consecutive +6 verranno considetate come da 1 a 6]")
        self.l3.move(100,70)
        self.l3.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.l2)
        self.layout.addWidget(self.l3) 
        self.layout.addWidget(self.tableWidget) 

        self.backbutton = QPushButton('Indietro <-', self)
        self.backbutton.setToolTip('Avanti')
        self.backbutton.move(100,70)
        self.textbox = QLineEdit(self)
        self.backbutton.move(120,70)
        self.backbutton.clicked.connect(self.goBack)

        self.Okbutton = QPushButton('Avanti ->', self)
        self.Okbutton.setToolTip('Avanti')
        self.Okbutton.move(100,70)
        self.textbox = QLineEdit(self)
        self.Okbutton.move(120,70)
        self.Okbutton.clicked.connect(lambda: self.postQuery(self.tableWidget,self.textbox,args[0]))
        
        self.l1 = QLabel()
        self.l1.setText("Nel caso di selezione multipla non consecutiva, inserire a mano le celle desiderate, separate da ','")
        self.l1.move(100,70)
        self.l1.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.Okbutton)
        self.layout.addWidget(self.backbutton)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.textbox)
        
        self.setLayout(self.layout) 
        self.show() 
        
    def createTable(self,dbResult):
        self.tableWidget = QTableWidget() 
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(w)
        self.tableWidget.setRowCount(len(dbResult)+1)  
        self.tableWidget.setColumnCount(5) 
#****************CREAZIONE DELLA TABELLA DINAMICA**************************

        self.tableWidget.setItem(0,0, QTableWidgetItem("CODICE_PALLET"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("BASE_MAGGIORE")) 
        self.tableWidget.setItem(0,2, QTableWidgetItem("BASE_MINORE"))
        self.tableWidget.setItem(0,3, QTableWidgetItem("ALTEZZA"))
        self.tableWidget.setItem(0,4, QTableWidgetItem("N_PACCHI"))
        
        i = 1
        for row in dbResult:
            for elemento in dbResult[row]:
                if elemento is None:
                    indice = dbResult[row].index(elemento)
                    dbResult[row][indice] = 'None'
            self.tableWidget.setItem((int(i)),0, QTableWidgetItem(str(row)))
            self.tableWidget.setItem((int(i)),1, QTableWidgetItem(str((dbResult[row])[0]))) 
            self.tableWidget.setItem((int(i)),2, QTableWidgetItem(str((dbResult[row])[1]))) 
            self.tableWidget.setItem((int(i)),3, QTableWidgetItem(str((dbResult[row])[2]))) 
            self.tableWidget.setItem((int(i)),4, QTableWidgetItem(str((dbResult[row])[3]))) 
            i +=1
   
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def postQuery(self, *args, **kwargs):
        retDict = {}
        manSelectedRows = []
        mouseSelectedRows = []
        tabellaObj = args[0]
        textFieldObj = args[1]
        testoImmesso = (((((textFieldObj.text()).replace(' ',',').replace('-',',')).replace(':',',')).replace(';','')).split(sep = ','))
        for rigaSelezionata in testoImmesso:
            manSelectedRows.append(rigaSelezionata)
        retDict['selezioneSingola'] = manSelectedRows
        y = tabellaObj.selectedRanges()
        try:
            y = (y[0]).rowCount()
            x = (tabellaObj.currentRow()) + 1
            
            rangeStop = ((x-y)+1)
            rangeStart = (x)
            if rangeStop <-1:
                rangeStop = (rangeStop *-1) +2  
                rowRange = range(rangeStart,rangeStop +1)
            else:
                rowRange = range(rangeStop,rangeStart +1)
            for n in rowRange:
                mouseSelectedRows.append(n)
            retDict['selezioneMultipla'] = mouseSelectedRows
        except IndexError as err:
            pass
            
        colonneSelezionate ={}
        chiavi = []
        i = 0
        qryRes = args[2]
        for chiave in qryRes:
            chiavi.append(chiave)
        for chiave in retDict:
            for idx in retDict[chiave]:
                if idx == '':
                    pass
                else:
                    idx = int(idx)
                    colonneSelezionate[str(chiavi[i])] = qryRes[str(chiavi[i])]
                    i +=1
        self.close()
        
        query = '''SELECT *
        FROM `pacchi`
        WHERE pacchi.CODICE_PALLET IN ('''
        i = 0
        for codice_pallet_assegato in colonneSelezionate:
            query += str(codice_pallet_assegato)
            if i<((len(colonneSelezionate))-1):
                query +=','
            i+=1
        query += ')'
        config_path = mainfolderFinder()
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)        
        try:
            mydb = mysql.connector.connect(
            host= str(config.get('DB_SETTINGS','db_host')),
            user=str(config.get('DB_SETTINGS','db_username')),
            password=str(config.get('DB_SETTINGS','db_password')),
            database=str(config.get('DB_SETTINGS','db_name')),
            )
            buffer_json = {}
            mycursor = mydb.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            i = 1
            for collo in myresult:
                buffer = {}
                buffer_json[str(i)] = {}
                buffer['NUM_SPEDIZIONE'] = int(collo[3])
                buffer['NUMERO_COLLO'] = int(collo[1])
                buffer['CODICE_CLIENTE'] = int(collo[4])
                buffer['PESO_NETTO'] = str(collo[5])
                buffer['PESO_LORDO'] = str(collo[6])
                buffer['BASE_MAGGIORE'] = int(collo[7])
                buffer['BASE_MINORE'] = int(collo[8])
                buffer['ALTEZZA'] = int(collo[9])
                buffer['FLAG_PALETTIZZABILE'] = str(collo[10])
                buffer['FLAG_SOVRAPPONIBILE'] = str(collo[11])
                buffer['FLAG_RUOTABILE'] = str(collo[12])
                buffer_json[str(i)] = copy.deepcopy(buffer)
                i+=1
            buffer_json["user_settings"] = {
            "Shipment_type": "Aereo",
            "Lenght": 800,
            "Width": 1200,
            "Height": 800,
            "Max Weight": 40
        }
            jsonPath = os.getcwd()
            jsonPath += '\\EPS_MODEL\\input_for_model.json'
            with open(jsonPath,'w') as j:
                json.dump(buffer_json, j, indent = 4)
            main_window.show_settings_window(askForCSV = False,width_edit = 1200, weight_edit = 40, height_edit = 800, length_edit = 800,shipment_type = 'Aereo',DBSelection = True)
            print()
                
        except mysql.connector.errors.DatabaseError as err:
            if err.errno == 1064:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Errore")
                msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nNessun pacco selezionato o i pacchi selezionati sono corrotti\n\n")
                msg.setWindowTitle("Errore Critico")
                msg.exec_()
                self.kill()
            else: 
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Errore durante il collegamento al DB")
                msg.setInformativeText("\nSi è verificata un'eccezione durante il collegamento al database\n\nControllare che l'indirizzo del DataBase sia corretto e che sia raggiungibile\n")
                msg.setWindowTitle("Errore durante il collegamento al DB")
                msg.exec_()

        
    def goBack(self):
        self.close()
        main_window.show()
    
    def kill(self):
        self.close()
        exit(0)


class databasePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()  
        self.setWindowTitle('Selezione colli da DataBase')
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 930
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.createTable(dbResult=args[0]) 
        self.layout = QVBoxLayout() 
        self.l2 = QLabel()
        self.l2.setText("Per selezionare più colonne tenere premuto il tasto Maiusc e allo stesso tempo selezionare le colonne con il mouse")
        self.l2.move(100,70)
        self.l2.setAlignment(Qt.AlignCenter)
        self.l3 = QLabel()
        self.l3.setText("La selezione a mano di colonne non consecutive verranno considerate consecutive ES[da 1 a 4 consecutive +6 verranno considetate come da 1 a 6]")
        self.l3.move(100,70)
        self.l3.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.l2)
        self.layout.addWidget(self.l3) 
        self.layout.addWidget(self.tableWidget) 

        self.backbutton = QPushButton('Indietro <-', self)
        self.backbutton.setToolTip('Avanti')
        self.backbutton.move(100,70)
        self.textbox = QLineEdit(self)
        self.backbutton.move(120,70)
        self.backbutton.clicked.connect(self.goBack)

        self.Okbutton = QPushButton('Avanti ->', self)
        self.Okbutton.setToolTip('Avanti')
        self.Okbutton.move(100,70)
        self.textbox = QLineEdit(self)
        self.Okbutton.move(120,70)
        self.Okbutton.clicked.connect(lambda: self.postSelezione(self.tableWidget,self.textbox,args[0]))
        self.l1 = QLabel()
        self.l1.setText("Nel caso di selezione multipla non consecutiva, inserire a mano le celle desiderate, separate da ','")
        self.l1.move(100,70)
        self.l1.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.backbutton)
        self.layout.addWidget(self.Okbutton)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.textbox)
        
        self.setLayout(self.layout) 
        self.show() 
   
    def createTable(self,dbResult): 
        self.tableWidget = QTableWidget() 
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(w)
        self.tableWidget.setRowCount(len(dbResult))  
        self.tableWidget.setColumnCount(12)           
        
        self.tableWidget.setItem(0,0, QTableWidgetItem("ID_PACCO"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("CODICE_PALLET")) 
        self.tableWidget.setItem(0,2, QTableWidgetItem("NUMERO_SPEDIZIONE")) 
        self.tableWidget.setItem(0,3, QTableWidgetItem("CODICE_CLIENTE")) 
        self.tableWidget.setItem(0,4, QTableWidgetItem("PESO_NETTO")) 
        self.tableWidget.setItem(0,5, QTableWidgetItem("PESO_LORDO")) 
        self.tableWidget.setItem(0,6, QTableWidgetItem("BASE_MAGGIORE"))
        self.tableWidget.setItem(0,7, QTableWidgetItem("BASE_MINORE"))
        self.tableWidget.setItem(0,8, QTableWidgetItem("ALTEZZA"))
        self.tableWidget.setItem(0,9, QTableWidgetItem("FLAG_PALLETTIZZABILE"))
        self.tableWidget.setItem(0,10, QTableWidgetItem("FLAG_SOVRAPPONIBILE"))
        self.tableWidget.setItem(0,11, QTableWidgetItem("FLAG_RUOTABILE"))
        
        for row in dbResult:
            self.tableWidget.setItem((int(row)),0, QTableWidgetItem(str(dbResult[row][0])))
            self.tableWidget.setItem((int(row)),1, QTableWidgetItem(str((dbResult[row])[1]))) 
            self.tableWidget.setItem((int(row)),2, QTableWidgetItem(str((dbResult[row])[2]))) 
            self.tableWidget.setItem((int(row)),3, QTableWidgetItem(str((dbResult[row])[3]))) 
            self.tableWidget.setItem((int(row)),4, QTableWidgetItem(str((dbResult[row])[4]))) 
            self.tableWidget.setItem((int(row)),5, QTableWidgetItem(str((dbResult[row])[5]))) 
            self.tableWidget.setItem((int(row)),6, QTableWidgetItem(str((dbResult[row])[6]))) 
            self.tableWidget.setItem((int(row)),7, QTableWidgetItem(str((dbResult[row])[7]))) 
            self.tableWidget.setItem((int(row)),8, QTableWidgetItem(str((dbResult[row])[8]))) 
            self.tableWidget.setItem((int(row)),9, QTableWidgetItem(str((dbResult[row])[9]))) 
            self.tableWidget.setItem((int(row)),10, QTableWidgetItem(str((dbResult[row])[10])))
            self.tableWidget.setItem((int(row)),11, QTableWidgetItem(str((dbResult[row])[11])))
   
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def postSelezione(self, *args, **kwargs):
        retDict = {}
        manSelectedRows = []
        mouseSelectedRows = []
        tabellaObj = args[0]
        textFieldObj = args[1]
        testoImmesso = (((((textFieldObj.text()).replace(' ',',').replace('-',',')).replace(':',',')).replace(';','')).split(sep = ','))
        for rigaSelezionata in testoImmesso:
            manSelectedRows.append(rigaSelezionata)
        retDict['selezioneSingola'] = manSelectedRows
        y = tabellaObj.selectedRanges()
        try:
            y = (y[0]).rowCount()
            x = (tabellaObj.currentRow()) + 1
            
            rangeStop = ((x-y)+1)
            rangeStart = (x)
            if rangeStop <-1:
                rangeStop = (rangeStop *-1) +2  
                rowRange = range(rangeStart,rangeStop +1)
            else:
                rowRange = range(rangeStop,rangeStart +1)
            for n in rowRange:
                mouseSelectedRows.append(n)
            retDict['selezioneMultipla'] = mouseSelectedRows
        except IndexError as err:
            pass
            
        colonneSelezionate ={}
        qryRes = args[2]
        for chiave in retDict:
            for idx in retDict[chiave]:
                if idx == '':
                    pass
                else:
                    idx = int(idx)
                    colonneSelezionate[str(idx-1)] = qryRes[str(idx-1)]
        if len(colonneSelezionate) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Errore")
            msg.setInformativeText("\nDurante l'esecuzione dell'algoritmo di nesting si è verificata un'eccezione\n\nNessun pacco selezionato o i pacchi selezionati sono corrotti\n\n")
            msg.setWindowTitle("Errore Critico")
            msg.exec_()
            self.kill()
        self.close()
        json_payload = {}
        for chiave in colonneSelezionate:
            buffer = {}
            json_payload[str(chiave)] = {}
            buffer['NUM_SPEDIZIONE'] = colonneSelezionate[str(chiave)][2]
            buffer['NUMERO_COLLO'] = colonneSelezionate[str(chiave)][0]
            buffer['CODICE_CLIENTE'] = colonneSelezionate[str(chiave)][3]
            buffer['PESO_NETTO'] = colonneSelezionate[str(chiave)][4]
            buffer['PESO_LORDO'] = colonneSelezionate[str(chiave)][5]
            buffer['BASE_MAGGIORE'] = colonneSelezionate[str(chiave)][6]
            buffer['BASE_MINORE'] = colonneSelezionate[str(chiave)][7]
            buffer['ALTEZZA'] = colonneSelezionate[str(chiave)][8]
            buffer['FLAG_PALETTIZZABILE'] = colonneSelezionate[str(chiave)][9]
            buffer['FLAG_SOVRAPPONIBILE'] = colonneSelezionate[str(chiave)][10]
            buffer['FLAG_RUOTABILE'] = colonneSelezionate[str(chiave)][11]
            json_payload[str(chiave)] = copy.deepcopy(buffer)
        json_payload["user_settings"] = {
        "Shipment_type": "Aereo",
        "Lenght": 800,
        "Width": 1200,
        "Height": 800,
        "Max Weight": 40
    }
        jsonPath = os.getcwd()
        jsonPath += '\\EPS_MODEL\\input_for_model.json'
        with open(jsonPath,'w') as j:
            json.dump(json_payload, j, indent = 4)
        main_window.show_settings_window(askForCSV = False,width_edit = 1200, weight_edit = 40, height_edit = 800, length_edit = 800,shipment_type = 'Aereo',DBSelection = True)
        
    def goBack(self):
        self.close()
        main_window.show()    
    
    def kill(self):
        self.close()
        exit(0)
        
class UserSettings(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()  
        self.setWindowTitle('Impostazioni Utente')
        self.setGeometry(100,100,320,210)

        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 930
        self.layout = QVBoxLayout() 
        
        self.l1 = QLabel()
        self.l1.setText("Nome e Cognome del Cliente")
        self.l1.move(100,70)
        self.l1.setAlignment(Qt.AlignTop)
        
        self.l2 = QLabel()
        self.l2.setText("Via del Cliente")
        self.l2.move(100,70)
        self.l2.setAlignment(Qt.AlignTop)
        
        self.l3 = QLabel()
        self.l3.setText("Città di residenza del Cliente")
        self.l3.move(100,70)
        self.l3.setAlignment(Qt.AlignTop)
        
        self.l4 = QLabel()
        self.l4.setText("Nazione di residenza del Cliente")
        self.l4.move(100,70)
        self.l4.setAlignment(Qt.AlignTop)
        
        self.l5 = QLabel()
        self.l5.setText("CAP di residenza del Cliente")
        self.l5.move(100,70)
        self.l5.setAlignment(Qt.AlignTop)
        
        
        self.Okbutton = QPushButton('Applica', self)
        self.Okbutton.setToolTip('Applica')
        self.Okbutton.move(100,70)
        self.Okbutton.clicked.connect(lambda: self.apply(apply = True,nome = self.nome,via = self.via,citta = self.citta, nazione = self.naz, cap = self.cap))
        
        self.Nobutton = QPushButton('Annulla', self)
        self.Nobutton.setToolTip('Annulla')
        self.Nobutton.clicked.connect(lambda: self.apply(apply = False))
        self.Nobutton.move(100,70)
        
        
        self.nome = QLineEdit(self)
        self.nome.resize(400,75)
        self.layout.addWidget(self.nome)
        self.layout.addWidget(self.l1)
        
        self.via = QLineEdit(self)
        self.via.resize(400,75)
        self.layout.addWidget(self.via)
        self.layout.addWidget(self.l2)
        
        self.citta = QLineEdit(self)
        self.citta.resize(400,75)
        self.layout.addWidget(self.citta)
        self.layout.addWidget(self.l3)
        
        self.naz = QLineEdit(self)
        self.naz.resize(400,75)
        self.layout.addWidget(self.naz)
        self.layout.addWidget(self.l4)
        
        self.cap = QLineEdit(self)
        self.cap.resize(400,75)
        self.layout.addWidget(self.cap)
        self.layout.addWidget(self.l5)
                
        self.layout.addWidget(self.Okbutton)
        self.layout.addWidget(self.Nobutton)
        
        self.setLayout(self.layout) 
        self.show()
        
    def apply(self, *args, **kwargs):
        config_path = mainfolderFinder()
        config_path += 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        
        if kwargs['apply'] is True:
            nome = kwargs['nome'].text()
            via = kwargs['via'].text()
            citta = kwargs['citta'].text()
            nazione = kwargs['nazione'].text()
            cap = kwargs['cap'].text()
            
            config.set('RECAPITI','nome',str(nome))
            config.set('RECAPITI','via',str(via))
            config.set('RECAPITI','citta',str(citta))
            config.set('RECAPITI','nazione',str(nazione))
            config.set('RECAPITI','cap',str(cap))
            config.write(open(config_path, "w"))
            
            msg = QMessageBox()
            msg.setWindowTitle("Impostazioni Applicate")
            msg.setText("Impostazioni applicate correttamente")
            x = msg.exec_()
            self.close()
            main_window.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Impostazioni non Applicate")
            msg.setText("Impostazioni non applicate")
            x = msg.exec_()
            self.close()
            main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    
