# semestre_routes.py

from flask import request, jsonify
from app.Models.myModels import Semestre

def init_semestre_routes(app):
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