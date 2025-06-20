# backend/app/routes/cita.py

import logging
from flask import Blueprint, request, jsonify
from backend.app.config import db
from backend.app.models.cita import Cita
from backend.app.models.paciente import Paciente
from backend.app.models.sms import SMS
from backend.app.utils.token_manager import token_requerido
from datetime import datetime
from backend.app.models.confirmacion import Confirmacion


logger = logging.getLogger(__name__)
cita_bp = Blueprint('cita', __name__)

@cita_bp.route('/citas', methods=['POST'])
@token_requerido
def crear_cita():
    datos = request.get_json()

    celular = datos.get('celular')
    especialidad_id = datos.get('especialidad_id')
    fecha_hora = datos.get('fecha_hora')

    if not celular or not especialidad_id or not fecha_hora:
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    paciente = Paciente.query.filter_by(celular=celular).first()
    if not paciente:
        return jsonify({'error': 'Paciente no encontrado'}), 404

    # Verificar si el paciente ya tiene una cita a esa misma hora
    try:
        fecha_obj = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD HH:MM:SS'}), 400
    conflicto = Cita.query.filter_by(paciente_id=paciente.id, fecha_hora=fecha_obj).first()
    if conflicto:
        return jsonify({'error': 'El paciente ya tiene una cita programada en esa hora'}), 409

    nueva_cita = Cita(
        paciente_id=paciente.id,
        especialidad_id=especialidad_id,
        fecha_hora=fecha_obj
    )

    db.session.add(nueva_cita)
    db.session.commit()

    return jsonify({'mensaje': 'Cita registrada exitosamente'}), 201

@cita_bp.route('/confirmar-cita', methods=['POST'])
@token_requerido
def confirmar_cita():
    datos = request.get_json()

    celular = datos.get('celular')
    fecha_str = datos.get('fecha_hora')

    if not celular or not fecha_str:
        return jsonify({'error': 'Celular y fecha_hora son obligatorios'}), 400

    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD HH:MM:SS'}), 400

    paciente = Paciente.query.filter_by(celular=celular).first()
    if not paciente:
        return jsonify({'error': 'Paciente no encontrado'}), 404

    cita = Cita.query.filter_by(paciente_id=paciente.id, fecha_hora=fecha_obj).first()
    if not cita:
        return jsonify({'error': 'Cita no encontrada'}), 404

    sms = SMS.query.filter_by(celular=celular).order_by(SMS.fecha_envio.desc()).first()
    if not sms:
        return jsonify({'error': 'SMS relacionado no encontrado'}), 404

    confirmacion = Confirmacion(cita_id=cita.id, sms_id=sms.id)
    db.session.add(confirmacion)
    db.session.commit()

    return jsonify({'mensaje': '✅ Cita confirmada correctamente.'}), 200
