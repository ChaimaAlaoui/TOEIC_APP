from flask import Flask, request, jsonify
from app import db
import pandas as pd
from io import BytesIO
from app.models import Etudiant, Groupe, Promotion, Site

def init_routes(app):
    @app.route('/api/etudiants', methods=['GET'])
    def getEtudiants():
        app.logger.info("Route /api/etudiants a été atteinte.")
        try:
            etudiants = Etudiant.query.all()
            if not etudiants:
                app.logger.info("Aucun étudiant trouvé.")
                return jsonify({'message': 'No students found'}), 404
            return jsonify([etudiant.to_dict() for etudiant in etudiants])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching students'}), 500

    @app.route('/api/etudiants', methods=['POST'])
    def addStudent():
        try:
            data = request.get_json()
            promotion = Promotion.query.get(data['promotion_id'])
            groupe = Groupe.query.get(data['groupe_id'])
            site = Site.query.get(data['site_id'])
            if not promotion or not groupe or not site:
                return jsonify({'error': 'Promotion, groupe ou site non trouvé'}), 400
            new_student = Etudiant(
                nom=data['nom'],
                prenom=data['prenom'],
                promotion_id=data['promotion_id'],
                groupe_id=data['groupe_id'],
                site_id=data['site_id'],
                specialite=data['specialite'],
                email=data['email']
            )
            db.session.add(new_student)
            db.session.commit()
            return jsonify(new_student.to_dict()), 201
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while adding the student'}), 500

    @app.route('/api/etudiants/<int:id>', methods=['GET'])
    def getStudent(id):
        try:
            etudiant = Etudiant.query.get(id)
            if not etudiant:
                return jsonify({'message': 'Student not found'}), 404
            return jsonify(etudiant.to_dict())
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching the student'}), 500

    @app.route('/api/etudiants/<int:id>', methods=['PUT'])
    def updateStudent(id):
        try:
            data = request.get_json()
            etudiant = Etudiant.query.get(id)
            if not etudiant:
                return jsonify({'message': 'Student not found'}), 404
            etudiant.nom = data.get('nom', etudiant.nom)
            etudiant.prenom = data.get('prenom', etudiant.prenom)
            etudiant.promotion_id = data.get('promotion_id', etudiant.promotion_id)
            etudiant.groupe_id = data.get('groupe_id', etudiant.groupe_id)
            etudiant.site_id = data.get('site_id', etudiant.site_id)
            etudiant.specialite = data.get('specialite', etudiant.specialite)
            etudiant.email = data.get('email', etudiant.email)
            db.session.commit()
            return jsonify(etudiant.to_dict()), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while updating the student'}), 500

    @app.route('/api/etudiants/<int:id>', methods=['DELETE'])
    def deleteStudent(id):
        try:
            etudiant = Etudiant.query.get(id)
            if not etudiant:
                return jsonify({'message': 'Student not found'}), 404
            db.session.delete(etudiant)
            db.session.commit()
            app.logger.info(f"L'étudiant avec l'ID {id} a été supprimé avec succès.")
            return jsonify({'message': 'Student deleted successfully'}), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while deleting the student'}), 500
#UPLOAD EXCEL
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        app.logger.info("Je suis au début de UPLOAD.")
        if 'file' not in request.files:
            app.logger.error("Aucun fichier trouvé dans la requête.")
            return jsonify({"error": "Aucun fichier trouvé"}), 400
        file = request.files['file']
        if file.filename == '':
            app.logger.error("Le fichier est vide (pas de nom).")
            return jsonify({"error": "Aucun fichier sélectionné"}), 400
        try:
            app.logger.info(f"Lecture du fichier : {file.filename}")
            df = pd.read_excel(file)
            app.logger.info("Fichier chargé avec succès.")
            
            # Afficher les colonnes du fichier
            app.logger.info(f"Colonnes du fichier : {df.columns.tolist()}")
            
            required_columns = ["nom", "prenom", "promotion", "groupe", "site", "specialite", "email"]
            if not all(column in df.columns for column in required_columns):
                missing_cols = [column for column in required_columns if column not in df.columns]
                app.logger.error(f"Colonnes manquantes dans le fichier : {', '.join(missing_cols)}")
                return jsonify({"error": f"Le fichier doit contenir les colonnes suivantes: {', '.join(required_columns)}"}), 400

            for index, row in df.iterrows():
                app.logger.info(f"Vérification des données pour la ligne : {row}")
                promotion = Promotion.query.filter_by(nom=row["promotion"]).first()
                groupe = Groupe.query.filter_by(nom=row["groupe"]).first()
                site = Site.query.filter_by(nom=row["site"]).first()
                
                if not promotion:
                    app.logger.error(f"Promotion non trouvée pour : {row['promotion']}")
                if not groupe:
                    app.logger.error(f"Groupe non trouvé pour : {row['groupe']}")
                if not site:
                    app.logger.error(f"Site non trouvé pour : {row['site']}")

                if not promotion or not groupe or not site:
                    app.logger.error(f"Données invalides dans la ligne : {row}")
                    return jsonify({"error": f"Données invalides dans la ligne : {row}"}), 400

                # Vérifier si l'étudiant existe déjà
                existing_student = Etudiant.query.filter_by(email=row["email"]).first()
                if existing_student:
                    app.logger.info(f"Étudiant déjà existant : {row['email']}")
                    continue  # ou retournez une erreur si nécessaire

                etudiant = Etudiant(
                    nom=row["nom"],
                    prenom=row["prenom"],
                    promotion_id=promotion.id,
                    groupe_id=groupe.id,
                    site_id=site.id,
                    specialite=row["specialite"],
                    email=row["email"]
                )
                db.session.add(etudiant)

            db.session.commit()
            app.logger.info("Étudiants importés avec succès.")
            return jsonify({"message": "Étudiants importés avec succès"}), 200
        except Exception as e:
            app.logger.error(f"Erreur lors du traitement du fichier : {str(e)}")
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


    # Gestion sites
    @app.route('/api/sites', methods=['GET'])
    def get_sites():
        app.logger.info("Route /api/sites a été atteinte.")
        try:
            # Récupérer tous les sites depuis la base de données
            sites = Site.query.all()

            # Si aucun site n'est trouvé
            if not sites:
                app.logger.info("Aucun site trouvé.")
                return jsonify({'message': 'No sites found'}), 404

            # Convertir les sites en dictionnaires et les retourner en JSON
            return jsonify([site.to_dict() for site in sites])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching sites'}), 500

    # Gestion des Promotions
    @app.route('/api/promotions', methods=['GET'])
    def get_promotions():
        try:
            promotions = Promotion.query.all()
            if not promotions:
                return jsonify({'message': 'No promotions found'}), 404
            return jsonify([promotion.to_dict() for promotion in promotions])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching promotions'}), 500

    @app.route('/api/promotions/<int:id>', methods=['GET'])
    def get_promotion(id):
        try:
            promotion = Promotion.query.get(id)
            if not promotion:
                return jsonify({'message': 'Promotion not found'}), 404
            return jsonify(promotion.to_dict())
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching the promotion'}), 500

    @app.route('/api/promotions', methods=['POST'])
    def add_promotion():
        try:
            data = request.get_json()
            new_promotion = Promotion(
                nom=data['nom'],
                site_id=data['site_id']
            )
            db.session.add(new_promotion)
            db.session.commit()
            return jsonify(new_promotion.to_dict()), 201
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while adding the promotion'}), 500

    @app.route('/api/promotions/<int:id>', methods=['PUT'])
    def update_promotion(id):
        try:
            data = request.get_json()
            promotion = Promotion.query.get(id)
            if not promotion:
                return jsonify({'message': 'Promotion not found'}), 404
            promotion.nom = data['nom']
            promotion.site_id = data['site_id']
            db.session.commit()
            return jsonify(promotion.to_dict()), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while updating the promotion'}), 500

    @app.route('/api/promotions/<int:id>', methods=['DELETE'])
    def delete_promotion(id):
        try:
            promotion = Promotion.query.get(id)
            if not promotion:
                return jsonify({'message': 'Promotion not found'}), 404
            db.session.delete(promotion)
            db.session.commit()
            return jsonify({'message': 'Promotion deleted successfully'}), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while deleting the promotion'}), 500

    # Gestion groupes
    # Liste des groupes
    @app.route('/api/groupes', methods=['GET'])
    def get_groupes():
        try:
            groupes = Groupe.query.all()
            if not groupes:
                return jsonify({'message': 'No groupes found'}), 404
            return jsonify([groupe.to_dict() for groupe in groupes])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching groupes'}), 500

    # Ajouter un groupe
    @app.route('/api/groupes', methods=['POST'])
    def add_groupe():
        try:
            data = request.get_json()
            promotion = Promotion.query.filter_by(nom=data['promotion']).first()
            site = Site.query.filter_by(nom=data['site']).first()
            if not promotion:
                return jsonify({'message': 'Promotion not found'}), 404
            if not site:
                return jsonify({'message': 'Site not found'}), 404

            new_groupe = Groupe(
                nom=data['nom'],
                promotion_id=promotion.id,
                site_id=site.id,
            )
            db.session.add(new_groupe)
            db.session.commit()
            return jsonify(new_groupe.to_dict()), 201
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while adding the groupe'}), 500

    # Supprimer un groupe
    @app.route('/api/groupes/<int:id>', methods=['DELETE'])
    def delete_groupe(id):
        try:
            groupe = Groupe.query.get(id)
            if not groupe:
                return jsonify({'message': 'Groupe not found'}), 404
            db.session.delete(groupe)
            db.session.commit()
            return jsonify({'message': 'Groupe deleted successfully'}), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while deleting the groupe'}), 500
