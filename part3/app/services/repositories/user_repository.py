
from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def add(self, user):
        """Ajouter un nouvel utilisateur dans la base de données"""
        db.session.add(user)
        db.session.commit()

    def get(self, user_id):
        """Récupérer un utilisateur par son ID"""
        return self.model.query.get(user_id)

    def get_user_by_email(self, email):
        """Récupérer un utilisateur par son email"""
        return self.model.query.filter_by(email=email).first()

    def update(self, user_id, updated_data):
        """Mettre à jour un utilisateur"""
        user = self.get(user_id)
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user

    def delete(self, user_id):
        """Supprimer un utilisateur de la base de données"""
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
    
    def get_all(self):
        """Récupérer tous les utilisateurs"""
        return self.model.query.all()
