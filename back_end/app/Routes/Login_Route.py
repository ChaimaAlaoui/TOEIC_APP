
# ------------------------------------------------------
# DÉPENDANCES NÉCESSAIRES
# ------------------------------------------------------

from flask import jsonify, request
from app.Models.Prof import Prof
from flask import jsonify, request
from app.Models.Prof import Prof

# ------------------------------------------------------
# Fonction de login pour les enseignants
# ------------------------------------------------------
def login_user(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        # Récupérer les données envoyées dans le corps de la requête
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Vérifier que l'email et le mot de passe sont présents
        if not email or not password:
            return jsonify({"status": "error", "message": "Email et mot de passe requis"}), 400

        # Chercher l'utilisateur dans la base de données
        teacher = Prof.query.filter_by(email=email).first()
        
        # Si l'utilisateur n'existe pas ou que le mot de passe est incorrect
        if not teacher or not teacher.check_password(password): 
            return jsonify({"status": "error", "message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

        # Si le compte n'est pas encore activé
        if not teacher.is_active:
            return jsonify({"status": "success", "accountActivated": False}), 200

        # Connexion réussie avec compte activé
        return jsonify({"status": "success", "accountActivated": True}), 200

