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
import urllib.request 

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Fill, Border, Side, alignment
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

#generador de up automatico
from upgenerator import autoup 


from pdb import set_trace as bp
from appJar import gui
from screeninfo import get_monitors

import requests
import pandas as pd

import subprocess #para probar el script sin necesidad de estar cerrando excel todo el tiempo. solo funciona en windows.
try:
	subprocess.call(["taskkill", "/f", "/im", "EXCEL.EXE"])
except:
	pass

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
orafile = None
listaUsuarios = None
listaTalleres = None

#Codidogs de drive
cdr_reporte = "18EpFEFPe4i160crMvSeZ5pplGoc9Mua5"
cdr_listausuarios = "1LYgBb2b-S0IBDVwVwkCldiMC78qbgvry"
cdr_listanegra = "1zWHomYLfFHPr4usbFbuGb5eAZSVlPRih"
cdr_encuesta = "1SqvYZKenDJh7nKn0kDPi4zYt_bQmU6he"
cdr_anolaias = "1Cqd_2glf7-yCZJ-Ry1qdB0CYOUaaL61_"


class WindowsGui():
	def __init__(self, nameOfGui):
		self.app = gui(nameOfGui, "600x400")
	
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

	def SubmitPROFile(self, btnName):
		print("Subir file")
		dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
		print(dirFile)
		self.app.setLabel("FilePRO", dirFile)

	def SubmitUPJSONFile(self, btnName):
		print("Subir file")
		dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
		print(dirFile)
		self.app.setLabel("FileUPJ", dirFile)

class StartApp(WindowsGui):

	def __init__(self, nameOfGui):
		self.app = gui(str(nameOfGui))

	def Revisar(self, btnName):  # Obtener datos por sujeto

		File = self.app.getLabel("FileCSV")
		orafile = self.app.getLabel("FileORA")
		PROfile = self.app.getLabel("FilePRO")
		valueSubirDrive = self.app.getCheckBox("Subir a drive")
		valuejsoncurso = self.app.getCheckBox("Generar json del curso")
		NameCurso = self.app.getEntry("Curso")
		enccl3 = self.app.getCheckBox("Encuesta clase 3")
		valuesubirdatos = self.app.getCheckBox("Subir datos")
		datoslocales = self.app.getCheckBox("Datos locales")

		# Casillas usuarios de prueba
		UPJfile = ""
		UPURL = ""

		puntoscheck = 0
		check_uplocal =  self.app.getCheckBox("UP Local")
		check_upurl =  self.app.getCheckBox("UP URL")
		check_upauto =  self.app.getCheckBox("UP Automatico")
		


		if check_uplocal == True:
			puntoscheck += 1
			print("casilla local")
		
		if check_upurl == True:
			puntoscheck += 1
			print("casilla url")

		if check_upauto == True:
			print("casilla auto")
			puntoscheck += 1

		if puntoscheck == 1:
			print("Solo hay un UP ahora si...")

			if check_uplocal:
				UPJfile = self.app.getLabel("FileUPJ")

			if check_upurl:
				UPURL = self.app.getEntry("UPURL")

			if check_upauto:
				print("el up es automatico")

				prefijo = self.app.getEntry("UPPrefi")
				programa = self.app.getEntry("UPProg")
				subprograma = self.app.getEntry("UPSubProg")
				siglas = self.app.getEntry("UPSig")
				seccion = self.app.getEntry("UPSecc")
				anio = self.app.getEntry("UPAno")
				semestre = self.app.getEntry("UPSem")
				subirautoupstatic = self.app.getCheckBox("subir UP a static")

				autoupgenerado = autoup.AutoUP(prefijo,programa,subprograma,siglas,seccion,anio,semestre,subirautoupstatic)
				print ("generado")
				print(autoupgenerado)
				UPJfile = autoupgenerado
		
			if valuesubirdatos:
				valuejsoncurso = True

			Run(NameCurso ,orafile, PROfile, File, UPJfile,UPURL ,valueSubirDrive,valuejsoncurso,enccl3,valuesubirdatos,datoslocales)

		elif puntoscheck == 0:
			self.app.errorBox("No usuario prueba", "Debe marcar UNA casilla de UP", parent=None)
		elif puntoscheck > 1:
			self.app.errorBox("No usuario prueba", "Debe marcar solamente UNA casilla de UP", parent=None)

			



	def Prepare(self):
		self.sizeOfWindow()
		
		self.app.addLabel("cursoTag", "Curso", 3, 0)
		self.app.addEntry("Curso", 3, 1)
		self.app.setEntryAlign("Curso", "left")
		self.app.setEntryWidth("Curso", 30)

		self.app.addLabel("FileCSVTag", "Archivo CSV", 4, 0)
		self.app.setLabelAlign("FileCSVTag", "left")
		self.app.addLabel("FileCSV", "", 4, 1)
		self.app.setLabelAlign("FileCSV", "left")
		self.app.setLabelWidth("FileCSV", 40)
		self.app.setLabelBg('FileCSV', 'white')
		self.app.addNamedButton("Abrir archivo CSV",'SaveCSVFile', self.SubmitCSVFile, 4, 2)
		self.app.setButtonSticky('SaveCSVFile', 'right')

		self.app.addLabel("FileORATag", "Archivo ORA", 5, 0)
		self.app.setLabelAlign("FileORATag", "left")
		self.app.addLabel("FileORA", "", 5, 1)
		self.app.setLabelAlign("FileORA", "left")
		self.app.setLabelWidth("FileORA", 40)
		self.app.setLabelBg('FileORA', 'white')
		self.app.addNamedButton("Abrir archivo ORA",'SaveORAFile', self.SubmitORAFile, 5, 2)
		self.app.setButtonSticky('SaveORAFile', 'right')

		self.app.addLabel("FilePROTag", "Archivo PROFILE", 6, 0)
		self.app.setLabelAlign("FilePROTag", "left")
		self.app.addLabel("FilePRO", "", 6, 1)
		self.app.setLabelAlign("FilePRO", "left")
		self.app.setLabelWidth("FilePRO", 40)
		self.app.setLabelBg('FilePRO', 'white')
		self.app.addNamedButton("Abrir archivo PROFILE",'SavePROFile', self.SubmitPROFile, 6, 2)
		self.app.setButtonSticky('SavePROFile', 'right')

		self.app.addLabel("UP", "Usuario de prueba: (Solo marque un checkbox de UP)", 7, 0)
		self.app.getLabelWidget("UP").config(font=("Comic Sans","16", "bold"))

		self.app.addCheckBox("UP Local")
		self.app.addLabel("FileUPJTag", "Archivo UP JSON", 9, 0)
		self.app.setLabelAlign("FileUPJTag", "left")
		self.app.addLabel("FileUPJ", "", 9, 1)
		self.app.setLabelAlign("FileUPJ", "left")
		self.app.setLabelWidth("FileUPJ", 40)
		self.app.setLabelBg('FileUPJ', 'white')
		self.app.addNamedButton("Abrir archivo UPJSON",'SaveUPJFile', self.SubmitUPJSONFile, 9, 2)
		self.app.setButtonSticky('SaveUPJFile', 'right')

		self.app.addCheckBox("UP URL")
		self.app.addLabel("UPURTagL", "URL UP JSON", 11, 0)
		self.app.addEntry("UPURL", 11, 1)
		self.app.setEntryAlign("UPURL", "left")
		self.app.setEntryWidth("UPURL", 40)

		self.app.addCheckBox("UP Automatico")
		self.app.addLabel("UPPrefiTag", "Prefijo", 13, 0)
		self.app.addEntry("UPPrefi", 13, 1)
		self.app.setEntryAlign("UPPrefi", "left")
		self.app.setEntryWidth("UPPrefi", 40)
		self.app.setEntryDefault("UPPrefi", "cmm")
		self.app.addLabel("UPProgTag", "Programa", 14, 0)
		self.app.addEntry("UPProg", 14, 1)
		self.app.setEntryAlign("UPProg", "left")
		self.app.setEntryWidth("UPProg", 40)
		self.app.setEntryDefault("UPProg", "SYS")
		self.app.addLabel("UPSubProgTag", "Sub-programa", 15, 0)
		self.app.addEntry("UPSubProg", 15, 1)
		self.app.setEntryAlign("UPSubProg", "left")
		self.app.setEntryWidth("UPSubProg", 40)
		self.app.setEntryDefault("UPSubProg", "ELEAR")
		self.app.addLabel("UPSigTag", "Siglas del curso", 16, 0)
		self.app.addEntry("UPSig", 16, 1)
		self.app.setEntryAlign("UPSig", "left")
		self.app.setEntryWidth("UPSig", 40)
		self.app.setEntryDefault("UPSig", "DMF")
		self.app.addLabel("UPSeccTag", "Sección", 17, 0)
		self.app.addEntry("UPSecc", 17, 1)
		self.app.setEntryAlign("UPSecc", "left")
		self.app.setEntryWidth("UPSecc", 40)
		self.app.setEntryDefault("UPSecc", "SLF04 o 01")
		self.app.addLabel("UPAnoTag", "Año", 18, 0)
		self.app.addEntry("UPAno", 18, 1)
		self.app.setEntryAlign("UPAno", "left")
		self.app.setEntryWidth("UPAno", 40)
		self.app.setEntryDefault("UPAno", "2021")
		self.app.addLabel("UPSemTag", "Semestre", 19, 0)
		self.app.addEntry("UPSem", 19, 1)
		self.app.setEntryAlign("UPSem", "left")
		self.app.setEntryWidth("UPSem", 40)
		self.app.setEntryDefault("UPSem", "1")
		self.app.addCheckBox("subir UP a static")

		self.app.addLabel("Op", "Opciones de exportado: ", 21, 0,)
		self.app.getLabelWidget("Op").config(font=("Comic Sans","16", "bold"))

		self.app.addCheckBox("Subir a drive")
		self.app.addCheckBox("Generar json del curso")
		self.app.setCheckBox("Generar json del curso", ticked=True, callFunction=False)
		self.app.addCheckBox("Encuesta clase 3")
		self.app.setCheckBox("Encuesta clase 3", ticked=True, callFunction=False)
		self.app.addCheckBox("Subir datos")
		self.app.addCheckBox("Datos locales")
		self.app.setCheckBox("Datos locales", ticked=True, callFunction=False)
		

		self.app.addNamedButton("Revisar", 'Revisar', self.Revisar, 27, 2)
		self.app.setButtonSticky('Revisar', 'right')

def Run(nombrecurso, orafile, listaUsuarios, state, loaded_file, url_file, valSubirDrive,valuejsoncurso,enccl3,subdatos,localdata):

	#SACAR TIME SLEEP
	org_sleep = time.sleep # save the original #time.sleep
	#Preguntas sobre la ejecución
	sleep =  False # set sleep to false when doesn’t want to sleep
	saltarPrimeriaLienaListaUsuarios = False
	subirDrive = valSubirDrive # Subir los documentos a drive
	generarjson = valuejsoncurso #Generar json de preguntas de este curso
	encuestaclase3 = enccl3
	subirdatos = subdatos
	datoslocal = localdata
	urldatos = "http://localhost:5000"
	clasesyvariables.doSilent = True

	if not datoslocal:
		urldatos = "http://localhost:5000"

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
		logError_dir = os.path.join(sys.path[0],"Generado\Txt", nombreAnomalo )
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
				#time.sleep(12)


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
			print("arvhivo student" + archivo_student_profile )
			print("arvhivo student" + archivo_json_UP )

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

	clasesyvariables.location_to_save_report = ""

	if len(sys.argv)>2:
		if sys.argv[2] == '-silent':
			doSilent = True

	print("Archivo: " + loaded_file + " URL: " + url_file)

	if loaded_file != "" :

		with open(loaded_file, 'r',encoding="cp866") as loaded_json_file:
			data=loaded_json_file.read()

		JsonEntrada = json.loads(data)
	else:
		JsonEntrada = ""

	#print (JsonEntrada)
	if listaUsuarios is None:
		listaUsuarios = JsonEntrada["listausuarios"]
	if orafile is None:
		orafile = JsonEntrada["ora"]
	
	#if listaTalleres is None:
	#	listaTalleres = JsonEntrada ["talleres"]
	
	listaTalleres=[]

	listaTalleres.append(state)

	#jsonUsuarioPrueba = JsonEntrada["jsonuserprueba"] #ya no lo obtengo del Json


	print ("Talleres " + str(listaTalleres))

	# Descarga archivo Drive de lista usuarios del curso en específico
	if nombrecurso != "":
		curso = nombrecurso
	else:
		curso = listaUsuarios.split('/')[-1]
	print ("curso: " + curso )
	#time.sleep(50)
	#curso = JsonEntrada['listausuarios'].split('/')[-1]
	#bp()
	codigosSec = curso.split('_')[1]
	anoSec = curso.split('_')[2]
	programa = codigosSec[3:8]          # 3 - 8 va el programa del curso ej: MEDIA, ELEARN, BASIC
	siglasCurso = codigosSec[8:11]      # 8 - 11 van las siglas del curso ej IEP, DPA, SND, etc
	sleCurso = codigosSec[11:14]        # 11 - 14 van las siglas del servicio local o territorio (o en su defecto instancia) ej RMP (region metropolitana), COA (costa araucania), CON (conce), PIL (piloto)
	numeroSeccion = codigosSec[14:]     # 14 - final van los dos dígitos que indican el numero de la sección ej 01, 02, etc.
	nombreArchivoDriveDatosUsuarios = 'DATOS_CPEIP_'+programa+'_'+siglasCurso+'_'+sleCurso+'_SEC'+numeroSeccion
	
	#listaUsuariosFilepath = '/var/www/html/seguimiento/datosUsuarios.xlsx'

	#jsonUsuarioPrueba = "https://static.sumaysigue.uchile.cl/Usuarios%20Prueba//UsuarioPrueba_" + siglasCurso +".json"
	if url_file == "":
		jsonUsuarioPrueba = "file:///" +  loaded_file
	else:
		jsonUsuarioPrueba = url_file
	
	#Ya no es necesario descargar los datos de usuarios 
	"""
	listaUsuariosFilepath = 'datosUsuarios.xlsx'
	if os.path.isfile(listaUsuariosFilepath):
		os.remove(listaUsuariosFilepath)

	codigodrive_listausuarios = cdr_listausuarios
	driveapi.downloadFile(listaUsuariosFilepath,codigodrive_listausuarios,nombreArchivoDriveDatosUsuarios)
	student_profilefile = listaUsuariosFilepath
	"""
	#########################################

	# Descarga archivo Drive lista negra 
	#listaNegraFilePath = '/var/www/html/seguimiento/listaNegra.xlsx'
	listaNegraFilePath = 'listaNegra.xlsx'
	codigodrive_listanegra = cdr_listanegra
	driveapi.downloadFile(listaNegraFilePath,codigodrive_listanegra,'listaUsuariosEquipo')  

	# Descraga de version anterior del reporte 
	codigoCarpetaPlanillasInput = cdr_reporte
	prenombre = programa+'_'+siglasCurso+'_'+sleCurso+'_SEC'+numeroSeccion
	nombreReporteDrive = 'REPORTE_'+ prenombre
	#ReportePath = '/var/www/html/seguimiento/ReporteDescargado.xlsx'
	ReportePath = 'ReporteDescargado.xlsx'

	#Codigo para subir la encuesta a drive
	codigoCarpetaEncuesta = cdr_encuesta
	nombreEncuestaDrive = "ENCUESTA_" + prenombre
	nombreAnomaliasDrive = "ANOMALIAS_"+ prenombre
	nombreJson = "JSON_" + prenombre 


	#Codigo para subir las anomalias
	codigoCarpetaAnomalias = cdr_anolaias



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
	print("Lista Talleres")
	print(listaTalleres)
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

		if generarjson and jsonFile != "nada":
			driveapi.uploadFile(jsonFile, codigoCarpetaPlanillasInput, nombreJson,tipoJson)

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
				raise Exception(f"Error subiendo respuestas")

		#subo oras
		response = requests.post(
				urldatos +"/oras/"+str(id_seccion),
				files={'json_respuestas': open(json_respuestas,'rb'), 'archivo_oras': open(csv_oras,'rb')}
				)
		if(response.status_code != 200):
				raise Exception(f"Error subiendo ORAs")

		#subo encuestas
		response = requests.post(
				urldatos + "/encuestas/"+str(id_seccion),
				files={'archivo_encuestas': open(csv_encuestas,'rb')}
				)
		if(response.status_code != 200):
				raise Exception(f"Error subiendo encuestas")



	print("tiempo empleado: "+str(round(time.time() - t,2))+" seg")

	#autoabrir archivo excel
	try:
		subprocess.check_output(["start", "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL", archivoSalida],stderr=subprocess.STDOUT,shell=True)
	except:
		pass

if len(sys.argv) == 1:
   
	
	App = StartApp("Seguimiento")
	App.Start()

elif len(sys.argv)>2:
	if sys.argv[2]=='-silent':
		del print
else:
	Run(None,None,None,None)