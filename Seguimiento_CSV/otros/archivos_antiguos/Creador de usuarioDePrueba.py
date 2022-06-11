#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
from appJar import gui
from screeninfo import get_monitors
import datetime
import zipfile
from tempfile import NamedTemporaryFile
import csv
import os
import io
import time
import json
import openpyxl
import string  
import ftplib
import pysftp
#import pyexcel as p

import xml.etree.ElementTree as ET

#CodigosLocales
import clasesyvariables
from clasesyvariables import usuario
from clasesyvariables import pregunta
from clasesyvariables import subpreguntaencuesta
from clasesyvariables import ora
clasesyvariables.init()

import funcionesjson
from funcionesjson import createJsonUsuario
import funcionescsv
import funcionesplanilla



#Variables para Static
myHostname = "sumaysigue.cmm.uchile.cl"
myUsername = "edustatic"
myPassword = "qD7pcVQF"
puerto = 2837 
#listaoras = []

class WindowsGui():
    def __init__(self, nameOfGui):
        self.app = gui(nameOfGui, "600x300")
    
    def Start(self):
        self.Prepare()
        self.app.go()

    def sizeOfWindow(self):
        self.app.setBg('#b4cbdc')
        self.app.setResizable(canResize=False)
        m = get_monitors()
        #self.app.setLocation(m[0].width * (0.6), m[0].height * (0.2))
        self.app.setPadX(5)
        #self.app.setIcon('ind.ico')

    def SubmitCSVFile(self, btnName):
        print("Subir file")
        dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
        print(dirFile)
        self.app.setLabel("FileCSV", dirFile)

    def SubmitORAFile(self, btnName):
        print("Subir file")
        dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
        print(dirFile)
        self.app.setLabel("FileORA", dirFile)


class StartApp(WindowsGui):

    def __init__(self, nameOfGui):
        self.app = gui(str(nameOfGui))

    def PorPersona(self, btnName):  # Obtener datos por sujeto

        nombreUsuarioPrueba =  self.app.getEntry("name")
        print ("Nombre del usuario de prueba " + nombreUsuarioPrueba)
        if(nombreUsuarioPrueba == ""):
            nombreUsuarioPrueba = "UsuarioPruebaCMMEDU" 
        codigocurso =  self.app.getEntry("code")
        print("Codigo del curso " + codigocurso)

        #listanegra = []
        ListaPregutnasEncuestas = []
        nombresEncuestas =[]
        orafile = self.app.getLabel("FileORA")
        clasesyvariables.listaoras = funcionescsv.crearListaOra(orafile)

        print("Recorrer CVS")
        #time.sleep(3)

        usr = usuario()
        usr.username = nombreUsuarioPrueba
        usr.usuarioprueba = True
        usr.nombre = "Usuario"
        usr.ApellidoM = "CMMEdu"
        usr.ApellidoP = "Prueba"

        clasesyvariables.usuarios.append(usr)

        File = self.app.getLabel("FileCSV")
        funcionescsv.RecorrerCSV( File, clasesyvariables.usuarios, clasesyvariables.listaoras )
      
        
        print ("Total contestadas " +  str(usr.totalContestadas) + " ConTaller: " + str(usr.totalConTaller) )
        print ("Total preguntas por taller"  +str(usr.totalPreguntasPorTaller))
        print ("Total preguntas evaluables por taller" + str(usr.totalPreguntasBuenasOMalasPorTaller))
        print ("Total preguntas correctas por taller " + str(usr.totalPreguntasCorrectasPorTaller))
        print ("Total preguntas pre test " + str(usr.totalpretest))
        print ("Total preguntas post test " + str(usr.totalpostest))
        print ("Nombres de encuesta " + str(usr.nombresEncuestas))
        print ("Nombres Asistencias " + str(usr.nombresAsistencias))

        jsonfile = funcionesjson.createJsonUsuario( usr,codigocurso ) #Crear achivo Json

        subir =  self.app.getCheckBox("Subir a servidor")
        if(subir):
            print ("subir " + str(codigocurso) + " al serivdor")
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None 

            with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword , port= puerto, cnopts= cnopts) as sftp:
                print ("Estamos en static ... ")
                print (str (sftp))

                subirDir = "/usr/share/nginx/static.sumaysigue.uchile.cl/Usuarios Prueba/" + "UsuarioPrueba_" + codigocurso + ".json"

                print ("Subir "+ jsonfile  + " en " + subirDir)

                sftp.put(jsonfile, subirDir)

        print ("TERMINADO")


    # Build the GUIs
    def Prepare(self):

        self.sizeOfWindow()

        self.app.addLabel("code", "Codigo de curso", 1, 0)
        self.app.setLabelAlign("code", "left")
        self.app.addEntry("code", 1, 1)
        self.app.setEntryAlign("code", "left")

        self.app.addLabel("name", "Nombre de usuario de prueba", 2, 0)
        self.app.setLabelAlign("name", "left")
        self.app.addEntry("name", 2, 1)
        self.app.setEntryDefault("name", "UsuarioPruebaCMMEDU")
        self.app.setEntryAlign("name", "left")

        self.app.addLabel("FileCSVTag", "Archivo CSV", 3, 0)
        self.app.setLabelAlign("FileCSVTag", "left")
        self.app.addLabel("FileCSV", "", 3, 1)
        self.app.setLabelAlign("FileCSV", "left")
        self.app.setLabelWidth("FileCSV", 40)
        self.app.setLabelBg('FileCSV', 'white')
        self.app.addNamedButton("Abrir archivo CSV",'SaveCSVFile', self.SubmitCSVFile, 3, 2)
        self.app.setButtonSticky('SaveCSVFile', 'right')

        self.app.addLabel("FileORATag", "Archivo ORA", 4, 0)
        self.app.setLabelAlign("FileORATag", "left")
        self.app.addLabel("FileORA", "", 4, 1)
        self.app.setLabelAlign("FileORA", "left")
        self.app.setLabelWidth("FileORA", 40)
        self.app.setLabelBg('FileORA', 'white')
        self.app.addNamedButton("Abrir archivo ORA",'SaveORAFile', self.SubmitORAFile, 4, 2)
        self.app.setButtonSticky('SaveORAFile', 'right')
        self.app.addCheckBox("Subir a servidor",5,1)

        self.app.addNamedButton("Crear Usuario de prueba", 'PorPersona', self.PorPersona, 6, 2)
        self.app.setButtonSticky('PorPersona', 'right')


if __name__ == '__main__':
    
    App = StartApp("Creador usuario de pruebas")
    App.Start()



