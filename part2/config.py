import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

from models import Place, User
Kanga=User('Brice', 'Kanga', 'brice@gmail.com', admin=True)
kangaplace = Place(title='ma_maison', price=100, latitude=60, longitude=43, owner=Kanga, )