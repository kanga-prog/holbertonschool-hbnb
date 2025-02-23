# /app/models/review.py

from datetime import datetime
import uuid
from .base_model import BaseModel
from .user import User  # Importation de User
from .place import Place  # Importation de Place

class Review(BaseModel):
    def __init__(self, text, rating, place: Place, user: User):
        super().__init__()
        
        self.id = str(uuid.uuid4())  # Identifiant unique de la revue
        self.text = text  # Texte de la revue
        self.rating = rating  # Note de la revue (par exemple, de 1 à 5)
        self.place = place  # Lieu associé à la revue (instance de Place)
        self.user = user  # Utilisateur ayant écrit la revue (instance de User)
        self.created_at = datetime.now()  # Horodatage de la création de la revue
        
        self.validate_review()

    def validate_review(self):
        """Valide les attributs de la revue"""
        if not (1 <= self.rating <= 5):
            raise ValueError("La note doit être comprise entre 1 et 5.")
        if not isinstance(self.place, Place):
            raise ValueError("Le lieu doit être une instance valide de la classe Place.")
        if not isinstance(self.user, User):
            raise ValueError("L'utilisateur doit être une instance valide de la classe User.")
