# /app/models/place.py

from datetime import datetime
import uuid
from .user import User  # Importation de User
from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner: User, description=None):
        super().__init__()
        
        self.id = str(uuid.uuid4())  # Identifiant unique généré automatiquement
        self.title = title  # Le titre du lieu (obligatoire, longueur maximale de 100 caractères)
        self.description = description  # La description est facultative
        self.price = price  # Le prix doit être positif
        self.latitude = latitude  # Latitude dans la plage (-90 <= latitude <= 90)
        self.longitude = longitude  # Longitude dans la plage (-180 <= longitude <= 180)
        self.owner = owner  # L'utilisateur qui est le propriétaire du lieu (instance de User)
        self.created_at = datetime.now()  # Horodatage de la création du lieu
        self.updated_at = datetime.now()  # Horodatage de la mise à jour du lieu
        self.reviews = []  # Liste des reviews pour ce lieu
        self.amenities = []  # Liste des équipements pour ce lieu
        
        # Validation des attributs du lieu
        self.validate_place()

    def validate_place(self):
        """Valide les attributs du lieu selon les consignes"""
        if not self.title or len(self.title) > 100:
            raise ValueError("Le titre du lieu doit être une chaîne non vide de moins de 100 caractères.")
        if self.price <= 0:
            raise ValueError("Le prix doit être positif.")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("La latitude doit être comprise entre -90 et 90.")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("La longitude doit être comprise entre -180 et 180.")
        if not isinstance(self.owner, User):
            raise ValueError("Le propriétaire doit être une instance valide de la classe User.")

    def add_review(self, review):
        """Ajoute une revue à la place"""
        self.reviews.append(review)
        self.updated_at = datetime.now()  # Mise à jour du timestamp lors de l'ajout d'une revue

    def add_amenity(self, amenity):
        """Ajoute un équipement au lieu"""
        self.amenities.append(amenity)
        self.updated_at = datetime.now()  # Mise à jour du timestamp lors de l'ajout d'un équipement
