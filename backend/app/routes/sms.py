# backend/app/routes/sms.py

from flask import Blueprint, request, jsonify
import requests
import json
import os
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.app.config import db
from backend.app.models.sms import Especialidad, SMS, Confirmacion
from backend.app.models.user import Usuario  # Si deseas asociar con usuario

sms_bp = Blueprint('sms', __name__)

# ========================
# Funciones auxiliares
# ========================

def obtener_headers():
    return {
        "Content-Type": "application/json",
        "Account": os.getenv("HABLAME_ACCOUNT"),
        "ApiKey": os.getenv("HABLAME_APIKEY"),
        "Token": os.getenv("HABLAME_TOKEN")
    }

# ========================
# Enviar SMS individual
# ========================

@sms_bp.route('/enviar-sms', methods=['POST'])
def enviar_sms():
    data = request.get_json()
    numero = data.get('numero')
    mensaje = data.get('mensaje')

    headers = obtener_headers()
    payload = {
        "flash": "0",
        "sc": "890202",
        "request_dlvr_rcpt": "0",
        "bulk": [
            {
                "numero": numero,
                "sms": mensaje
            }
        ]
    }

    try:
        res = requests.post("https://api103.hablame.co/api/sms/v3/send/marketing/bulk",
                            headers=headers, data=json.dumps(payload))

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
def importar_sms():
    data = request.get_json()
    mensajes = data.get('mensajes')

    headers = obtener_headers()
    bulk = [{"numero": m["numero"], "sms": m["mensaje"]} for m in mensajes]

    payload = {
        "flash": "0",
        "sc": "890202",
        "request_dlvr_rcpt": "0",
        "bulk": bulk
    }

    try:
        res = requests.post("https://api103.hablame.co/api/sms/v3/send/marketing/bulk",
                            headers=headers, data=json.dumps(payload))

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
