from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('Protected', description='A protected endpoint that requires a valid JWT token')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()  # Ce décorateur vérifie que le token JWT est valide
    def get(self):
        """Un endpoint protégé qui nécessite un token JWT valide"""
        current_user_identity = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du token
        claims = get_jwt()  # Récupérer les autres claims comme is_admin

        # Retourne un message et les informations de l'utilisateur
        return {
            'message': f'Hello, user {current_user_identity}',
            'is_admin': claims.get("is_admin", False)  # Si l'utilisateur est admin, récupérer cette info
        }, 200

