# backend/app/routes/sms.py

import logging
from flask import Blueprint, request, jsonify
import asyncio
import json
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.app.config import db
from backend.app.models.sms import Especialidad, SMS
from backend.app.models.confirmacion import Confirmacion
from backend.app.utils.token_manager import token_requerido
from backend.app.hablame_client import HablameClient

logger = logging.getLogger(__name__)
sms_bp = Blueprint('sms', __name__)
_hablame_client = HablameClient()

# ========================
# Enviar SMS individual
# ========================

@sms_bp.route('/enviar-sms', methods=['POST'])
@token_requerido
def enviar_sms():
    data = request.get_json()
    numero = data.get('numero')
    mensaje = data.get('mensaje')

    bulk = [{"numero": numero, "sms": mensaje}]

    try:
        res = asyncio.run(_hablame_client.send_sms(bulk))

        if res.status_code == 200:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'detalle': res.text}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========================
# Importar múltiples SMS
# ========================

@sms_bp.route('/importar-sms', methods=['POST'])
@token_requerido
def importar_sms():
    data = request.get_json()
    mensajes = data.get('mensajes')

    bulk = [{"numero": m["numero"], "sms": m["mensaje"]} for m in mensajes]

    try:
        res = asyncio.run(_hablame_client.send_sms(bulk))

        if res.status_code == 200:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'detalle': res.text}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========================
# Dashboard de SMS
# ========================

@sms_bp.route('/dashboard', methods=['GET'])
@token_requerido
def dashboard():
    hoy = datetime.now().date()

    enviados_hoy = db.session.query(func.count(SMS.id)).filter(
        func.date(SMS.fecha_envio) == hoy
    ).scalar()

    entregados = db.session.query(func.count(SMS.id)).filter(
        SMS.estado == 'Entregado', func.date(SMS.fecha_envio) == hoy
    ).scalar()

    fallidos = db.session.query(func.count(SMS.id)).filter(
        SMS.estado == 'Fallido', func.date(SMS.fecha_envio) == hoy
    ).scalar()

    dias = []
    cantidades = []
    for i in range(6, -1, -1):  # Últimos 7 días
        dia = hoy - timedelta(days=i)
        count = db.session.query(func.count(SMS.id)).filter(
            func.date(SMS.fecha_envio) == dia
        ).scalar()
        dias.append(dia.strftime("%d/%m"))
        cantidades.append(count)

    return jsonify({
        'enviados': enviados_hoy,
        'entregados': entregados,
        'fallidos': fallidos,
        'dias': dias,
        'cantidades': cantidades
    })

# ========================
# Historial de SMS
# ========================

@sms_bp.route('/historial', methods=['GET'])
@token_requerido
def historial_sms():
    mensajes = db.session.query(SMS).order_by(SMS.fecha_envio.desc()).all()

    result = [
        {
            "fecha_envio": m.fecha_envio.strftime("%Y-%m-%d %H:%M") if m.fecha_envio else "",
            "numero": m.celular,
            "mensaje": m.mensaje,
            "estado": m.estado,
        }
        for m in mensajes
    ]

    return jsonify(result)
