from app import create_app
from flask_script import Manager
from config import DevConfig

app = create_app(DevConfig)
# manager = Manager(app)

if __name__ == '__main__':
    # manager.run()
    app.run()
