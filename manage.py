# KIBA/manage.py
import os

# Ensure a SECRET_KEY exists for the application
os.environ.setdefault('SECRET_KEY', 'kiba-insecure-secret')

from backend.app.main import app
from backend.app.config import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


# Configura Migrate
migrate = Migrate(app, db)


# Configura Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
