# para empezar

crear un entorno virtual:

`python -m venv env`

activar entorno:

`env\Scripts\activate`

instalar paquetes:

`pip install -r requirements.txt`

definir variables de entorno: 

powershell:
`$env:FLASK_APP = run.py`
`$env:FLASK_ENV = development`

cmd:
`set FLASK_APP = run.py`
`set FLASK_ENV = development`

linux:
`export FLASK_APP = run.py`
`export FLASK_ENV = development` 

luego, iniciar MYSQL (la primera vez correr `py migrate.py` para crear db)

por último iniciar la app de flask:
`flask run`

Si no se inicia se puede probar con `py run.py` pero trae problemas con sqlalchemy y la librería del profiling.

TODO:
- registrar ejecuciones de usuarios en un log
- boton enviar reporte para usuarios no admin cuando les salga un error en la ejecución.