# /app/models/amenity.py

from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=None):
        super().__init__()
        self.name = name  # Nom de l'équipement
        self.description = description
        if len(self.name) > 50:
            raise ValueError("The amenity name must be fewer than 50 characters.")
        if not self.name:
            raise ValueError("The amenity must have a name") 
        if not description:
            raise ValueError("Please give a description")