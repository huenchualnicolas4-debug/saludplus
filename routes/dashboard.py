from datetime import datetime, timezone

from flask import Blueprint, render_template
from flask_login import login_required

from models import db, Paciente, Medico, Cita


dashboard_bp = Blueprint('main', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    ahora_utc = datetime.now(timezone.utc)
    stats = {
        'pacientes': Paciente.query.count(),
        'medicos': Medico.query.filter_by(activo=True).count(),
        'citas_hoy': Cita.query.filter(
            db.func.date(Cita.fecha_hora) == ahora_utc.date()
        ).count(),
        'citas_pendientes': Cita.query.filter_by(estado='pendiente').count()
    }
    citas_proximas = Cita.query.filter(
        Cita.fecha_hora >= ahora_utc
    ).order_by(Cita.fecha_hora).limit(5).all()

    return render_template('dashboard.html', stats=stats, citas=citas_proximas)
