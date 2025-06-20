# backend/app/models/cita.py

from backend.app.config import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False, index=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False, index=True)
    fecha_hora = db.Column(db.DateTime, nullable=False, index=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relaciones
    paciente = db.relationship(
        'Paciente',
        backref=db.backref('citas', lazy='selectin'),
        lazy='joined'
    )
    especialidad = db.relationship(
        'Especialidad',
        backref=db.backref('citas', lazy='selectin'),
        lazy='joined'
    )
    
    # Relación con confirmaciones
    confirmaciones = db.relationship('Confirmacion', back_populates='cita', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cita {self.id} - Paciente {self.paciente_id} - {self.fecha_hora}>'
