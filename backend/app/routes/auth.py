from flask import Blueprint, request, jsonify
from backend.app.config import db
from backend.app.models.user import Usuario
from backend.app.utils.token_manager import generar_token, token_requerido


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login_v2():
    """Login endpoint using email and password with detailed errors."""
    datos = request.get_json() or {}
    email = datos.get('email')
    password = datos.get('password')

    if not email or not password:
        return jsonify({'success': False, 'error': 'Faltan credenciales'}), 400

    usuario = Usuario.query.filter_by(correo=email).first()
    if not usuario:
        return jsonify({'success': False, 'error': 'Email no registrado'}), 404

    if not usuario.verificar_contrasena(password):
        return jsonify({'success': False, 'error': 'Contraseña incorrecta'}), 401

    token = generar_token(usuario)
    return jsonify({'success': True, 'token': token})

@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()

    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    if not correo or not contrasena:
        return jsonify({'error': 'Correo y contraseña son obligatorios.'}), 400

    usuario = Usuario.query.filter_by(correo=correo).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    if not usuario.verificar_contrasena(contrasena):
        return jsonify({'error': 'Contraseña incorrecta.'}), 401

    # Generar Token JWT
    token = generar_token(usuario)

    return jsonify({
        'mensaje': 'Login exitoso',
        'token': token,
        'rol': usuario.rol.nombre
    }), 200

@auth_bp.route('/crear-admin', methods=['POST'])
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

@auth_bp.route('/perfil', methods=['GET'])
@token_requerido
def perfil():
    usuario = request.usuario
    return jsonify({
        'mensaje': 'Acceso permitido',
        'correo': usuario.correo,
        'rol': usuario.rol.nombre
    }), 200

@auth_bp.route('/crear-usuario', methods=['POST'])
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
