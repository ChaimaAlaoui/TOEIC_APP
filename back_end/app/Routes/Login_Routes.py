from flask import Blueprint, request, jsonify
from app import db
from app.Models.Teacher import  ReponseJuste, Test
from datetime import datetime


test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['GET'])
def get_tests():
    tests = Test.query.all()
    results = []
    for t in tests:
        results.append({
            'id_test': t.id_test,
            'Titre': t.titre,
            'Description': t.description,
            'Site': t.site,  
            'Date': t.date.isoformat() if t.date else None
        })
    return jsonify(results), 200

@test_bp.route('/', methods=['POST'])
def create_test():
    data = request.json
    date_obj = None
    if data.get('Date'):
        date_obj = datetime.strptime(data['Date'], '%Y-%m-%d').date()

    new_test = Test(
        titre=data.get('Titre'),
        description=data.get('Description'),
        site=data.get('Site'),
        date=date_obj
    )
    db.session.add(new_test)
    db.session.commit()

    # RENVOYER l'id_test dans la réponse
    return jsonify({
        'message': 'Test créé avec succès',
        'id_test': new_test.id_test
    }), 201

@test_bp.route('/<int:test_id>', methods=['GET'])
def get_test_by_id(test_id):
    t = Test.query.get(test_id)
    if not t:
        return jsonify({'message': 'Test introuvable'}), 404
    
    return jsonify({
        'id_test': t.id_test,
        'Titre': t.titre,
        'Description': t.description,
        'Site': t.site,  # Affiche "Site" à partir de la colonne "type"
        'Date': t.date.isoformat() if t.date else None
    }), 200

@test_bp.route('/<int:test_id>', methods=['PUT'])
def update_test(test_id):
    t = Test.query.get(test_id)
    if not t:
        return jsonify({'message': 'Test introuvable'}), 404

    data = request.json
    t.titre = data.get('Titre', t.titre)
    t.description = data.get('Description', t.description)
    t.site = data.get('Site', t.site)  # Mise à jour du champ "Site" stocké dans "type"
    if data.get('Date'):
        t.date = datetime.strptime(data['Date'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify({'message': 'Test modifié avec succès'}), 200

@test_bp.route('/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    t = Test.query.get(test_id)
    if not t:
        return jsonify({'message': 'Test introuvable'}), 404
    
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Test supprimé avec succès'}), 200





"""
groupe_bp = Blueprint('groupe_bp', __name__)

@groupe_bp.route('/', methods=['GET'])
def get_groupes():
    groupes = Groupe.query.all()
    results = []
    for g in groupes:
        results.append({
            'id_groupe': g.id_groupe,
            'nom': g.nom,
            'id_promotion': g.id_promotion
        })
    return jsonify(results), 200

@groupe_bp.route('/', methods=['POST'])
def create_groupe():
    data = request.json
    new_groupe = Groupe(
        nom=data.get('nom'),
        id_promotion=data.get('id_promotion')
    )
    db.session.add(new_groupe)
    db.session.commit()
    return jsonify({'message': 'Groupe créé avec succès'}), 201

@groupe_bp.route('/<int:groupe_id>', methods=['GET'])
def get_groupe_by_id(groupe_id):
    g = Groupe.query.get(groupe_id)
    if not g:
        return jsonify({'message': 'Groupe introuvable'}), 404

    return jsonify({
        'id_groupe': g.id_groupe,
        'nom': g.nom,
        'id_promotion': g.id_promotion
    }), 200

@groupe_bp.route('/<int:groupe_id>', methods=['PUT'])
def update_groupe(groupe_id):
    g = Groupe.query.get(groupe_id)
    if not g:
        return jsonify({'message': 'Groupe introuvable'}), 404

    data = request.json
    g.nom = data.get('nom', g.nom)
    g.id_promotion = data.get('id_promotion', g.id_promotion)
    db.session.commit()
    return jsonify({'message': 'Groupe modifié avec succès'}), 200

@groupe_bp.route('/<int:groupe_id>', methods=['DELETE'])
def delete_groupe(groupe_id):
    g = Groupe.query.get(groupe_id)
    if not g:
        return jsonify({'message': 'Groupe introuvable'}), 404

    db.session.delete(g)
    db.session.commit()
    return jsonify({'message': 'Groupe supprimé avec succès'}), 200


test_groupe_bp = Blueprint('test_groupe_bp', __name__)

@test_groupe_bp.route('/', methods=['GET'])
def get_tests_groupes():
    tests_groupes = TestGroupe.query.all()
    results = []
    for tg in tests_groupes:
        results.append({
            'id_test': tg.id_test,
            'id_groupe': tg.id_groupe,
            'titre': tg.titre,
            'description': tg.description,
            'nombre_evaluation': tg.nombre_evaluation,
            'nombre_etudiant': tg.nombre_etudiant
        })
    return jsonify(results), 200

@test_groupe_bp.route('/', methods=['POST'])
def create_test_groupe():
    data = request.json
    new_tg = TestGroupe(
        id_groupe=data.get('id_groupe'),
        titre=data.get('titre'),
        description=data.get('description'),
        nombre_evaluation=data.get('nombre_evaluation'),
        nombre_etudiant=data.get('nombre_etudiant')
    )
    db.session.add(new_tg)
    db.session.commit()
    return jsonify({'message': 'Test_groupe créé avec succès'}), 201

@test_groupe_bp.route('/<int:test_id>', methods=['GET'])
def get_test_groupe_by_id(test_id):
    tg = TestGroupe.query.get(test_id)
    if not tg:
        return jsonify({'message': 'Test_groupe introuvable'}), 404

    return jsonify({
        'id_test': tg.id_test,
        'id_groupe': tg.id_groupe,
        'titre': tg.titre,
        'description': tg.description,
        'nombre_evaluation': tg.nombre_evaluation,
        'nombre_etudiant': tg.nombre_etudiant
    }), 200

@test_groupe_bp.route('/<int:test_id>', methods=['PUT'])
def update_test_groupe(test_id):
    tg = TestGroupe.query.get(test_id)
    if not tg:
        return jsonify({'message': 'Test_groupe introuvable'}), 404

    data = request.json
    tg.id_groupe = data.get('id_groupe', tg.id_groupe)
    tg.titre = data.get('titre', tg.titre)
    tg.description = data.get('description', tg.description)
    tg.nombre_evaluation = data.get('nombre_evaluation', tg.nombre_evaluation)
    tg.nombre_etudiant = data.get('nombre_etudiant', tg.nombre_etudiant)
    db.session.commit()
    return jsonify({'message': 'Test_groupe modifié avec succès'}), 200

@test_groupe_bp.route('/<int:test_id>', methods=['DELETE'])
def delete_test_groupe(test_id):
    tg = TestGroupe.query.get(test_id)
    if not tg:
        return jsonify({'message': 'Test_groupe introuvable'}), 404

    db.session.delete(tg)
    db.session.commit()
    return jsonify({'message': 'Test_groupe supprimé avec succès'}), 200

"""

reponse_juste_bp = Blueprint('reponse_juste_bp', __name__)

@reponse_juste_bp.route('/batch', methods=['POST'])
def create_reponses_justes():
    data = request.json  # Attendu: liste d'objets { numero_question, choix, id_test }
    print("Données reçues:", data)
    if not isinstance(data, list):
        return jsonify({'message': 'Données invalides, une liste est attendue'}), 400

    created = 0
    for item in data:
        numero = item.get('numero_question')
        choix = item.get('choix')
        id_test = item.get('id_test')
        # Vérifier que le test existe
        test = Test.query.get(id_test)
        if not test:
            print(f"Test avec id {id_test} non trouvé !")
            continue  # ou retourner une erreur

        new_rep = ReponseJuste(numero_question=numero, choix=choix, id_test=id_test)
        db.session.add(new_rep)
        created += 1

    db.session.commit()
    return jsonify({'message': f'{created} réponses créées'}), 201

def init_routes(app):
    """
    Fonction d'initialisation des routes.
    Enregistre le blueprint 'test_bp' avec le préfixe '/api/tests'.
    """
    app.register_blueprint(test_bp, url_prefix='/api/tests')
    app.register_blueprint(reponse_juste_bp, url_prefix='/api/reponses_justes')