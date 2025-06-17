# backend/app/models/cita.py

import logging
from backend.app.config import db
from datetime import datetime

logger = logging.getLogger(__name__)

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    paciente = db.relationship('Paciente', backref='citas')
    especialidad = db.relationship('Especialidad', backref='citas')
    
    # Relación con confirmaciones
    confirmaciones = db.relationship('Confirmacion', back_populates='cita', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cita {self.id} - Paciente {self.paciente_id} - {self.fecha_hora}>'
