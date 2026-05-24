from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from forms import LoginForm
from models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nombre_usuario=form.usuario.data).first()
        if usuario and usuario.activo and usuario.check_password(form.contrasena.data):
            login_user(usuario)
            flash(f'Bienvenido, {usuario.nombre_completo}', 'success')
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        flash('Credenciales incorrectas', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))
