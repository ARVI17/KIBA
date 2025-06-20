# backend/app/routes/paciente.py

import logging
from flask import Blueprint, request, jsonify
from backend.app.config import db
from backend.app.models.paciente import Paciente
from backend.app.models.sms import Especialidad
from backend.app.utils.token_manager import token_requerido
from datetime import datetime


logger = logging.getLogger(__name__)
paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route('/pacientes', methods=['POST'])
@token_requerido
def crear_paciente():
    datos = request.get_json()

    nombre = datos.get('nombre')
    celular = datos.get('celular')
    especialidad_id = datos.get('especialidad_id')
    programada = datos.get('programada')  # Opcional

    if not nombre or not celular or not especialidad_id:
        return jsonify({'error': 'Faltan datos obligatorios.'}), 400

    if Paciente.query.filter_by(celular=celular).first():
        return jsonify({'error': 'Ya existe un paciente con este celular.'}), 400

    programada_dt = None
    if programada:
        try:
            programada_dt = datetime.strptime(programada, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD HH:MM:SS'}), 400

    nuevo_paciente = Paciente(
        nombre=nombre,
        celular=celular,
        especialidad_id=especialidad_id,
        programada=programada_dt
    )

    db.session.add(nuevo_paciente)
    db.session.commit()

    return jsonify({'mensaje': 'Paciente creado exitosamente.'}), 201

@paciente_bp.route('/pacientes', methods=['GET'])
@token_requerido
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([paciente.to_dict() for paciente in pacientes]), 200
