from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_bcrypt import Bcrypt
from config import configurations

bcrypt = Bcrypt()


def create_app(config_class="development"):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    # Charger la configuration appropriée selon l'environnement (développement ou production)
    app.config.from_object(configurations.get(config_class))

    # Initialiser les extensions
    bcrypt.init_app(app)

    # save all the namespaces
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path= '/api/v1/reviews')

    bcrypt.init_app(app) 
    return app
