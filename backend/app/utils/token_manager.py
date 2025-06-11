# backend/app/utils/token_manager.py

import os
import jwt
import datetime
from flask import request, jsonify
from backend.app.config import db
from backend.app.models.user import Usuario

# Clave secreta para firmar el Token JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-super-secreta-kiba')

# Función para generar el token
def generar_token(usuario):
    payload = {
        'id': usuario.id,
        'correo': usuario.correo,
        'rol': usuario.rol.nombre,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)  # Válido por 12 horas
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Decorador para proteger rutas
def token_requerido(f):
    def decorador(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'error': 'Token de acceso requerido.'}), 401

        try:
            datos = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            usuario = Usuario.query.get(datos['id'])
            if not usuario:
                return jsonify({'error': 'Usuario no válido.'}), 401
            request.usuario = usuario  # Guardamos el usuario logueado en request
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado, vuelve a iniciar sesión.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido.'}), 401

        return f(*args, **kwargs)

    decorador.__name__ = f.__name__
    return decorador
