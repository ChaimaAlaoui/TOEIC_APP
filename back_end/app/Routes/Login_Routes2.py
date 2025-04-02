from datetime import datetime
from flask import request, jsonify
from flask_cors import cross_origin
from app import db, mail
from app.Models.Prof import Prof
from werkzeug.security import generate_password_hash
from flask_mail import Message
import logging
from itsdangerous import URLSafeTimedSerializer
from flask import url_for

import os

from app.Models.myModels import Etudiant, Groupe, Promotion, ReponseProf, Site, Test,test_groupe,test_promotion

secret_key = os.urandom(24)  


s = URLSafeTimedSerializer(secret_key)

def generate_activation_link(email):
    token = s.dumps(email, salt='email-activation')
    return f'http://localhost:4200/activate-account/{token}'


def register_routes(app):
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

          
            teacher_exists = Prof.query.filter_by(email=email).first()
            if teacher_exists:
                return jsonify({"status": "error", "message": "L'email est déjà utilisé"}), 400

         
            hashed_password = generate_password_hash(mot_de_passe, method='pbkdf2:sha256')

           
            new_teacher = Prof(nom=nom, prenom=prenom, email=email, mot_de_passe=hashed_password, is_active=False)

         
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





from itsdangerous import BadSignature, SignatureExpired
def activate(app):
    @app.route('/api/activate/<token>', methods=['GET'])
    def activate_account(token):
        try:
          
            email = s.loads(token, salt='email-activation', max_age=3600)  
            
           
            teacher = Prof.query.filter_by(email=email).first()
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

        teacher = Prof.query.filter_by(email=email).first()
        
  
        if not teacher:
            return jsonify({"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

        if not teacher.check_password(password): 
            return jsonify({"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

       
        if not teacher.is_active:
            return jsonify({"status": "success", "accountActivated": False}), 200

       
        return jsonify({"status": "success", "accountActivated": True}), 200

# 
# //ad test
from flask import Flask, request, jsonify
from datetime import datetime
from app.Models.myModels import Test, Groupe, ReponseProf
def add_test(app):
    @app.route('/api/tests', methods=['POST', 'OPTIONS'])
    @cross_origin(origin='http://localhost:4200', headers=['Content-Type'])
    def ajouter_test():
        """Créer un nouveau test avec ses réponses, groupes et promotions associées"""

        if request.method == "OPTIONS":
            response = jsonify({'message': 'CORS preflight request successful'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            return response, 200  

        try:
            data = request.json
            if not data:
                return jsonify({'error': 'Aucune donnée reçue'}), 400

            test_data = data.get('test_data', {})
            test_responses = data.get('test_responses', [])
            selected_groups = data.get('selected_groups', [])  # Liste des IDs des groupes
            site_id = test_data.get('site')


            # Vérification des champs obligatoires
            if not test_data.get('nom'):
                return jsonify({'error': 'Le nom du test est requis'}), 400
            if not test_data.get('date'):
                return jsonify({'error': 'La date du test est requise'}), 400
            if not selected_groups:
                return jsonify({'error': 'Au moins un groupe doit être sélectionné'}), 400
            if not test_responses:
                return jsonify({'error': 'Les réponses du test sont requises'}), 400
            if not site_id:
                return jsonify({'error': 'Le site est requis'}), 400

            # Création du test
            test = Test(
                nom=test_data['nom'],
                description=test_data.get('description', ''),  
                date=datetime.strptime(test_data['date'], '%Y-%m-%d'),
                site_id=site_id  # Vérifie que ce champ existe bien dans le modèle Test
            )

            db.session.add(test)
            
            added_promotions = set()  # Pour éviter les doublons
            for groupe_id in selected_groups:
                groupe = Groupe.query.get(groupe_id)
                if groupe:
                    # Utiliser UNIQUEMENT cette méthode (pas d'insert explicite)
                    test.groupes.append(groupe)
                    
                    # Ajouter la promotion si pas déjà ajoutée
                    if groupe.promotion_id and groupe.promotion_id not in added_promotions:
                        promotion = Promotion.query.get(groupe.promotion_id)
                        if promotion:
                            test.promotions.append(promotion)
                            added_promotions.add(promotion.id)

            # Important: faire un flush avant d'ajouter les réponses
            db.session.flush()

            # Ajout des réponses
            for response in test_responses:
                if 'num_question' in response and 'choix' in response:
                    reponse_prof = ReponseProf(
                        num_question=response['num_question'],
                        choix=response['choix'],
                        test_id=test.id
                    )
                    db.session.add(reponse_prof)
                else:
                    return jsonify({'error': 'Données de réponse incomplètes'}), 400

            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Test créé avec succès',
                'test_id': test.id
            })

        except Exception as e:
            db.session.rollback()
            print(f"Erreur backend: {e}")  
            return jsonify({'error': str(e)}), 500
        
def trouver_sites(app):
    @app.route('/api/sitesachraf', methods=['GET'])
    def trouver_sitess():
        # Récupérer tous les sites depuis la base de données
        sites = Site.query.all()  # Assurez-vous que Site est une table dans votre base de données
        result = [{"id": site.id, "nom": site.nom} for site in sites]  # Adapté selon les attributs de votre modèle
        return jsonify(result)
   
def trouvergroups(app):
    @app.route('/api/groupesachraf', methods=['GET'])
    def get_groupes_achraf():
        site_id = request.args.get('site_id', type=int)

        # Debugging
        if site_id is None:
            print("⚠️ Avertissement : site_id est None ! Vérifiez la requête GET.")
            return jsonify({"error": "Le paramètre site_id est requis."}), 400

        print(f"🔍 Site ID reçu: {site_id}")

        # Vérifier si le site existe dans la base de données
        site = Site.query.get(site_id)
        if not site:
            print("❌ Aucun site trouvé avec cet ID")
            return jsonify([])  # Retourner une liste vide si le site n'existe pas

        # Récupérer uniquement les groupes du site sélectionné
        groupes = Groupe.query.filter_by(site_id=site_id).all()
        print(f"📌 Groupes trouvés ({len(groupes)}): {groupes}")

        result = []
        for groupe in groupes:
            nombre_etudiants = db.session.query(Etudiant).filter(Etudiant.groupe_id == groupe.id).count()
            nombre_tests = db.session.query(Test).join(test_groupe).filter(test_groupe.c.groupe_id == groupe.id).count()

            result.append({
                'id_groupe': groupe.id,
                'nom': groupe.nom,
                'promotion': groupe.promotion.nom if groupe.promotion else None,
                'site': groupe.site.nom if groupe.site else None,
                'semestre': groupe.semestre.nom if groupe.semestre else None,
                'nombre_tests': nombre_tests,
                'nombre_etudiants': nombre_etudiants
            })

        print("✅ API Response:", result)
        return jsonify(result)

