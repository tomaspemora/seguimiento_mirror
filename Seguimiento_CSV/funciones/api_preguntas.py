import requests
import json
import time

def bajarJson(email,password,raiz,curso):

    headers = {'Referer': raiz}
    sess = requests.Session()

    # Setup CSRF
    csrf = sess.get(raiz+'/csrf/api/v1/token').json()['csrfToken']
    headers['x-csrftoken'] = csrf

    # Login
    # print ("url")
    sess.post(raiz+'/user_api/v1/account/login_session/', data={'email': email, 'password': password}, headers=headers)

    # Update csrf
    headers['x-csrftoken'] = sess.cookies['csrftoken']

    # print(curso)
    # print(raiz + '/api/courses/v1/blocks/' ) 
    #time.sleep(12)

    print 
    r1 = sess.get(raiz+'/api/courses/v1/blocks/',
         params={'course_id':curso, 'all_blocks':True,'depth':'all','requested_fields':'name,display_name,block_type,children,name'},
         headers=headers)

    r2 = sess.get(raiz+'/api/courses/v1/blocks/',
         params={'course_id':curso, 'all_blocks':True,'depth':'1','requested_fields':'display_name,block_type'},
         headers=headers)

    #esto habria que imprimirlo a un archivo en verdad
    # with open('data_'+curso.replace(':','_').replace('+','_')+'.json', 'w') as outfile:
    #     json.dump(r.json(), outfile)

    # with open('da2ta_'+curso.replace(':','_').replace('+','_')+'.json', 'w') as outfile:
    #     json.dump(r2.json(), outfile)

    return [r1.json(), r2.json()]

    #r = s.post('https://staging.eol.espinoza.dev/courses/course-v1:cmm+SYSDPA02+2020_2/instructor/api/get_problem_responses',
    #    data={'problem_location': 'block-v1:cmm+SYSDPA02+2020_2+type@vertical+block@574936cda264472d8e06c4175a0521e7'},
    #    headers=headers)
    #print(r.json())
