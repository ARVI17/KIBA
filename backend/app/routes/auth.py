from flask import Blueprint, request, jsonify
import logging
from backend.app.config import db
from backend.app.models.user import Usuario
from backend.app.utils.token_manager import generar_token, token_requerido

logger = logging.getLogger(__name__)


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['POST'])
def login():
    datos = request.get_json() or {}
    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    logger.info("Login intento para %s", correo)

    if not correo or not contrasena:
        logger.warning("Login fallido: faltan datos")
        return jsonify({'error': 'Correo y contraseña son obligatorios.'}), 400

    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario:
        logger.warning("Login fallido: usuario no encontrado")
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    if not usuario.verificar_contrasena(contrasena):
        logger.warning("Login fallido: contraseña incorrecta")
        return jsonify({'error': 'Contraseña incorrecta.'}), 401

    token = generar_token(usuario)
    logger.info("Login exitoso para %s", correo)
    return jsonify({'mensaje': 'Login exitoso', 'token': token, 'rol': usuario.rol.nombre}), 200

@auth.route('/crear-admin', methods=['POST'])
def crear_admin():
    datos = request.get_json()

    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    if not correo or not contrasena:
        return jsonify({'error': 'Correo y contraseña son obligatorios.'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Usuario ya existe.'}), 400

    nuevo_usuario = Usuario(correo=correo, rol_id=1)
    nuevo_usuario.set_contrasena(contrasena)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Administrador creado exitosamente.'}), 201

@auth.route('/perfil', methods=['GET'])
@token_requerido
def perfil():
    usuario = request.usuario
    return jsonify({
        'mensaje': 'Acceso permitido',
        'correo': usuario.correo,
        'rol': usuario.rol.nombre
    }), 200

@auth.route('/crear-usuario', methods=['POST'])
@token_requerido
def crear_usuario():
    usuario_actual = request.usuario

    # Validar que sea administrador
    if usuario_actual.rol.nombre != 'Administrador':
        return jsonify({'error': 'Acceso denegado. Solo administradores pueden crear usuarios.'}), 403

    datos = request.get_json()

    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    if not correo or not contrasena:
        return jsonify({'error': 'Correo y contraseña son obligatorios.'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'error': 'Usuario ya existe.'}), 400

    nuevo_usuario = Usuario(
        correo=correo,
        rol_id=2  # Rol Operador
    )
    nuevo_usuario.set_contrasena(contrasena)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario operador creado exitosamente.'}), 201
