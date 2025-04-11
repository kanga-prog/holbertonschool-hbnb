from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Liste des utilisateurs avec leurs mots de passe hachés
users_db = {}

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # 🔐 Change this in prod
CORS(app)
jwt = JWTManager(app)

# Route pour créer un utilisateur (inscription)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Vérification si l'utilisateur existe déjà
    if email in users_db:
        return jsonify({'msg': 'User already exists'}), 400

    # Hash du mot de passe avant de le stocker
    hashed_password = generate_password_hash(password)
    users_db[email] = hashed_password

    return jsonify({'msg': 'User created successfully'}), 201

# Route pour la connexion (login)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Vérification des identifiants
    if email not in users_db or not check_password_hash(users_db[email], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # Création du token JWT
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    app.run(debug=True)
