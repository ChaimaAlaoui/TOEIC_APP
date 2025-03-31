from flask import Flask, request, jsonify
from app import db
import pandas as pd
from io import BytesIO
from app.models import Etudiant, Groupe, Promotion, Semestre, Site,test_groupe, Test,ReponseEtudiant,ReponseProf,Score
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

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

            # Vérifier que les entités existent
            promotion = Promotion.query.get(data['promotion_id'])
            groupe = Groupe.query.get(data['groupe_id'])
            site = Site.query.get(data['site_id'])
            semestre = Semestre.query.get(data['semestre_id'])

            if not promotion or not groupe or not site or not semestre:
                return jsonify({'error': 'Promotion, groupe, site ou semestre non trouvé'}), 400

            # Créer un nouvel étudiant
            new_student = Etudiant(
                nom=data['nom'],
                prenom=data['prenom'],
                promotion_id=data['promotion_id'],
                groupe_id=data['groupe_id'],
                site_id=data['site_id'],
                semestre_id=data['semestre_id'],  # Ajout du semestre_id
                specialite=data['specialite'],
                email=data['email']
            )

            # Ajouter et valider l'étudiant
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
            etudiant.semestre_id = data.get('semestre_id', etudiant.semestre_id)
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

    @app.route('/api/groupes', methods=['POST'])
    def add_groupe():
        try:
            data = request.get_json()
            print('Voici le groupe à ajouter :', data)

            # Chercher la promotion, le site et le semestre par ID (et non par nom)
            promotion = Promotion.query.filter_by(id=int(data['promotion_id'])).first()
            site = Site.query.filter_by(id=int(data['site_id'])).first()
            semestre = Semestre.query.filter_by(id=int(data['semestre_id'])).first()

            # Vérifier que la promotion, le site et le semestre existent
            if not promotion:
                return jsonify({'message': 'Promotion not found'}), 404
            if not site:
                return jsonify({'message': 'Site not found'}), 404
            if not semestre:
                return jsonify({'message': 'Semestre not found'}), 404

            # Créer un nouveau groupe avec le semestre_id
            new_groupe = Groupe(
                nom=data['nom'],
                promotion_id=promotion.id,
                site_id=site.id,
                semestre_id=semestre.id  # Ajout du semestre_id
            )

            # Ajouter et valider le nouveau groupe
            db.session.add(new_groupe)
            db.session.commit()

            print('Groupe ajouté avec succès :', new_groupe.to_dict())
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
    @app.route('/api/groupes/<int:id>', methods=['GET'])
    def get_groupe(id):
        try:
           groupe = Groupe.query.get(id)
           if not groupe:
               return jsonify({'message': 'Groupe not found'}), 404
           return jsonify(groupe.to_dict())
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching the groupe'}), 500
    @app.route('/api/groupes/<int:id>', methods=['PUT'])
    def update_groupe(id):
        try:
            data = request.get_json()
            print('here the data of groupe to update',data)
            groupe = Groupe.query.get(id)
            if not groupe:
                return jsonify({'message': 'Groupe not found'}), 404
        
            groupe.nom = data.get('nom', groupe.nom)
            groupe.promotion_id = data.get('promotion_id', groupe.promotion_id)
            groupe.site_id = data.get('site_id', groupe.site_id)
            groupe.semestre_id = data.get('semestre_id', groupe.semestre_id)
        
            db.session.commit()
        
            return jsonify(groupe.to_dict()), 200
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while updating the groupe'}), 500
        
    @app.route('/api/groupes/by_site_promotion_semestre', methods=['GET'])
    def get_groupes_by_site_promotion_semestre():
        try:
            # Récupérer les paramètres de la requête
            site_id = request.args.get('site_id')
            promotion_id = request.args.get('promotion_id')
            semestre_id = request.args.get('semestre_id')

            # Vérifier que les paramètres sont présents
            if not site_id or not promotion_id or not semestre_id:
                return jsonify({'error': 'Les paramètres site_id, promotion_id et semestre_id sont requis'}), 400

            # Convertir les paramètres en entiers
            site_id = int(site_id)
            promotion_id = int(promotion_id)
            semestre_id = int(semestre_id)

            # Filtrer les groupes par site, promotion et semestre
            groupes = Groupe.query.filter_by(
                site_id=site_id,
                promotion_id=promotion_id,
                semestre_id=semestre_id
            ).all()

            # Si aucun groupe n'est trouvé
            if not groupes:
                return jsonify({'message': 'Aucun groupe trouvé pour ce site, promotion et semestre'}), 404

            # Retourner les groupes au format JSON
            return jsonify([groupe.to_dict() for groupe in groupes])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'Une erreur est survenue lors de la récupération des groupes'}), 500
            
    #pour la partie recherche de score
    @app.route('/api/promotions/by_site/<int:site_id>', methods=['GET'])
    def get_promotions_by_site(site_id):
        try:
            promotions = Promotion.query.filter_by(site_id=site_id).all()
            if not promotions:
                return jsonify({'message': 'No promotions found for this site'}), 404
            return jsonify([promotion.to_dict() for promotion in promotions])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching promotions'}), 500

    @app.route('/api/groupes/by_promotion_and_site/<int:promotion_id>/<int:site_id>', methods=['GET'])
    def get_groupes_by_promotion_and_site(promotion_id, site_id):
        try:
            groupes = Groupe.query.filter_by(promotion_id=promotion_id, site_id=site_id).all()
            if not groupes:
                return jsonify({'message': 'No groupes found for this promotion and site'}), 404
            return jsonify([groupe.to_dict() for groupe in groupes])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'An error occurred while fetching groupes'}), 500
        

    @app.route('/api/tests/by_site_promotion_group_semester/<int:site_id>/<int:promotion_id>/<int:groupe_id>/<int:semestre_id>', methods=['GET'])
    def get_tests_by_site_promotion_group_semester(site_id, promotion_id, groupe_id, semestre_id):
        try:
            # Vérifier d'abord que le groupe existe et appartient à la promotion, site et semestre
            groupe = Groupe.query.filter_by(
                id=groupe_id,
                promotion_id=promotion_id,
                site_id=site_id,
                semestre_id=semestre_id
            ).first()
            
            if not groupe:
                return jsonify({'message': 'Groupe non trouvé pour cette combinaison site/promotion/semestre'}), 404

            # Récupérer les tests associés à ce groupe
            tests = Test.query \
                .join(test_groupe, Test.id == test_groupe.c.test_id) \
                .filter(test_groupe.c.groupe_id == groupe_id) \
                .all()

            if not tests:
                return jsonify({'message': 'Aucun test trouvé pour ce groupe'}), 404

            return jsonify([test.to_dict() for test in tests])

        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'Une erreur est survenue lors de la récupération des tests'}), 500

    @app.route('/api/semestres/by_promotion', methods=['GET'])
    def get_semestres_by_site_and_promotion():
        try:
            # Récupérer les paramètres de la requête
            promotion_id = request.args.get('promotion_id')

            # Vérifier que les paramètres sont présents
            if not promotion_id:
                return jsonify({'error': 'Les paramètres promotion_id est requis'}), 400

            # Convertir les paramètres en entiers
           
            promotion_id = int(promotion_id)

            # Filtrer les semestres par site et promotion
            semestres = Semestre.query.filter_by(promotion_id=promotion_id).all()

            # Vérifier si des semestres ont été trouvés
            if not semestres:
                return jsonify({'message': 'Aucun semestre trouvé pour ce site et cette promotion'}), 404

            # Retourner les semestres au format JSON
            return jsonify([semestre.to_dict() for semestre in semestres])
        except Exception as e:
            app.logger.error(f"Erreur : {e}")
            return jsonify({'error': 'Une erreur est survenue lors de la récupération des semestres'}), 500

    @app.route('/api/scores/calculate', methods=['GET'])
    def calculate_scores():
        try:
            # Récupérer les paramètres de la requête
            site_id = request.args.get('site_id')
            promotion_id = request.args.get('promotion_id')
            groupe_id = request.args.get('groupe_id')
            semestre_id = request.args.get('semestre_id')
            test_id = request.args.get('test_id')

            # Vérifier que tous les paramètres sont présents
            if not all([site_id, promotion_id, groupe_id, semestre_id, test_id]):
                return jsonify({'error': 'Tous les paramètres sont requis'}), 400

            # Convertir les paramètres en entiers
            site_id = int(site_id)
            promotion_id = int(promotion_id)
            groupe_id = int(groupe_id)
            semestre_id = int(semestre_id)
            test_id = int(test_id)

            # Récupérer le semestre pour connaître la valeur M
            semestre = Semestre.query.get(semestre_id)
            if not semestre:
                return jsonify({'error': 'Semestre non trouvé'}), 404

            # Déterminer la valeur M en fonction du semestre
            semestre_nom = semestre.nom.upper()
            if 'S5' in semestre_nom:
                M = 535
            elif 'S6' in semestre_nom:
                M = 585
            elif 'S7' in semestre_nom:
                M = 635
            elif 'S8' in semestre_nom:
                M = 685
            else:
                M = 535  # Valeur par défaut

            # Récupérer les étudiants qui ont répondu au test sélectionné
            etudiants = db.session.query(Etudiant)\
                .join(ReponseEtudiant, (Etudiant.id == ReponseEtudiant.etudiant_id) & 
                                (ReponseEtudiant.test_id == test_id))\
                .filter(
                    Etudiant.site_id == site_id,
                    Etudiant.promotion_id == promotion_id,
                    Etudiant.groupe_id == groupe_id,
                    Etudiant.semestre_id == semestre_id
                )\
                .distinct()\
                .all()

            if not etudiants:
                return jsonify({'message': 'Aucun étudiant avec des réponses trouvé pour ces critères'}), 404

            # Récupérer les réponses correctes du professeur pour ce test
            reponses_prof = {
                int(r.num_question): r.choix 
                for r in ReponseProf.query.filter_by(test_id=test_id).all()
            }

            results = []

            for etudiant in etudiants:
                # Vérifier si un score existe déjà pour cet étudiant et ce test
                existing_score = Score.query.filter_by(
                    etudiant_id=etudiant.id,
                    test_id=test_id
                ).first()

                # Récupérer toutes les réponses de l'étudiant pour ce test
                reponses_etudiant = ReponseEtudiant.query.filter_by(
                    etudiant_id=etudiant.id,
                    test_id=test_id
                ).all()

                # Si l'étudiant n'a pas de réponses pour ce test, on passe au suivant
                if not reponses_etudiant:
                    continue

                # Convertir en format {num_question: choix}
                reponses_etudiant_dict = {int(r.num_question): r.choix for r in reponses_etudiant}

                # Calculer H2 Oral (questions 1-100)
                h2_oral = 0
                for q in range(1, 101):
                    if q in reponses_etudiant_dict and q in reponses_prof:
                        if reponses_etudiant_dict[q] == reponses_prof[q]:
                            h2_oral += 1

                # Calculer Note Oral
                note_oral = (h2_oral * 20) / 100

                # Calculer Score Oral
                if h2_oral < 6:
                    score_oral = 5
                elif h2_oral < 26:
                    score_oral = (h2_oral - 5) * 5
                elif h2_oral < 35:
                    score_oral = (h2_oral - 4) * 5
                elif h2_oral < 44:
                    score_oral = (h2_oral - 3) * 5
                elif h2_oral < 47:
                    score_oral = (h2_oral - 2) * 5
                elif h2_oral < 48:
                    score_oral = (h2_oral - 1) * 5
                elif h2_oral < 53:
                    score_oral = h2_oral * 5
                elif h2_oral < 56:
                    score_oral = (h2_oral + 1) * 5
                elif h2_oral < 59:
                    score_oral = (h2_oral + 2) * 5
                elif h2_oral < 64:
                    score_oral = (h2_oral + 3) * 5
                elif h2_oral < 67:
                    score_oral = (h2_oral + 4) * 5
                elif h2_oral < 70:
                    score_oral = (h2_oral + 5) * 5
                elif h2_oral < 77:
                    score_oral = (h2_oral + 6) * 5
                elif h2_oral < 80:
                    score_oral = (h2_oral + 7) * 5
                elif h2_oral < 83:
                    score_oral = (h2_oral + 8) * 5
                elif h2_oral < 90:
                    score_oral = (h2_oral + 9) * 5
                else:
                    score_oral = 495

                # Calculer H2 Ecrit (questions 101-200)
                h2_ecrit = 0
                for q in range(101, 201):
                    if q in reponses_etudiant_dict and q in reponses_prof:
                        if reponses_etudiant_dict[q] == reponses_prof[q]:
                            h2_ecrit += 1

                # Calculer Note Ecrit
                note_ecrit = (h2_ecrit * 20) / 100

                # Calculer Score Ecrit
                if h2_ecrit < 16:
                    score_ecrit = 5
                elif h2_ecrit < 25:
                    score_ecrit = (h2_ecrit - 14) * 5
                elif h2_ecrit < 28:
                    score_ecrit = (h2_ecrit - 13) * 5
                elif h2_ecrit < 33:
                    score_ecrit = (h2_ecrit - 12) * 5
                elif h2_ecrit < 38:
                    score_ecrit = (h2_ecrit - 11) * 5
                elif h2_ecrit < 41:
                    score_ecrit = (h2_ecrit - 10) * 5
                elif h2_ecrit < 46:
                    score_ecrit = (h2_ecrit - 9) * 5
                elif h2_ecrit < 49:
                    score_ecrit = (h2_ecrit - 8) * 5
                elif h2_ecrit < 56:
                    score_ecrit = (h2_ecrit - 7) * 5
                elif h2_ecrit < 61:
                    score_ecrit = (h2_ecrit - 6) * 5
                elif h2_ecrit < 64:
                    score_ecrit = (h2_ecrit - 5) * 5
                elif h2_ecrit < 67:
                    score_ecrit = (h2_ecrit - 4) * 5
                elif h2_ecrit < 72:
                    score_ecrit = (h2_ecrit - 3) * 5
                elif h2_ecrit < 77:
                    score_ecrit = (h2_ecrit - 2) * 5
                elif h2_ecrit < 89:
                    score_ecrit = (h2_ecrit - 1) * 5
                elif h2_ecrit < 92:
                    score_ecrit = h2_ecrit * 5
                elif h2_ecrit < 94:
                    score_ecrit = (h2_ecrit + 1) * 5
                elif h2_ecrit < 98:
                    score_ecrit = (h2_ecrit + 2) * 5
                else:
                    score_ecrit = 495

                # Calculer Score Total TOEIC
                score_total_toeic = score_oral + score_ecrit

                # Calculer Note C.C
                note_cc = score_total_toeic / 49.5

                # Calculer Note ECUE TOEIC
                note_ecue_toeic = max(10 * (1 + (score_total_toeic - M) / (990 - M)), 0)

                # Créer ou mettre à jour le score dans la base de données
                if existing_score:
                    # Mettre à jour le score existant
                    existing_score.h2_oral = h2_oral
                    existing_score.note_oral = round(note_oral, 2)
                    existing_score.score_oral = score_oral
                    existing_score.h2_ecrit = h2_ecrit
                    existing_score.note_ecrit = round(note_ecrit, 2)
                    existing_score.score_ecrit = score_ecrit
                    existing_score.score_total_toeic = score_total_toeic
                    existing_score.note_cc = round(note_cc, 2)
                    existing_score.note_ecue_toeic = round(note_ecue_toeic, 2)
                else:
                    # Créer un nouveau score
                    new_score = Score(
                        h2_oral=h2_oral,
                        note_oral=round(note_oral, 2),
                        score_oral=score_oral,
                        h2_ecrit=h2_ecrit,
                        note_ecrit=round(note_ecrit, 2),
                        score_ecrit=score_ecrit,
                        score_total_toeic=score_total_toeic,
                        note_cc=round(note_cc, 2),
                        note_ecue_toeic=round(note_ecue_toeic, 2),
                        etudiant_id=etudiant.id,
                        test_id=test_id
                    )
                    db.session.add(new_score)

                # Ajouter le résultat pour la réponse JSON
                results.append({
                    'etudiant_id': etudiant.id,
                    'nom': etudiant.nom,
                    'prenom': etudiant.prenom,
                    'h2_oral': h2_oral,
                    'note_oral': round(note_oral, 2),
                    'score_oral': score_oral,
                    'h2_ecrit': h2_ecrit,
                    'note_ecrit': round(note_ecrit, 2),
                    'score_ecrit': score_ecrit,
                    'score_total_toeic': score_total_toeic,
                    'note_cc': round(note_cc, 2),
                    'note_ecue_toeic': round(note_ecue_toeic, 2)
                })

            # Valider les changements dans la base de données
            db.session.commit()

            return jsonify(results)

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erreur lors du calcul et sauvegarde des scores: {str(e)}")
            return jsonify({'error': str(e)}), 500


     ##########################generer PDFs#########################################################
    # @app.route('/api/generate-oral-pdf', methods=['GET'])
    # def generate_oral_pdf():
    #     try:
    #         # Récupérer les paramètres de la requête
    #         site_id = request.args.get('site_id')
    #         promotion_id = request.args.get('promotion_id')
    #         groupe_id = request.args.get('groupe_id')
    #         semestre_id = request.args.get('semestre_id')
    #         test_id = request.args.get('test_id')

    #         # Vérifier que tous les paramètres sont présents
    #         if not all([site_id, promotion_id, groupe_id, semestre_id, test_id]):
    #             return jsonify({'error': 'Tous les paramètres sont requis'}), 400

    #         # Convertir les paramètres en entiers
    #         site_id = int(site_id)
    #         promotion_id = int(promotion_id)
    #         groupe_id = int(groupe_id)
    #         semestre_id = int(semestre_id)
    #         test_id = int(test_id)

    #         # Récupérer les étudiants qui ont répondu au test sélectionné
    #         etudiants = db.session.query(Etudiant)\
    #             .join(ReponseEtudiant, (Etudiant.id == ReponseEtudiant.etudiant_id) & 
    #                             (ReponseEtudiant.test_id == test_id))\
    #             .filter(
    #                 Etudiant.site_id == site_id,
    #                 Etudiant.promotion_id == promotion_id,
    #                 Etudiant.groupe_id == groupe_id,
    #                 Etudiant.semestre_id == semestre_id
    #             )\
    #             .distinct()\
    #             .all()

    #         if not etudiants:
    #             return jsonify({'message': 'Aucun étudiant avec des réponses trouvé pour ces critères'}), 404

    #         # Récupérer les réponses correctes du professeur pour ce test
    #         reponses_prof = {
    #             int(r.num_question): r.choix 
    #             for r in ReponseProf.query.filter_by(test_id=test_id).all()
    #         }

    #         # Créer un buffer pour le PDF
    #         buffer = BytesIO()

    #         # Créer le document PDF
    #         doc = SimpleDocTemplate(buffer, pagesize=letter)
    #         elements = []

    #         # Styles
    #         styles = getSampleStyleSheet()
    #         style_title = styles['Title']
    #         style_heading = styles['Heading2']
    #         style_normal = styles['Normal']

    #         # Titre du document
    #         title = Paragraph("Rapport des Scores Oral - TOEIC", style_title)
    #         elements.append(title)
    #         elements.append(Spacer(1, 0.5 * inch))

    #         # Pour chaque étudiant, calculer les scores par partie
    #         for etudiant in etudiants:
    #             # Récupérer toutes les réponses de l'étudiant pour ce test
    #             reponses_etudiant = ReponseEtudiant.query.filter_by(
    #                 etudiant_id=etudiant.id,
    #                 test_id=test_id
    #             ).all()

    #             # Si l'étudiant n'a pas de réponses pour ce test, on passe au suivant
    #             if not reponses_etudiant:
    #                 continue

    #             # Convertir en format {num_question: choix}
    #             reponses_etudiant_dict = {int(r.num_question): r.choix for r in reponses_etudiant}

    #             # Calculer les scores par partie
    #             parties = [
    #                 {'nom': 'Partie 1 (Q1-6)', 'debut': 1, 'fin': 6},
    #                 {'nom': 'Partie 2 (Q7-31)', 'debut': 7, 'fin': 31},
    #                 {'nom': 'Partie 3 (Q32-70)', 'debut': 32, 'fin': 70},
    #                 {'nom': 'Partie 4 (Q71-100)', 'debut': 71, 'fin': 100}
    #             ]

    #             scores_parties = []
    #             for partie in parties:
    #                 bonnes_reponses = 0
    #                 for q in range(partie['debut'], partie['fin'] + 1):
    #                     if q in reponses_etudiant_dict and q in reponses_prof:
    #                         if reponses_etudiant_dict[q] == reponses_prof[q]:
    #                             bonnes_reponses += 1
    #                 scores_parties.append({
    #                     'partie': partie['nom'],
    #                     'bonnes_reponses': bonnes_reponses,
    #                     'total_questions': partie['fin'] - partie['debut'] + 1
    #                 })

    #             # Calculer le score total oral
    #             h2_oral = sum([p['bonnes_reponses'] for p in scores_parties])
    #             score_oral = calculate_oral_score(h2_oral)  # Utilisez votre fonction de calcul existante

    #             # Ajouter l'entête de l'étudiant
    #             student_header = Paragraph(f"Étudiant: {etudiant.nom} {etudiant.prenom}", style_heading)
    #             elements.append(student_header)
    #             elements.append(Spacer(1, 0.2 * inch))

    #             # Créer le tableau des scores par partie
    #             data = [
    #                 ['Partie', 'Questions Correctes', 'Total Questions', 'Pourcentage']
    #             ]

    #             for score in scores_parties:
    #                 pourcentage = (score['bonnes_reponses'] / score['total_questions']) * 100
    #                 data.append([
    #                     score['partie'],
    #                     str(score['bonnes_reponses']),
    #                     str(score['total_questions']),
    #                     f"{pourcentage:.1f}%"
    #                 ])

    #             # Ajouter le score total
    #             data.append([
    #                 'TOTAL ORAL',
    #                 str(h2_oral),
    #                 '100',
    #                 f"{(h2_oral / 100) * 100:.1f}%"
    #             ])
    #             data.append([
    #                 'SCORE TOEIC ORAL',
    #                 str(score_oral),
    #                 '',
    #                 ''
    #             ])

    #             # Créer le tableau
    #             table = Table(data)
    #             table.setStyle(TableStyle([
    #                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                 ('FONTSIZE', (0, 0), (-1, 0), 12),
    #                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #                 ('SPAN', (0, -1), (1, -1)),  # Fusionner les cellules pour le score TOEIC
    #                 ('BACKGROUND', (0, -2), (-1, -2), colors.lightgrey),
    #                 ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
    #             ]))

    #             elements.append(table)
    #             elements.append(Spacer(1, 0.5 * inch))

    #         # Générer le PDF
    #         doc.build(elements)

    #         # Préparer la réponse
    #         buffer.seek(0)
    #         response = make_response(buffer.getvalue())
    #         response.headers['Content-Type'] = 'application/pdf'
    #         response.headers['Content-Disposition'] = 'attachment; filename=scores_oral.pdf'

    #         return response

    #     except Exception as e:
    #         app.logger.error(f"Erreur lors de la génération du PDF: {str(e)}")
    #         return jsonify({'error': str(e)}), 500
    @app.route('/api/generate-oral-pdf', methods=['GET'])
    def generate_oral_pdf():
        try:
            # Récupérer les paramètres de la requête
            site_id = request.args.get('site_id')
            promotion_id = request.args.get('promotion_id')
            groupe_id = request.args.get('groupe_id')
            semestre_id = request.args.get('semestre_id')
            test_id = request.args.get('test_id')

            # Vérifier que tous les paramètres sont présents
            if not all([site_id, promotion_id, groupe_id, semestre_id, test_id]):
                return jsonify({'error': 'Tous les paramètres sont requis'}), 400

            # Convertir les paramètres en entiers
            site_id = int(site_id)
            promotion_id = int(promotion_id)
            groupe_id = int(groupe_id)
            semestre_id = int(semestre_id)
            test_id = int(test_id)

            # Récupérer les étudiants avec leurs scores depuis la table Score
            etudiants_scores = db.session.query(Etudiant, Score)\
                .join(Score, Etudiant.id == Score.etudiant_id)\
                .filter(
                    Score.test_id == test_id,
                    Etudiant.site_id == site_id,
                    Etudiant.promotion_id == promotion_id,
                    Etudiant.groupe_id == groupe_id,
                    Etudiant.semestre_id == semestre_id
                )\
                .all()

            if not etudiants_scores:
                return jsonify({'message': 'Aucun score trouvé pour ces critères'}), 404

            # Récupérer les réponses correctes du professeur pour ce test
            reponses_prof = {
                int(r.num_question): r.choix 
                for r in ReponseProf.query.filter_by(test_id=test_id).all()
            }

            # Créer un buffer pour le PDF
            buffer = BytesIO()

            # Créer le document PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            style_title = styles['Title']
            style_heading = styles['Heading2']
            style_normal = styles['Normal']

            # Titre du document
            title = Paragraph("Rapport des Scores Oral - TOEIC", style_title)
            elements.append(title)
            elements.append(Spacer(1, 0.5 * inch))

            # Pour chaque étudiant avec son score
            for etudiant, score in etudiants_scores:
                # Récupérer toutes les réponses de l'étudiant pour ce test
                reponses_etudiant = ReponseEtudiant.query.filter_by(
                    etudiant_id=etudiant.id,
                    test_id=test_id
                ).all()

                # Si l'étudiant n'a pas de réponses pour ce test, on passe au suivant
                if not reponses_etudiant:
                    continue

                # Convertir en format {num_question: choix}
                reponses_etudiant_dict = {int(r.num_question): r.choix for r in reponses_etudiant}

                # Calculer les scores par partie (pour le détail dans le PDF)
                parties = [
                    {'nom': 'Partie 1 (Q1-6)', 'debut': 1, 'fin': 6},
                    {'nom': 'Partie 2 (Q7-31)', 'debut': 7, 'fin': 31},
                    {'nom': 'Partie 3 (Q32-70)', 'debut': 32, 'fin': 70},
                    {'nom': 'Partie 4 (Q71-100)', 'debut': 71, 'fin': 100}
                ]

                scores_parties = []
                for partie in parties:
                    bonnes_reponses = 0
                    for q in range(partie['debut'], partie['fin'] + 1):
                        if q in reponses_etudiant_dict and q in reponses_prof:
                            if reponses_etudiant_dict[q] == reponses_prof[q]:
                                bonnes_reponses += 1
                    scores_parties.append({
                        'partie': partie['nom'],
                        'bonnes_reponses': bonnes_reponses,
                        'total_questions': partie['fin'] - partie['debut'] + 1
                    })

                # Utiliser les valeurs directement depuis la table Score
                h2_oral = score.h2_oral
                score_oral = score.score_oral

                # Ajouter l'entête de l'étudiant
                student_header = Paragraph(f"Étudiant: {etudiant.nom} {etudiant.prenom}", style_heading)
                elements.append(student_header)
                elements.append(Spacer(1, 0.2 * inch))

                # Créer le tableau des scores par partie
                data = [
                    ['Partie', 'Questions Correctes', 'Total Questions', 'Pourcentage']
                ]

                for score_partie in scores_parties:
                    pourcentage = (score_partie['bonnes_reponses'] / score_partie['total_questions']) * 100
                    data.append([
                        score_partie['partie'],
                        str(score_partie['bonnes_reponses']),
                        str(score_partie['total_questions']),
                        f"{pourcentage:.1f}%"
                    ])

                # Ajouter le score total
                data.append([
                    'TOTAL ORAL',
                    str(h2_oral),
                    '100',
                    f"{(h2_oral / 100) * 100:.1f}%"
                ])
                data.append([
                    'SCORE TOEIC ORAL',
                    str(score_oral),
                    '',
                    ''
                ])

                # Créer le tableau
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('SPAN', (0, -1), (1, -1)),  # Fusionner les cellules pour le score TOEIC
                    ('BACKGROUND', (0, -2), (-1, -2), colors.lightgrey),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
                ]))

                elements.append(table)
                elements.append(Spacer(1, 0.5 * inch))

            # Générer le PDF
            doc.build(elements)

            # Préparer la réponse
            buffer.seek(0)
            response = make_response(buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=scores_oral.pdf'

            return response

        except Exception as e:
            app.logger.error(f"Erreur lors de la génération du PDF: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
    #pour Pdf ecrit
    @app.route('/api/generate-ecrit-pdf', methods=['GET'])
    def generate_ecrit_pdf():
        try:
            # Récupérer les paramètres de la requête
            site_id = request.args.get('site_id')
            promotion_id = request.args.get('promotion_id')
            groupe_id = request.args.get('groupe_id')
            semestre_id = request.args.get('semestre_id')
            test_id = request.args.get('test_id')

            # Vérifier que tous les paramètres sont présents
            if not all([site_id, promotion_id, groupe_id, semestre_id, test_id]):
                return jsonify({'error': 'Tous les paramètres sont requis'}), 400

            # Convertir les paramètres en entiers
            site_id = int(site_id)
            promotion_id = int(promotion_id)
            groupe_id = int(groupe_id)
            semestre_id = int(semestre_id)
            test_id = int(test_id)

            # Récupérer les étudiants avec leurs scores depuis la table Score
            etudiants_scores = db.session.query(Etudiant, Score)\
                .join(Score, Etudiant.id == Score.etudiant_id)\
                .filter(
                    Score.test_id == test_id,
                    Etudiant.site_id == site_id,
                    Etudiant.promotion_id == promotion_id,
                    Etudiant.groupe_id == groupe_id,
                    Etudiant.semestre_id == semestre_id
                )\
                .all()

            if not etudiants_scores:
                return jsonify({'message': 'Aucun score trouvé pour ces critères'}), 404

            # Récupérer les réponses correctes du professeur pour ce test
            reponses_prof = {
                int(r.num_question): r.choix 
                for r in ReponseProf.query.filter_by(test_id=test_id).all()
            }

            # Créer un buffer pour le PDF
            buffer = BytesIO()

            # Créer le document PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            style_title = styles['Title']
            style_heading = styles['Heading2']
            style_normal = styles['Normal']

            # Titre du document
            title = Paragraph("Rapport des Scores Écrit - TOEIC", style_title)
            elements.append(title)
            elements.append(Spacer(1, 0.5 * inch))

            # Pour chaque étudiant avec son score
            for etudiant, score in etudiants_scores:
                # Récupérer toutes les réponses de l'étudiant pour ce test
                reponses_etudiant = ReponseEtudiant.query.filter_by(
                    etudiant_id=etudiant.id,
                    test_id=test_id
                ).all()

                # Si l'étudiant n'a pas de réponses pour ce test, on passe au suivant
                if not reponses_etudiant:
                    continue

                # Convertir en format {num_question: choix}
                reponses_etudiant_dict = {int(r.num_question): r.choix for r in reponses_etudiant}

                # Calculer les scores par partie (pour le détail dans le PDF)
                parties = [
                    {'nom': 'Partie 5 (Q101-130)', 'debut': 101, 'fin': 130},
                    {'nom': 'Partie 6 (Q131-146)', 'debut': 131, 'fin': 146},
                    {'nom': 'Partie 7 (Q147-200)', 'debut': 147, 'fin': 200}
                ]

                scores_parties = []
                for partie in parties:
                    bonnes_reponses = 0
                    for q in range(partie['debut'], partie['fin'] + 1):
                        if q in reponses_etudiant_dict and q in reponses_prof:
                            if reponses_etudiant_dict[q] == reponses_prof[q]:
                                bonnes_reponses += 1
                    scores_parties.append({
                        'partie': partie['nom'],
                        'bonnes_reponses': bonnes_reponses,
                        'total_questions': partie['fin'] - partie['debut'] + 1
                    })

                # Utiliser les valeurs directement depuis la table Score
                h2_ecrit = score.h2_ecrit
                score_ecrit = score.score_ecrit

                # Ajouter l'entête de l'étudiant
                student_header = Paragraph(f"Étudiant: {etudiant.nom} {etudiant.prenom}", style_heading)
                elements.append(student_header)
                elements.append(Spacer(1, 0.2 * inch))

                # Créer le tableau des scores par partie
                data = [
                    ['Partie', 'Questions Correctes', 'Total Questions', 'Pourcentage']
                ]

                for score_partie in scores_parties:
                    pourcentage = (score_partie['bonnes_reponses'] / score_partie['total_questions']) * 100
                    data.append([
                        score_partie['partie'],
                        str(score_partie['bonnes_reponses']),
                        str(score_partie['total_questions']),
                        f"{pourcentage:.1f}%"
                    ])

                # Ajouter le score total
                data.append([
                    'TOTAL ÉCRIT',
                    str(h2_ecrit),
                    '100',
                    f"{(h2_ecrit / 100) * 100:.1f}%"
                ])
                data.append([
                    'SCORE TOEIC ÉCRIT',
                    str(score_ecrit),
                    '',
                    ''
                ])

                # Créer le tableau
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('SPAN', (0, -1), (1, -1)),  # Fusionner les cellules pour le score TOEIC
                    ('BACKGROUND', (0, -2), (-1, -2), colors.lightgrey),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
                ]))

                elements.append(table)
                elements.append(Spacer(1, 0.5 * inch))

            # Générer le PDF
            doc.build(elements)

            # Préparer la réponse
            buffer.seek(0)
            response = make_response(buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=scores_ecrit.pdf'

            return response

        except Exception as e:
            app.logger.error(f"Erreur lors de la génération du PDF: {str(e)}")
            return jsonify({'error': str(e)}), 500
         

    # def calculate_oral_score(h2_oral):
    #     """Fonction pour calculer le score oral TOEIC"""
    #     if h2_oral < 6:
    #         return 5
    #     elif h2_oral < 26:
    #         return (h2_oral - 5) * 5
    #     elif h2_oral < 35:
    #         return (h2_oral - 4) * 5
    #     elif h2_oral < 44:
    #         return (h2_oral - 3) * 5
    #     elif h2_oral < 47:
    #         return (h2_oral - 2) * 5
    #     elif h2_oral < 48:
    #         return (h2_oral - 1) * 5
    #     elif h2_oral < 53:
    #         return h2_oral * 5
    #     elif h2_oral < 56:
    #         return (h2_oral + 1) * 5
    #     elif h2_oral < 59:
    #         return (h2_oral + 2) * 5
    #     elif h2_oral < 64:
    #         return (h2_oral + 3) * 5
    #     elif h2_oral < 67:
    #         return (h2_oral + 4) * 5
    #     elif h2_oral < 70:
    #         return (h2_oral + 5) * 5
    #     elif h2_oral < 77:
    #         return (h2_oral + 6) * 5
    #     elif h2_oral < 80:
    #         return (h2_oral + 7) * 5
    #     elif h2_oral < 83:
    #         return (h2_oral + 8) * 5
    #     elif h2_oral < 90:
    #         return (h2_oral + 9) * 5
    #     else:
    #         return 495       
#     def calculer_h2(etudiant_id, test_id):
#         # Récupérer les réponses de l'étudiant
#         reponses_etudiant = {
#             int(r.num_question): r.choix for r in ReponseEtudiant.query.filter_by(etudiant_id=etudiant_id, test_id=test_id).all()
#         }

#         # Récupérer les réponses correctes du professeur
#         reponses_prof = {
#             int(r.num_question): r.choix for r in ReponseProf.query.filter_by(test_id=test_id).all()
#         }

#         # Initialisation des scores
#         h2_oral = 0
#         h2_ecrit = 0
#         #tempo
#         score_oral = 0
#         score_ecrit = 0
#         score_total_toeic = 0
#         note_cc = 0
#         note_ecue_toeic = 0


#         # Comparaison des réponses
#         for num_question, choix_etudiant in reponses_etudiant.items():
#             choix_correct = reponses_prof.get(num_question)  # Utilisation de .get() pour éviter KeyError

#             if choix_correct is not None and choix_etudiant == choix_correct:
#                 if 1 <= num_question <= 100:
#                     h2_oral += 1
#                 elif 101 <= num_question <= 200:
#                     h2_ecrit += 1

#         # Calcul des notes sur 20
#         note_oral = (h2_oral * 20) / 100
#         note_ecrit = (h2_ecrit * 20) / 100   

#         # Affichage des résultats
#         print("====================================")
#         print(f"Étudiant ID : {etudiant_id}, Test ID : {test_id}")
#         print(f"Nombre de réponses correctes - ORAL : {h2_oral}/100")
#         print(f"Nombre de réponses correctes - ÉCRIT : {h2_ecrit}/100")
#         print(f"Note ORAL : {note_oral:.2f}/20")
#         print(f"Note ÉCRIT : {note_ecrit:.2f}/20")
#         print("====================================")

#         # Enregistrement dans la base de données
#         resultat = Score.query.filter_by(etudiant_id=etudiant_id, test_id=test_id).first()

#         if resultat:  # Mise à jour si l'entrée existe déjà
#             resultat.h2_oral = h2_oral
#             resultat.h2_ecrit = h2_ecrit
#             resultat.note_oral = note_oral
#             resultat.note_ecrit = note_ecrit
#         else:  # Création d'un nouvel enregistrement
#             resultat = Score(
#                 etudiant_id=etudiant_id,
#                 test_id=test_id,
#                 h2_oral=h2_oral,
#                 h2_ecrit=h2_ecrit,
#                 note_oral=note_oral,
#                 note_ecrit=note_ecrit,
#                 score_oral=score_oral,
#                 score_ecrit=score_ecrit,
#                 score_total_toeic=score_total_toeic,
#                 note_cc=note_cc,
#                 note_ecue_toeic=note_ecue_toeic
# )

#             db.session.add(resultat)

#         db.session.commit()  # Sauvegarde des modifications

#     # Retour des résultats
#         return {"h2_oral": h2_oral, "h2_ecrit": h2_ecrit, "note_oral": note_oral, "note_ecrit": note_ecrit}

# # Exécution dans le contexte de l'application Flask
#     with app.app_context():
#            calculer_h2(etudiant_id=32, test_id=1)

      

