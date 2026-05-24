"""
Formularios con validación del lado del servidor.
WTForms valida los datos antes de tocar la BD, evitando que datos
maliciosos o malformados lleguen a las consultas (Goodrich y Tamassia, 2014).
También incorpora tokens CSRF automáticamente vía Flask-WTF.
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectField, DateField,
                     DateTimeLocalField, TextAreaField, SubmitField)
from wtforms.validators import (DataRequired, Email, Length, Regexp,
                                EqualTo, Optional)


class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50)
    ])
    contrasena = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, max=100)
    ])
    submit = SubmitField('Iniciar sesión')


class PacienteForm(FlaskForm):
    rut = StringField('RUT', validators=[
        DataRequired(),
        Regexp(r'^\d{7,8}-[\dkK]$', message='Formato: 12345678-9')
    ])
    nombre = StringField('Nombre', validators=[
        DataRequired(), Length(min=2, max=60)
    ])
    apellido = StringField('Apellido', validators=[
        DataRequired(), Length(min=2, max=60)
    ])
    fecha_nacimiento = DateField('Fecha de nacimiento', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    telefono = StringField('Teléfono', validators=[
        Optional(),
        Regexp(r'^\+?\d{8,15}$', message='Solo números, opcionalmente con +')
    ])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Guardar')


class MedicoForm(FlaskForm):
    rut = StringField('RUT', validators=[
        DataRequired(),
        Regexp(r'^\d{7,8}-[\dkK]$', message='Formato: 12345678-9')
    ])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=60)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    especialidad_id = SelectField('Especialidad', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')


class CitaForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    medico_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    fecha_hora = DateTimeLocalField('Fecha y hora', 
                                    format='%Y-%m-%dT%H:%M',
                                    validators=[DataRequired()])
    motivo = StringField('Motivo', validators=[DataRequired(), Length(max=255)])
    estado = SelectField('Estado', choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('realizada', 'Realizada')
    ])
    notas = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Guardar')
