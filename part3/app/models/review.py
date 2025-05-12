# /app/models/review.py
from .base_model import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(255), nullable=False)  # Texte de l'avis
    rating = db.Column(db.Integer, nullable=False)  # Note

    #relations
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    
    
    def __init__(self, text, rating, place_id = None, user_id = None):
        super().__init__()
        self.text = text  # Texte de la revue
        self.rating = rating  # Note de la revue (par exemple, de 1 à 5)
        self.place_id = place_id  # Lieu associé à la revue (instance de Place)
        self.user_id = user_id  # Utilisateur ayant écrit la revue (instance de User)
        self.validate_review()

    def validate_review(self):
        """Valide les attributs de la revue"""
        if not (1 <= self.rating <= 5):
            raise ValueError("The rating must be between 1 and 5")
        if not self.text:
            raise ValueError("Review text cannot be empty.")

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
            # Ajoutez d'autres champs si nécessaire
        }