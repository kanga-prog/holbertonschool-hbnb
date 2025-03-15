from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.api.v2.users import api as users_ns
from app.api.v2.amenities import api as amenities_ns
from app.api.v2.places import api as places_ns
from app.api.v2.reviews import api as reviews_ns
from flask_bcrypt import Bcrypt
from config import configurations
from app.api.v2.auth import api as auth_ns
from app.api.v2.protected import api as protected_ns
from app.api.v2.admins import api as admins_ns
import os

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="development"):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    # Charger la configuration appropriée selon l'environnement (développement ou production)
    # Création de l'API avec la documentation Swagger à l'endpoint /docs
    app.config.from_object(configurations.get(config_class))
    app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

    # save all the namespaces
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected') 

    if config_class == "development":
        api.add_namespace(admins_ns, path='/api/v1/admins')

# Initialiser les extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    return app
