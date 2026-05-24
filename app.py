"""
SaludPlus - Sistema de Gestión de Reservas Médicas
==================================================
Aplicación web Flask con:
  - Autenticación segura (bcrypt + Flask-Login)
  - Autorización por roles (admin, recepcionista, medico)
  - CRUD completo de pacientes, médicos y citas
  - Protección contra inyección SQL vía SQLAlchemy ORM
  - Protección CSRF en todos los formularios (Flask-WTF)
  - Validación de datos del lado del servidor (WTForms)
  - Listo para despliegue en Render.com con PostgreSQL
"""

from datetime import timezone

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager

from config import Config
from models import db, Usuario
from routes import register_blueprints


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Debes iniciar sesión para acceder'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def cargar_usuario(user_id):
    return Usuario.query.get(int(user_id))


def local_datetime(value):
    """Convierte una fecha UTC a hora local de Santiago para el frontend."""
    if value is None:
        return ''
    try:
        from zoneinfo import ZoneInfo
    except Exception:
        return value

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(ZoneInfo('America/Santiago'))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.jinja_env.filters['local_datetime'] = local_datetime

    register_blueprints(app)

    @app.route('/')
    def index():
        from flask_login import current_user
        return redirect(url_for('main.dashboard') if current_user.is_authenticated else url_for('auth.login'))

    @app.errorhandler(404)
    def no_encontrado(e):
        return render_template('error.html', codigo=404, mensaje='Página no encontrada'), 404

    @app.errorhandler(500)
    def error_servidor(e):
        return render_template('error.html', codigo=500, mensaje='Error interno del servidor'), 500

    return app


app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
