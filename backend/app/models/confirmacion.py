# backend/app/models/confirmacion.py

from backend.app.config import db
from datetime import datetime

class Confirmacion(db.Model):
    __tablename__ = 'confirmaciones'

    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False, index=True)
    sms_id = db.Column(db.Integer, db.ForeignKey('sms.id'), nullable=False, index=True)
    confirmada_en = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relaciones
    cita = db.relationship(
        'Cita',
        back_populates='confirmaciones',
        lazy='joined'
    )
    sms = db.relationship(
        'SMS',
        backref=db.backref('confirmaciones', lazy='selectin'),
        lazy='joined'
    )

    def __repr__(self):
        return f'<Confirmacion {self.id} - Cita {self.cita_id} - SMS {self.sms_id}>'
