# repositories/amenity_repository.py
from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def add(self, amenity):
        """Ajouter un aménagement"""
        db.session.add(amenity)
        db.session.commit()

    def get(self, amenity_id):
        """Récupérer un aménagement par son ID"""
        return self.model.query.get(amenity_id)

    def update(self, amenity_id, updated_data):
        """Mettre à jour un aménagement"""
        amenity = self.get(amenity_id)
        if amenity:
            for key, value in updated_data.items():
                setattr(amenity, key, value)
            db.session.commit()
        return amenity

    def delete(self, amenity_id):
        """Supprimer un aménagement"""
        amenity = self.get(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
        return amenity

    def get_all(self):
        """Récupérer tous les aménagements"""
        return self.model.query.all()
