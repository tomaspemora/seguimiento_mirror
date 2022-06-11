import driveapi
import sys

if __name__ == '__main__':
	driveapi.uploadFile(sys.argv[1],'1rUQsgAtbrSRW_C35MtPDJrJ1QCbhgVxp','ArchivoTest')
	driveapi.downloadFile('/var/www/html/seguimiento/archivoTestBjadaex.xlsx','1rUQsgAtbrSRW_C35MtPDJrJ1QCbhgVxp','ArchivoTest')
	#driveapi.downloadFile('/var/www/html/seguimiento/archivoTestBjadags.xlsx','1rUQsgAtbrSRW_C35MtPDJrJ1QCbhgVxp','ArchivoTestGS')