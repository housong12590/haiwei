from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
import models

app = create_app()

manager = Manager(app)

"""
 python manage.py db init 
 python manage.py db migrate -m "initial migration"
 python manage.py db upgrade
"""
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
