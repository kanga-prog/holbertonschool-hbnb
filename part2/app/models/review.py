# /app/models/review.py
from .base_model import BaseModel
from .user import User  # Importation de User
from .place import Place  # Importation de Place

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text  # Texte de la revue
        self.rating = rating  # Note de la revue (par exemple, de 1 à 5)
        self.place = place  # Lieu associé à la revue (instance de Place)
        self.user = user  # Utilisateur ayant écrit la revue (instance de User)
        self.validate_review()
        self.user.reviews_posted.append(self.id)
        self.place.add_review(self.id)

    def validate_review(self):
        """Valide les attributs de la revue"""
        if not (1 <= self.rating <= 5):
            raise ValueError("The rating must be between 1 and 5")
        if not isinstance(self.place, Place):
            raise ValueError("Invalid place.")
        if not isinstance(self.user, User):
            raise ValueError("Invalid User.")
        if not self.text:
            raise ValueError("Review text cannot be empty.")