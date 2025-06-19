# backend/app/models/paciente.py

from backend.app.config import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(20), unique=True, nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    programada = db.Column(db.DateTime, nullable=True)

    especialidad = db.relationship('Especialidad', backref=db.backref('pacientes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'celular': self.celular,
            'especialidad': self.especialidad.nombre if self.especialidad else None,
            'programada': self.programada.strftime('%Y-%m-%d %H:%M:%S') if self.programada else None
        }
