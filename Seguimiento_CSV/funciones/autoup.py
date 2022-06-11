#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pickle import UnpicklingError
import sys, os
from . import api_preguntas as api_preguntas
from . import csvup as csvup
from . import creador_de_usuario_prueba as creador_de_usuario_prueba

from pdb import set_trace as bp
from datetime import datetime

'''
prefix = 'cmm'
programa = 'SYS'
subprograma = ELEAR | CBASE
siglas_curso = 'DMF'
seccion = SLF01 | SLF00
ano = '2020'
semestre='1'

curso = 'course-v1:'+prefix+'+'+programa+siglas_curso+'+'+ano+'_'+semestre # esto sería la variable que hay que ver como armar ej: course-v1:cmm+SYSELEARDMFSLF01+2020_1
'''

def AutoUP(prefix,programa,subprograma,siglas_curso,seccion,ano,semestre,subir,ora_file_io=None):
    curso = 'course-v1:'+prefix+'+'+programa+subprograma+siglas_curso+seccion+'+'+ano+'_'+semestre
    # print("curso: " + curso)
    now = datetime.now()
    date_now_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    email = 'jromo.dcc@gmail.com'
    password = 'dimcmm33'
    raiz = 'https://cmmeduformacion.uchile.cl'
    nombre_sect = curso.replace('course-v1:','').replace('+','_')
    [r,r2] = api_preguntas.bajarJson(email,password,raiz,curso)
    original_stdout = sys.stdout
    talleres_name = 'talleres_'+nombre_sect+"_"+date_now_string+'.txt'
    talleres_location = os.path.join(sys.path[0],"Generado/Txt",talleres_name)
    with open(talleres_location, "w+", encoding='utf-8') as f:
        #sys.stdout = f # Change the standard output to the file we created.

        for block in r2["blocks"]:
            if r2["blocks"][block]["type"] == "chapter":
                f.write(r2["blocks"][block]["display_name"]+"\n")
        
        #sys.stdout = original_stdout # Reset the standard output to its original value
        
    csvup.JSON2CSV(r,nombre_sect,date_now_string)

    csv_file = "Bloques_" +nombre_sect+"_"+date_now_string+".csv"
    csv_file_dir = os.path.join(sys.path[0],"Generado/Csv", csv_file)
    #csv_file_dir =  "file:///" + csv_file_dir

    talleres_file = 'talleres_'+nombre_sect+"_"+date_now_string+'.txt'
    talleres_file_dir = os.path.join(sys.path[0],"Generado/Txt", talleres_file)
    #talleres_file_dir = "file:///" + talleres_file_dir

    csvup.ordenar(CSV = csv_file_dir ,Talleres = talleres_file_dir)


    orafile= "ORAS_"+nombre_sect+"_"+date_now_string+".csv"
    orafile_dir = os.path.join(sys.path[0],"Generado/Csv", orafile)
    #orafile_dir = "file:///" + orafile_dir

    csv_ordenado_file = "Bloques_"+nombre_sect+"_"+date_now_string+"_Ordenado.csv"
    csv_ordenado_file_dir = os.path.join(sys.path[0],"Generado/Csv", csv_ordenado_file)
    #csv_ordenado_file_dir = "file:///" + csv_ordenado_file_dir

    subirup = subir

    #upfile = creador_de_usuario_prueba.UsuarioPrueba(orafile = orafile_dir ,csvfile = csv_ordenado_file_dir ,subir = subirup,codigocurso=programa+siglas_curso+"_"+ano+'_'+semestre+"__",id_string=date_now_string)
    [upfile,json_file] = creador_de_usuario_prueba.UsuarioPrueba(orafile = orafile_dir ,csvfile = csv_ordenado_file_dir ,subir = subirup,codigocurso=programa+subprograma+siglas_curso+seccion+"_"+ano+'_'+semestre+"__",id_string=date_now_string, ora_file_io= ora_file_io)
    os.remove(csv_file_dir) #Borrar bloques
    os.remove(talleres_file_dir) #Borrar talleres
    os.remove(orafile_dir) #Borrar Oras
    os.remove(csv_ordenado_file_dir) #Borrar bloques ordenados
    
    # print("up creado")
    # print (json_file)

    return [upfile,json_file]

#AutoUP(curso="course-v1:cmm+SYSDMF01+2020_1")

