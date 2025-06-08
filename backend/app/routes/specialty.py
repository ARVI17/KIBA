# backend/app/routes/specialty.py

from flask import Blueprint, request, jsonify
from backend.app.config import db
from backend.app.models.sms import Especialidad
from backend.app.utils.token_manager import token_requerido  


specialty_bp = Blueprint('specialty', __name__)

@specialty_bp.route('/especialidades', methods=['POST'])
@token_requerido
def crear_especialidad():
    datos = request.get_json()
    nombre = datos.get('nombre')

    if not nombre:
        return jsonify({'error': 'El nombre de la especialidad es obligatorio.'}), 400

    if Especialidad.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'La especialidad ya existe.'}), 400

    nueva_especialidad = Especialidad(nombre=nombre)
    db.session.add(nueva_especialidad)
    db.session.commit()

    return jsonify({'mensaje': 'Especialidad creada exitosamente.'}), 201

@specialty_bp.route('/especialidades', methods=['GET'])
@token_requerido
def listar_especialidades():
    especialidades = Especialidad.query.all()
    resultado = [{'id': esp.id, 'nombre': esp.nombre} for esp in especialidades]

    return jsonify(resultado), 200
