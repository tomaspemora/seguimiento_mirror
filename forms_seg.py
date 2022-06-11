from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, RadioField, EmailField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import *
from flask_wtf import FlaskForm
from wtforms.validators import Regexp

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Promover')
    submit_degrada = SubmitField('Degradar')

class SeguimientoForm(FlaskForm):
    data_file = FileField(render_kw={'class': 'file-input', 'id' : 'data_file'}, validators=[Regexp('.+\.csv$')])  # add your class
    ora_file = FileField(render_kw={'class': 'file-input', 'id' : 'ora_file'}, validators=[Regexp('.+\.csv$')])  # add your class
    profile_file = FileField(render_kw={'class': 'file-input', 'id' : 'profile_file'}, validators=[Regexp('.+\.csv$')])  # add your class
    submit = SubmitField('Enviar',render_kw={'id' : 'form-button','onclick':'loader();'}, name='form-button')

def tabla_parametros_form(**kwargs):
    class TablaParametrosForm(FlaskForm):
        pass

    for k,v in kwargs.items():
        if isinstance(v,bool) or v.lower() in ('true', '1', 't','false','1','f'):
            field = BooleanField(k, render_kw ={'checked':v.lower() in ('true', '1', 't') })
        else:
            field = StringField(k, render_kw ={'placeholder': v, 'value': v })
        setattr(TablaParametrosForm, k, field)
    return TablaParametrosForm()
    