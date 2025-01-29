from flask import request, jsonify
from flask_cors import CORS
from app import db, mail
from app.models import Teacher, Test
from werkzeug.security import generate_password_hash
from flask_mail import Message
import logging
from itsdangerous import URLSafeTimedSerializer
from flask import url_for

import os
secret_key = os.urandom(24)  


s = URLSafeTimedSerializer(secret_key)




def generate_activation_link(email):
    token = s.dumps(email, salt='email-activation')
    return f'http://localhost:4200/activate-account/{token}'


def register_routes(app):
    

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)  # ✅ Autoriser CORS pour toutes les API

  # ✅ Active CORS globalement

    @app.before_request
    def before_request():
        """ Gérer les requêtes OPTIONS pour CORS """
        if request.method == "OPTIONS":
            response = jsonify({"message": "CORS Preflight OK"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            return response, 200  # ✅ Répond avec un HTTP 200 OK

    @app.route('/api/tests/create', methods=['POST', 'OPTIONS'])

    @app.route('/api/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            print("Données reçues:", data)

            nom = data.get('firstName')
            prenom = data.get('lastName')
            email = data.get('email')
            mot_de_passe = data.get('password')

            if not nom or not prenom or not email or not mot_de_passe:
                return jsonify({"status": "error", "message": "Tous les champs sont obligatoires"}), 400

          
            teacher_exists = Teacher.query.filter_by(email=email).first()
            if teacher_exists:
                return jsonify({"status": "error", "message": "L'email est déjà utilisé"}), 400

         
            hashed_password = generate_password_hash(mot_de_passe, method='pbkdf2:sha256')

           
            new_teacher = Teacher(nom=nom, prenom=prenom, email=email, mot_de_passe=hashed_password, is_active=False)

         
            db.session.add(new_teacher)
            db.session.commit()

          
            activation_link = generate_activation_link(email)

            
            msg = Message(
                subject="Confirmation de votre compte",
                sender='elalamisafa2003@gmail.com',
                recipients=[email]
            )
            msg.body = f"Bonjour {prenom} {nom},\n\nVotre compte a été créé avec succès. Cliquez sur le lien suivant pour activer votre compte :\n{activation_link}"

          
            mail.send(msg)

          
            return jsonify({"status": "success", "emailSent": True, "message": "Enseignant enregistré avec succès"}), 201

        except Exception as e:
            print("Erreur survenue:", e)
            logging.error(f"Erreur dans la route /api/register: {e}")

            return jsonify({"status": "error", "message": f"Erreur interne du serveur: {str(e)}"}), 500
        
    
    @app.route('/api/tests', methods=['POST'])
    def create_test():
        if request.method == "OPTIONS":
            return jsonify({"message": "CORS preflight OK"}), 200  # ✅ Répond aux requêtes préflight CORS

        data = request.json
        if not data or not all(k in data for k in ("Titre", "Type", "Date", "groupe")):
            return jsonify({"error": "Données manquantes"}), 400

        new_test = Test(
            Titre=data["Titre"],
            Type=data["Type"],
            Date=data["Date"],
            groupe=data["groupe"]
        )
        db.session.add(new_test)
        db.session.commit()
        return jsonify({"message": "Test ajouté avec succès"}), 201

    @app.route('/api/tests', methods=['GET'])
    def get_tests():
        """ Récupérer tous les tests existants """
        tests = Test.query.all()
        return jsonify([{"ID_date_groupe": test.ID_date_groupe, "Titre": test.Titre, "Type": test.Type, "Date": test.Date} for test in tests])

    @app.route('/api/tests/<int:test_id>', methods=['DELETE'])
    def delete_test(test_id):
        """ Supprimer un test par son ID """
        test = Test.query.get_or_404(test_id)
        db.session.delete(test)
        db.session.commit()
        return jsonify({"message": "Test supprimé"}), 200





from itsdangerous import BadSignature, SignatureExpired
def activate(app):
    @app.route('/api/activate/<token>', methods=['GET'])
    def activate_account(token):
        try:
          
            email = s.loads(token, salt='email-activation', max_age=3600)  
            
           
            teacher = Teacher.query.filter_by(email=email).first()
            if not teacher:
                return jsonify({"status": "error", "message": "Utilisateur non trouvé"}), 404

           
            teacher.is_active = True
            db.session.commit()

            return jsonify({"status": "success", "message": "Compte activé avec succès"}), 200

        except SignatureExpired:
            return jsonify({"status": "error", "message": "Le lien d'activation a expiré"}), 400
        except BadSignature:
            return jsonify({"status": "error", "message": "Jeton d'activation invalide"}), 400
        

import re

  # if not re.match(r"^[a-zA-Z0-9._%+-]+@etu\.eilco\.univ-littoral\.fr$", email):
        #     return jsonify({"status": "error", "message": "Email académique invalide"}), 400
def login_user(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "error", "message": "Email et mot de passe requis"}), 400

        teacher = Teacher.query.filter_by(email=email).first()
        
  
        if not teacher:
            return jsonify({"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

        if not teacher.check_password(password): 
            return jsonify({"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

       
        if not teacher.is_active:
            return jsonify({"status": "success", "accountActivated": False}), 200

       
        return jsonify({"status": "success", "accountActivated": True}), 200

