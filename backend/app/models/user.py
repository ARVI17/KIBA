# backend/app/models/user.py

import bcrypt
from backend.app.config import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    rol = db.relationship(
        'Rol',
        backref=db.backref('usuarios', lazy='selectin'),
        lazy='joined'
    )

    def set_contrasena(self, contrasena_plana):
        self.contrasena = bcrypt.hashpw(contrasena_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_contrasena(self, contrasena_plana):
        return bcrypt.checkpw(contrasena_plana.encode('utf-8'), self.contrasena.encode('utf-8'))

    def __repr__(self):
        return f'<Usuario {self.correo}>'
