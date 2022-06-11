import sys, api_preguntas_para_comparador, os
from pdb import set_trace as bp
from datetime import datetime
from termcolor import colored
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config

prefix = 'cmm'
programa = 'SYS'
siglas_curso = 'DMF01'
ano = '2020'
semestre='1'

curso = 'course-v1:'+prefix+'+'+programa+siglas_curso+'+'+ano+'_'+semestre # esto sería la variable que hay que ver como armar ej: course-v1:cmm+SYSDMF01+2020_1

secciones = [   'course-v1:cmm+SYSTMD01+2020_2',
                'course-v1:cmm+SYSTNR01+2020_2',
                'course-v1:cmm+SYSTFR01+2020_2',
                'course-v1:cmm+SYSIPE01+2020_2',
                'course-v1:cmm+SYSARP01+2020_2',
                'course-v1:cmm+SYSDPA02+2020_2',
                'course-v1:cmm+SYSDPE01+2020_1',
                'course-v1:cmm+SYSDPG01+2021_1',
                'course-v1:cmm+SYSDMF01+2020_1',
                'course-v1:cmm+SYSGTD01+2020_2',
                'course-v1:cmm+SYSIPG01+2020_1',
                'course-v1:cmm+SYSMEPI01+2019_1',
                'course-v1:cmm+SYSSND01+2019_02',
                'course-v1:cmm+SYSTIP01+2021_1',
                'course-v1:cmm+SYSTMM01+2020_1'
                ]

def prettyDicts(d, indent=0):
    if isinstance(d,list) or isinstance(d,set):
        for i in range(len(d)):
            print('\t' * (indent) + str(i),end='')
            

            prettyDicts(d[i], indent)
    elif isinstance(d, dict):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                prettyDicts(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))
        print('\t' * (indent) +'________________________')
    else:
        print('\t' * (indent+1) + str(d))

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

def comparatorUP(secciones = secciones):
    sys.stdout = Logger()

    email = 'jromo.dcc@gmail.com'
    password = 'dimcmm33'
    raiz = 'https://cmmeduformacion.uchile.cl'
    types_allowed_equal_id = ['eolzoom','course','vertical','sequential','html','chapter','eolquestion','eolcontainer','discussion', 'eoldialogs', 'eolconditional']
    [con,headers] = api_preguntas_para_comparador.conectarseAPI(email,password,raiz)
    consultas = {}
    pags = {}
    for seccion in secciones:
        consultas[seccion] = api_preguntas_para_comparador.bajarJson(con,headers,seccion)
        paginas = api_preguntas_para_comparador.bajarPaginas(con,headers,seccion)
        pags[seccion] = {}
        for it in consultas[seccion]["blocks"]:
            if consultas[seccion]["blocks"][it]["type"] == "vertical":
                pags[seccion][it] = consultas[seccion]["blocks"][it]

    count=0
    color = 'blue'
    contador = 0
    n = len(secciones)
    types_encountered = []
    copia_secciones = secciones.copy()
    for seccion in copia_secciones:
        secciones.remove(seccion)
        r = consultas[seccion]
        for seccion2 in secciones:
            r2 = consultas[seccion2]
            for element in r["blocks"]:
                for element2 in r2["blocks"]:
                    if r["blocks"][element]["block_id"] == r2["blocks"][element2]["block_id"] and r2["blocks"][element2]["type"] not in types_allowed_equal_id:
                        bool1 = True
                        bool2 = True

                        for el in pags[seccion]:
                            if "children" in pags[seccion][el]:
                                if r["blocks"][element]["id"] in pags[seccion][el]["children"]:
                                    if pags[seccion][el]["display_name"].lower().find("encuesta") != -1 or pags[seccion][el]["display_name"].lower().find("consentimiento") != -1 or pags[seccion][el]["display_name"].lower().find("diagnóstico") != -1 or pags[seccion][el]["display_name"].lower().find("reglamento") != -1:
                                       bool1 = False

                        for el2 in pags[seccion2]:
                            if "children" in pags[seccion2][el2]:
                                if r2["blocks"][element2]["id"] in pags[seccion2][el2]["children"]:
                                    if pags[seccion2][el2]["display_name"].lower().find("encuesta") != -1 or pags[seccion2][el2]["display_name"].lower().find("consentimiento") != -1 or pags[seccion2][el2]["display_name"].lower().find("diagnóstico") != -1 or pags[seccion2][el2]["display_name"].lower().find("reglamento") != -1:
                                       bool2 = False

                        if bool1 or bool2:

                            if color == 'blue':
                                color = 'yellow'
                            else:
                                color = 'blue'

                            for el in r["blocks"][element]:
                                print(colored('{0: <20}'.format(el) + " ----> " + r["blocks"][element][el],color))

                            for el in pags[seccion]:
                                if "children" in pags[seccion][el]:
                                    if r["blocks"][element]["id"] in pags[seccion][el]["children"]:
                                        print(colored(pags[seccion][el]["lms_web_url"],'magenta'))
                                        print(colored(pags[seccion][el]["display_name"],'magenta'))

                            print(colored('______________________________','green'))
                            print(colored('es igual a','green'))
                            print(colored('______________________________','green'))

                            for el2 in r2["blocks"][element2]:
                                print(colored('{0: <20}'.format(el2) + " ----> " + r2["blocks"][element2][el2],color))

                            for el2 in pags[seccion2]:
                                if "children" in pags[seccion2][el2]:
                                    if r2["blocks"][element2]["id"] in pags[seccion2][el2]["children"]:
                                        print(colored(pags[seccion2][el2]["lms_web_url"],'cyan'))
                                        print(colored(pags[seccion2][el2]["display_name"],'cyan'))
                                        
                            print(colored('________________________________________________________________________________________________________________________','red'))
                            count +=1

                        # curso_id = r2["root"].replace('block-v1','course-v1').replace('+type@course+block@course','')
                        # api_preguntas_para_comparador.bajarPaginas(con,headers,curso_id)
                        # params={'scope_ids': block_id}

                        if r2["blocks"][element2]["type"] not in types_encountered:
                            types_encountered.append(r2["blocks"][element2]["type"])
            contador += 1
            print(seccion + '/ vs / ' + seccion2 + "     " , end='')
            print(str(contador/(n*(n-1)/2) * 100)+"%")
    print('Total de id duplicados: '+str(count))
    print(types_encountered)
    sys.stdout.close()

def comparatorUP2(secciones = secciones):
    contador = 0
    copia_secciones = secciones.copy()
    n = len(secciones)
    for seccion in copia_secciones:
        secciones.remove(seccion)
        for seccion2 in secciones:      
            contador += 1
            print(seccion + '/ vs / ' + seccion2 + "     " , end='')
            print(str(contador) + " | " + str(n) + " | "+ str(contador/(n*(n-1)/2) * 100)+"%")


config = Config(max_depth=8)
with PyCallGraph(output=GraphvizOutput(),config=config):
    # comparatorUP(secciones = secciones)
    comparatorUP(secciones = secciones)
