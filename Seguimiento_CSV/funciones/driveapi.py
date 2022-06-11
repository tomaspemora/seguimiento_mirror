from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from pdb import set_trace as bp
from io import FileIO
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint
import logging
import pathlib

SCOPES = ['https://www.googleapis.com/auth/drive']

def uploadFile(local_file_name,drive_folder_toUpload,drive_file_name_toUpload,upload_type):
	# retorna 1 significa que el archivo se creo porque no se encontro en la carpeta de Drive especificada
	# retorna 2 significa que el archivo se updateo porque se encontro en la carpeta de Drive especificada
	# retorna 0 significa que el archivo que se iba a subir no se encontró
	
	if Path(local_file_name).is_file():
		[creds,service] = AuthGoogle()
		results = service.files().list(q='\''+drive_folder_toUpload+'\' in parents',fields='*').execute()
		files= results.get('files',[])
		file_id = None
		for f in files:
			if f['name'] == drive_file_name_toUpload:
				if f['id'] is not None:
					file_id = f['id']
					file_name = f['name']
					file_trashed = f['trashed']
					break

		if file_id is None:
			#create
			file_metadata = {'name': drive_file_name_toUpload, 'parents': [drive_folder_toUpload]}
			media = MediaFileUpload(local_file_name,mimetype=upload_type)
			file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
			# breakpoint()
			# print('El archivo local de planilla -> '+local_file_name+' fue creado en Drive ya que no había una versión anterior')
			# print('Cree Planilla')
			return 1, f"https://docs.google.com/spreadsheets/d/{file['id']}/edit"
		else:
			#update
			media = MediaFileUpload(local_file_name, mimetype=upload_type, resumable=True)
			updated_file = service.files().update(fileId=file_id,media_body=media).execute()
			# force set to trash = False if file is updated
			# breakpoint()
			if file_trashed:
				updated_file = service.files().get(fileId=file_id,fields='trashed').execute()
				updated_file['trashed'] = False
				service.files().update(fileId=file_id, body=updated_file).execute()
			# print('El archivo local de planilla -> '+local_file_name+' fue actualizado en Drive correctamente')
			return 2, f"https://docs.google.com/spreadsheets/d/{updated_file['id']}/edit"
	else:
		print('al intentar subir el archivo local '+local_file_name+ ' a Drive, no se encontró en la ruta local especificada.')
		return 0



def downloadFile(local_file_name,drive_folder_to_Download,drive_file_name_toDownload):

	[creds,service] = AuthGoogle()
	results = service.files().list(q='\''+drive_folder_to_Download+'\' in parents',fields='*').execute()
	files= results.get('files',[])
	file_id = None
	for f in files:
		if f['name'] == drive_file_name_toDownload:
			file_id = f['id']
			file_name = f['name']
			file_trashed = f['trashed']
			break
	
	if file_id is not None and not file_trashed:
		if f['mimeType'] == 'application/vnd.google-apps.spreadsheet':
			request = service.files().export(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		else:
			request = service.files().get_media(fileId=file_id)

		downloader = MediaIoBaseDownload(FileIO(local_file_name,'wb'), request)
		done = False
		while done is False:
			status, done = downloader.next_chunk()
		# print('El archivo en Drive -> '+drive_file_name_toDownload+' fue bajado correctamente')
		return 1
	else:
		print('al intentar bajar el archivo desde Drive, '+drive_file_name_toDownload +', no se encontró en la carpeta id: '+ drive_folder_to_Download)
		return 0		

def AuthGoogle():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			cred_dir = sorted(pathlib.Path('.').glob('**/credentials.json')) # La primera coincidencia dentro de la carpeta del archivo seg-config.env será la que se utilice para la configuración del seguimiento.

			flow = InstalledAppFlow.from_client_secrets_file(cred_dir[0], SCOPES)
			#flow = InstalledAppFlow.from_client_secrets_file('C:/CMM-LabE/Seguimiento CSV/credentials.json', SCOPES)
			creds = flow.run_local_server()
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds, cache_discovery=False)
	return [creds, service]

if __name__ == "__main__":

	#is_down = downloadFile(os.path.join(os.path.dirname(os.path.abspath(__file__)),'archivosRevision','planillas','nombre_interno.xlsx'),'1GgAUDy45gmzDtCxCl3jsdSEGLHMiHZvF','planilla_sheet')
	is_up = uploadFile("archivo.xlsx","1O_wB_e06yYTu12GPcpemfT_Cyvnnf-eD","archivazon",'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	print(is_up)