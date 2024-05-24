import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QDialog, QFormLayout, QLabel, QComboBox, QLineEdit, QHBoxLayout, QGroupBox, QSizePolicy, QHeaderView, QTableWidgetItem,QTableWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView
from PyQt5 import QtPrintSupport,QtWidgets
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

def json_updater(json_path,Lenght,Width,Height,MXWeight,Shipment_type):
    if Lenght is None or Width is None or Height is None: # or Shipment_type is None 
        print('Valori utente non caricati\nDefault Lenght : 120\nWidth : 120\nHeight : 120\nMxWeight : 20\n')
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
        print('Valori utente caricati\nLenght : {0}\nWidth : {1}\nHeight : {2}\nMax Weight : {3}'.format(Lenght,Width,Height,MXWeight))
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
    n_p=0
    try:
        html_path = mainfolder
        html_path += 'template_bolla.html'
        or_html = mainfolder
        or_html += 'default'
        json_path = mainfolder
        json_path += '\EPS_MODEL\input_for_model.json'
        my_data = load_json(json_path)
        for pallet in (data['Pallets']):
            i=0
            for pacco in pallet['Packs']:
                idx = str(n_p)
                idx += '_'
                idx += str(i)
                temp_pallet[idx] = pacco
                try:
                    built_pallets[idx] = my_data[str(pacco-1)]
                except Exception:
                    if firstRound is True:
                        for chiave in my_data:
                            if chiave == 'user_settings':
                                pass
                            else:
                                chiavi.append(int(chiave))
                    firstRound = False
                    built_pallets[idx] = my_data[str(chiavi[i])]
                i=i+1
            n_p = n_p+1

        with open(or_html, 'r') as h: #RESET DEL FILE HTML
            orBuff = h.readlines()    #RESET DEL FILE HTML
        with open(html_path, 'w') as h:#RESET DEL FILE HTML
            h.writelines(orBuff)      #RESET DEL FILE HTML

        with open(html_path, 'r') as h:
            buffer = h.readlines()
        strt_line = []
        for linea in buffer:
            if "tabella_dinamica" in linea:
                print("Da ",buffer.index(linea))
                strt_line.append(buffer.index(linea))
                if "'id=\"end_of_tabella_dinamica\">'" in linea:
                    print("A: ",buffer.index(linea))
                    tt_lines = strt_line[0] - strt_line[1]
                    break
        tt_lines = strt_line[1] - strt_line[0]
        for pallet in built_pallets:
            i=0
            idx = tt_lines -2
            k = strt_line[1]
            stringhe = []
            stringhe.append('''<tr id="colonna_dinamica">\n''')
            stringhe.append('''<th scope="row" style="font-family:\'Serif\'">{0}</th>\n'''.format(str(pallet)))
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(built_pallets[str(pallet)]['NUMERO_COLLO']))
            dimensioni = str(built_pallets[str(pallet)]['BASE_MAGGIORE'])
            dimensioni += 'x'
            dimensioni += str(built_pallets[str(pallet)]['BASE_MINORE'])
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(dimensioni))
            fr = built_pallets[str(pallet)]['FLAG_RUOTABILE']
            if fr == '':
                fr = 'No'
            else:
                fr = 'Yes'
            stringhe.append('''<td style="font-family:\'Serif\'">{0}</td>\n'''.format(fr))   
            fs = built_pallets[str(pallet)]['FLAG_SOVRAPPONIBILE']
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

        with open(html_path,'w') as h:
            h.writelines(buffer)

        template_loader = jinja2.FileSystemLoader(mainfolder)
        template_env = jinja2.Environment(loader=template_loader)
        bollaPathOut = mainfolder
        bollaPathOut += 'bolla.pdf'
        cssPath = mainfolder
        cssPath += 'Bootstrap\\bootstrap-5.0.2-dist\\css\\bootstrap.css'
        template = template_env.get_template('template_bolla.html')
        dt_naive = datetime.now()
        context={"nome_cliente":"Mario Rossi","via_cliente": "Via Aldo Moro 24","citt_cliente":"Bologna","naz_cliente":"Italia","cap_cliente":36069,"plt_idx":1,"art_cdx":2,"dim":"24x60 Cm","RT_flag":True,"SV_flag":False,"n_delivery":4,"date_of_delivery":dt_naive.strftime("%d/%m/%Y %H:%M"),"shipm_type":my_data['user_settings']['Shipment_type']}
        output_text = template.render(context)
        options={"enable-local-file-access": ""}
        wkhtmltopdf = mainfolder
        wkhtmltopdf += 'wkhtmltox\\bin\\wkhtmltopdf.exe'
        pdfConfig = pdfkit.configuration(wkhtmltopdf= wkhtmltopdf)
        pdfkit.from_string(output_text,options=options, output_path=bollaPathOut, configuration=pdfConfig,css=cssPath)
    except Exception as err:
        print(err)

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_image(rectangles, plane_dimensions):
    print("bypasscreate_image")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Menù Principale')
        self.setGeometry(100, 100, 320, 210)

        upload_button = QPushButton('Recupera collo da CSV', self)
        upload_button.clicked.connect(self.show_settings_window)
        upload_button.setFixedSize(320, 70)

        seatchDB_button = QPushButton('Recupera collo da DataBase', self)
        seatchDB_button.clicked.connect(self.show_DB_window)
        seatchDB_button.setFixedSize(320, 70)

        seatchPLT_DB_button = QPushButton('Recupera pallet da DataBase', self)
        seatchPLT_DB_button.clicked.connect(self.show_DB_window)
        seatchPLT_DB_button.setFixedSize(320, 70)

        layout = QVBoxLayout()
        layout.addWidget(upload_button)
        layout.addWidget(seatchDB_button)
        layout.addWidget(seatchPLT_DB_button)

        self.setLayout(layout)
        

    def show_DB_window(self):
        try:
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eps"
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
                mainfolder = ''
                config_path = ''
                mainfolder_buff=__file__
                mainfolder_buff = mainfolder_buff.split(sep='\\')
                mainfolder_buff.pop(-1)
                for name in mainfolder_buff:
                    mainfolder += name
                    mainfolder += '\\' 
                config_path += mainfolder
                config_path += 'config.ini'
                config = configparser.ConfigParser()
                config.read(config_path)
                #BISOGNA FARE LA SELEZIONE DA DATABASE E QUI CARICARE I DATI CHE NORMALMENTE SI SAREBBERO PRESI DAL CSV
                uscita= pd.read_csv(file_path, delimiter=";",usecols=["NUM_SPEDIZIONE","NUMERO_COLLO","CODICE_CLIENTE","PESO_NETTO","PESO_LORDO","BASE_MAGGIORE","BASE_MINORE","ALTEZZA","FLAG_PALETTIZZABILE","FLAG_SOVRAPPONIBILE","FLAG_RUOTABILE"])
                uscita= uscita.fillna("")
                uscita.to_json(config['DEFAULT']['nome_json'],orient='index', indent=4)
            if (kwargs.get('width_edit') is None or kwargs.get('weight_edit') is None or kwargs.get('height_edit') is None or kwargs.get('length_edit') is None ):
                try:
                    json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=None,Width=None,Height=None,MXWeight=None,Shipment_type=None) #bisogna inserire qua i parametri richiesti sulla funziona main 
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
            mainfolder = ''
            config_path = ''
            mainfolder_buff=__file__
            mainfolder_buff = mainfolder_buff.split(sep='\\')
            mainfolder_buff.pop(-1)
            for name in mainfolder_buff:
                mainfolder += name
                mainfolder += '\\' 
            config_path += mainfolder
            config_path += 'config.ini'
            config = configparser.ConfigParser()
            config.read(config_path)
            json_path = mainfolder
            json_path += config['DEFAULT']['nome_json']
            checkForErrorPath = mainfolder
            checkForErrorPath += 'EPS_MODEL\\EPS_MODEL.exe'
            print("directory output.json: {0}".format(json_path))
            try:
                checkForError = (subprocess.check_output([checkForErrorPath, str(json_path)]))
            except Exception as err:
                print("Programma terminato con codice diverso da 0 \nCode: {0}".format(checkForError))
                exit(1)
            
            json_path = mainfolder
            json_path += 'output.json'
            with open(json_path) as json_file:
                data = json.load(json_file)
            print("\nOutput ESP_MODEL.exe: {0}\n".format(data))
            create_pdf(mainfolder,data)
            self.settings_window = SettingsWindow(file_path)
            self.settings_window.show()
            self.close()
        else:
            #test = kwargs.get('length_edit')
            mainfolder = ''
            config_path = ''
            mainfolder_buff=__file__
            mainfolder_buff = mainfolder_buff.split(sep='\\')
            mainfolder_buff.pop(-1)
            for name in mainfolder_buff:
                mainfolder += name
                mainfolder += '\\' 
            config_path += mainfolder
            config_path += 'config.ini'
            config = configparser.ConfigParser()
            config.read(config_path)
            if (kwargs.get('width_edit') is None or kwargs.get('weight_edit') is None or kwargs.get('height_edit') is None or kwargs.get('length_edit') is None ):
                json_updater(json_path=config['DEFAULT']['nome_json'],Lenght=None,Width=None,Height=None,MXWeight=None,Shipment_type=None) #bisogna inserire qua i parametri richiesti sulla funziona main 
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
            print("path output.json {0}".format(json_path))
            try:
                checkForError = (subprocess.check_output([checkForErrorPath, str(json_path)]))
            except Exception as err:
                print("Programma terminato con codice diverso da 0 \nCode: {0}".format(checkForError))
                exit(1)
            
            json_path = mainfolder
            json_path += 'output.json'
            with open(json_path) as json_file:
                data = json.load(json_file)
            print("\nOutput ESP_MODEL.exe: {0}\n".format(data))
            create_pdf(mainfolder,data)
            self.settings_window = SettingsWindow(csv_file_path=None)
            self.settings_window.show()
            self.close()

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

        self.setWindowTitle('Impostazioni')

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

        
        type_combobox2 = QComboBox(self)
        type_combobox2.addItems(['1', '2', '3'])
        type_combobox2.setObjectName('selezione_pallet')
        form_layout.addRow('Numero Pallet massimo:', type_combobox2)
        if isinstance(type_combobox2.currentText(), str) == True:
            self.selezione_pallet = int(type_combobox2.currentText())
            if (type_combobox2.currentIndex()) is None:
                pass
            else:
                pass

            pass
        else:
            print("no")

        settings_groupbox.setLayout(form_layout)

        # Image Preview
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
        print_button.clicked.connect(main_window.printPDF)#DEVE CHIAMARE LA FUNZIONE DI STAMPA DI SISTEMA
        form_layout.addRow(print_button)

        writeDB_button = QPushButton('Carica la bolla nel DataBase', self)
        writeDB_button.clicked.connect(main_window.show_DB_window)#Effettua un insert al database di bitchesgoes
        form_layout.addRow(writeDB_button)
        


    def apply_settings_and_show_image(self):
        mainfolder = ''
        config_path = ''
        mainfolder_buff=__file__
        mainfolder_buff = mainfolder_buff.split(sep='\\')
        mainfolder_buff.pop(-1)
        for name in mainfolder_buff:
            mainfolder += name
            mainfolder += '\\' 
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
       #("/images_output/output_image{0}.png".format(self.selezione_pallet))
        pdf += '/bolla.pdf'
        doc = fitz.open(pdf)
        for i, page in enumerate(doc):
            image = (self.root).replace("\\","/")
            pix = page.get_pixmap()  # render page to an image
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


class databasePage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()  
        self.setWindowTitle('Selezione da DataBase')

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
        
        self.layout.addWidget(self.Okbutton)
        self.layout.addWidget(self.l1)
        self.layout.addWidget(self.textbox)
        
        self.setLayout(self.layout) 
        #Show window 
        self.show() 
   
    #Create table 
    def createTable(self,dbResult): 
        self.tableWidget = QTableWidget() 
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(w)
        self.tableWidget.setRowCount(len(dbResult))  
        self.tableWidget.setColumnCount(11)           
        
        self.tableWidget.setItem(0,0, QTableWidgetItem("NUMERO_COLLO")) #corrisponde a ID_PACCO chiave univoca
        self.tableWidget.setItem(0,1, QTableWidgetItem("NUM_SPEDIZIONE")) 
        self.tableWidget.setItem(0,2, QTableWidgetItem("CODICE_CLIENTE")) 
        self.tableWidget.setItem(0,3, QTableWidgetItem("PESO_NETTO")) 
        self.tableWidget.setItem(0,4, QTableWidgetItem("PESO_LORDO")) 
        self.tableWidget.setItem(0,5, QTableWidgetItem("BASE_MAGGIORE")) 
        self.tableWidget.setItem(0,6, QTableWidgetItem("BASE_MINORE"))
        self.tableWidget.setItem(0,7, QTableWidgetItem("ALTEZZA"))
        self.tableWidget.setItem(0,8, QTableWidgetItem("FLAG_PALETTIZZABILE"))
        self.tableWidget.setItem(0,9, QTableWidgetItem("FLAG_SOVRAPPONIBILE"))
        self.tableWidget.setItem(0,10, QTableWidgetItem("FLAG_RUOTABILE"))
        
        for row in dbResult:
            self.tableWidget.setItem((int(row)),0, QTableWidgetItem(str(row)))
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
   
        #Table will fit the screen horizontally 
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def postSelezione(self, *args, **kwargs):
        retDict = {}
        manSelectedRows = []
        mouseSelectedRows = []
        tabellaObj = args[0]
        #totalRowCount = tabellaObj.selectedItems()
        #for row in totalRowCount:                    #TROVARE LE COLONNE SELEZIONATE
        #    print(row.isSelected())
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
        print("Risultato: ",retDict)
        for chiave in retDict:
            for idx in retDict[chiave]:
                if idx == '':
                    pass
                else:
                    colonneSelezionate[str(idx)] = qryRes[str(idx-1)]
        self.close()
        json_payload = {}
        for chiave in colonneSelezionate:
            buffer = {}
            json_payload[str(chiave)] = {}
            buffer['NUM_SPEDIZIONE'] = colonneSelezionate[str(chiave)][1]
            buffer['NUM_SPEDIZIONE'] = colonneSelezionate[str(chiave)][1]
            buffer['NUMERO_COLLO'] = colonneSelezionate[str(chiave)][0]
            buffer['CODICE_CLIENTE'] = colonneSelezionate[str(chiave)][2]
            buffer['PESO_NETTO'] = colonneSelezionate[str(chiave)][3]
            buffer['PESO_LORDO'] = colonneSelezionate[str(chiave)][4]
            buffer['BASE_MAGGIORE'] = colonneSelezionate[str(chiave)][5]
            buffer['BASE_MINORE'] = colonneSelezionate[str(chiave)][6]
            buffer['ALTEZZA'] = colonneSelezionate[str(chiave)][7]
            buffer['FLAG_PALETTIZZABILE'] = colonneSelezionate[str(chiave)][8]
            buffer['FLAG_SOVRAPPONIBILE'] = colonneSelezionate[str(chiave)][9]
            buffer['FLAG_RUOTABILE'] = colonneSelezionate[str(chiave)][10]
            json_payload[str(chiave)] = copy.deepcopy(buffer)
        #"0": {
        #"NUM_SPEDIZIONE": 17362,
        #"NUMERO_COLLO": 1,
        #"CODICE_CLIENTE": 2,
        #"PESO_NETTO": "40,7",
        #"PESO_LORDO": "48,7",
        #"BASE_MAGGIORE": 72,
        #"BASE_MINORE": 61,
        #"ALTEZZA": 44,
        #"FLAG_PALETTIZZABILE": "",
        #"FLAG_SOVRAPPONIBILE": "",
        #"FLAG_RUOTABILE": "N"
        #},
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
        main_window.show_settings_window(askForCSV = False,width_edit = 1200, weight_edit = 40, height_edit = 800, length_edit = 800,shipment_type = 'Aereo',DBSelection = True) #bisogna collegare la funzione che riscagazza i dati alla pagina post selezione csv
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
