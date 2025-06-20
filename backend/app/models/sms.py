# backend/app/models/sms.py

from backend.app.config import db
from datetime import datetime

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'<Especialidad {self.nombre}>'

class SMS(db.Model):
    __tablename__ = 'sms'
    id = db.Column(db.Integer, primary_key=True)
    celular = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    fecha_envio = db.Column(db.DateTime, index=True)
    estado = db.Column(db.String(50), index=True)
    token_confirmacion = db.Column(db.String(50), unique=True, index=True)
    confirmado = db.Column(db.Boolean, default=False)

    especialidad = db.relationship(
        'Especialidad',
        backref=db.backref('sms', lazy='selectin'),
        lazy='joined'
    )

    def __repr__(self):
        return f'<SMS {self.celular}>'


