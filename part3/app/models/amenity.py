# /app/models/amenity.py

from .base_model import BaseModel
from app import db
from app.models.place import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)  # Nom de l'aménagement
    description = db.Column(db.String(500), nullable=True)

    associated_places = db.relationship('Place', secondary=place_amenity, backref='amenities_associated')

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
