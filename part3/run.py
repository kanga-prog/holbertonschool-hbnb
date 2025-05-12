#!/usr/bin/python3
from app import create_app, db
from flask_cors import CORS

app = create_app()
# Configuration CORS ultra-permissive (DEV ONLY)
CORS(app, resources={r"/api/*": {
            "origins": "*",  # Autorise toutes les origines
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
})

app.config['PREFERRED_URL_SCHEME'] = 'http'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
