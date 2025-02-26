# /app/models/base_model.py

import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Générer un identifiant unique (UUID)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Mets à jour le timestamp de 'updated_at' lorsque l'objet est modifié"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Mets à jour les attributs de l'objet à partir d'un dictionnaire de données"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Mettre à jour le timestamp 'updated_at'

