🏠 HolbertonBnB (Projet HBnB)
📚 Description
HolbertonBnB est un projet full-stack inspiré d'Airbnb, développé dans le cadre du programme de la Holberton School. Il met en œuvre une architecture modulaire avec séparation des couches (présentation, logique métier, persistance), une API RESTful sécurisée via JWT, et une interface web interactive construite avec HTML, CSS et JavaScript.

Le projet est divisé en plusieurs parties, chacune avec ses objectifs pédagogiques, allant de la gestion des entités métiers à l’implémentation d’une interface web complète.

🗂️ Structure du Projet
graphql

Photocopieuse

Modificateur
holbertonschool-hbnb/
├── part1/                  # Entités métiers (User, Place, Review, Amenity)
├── part2/                  # API REST avec Flask + Flask-RESTx
├── part3/                  # Authentification avec JWT
├── part4/                  # Interface web (HTML, CSS, JS)
├── models/                 # Représentation des entités et persistance
├── services/               # Logique métier (façade, gestion des opérations)
├── tests/                  # Tests unitaires
├── static/                 # Fichiers CSS, JS, images
├── templates/              # Fichiers HTML (login.html, index.html, place.html, etc.)
└── app.py                  # Application Flask principale (factory pattern)
✅ Fonctionnalités
🔧 Back-End
Architecture MVC avec séparation claire des responsabilités

,Représentation des entités User, Place, Review, Amenity

API RESTful complète avec Flask-RESTx

Authentification sécurisée avec JWT (Flask-JWT-Extended)

Persistance en mémoire ou via SQLite + SQLAlchemy (facultatif selon la partie)

CORS configuré pour interaction avec le front-end

🌐 Front-End
Interface utilisateur responsive avec HTML5, CSS3, et JavaScript ES6

Authentification via formulaire et stockage de token JWT dans les cookies

Affichage dynamique des places et détails via Fetch API

Soumission de reviews avec formulaire accessible uniquement aux utilisateurs connectés

Filtrage client par prix sur la liste des places

🚀 Installation & Lancement
🔗 Cloner le projet
frapper

Photocopieuse

Modificateur
git clone https://github.com/ton-utilisateur/holbertonschool-hbnb.git
cd holbertonschool-hbnb
⚙️ Installer les dépendances Python
frapper

Photocopieuse

Modificateur
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
▶️ Lancer l'application Flask
frapper

Photocopieuse

Modificateur
cd part4  # ou à la racine selon structure
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
🌍 Accéder à l'application
L'extrémité avant:http://localhost:5000/index.html

Back-end (API) :http://localhost:5000/api/...

🔑 Authentification
Le login est géré par un formulaire HTML.

En cas de succès, un JWT est généré par l’API (/api/login) et stocké dans un cookie.

Les endpoints protégés nécessitent ce token dans l'en-tête Authorization.

🧪 Tests
✅ Tester l'API
Test via Swagger ou cURL :

frapper

Photocopieuse

Modificateur
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"email":"user@test.com","password":"secret"}'
✅ Tester le Frontend
Naviguer sur index.html, place.html, etc.

Tester le login, la redirection, le filtrage par prix, et l’ajout de reviews.

📁 Pages Web
index.html : liste des places avec filtrage par prix

login.html : formulaire de connexion

register.html : inscription utilisateur

place.html : vue détaillée d’une place avec reviews

add_review.html : formulaire de review (optionnel si inline)

🛠 Technologies Utilisées
Python 3

Flacon , Flacon-RESTx , Flacon-JWT-Extended

HTML5 , CSS3 , JavaScript ES6

Récupérer l'API , Cookies

SQLite / SQLAlchemy (optionnel pour persistance réelle)

JWT pour sécuriser l’accès

📚 Ressources Utilisées
Documents Web MDN

Documentation Documentation Flask

Guide (Guide JWT (Auth0)

Validateur W3C

📸 Aperçu
Voici un aperçu du rendu attendu :

Capture d'écran des détails
