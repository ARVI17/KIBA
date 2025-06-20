# backend/app/routes/confirmacion.py
import logging
from flask import Blueprint, jsonify, request
from backend.app.models.confirmacion import Confirmacion
from backend.app.config import db
from backend.app.models.sms import SMS
from backend.app.models.cita import Cita
from backend.app.models.paciente import Paciente
from backend.app.utils.token_manager import token_requerido
from datetime import datetime, time

logger = logging.getLogger(__name__)
confirmacion_bp = Blueprint('confirmacion', __name__)

@confirmacion_bp.route('/confirmaciones', methods=['GET'])
@token_requerido
def obtener_confirmaciones():
    fecha_filtro = request.args.get('fecha')  # Formato esperado: YYYY-MM-DD
    paciente_id = request.args.get('paciente_id')

    query = Confirmacion.query

    joined = False
    if fecha_filtro or paciente_id:
        query = query.join(Cita)
        joined = True

    if fecha_filtro:
        try:
            fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            inicio = datetime.combine(fecha, time.min)
            fin = datetime.combine(fecha, time.max)
            query = query.filter(Cita.fecha_hora >= inicio, Cita.fecha_hora <= fin)
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}), 400

    if paciente_id:
        if not joined:
            query = query.join(Cita)
            joined = True
        query = query.filter(Cita.paciente_id == paciente_id)

    confirmaciones = query.all()
    resultado = []

    for conf in confirmaciones:
        cita = conf.cita
        paciente = cita.paciente
        especialidad = cita.especialidad
        sms = conf.sms

        resultado.append({
            "id_confirmacion": conf.id,
            "confirmada_en": conf.confirmada_en.strftime('%Y-%m-%d %H:%M:%S'),
            "sms_id": sms.id,
            "mensaje_sms": sms.mensaje,
            "estado_sms": sms.estado,
            "numero_enviado": sms.celular,
            "fecha_sms": sms.fecha_envio.strftime('%Y-%m-%d %H:%M:%S') if sms.fecha_envio else None,
            "cita_id": cita.id,
            "fecha_cita": cita.fecha_hora.strftime('%Y-%m-%d %H:%M'),
            "paciente": {
                "id": paciente.id,
                "nombre": paciente.nombre,
                "celular": paciente.celular
            },
            "especialidad": especialidad.nombre
        })

    return jsonify(resultado)
