# /app/models/amenity.py

from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Nom de l'équipement
        if len(self.name) > 50:
            raise ValueError("Le nom de l'équipement ne doit pas dépasser 50 caractères.")
