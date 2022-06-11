import requests


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