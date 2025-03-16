# /app/models/user.py

import re  # Ajoutez l'importation du module re

from .base_model import BaseModel
from flask_bcrypt import Bcrypt
from app import db
bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'  # Name of the table in the database

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Ensure unique email
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations : one user can have many places and many reviews
    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()  # Appel du constructeur de BaseModel pour générer l'id et les timestamps
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.validate_email()
        self.hash_password()

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
    
    def hash_password(self):
        """Hache le mot de passe avant de le stocker."""
        self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au mot de passe haché."""
        return bcrypt.check_password_hash(self.password, password)
