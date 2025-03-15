# /app/models/place.py

from datetime import datetime
from .user import User  # Importation de User
from .base_model import BaseModel
from app import db

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)  # Clé primaire
    title = db.Column(db.String(100), nullable=False)  # Titre du lieu
    description = db.Column(db.String(255), nullable=False)  # Description du lieu
    price = db.Column(db.Float, nullable=False)  # Prix par nuit
    latitude = db.Column(db.Float, nullable=False)  # Latitude
    longitude = db.Column(db.Float, nullable=False)  # Longitude

    def __init__(self, title, price, latitude, longitude, owner_id = None, reviews=[], amenities=[], description=None):
        super().__init__()
        self.title = title  # Le titre du lieu (obligatoire, longueur maximale de 100 caractères)
        self.description = description  # La description est facultative
        self.price = price  # Le prix doit être positif
        self.latitude = latitude  # Latitude dans la plage (-90 <= latitude <= 90)
        self.longitude = longitude  # Longitude dans la plage (-180 <= longitude <= 180)
        self.owner_id = owner_id  # L'utilisateur qui est le propriétaire du lieu (instance de User)
        self.reviews = reviews # Liste des reviews pour ce lieu
        self.amenities = amenities  # Liste des équipements pour ce lieu
        
        # Validation des attributs du lieu
        self.validate_place()
    
    def validate_place(self):
        """Valide les attributs du lieu selon les consignes"""
        if not self.title:
            raise ValueError("The place must have a title")
        if len(self.title) > 100:
            raise ValueError("The title must be fewer than 100 characters.")
        if self.price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be beeween -180 and 180.")
        
    def add_review(self, review):
        """Ajoute une revue à la place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajoute un équipement au lieu"""
        self.amenities.append(amenity)
