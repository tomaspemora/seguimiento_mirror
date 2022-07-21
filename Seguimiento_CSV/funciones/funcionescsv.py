from asyncio import Task
import csv
import os
import io
from sqlite3 import Time
import time
import json
import string 
import sys
from io import StringIO

from . import clasesyvariables
from .clasesyvariables import usuario
from .clasesyvariables import pregunta
from .clasesyvariables import subpreguntaencuesta
from .clasesyvariables import ora

from flask_debugtoolbar_lineprofilerpanel.profile import line_profile


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

cantidadControles = 0
cantidadEncuestas = 0
cantidadTipoPreguntaEvaluada = 0
#totalPreguntasBuenasOMalas = {}
#totalPreguntasPorTaller = {}
totalPreguntasPorControl = {}
totalPreguntasEvaluadas = {}
totalPregutnasEncuestas = {}
totalEncuestas = {}
cantidadControles = 0
cantidadEncuestas = 0
cantidadTipoPreguntaEvaluada = 0
nombresEncuestas = []

def fields(ob):
    return csv.DictReader(ob).fieldnames[0]


def crearListaUsuarios(filelocation,file_obj=None):
    # print("Crear la lista de usuarios de " + filelocation )
    #time.sleep(5)
    File = filelocation

    nombres = []

    # print("Arvchivo: " + File)
    usuarioActual = ""
    # breakpoint()
    #clasesyvariables.usuarioPrueba.username = clasesyvariables.nombreUsuarioPrueba
    # with open(File, newline='', encoding="utf-8") as f: #recolectar nombres

    # if file_obj is None:
    #     f = open(File, newline='', encoding="utf-8")  #recolectar nombres
    # else:
    #     fstr = file_obj.read().decode("utf-8")
    #     f = file_obj

    #     # fs = io.TextIOWrapper(io.BufferedReader(file_obj), encoding="utf-8", name=file_obj.filename)
    #     breakpoint()
    #     ff = StringIO(file_obj)
    #     fs = io.TextIOWrapper(file_obj.stream, encoding='utf-8')
    #     f2 = open(File, newline='', encoding="utf-8")  #recolectar nombres

    first = True
    reader = csv.reader(file_obj)
    for row in reader:
        # print ("["+str(i) + "]: ")
        #Estos index se movieron en +1 porque antes no habia rut en la lista de usuarios
        user  = usuario()
        rut = row[0]
        verificador = 'x'
        #id_usr = row[1]
        username = row[2]
        email = row[4]
        nacimiento = row[7]

        #estilizar el rut
        if  len(rut)> 1:
            if rut[0] == ' ': #Elimino vacio si que hay
                rut = rut[1:]

            if rut[0] == '0': #Elimino el 0 si parte con uno
                rut = rut[1:]

            verificador = rut[-1]
            rut = rut[:-1]
            rut += "-"+ verificador

        else:
            rut="0-X"
            clasesyvariables.logErrores.append("El usuario " + username + " no tiene rut")
        #print ("NoMbRe:___" + nombre + "__")

        if ( (username  not in nombres) and (username != "username") ):
            # print (username  + " Vs. " + "username")
            if clasesyvariables.saltarPrimeriaLienaListaUsuarios is True and first is True :
                first = False
                # print("es la primera linea")
                ##time.sleep(4)
            else:
                nombres.append(username)
                # print("agregar " + username)
                user.RUT = rut
                user.nverificador = verificador
                user.username = username
                user.email = email
                if( email.find("@invalid.invalid") != -1 ):
                    clasesyvariables.logErrores.append('El usuario ' + str(user.nombre) + " tiene un correo invalido " + str(user.email)) 
                user.nacimiento = nacimiento
                clasesyvariables.usuarios.append(user)
                #time.sleep(1)
    if file_obj is None:
        f.close()
    # print("Usuarios: " + str(clasesyvariables.usuarios) )


def crearListaOra(oralocation,file_obj=None):
    # print("Leer CVS")
    first = True
    formatoNuevo = False
    listaOras = []

    # File = oralocation
    # with open(File,newline='',encoding="utf-8") as f:
    # breakpoint()
    reader= csv.reader(file_obj)
    for row in reader:
        # print(row)
        oratoadd = ora()

        #formato nuevo desde 2021
        if(formatoNuevo):
            oratoadd.submissioid = row[0]
            oratoadd.itemid = row[3]
            oratoadd.studentid = row[4]
            oratoadd.fecharespuesta = row[5]

            respuestatoadd = clasesyvariables.find_between(row[4],"{u'parts': [{u'text': u'","'}]}")
            oratoadd.respuesta = respuestatoadd
            oratoadd.fechacalificacion = row[9]
        else:
            oratoadd.submissioid = row[0]
            oratoadd.itemid = row[1]
            oratoadd.studentid = row[2]
            oratoadd.fecharespuesta = row[3]

            respuestatoadd = clasesyvariables.find_between(row[4],"{u'parts': [{u'text': u'","'}]}")
            oratoadd.respuesta = respuestatoadd
            oratoadd.fechacalificacion = row[7]
        
        if(first == True):
            first = False
            if(row[1] == "Location"):
                formatoNuevo = True
        else:
            if(formatoNuevo):
                if(str(row[10]) != ""):
                    oratoadd.score = int(row[10])
                    oratoadd.calificada = True
                else:
                    oratoadd.score = 0
                    oratoadd.calificada = False
                listaOras.append(oratoadd)
                #clasesyvariables.listaoras.append(oratoadd)
            else:
                if(str(row[8]) != ""):
                    oratoadd.score = int(row[8])
                    oratoadd.calificada = True
                else:
                    oratoadd.score = 0
                    oratoadd.calificada = False
                listaOras.append(oratoadd)
                #clasesyvariables.listaoras.append(oratoadd)

    return listaOras

def checkearNombreEncuestas(nombreencuesta,esUprueba):
    if(nombreencuesta not in clasesyvariables.usuarioPrueba.nombresEncuestas):
        # print("añadir nombre de encuesta " + nombreencuesta + " a la lista")
        if(esUprueba):
            clasesyvariables.usuarioPrueba.nombresEncuestas.append(nombreencuesta)
            return True
        else:
            clasesyvariables.logErrores.append(nombreencuesta + " no encontrada en el usuario de prueba " + str(clasesyvariables.usuarioPrueba.nombresEncuestas) )
            return False
    else:
        return True


def checkearNombreAsistencia(nombreasistencia,codigoasistencia,esUprueba):
    if(nombreasistencia not in clasesyvariables.usuarioPrueba.nombresAsistencias):
        print("evaluar si agrego nombre de encuesta " + nombreasistencia + " a la lista")
        if(esUprueba):
            #nombrecodigoasis = nombreasistencia + "_:_" + codigoasistencia  
            clasesyvariables.usuarioPrueba.nombresAsistencias.append(nombreasistencia)
            #time.sleep(5) 
            return True
        else:
            clasesyvariables.logErrores.append(nombreasistencia + " no encontrada en el usuario de prueba " + str(clasesyvariables.usuarioPrueba.nombresAsistencias) )
            return False
    else:
        return True



#####-----------------------Recorrido del Stutent-State-----------------------#####
@line_profile
def RecorrerCSV(fileLocation,usuarios,listadeoras,student_obj=None): 

    # print("Recorrer CVS")
    ##time.sleep(3)
    # breakpoint()
    File = fileLocation
    # print("File " + File)
    # with open(File, newline='', encoding="utf-8") as f:
    if student_obj == None:
        f = open(File, newline='', encoding="utf-8")  #recolectar nombres
    else:
        f = student_obj
    reader = csv.reader(f)
    completo = False
    for row in reader:
        # print(row)
        nombre = row[0]
        #print ("Nombre tomado del csv: " + nombre)
        ##time.sleep(3)
        for usr in usuarios:
            #print ("Nombre en la lista de usuarios " + usr.username )
            ##time.sleep(1)
            preg = pregunta()
            #if usr.username.lower().find(nombre.lower()) != -1: 
            #el nombre de usuario tiene que ser identico o puede encontrar un usuario dos veces
            if usr.username.lower() == nombre.lower(): 
                usuarioActual = nombre
                #print ("Lo encontre " + nombre + " VS " + usr.username)
                ##time.sleep(1)
                titulos= row[2].split(">")
                preg.curso = titulos[0]
                enunciadopreg = row[4]
                #rescon = row[5].lower() 

                preg.deTaller = False
                preg.esDeActividad  = False
                preg.esDeControl = False
                preg.moduloinicial = False
                preg.modulofinal = False
                preg.esDeEncuesta = False
                preg.reglamento = False
                preg.consentimiento = False

                yaesencuesta = False

                valida1Asist = False
                validaSitua = False

                # print(row[1].lower())

                if str(row[1].lower()).find("asistencia") != -1:
                    valida1Asist = True
                    # print("primera validación de asistencia" )

                if str(row[1].lower()).find("situación actual curso") != -1 or str(row[1].lower()).find("situacion actual curso") != -1 or str(row[1].lower()).find("situación actual") != -1 or str(row[1].lower()).find("situacion actual") != -1:
                    validaSitua = True


                if( len(titulos) > 1 ):

                    #ubicaciones 
                    loc1 = 1
                    loc2 = 2
                    loc3 = 3
                    loc4 = 4

                    #print("tamaño del arreglo titulos " + str(len(titulos)) )
                    if(len(titulos) == 5):
                        completo == True
                    elif(len(titulos) == 4):
                        loc1 = 0
                        loc2 = 1 
                        loc3 = 2
                        loc4 = 3
                        completo == False
                    elif(len(titulos) == 3):
                        loc1 = 0
                        loc2 = 0 
                        loc3 = 1
                        loc4 = 4

                    
                    subtitulo = str(titulos[loc2].lower())
                    if(subtitulo[0] == ' '):
                        #print("Tiene un espaciio en blanco")
                        subtitulo = subtitulo[1:]
                        ##time.sleep(1)

                    #subtitulo = quitarAcentos(subtitulo)

                    if( subtitulo.startswith("encuesta") ):
                        # print("Encontre la encuesta " + str(titulos[loc2]))
                        nombreencuesta = subtitulo

                        if nombreencuesta.lower().find("encuesta de la discusión") != -1 :
                            nombreencuesta = str(titulos[loc3])

                        preg.esDeEncuesta = True
                        preg.tallerNumero = -1
                        preg.numeroEncuesta = 0
                        preg.esunapreguntade = "Encuesta"

                        checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                        indexEncuesta = 0
                        if checkpregunta:
                            indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                        preg.esDeActividad = False

                        preg.numeroEncuesta = indexEncuesta + 1
                        yaesencuesta = True
                        preg.deTaller = False
                    

                    elif subtitulo.find("taller online") != -1:
                        
                        nombreencuesta = str(titulos[loc3])

                        if nombreencuesta.find("encuesta") != -1:

                            subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") #Reviso que no tenga la plabra encuesta sola
                            if(subnombreencuesta == "encuesta"):
                                nombreencuesta = "encuesta " + subtitulo

                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)

                            yaesencuesta = True
                            preg.esDeEncuesta = True
                            preg.esunapreguntade = "encuesta"

                            preg.numeroEncuesta = indexEncuesta + 1

                        preg.deTaller = False
                        preg.esDeActividad = False

                    elif subtitulo.find("taller sincrónico") != -1:
                        
                        nombreencuesta = str(titulos[loc3])

                        if nombreencuesta.find("encuesta") != -1:

                            subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") #Reviso que no tenga la plabra encuesta sola
                            if(subnombreencuesta == "encuesta"):
                                nombreencuesta = "encuesta " + subtitulo

                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)

                            yaesencuesta = True
                            preg.esDeEncuesta = True
                            preg.esunapreguntade = "encuesta"

                            preg.numeroEncuesta = indexEncuesta + 1

                        preg.deTaller = False
                        preg.esDeActividad = False


                    elif( subtitulo.find("discusión virtual") != -1):

                        nombreencuesta = str(titulos[loc3])
                        # print(nombreencuesta)
                        if nombreencuesta.find("encuesta") != -1:

                            subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") #Reviso que no tenga la plabra encuesta sola
                            if(subnombreencuesta == "encuesta"):
                                nombreencuesta = "encuesta " + subtitulo

                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)

                            yaesencuesta = True
                            preg.esDeEncuesta = True

                            preg.numeroEncuesta = indexEncuesta + 1

                        preg.deTaller = False
                        preg.esunapreguntade = "discusión"
                        preg.esDeActividad = False

                    elif( subtitulo.find("prueba de diagnóstico") != -1):
                        #print("titulo: " + str(titulos[loc2]) )
                        #print ("PRUEBA DE DIAGNÓSTICO")
                        preg.pretest = True
                        preg.tallerNumero = 1
                        #time.sleep(5)
                        preg.deTaller = False
                        preg.esunapreguntade = "pre-Test"
                        preg.moduloinicial = True
                        preg.esDeActividad = False
                        #print("Tenemos una pregunta de diagnóstico para" + usr.username ) 

                    elif( subtitulo.find("post-test") != -1):
                        #print("titulo: " + str(titulos[loc2]) )
                        #print ("PRUEBA DE DIAGNÓSTICO")
                        preg.postest = True
                        preg.tallerNumero = 1
                        #time.sleep(5)
                        preg.deTaller = False
                        preg.esunapreguntade = "post-Test"
                        preg.moduloFinal = True
                        preg.esDeActividad = False
                        #print("Tenemos una pregunta final para" + usr.username ) 

                    elif( subtitulo.find("consentimiento") != -1 ):
                        #print("encontre el consentimiento: " + str(titulos[loc2]) )
                        preg.consentimiento = True
                        #preg.tallerNumero = 1
                        ##time.sleep(5)
                        preg.deTaller = False
                        preg.esunapreguntade = "consentimiento"
                        preg.moduloinicial = True
                        preg.esDeActividad = False
                        #print("Tenemos un consentimiento para" + usr.username ) 

                    elif( subtitulo.startswith("reglamento") == True):
                        # print("encontre el reglamento: " + str(titulos[loc2]) )
                        preg.reglamento = True
                        #preg.tallerNumero = 1
                        preg.deTaller = False
                        preg.esunapreguntade = "reglamento"
                        preg.moduloinicial = True
                        preg.esDeActividad = False

                    tallerNombre = titulos[loc1]
                    actividadNombre = titulos[loc2]
                    preg.tallerNombre = tallerNombre
                    preg.actividadNombre = actividadNombre

                    numerosEnTaller = [int(i) for i in tallerNombre if i.isdigit()]
                    if(len(numerosEnTaller)>0):
                        # print(tallerNombre +" numeros en taller " + str(numerosEnTaller))
                        preg.esunapreguntade = "Taller" 
                        if(preg.esDeControl):
                            preg.esunapreguntade = "Control" 
                            preg.numerocontrol = preg.tallerNumero
                            preg.deTaller = False
                        elif(preg.esDeEncuesta):
                            preg.esunapreguntade = "Encuesta" 
                            preg.deTaller = False

                        preg.tallerNumero = numerosEnTaller[0]
                        preg.deTaller = True
                        preg.textoUbicacion = "T" + str(preg.tallerNumero)
                        preg.tallerNombre = tallerNombre.replace("Taller " + str(numerosEnTaller[0]) + ": " , "")
                    else:
                        #print("No tiene numero en el taller")
                        preg.tallerNumero = -1
                        preg.deTaller = False

                        
                    actividadNombre = titulos[loc2]
                    preg.actividadNombre = actividadNombre
                    numerosEnActividad =  [int(i) for i in actividadNombre if i.isdigit()]
                    if(len(numerosEnActividad)>0):
                        preg.actividadNumero = numerosEnActividad[0]
                        preg.actividadNombre = actividadNombre.replace("Actividad "+ str(numerosEnActividad[0]) + ": ", "")
                        preg.esDeActividad = True
                        preg.deTaller = True

                        # print("actividad numero:")
                        # print(preg.actividadNumero)
                        if preg.actividadNumero:
                            preg.textoUbicacion  += "A" + str(preg.actividadNumero)
                        else:
                            preg.textoUbicacion = "A-1"
                    else:
                        #print("No tiene numero en la actividad")
                        preg.actividadNumero = -1

                    
                    preg.pagina = titulos[loc3] #Pagina

                    recap = False
                    
                    if (preg.pagina.lower()).find("control") != -1 :
                        #print (preg.pagina.lower() + " contiene la palabra control")
                        preg.esDeControl = True
                        preg.paginaNumero = 0
                        preg.deTaller = False
                        preg.esunapreguntade = "control"
                

                    if (preg.pagina.lower()).find("recapitulemos") != -1 :
                        #print (preg.pagina.lower() + " contiene la palabra recapitulemos")
                        #preg.esDeControl = True
                        preg.deTaller = False
                        recap = True
                        preg.esunapreguntade = "recapitulemos"

                    if (preg.pagina.lower()).find("prueba de diagnóstico") != -1 :
                        #print (preg.pagina.lower() + " contiene la palabra prueba de diagnóstico")
                        preg.pretest = True
                        preg.tallerNumero = 1
                        #time.sleep(5)
                        preg.deTaller = False
                        preg.esunapreguntade = "pre-test"
                        #print("Tenemos una pregunta pretest para" + usr.username ) 

                    if (preg.pagina.lower()).find("post-test") != -1 :
                        #print (preg.pagina.lower() + " contiene la palabra prueba de diagnóstico")
                        preg.postest = True
                        preg.tallerNumero = 1
                        #time.sleep(5)
                        preg.deTaller = False
                        preg.esunapreguntade = "post-test"
                        #print("Tenemos una pregunta final para" + usr.username ) 


                    if (preg.pagina.lower()).find("pregunta calificada") != -1 or (preg.pagina.lower()).find("pregunta evaluada") != -1:
                        #print (preg.pagina.lower() + " contiene la palabra pregunta calificada")
                        #preg.esDeControl = True
                        #preg.esDeControl = True
                        preg.deTaller = False
                        preg.preguntaEvaluada = True
                        preg.esunapreguntade = "preguntas calificadas"


                    if(preg.pagina.lower()).find("consentimiento") != -1:
                        #print ("Pagina " + preg.pagina.lower() + " contiene la palabra consentimiento")
                        preg.consentimiento = True
                        preg.deTaller = False
                        preg.esunapreguntade = "consentimiento"

                    if(preg.pagina.lower()).find("firma reglamento") == True:
                        # print ("Pagina "+ preg.pagina.lower() + " contiene la palabra reglamento")
                        preg.reglamento = True
                        preg.deTaller = False
                        preg.esunapreguntade = "reglamento"
                        if(preg.tallerNumero > 0):
                            print("Pregunta " + str(preg.tallerNombre) + " N:" + str(preg.tallerNumero) +" ("+ str(preg.textoUbicacion) +") " + str(preg.respuesta) )
                            time.sleep(10)

                    if yaesencuesta == False: #Segunda verificación si me encuentro ante una encuesta

                        if(str(preg.pagina.lower()) == "encuesta"):
                            preg.deTaller = False
                            preg.esDeEncuesta = True
                            preg.esunapreguntade = "encuesta"

                        if(preg.pagina.lower()).find("encuesta página") != -1 or (preg.pagina.lower()).find("encuesta taller") !=-1:
                            #print (preg.pagina.lower() + " contiene la palabra encuesta")
                            preg.deTaller = False
                            preg.esDeEncuesta = True
                            preg.esunapreguntade = "encuesta"
                            #time.sleep(3)

                        if (preg.pagina.lower()).find("encuesta taller online") !=-1 and yaesencuesta == False:
                            nombreencuesta = preg.pagina
                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                            yaesencuesta = True
                            preg.numeroEncuesta = indexEncuesta + 1

                        if (preg.pagina.lower()).find("encuesta taller sincrónico") !=-1 and yaesencuesta == False:
                            nombreencuesta = preg.pagina
                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                            yaesencuesta = True
                            preg.numeroEncuesta = indexEncuesta + 1

                        if (preg.pagina.lower()).find("encuesta discusión virtual") !=-1 and yaesencuesta == False:
                            nombreencuesta = preg.pagina
                            checkpregunta = checkearNombreEncuestas(nombreencuesta,usr.usuarioprueba)
                            if checkpregunta:
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                            yaesencuesta = True
                            preg.numeroEncuesta = indexEncuesta + 1

                    if(recap == False and preg.esDeControl == False and preg.esDeEncuesta == False and preg.preguntaEvaluada == False and preg.consentimiento == False and preg.reglamento == False):
                        paginatext = titulos[loc3].split('#')
                        #print("Títulos "+ str(titulos) +" paginatext: " + str(paginatext) )
                        if(len(paginatext) > 1):
                            preg.paginaNumero = int(paginatext[1])
                            preg.textoUbicacion  += "#" + paginatext[1]
                            preg.deTaller = True
                        #else:
                            ##time.sleep(1)

                    preg.textoUbicacion = str(preg.esunapreguntade) +"_" + str(preg.textoUbicacion)


                    if len(row) > 6 :
                        preg.blockKeyCompleto = row[7]

                        blockkeyArray = row[7].split('@')
                    else:
                        preg.blockKeyCompleto = "SIN blockkey"
                        blockkeyArray = []

                    #print ("Blockkey Array: " + str(blockkeyArray))

                    if len(blockkeyArray) > 1 :
                        preg.tieneBlockkey = True
                    else:
                        preg.tieneBlockkey = False
                        #print("ERROR en el blockkey REVISE LOS PUNTO Y COMA")
                        ##time.sleep(6)


                    idRespuesta = ""
                    contestado = False

                    if(preg.tieneBlockkey):

                        preg.blockKey = blockkeyArray[0]
                        preg.tipo = blockkeyArray[1]
                        preg.codigo = blockkeyArray[2]

                        #Asignar tipo si le falta
                        tipo = preg.tipo

                        #print ("ususario " + usr.nombre + " tiene " + str(len(usr.preguntas)) )
                        ##time.sleep(1)
                        #print("row[8]: " + str(row[8]))
                        if  (str(row[8])).lower() != "none" :
                            loaded_json = json.loads(row[8])
                            #print("Json:")
                            #print(loaded_json)
                            #print("Values: ")
                            #for key, value in loaded_json.items():
                                #print (key +" : "+ str(value))

                            if("correct_map" in loaded_json):
                                contestado = True


                            #print("\n revisar si tiene intentos...") 
                            if(loaded_json.get("attempts")):
                                #print("si tiene intentos")
                                preg.intentos = loaded_json["attempts"]
                                contestado = True

                            #print("\n revisar si tiene Score...")
                            if(loaded_json.get("score")):
                                #print ("esta pregunta tiene score")
                                if( str(loaded_json["score"])[0] != '{' ):
                                    preg.score = loaded_json["score"]

                            else:
                                if (preg.pretest or preg.postest or preg.esDeControl or preg.preguntaEvaluada):
                                    #preg.score = -2
                                    clasesyvariables.logErrores.append("la pregunta " + preg.blockKeyCompleto+ " contestada por " + usuarioActual + " no tiene score, es una " + preg.esunapreguntade )
                                

                            if( tipo.lower().find("problem+block") != -1):
                                #print("\n es un problem block")

                                preg.multipleRespuesta = False
                                
                                interactivo = False
                                if(row[3] != ""):
                                    #print("row " + str(row) )
                                    #print(" ")
                                    #print("json " + str(loaded_json) )
                                    #if(preg.deTaller == False):
                                        #print("Sí es un caso especial")
                                        ##time.sleep(3)
                                    preg.idrespuesta = row[3]
                                    idRespuesta = row[3]
                                    preg.respuestaCorrecta = row[6]
                                    if "last_submission_time" in loaded_json:
                                        preg.fechaRespuesta = loaded_json["last_submission_time"]

                                    resopu = row[5]

                                    addfromList= False

                                    #print("resopu " + str(resopu))

                                    if( len(resopu) > 1 and resopu[0:2] != '{"' ):
                                        preg.respuesta = row[5]
                                        #print ("Se guardo respuesta rapida")
                                    else:
                                        #print("No hay respuesta rapida")
                                        preg.respuesta = "Presumiblemente RECURSO INTERACTIVO"
                                        addfromList= True
                                        interactivo = True
                                    

                                    #if ("correct_map" not in loaded_json):
                                        #print ("NO TIENE CORRECT MAP")

                                    #if("student_answers" not in loaded_json):
                                        #print ("NO TIENE STUDENT ANSWERS")

                                    ##time.sleep(5)
                                    if ( ("correct_map" not in loaded_json) and ("student_answers" not in loaded_json)):
                                        interactivo = True
                                        #print("pregunta " + preg.codigo + " es un recurso interactivo")
                                        preg.respuesta += "No se entonctro respuesta en el json"
                                        ##time.sleep(3)

                                    #print ("id respuesta: " + idRespuesta + " " + str(loaded_json[idRespuesta]))
                                    #print (" cantidad de respuestas " + str(len(loaded_json["student_answers"][idRespuesta])) )
                                    cantrespuestas = len(loaded_json["student_answers"][idRespuesta])
                                    #print (" student answers: " + str(loaded_json["student_answers"][idRespuesta]))
                                    #print (" correctness: " + str(loaded_json[idRespuesta]))
                                    
                                    ##time.sleep(30)

                                    if( isinstance( loaded_json["student_answers"][idRespuesta] ,list ) ):
                                        #print("hay mas de una respuesta")
                                        for resp in loaded_json["student_answers"][idRespuesta]:
                                            preg.respuestas.append(resp)
                                            if(addfromList and cantrespuestas >0):
                                                preg.respuesta = "_"
                                                preg.respuesta += str(resp) + "_"
                                    else:
                                        preg.respuestas.append(loaded_json["student_answers"][idRespuesta])
                                        if(addfromList and cantrespuestas >0):
                                            preg.respuesta = "_"
                                            resp1 = loaded_json["student_answers"][idRespuesta]
                                            preg.respuesta += str(resp1) + "_"

                                    
                                    if("correct_map" in loaded_json):
                                        contestado = True
                                        correcta = loaded_json["correct_map"][idRespuesta]["correctness"]
                                        #print ("evaluar la respuesta " + str(correcta))

                                        if(correcta == "correct"):
                                            #print (idRespuesta + " es correcta")
                                            preg.esCorrecta = True
                                            preg.score = 12
                                        else:
                                            #print (idRespuesta + " NO esta correcta")
                                            preg.esCorrecta = False
                                            preg.score = 0
                                    #else:
                                        #print("no esta la respuesta, pero no debería entrar aquí")
                                        ##time.sleep(3)
                                        #contestado = False


                                    if ("has_saved_answers" in loaded_json):
                                        contestado = False 
                                                                    
                                else:
                                    #print("no esta la respuesta " + row[3])
                                    preg.respuesta = "Respuesta no existente"
                                    contestado = False
                                    #time.sleep(3)


                                for precheck in usr.preguntas:
                                    #print ("block key [" + preg.o
                                    if(precheck.blockKeyCompleto == preg.blockKeyCompleto and contestado):
                                        #print ("esta repetido el block key [" + preg.blockKeyCompleto +"] para el usuario " + usr.nombre)
                                        ##time.sleep(1)
                                        #print ("id respuesta [" + precheck.idrespuesta + "] VS [" + preg.idrespuesta +"]")
                                        if(preg.esCorrecta == False):
                                            precheck.esCorrecta = False
                                            precheck.nincorrectas +=1
                                        else:
                                            precheck.ncorrectas += 1
                                        
                                        precheck.cantidaddeveces +=1
                                        
                                        contestado = False
                                        ##time.sleep(5)


                            if(tipo == "vof+block"):
                                #print("\n es un verdadero y falso")
                                cantresp = 0
                                resp = ""
                                contestado = True
                                #print ("respuestas")
                                #print (loaded_json["respuestas"])
                                for reskey, valkey in loaded_json["respuestas"].items():
                                    cantresp +=1
                                    #print(reskey + ":" + str(valkey))
                                    preg.respuestas.append(valkey)
                                    resp += ( valkey +"_")
                                if(len(resp) > 1): resp = resp[:-1]
                                preg.respuesta = resp

                                if(loaded_json["score"] == 1):
                                    preg.esCorrecta = True
                                    preg.score = 12
                                else:
                                    preg.esCorrecta = False
                                    preg.score = 12 * float(loaded_json["score"])

                                preg.idrespuesta = clasesyvariables.find_id(preg.blockKey,'@')

                            if(tipo == "freetextresponse+block"):
                                #print("\n es un free text")
                                contestado = True
                                preg.idrespuesta = clasesyvariables.find_id(preg.blockKey,'@')
                                #preg.intentos =  loaded_json["count_attempts"]
                                preg.respuesta = loaded_json["student_answer"]
                                if( isinstance( loaded_json["student_answer"] ,list ) ):
                                    #print("hay mas de una respuesta")
                                    for resp in loaded_json["student_answer"]:
                                        preg.respuestas.append(resp)
                                    else:
                                        preg.respuestas.append = loaded_json["student_answer"]
                                preg.esCorrecta = None
                                if(loaded_json.get("count_attempts")):
                                    preg.intentos = loaded_json["count_attempts"]


                            if(tipo == "openassessment+block"):
                                #print ("pregunta con ORA ORA ORA...")
                                contestado = True
                                preg.tipoOra = True
                                if("submission_uuid" in loaded_json):
                                    submiid = loaded_json["submission_uuid"]
                                    contestado = True
                                else:
                                    submiid  = "No existo"
                                    #print("No encontre submission_uuid en el json de " + preg.blockKeyCompleto)
                                    ##time.sleep(20)
                                    contestado = False
                                #print ("submisionid " + str(submiid))
                                for ora in listadeoras:
                                    if(str(ora.submissioid) == str(submiid)):
                                        #print ("Lo encontre " + str(ora.submissioid) + " VS. " + str(submiid) )
                                        preg.oraCode = submiid
                                        contestado = True
                                        preg.score = ora.score
                                        preg.fechaRespuesta = ora.fecharespuesta
                                        preg.respuesta = ora.respuesta
                                        if(ora.score > 7):
                                            preg.esCorrecta = True
                                            #preg.score = 12
                                        else:
                                            preg.esCorrecta = False
                                            #preg.score = ora.score
                                            #preg.score = 0
                                        preg.score = max(0,min(12,ora.score))
                                        if ( int(preg.score) != 0 and int(preg.score) != 4 and int(preg.score) != 8 and int(preg.score) != 12 ):
                                            clasesyvariables.logErrores.append( "pregunta "+ preg.codigo +" tiene un puntaje ORA animalo " + str(preg.score) )
                                        
                                ##time.sleep(10)

                            if(tipo == "dialogsquestionsxblock+block"):
                                #print("\n es un dialogo question")
                                contestado = True
                                preg.idrespuesta = clasesyvariables.find_id(preg.blockKey,'@')
                                respu = ""
                                for resp in loaded_json["student_answers"]:                                        
                                    preg.respuestas.append(resp)
                                    respu += resp + "_"
                                if(len(respu) > 1): respu = respu[:-1]
                                preg.respuesta = respu

                                if(loaded_json["score"] == 1):
                                    preg.esCorrecta = True
                                else:
                                    preg.esCorrecta = False

                            if(tipo == "drag-and-drop-v2+block"):
                                contestado = True
                                #print("\n es un drag and drop")
                                if(loaded_json.get("attempts")):
                                    preg.intentos = loaded_json["attempts"]
                                buena = True
                                respu = ""
                                for item in loaded_json["item_state"]:                                        
                                    preg.respuestas.append( loaded_json["item_state"][item]["zone"]  )
                                    respu += loaded_json["item_state"][item]["zone"] +"_"
                                    if (  loaded_json["item_state"][item]["correct"] == False ):
                                        buena = False
                                if(len(respu) > 1): respu = respu[:-1]    
                                preg.respuesta = respu
                                preg.esCorrecta = buena
                                preg.idrespuesta = clasesyvariables.find_id(preg.blockKey,'@')


                            if(tipo == "eollistgrade+block"):

                                preg.score = str(loaded_json["student_score"])
                                preg.respuesta = str(loaded_json["student_score"]) +"_"+ loaded_json["comment"]
                                preg.respuestas = [ preg.respuesta,loaded_json["comment"] ]
                                contestado = True

                                # print("Encontre una lista de evaluación")
                                # print(str(loaded_json))

                                time.sleep(5)
                               
                                if valida1Asist:
                                    # print("es una asistencia")
                                    
                                    preg.esAsistencia = True
                                    preg.deTaller = False

                                    subnombreasistencia = preg.tallerNombre +"_"+ preg.actividadNombre
                                    nombrefinalasistencia = subnombreasistencia

                                    if( ( subnombreasistencia.lower() ).find("discusión virtual") != -1 or ( subnombreasistencia.lower() ).find("discusion virtual") != -1 ):
                                        # print("encontre discusión virtual")
                                        arrnumdv = [int(i) for i in  (  preg.tallerNombre.lower() ).split() if i.isdigit()]
                                        numerdv = 0
                                        if len(arrnumdv) > 0:
                                            numerdv = arrnumdv[0]

                                        nombrefinalasistencia = "DV_" + str(numerdv)
                                                                            
                                    elif( ( subnombreasistencia.lower() ).find("bienvenida") != -1 ):
                                        # print("encontre bienvenida")
                                        nombrefinalasistencia = "TB"


                                    elif( ( subnombreasistencia.lower() ).find("formato de controles") != -1 ):
                                        # print("encontre formato controles")
                                        nombrefinalasistencia = "PFC"

                                    elif( ( subnombreasistencia.lower() ).find("taller sincrónico") != -1 or ( subnombreasistencia.lower() ).find("taller sincronico") != -1 ):

                                        arrnumts = [int(i) for i in  (  preg.tallerNombre.lower() ).split() if i.isdigit()]
                                        numerts = 0
                                        if len(arrnumts) > 0:
                                            numerts = arrnumts[0]
                                        # print("encontre taller sincronico " + str(numerts))
                                        nombrefinalasistencia = "TS_" + str(numerts)

                                    preg.respuesta = "Asistencia:__" + nombrefinalasistencia + "__" + str(loaded_json["student_score"]) +"__"+ loaded_json["comment"] + "__"
                                    checkpreguntaasist = checkearNombreAsistencia(nombrefinalasistencia,preg.codigo,usr.usuarioprueba)
                                    
                                    time.sleep(6)
                                    # print(nombrefinalasistencia)
                                    preg.nombreAsistencia = nombrefinalasistencia

                                
                                elif validaSitua:
                                    contestado = True
                                    preg.deTaller = False
                                    # print("es el estado del estudiante")
                                    usr.situacionactual = int(loaded_json["student_score"])
                                    preg.score = str(loaded_json["student_score"])
                                    preg.respuesta = "Situación Actual:__" + str(loaded_json["student_score"])+"__"
                                    preg.respuestas = str(loaded_json["student_score"])

                            preg.contestado = contestado
                            
                            if(preg.esDeEncuesta):
                                preg.deTaller = False
                                if( str(titulos[loc3]).find("#") > 0):
                                    preg.paginaNumero
                                    paginatext = titulos[loc3].split('#')
                                    if(len(paginatext) > 1):
                                        preg.paginaNumero = int(paginatext[1])

                                #print("blockey compelto de la encuesta " + str(preg.blockKeyCompleto))

                                if(str(preg.idrespuesta).find("_") > 0):
                                    identificatorios = preg.idrespuesta.split('_')
                                    # print(str(identificatorios))
                                    #time.sleep(5)


                            if preg.consentimiento and ( enunciadopreg.find("NOMBRE") != -1 or enunciadopreg.find("RUT") != -1 ):
                                contestado = False


                            if preg.consentimiento and preg.respuesta.lower().find("no acepto") != -1:
                                clasesyvariables.logErrores.append("El usuario " + usr.username + " Conteso NO en el Consentimiento")
                                preg.respuesta = '0'
                            elif preg.consentimiento and preg.respuesta.lower().find("acepto") != -1:
                                preg.respuesta = '1'


                            if preg.reglamento == True and preg.respuesta.lower().find("declaro") != -1:
                                #preg.respuesta = "Declaro conocer y aceptar"
                                preg.respuesta = '1'


                            #Revisar si el usuario de prueba tiene estta pregunta
                            blockkey_encontrado = False
                            for preguntaUprueba in clasesyvariables.usuarioPrueba.preguntas:
                                if preg.codigo == preguntaUprueba.codigo:
                                    blockkey_encontrado = True 
                                    preg.latieneusuariodeprueba =True

                            if(usr.usuarioprueba):
                                blockkey_encontrado = True
                                    
                            #if(contestado and  recap == False and preg.consentimiento == False and preg.reglamento == False  and preg.esDeControl == False and preg.esDeEncuesta == False and preg.modulofinal == False and preg.moduloinicial == False):
                            #    preg.deTaller = True
                            
                            if(contestado and blockkey_encontrado == False and  recap == False and preg.consentimiento == False and preg.reglamento == False ):
                                clasesyvariables.logErrores.append("la pregunta: " + preg.blockKeyCompleto + " de "+ preg.esunapreguntade + ", contestada por " + usuarioActual + " no se encontro en el usuario de prueba ") 

                            if(contestado and blockkey_encontrado and recap == False):
                                #print ("Agragar pregunta " + preg.pagina + " " + preg.blockKey + " a " + usr.username)
                                
                                usr.preguntas.append(preg) 

                                
                                if(tipo == "problem+block"): usr.totalPreguntasPBlock += 1
                                if(tipo == "vof+block"): usr.totalPreguntasVF += 1
                                if(tipo == "freetextresponse+block"): usr.totalPreguntasFreeResp += 1
                                if(tipo == "dialogsquestionsxblock+block"): usr.totalPreguntasDiaQues += 1
                                if(tipo == "drag-and-drop-v2+block"): usr.totalPreguntasDragDrop += 1
                               


                                if(preg.esCorrecta):
                                    usr.totalBuenas += 1
                                elif (preg.esCorrecta == False):
                                    usr.totalMalas += 1
                                else:
                                    usr.totalPreguntasFreeResp += 1

                                
                                if(preg.esDeEncuesta == True):
                                    if preg.numeroEncuesta not in usr.totalEncuestas:
                                        usr.totalEncuestas[preg.numeroEncuesta] = 1
                                        usr.cantidadEncuestas += 1
                                    else:
                                        usr.totalEncuestas[preg.numeroEncuesta] += 1

                                if(preg.preguntaEvaluada == True):
                                    preg.numerocontrol = preg.tallerNumero
                                    if preg.tallerNumero not in usr.totalPreguntasEvaluadas:
                                        usr.totalPreguntasEvaluadas[preg.tallerNumero] = 1
                                        usr.cantidadTipoPreguntaEvaluada += 1
                                    else:
                                        usr.totalPreguntasEvaluadas[preg.tallerNumero] += 1
                            
                                if(preg.esDeControl == True):
                                    preg.numerocontrol = preg.tallerNumero
                                    if preg.tallerNumero not in usr.totalPreguntasPorControl:
                                        usr.totalPreguntasPorControl[preg.tallerNumero] = 1
                                        usr.cantidadControles += 1
                                    else:
                                        usr.totalPreguntasPorControl[preg.tallerNumero] += 1

                                if(preg.pretest):
                                    usr.totalpretest +=1

                                if(preg.postest):
                                    usr.totalpostest +=1
                        

                                #guardare cuantas ha respondido por taller-actividad
                                if(preg.esDeControl == False and preg.deTaller and preg.tallerNumero > 0  ):
                                    if preg.tallerNumero not in usr.totalPreguntasPorTaller:
                                        usr.totalPreguntasPorTaller[preg.tallerNumero] = {}
                                        usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero] = {} # no contempla preguntas abiertas
                                        usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero] = {}
                                        usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero] = {} #contempla preguntas abiertas

                                    if preg.actividadNumero not in usr.totalPreguntasPorTaller[preg.tallerNumero]:
                                        usr.totalPreguntasPorTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        #usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero][preg.actividadNumero]= 1
                                    else:
                                        usr.totalPreguntasPorTaller[preg.tallerNumero][preg.actividadNumero] += 1
                                        #usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero][preg.actividadNumero]+= 1

                                    if(preg.esCorrecta == True):
                                        if( preg.actividadNumero not in usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero]):
                                            usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        else:
                                            usr.totalPreguntasCorrectasPorTaller[preg.tallerNumero][preg.actividadNumero] += 1

                                        if (preg.actividadNumero not in usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero]):
                                            usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        else:
                                            usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero][preg.actividadNumero] += 1

                                        if(preg.actividadNumero not in usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero]):
                                            usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        else:
                                            usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero][preg.actividadNumero] += 1
                                            
                                    elif (preg.esCorrecta == False):
                                        if(preg.actividadNumero not in usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero]):
                                            usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        else:
                                            usr.totalPreguntasBuenasOMalasPorTaller[preg.tallerNumero][preg.actividadNumero] += 1

                                    elif (preg.esCorrecta == None):
                                        if (preg.actividadNumero not in usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero]):
                                            usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero][preg.actividadNumero] = 1
                                        else:
                                            usr.totalPreguntasBuenasEnviadasTaller[preg.tallerNumero][preg.actividadNumero] += 1

                                    usr.totalConTaller += 1 
                            

                                #Parte sacada del usuario de prueba
                                
                                #print ("Agragar pregunta " + preg.pagina + " " + preg.blockKey + " a " + usr.username)
                                #if(preg.deTaller == False and preg.esDeControl == False):
                                ##time.sleep(3)
                                """
                                #esto sirvio para ver cuando estaba guardando dos veces una preg en un usuario lo dejo por si acaso
                                for p in usr.preguntas:
                                    if p.codigo == preg.codigo:
                                        print("Estoy repitiendo "+preg.codigo+" para "+usr.username+" "+preg.blockKeyCompleto)
                                        print(row)
                                        time.sleep(5)
                                        break
                                """

                                if(preg.fechaRespuesta != None ):
                                    
                                    #print ( "fecha tomada " + str(preg.fechaRespuesta)) #
                                    #fechaTomada = datetime.strptime(preg.fechaRespuesta, '%Y-%m-%dT%H:%M:%SZ')
                                    fechaTomada = preg.fechaRespuesta 

                                    if(usr.ultimaconexion == None):
                                        usr.ultimaconexion = fechaTomada
                                    else:
                                        #print (str(fechaTomada) + " -VS- " + str(usr.ultimaconexion) )
                                        #print("formato fecha tomada " + str(type(fechaTomada)) )
                                        #print("formato fecha ultima conexion " +  str(type(usr.ultimaconexion))  )
                                        if( fechaTomada > usr.ultimaconexion ):
                                            #print("La fecha obtenida es MAYOR a la guardada")
                                            usr.ultimaconexion = fechaTomada
                                
                                ##time.sleep(10)
                            #if str(usr.username.lower()).find(nombreUsuarioPrueba.lower()) != -1 :
                             #   usuarioPrueba.preguntas.append(preg)
                              #  print("Añadrir pregunta al usuario de prueba " + preg.codigo)
                                ##time.sleep(3)
                            ##time.sleep(12)

            if usr.usuarioprueba == True:
                usr.totalPregutnasEncuestas = totalPregutnasEncuestas
                usr.nombresEncuestas = clasesyvariables.usuarioPrueba.nombresEncuestas
                usr.nombresAsistencias = clasesyvariables.usuarioPrueba.nombresAsistencias
                usr.cantidadControles = len(usr.totalPreguntasPorControl)
                usr.totalContestadas = len(usr.preguntas)

                '''
                if(usr.totalpretest < 1):
                    usr.totalpretest = 10
                
                if(usr.totalpostest < 1):
                    usr.totalpostest = 10
                '''
                            ##time.sleep(3)
                        

                    #print("")
                ##time.sleep(10)

        #print(" pasar a la siguiente fila")    
        ##time.sleep(2)
# print (" Recorrido ")
    
def RecorrerCSVParaEncuesta(fileLocation,usuarios,student_obj=None): 
    # print("Recorrer CVS en busca de preguntas de encuestas")
    ##time.sleep(3)

    File = fileLocation
    # with open(File, newline='', encoding="utf-8") as f:
    f = student_obj
    reader = csv.reader(f)
    completo = False
    for row in reader:
        if(len(row) > 6 ):
            nombre = row[0]
            #print ("Nombre tomado del csv: " + nombre)
            ##time.sleep(3)
            for usr in usuarios:
                #print ("Nombre en la lista de usuarios " + usr.username )
                ##time.sleep(1)
                if usr.username.lower() == nombre.lower() : 
                    #usuarioActual = nombre
                    #print ("Lo encontre " + nombre + " VS " + usr.username)
                    ##time.sleep(1)
                    titulos= row[2].split(">")

                    if( len(titulos) > 1 ):

                        #ubicaciones 
                        loc1 = 1
                        loc2 = 2
                        loc3 = 3
                        loc4 = 4

                        #print("tamaño del arreglo titulos " + str(len(titulos)) )
                        if(len(titulos) == 5):
                            completo == True
                        elif(len(titulos) == 4):
                            loc1 = 0
                            loc2 = 1 
                            loc3 = 2
                            loc4 = 3
                            completo == False
                        elif(len(titulos) == 3):
                            loc1 = 0
                            loc2 = 0 
                            loc3 = 1
                            loc4 = 4

                        
                        subtitulo = str(titulos[loc2].lower())
                        if(subtitulo[0] == ' '):
                            #print("Tiene un espaciio en blanco")
                            subtitulo = subtitulo[1:]
                            ##time.sleep(1)

                        nombreencuesta= ""
                        soyencuesta = False

                        if( subtitulo.startswith("encuesta") ):
                            #print("Encontre la encuesta " + str(titulos[loc2]))
                            nombreencuesta = subtitulo
                            soyencuesta = True

                            if(nombreencuesta.find("encuesta de la discusión") != -1):
                                nombreencuesta = "encuesta " + (titulos[loc1]).lower()

                        elif subtitulo.find("taller online") != -1:
                        
                            nombreencuesta = str(titulos[loc3])

                            if (nombreencuesta.lower()).find("encuesta") != -1:
                                subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") 

                                if(subnombreencuesta == "encuesta"): #Reviso que no tenga la plabra encuesta sola
                                    nombreencuesta = "encuesta " + subtitulo

                                soyencuesta = True

                            #time.sleep(5)

                        elif( subtitulo.find("discusión virtual") != -1):

                            nombreencuesta = str(titulos[loc3])
                            
                            if (nombreencuesta.lower()).find("encuesta") != -1:
                                subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") 

                                if(subnombreencuesta == "encuesta"): #Reviso que no tenga la plabra encuesta sola
                                    nombreencuesta = "encuesta " + subtitulo

                                soyencuesta = True

                            
                            #time.sleep(5)

                        if  soyencuesta:

                            #print(nombreencuesta + " VS " + str(clasesyvariables.usuarioPrueba.nombresEncuestas) )
                            
                            
                            pregencuesta = subpreguntaencuesta()

                            if(nombreencuesta in clasesyvariables.usuarioPrueba.nombresEncuestas):
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                                numeroEncuesta = indexEncuesta + 1
                            else:
                                numeroEncuesta = -1
                    
                            paginaNumero = 0
                            if( str(titulos[loc3]).find("#") > 0):
                                paginatext = titulos[loc3].split('#')
                                if(len(paginatext) > 1):
                                    paginaNumero = int(paginatext[1])

                            tipo = row[1]
                            idrespuesta = row[3]
                            nombrepregunta = row[4]
                            respuesta = row[5]
                            arrayresp = row[6]

                            if(tipo == 'freetextresponse'):
                                nombrepregunta = "p_abierta"
                                loaded_json = json.loads(row[8])
                                if("student_answer" in loaded_json):
                                    respuesta = loaded_json['student_answer']

                            blockkeyArray = row[7].split('@')
                            if(len(blockkeyArray) > 1 ):
                                blockKeyCompleto = row[7]
                                blockKey = blockkeyArray[0]
                                blockTipo = blockkeyArray[1]
                                blockkeyArray[2]

                            #idrespuesta = find_id(blockKey,'@')


                            if(str(idrespuesta).find("_") > 0):
                                identificatorios =idrespuesta.split('_')
                                # print(nombrepregunta)
                                # print(str(identificatorios))
                                ##time.sleep(5)
                                pregencuesta.numeroidentificatorio1 = identificatorios[1]
                                if(len(identificatorios) > 2):
                                    pregencuesta.numeroidentificatorio2 = identificatorios[2]

                            if("otro" not in nombrepregunta and "OTRO" not in nombrepregunta 
                            and 
                            ("chbx" in nombrepregunta 
                            or "p3_2" in nombrepregunta
                            or "p3_4" in nombrepregunta
                            or "p4_4" in nombrepregunta
                            or "p4_8" in nombrepregunta
                            or "p5_2" in nombrepregunta
                            or "p5_5" in nombrepregunta
                            or "EC_Mencion" in nombrepregunta
                            or ("EC_Posgrado" in nombrepregunta and "AreaMatem" not in nombrepregunta)
                            or ("EC_IMPARTE" in nombrepregunta and "IMPARTE.MATE" not in nombrepregunta)
                            or "EC_TRABAJOEXTRA" in nombrepregunta
                            or "EC_APRENDIZAJE.TIC" in nombrepregunta
                            or "EC_INTERNET" in nombrepregunta
                            or "EC_MOTIVO.NOUSOTIC" in nombrepregunta)):

                                # print("checkbox")

                                if("chbx" in nombrepregunta):
                                    totalopciones = int(nombrepregunta[-1])
                                    if(nombrepregunta[-2].isnumeric()):
                                        totalopciones = int(nombrepregunta[-2:])
                                elif("p3_2" in nombrepregunta):
                                    totalopciones = 9
                                elif("p3_4" in nombrepregunta):
                                    totalopciones = 5
                                elif("p4_4" in nombrepregunta):
                                    totalopciones = 7
                                elif("p4_8" in nombrepregunta):
                                    totalopciones = 7
                                elif("p5_2" in nombrepregunta):
                                    totalopciones = 5
                                elif("p5_5" in nombrepregunta):
                                    totalopciones = 4
                                elif("EC_Mencion" in nombrepregunta):
                                    totalopciones = 13
                                elif("EC_Posgrado" in nombrepregunta):
                                    totalopciones = 6
                                elif("EC_IMPARTE" in nombrepregunta):
                                    if("MEDIA" in row[7]):
                                        totalopciones = 7
                                    else:
                                        totalopciones = 9
                                elif("EC_TRABAJOEXTRA" in nombrepregunta):
                                    if("MEDIA" in row[7]):
                                        totalopciones = 5
                                    else:
                                        totalopciones = 6
                                elif("EC_APRENDIZAJE.TIC" in nombrepregunta):
                                    totalopciones = 6
                                elif("EC_INTERNET" in nombrepregunta):
                                    totalopciones = 4
                                elif("EC_MOTIVO.NOUSOTIC" in nombrepregunta):
                                    totalopciones = 8

                                    
                                #marcadas = respuesta.split(",")
                                carnum = 0
                                pivote = 0
                                marcadas = []
                                for c in respuesta:
                                    if(carnum >= 2 and c.isupper() and respuesta[carnum-1] == " " and respuesta[carnum-2] == ","):
                                        marcadas.append(respuesta[pivote:(carnum-2)])
                                        pivote = carnum
                                    carnum += 1
                                    if(carnum == len(respuesta)):
                                        marcadas.append(respuesta[pivote:])
                                loaded_json = json.loads(row[8])
                                codmarcadas = []
                                if("student_answers" in loaded_json):
                                    if idrespuesta in loaded_json['student_answers']:
                                        codmarcadas = loaded_json['student_answers'][idrespuesta]
                                j = 0
                                id1 = pregencuesta.numeroidentificatorio1
                                id2 = pregencuesta.numeroidentificatorio2
                                for i in range(0,totalopciones):
                                    pregencuesta = subpreguntaencuesta()
                                    # print(i)
                                    pregencuesta.nombrepregunta = nombrepregunta+"_"+str(i)
                                    if("choice_"+str(i) in codmarcadas):
                                        print("marqué choice_"+str(i))
                                        pregencuesta.respuesta = str(marcadas[j])
                                        j += 1
                                    else:
                                        pregencuesta.respuesta = "999"
                                    # print("guardo pregencuesta con nombrepreg = "+pregencuesta.nombrepregunta+" y resp = "+pregencuesta.respuesta)
                                    pregencuesta.usuariorut = usr.RUT
                                    pregencuesta.usuariocorreo = usr.email
                                    pregencuesta.nombre = usr.ApellidoP + " " + usr.nombre
                                    pregencuesta.nombreusuario = usr.username
                                    pregencuesta.nombreencuesta = nombreencuesta
                                    pregencuesta.numeroencuesta = numeroEncuesta
                                    pregencuesta.arrayres = str(arrayresp)
                                    pregencuesta.blockkey = blockKeyCompleto
                                    pregencuesta.pagina = paginaNumero
                                    pregencuesta.tipo = tipo
                                    pregencuesta.numeroidentificatorio1 = id1
                                    pregencuesta.numeroidentificatorio2 = id2
                                    clasesyvariables.ListaPregutnasEncuestas.append(pregencuesta)
                            else:
                                pregencuesta.usuariorut = usr.RUT
                                pregencuesta.usuariocorreo = usr.email
                                pregencuesta.nombre = usr.ApellidoP + " " + usr.nombre
                                pregencuesta.nombreusuario = usr.username
                                pregencuesta.nombreencuesta = nombreencuesta
                                pregencuesta.nombrepregunta = nombrepregunta
                                pregencuesta.numeroencuesta = numeroEncuesta
                                pregencuesta.respuesta = str(respuesta)
                                pregencuesta.arrayres = str(arrayresp)
                                pregencuesta.blockkey = blockKeyCompleto
                                pregencuesta.pagina = paginaNumero
                                pregencuesta.tipo = tipo
                                clasesyvariables.ListaPregutnasEncuestas.append(pregencuesta)
            
# print (" Recorrido ")


def RecorrerCSVParaEncuestaClase3(fileLocation,usuarios,student_obj=None): 
    # print("Recorrer CVS en busca de preguntas clase 3 de encuestas en js input")
    File = fileLocation
    # with open(File, newline='', encoding="utf-8") as f:
    f = student_obj
    reader = csv.reader(f)
    completo = False
    for row in reader:
        if(len(row) > 6 ):
            nombre = row[0]
            #print ("Nombre tomado del csv: " + nombre)
            ##time.sleep(3)
            for usr in usuarios:
                #print ("Nombre en la lista de usuarios " + usr.username )
                ##time.sleep(1)
                if usr.username.lower() == nombre.lower() : 
                    #usuarioActual = nombre
                    # print ("Lo encontre " + nombre + " VS " + usr.username)
                    titulos= row[2].split(">")

                    if( len(titulos) > 1 ):

                        #ubicaciones 
                        loc1 = 1
                        loc2 = 2
                        loc3 = 3
                        loc4 = 4

                        #print("tamaño del arreglo titulos " + str(len(titulos)) )
                        if(len(titulos) == 5):
                            completo == True
                        elif(len(titulos) == 4):
                            loc1 = 0
                            loc2 = 1 
                            loc3 = 2
                            loc4 = 3
                            completo == False
                        elif(len(titulos) == 3):
                            loc1 = 0
                            loc2 = 0 
                            loc3 = 1
                            loc4 = 4

                        
                        subtitulo = str(titulos[loc2].lower())
                        if(subtitulo[0] == ' '):
                            #print("Tiene un espaciio en blanco")
                            subtitulo = subtitulo[1:]
                            ##time.sleep(1)

                        nombreencuesta= ""
                        soyencuesta = False

                        if( subtitulo.startswith("encuesta") ):
                            #print("Encontre la encuesta " + str(titulos[loc2]))
                            nombreencuesta = subtitulo
                            soyencuesta = True

                            if(nombreencuesta.find("encuesta de la discusión") != -1):
                                nombreencuesta = "encuesta " + (titulos[loc1]).lower()

                        elif subtitulo.find("taller online") != -1:
                        
                            nombreencuesta = str(titulos[loc3])

                            if (nombreencuesta.lower()).find("encuesta") != -1:
                                subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") 

                                if(subnombreencuesta == "encuesta"): #Reviso que no tenga la plabra encuesta sola
                                    nombreencuesta = "encuesta " + subtitulo

                                soyencuesta = True

                            #time.sleep(5)

                        elif( subtitulo.find("discusión virtual") != -1):

                            nombreencuesta = str(titulos[loc3])
                            
                            if (nombreencuesta.lower()).find("encuesta") != -1:
                                subnombreencuesta = str(nombreencuesta.lower()).replace(" ", "") 

                                if(subnombreencuesta == "encuesta"): #Reviso que no tenga la plabra encuesta sola
                                    nombreencuesta = "encuesta " + subtitulo

                                soyencuesta = True

                            
                            #time.sleep(5)

                        if  soyencuesta:

                            # print(nombreencuesta + " VS " + str(clasesyvariables.usuarioPrueba.nombresEncuestas) )
                            
                            if(nombreencuesta in clasesyvariables.usuarioPrueba.nombresEncuestas):
                                indexEncuesta = clasesyvariables.usuarioPrueba.nombresEncuestas.index(nombreencuesta)
                                numeroEncuesta = indexEncuesta + 1
                            else:
                                numeroEncuesta = -1
                    
                            paginaNumero = 0
                            if( str(titulos[loc3]).find("#") > 0):
                                paginatext = titulos[loc3].split('#')
                                if(len(paginatext) > 1):
                                    paginaNumero = int(paginatext[1])

                            tipo = row[1]
                            idrespuesta = row[3]
                            nombrepregunta = row[4]
                            respuesta = row[5]
                            arrayresp = row[6]

                            # print(usr.username)
                            # print("Respuestas: ")
                            # print(respuesta)
                            

                            if respuesta !=  "":
                                json_encurespuestas = json.loads(respuesta)

                                conjuntorespuestas = json_encurespuestas["answer"]


                                if json_encurespuestas["answer"] == "\"nada\"":
                                    #print("es nada")
                                    conjuntorespuestas = json_encurespuestas["state"]
                                    #print(conjuntorespuestas)
                                    #time.sleep(6)

                                encurespuestas = ( conjuntorespuestas[1:-1] ).split("_*_") 

                                blockkeyArray = row[7].split('@')
                                if(len(blockkeyArray) > 1 ):
                                    blockKeyCompleto = row[7]
                                    blockKey = blockkeyArray[0]
                                    blockTipo = blockkeyArray[1]
                                    blockkeyArray[2]

                                iterator_penc = 0

                                #armar dict de respuestas
                                ptrs =[] #Preguntas tipos y respuestas 

                                for encuresp in encurespuestas:

                                    pregenccomp = encuresp.split("_;_")
                                    p_enunciado = pregenccomp[0]
                                    p_respuesta = pregenccomp[1]

                                    if p_enunciado == "valoresalternativas":
                                        # print("encontre especial")
                                        pregtipoyrespuestas = p_respuesta.split("__")
                                        if len(pregtipoyrespuestas) > 0:
                                            for pregtipoyrespuesta in pregtipoyrespuestas:
                                                ptr = {}
                                                
                                                ptr_values = pregtipoyrespuesta.split("::")
                                                
                                                if len(ptr_values) > 1:
                                                    ptr["tag"] = ptr_values[0]
                                            
                                                    posibletipo = "no identificado"
                                                    start = ptr_values[1].find("[") + len("[")
                                                    end =  ptr_values[1].find("]")
                                                    if start > -1 and end > -1:
                                                        posibletipo =  (ptr_values[1])[start:end]
                                                        
                                                    ptr["tipo"] = posibletipo

                                                    if(posibletipo == "checkbox"):
                                                        ptr_respuestas = []
                                                        ptr_respuestas_aux = ( ptr_values[1].replace("[" + posibletipo + "]","") ).split(";;")
                                                        for e in encurespuestas:
                                                            if(ptr["tag"]+"_;_" in e):
                                                                ans = e.split("_;_")[1]
                                                                break
                                                        for r in ans.split("_"):
                                                            if(r == "false"):
                                                                ptr_respuestas.append("sin marcar")
                                                            else:
                                                                ptr_respuestas.append(ptr_respuestas_aux.pop(0))
                                                        else:
                                                            ptr_respuestas = ( ptr_values[1].replace("[" + posibletipo + "]","") ).split(";;")
                                                    ptr["respuestas"] = ptr_respuestas

                                                    ptrs.append(ptr)

                                clasesyvariables.logErrores.append("Lista alternativas " + usr.username + "  : " + str(ptrs) )

                                #Recorrer ahora llenando las respuestas
                                for encuresp in encurespuestas:
                                    # print(encuresp)
                                    pregenccomp = encuresp.split("_;_")
                                    # print("esta")

                                    iterator_penc += 1

                                    if len(pregenccomp) > 1:

                                        p_enunciado = pregenccomp[0]
                                        p_resp = pregenccomp[1]

                                        if p_enunciado != "faltanrespuestas" and p_enunciado !="valoresalternativas":

                                            findedespecial = False #Buscare si es una pregunta que esta en la lista
                                            
                                            for respespecial in ptrs:
                                                if respespecial["tag"] == p_enunciado:
                                                    # print("es una respuesta especial")
                                                    findedespecial = True

                                                    iterator_penc2 = 0
                                                    respespecial_resp = respespecial["respuestas"]

                                                    if len(respespecial["respuestas"]) > 1:
                                                        respuestasEspeciales = respespecial["respuestas"]
                                                        for subrespes in respuestasEspeciales:

                                                            iterator_penc2 += 1

                                                            pregencuesta = subpreguntaencuesta()

                                                            pregencuesta.usuariorut = usr.RUT
                                                            pregencuesta.usuariocorreo = usr.email
                                                            pregencuesta.nombre = usr.ApellidoP + " " + usr.nombre
                                                            pregencuesta.nombreusuario = usr.username
                                                            pregencuesta.nombreencuesta = nombreencuesta
                                                            pregencuesta.nombrepregunta = p_enunciado + "_" + str(iterator_penc2)
                                                            pregencuesta.numeroencuesta = numeroEncuesta
                                                            pregencuesta.respuesta = subrespes
                                                            pregencuesta.arrayres = str(p_resp)
                                                            pregencuesta.blockkey = blockKeyCompleto
                                                            pregencuesta.pagina = paginaNumero
                                                            pregencuesta.tipo = tipo

                                                            pregencuesta.numeroidentificatorio1 = paginaNumero
                                                            pregencuesta.numeroidentificatorio2 = iterator_penc

                                                            clasesyvariables.ListaPregutnasEncuestas.append(pregencuesta) 
                                                    
                                                    else:
                                                        pregencuesta = subpreguntaencuesta()

                                                        pregencuesta.usuariorut = usr.RUT
                                                        pregencuesta.usuariocorreo = usr.email
                                                        pregencuesta.nombre = usr.ApellidoP + " " + usr.nombre
                                                        pregencuesta.nombreusuario = usr.username
                                                        pregencuesta.nombreencuesta = nombreencuesta
                                                        pregencuesta.nombrepregunta = p_enunciado
                                                        pregencuesta.numeroencuesta = numeroEncuesta
                                                        pregencuesta.respuesta = str(respespecial_resp[0]) 
                                                        pregencuesta.arrayres = str(p_resp)
                                                        pregencuesta.blockkey = blockKeyCompleto
                                                        pregencuesta.pagina = paginaNumero
                                                        pregencuesta.tipo = tipo

                                                        pregencuesta.numeroidentificatorio1 = paginaNumero
                                                        pregencuesta.numeroidentificatorio2 = iterator_penc 
                                                                                                            
                                                        clasesyvariables.ListaPregutnasEncuestas.append(pregencuesta)

                                            
                                            if  not findedespecial:
                                                pregencuesta = subpreguntaencuesta()

                                                pregencuesta.usuariorut = usr.RUT
                                                pregencuesta.usuariocorreo = usr.email
                                                pregencuesta.nombre = usr.ApellidoP + " " + usr.nombre
                                                pregencuesta.nombreusuario = usr.username
                                                pregencuesta.nombreencuesta = nombreencuesta
                                                pregencuesta.nombrepregunta = p_enunciado
                                                pregencuesta.numeroencuesta = numeroEncuesta
                                                pregencuesta.respuesta = p_resp
                                                pregencuesta.arrayres = str(p_resp)
                                                pregencuesta.blockkey = blockKeyCompleto
                                                pregencuesta.pagina = paginaNumero
                                                pregencuesta.tipo = tipo

                                                pregencuesta.numeroidentificatorio1 = paginaNumero
                                                pregencuesta.numeroidentificatorio2 = iterator_penc 

                                                clasesyvariables.ListaPregutnasEncuestas.append(pregencuesta)
                                        else:
                                            if p_resp != "no":
                                                clasesyvariables.logErrores.append("El usuario " + usr.username + " le faltan resuestas en " + blockKeyCompleto)


                            else:
                                print("Respuesta Vacia")