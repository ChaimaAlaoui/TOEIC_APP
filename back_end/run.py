from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from app import db
from app import create_app
from app.Routes.Login_Routes import register_routes
from app.Routes.Login_Routes import activate
from app.Routes.Login_Routes import login_user

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
