import os


class Config(object):
    DEBUG = True

    SECRET_KEY = 'mwpcfnnwttcclwaf0r3bxwe3jr7epk74'

    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '123.207.152.86'

    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)

    MYSQL_DB = os.environ.get('MYSQL_DB') or 'ghost'

    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'

    MYSQL_PWD = os.environ.get('MYSQL_PASSWORD') or '123546'

    ORATOR_DATABASES = {
        'default': 'mysql',
        'mysql': {
            'driver': 'mysql',
            'host': MYSQL_HOST,
            'port': int(MYSQL_PORT),
            'database': MYSQL_DB,
            'user': MYSQL_USER,
            'password': MYSQL_PWD,
            'log_queries': DEBUG
        }
    }

    PROJECT_LIST = 'http://aegaeon.default.192.168.0.240.xip.io/products'

    # 开发环境k8s部署url
    DEPLOY_DEV_URL = 'http://aegaeon-dev.default.192.168.0.240.xip.io/products'

    # 生产环境k8s部署url
    DEPLOY_PRO_URL = 'http://aegaeon.default.192.168.0.240.xip.io/products'

    PROJECTS_PATH = './config/project.json'

    PROJECTS_DATA = None

    @staticmethod
    def projects(update=False) -> dict:
        if Config.PROJECTS_DATA is None or update:
            with open(Config.PROJECTS_PATH, 'r', encoding='utf8') as f:
                import json
                projects = json.load(f).get('data')
                for project in projects:
                    image = project.get('image')
                    try:
                        image, tag = image.split(':')
                    except ValueError:
                        tag = 'latest'
                    try:
                        prefix, image = image.rsplit('/', 1)
                    except ValueError:
                        prefix = ''
                    project.pop('image')
                    desc = project.get('description', '')
                    index = desc.find('（')
                    if index != -1:
                        desc = desc[:index]
                    project['desc'] = desc
                    project['name'] = image
                    project['tag'] = tag
                    project['prefix'] = prefix
                Config.PROJECTS_DATA = projects
        return Config.PROJECTS_DATA
