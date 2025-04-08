# site_routes.py

from flask import jsonify
from app.Models.myModels import Site

def init_site_routes(app):
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