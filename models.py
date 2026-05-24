"""
Modelos de datos del sistema SaludPlus.

Diagrama Entidad-Relación:

    Usuario (autenticación)
        |
    Especialidad ──┐
                   │ 1:N
                   ▼
    Paciente ──N:1─┐
                   │
                   ▼
                  Cita ──N:1── Medico

Tablas:
    - usuarios:      autenticación y autorización por roles
    - especialidades: catálogo de especialidades médicas
    - medicos:       profesionales (FK → especialidades)
    - pacientes:     personas atendidas
    - citas:         reservas (FK → paciente, FK → medico)

El uso de SQLAlchemy ORM previene automáticamente las inyecciones SQL,
ya que todas las consultas se parametrizan internamente (OWASP, 2021).
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
import bcrypt

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


# ============== USUARIOS (autenticación) ==============

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False, index=True)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='recepcionista')
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime(timezone=True), default=utcnow)
    
    def set_password(self, contrasena):
        """Hashea la contraseña con bcrypt (salt automático, 12 rounds por defecto)"""
        salt = bcrypt.gensalt(rounds=12)
        self.contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, contrasena):
        """Verifica la contraseña en tiempo constante (resistente a timing attacks)"""
        return bcrypt.checkpw(
            contrasena.encode('utf-8'),
            self.contrasena_hash.encode('utf-8')
        )
    
    def es_admin(self):
        return self.rol == 'admin'
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario} ({self.rol})>'


# ============== ESPECIALIDADES ==============

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    
    medicos = db.relationship('Medico', backref='especialidad', lazy=True)
    
    def __repr__(self):
        return f'<Especialidad {self.nombre}>'


# ============== MÉDICOS ==============

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    citas = db.relationship('Cita', backref='medico', lazy=True)
    
    @property
    def nombre_completo(self):
        return f'Dr(a). {self.nombre} {self.apellido}'
    
    def __repr__(self):
        return f'<Medico {self.nombre_completo}>'


# ============== PACIENTES ==============

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    creado_en = db.Column(db.DateTime(timezone=True), default=utcnow)
    
    citas = db.relationship('Cita', backref='paciente', lazy=True)
    
    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    @property
    def edad(self):
        hoy = utcnow().date()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < 
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def __repr__(self):
        return f'<Paciente {self.nombre_completo}>'


# ============== CITAS ==============

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime(timezone=True), nullable=False)
    motivo = db.Column(db.String(255))
    estado = db.Column(db.String(20), default='pendiente')  
    # estados: pendiente | confirmada | cancelada | realizada
    notas = db.Column(db.Text)
    creada_en = db.Column(db.DateTime(timezone=True), default=utcnow)
    
    def __repr__(self):
        return f'<Cita {self.fecha_hora} - {self.estado}>'
