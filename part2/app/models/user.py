# /app/models/user.py

import re  # Ajoutez l'importation du module re

from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()  # Appel du constructeur de BaseModel pour générer l'id et les timestamps
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_email()

    def validate_email(self):
        """Valide l'email"""
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, self.email):
            raise ValueError("L'email est invalide.")
