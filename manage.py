from app import create_app
from flask_script import Manager
from config import Config

app = create_app(Config)
manager = Manager(app)

if __name__ == '__main__':
    app.run()
    # manager.run()
