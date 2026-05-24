"""
Configuración de la aplicación SaludPlus.
Se separan entornos de desarrollo y producción usando variables de entorno,
siguiendo la metodología The Twelve-Factor App (Wiggins, 2017).
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables desde archivo .env

class Config:
    """Configuración base"""
    # Clave secreta para firmar cookies de sesión y tokens CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'desarrollo-cambiar-en-produccion'
    
    # URL de la base de datos:
    #  - En Render.com se inyecta automáticamente como DATABASE_URL (PostgreSQL)
    #  - En local cae a SQLite si no hay variable definida
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///saludplus_local.db')
    # Render usa "postgres://" pero SQLAlchemy requiere "postgresql://"
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = db_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de seguridad de sesiones
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True   # No accesible vía JavaScript (anti-XSS)
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección contra CSRF
    
    # Configuración WTF (protección CSRF activa por defecto)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora
