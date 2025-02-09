from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Charger la configuration
    app.config.from_object('app.config.Config')

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurer CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200", "allow_headers": ["Content-Type"], "methods": ["GET", "POST", "OPTIONS","PUT","DELETE"]}})

    # Importer les modèles après l'initialisation
    from app import models

    # Enregistrer les routes
    from app.routes import init_routes
    init_routes(app)

    return app