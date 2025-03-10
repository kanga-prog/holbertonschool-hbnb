# HBnB Application

## Structure du projet

- `app/` : Code principal de l'application
  - `api/` : Routes API organisées par version
  - `models/` : Modèles de données (user, place, review, amenity)
  - `services/` : Logique de service, y compris la façade
  - `persistence/` : Gestion du stockage (référentiel en mémoire)

## Installation

1. Clonez le projet.
2. Installez les dépendances avec :
   ```bash
   pip install -r requirements.txt
