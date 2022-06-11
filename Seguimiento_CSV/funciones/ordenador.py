
import string  
import sys
import zipfile
from tempfile import NamedTemporaryFile
import csv
import os
import io
import time
import json
import re

from itertools import cycle

from pdb import set_trace as bp
from appJar import gui
from screeninfo import get_monitors

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
		# print("Subir file")
		dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
		# print(dirFile)
		self.app.setLabel("FileCSV", dirFile)


	def SubmitTalleresFile(self, btnName):
		# print("Subir file")
		dirFile = self.app.openBox(title="Buscar file...", dirName="C:User/desktop", asFile=False)
		# print(dirFile)
		self.app.setLabel("FileTaller", dirFile)

class StartApp(WindowsGui):

	def __init__(self, nameOfGui):
		self.app = gui(str(nameOfGui))

	def Ordenar(self, btnName):  # Obtener datos por sujeto

		File_CSV = self.app.getLabel("FileCSV")
		File_TalleresNombre = self.app.getLabel("FileTaller")
		NameCurso = self.app.getEntry("Nombre")
		Run(File_CSV,File_TalleresNombre,NameCurso)

	def Prepare(self):
		self.sizeOfWindow()
		
		self.app.addLabel("NombreTag", "Nombre del archivo", 3, 0)
		self.app.addEntry("Nombre", 3, 1)
		self.app.setEntryAlign("Nombre", "left")
		self.app.setEntryWidth("Nombre", 30)

		self.app.addLabel("FileCSVTag", "Archivo CSV", 4, 0)
		self.app.setLabelAlign("FileCSVTag", "left")
		self.app.addLabel("FileCSV", "", 4, 1)
		self.app.setLabelAlign("FileCSV", "left")
		self.app.setLabelWidth("FileCSV", 40)
		self.app.setLabelBg('FileCSV', 'white')
		self.app.addNamedButton("Abrir archivo CSV",'SaveCSVFile', self.SubmitCSVFile, 4, 2)
		self.app.setButtonSticky('SaveCSVFile', 'right')


		self.app.addLabel("FileTallerTag", "Archivo Talleres", 7, 0)
		self.app.setLabelAlign("FileTallerTag", "left")
		self.app.addLabel("FileTaller", "", 7, 1)
		self.app.setLabelAlign("FileTaller", "left")
		self.app.setLabelWidth("FileTaller", 40)
		self.app.setLabelBg('FileTaller', 'white')
		self.app.addNamedButton("Abrir archivo nombres de taller",'SaveTalleresFile', self.SubmitTalleresFile, 7, 2)
		self.app.setButtonSticky('SaveTalleresFile', 'right')


		self.app.addNamedButton("Ordenar", 'Ordenar', self.Ordenar, 10, 2)
		self.app.setButtonSticky('Ordenar', 'right')



def Run(CSV,Talleres,Nombre):
	# print("Ordenar")


	FileNombres = open(Talleres, "r",encoding="utf-8", newline='')
	csvordenado = []

	
	
	primeraLinea = True
	
	for line in FileNombres:

		stripped_line = line.strip()
		namelower = stripped_line.lower()
		# print(namelower)

		FileCSV = open(CSV,"r",encoding="utf-8", newline='')
		reader = csv.reader(FileCSV)
		for row in reader:

			if primeraLinea:
				csvordenado.append(row)
				primeraLinea = False

			nombreCompleto = row[2].split(">")

			if len(nombreCompleto)  > 1:
				nombreTaller = nombreCompleto[1].lower()
				# print(namelower  + " Vs. " + nombreTaller)
				if nombreTaller.find(namelower) != -1:
					# print("coinciden")
					csvordenado.append(row)
					#time.sleep(3)

	
	filename = Nombre + ".csv"
	if filename == ".csv":
		archivoname = os.path.splitext(os.path.basename(CSV))[0]
		filemame = archivoname + "_Ordenado.csv"
		# print(filemame)
	csvdir = os.path.join(sys.path[0], filemame)
	# print ("csvdir " + csvdir)
	text_file = open(csvdir, "w+", encoding='utf-8', newline='')
	
	'''
	for csvline in csvordenado:

		lineastring = ''

		for textum in csvline:
			lineastring += textum + ','
			print(textum)
		
		if lineastring[-1] == ',':
			lineastring = lineastring[:-1]

		lineastring += '\n'

		n = text_file.write(lineastring)
		#ime.sleep(5)
	'''

	print(csvordenado)
	
	try:
		write = csv.writer(text_file)
		write.writerows(csvordenado)
	except IOError:
		print("I/O error")
	
	print ("Guardar CSV")
	text_file.close()


App = StartApp("Ordenador")
App.Start()
