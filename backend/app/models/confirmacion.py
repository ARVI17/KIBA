# backend/app/models/confirmacion.py

from backend.app.config import db
from datetime import datetime

class Confirmacion(db.Model):
    __tablename__ = 'confirmaciones'

    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    sms_id = db.Column(db.Integer, db.ForeignKey('sms.id'), nullable=False)
    confirmada_en = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    cita = db.relationship('Cita', backref='confirmaciones')
    sms = db.relationship('SMS', backref='confirmaciones')

    def __repr__(self):
        return f'<Confirmacion {self.id} - Cita {self.cita_id} - SMS {self.sms_id}>'
