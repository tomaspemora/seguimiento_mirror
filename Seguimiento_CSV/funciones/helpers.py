from . import clasesyvariables
import os, sys
import time
def CreateErrorFile(listaErrores,nombre):

    nombreAnomalo = "Anomalias_" + nombre + ".txt"    
    logError_dir = os.path.join(sys.path[0],"Generado/Txt", nombreAnomalo )
    if os.path.isfile(logError_dir):
        os.remove(logError_dir)
    # print ("Anomalias " + logError_dir)
    text_file2 = open(logError_dir, "w+", encoding='utf-8')

    for anomalia in listaErrores:
        n = text_file2.write(anomalia + '\n' )

    # print ("Guardar Txt")
    text_file2.close()

    return logError_dir


def quitarUsuarioPruebadelaLista(nombreUsrPrueba):
    # print("Buscar al ususario de prueba para sacarlo "  + str(nombreUsrPrueba))
    for usrprueba in clasesyvariables.usuarios:
        # print (str(usrprueba.nombre) + " VS " + nombreUsrPrueba)
        if(usrprueba.username.find(nombreUsrPrueba) != -1):
            # print("Borarre al usuario de prueba: " + usrprueba.nombre + " por USERNAME")
            usrtoDelete = usrprueba
            clasesyvariables.usuarios.remove(usrtoDelete)


def renew_time(t,medir_tiempo,tiempos,nombre_key):
    print(f'Ejecutando: {nombre_key}')
    if medir_tiempo:
        tiempos[nombre_key] = round(time.time() - t,2)
        t = time.time()
        return t,tiempos
    return (None, None)
    