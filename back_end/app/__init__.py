from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail


# from app.Models.Prof import Prof
# from app.Models.Teacher import Test, ReponseJuste


# Initialisation des extensions globales
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Import models here
    from app.Models.Prof import Prof
    from app.Models.Teacher import Test, ReponseJuste

   
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app) 

   
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200", "allow_headers": ["Content-Type"], "methods": ["GET", "POST", "OPTIONS"]}})

   
    # Importer et enregistrer les routes automatiquement
    from app.Routes.Login_Routes2 import register_routes, activate, login_user
    register_routes(app)
    activate(app)
    login_user(app)
   

    return app
