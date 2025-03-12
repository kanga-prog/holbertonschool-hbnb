from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import configurations
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns


def create_app(config_class=config.developmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    # Charger la configuration appropriée selon l'environnement (développement ou production)
    app.config.from_object(configurations.get(config_class))

    bcrypt = Bcrypt()
    jwt = JWTManager()

    # Initialiser les extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # save all the namespaces
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path= '/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    bcrypt.init_app(app) 
    return app