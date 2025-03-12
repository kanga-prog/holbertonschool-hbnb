# /app/models/user.py
from flask_bcrypt import Bcrypt
import re  # Ajoutez l'importation du module re
from .base_model import BaseModel

bcrypt = Bcrypt() 

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, place_list=[], reviews_posted = [], is_admin=False):
        super().__init__()  # Appel du constructeur de BaseModel pour générer l'id et les timestamps
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.place_list = place_list
        self.password = password
        self.reviews_posted = reviews_posted
        self.validate_email()


    def validate_email(self):
        """Valide l'email"""
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, self.email):
            raise ValueError("Invalid email.")
        if not self.first_name:
            raise ValueError("Please enter your first name")
        if not self.last_name:
            raise ValueError("Please enter your last name")
        if not self.password:
            raise ValueError("Please enter your password")
        
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)