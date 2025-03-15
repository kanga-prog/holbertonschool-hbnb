# repositories/place_repository.py
from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def add(self, place):
        """Ajouter un lieu"""
        db.session.add(place)
        db.session.commit()

    def get(self, place_id):
        """Récupérer un lieu par son ID"""
        return self.model.query.get(place_id)

    def update(self, place_id, updated_data):
        """Mettre à jour un lieu"""
        place = self.get(place_id)
        if place:
            for key, value in updated_data.items():
                setattr(place, key, value)
            db.session.commit()
        return place

    def delete(self, place_id):
        """Supprimer un lieu"""
        place = self.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
        return place

    def get_all(self):
        """Récupérer tous les lieux"""
        return self.model.query.all()
