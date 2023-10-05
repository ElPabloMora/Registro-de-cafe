import os


UPLOAD_DATA = os.path.abspath("./data/")
DB_URI = 'TBD'

class config(object):
    DEBUG = False
    SECRET_KEY = '60e08d27fb0b5f39cd336135af7a1b29bada23452f09ae0949'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_DATA = UPLOAD_DATA
    
    
class productionConfig(config):
    SECRET_KEY = os.getenv
    SQLALCHEMY_DATABASE_URI = DB_URI
    
    
class developmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath('./database.db')