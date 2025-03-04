# /app/models/place.py

from datetime import datetime
import uuid
from .user import User  # Importation de User
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title  # Le titre du lieu (obligatoire, longueur maximale de 100 caractères)
        self.description = description  # La description est facultative
        self.price = price  # Le prix doit être positif
        self.latitude = latitude  # Latitude dans la plage (-90 <= latitude <= 90)
        self.longitude = longitude  # Longitude dans la plage (-180 <= longitude <= 180)
        self.owner = owner  # L'utilisateur qui est le propriétaire du lieu (instance de User)
        self.reviews = []  # Liste des reviews pour ce lieu
        self.amenities = []  # Liste des équipements pour ce lieu
        
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
        if not isinstance(self.owner, User):
            raise ValueError("Invalid user.")
        
    def add_review(self, review):
        """Ajoute une revue à la place"""
        self.reviews.append(review)
        self.updated_at = datetime.now()  # Mise à jour du timestamp lors de l'ajout d'une revue

    def add_amenity(self, amenity):
        """Ajoute un équipement au lieu"""
        self.amenities.append(amenity)
        self.updated_at = datetime.now()  # Mise à jour du timestamp lors de l'ajout d'un équipement
