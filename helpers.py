from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user


def rol_requerido(*roles):
    """Restringe acceso por rol (autorización)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.rol not in roles:
                flash('No tienes permisos para esta acción', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
