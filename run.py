#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil, csv, io, traceback, logging, requests, json, sys, os
sys.path.insert(0, 'Seguimiento_CSV')
from flask_wtf import CSRFProtect
from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap5
from flask import request, redirect, url_for
from pdb import set_trace as bp
from Seguimiento_CSV.Seguimiento2 import Seguimiento 
import flask_debugtoolbar
from flask_debugtoolbar_lineprofilerpanel.profile import line_profile
from flask import send_from_directory
from dotenv import dotenv_values
# instantiate a flask app
app = Flask(__name__)
cors = CORS(app)
Bootstrap5(app)
app.secret_key = 'dev'
app.config['WTF_CSRF_ENABLED'] = False
# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme
# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

## _____________ DATA BASE ________________
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
from forms_seg import *
import pathlib

config = dotenv_values('.env')
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_LOCALHOST']}/{config['MYSQL_DATABASE']}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
from models_seg import User#, db
## _____________ DATA BASE ________________

# csrf = CSRFProtect(app)
# csrf.init_app(app)

# from custom_jinja_filters import custom_function
# app.jinja_env.filters["custom_function"] = custom_function

# routes
@cross_origin()
@app.route('/', methods=['POST','GET'])
@login_required
# @line_profile
def index():
    dotenv_dir = sorted(pathlib.Path('.').glob('**/seg-config.env'))
    config_dir = dotenv_values(dotenv_dir[0]) 
    form1 = tabla_parametros_form(**config_dir)
    if request.method == "POST":
        if current_user.is_admin and len(request.form) > 1:
            parametros_form = request.form
            # breakpoint()
            for k in config_dir.keys():
                if config_dir[k].lower() in ('true', '1', 't','false','1','f'):
                    config_dir[k] = 'False'
            keys_to_iterate = config_dir.keys() & parametros_form.keys()
            for k in keys_to_iterate:
                if config_dir[k].lower() in ('true', '1', 't','false','1','f'):
                    if parametros_form[k] == 'y':
                        config_dir[k] = 'True'
                else:
                    config_dir[k] = parametros_form[k]
        file_list = {  
                        'data_file' : request.files.get('data_file') ,
                        'ora_file' : request.files.get('ora_file') ,
                        'profile_file' : request.files.get('profile_file')
                    }
        [_,seguimiento_response, string_error] = seguimiento(file_list, config_dir)
        if current_user.is_admin:
            form1 = tabla_parametros_form(**config_dir)
        return render_template('index.html', seg_response = seguimiento_response , str_error = string_error,
                                form=SeguimientoForm(), config=config_dir, tabla_form = form1)
    return render_template('index.html', form=SeguimientoForm(), config=config_dir, tabla_form = form1)


@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('Seguimiento_CSV/Generado/Xls/', path)

@cross_origin()
@app.route('/admin', methods = ['POST','GET'])
@login_required
def admin():
    print(current_user.is_admin)
    if not current_user.is_admin:
        return render_template('index.html', form=SeguimientoForm(), admin=current_user.is_admin, config=config)
    form = AdminForm()
    error = None
    if form.validate_on_submit():
        if form.data['submit_degrada']:
            mail_to_degrade = form.email.data
            user = User.get_by_email(mail_to_degrade)
            if user is None:
                error = f'El mail {mail_to_degrade} no existe en la base de datos.'
            if user == current_user:
                error = f'No se puede degradar a sí mismo.'
            else:
                user.set_admin(False)
                user.save()            
                error = f'El usuario de {user.name} - {mail_to_degrade} fue degradado a no-admin'
                return render_template('admin.html', form=AdminForm(), admin=current_user.is_admin, error = error)
        else:            
            mail_to_promote = form.email.data
            user = User.get_by_email(mail_to_promote)
            if user is None:
                error = f'El mail {mail_to_promote} no existe en la base de datos.'
            else:
                user.set_admin(True)
                user.save()            
                error = f'El usuario de {user.name} - {mail_to_promote} fue promovido a admin'
                return render_template('admin.html', form = AdminForm(), admin=current_user.is_admin, error = error)
    return render_template('admin.html', form = AdminForm(), admin=current_user.is_admin , error = error)

def seguimiento(file_list, config_seg):
    # aca debería hacer una validación de los archivos primero
    seg = Seguimiento()
    prof_data_text = file_list['profile_file'].read().decode("utf-8")
    prof_data_io = io.StringIO(prof_data_text, newline='\n')
    prof_data_obj = {'fs': file_list['profile_file'], 'io_obj': prof_data_io}

    ora_data_text = file_list['ora_file'].read().decode("utf-8")
    ora_data_io = io.StringIO(ora_data_text, newline='\n')
    ora_data_obj = {'fs': file_list['ora_file'], 'io_obj': ora_data_io}

    student_data_text = file_list['data_file'].read().decode("utf-8")
    student_data_io = io.StringIO(student_data_text, newline='\n')
    student_data_obj = {'fs': file_list['data_file'], 'io_obj': student_data_io}
    try:
        seguimiento_response = seg.ejecutar(student_data_obj,ora_data_obj,prof_data_obj, seg_config=config_seg)
        string_error = 'No errors'
    except BaseException as error:
        string_error = str(traceback.format_exc())
        seguimiento_response = {
                                'error':'el seguimiento genero errores en su ejecución',
                                'error_detail' : string_error
                                }
    
    return [file_list, seguimiento_response, string_error]

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            error = f'Inicio de sesión incorrecto'
    return render_template('login_form.html', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__=='__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.debug = True

    # Specify the debug panels you want
    app.config['DEBUG_TB_PANELS'] = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the line profiling
        'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel'
    ]
    toolbar = flask_debugtoolbar.DebugToolbarExtension(app)
    app.run(debug=True,host='localhost')