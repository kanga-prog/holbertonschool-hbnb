# /app/models/amenity.py

from .base_model import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)  # Clé primaire
    name = db.Column(db.String(100), nullable=False)  # Nom de l'aménagement

    def __init__(self, name, description):
        super().__init__()
        self.name = name  # Nom de l'équipement
        self.description = description
        if len(self.name) > 50:
            raise ValueError("The amenity name must be fewer than 50 characters.")
        if not self.name:
            raise ValueError("The amenity must have a name") 
        if not self.description:
            raise ValueError("Please give a description")