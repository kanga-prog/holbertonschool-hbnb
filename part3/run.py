#!/usr/bin/python3
from app import create_app, db
from flask_cors import CORS

app = create_app()
CORS(app)
app.config['PREFERRED_URL_SCHEME'] = 'http'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
