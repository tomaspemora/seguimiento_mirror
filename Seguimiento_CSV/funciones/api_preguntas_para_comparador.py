import requests
import json
from pdb import set_trace as bp


def conectarseAPI(email,password,raiz):
     headers = {'Referer': raiz}
     s = requests.Session()

     # Setup CSRF
     csrf = s.get(raiz+'/csrf/api/v1/token').json()['csrfToken']
     headers['x-csrftoken'] = csrf

     # Login
     s.post(raiz+'/user_api/v1/account/login_session/', data={'email': email, 'password': password}, headers=headers)
     # Update csrf
     headers['x-csrftoken'] = s.cookies['csrftoken']
     return [s,headers]

def bajarJson(con,headers,curso):

    r = con.get(headers['Referer']+'/api/courses/v2/blocks/',
         params={'course_id':curso, 'all_blocks':True,'depth':'all','requested_fields':'parent_id,parent,display_name,block_type,children,name'},
         headers=headers)

    # r2 = con.get(raiz+'/api/courses/v1/blocks/',
    #      params={'course_id':curso, 'all_blocks':True,'depth':'1','requested_fields':'display_name,block_type'},
    #      headers=headers)

    #esto habria que imprimirlo a un archivo en verdad
    # with open('data_'+curso.replace(':','_').replace('+','_')+'.json', 'w') as outfile:
    #     json.dump(r.json(), outfile)

    # with open('da2ta_'+curso.replace(':','_').replace('+','_')+'.json', 'w') as outfile:
    #     json.dump(r2.json(), outfile)

    return r.json()

def bajarPaginas(con,headers,curso):

     r = con.get(headers['Referer']+'/api/courses/v2/blocks/',
         params={'course_id':curso, 'all_blocks':True,'depth':'3','requested_fields':'children'},
         headers=headers)
     # print(r)
     return r.json()
def pruebe(con,headers,block_id):

     r = con.get(headers['Referer']+'/api/xblock/'+block_id,
         headers=headers)
     # print(r)
     return r.json()

    #r = s.post('https://staging.eol.espinoza.dev/courses/course-v1:cmm+SYSDPA02+2020_2/instructor/api/get_problem_responses',
    #    data={'problem_location': 'block-v1:cmm+SYSDPA02+2020_2+type@vertical+block@574936cda264472d8e06c4175a0521e7'},
    #    headers=headers)
    #print(r.json())