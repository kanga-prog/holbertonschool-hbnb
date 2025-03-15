# repositories/review_repository.py
from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def add(self, review):
        """Ajouter un avis"""
        db.session.add(review)
        db.session.commit()

    def get(self, review_id):
        """Récupérer un avis par son ID"""
        return self.model.query.get(review_id)

    def update(self, review_id, updated_data):
        """Mettre à jour un avis"""
        review = self.get(review_id)
        if review:
            for key, value in updated_data.items():
                setattr(review, key, value)
            db.session.commit()
        return review

    def delete(self, review_id):
        """Supprimer un avis"""
        review = self.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
        return review

    def get_all(self):
        """Récupérer tous les avis"""
        return self.model.query.all()
