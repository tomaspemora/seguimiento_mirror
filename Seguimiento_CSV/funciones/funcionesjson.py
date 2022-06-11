from itertools import filterfalse
import json
import time
import sys
import os
import io
import urllib.request 

#CodigosLocales
from . import clasesyvariables
from .clasesyvariables import usuario
from .clasesyvariables import pregunta
from .clasesyvariables import subpreguntaencuesta
from .clasesyvariables import ora

if(clasesyvariables.doSilent):
    time.sleep = lambda x: None 

    def print(*args):
        pass

def LoadUsuarioDePrueba(fileLocation,json_obj = None):

    print ("Cargar usuario de prueba")

    #with open(fileLocation, 'r', encoding='utf-8') as loaded_json_file: #Json local
    #   data = loaded_json_file.read()
    if json_obj == None:
        # print (fileLocation)
        data = urllib.request.urlopen(fileLocation).read()

        JsonUPrueba = json.loads(data.decode('utf-8'))
    else:
        JsonUPrueba = json_obj
    clasesyvariables.usuarioPrueba.username = JsonUPrueba["username"]

    anandidas = 0
    
    for preg in JsonUPrueba["preguntas"]:
        # print(" - " + str(preg) )
        
        pregtoadd = pregunta()
        pregtoadd.pagina = preg["pagina"]
        pregtoadd.paginaNumero = preg["paginanumero"]
        #pregtoadd.curso =  preg[""]
        pregtoadd.tallerNombre = preg["tallernombre"]
        pregtoadd.tallerNumero = preg["tallernumero"]
        pregtoadd.actividadNombre = preg["actividadnombre"]
        pregtoadd.actividadNumero = preg["actividadnumero"]
        #pregtoadd.blockKey = preg[""]
        pregtoadd.codigo = preg["codigo"]
        #pregtoadd.numero = preg[""]
        pregtoadd.tipo = preg["tipo"]
        pregtoadd.pretest = preg["pretest"]
        pregtoadd.postest = preg["postest"]
        pregtoadd.esDeControl = preg["Es de control"]
        pregtoadd.esDeEncuesta = preg["Es de encuesta"]

        pregtoadd.esDeActividad = preg["Es de actividad"]
        if "Es de Asistencia" in JsonUPrueba["preguntas"]:
            pregtoadd.esAsistencia = preg["Es de Asistencia"]
        else:
            pregtoadd.esAsistencia = False
        pregtoadd.preguntaEvaluada = preg["preguntacalificada"]
        #pregtoadd.completa = preg[""]
        pregtoadd.multipleRespuesta = preg["multiplerespuesta"]
        pregtoadd.esCorrecta = preg["correcta"]
        pregtoadd.respuesta = preg["respuesta"]
        pregtoadd.respuestas = preg["respuestas"]
        pregtoadd.respuestaCorrecta = preg["respuestacorrecta"]
        pregtoadd.idrespuesta = preg["idrespuesta"]
        pregtoadd.tipoOra = preg["tipoora"]
        pregtoadd.oraCode = preg["oraCode"]
        pregtoadd.numerocontrol = preg["numerocontrol"]
        pregtoadd.consentimiento = preg["consentimiento"]
        pregtoadd.reglamento = preg["reglamento"]
        pregtoadd.deTaller = preg["detaller"]
        pregtoadd.tieneBlockkey = preg["tieneblockkey"]
        #pregtoadd.cantidaddeveces = preg[""]
        #pregtoadd.ncorrectas = preg[""]
        #pregtoadd.nincorrectas = preg[""]
        
        anandidas +=1 
        clasesyvariables.usuarioPrueba.preguntas.append(pregtoadd)

        if(pregtoadd.pretest == True):
            clasesyvariables.listapreguntaspretest.append(pregtoadd.codigo)
        ##time.sleep(5)

    #pregunta dummy para iteracion

    pregdummy = pregunta()
    pregdummy.pagina = "dummy"
    pregdummy.paginaNumero = 0
    #pregdummy.curso =  preg[""]
    pregdummy.tallerNombre = "dummy"
    pregdummy.tallerNumero = 0
    pregdummy.actividadNombre = "dummy"
    pregdummy.actividadNumero = 0
    #pregdummy.blockKey = preg[""]
    pregdummy.codigo = "dummy"
    #pregdummy.numero = preg[""]
    pregdummy.tipo = "dummy"
    pregdummy.pretest = False
    pregdummy.postest = False
    pregdummy.esDeControl = False
    pregdummy.esDeEncuesta = False
    pregdummy.esDeActividad = False
    pregdummy.esAsistencia = False
    pregdummy.preguntaEvaluada = False
    #pregdummy.completa = preg[""]
    pregdummy.multipleRespuesta = False
    pregdummy.esCorrecta = False
    pregdummy.respuesta =  "dummy"
    pregdummy.respuestas =  ["dummy"]
    pregdummy.respuestaCorrecta =  "dummy"
    pregdummy.idrespuesta =  "dummy"
    pregdummy.tipoOra = False
    pregdummy.oraCode =  ""
    pregdummy.numerocontrol = -1
    pregdummy.consentimiento = False
    pregdummy.reglamento = False
    pregdummy.deTaller = False
    pregdummy.tieneBlockkey = True
    #pregdummy.cantidaddeveces = preg[""]
    #pregdummy.ncorrectas = preg[""]
    #pregdummy.nincorrectas = preg[""]
    
    #anandidas +=1  #Por ahora no sumar una pregunta mas
    clasesyvariables.usuarioPrueba.preguntas.append(pregdummy)


    #Variables del usuario de prueba
    clasesyvariables.usuarioPrueba.totalContestadas = JsonUPrueba["totalcontestadas"]
    clasesyvariables.usuarioPrueba.totalConTaller = JsonUPrueba["totalcontaller"]
    clasesyvariables.usuarioPrueba.totalPreguntasPorTaller = JsonUPrueba["totalpreguntasportaller"]
    clasesyvariables.usuarioPrueba.totalPreguntasPorControl = JsonUPrueba["totalpreguntascontrol"]
    clasesyvariables.usuarioPrueba.totalPreguntasEvaluadas = JsonUPrueba["totalpreguntascalificadas"]
    clasesyvariables.usuarioPrueba.totalPregutnasEncuestas = JsonUPrueba["totalpreguntasporencuesta"]
    clasesyvariables.usuarioPrueba.totalEncuestas = JsonUPrueba["totalencuestas"]
    clasesyvariables.usuarioPrueba.cantidadControles = JsonUPrueba["cantidadcontroles"]
    clasesyvariables.usuarioPrueba.cantidadEncuestas = JsonUPrueba["cantidadencuestas"]
    clasesyvariables.usuarioPrueba.cantidadTipoPreguntaEvaluada = JsonUPrueba["cantidadtipopc"]
    clasesyvariables.usuarioPrueba.nombresEncuestas = JsonUPrueba["nombresdeencuestas"]
    if "nombresasistencias" in JsonUPrueba:
        clasesyvariables.usuarioPrueba.nombresAsistencias = JsonUPrueba["nombresasistencias"]
    else:
        clasesyvariables.usuarioPrueba.nombresAsistencias = []
    
    clasesyvariables.usuarioPrueba.situacionactual = 0
    clasesyvariables.usuarioPrueba.totalpretest = JsonUPrueba["totalpretest"]
    clasesyvariables.usuarioPrueba.totalpostest = JsonUPrueba["totalpostest"]
    
    #clasesyvariables.logErrores.append("Preguntas añadidas: " + str(anandidas))
    #clasesyvariables.logErrores.append("Lista: ")
    #clasesyvariables.logErrores.append(str(listapretestu))

    clasesyvariables.totalContestadas = JsonUPrueba["totalcontestadas"]
    clasesyvariables.totalPreguntasPorTaller = JsonUPrueba["totalpreguntasportaller"]
    clasesyvariables.totalPreguntasBuenasOMalasPorTaller = JsonUPrueba["totalpreguntasevaportaller"]
    clasesyvariables.totalpretest = JsonUPrueba["totalpretest"]
    clasesyvariables.totalpostest = JsonUPrueba["totalpostest"]
    

def createJsonTaller(listaUsuarios,nombre):
    strings_tojson = []
    string_tojson = "[" 
    substring = ""
    substring2 = ""
    substring3 = ""

    strings_tojson.append("[")

    for usr2 in listaUsuarios:
        # print ("\n____-------"+usr2.nombre + " numero de preguntas " + str(len(usr2.preguntas)) +"-------____")
        if(usr2.ultimaconexion == None ):
            fechaultimaco = ""
        else:
            fechaultimaco = str(usr2.ultimaconexion)

        ''' '","avance":['+json.dumps(usr2.totalPreguntasPorTaller) +']' '''#Mostrado de avance
        substring = '{"nombrecompleto":"'+ usr2.nombre + '","rut":"'+ usr2.RUT + '","username":"'+ usr2.username  + '","correo":"'+ usr2.email + '","situacionactual":'+ str(usr2.situacionactual) + ',"ultimaconexion":"'+ fechaultimaco +'","preguntas":['
        for pre in usr2.preguntas:
            # print("añadir pregunta ")

            if (pre.fechaRespuesta == None):
                feharespuesta = ""
            else:
                feharespuesta = str(pre.fechaRespuesta)

            escribirCorrecta = str(pre.esCorrecta).lower()
            if( escribirCorrecta == "none" ):
                escribirCorrecta = "null"


            respuesta = pre.respuesta.replace('"',"'")
            respuesta = respuesta.replace(",",".")
            respuesta = respuesta.rstrip()
            respuesta = respuesta.replace("\\","/")
            if not (respuesta.isprintable()):
                respuesta = "Contiene caracteres no imprimibles"


            respcorrecta = pre.respuestaCorrecta.replace('"',"'")
            respcorrecta = respcorrecta.replace(",",".")
            respcorrecta = respcorrecta.rstrip()
            respcorrecta = respcorrecta.replace("\\","/")
            if not (respcorrecta.isprintable()):
                respcorrecta = "Contiene caracteres no imprimibles"

            tallerNoComillas = pre.tallerNombre.replace('"',"'")
            paginaNoComillas = pre.pagina.replace('"',"'")
            actividadNoComillas = pre.actividadNombre.replace('"',"'")

            pre_substring2= '{"pagina":"'+paginaNoComillas + '","paginanumero":'+ str(pre.paginaNumero) + ',"tallernombre":"'+ tallerNoComillas + '","tallernumero":'+ str(pre.tallerNumero) +',"actividadnombre":"'+ actividadNoComillas + '","actividadnumero":'+ str(pre.actividadNumero) +',"textoUbicacion":"'+str(pre.textoUbicacion) +'"'
            pre_substring2 += ',"blockkeycompleto":"'+pre.blockKeyCompleto +'","blockkey":"'+pre.blockKey +'","codigo":"'+pre.codigo + '","tipo":"'+ pre.tipo + '","preguntacalificada":'+ str(pre.preguntaEvaluada).lower() + ',"pretest":'+ str(pre.pretest).lower() + ',"postest":'+ str(pre.postest).lower() + ',"Es de control":'+ str(pre.esDeControl).lower() + ',"Es de Asistencia":'+ str(pre.esAsistencia).lower() 
            pre_substring2 += ',"numerocontrol":'+ str(pre.numerocontrol) + ',"Es de encuesta":'+ str(pre.esDeEncuesta).lower() +',"Es de actividad":'+ str(pre.esDeActividad).lower() +',"moduloinicial":'+ str(pre.moduloinicial).lower() +',"modulofinal":'+ str(pre.modulofinal).lower() + ',"consentimiento":' + str(pre.consentimiento).lower()+ ',"reglamento":' + str(pre.reglamento).lower() 
            pre_substring2 += ',"detaller":'+ str(pre.deTaller).lower()+ ',"tieneblockkey":'+ str(pre.tieneBlockkey).lower() +',"esunapreguntade":"'+ pre.esunapreguntade + '","intentos":' + str(pre.intentos) +',"idrespuesta":"'+ pre.idrespuesta+'","correcta":'+ escribirCorrecta +',"tipoora":' + str(pre.tipoOra).lower() + ',"oraCode":"'+  pre.oraCode + '","score":'+ str(pre.score) +',"fecharespuesta":"'+ feharespuesta + '"'
            pre_substring2 +=',"multiplerespuesta":'+ str(pre.multipleRespuesta).lower() + ',"respuestacorrecta":"'+ respcorrecta +'","respuesta":"'+respuesta+'","respuestas":['

            substring3 = ""
            for res in pre.respuestas :
                pre_substring3 = '"' + res.replace('"',"'") + '"'
                pre_substring3 = pre_substring3.replace("\\","/")
                pre_substring3 = pre_substring3.replace("\n","")
                if not (pre_substring3.isprintable()):
                    pre_substring3 = '"Contiene caracteres no imprimibles"'
                substring3 += pre_substring3 + ","
                print("res: " + res + " __substring 3: " + substring3)
                ##time.sleep(3)
            if(len(substring3) > 1 and substring3[-1] == ","): substring3 = substring3[:-1] 
            pre_substring2 += substring3 +"]},"
            substring2 += pre_substring2

        if(len(substring2) > 1 and substring2[-1] == ","): substring2 = substring2[:-1]    
        substring += substring2 + "]}," 
        strings_tojson.append(substring)
        string_tojson += substring
        substring2 = ""
        ##time.sleep(3)
            
    string_tojson = string_tojson[:-1] +']'
    strings_tojson[-1] = strings_tojson[-1][:-1] + ']'
            
            
    # print("\n")
    # print("caracteres en el json: " + str(len(string_tojson)))
    #print (string_tojson)

    #jsondir = os.path.join(sys.path[0], "seguimiento.json")
    mame = "Seguimiento_ " + nombre + ".json"
    jsondir = os.path.join(sys.path[0],"Generado/Json", mame)
    # print ("jsondir " + jsondir)
    text_file = open(jsondir, "w+", encoding='utf-8')
    
    for jsontext in strings_tojson:
        #print (jsontext)
        n = text_file.write(jsontext)
        ##time.sleep(2)

    # print ("Guardar Json")
    text_file.close()

    return jsondir


def createJsonUsuario(usr2,codigo):

    strings_tojson = [] #Caso arreglo   
    #string_tojson = "" #Caso string unico
    substring = ""
    substring2 = ""
    substring3 = ""
 
    # print ("\n____-------"+usr2.nombre + " numero de preguntas " + str(len(usr2.preguntas)) +"-------____")
    if(usr2.ultimaconexion == None ):
        fechaultimaco = ""
    else:
        fechaultimaco = str(usr2.ultimaconexion)

    ''' '","avance":['+json.dumps(usr2.totalPreguntasPorTaller) +']' '''#Mostrado de avance
    substring = '{"nombrecompleto":"'+ usr2.nombre + '","rut":"'+ usr2.RUT + '","username":"'+ usr2.username  + '","correo":"'+ usr2.email + '","situacionactual":'+ str(usr2.situacionactual) + ',"ultimaconexion":"'+ fechaultimaco + '","preguntas":['
    for pre in usr2.preguntas:
        # print("añadir pregunta ")

        if (pre.fechaRespuesta == None):
            feharespuesta = ""
        else:
            feharespuesta = str(pre.fechaRespuesta)

        escribirCorrecta = str(pre.esCorrecta).lower()
        if( escribirCorrecta == "none" ):
            escribirCorrecta = "null"

        respuesta = pre.respuesta.replace('"',"'")
        respuesta = respuesta.replace(",",".")
        respuesta = respuesta.rstrip()
        respuesta = respuesta.replace("\\","/")
        if not (respuesta.isprintable()):
            respuesta = "Contiene caracteres no imprimibles"

        respcorrecta = pre.respuestaCorrecta.replace('"',"'")
        respcorrecta = respcorrecta.replace(",",".")
        respcorrecta = respcorrecta.rstrip()
        respcorrecta = respcorrecta.replace("\\","/")
        if not (respcorrecta.isprintable()):
            respcorrecta = "Contiene caracteres no imprimibles"


        respcorrecta = "NO POR AHORA"
        tallerNoComillas = pre.tallerNombre.replace('"',"'")
        paginaNoComillas = pre.pagina.replace('"',"'")
        actividadNoComillas = pre.actividadNombre.replace('"',"'")

        pre_substring2 = '{"pagina":"'+paginaNoComillas + '","paginanumero":'+ str(pre.paginaNumero) + ',"tallernombre":"'+ tallerNoComillas + '","tallernumero":'+ str(pre.tallerNumero) +',"actividadnombre":"'+ actividadNoComillas + '","actividadnumero":'+ str(pre.actividadNumero)  +',"textoUbicacion":"'+str(pre.textoUbicacion) +'"'
        pre_substring2 +=',"blockkeycompleto":"'+pre.blockKeyCompleto +'","blockkey":"'+pre.blockKey +'","codigo":"'+pre.codigo + '","tipo":"'+ pre.tipo + '","preguntacalificada":'+ str(pre.preguntaEvaluada).lower() + ',"pretest":'+ str(pre.pretest).lower() + ',"postest":'+ str(pre.postest).lower() + ',"Es de control":'+ str(pre.esDeControl).lower() + ',"Es de Asistencia":'+ str(pre.esAsistencia).lower() 
        pre_substring2 += ',"numerocontrol":'+ str(pre.numerocontrol) + ',"Es de encuesta":'+ str(pre.esDeEncuesta).lower() +',"Es de actividad":'+ str(pre.esDeActividad).lower() +',"moduloinicial":'+ str(pre.moduloinicial).lower() +',"modulofinal":'+ str(pre.modulofinal).lower() + ',"consentimiento":' + str(pre.consentimiento).lower()+ ',"reglamento":' + str(pre.reglamento).lower() 
        pre_substring2 += ',"detaller":'+ str(pre.deTaller).lower()+ ',"tieneblockkey":'+ str(pre.tieneBlockkey).lower() +',"esunapreguntade":"'+ pre.esunapreguntade + '","intentos":' + str(pre.intentos) +',"idrespuesta":"'+ pre.idrespuesta+'","correcta":'+ escribirCorrecta +',"tipoora":' + str(pre.tipoOra).lower() + ',"oraCode":"'+  pre.oraCode + '","score":'+ str(pre.score) +',"fecharespuesta":"'+ feharespuesta + '"'
        pre_substring2 +=',"multiplerespuesta":'+ str(pre.multipleRespuesta).lower() + ',"respuestacorrecta":"'+ respcorrecta + '"'
        
        if respuesta.isdecimal():
            pre_substring2 += ',"respuesta":' + respuesta 
        else:
            pre_substring2 += ',"respuesta":"' + respuesta + '"'
        
        pre_substring2 += ',"respuestas":['
        substring3 = ""
        for res in pre.respuestas :
            pre_substring3 = '"' + res.replace('"',"'") + '"'
            pre_substring3 = pre_substring3.rstrip()
            pre_substring3 = pre_substring3.replace("\\","/")
            pre_substring3 = pre_substring3.replace("\n","")
            if not (pre_substring3.isprintable()):
                pre_substring3 = '"Contiene caracteres no imprimibles"'

            substring3 += pre_substring3 + ","
            # print("res: " + res + " __substring 3: " + substring3)
            #time.sleep(3)
        if(len(substring3) > 1 and substring3[-1] == ","): substring3 = substring3[:-1] 
        pre_substring2 += substring3 +"]},"
        substring2 += pre_substring2

    if(len(substring2) > 1 and substring2[-1] == ","): substring2 = substring2[:-1]    
    substring += substring2 + '],"totalcontestadas":' + str(usr2.totalContestadas) + ',"totalcontaller":' + str(usr2.totalConTaller) +',"totalpreguntasportaller":' 
    strings_tojson.append(substring)

    jsontotalppt = json.dumps(usr2.totalPreguntasPorTaller, sort_keys=True)
    jsonstotalevapt = json.dumps(usr2.totalPreguntasBuenasOMalasPorTaller, sort_keys=True)
    jsontotalcopt = json.dumps(usr2.totalPreguntasCorrectasPorTaller, sort_keys=True)
    jsonppcontrol = json.dumps(usr2.totalPreguntasPorControl, sort_keys=True)
    jsonppencu = json.dumps(usr2.totalPreguntasPorControl, sort_keys=True)
    jsontotalpc= json.dumps(usr2.totalPreguntasEvaluadas, sort_keys=True)
    jsontotalEnc = json.dumps(usr2.totalEncuestas, sort_keys=True)

    strings_tojson.append(str(jsontotalppt)+ ',"totalpreguntasevaportaller":')
    strings_tojson.append(str(jsonstotalevapt)+ ',"totalpreguntascorrectastaller":')
    strings_tojson.append(str(jsontotalcopt) + ',"totalpreguntascontrol":')
    strings_tojson.append(str(jsonppcontrol) + ',"totalpreguntasporencuesta":')
    strings_tojson.append(str(jsonppencu) + ',"totalpreguntascalificadas":')
    strings_tojson.append(str(jsontotalpc) + ',"totalencuestas":')
    strings_tojson.append(str(jsontotalEnc) + "," )

    strings_tojson.append('"totalpretest":'+ str(usr2.totalpretest) + ",")
    strings_tojson.append('"totalpostest":'+ str(usr2.totalpostest) + ",")
    strings_tojson.append('"cantidadcontroles":'+ str(usr2.cantidadControles) + "," )
    strings_tojson.append('"cantidadencuestas":'+ str(usr2.cantidadEncuestas) + "," )
    strings_tojson.append('"cantidadtipopc":'+ str(usr2.cantidadTipoPreguntaEvaluada) + ",")
    
    
    nombresEncToADD = str(usr2.nombresEncuestas).replace("'",'"') 
    strings_tojson.append('"nombresdeencuestas":' + str(nombresEncToADD) + ",") 
    #string_tojson += substring
    substring2 = ""

    nombresAsisToADD =  str(usr2.nombresAsistencias).replace("'",'"') 
    # print("la lista de asistancia... ")
    # print(nombresAsisToADD)
    strings_tojson.append ('"nombresasistencias":'+ str(nombresAsisToADD))
    time.sleep(3)


    strings_tojson.append("}") #},

    #Borro la ultima coma
    #string_tojson = string_tojson[:-1] 
    #strings_tojson[-1] = strings_tojson[-1][:-1] 
            
            
    # print("\n")
    #print("caracteres en el json: " + str(len(string_tojson)))
    #print (string_tojson)

    #jsondir = os.path.join(sys.path[0], "seguimiento.json")
    nombrejson = "UsuarioPrueba_" + codigo + ".json"
    jsondir = os.path.join(sys.path[0],"Generado/Json", nombrejson)
    # print ("jsondir " + jsondir)
    text_file = open(jsondir, "w+", encoding='utf-8')
    
    for jsontext in strings_tojson:
        # print (jsontext)
        n = text_file.write(jsontext)
        #time.sleep(2)

    # print ("Guardar Json")
    text_file.close()
    return [jsondir, strings_tojson]