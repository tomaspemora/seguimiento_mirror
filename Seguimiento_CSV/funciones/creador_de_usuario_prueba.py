#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys


import datetime
import zipfile

import csv
import os
import io
import time
import json
import openpyxl
import string  
import ftplib
import pysftp
#CodigosLocales

from . import clasesyvariables
from .clasesyvariables import usuario
from .clasesyvariables import pregunta
from .clasesyvariables import subpreguntaencuesta
from .clasesyvariables import ora

from . import funcionesjson
from .funcionesjson import createJsonUsuario
from . import funcionescsv


#Variables para Static
myHostname = "sumaysigue.cmm.uchile.cl"
myUsername = "edustatic"
myPassword = "qD7pcVQF"
puerto = 2837 
#listaoras = []

def UsuarioPrueba(orafile,csvfile,subir,codigocurso,id_string,ora_file_io=None):  # Obtener datos por sujeto


    nombreUsuarioPrueba = "UsuarioPruebaCMMEDU" 

    ListaPregutnasEncuestas = []
    nombresEncuestas = []

    clasesyvariables.listaoras = funcionescsv.crearListaOra(orafile, ora_file_io)

    usr = usuario()
    usr.username = nombreUsuarioPrueba
    usr.usuarioprueba = True
    usr.nombre = "Usuario"
    usr.ApellidoM = "CMMEdu"
    usr.ApellidoP = "Prueba"

    clasesyvariables.usuarios.append(usr)

    File = csvfile
    # print("el file")
    # print (File)
    funcionescsv.RecorrerCSV( File, clasesyvariables.usuarios, clasesyvariables.listaoras )
    # print("Creando UP automatico")
    [jsonfile,jsonobj] = funcionesjson.createJsonUsuario( usr, codigocurso + "_" + id_string) #Crear achivo Json
    
    if subir:

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 

        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword , port= puerto, cnopts= cnopts) as sftp:

            ubicacion = "/usr/share/nginx/static.sumaysigue.uchile.cl/Usuarios Prueba/autogenerados/"
            nombrearchivo = "UsuarioPrueba_" + codigocurso +"_" + ".json"
            subirDir =  ubicacion + nombrearchivo
            sftp.put(jsonfile, subirDir)

            ubicacionfinal = "https://static.sumaysigue.uchile.cl/Usuarios%20Prueba/autogenerados/" + nombrearchivo
        
        return [ubicacionfinal, jsonobj]
    return ["", jsonobj]