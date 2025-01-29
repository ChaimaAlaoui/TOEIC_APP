from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from app import db
from app.models import Teacher
from app import create_app
from app.routes import register_routes
from app.routes import activate
from app.routes import login_user

app = create_app()
register_routes(app)
activate(app)
login_user(app)


from app import db, create_app

app = create_app()


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

