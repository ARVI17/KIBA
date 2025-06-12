# backend/app/utils/token_manager.py

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from backend.app.config import db
from backend.app.models.user import Usuario


# Función para generar el token
def generar_token(usuario):
    payload = {
        'id': usuario.id,
        'correo': usuario.correo,
        'rol': usuario.rol.nombre,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)  # Válido por 12 horas
    }
    secret = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

# Decorador para proteger rutas
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            if token.startswith('Bearer '):
                token = token[len('Bearer '):]

        if not token:
            return jsonify({'error': 'Token de acceso requerido.'}), 401

        try:
            secret = current_app.config['SECRET_KEY']
            datos = jwt.decode(token, secret, algorithms=['HS256'])
            usuario = Usuario.query.get(datos['id'])
            if not usuario:
                return jsonify({'error': 'Usuario no válido.'}), 401
            request.usuario = usuario  # Guardamos el usuario logueado en request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado, vuelve a iniciar sesión.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido.'}), 401

        return f(*args, **kwargs)

    return decorador
