# backend/app/routes/sms.py

from flask import Blueprint, request, jsonify
import requests
import json
import os
from datetime import datetime, timedelta
from sqlalchemy import func
from backend.app.config import db
from backend.app.models.sms import Especialidad, SMS
from backend.app.models.confirmacion import Confirmacion
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

    enviados_hoy = db.session.execute(
        "SELECT COUNT(*) FROM sms WHERE DATE(fecha_envio) = %s", (hoy,)
    ).scalar()

    entregados = db.session.execute(
        "SELECT COUNT(*) FROM sms WHERE estado = 'Entregado' AND DATE(fecha_envio) = %s", (hoy,)
    ).scalar()

    fallidos = db.session.execute(
        "SELECT COUNT(*) FROM sms WHERE estado = 'Fallido' AND DATE(fecha_envio) = %s", (hoy,)
    ).scalar()

    dias = []
    cantidades = []
    for i in range(6, -1, -1):  # Últimos 7 días
        dia = hoy - timedelta(days=i)
        count = db.session.execute(
            "SELECT COUNT(*) FROM sms WHERE DATE(fecha_envio) = %s", (dia,)
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
    rows = db.session.execute("SELECT fecha_envio, celular, mensaje, estado FROM sms ORDER BY fecha_envio DESC").fetchall()

    result = [{
        "fecha_envio": row[0].strftime("%Y-%m-%d %H:%M") if row[0] else "",
        "numero": row[1],
        "mensaje": row[2],
        "estado": row[3]
    } for row in rows]

    return jsonify(result)
