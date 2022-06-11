#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
from datetime import datetime
import zipfile
from tempfile import NamedTemporaryFile
import csv
import os
import io
import time
import json
import re
#import requests
import urllib.request 

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Fill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill

from itertools import cycle
import string  
#import pyexcel as p
import xml.etree.ElementTree as ET

#CodigosLocales
import driveapi
import clasesyvariables
from clasesyvariables import usuario
from clasesyvariables import pregunta
from clasesyvariables import subpreguntaencuesta
from clasesyvariables import ora
clasesyvariables.init()


import funcionesjson
from funcionesjson import createJsonTaller
import funcionescsv
import funcionesplanilla

import requests
import pandas as pd

#generador de up automatico
from upgenerator import autoup 

from pdb import set_trace as bp

import subprocess #para probar el script sin necesidad de estar cerrando excel todo el tiempo. solo funciona en windows.
try:
	subprocess.call(["taskkill", "/f", "/im", "EXCEL.EXE"])
except:
	pass

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


#SACAR TIME SLEEP
org_sleep = time.sleep # save the original #time.sleep
#Preguntas sobre la ejecución
sleep =  False # set sleep to false when doesn’t want to sleep
saltarPrimeriaLienaListaUsuarios = False
subirDrive = True # Subir los documentos a drive
generarjson = True #Generar json de preguntas de este curso
upautomatico = True
clasesyvariables.doSilent = True
upautomatico_static = False
subirdatos = False
datoslocal = True
urldatos = "http://localhost:5000"
encuestaclase3 = True

if sleep != True: # if sleep is false
    # override #time.sleep to an empty function
    time.sleep = lambda x: None 
    
if(clasesyvariables.doSilent):
    time.sleep = lambda x: None 

    def print(*args):
        pass

def CreateErrorFile(listaErrores,nombre):
    print("Es hora deeee Anomaliacs ")

    nombreAnomalo = "Anomalias_" + nombre + ".txt"    
    logError_dir = os.path.join(sys.path[0],"Generado/Txt", nombreAnomalo )
    if os.path.isfile(logError_dir):
        os.remove(logError_dir)
    print ("Anomalias " + logError_dir)
    text_file2 = open(logError_dir, "w+", encoding='utf-8')

    for anomalia in listaErrores:
        n = text_file2.write(anomalia + '\n' )

    print ("Guardar Txt")
    text_file2.close()

    return logError_dir


def quitarUsuarioPruebadelaLista(nombreUsrPrueba):
    print("Buscar al ususario de prueba para sacarlo "  + str(nombreUsrPrueba))
    ##time.sleep(5)
    for usrprueba in clasesyvariables.usuarios:
        print (str(usrprueba.nombre) + " VS " + nombreUsrPrueba)
        if(usrprueba.username.find(nombreUsrPrueba) != -1):
            print("Borarre al usuario de prueba: " + usrprueba.nombre + " por USERNAME")
            usrtoDelete = usrprueba
            clasesyvariables.usuarios.remove(usrtoDelete)
           # #time.sleep(12)

#Busquedas en la API
def buscar_o_crear_curso_base(archivo_student_profile,archivo_json_UP):
    response = requests.post(
    urldatos + "/encontrar_curso_base",
    files={'archivo_usuarios': open(archivo_student_profile,'rb')}
    )
    if(response.status_code == 200):
        id_curso_base = response.json()['id_curso_base']
    else:
        #creo curso base
        response = requests.post(
        urldatos + "/curso_base",
        files={'archivo_usuarios': open(archivo_student_profile,'rb'), 
                'archivo_usuario_prueba': open(archivo_json_UP,'rb')}
        )
        #obtengo su id
        response = requests.post(
        urldatos + "/encontrar_curso_base",
        files={'archivo_usuarios': open(archivo_student_profile,'rb')}
        )
        id_curso_base = response.json()['id_curso_base']
    return id_curso_base

def buscar_o_crear_seccion(archivo_student_profile, id_curso_base):
    response = requests.post(
    urldatos + "/encontrar_seccion",
    data = {'id_curso_base':id_curso_base},
    files={'archivo_usuarios': open(archivo_student_profile,'rb')}
    )
    if(response.status_code == 200):
        id_seccion = response.json()['id_seccion']
    else:
        #creo seccion
        response = requests.post(
        urldatos + "/seccion",
        files={'archivo_usuarios': open(archivo_student_profile,'rb')}
        )
        #obtengo su id
        response = requests.post(
        urldatos + "/encontrar_seccion",
        data = {'id_curso_base':id_curso_base},
        files={'archivo_usuarios': open(archivo_student_profile,'rb')}
        )
        id_seccion = response.json()['id_seccion']
    return id_seccion




###-----------------------------### Ejecución  ###-----------------------------###
# Aqui empieza ejecución
t = time.time()
cantidadTalleres = 0

loaded_file = ""
clasesyvariables.location_to_save_report = ""

listaUsuarios = ""

try:
	loaded_file = sys.argv[1]
except IndexError:
    loaded_file = "C:\CMM-LabE\Seguimiento\Entradas json\Entrada-Diego - Auto.json"
    

if len(sys.argv)>2:
    if sys.argv[2] == '-silent':
        doSilent = True

print("Archivo: " + loaded_file)

with open(loaded_file, 'r') as loaded_json_file:
    data=loaded_json_file.read()

JsonEntrada = json.loads(data)

#print (JsonEntrada)

listaUsuarios = JsonEntrada["listausuarios"]
orafile = JsonEntrada["ora"]
listaTalleres = JsonEntrada ["talleres"]

if "encuestaclase3" in JsonEntrada:
    encuestaclase3 = JsonEntrada["encuestaclase3"]

if "datoslocales" in JsonEntrada:
    datoslocal = JsonEntrada["datoslocales"]

if "subirdatos" in JsonEntrada:
    subirdatos = JsonEntrada["subirdatos"]

#jsonUsuarioPrueba = JsonEntrada["jsonuserprueba"] #ya no lo obtengo del Json


print ("Talleres " + str(listaTalleres))

# Descarga archivo Drive de lista usuarios del curso en específico
curso = JsonEntrada['listausuarios'].split('/')[-1]
codigosSec = curso.split('_')[1]
anoSec = curso.split('_')[2]
programa = codigosSec[3:8]          # 3 - 8 va el programa del curso ej: MEDIA, ELEARN, BASIC
siglasCurso = codigosSec[8:11]      # 8 - 11 van las siglas del curso ej IEP, DPA, SND, etc
sleCurso = codigosSec[11:14]        # 11 - 14 van las siglas del servicio local o territorio (o en su defecto instancia) ej RMP (region metropolitana), COA (costa araucania), CON (conce), PIL (piloto)
numeroSeccion = codigosSec[14:]     # 14 - final van los dos dígitos que indican el numero de la sección ej 01, 02, etc.
nombreArchivoDriveDatosUsuarios = 'DATOS_CPEIP_'+programa+'_'+siglasCurso+'_'+sleCurso+'_SEC'+numeroSeccion
#listaUsuariosFilepath = '/var/www/html/seguimiento/datosUsuarios.xlsx'
if(siglasCurso == "M01"):
    siglasCurso = "MP"+numeroSeccion[-1]
jsonUsuarioPrueba = "https://static.sumaysigue.uchile.cl/Usuarios%20Prueba/UsuarioPrueba_" + siglasCurso +".json"

upautomatico = False

if 'automatico' in JsonEntrada:
    upautomatico = JsonEntrada["automatico"]


prefijo = ""
programa_up = ""
subprograma_up = ""
siglas = ""
seccion = ""
anio = ""
semestre = ""

if upautomatico:
    prefijo = JsonEntrada["curso"]["pefijo"]
    programa_up = JsonEntrada["curso"]["programa"]
    subprograma_up = JsonEntrada["curso"]["subprograma"]
    siglas = JsonEntrada["curso"]["siglas"]
    seccion = JsonEntrada["curso"]["seccion"]
    anio = str(JsonEntrada["curso"]["ano"])
    semestre = str(JsonEntrada["curso"]["semestre"])
    
    upgenerado = autoup.AutoUP(prefijo,programa_up,subprograma_up,siglas,seccion,anio,semestre,upautomatico_static)
    if upautomatico_static:
        jsonUsuarioPrueba = upgenerado
    else:
        jsonUsuarioPrueba = "file:///" + upgenerado


print("Json usuario de prueba: ")
print(jsonUsuarioPrueba)



#Ya no es necesario descargar los datos de usuarios 
'''
listaUsuariosFilepath = 'datosUsuarios.xlsx'
if os.path.isfile(listaUsuariosFilepath):
    os.remove(listaUsuariosFilepath)

codigodrive_listausuarios = JsonEntrada["codigodrive_listausuarios"]
driveapi.downloadFile(listaUsuariosFilepath,codigodrive_listausuarios,nombreArchivoDriveDatosUsuarios)
'''
#########################################

# Descarga archivo Drive lista negra 
#listaNegraFilePath = '/var/www/html/seguimiento/listaNegra.xlsx'
listaNegraFilePath = 'listaNegra.xlsx'
codigodrive_listanegra = JsonEntrada["codigodrive_listanegra"]
driveapi.downloadFile(listaNegraFilePath,codigodrive_listanegra,'listaUsuariosEquipo')


# Descraga de version anterior del reporte 
codigoCarpetaPlanillasInput = JsonEntrada["codigodrive_reporte"]
prenombre = programa+'_'+siglasCurso+'_'+sleCurso+'_SEC'+numeroSeccion
nombreReporteDrive = 'REPORTE_'+ prenombre
#ReportePath = '/var/www/html/seguimiento/ReporteDescargado.xlsx'
ReportePath = 'Generado/Xls/ReporteDescargado.xlsx'

#Codigo para subir la encuesta a drive
codigoCarpetaEncuesta = JsonEntrada["codigodrive_encuesta"]
nombreEncuestaDrive = "ENCUESTA_" + prenombre
nombreAnomaliasDrive = "ANOMALIAS_"+ prenombre
nombreJson = "JSON_" + prenombre 


#Codigo para subir las anomalias
codigoCarpetaAnomalias = codigoCarpetaPlanillasInput
if("codigodrive_anomalias" in  JsonEntrada ):
    codigoCarpetaAnomalias = JsonEntrada["codigodrive_anomalias"]



######################################

clasesyvariables.logErrores.append("#--------# Registro de anomalias de: " + prenombre + " #--------#") #Añadir nombre del curso a la lista de errores

#clasesyvariables.nombreUsuarioPrueba = "UsuarioPruebaCMMEDU"
tipoPlanilla = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
tipoTxt = 'text/plain'
tipoJson = 'application/json'

listanegra = []
controlesdisponibles = []
#conteoPreguntasEncuestas

print ("Execution")
funcionesjson.LoadUsuarioDePrueba(jsonUsuarioPrueba)
funcionescsv.crearListaUsuarios(listaUsuarios) #llenar la lista de usuarios
#LoadDatosUsuario(listaUsuariosFilepath) #agregar datos adicionales
funcionesplanilla.LoadListaNega(listaNegraFilePath) #Eliminar ususarios 
quitarUsuarioPruebadelaLista( clasesyvariables.nombreUsuarioPrueba )
clasesyvariables.listaoras = funcionescsv.crearListaOra(orafile)
for taller in listaTalleres: #Recorrer talleres 
    print("recorrer CSV Taller "+ taller)
    #time.sleep(1)
    funcionescsv.RecorrerCSV( taller, clasesyvariables.usuarios, clasesyvariables.listaoras )
for taller2 in listaTalleres:
    print("recorrer CSV para encuesta en "+ taller)
    #time.sleep(1)
    if encuestaclase3:
        funcionescsv.RecorrerCSVParaEncuestaClase3( taller, clasesyvariables.usuarios )
    else:
        funcionescsv.RecorrerCSVParaEncuesta( taller, clasesyvariables.usuarios )


jsonFile = "nada"
if generarjson :
    jsonFile = createJsonTaller( clasesyvariables.usuarios,prenombre ) #Crear achivo Json


#quitarUsuarioPruebadelaLista(nombreUsuarioPrueba)

archivoSalida = funcionesplanilla.createXLS ( clasesyvariables.usuarios,prenombre )  #Crear archivo .xls
archivoSalidaEncuesta = funcionesplanilla.createDocumentoEncuesta( clasesyvariables.ListaPregutnasEncuestas,prenombre )  #Creae archivo encuesta .xl

#Crear logs de errores
if len(clasesyvariables.logErrores) < 2 :
    clasesyvariables.logErrores.append("ESTE CURSO NO PRESENtA ANOMALIAS REGISTRADAS... Excelente")

clasesyvariables.logErrores.append("#-----------#Fin Anomalias#-----------#") #Añadir nombre del curso a la lista de errores

AnomaliasFile = CreateErrorFile(clasesyvariables.logErrores,prenombre)

''' prints del final
print("Total preguntas por taller: " + str(totalPreguntasPorTaller) + " Cantidad de talleres " + str(cantidadTalleres))
print("Total preguntas por control " + str(totalPreguntasPorControl) + " cantidad de controles " + str(cantidadControles))
print("Total Encuestas " + str(totalEncuestas) + " cantidad de encuestas " + str(cantidadEncuestas))
print("Total preguntas evaluadas" + str(totalPreguntasEvaluadas) + " cantidad preguntas evaluadas " + str(cantidadTipoPreguntaEvaluada) ) 
print( "Preguntas que pueden ser buenas o malas: " + str(totalPreguntasBuenasOMalas) )
print("Encuestas " + str(nombresEncuestas) )
#print ("registro de anomalias " + str(logErrores))
#print("Lista preguntas encuestas " + str(ListaPregutnasEncuestas))
'''
listausr ="Lista usuarios: "
for usrprint in clasesyvariables.usuarios:
    listausr += ","  + str(usrprint.username) + " "
print (listausr)



if(subirDrive):
    # Subir reporte a planillas input en Drive
    driveapi.uploadFile(archivoSalida, codigoCarpetaPlanillasInput, nombreReporteDrive,tipoPlanilla)
    
    # Subir registro de anomalias a drive
    driveapi.uploadFile(AnomaliasFile, codigoCarpetaAnomalias, nombreAnomaliasDrive,tipoTxt)

    # if generarjson and jsonFile != "nada":
        # driveapi.uploadFile(jsonFile, codigoCarpetaPlanillasInput, nombreJson,tipoJson)

    # Subir documento de encuesta a la carpeta en drive
    driveapi.uploadFile(archivoSalidaEncuesta, codigoCarpetaEncuesta, nombreEncuestaDrive,tipoPlanilla)
    #############################

if (subirdatos):

    if datoslocal:
        urldatos = "http://localhost:5000"
    else:
        urldatos = "http://localhost:5000"

    json_usuarioprueba = jsonUsuarioPrueba.replace('file:///', '')
    id_curso_base = buscar_o_crear_curso_base(listaUsuarios,json_usuarioprueba)

    print(id_curso_base)

    id_seccion = buscar_o_crear_seccion(listaUsuarios, id_curso_base)

    print(id_seccion)

    #ahora subo las respuestas
    json_respuestas = jsonFile
    csv_oras = orafile
    csv_encuestas = archivoSalidaEncuesta
    #HAY QUE CONVERTIR EL EXCEL DE ENCUESTAS A CSV SEPARADO POR COMAS
    read_file = pd.read_excel(csv_encuestas)
    read_file.to_csv(csv_encuestas[:-3]+"csv", index = None, header=True)
    csv_encuestas = csv_encuestas[:-3]+"csv"



    response = requests.post(
            urldatos + "/respuestas/"+str(id_seccion),
            files={'archivo_respuestas': open(json_respuestas,'rb')}
            )
    if(response.status_code != 200):
            raise Exception("Error subiendo respuestas")

    #subo oras
    response = requests.post(
            urldatos + "/oras/"+str(id_seccion),
            files={'json_respuestas': open(json_respuestas,'rb'), 'archivo_oras': open(csv_oras,'rb')}
            )
    if(response.status_code != 200):
            raise Exception("Error subiendo ORAs")

    #subo encuestas
    response = requests.post(
            urldatos + "/encuestas/"+str(id_seccion),
            files={'archivo_encuestas': open(csv_encuestas,'rb')}
            )
    if(response.status_code != 200):
            raise Exception("Error subiendo encuestas")


print ("Finished")
if len(sys.argv)>2:
	if sys.argv[2]=='-silent':
		del print
print("tiempo empleado: "+str(round(time.time() - t,2))+" seg")

#autoabrir archivo excel
try:
	subprocess.check_output(["start", "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL", archivoSalida],stderr=subprocess.STDOUT,shell=True)
except:
	pass