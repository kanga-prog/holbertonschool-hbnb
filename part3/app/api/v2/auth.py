from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from datetime import timedelta

api = Namespace('auth', description='Opérations d\'authentification')

# Modèle pour la validation des entrées
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload  # Récupérer l'email et le mot de passe du corps de la requête
        
        # Étape 1 : Récupérer l'utilisateur en fonction de l'email fourni
        user = facade.get_user_by_email(credentials['email'])
        
        # Étape 2 : Vérifier si l'utilisateur existe et si le mot de passe est correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        #check if the user is an admin.
        if user.is_admin:
            expires_delta = timedelta(days=365) # The token is valid for one year
        else:
            expires_delta = timedelta(days=1) # The token is valid for one day.
        
        # Étape 3 : Créer un token JWT avec l'ID de l'utilisateur et le flag is_admin
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin}, expires_delta = expires_delta)
        
        # Étape 4 : Retourner le token JWT au client
        return {'access_token': access_token}, 200

@api.route('/admin_token')
class GenerateAdminToken(Resource):
    def get(self):
        admin_token = create_access_token(identity="admin", expires_delta=timedelta(days=365),
                                    additional_claims={"is_admin": True})
        return ({'admin_token': admin_token})