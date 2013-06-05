class Settings(object):
    DEBUG = True
    SECRET_KEY = '}\xa8\xcd!\xcf\x00\\\xe7b\xec\x8a\\\xfdf\xd3J #\x880HUH\xb7'
    MONGO_DBNAME = 'aniseasons-dev'
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    MEDIA_PATH = os.path.join(PROJECT_PATH, 'media')
    UPLOAD_PATH = os.path.join(PROJECT_PATH, 'media/imgs/')
    STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
