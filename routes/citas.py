from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import db, Paciente, Medico, Cita
from forms import CitaForm

citas_bp = Blueprint('citas', __name__)


@citas_bp.route('/citas')
@login_required
def citas_lista():
    estado = request.args.get('estado', '')
    page = request.args.get('page', 1, type=int)
    query = Cita.query
    if estado:
        query = query.filter_by(estado=estado)
    pagination = query.order_by(Cita.fecha_hora.desc()).paginate(page=page, per_page=20, error_out=False)
    citas = pagination.items
    return render_template('citas_lista.html', citas=citas, estado=estado, pagination=pagination)


@citas_bp.route('/citas/nueva', methods=['GET', 'POST'])
@login_required
def cita_nueva():
    form = CitaForm()
    form.paciente_id.choices = [
        (p.id, f'{p.nombre_completo} ({p.rut})')
        for p in Paciente.query.order_by(Paciente.apellido).all()
    ]
    form.medico_id.choices = [
        (m.id, f'{m.nombre_completo} - {m.especialidad.nombre}')
        for m in Medico.query.filter_by(activo=True).all()
    ]

    if form.validate_on_submit():
        local_tz = ZoneInfo('America/Santiago')
        fecha_local = form.fecha_hora.data
        if fecha_local.tzinfo is None:
            fecha_utc = fecha_local.replace(tzinfo=local_tz).astimezone(timezone.utc)
        else:
            fecha_utc = fecha_local.astimezone(timezone.utc)

        cita = Cita(
            paciente_id=form.paciente_id.data,
            medico_id=form.medico_id.data,
            fecha_hora=fecha_utc,
            motivo=form.motivo.data,
            estado=form.estado.data or 'pendiente',
            notas=form.notas.data
        )
        db.session.add(cita)
        db.session.commit()
        flash('Cita agendada correctamente', 'success')
        return redirect(url_for('citas.citas_lista'))

    return render_template('citas_form.html', form=form, accion='Nueva')


@citas_bp.route('/citas/<int:id>/cancelar', methods=['POST'])
@login_required
def cita_cancelar(id):
    cita = Cita.query.get_or_404(id)
    cita.estado = 'cancelada'
    db.session.commit()
    flash('Cita cancelada', 'info')
    return redirect(url_for('citas.citas_lista'))
