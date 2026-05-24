from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from models import db, Medico, Especialidad
from forms import MedicoForm
from helpers import rol_requerido

medicos_bp = Blueprint('medicos', __name__)


@medicos_bp.route('/medicos')
@login_required
def medicos_lista():
    page = request.args.get('page', 1, type=int)
    pagination = Medico.query.filter_by(activo=True).order_by(Medico.apellido).paginate(page=page, per_page=20, error_out=False)
    medicos = pagination.items
    return render_template('medicos_lista.html', medicos=medicos, pagination=pagination)


@medicos_bp.route('/medicos/nuevo', methods=['GET', 'POST'])
@login_required
@rol_requerido('admin')
def medico_nuevo():
    form = MedicoForm()
    form.especialidad_id.choices = [(e.id, e.nombre) for e in Especialidad.query.all()]
    if form.validate_on_submit():
        medico = Medico(
            rut=form.rut.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            especialidad_id=form.especialidad_id.data
        )
        try:
            db.session.add(medico)
            db.session.commit()
            flash('Médico creado correctamente', 'success')
            return redirect(url_for('medicos.medicos_lista'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: RUT o email duplicado', 'danger')
    return render_template('medicos_form.html', form=form, accion='Nuevo')
