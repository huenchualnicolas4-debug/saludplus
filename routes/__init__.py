from .auth import auth_bp
from .dashboard import dashboard_bp
from .pacientes import pacientes_bp
from .medicos import medicos_bp
from .citas import citas_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(medicos_bp)
    app.register_blueprint(citas_bp)
