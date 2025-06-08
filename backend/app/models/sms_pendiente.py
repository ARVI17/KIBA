# backend/app/models/sms_pendiente.py

from backend.app.config import db

class SMSPendiente(db.Model):
    __tablename__ = 'sms_pendientes'

    id = db.Column(db.Integer, primary_key=True)
    celular = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    especialidad = db.Column(db.String(100))
    fecha_programada = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='pendiente')  # Estados posibles: pendiente, enviado, fallido

    def __repr__(self):
        return f'<SMSPendiente {self.celular} - {self.estado}>'
