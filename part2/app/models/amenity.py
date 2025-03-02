# /app/models/amenity.py

from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Nom de l'équipement
        if len(self.name) > 50:
            raise ValueError("The amenity name must be fewer than 50 characters.")