#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings(action='ignore', category=CryptographyDeprecationWarning)
import sys, os, io, time, json, requests, urllib.request, subprocess, cProfile
import pandas as pd
from dotenv import dotenv_values
from pathlib import Path
from pdb import set_trace as bp
import pathlib
'''  Codigos Locales:
        - driveapi.py: conexión con la api de drive para subir y bajar archivos a una carpeta específica. Actualmente solo funciona con planillas excel, porque no tiene como entrada el mimetype.
        - clasesyvariables.py: 
        - funcionesjson.py:
        - funcionescsv.py 
        - funcionesplanilla.py 
        - autoup.py: bajada y organización de los datos de estructura del curso. Utiliza la api a edX provista por eol.

    Otras de las clases y funciones que están en la carpeta funciones no se listan aquí porque no se importan directamente en esta clase.
'''
from funciones import driveapi
from funciones import clasesyvariables
clasesyvariables.init()
from funciones import funcionesjson
from funciones import funcionescsv
from funciones import funcionesplanilla
from funciones import autoup 
from funciones import datos_subida
from funciones import helpers
from funciones.helpers import renew_time


from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
from flask_login import LoginManager, logout_user, current_user, login_user, login_required


sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
org_sleep = time.sleep # save the original time.sleep
org_print = print # save the original print
class Seguimiento():
    @line_profile
    def ejecutar(self,student_state_data, ora_data, profile_data, nombre_curso=None,seg_config = None):
        org_print('Comenzó la ejecución')
        # archivos de entrada
        listaTalleres = student_state_data['fs'].filename
        orafile = ora_data['fs'].filename
        listaUsuarios = profile_data['fs'].filename
        seg_response = {}
        curso = None
        if nombre_curso:
            curso = nombre_curso
        else:
            curso = listaUsuarios.split('/')[-1]
        codigosSec = curso.split('_')[1]
        institucion = curso.split('_')[0]
        # asd = 1 / 0
        anoSec = curso.split('_')[2]
        semSec = curso.split('_')[3]
        subprograma = codigosSec[0:3]          # 0 - 3 va el programa del curso ej: SYS, ESP, DIP
        programa = codigosSec[3:8]          # 3 - 8 va el subprograma del curso ej: MEDIA, ELEARN, BASIC
        siglasCurso = codigosSec[8:11]      # 8 - 11 van las siglas del curso ej IEP, DPA, SND, etc
        sleCurso = codigosSec[11:14]        # 11 - 14 van las siglas del servicio local o territorio (o en su defecto instancia) ej RMP (region metropolitana), COA (costa araucania), CON (conce), PIL (piloto)
        numeroSeccion = codigosSec[14:]     # 14 - final van los dos dígitos que indican el numero de la sección ej 01, 02, etc.

        # Fix adhoc para MP1 tratar de solucionar
        if siglasCurso == "M01":
            siglasCurso = "MP"+numeroSeccion[-1]

        # configuración de la ejecución
        dotenv_dir = sorted(pathlib.Path('.').glob('**/seg-config.env')) # La primera coincidencia dentro de la carpeta del archivo seg-config.env será la que se utilice para la configuración del seguimiento.
        config = dotenv_values(dotenv_dir[0])
        if seg_config:
            keys_to_iterate = seg_config.keys() & config.keys()
            for key in keys_to_iterate:
                config[key] = seg_config[key]


        sleep =  config['sleep'].lower() in ('true', '1', 't') 
        saltar_primera_linea_lista_usuarios = config['saltarPrimeriaLienaListaUsuarios'].lower() in ('true', '1', 't') 
        subirDrive = config['subirDrive'].lower() in ('true', '1', 't') 
        generarjson = config['generarjson'].lower() in ('true', '1', 't') 
        upautomatico = config['upautomatico'].lower() in ('true', '1', 't')
        doSilent = config['doSilent'].lower() in ('true', '1', 't') 
        upautomatico_static = config['upautomatico_static'].lower() in ('true', '1', 't') 
        subirdatos = config['subirdatos'].lower() in ('true', '1', 't') 
        datoslocal = config['datoslocal'].lower() in ('true', '1', 't') 
        encuestaclase3 = config['encuestaclase3'].lower() in ('true', '1', 't') 
        medir_tiempo = config['medir_tiempo'].lower() in ('true', '1', 't') 

        urldatos = config['urldatos'] 
        codigoCarpetaEncuesta = config['codigoCarpetaEncuesta'] 
        codigodrive_listanegra = config['codigodrive_listanegra'] 
        codigoCarpetaPlanillasInput = config['codigoCarpetaPlanillasInput'] 
        codigodrive_anomalias = config['codigodrive_anomalias'] 
        codigodrive_listausuarios = config['codigodrive_listausuarios'] 

        # Construcción a mano del nombre de la planilla de datos del CPEIP
        nombreArchivoDriveDatosUsuarios = 'DATOS_CPEIP_'+subprograma+'_'+siglasCurso+'_'+sleCurso+'_SEC'+numeroSeccion

        jsonusuarioprueba = "https://static.sumaysigue.uchile.cl/usuarios%20prueba/usuarioprueba_" + siglasCurso +".json" #obsoleto, recordar que up responde a curso y año/sem

        time.sleep = lambda x: None if not sleep else org_sleep
        print = lambda *args, **kwargs: None if doSilent else org_print(*args, **kwargs)
        t = time.time() if medir_tiempo else False
        t_total = t
        tiempos = {}
        
        ###-----------------------------### ejecución  ###-----------------------------###

        cantidadtalleres = 0
        clasesyvariables.location_to_save_report = ""

        # print ("Talleres " + str(listaTalleres))
        jsonUsuarioPrueba = ""
        upgenerado = ""
        json_up = None
        # Hay que dar más soluciones para UP. Actualmente estaría solo aceptando UP automatico pero debería aceptar subir un UP
        if upautomatico:
            [upgenerado,json_up] = autoup.AutoUP(institucion,subprograma,programa,siglasCurso + sleCurso,numeroSeccion,anoSec,semSec,upautomatico_static, ora_data['io_obj'])
            json_up = json.loads("["+''.join(json_up)+"]")[0] # fix porque venía mal el json
            if upautomatico_static:
                jsonUsuarioPrueba = upgenerado
            else:
                jsonUsuarioPrueba = "file:///" + upgenerado
        else:
            # Implementar alguna lectura desde file.
            pass

        t,tiempos = renew_time(t,medir_tiempo,tiempos,'AutoUP')
        # Nombre del curso revisado
        prenombre = programa + '_' + siglasCurso + '_' + sleCurso+'_SEC'+numeroSeccion

        # print("Json usuario de prueba: ")
        # print(jsonUsuarioPrueba)

        # Descarga archivo Drive lista negra 
        listaNegraFilePath = 'listaNegra.xlsx'
        driveapi.downloadFile(listaNegraFilePath,codigodrive_listanegra,'listaUsuariosEquipo')

        # Descarga de version anterior del reporte 
        nombreReporteDrive = 'REPORTE_'+ prenombre
        ReportePath = 'Generado/Xls/ReporteDescargado.xlsx'

        #Codigo para subir la encuesta a drive
        nombreEncuestaDrive = "ENCUESTA_" + prenombre
        nombreAnomaliasDrive = "ANOMALIAS_"+ prenombre
        nombreJson = "JSON_" + prenombre 

        clasesyvariables.logErrores.append("#--------# Registro de anomalias de: " + prenombre + " #--------#") #Añadir nombre del curso a la lista de errores
        # Mimetypes archivos 
        tipoPlanilla = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        tipoTxt = 'text/plain'
        tipoJson = 'application/json'
        funcionesjson.LoadUsuarioDePrueba(jsonUsuarioPrueba,json_up)
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'LoadUsuarioDePrueba')
        funcionescsv.crearListaUsuarios(listaUsuarios,profile_data['io_obj']) #llenar la lista de usuarios
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'crearListaUsuarios')
        #LoadDatosUsuario(listaUsuariosFilepath) #agregar datos adicionales
        funcionesplanilla.LoadListaNega(listaNegraFilePath) #Eliminar ususarios
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'LoadListaNega')
        helpers.quitarUsuarioPruebadelaLista( clasesyvariables.nombreUsuarioPrueba )
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'quitarUsuarioPruebadelaLista')
        clasesyvariables.listaoras = funcionescsv.crearListaOra(orafile, ora_data['io_obj'])
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'crearListaOra')
        # Ejecutar RecorrerCSV en student data file 
        funcionescsv.RecorrerCSV( listaTalleres, clasesyvariables.usuarios, clasesyvariables.listaoras, student_state_data['io_obj'])
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'RecorrerCSV')
        if encuestaclase3:
            funcionescsv.RecorrerCSVParaEncuestaClase3( listaTalleres, clasesyvariables.usuarios , student_state_data['io_obj'])
            t,tiempos = renew_time(t,medir_tiempo,tiempos,'RecorrerCSVParaEncuestaClase3')
        else:
            funcionescsv.RecorrerCSVParaEncuesta( listaTalleres, clasesyvariables.usuarios , student_state_data['io_obj'])
            t,tiempos = renew_time(t,medir_tiempo,tiempos,'RecorrerCSVParaEncuesta')

        # Crear achivo Json
        jsonFile = funcionesjson.createJsonTaller(clasesyvariables.usuarios,prenombre) if generarjson else "nada"
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'createJsonTaller')

        # Crear archivo .xls
        archivoSalida = funcionesplanilla.createXLS ( clasesyvariables.usuarios,prenombre )
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'createXLS')  
        # Crear archivo encuesta .xls
        archivoSalidaEncuesta = funcionesplanilla.createDocumentoEncuesta( clasesyvariables.ListaPregutnasEncuestas,prenombre )
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'createDocumentoEncuesta')  

        # Crear logs de errores
        if len(clasesyvariables.logErrores) < 2 :
            clasesyvariables.logErrores.append("ESTE CURSO NO PRESENtA ANOMALIAS REGISTRADAS... Excelente")
        # Añadir nombre del curso a la lista de errores
        clasesyvariables.logErrores.append("#-----------#Fin Anomalias#-----------#") 
        AnomaliasFile = helpers.CreateErrorFile(clasesyvariables.logErrores,prenombre)
        t,tiempos = renew_time(t,medir_tiempo,tiempos,'CreateErrorFile')  

        listausr ="Lista usuarios: "
        for usrprint in clasesyvariables.usuarios:
            listausr += ","  + str(usrprint.username) + " "
        # print(listausr)

        # Subir a Drive
        if subirDrive:
            # Subir reporte a planillas input en Drive
            _,link_drive_archivo_salida = driveapi.uploadFile(archivoSalida, codigoCarpetaPlanillasInput, nombreReporteDrive,tipoPlanilla)
            # Subir registro de anomalias a drive
            driveapi.uploadFile(AnomaliasFile, codigodrive_anomalias, nombreAnomaliasDrive,tipoTxt)
            # Subir documento de encuesta a la carpeta en drive
            _,link_drive_archivo_encuesta = driveapi.uploadFile(archivoSalidaEncuesta, codigoCarpetaEncuesta, nombreEncuestaDrive,tipoPlanilla)
            t,tiempos = renew_time(t,medir_tiempo,tiempos,'uploadFile')  

        # Subir a plataforma datos
        if subirdatos:
            urldatos = "http://localhost:5000" if datoslocal else "http://localhost:5000" # Cambiar el valor del else.
            json_usuarioprueba = jsonUsuarioPrueba.replace('file:///', '')
            id_curso_base = datos_subida.buscar_o_crear_curso_base(listaUsuarios,json_usuarioprueba)
            id_seccion = datos_subida.buscar_o_crear_seccion(listaUsuarios, id_curso_base)

            # Subir las respuestas
            json_respuestas = jsonFile
            csv_oras = orafile
            csv_encuestas = archivoSalidaEncuesta
            # Hay que convertir el excel de encuestas a csv separado por comas
            read_file = pd.read_excel(csv_encuestas)
            read_file.to_csv(csv_encuestas[:-3]+"csv", index = None, header=True)
            csv_encuestas = csv_encuestas[:-3]+"csv"

            response = requests.post(
                    urldatos + "/respuestas/"+str(id_seccion),
                    files={'archivo_respuestas': open(json_respuestas,'rb')}
                    )
            if response.status_code != 200 :
                raise Exception("Error subiendo respuestas")

            # Subir oras
            response = requests.post(
                    urldatos + "/oras/"+str(id_seccion),
                    files={'json_respuestas': open(json_respuestas,'rb'), 'archivo_oras': open(csv_oras,'rb')}
                    )
            if response.status_code != 200:
                raise Exception("Error subiendo ORAs")

            # Subir encuestas
            response = requests.post(
                    urldatos + "/encuestas/"+str(id_seccion),
                    files={'archivo_encuestas': open(csv_encuestas,'rb')}
                    )
            if response.status_code != 200:
                raise Exception("Error subiendo encuestas")
            t,tiempos = renew_time(t,medir_tiempo,tiempos,'subida_datos')

        if medir_tiempo and current_user.is_admin:
            seg_response['tiempo_empleado'] = (round(time.time() - t_total,2))
            seg_response['tiempo_por_funcion'] = tiempos
            print(f"Fin: tiempo empleado: {(round(time.time() - t_total,2))} seg")

        seg_response['estado'] = f'ok, {200}'
        seg_response['archivo_salida_dir'] = archivoSalida.replace(os.getcwd(),'')
        seg_response['archivo_salida'] = os.path.basename(archivoSalida.replace(os.getcwd(),''))
        seg_response['archivo_salida_encuesta_dir'] = archivoSalidaEncuesta.replace(os.getcwd(),'')
        seg_response['archivo_salida_encuesta'] = os.path.basename(archivoSalidaEncuesta.replace(os.getcwd(),''))
        seg_response['config_ejecutada'] = config
        if current_user.is_admin and subirDrive:
            seg_response['archivo_salida_drive'] = link_drive_archivo_salida
            seg_response['archivo_encuesta_drive'] = link_drive_archivo_encuesta

        return seg_response
