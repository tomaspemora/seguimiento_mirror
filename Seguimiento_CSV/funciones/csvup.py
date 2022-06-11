import json
import csv
from pdb import set_trace as bp

import string  
import sys
import zipfile
from tempfile import NamedTemporaryFile
import os
import io
import time

import re

from itertools import cycle


# with open('./data_gtd.json') as f:
#   data = json.load(f)

def JSON2CSV(data,nombre_sect,random_string):
    csv_columns = ['username', 'title', 'location', 'id de la respuesta', 'pregunta', 'respuesta', 'respuesta correcta', 'block_key', 'state']
    csv_columns2 = ['Submission ID','Item ID','Anonymized Student ID','Date/Time Response Submitted','Response','Assessment Details','Assessment Scores','Date/Time Final Score Given','Final Score Points Earned','Final Score Points Possible','Feedback Statements Selected','Feedback on Peer Assessments']

    nombre_curso = "nombre"
    bloques = data["blocks"]
    for b in bloques:
        bloque = bloques[b]
        if(bloque["type"] == "course"):
            nombre_curso = bloque["display_name"]

    tipos = {'problem','dialogsquestionsxblock','vof','freetextresponse','openassessment','drag-and-drop-v2','eollistgrade'}
    dict_data = []
    dict_data2 = []
    countoas = 0

    for b in bloques:
        bloque = bloques[b]
        if(bloque["type"] == "chapter"):
            #print(bloque["display_name"]+" ("+bloque["id"]+")")
            #print("Actividades:")
            if "children" in bloque:
                for act in bloque["children"]:
                    #print(act)
                    #print(bloques[act]["display_name"])
                    #print("PAGINAS")
                    for pag in bloques[act]["children"]:
                        #print(bloques[pag]["id"])
                        #print(bloques[pag]["display_name"])
                        if "children" in bloques[pag]:
                            for preg in bloques[pag]["children"]:
                                if(bloques[preg]["type"] in tipos):
                                    if bloques[preg]["type"] == "freetextresponse":
                                        bloques[preg]["display_name"] = "freetextresponse"
                                    elif bloques[preg]["type"] == "drag-and-drop-v2":
                                        bloques[preg]["display_name"] = "Drag and Drop"

                                    if not bloques[preg]["display_name"]:
                                        bloques[preg]["display_name"] = "Problem"

                                    location = nombre_curso
                                    if bloque["display_name"]:
                                        location+=" > "+bloque["display_name"]
                                    if bloques[act]["display_name"]:
                                        location+=" > "+bloques[act]["display_name"]
                                    if bloques[pag]["display_name"]:
                                        location+=" > "+bloques[pag]["display_name"]
                                    if bloques[preg]["display_name"]:
                                        location+=" > "+bloques[preg]["display_name"]

                                    estado = ""
                                    if bloques[preg]["type"] == "vof":
                                        estado = '{"respuestas": {"2": "verdadero", "1": "verdadero", "3": "falso", "4": "falso", "5": "falso", "6": "falso", "7": "falso", "8": "falso", "9": "falso"}, "respondido": true, "attempts": 1, "score": 0.6666666666666666}'
                                    elif bloques[preg]["type"] == "freetextresponse":
                                        estado = '{"student_answer": "respuesta cualquiera", "score": 1.0, "count_attempts": 1}'
                                    elif bloques[preg]["type"] == "openassessment":
                                        #Aca ago las cosas de las ORAs
                                        estado = '{"has_saved": true, "submission_uuid": "id'+str(countoas)+'", "saved_response": {"parts": [{"text": "cualquier respuesta"}]}}'
                                        pregoas = {'Submission ID':'id'+str(countoas),'Item ID':countoas,'Anonymized Student ID':'idanonima','Date/Time Response Submitted':'2020-09-06 03:47:34.979350+00:00','Response':'{"parts": [{"text": "cualquier respuesta"}]}','Assessment Details':'','Assessment Scores':'','Date/Time Final Score Given':'','Final Score Points Earned':'','Final Score Points Possible':'','Feedback Statements Selected':'','Feedback on Peer Assessments':''}
                                        dict_data2.append(pregoas)
                                        countoas+=1
                                    elif bloques[preg]["type"] == "drag-and-drop-v2":
                                        estado = '{"item_state": {"0": {"zone": "middle", "correct": true}, "1": {"zone": "bottom", "correct": true}, "2": {"zone": "top", "correct": true}}, "completed": true, "attempts": 1, "raw_earned": 1.0}'
                                    else:
                                        estado = '{"done": true, "score": {"raw_earned": 1, "raw_possible": 1}, "input_state": {"asdf": {}}, "seed": 1, "last_submission_time": "2020-08-19T12:01:26Z", "correct_map": {"asdf": {"hint": "", "queuestate": null, "answervariable": null, "npoints": null, "correctness": "correct", "msg": "", "hintmode": null}}, "attempts": 1, "student_answers": {"asdf": "choice_0"}}'
                                    #username, title, location, id de la respuesta, pregunta, respuesta, respuesta correcta, block_key, state
                                    #lapreg = {"Taller": bloque["display_name"], "Actividad": bloques[act]["display_name"], "Pagina": bloques[pag]["display_name"], "Tipo": bloques[preg]["type"], "id_pregunta": bloques[preg]["id"]}
                                    
                                    if bloques[preg]["type"] == "eollistgrade":
                                        bloques[preg]["type"] = "eol list grade"
                                        estado = '{"comment": "asistencia", "student_score": 0}'

                                    lapreg = {"username": "UsuarioPruebaCMMEDU", "title": bloques[preg]["display_name"], "location": location, "id de la respuesta": "asdf", "pregunta": "preg", "respuesta": '{""}', "respuesta correcta":"asdf","block_key":bloques[preg]["id"],"state":estado}
                                    dict_data.append(lapreg)

    #aca yo deberia ordenar dict_data                    

    #print(dict_data)
    csv_file = "Bloques_"+nombre_sect+"_"+random_string+".csv"
    dir_csv_file = os.path.join(sys.path[0],"Generado/Csv",csv_file)
    try:
        with open(dir_csv_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error en Bloques")

    #print(dict_data2)
    csv_file2 = "ORAS_"+nombre_sect+"_"+random_string+".csv"
    dir_csv_file2 = os.path.join(sys.path[0],"Generado/Csv",csv_file2)
    try:
        with open(dir_csv_file2, 'w', encoding='utf-8', newline='') as csvfile2:
            writer = csv.DictWriter(csvfile2, fieldnames=csv_columns2)
            writer.writeheader()
            for data in dict_data2:
                writer.writerow(data)
    except IOError:
        print("I/O error en ORAS")

def ordenar(CSV,Talleres):
    FileNombres = open(Talleres, "r",encoding="utf-8", newline='')
    
    csvordenado = []    
    primeraLinea = True
    
    for line in FileNombres:

        stripped_line = line.strip()
        namelower = stripped_line.lower()
        FileCSV = open(CSV,"r",encoding="utf-8", newline='')
        reader = csv.reader(FileCSV)
        for row in reader:

            if primeraLinea:
                csvordenado.append(row)
                primeraLinea = False

            nombreCompleto = row[2].split(">")

            if len(nombreCompleto)  > 1:
                nombreTaller = nombreCompleto[1].lower()
                if nombreTaller.find(namelower) != -1:
                    csvordenado.append(row)
                    #time.sleep(3)

    

    archivoname = os.path.splitext(os.path.basename(CSV))[0]
    filemame = archivoname + "_Ordenado.csv"
    csvdir = os.path.join(sys.path[0],"Generado/Csv", filemame)
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

    
    try:
        write = csv.writer(text_file)
        write.writerows(csvordenado)
    except IOError:
        print("I/O erro Bloques ordnados")
    
    text_file.close()
    