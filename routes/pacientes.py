from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from helpers import rol_requerido
from models import db, Paciente
from forms import PacienteForm

pacientes_bp = Blueprint('pacientes', __name__)


@pacientes_bp.route('/pacientes')
@login_required
def pacientes_lista():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    query = Paciente.query
    if q:
        like = f'%{q}%'
        query = query.filter(
            db.or_(Paciente.nombre.ilike(like),
                   Paciente.apellido.ilike(like),
                   Paciente.rut.ilike(like))
        )
    pagination = query.order_by(Paciente.apellido).paginate(page=page, per_page=20, error_out=False)
    pacientes = pagination.items
    return render_template('pacientes_lista.html', pacientes=pacientes, q=q, pagination=pagination)


@pacientes_bp.route('/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
def paciente_nuevo():
    form = PacienteForm()
    if form.validate_on_submit():
        paciente = Paciente(
            rut=form.rut.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data
        )
        try:
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente creado correctamente', 'success')
            return redirect(url_for('pacientes.pacientes_lista'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: el RUT ya existe o hay datos duplicados', 'danger')
    return render_template('pacientes_form.html', form=form, accion='Nuevo')


@pacientes_bp.route('/pacientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def paciente_editar(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    if form.validate_on_submit():
        form.populate_obj(paciente)
        try:
            db.session.commit()
            flash('Paciente actualizado correctamente', 'success')
            return redirect(url_for('pacientes.pacientes_lista'))
        except IntegrityError:
            db.session.rollback()
            flash('Error al actualizar: datos duplicados', 'danger')
    return render_template('pacientes_form.html', form=form, accion='Editar')


@pacientes_bp.route('/pacientes/<int:id>/eliminar', methods=['POST'])
@login_required
@rol_requerido('admin')
def paciente_eliminar(id):
    paciente = Paciente.query.get_or_404(id)
    if paciente.citas:
        flash('No se puede eliminar: el paciente tiene citas registradas', 'warning')
    else:
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente eliminado', 'info')
    return redirect(url_for('pacientes.pacientes_lista'))
