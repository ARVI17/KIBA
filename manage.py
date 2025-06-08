# KIBA/manage.py
from backend.app.main import app
from backend.app.config import db
from flask_migrate import Migrate


# Configura Migrate
migrate = Migrate(app, db)


# Configura Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
