#Clases
import time

class usuario:
    def __init__(self):
        self.nombre ="usuario"
        self.username = "username"
        self.RUT = "0-X"
        self.nverificador = "X"
        self.email = "@cmm.com"
        self.ApellidoP = "Paterno"
        self.ApellidoM = "Materno"
        self.comuna = ""
        self.establecimiento =  ""
        self.telefono = ""
        self.RBD = ""
        self.nacimiento = ""
        self.ultimaconexion = None
        self.preguntas = []
        self.totalContestadas = 1
        self.totalConTaller = 0
        self.totalBuenas = 0
        self.totalMalas = 0
        self.totalOmitidas = 0
        self.totalPreguntasPBlock = 0
        self.totalPreguntasVF = 0
        self.totalPreguntasFreeResp = 0
        self.totalPreguntasDiaQues = 0
        self.totalPreguntasDragDrop = 0
        self.notaControles = []
        self.notaPreguntasCalificadas = []
        self.promedioControles = 0
        self.promedioPreCal = 0
        self.porLogroTest = 0
        self.notaPretest = 1
        self.notaPostest = 1
        #Adicionales generalmente para el usuario de prueba
        self.usuarioprueba = False
        self.totalPreguntasPorTaller = {}
        self.totalPreguntasBuenasOMalasPorTaller ={}
        self.totalPreguntasCorrectasPorTaller = {}
        self.totalPreguntasBuenasEnviadasTaller = {}
        self.sumaBuneasEnviadas = 0
        self.totalPreguntasPorControl = {}
        self.totalPreguntasEvaluadas = {}
        self.totalPregutnasEncuestas = {}
        self.totalEncuestas = {}
        self.cantidadControles = 0
        self.cantidadEncuestas = 0
        self.cantidadTipoPreguntaEvaluada = 0
        self.nombresEncuestas = []
        self.nombresAsistencias = []
        self.situacionactual = 0
        self.totalpretest = 0
        self.totalpostest = 0
        


class pregunta:
    def __init__(self):
        self.pagina = ""
        self.paginaNumero = 0
        self.curso = ""
        self.tallerNombre = ""
        self.tallerNumero = 0
        self.actividadNombre = ""
        self.actividadNumero = 0
        self.nombrePregunta = "0"
        self.nombreAsistencia = "NO_ASISTENCIA"
        self.numeroPregunta = 0
        self.textoUbicacion = 0
        self.blockKeyCompleto =""
        self.blockKey =""
        self.codigo = ""
        self.numero = 0
        self.tipo = ""
        self.pretest = False
        self.postest = False
        self.moduloinicial = False
        self.modulofinal = False
        self.esDeControl = False
        self.esDeEncuesta = False
        self.esDeActividad = False
        self.esAsistencia = False
        self.numeroEncuesta = 0
        self.preguntaEvaluada = False
        self.esunapreguntade = ""
        self.esCorrecta = None
        self.completa = True
        self.intentos = 0
        self.multipleRespuesta = False
        self.respuesta = ""
        self.respuestas = []
        self.respuestaCorrecta = ""
        self.idrespuesta = ""
        self.fechaRespuesta = None
        self.score = 0
        self.tipoOra = False
        self.oraCode = ""
        self.numerocontrol = 0
        self.consentimiento = False
        self.reglamento = False
        self.deTaller = False
        self.tieneBlockkey = False
        self.latieneusuariodeprueba = False
        #Necesarias cuando el blockkey esta repetido
        self.cantidaddeveces = 1
        self.ncorrectas = 0
        self.nincorrectas =  0 


class subpreguntaencuesta:
    def __init__(self):
        self.usuariorut = "0-0"
        self.usuariocorreo = "@.com"
        self.nombre = "Nombre Apellido"
        self.nombreusuario = "username"
        self.nombreencuesta = ""
        self.numeroencuesta = 0
        self.numeroidentificatorio1 = 0
        self.numeroidentificatorio2 = 0
        self.nombrepregunta  = ""
        self.tipo = ""
        self.respuesta = ""
        self.arrayres = ""
        self.pagina = 0
        self.blockkey = ""

class ora:
    def __init__(self):
        self.submissioid = ""
        self.itemid = ""
        self.studentid = ""
        self.fecharespuesta = None
        self.fechacalificacion = None
        self.respuesta = ""
        self.score = 0
        self.calificada = False

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_id(s, last):
    try:
        #print("Buscar id")
        start = s.rindex( last ) + len( last )
        end = len(s)
        # print ("id " + s)
        return s[start:end]
    except ValueError:
        return "ERROR"

def quitarAcentos(s):
    # print("string con acentos " + s )
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    # print ("string sin acentos " + s) 
    return s


def init():
    #Variables

    #Preguntas sobre la ejecución
    global sleep # set sleep to false when doesn’t want to sleep
    sleep =  True 
    global saltarPrimeriaLienaListaUsuarios 
    saltarPrimeriaLienaListaUsuarios = False
    global subirDrive # Subir los documentos a drive
    subirDrive = True 
    global generarjson # Generar json de preguntas de este curso
    generarjson= False
    global doSilent 
    doSilent = True
    global limpiar
    limpiar = False

    global usuarioPrueba 
    usuarioPrueba = usuario()
    global nombreUsuarioPrueba 
    nombreUsuarioPrueba= "UsuarioPruebaCMMEDU"
   
    global location_to_save_report
    location_to_save_report= ""

    global Limpiar 
    Limpiar = False
    global Resetear 
    Resetear = True

    global logErrores 
    logErrores = []

    global usuarios
    usuarios = []

    global listaoras
    listaoras = []

    global listapreguntaspretest
    listapreguntaspretest = []

    global ListaPregutnasEncuestas
    ListaPregutnasEncuestas = []

    if sleep != True: # if sleep is false
        # override #time.sleep to an empty function
        time.sleep = lambda x: None 
   