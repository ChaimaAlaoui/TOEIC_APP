from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Colonne de type Integer pour l'ID (clé primaire)
    nom = db.Column(db.String(100), nullable=False)  # Colonne pour le nom
    prenom = db.Column(db.String(100), nullable=False)  # Colonne pour le prénom
    email = db.Column(db.String(120), unique=True, nullable=False)  # Colonne pour l'email (unique)
    mot_de_passe = db.Column(db.String(200), nullable=False)  # Colonne pour le mot de passe
    is_active = db.Column(db.Boolean, default=True)  # Colonne pour l'état d'activité de l'enseignant (par défaut actif)

    def __repr__(self):
        return f"<Teacher {self.nom} {self.prenom}>"
    
    def set_password(self, password):
        # Hachage du mot de passe avant de le stocker
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        # Vérification du mot de passe avec le mot de passe haché stocké
        return check_password_hash(self.mot_de_passe, password)





class Test(db.Model):
    __tablename__ = 'test'

    ID_date_groupe = db.Column(db.Integer, primary_key=True)
    Titre = db.Column(db.String(100), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    
    reponses_officielles = db.relationship('RéponseOfficielle', backref='test', lazy=True)
    reponses_etudiants = db.relationship('Réponse', backref='test', lazy=True)

   
    def modifier_test(self, nouveau_titre, nouveau_type, nouvelle_date):
        """ Met à jour les informations du test """
        self.Titre = nouveau_titre
        self.Type = nouveau_type
        self.Date = nouvelle_date
        db.session.commit()

   
    def suppression_test(self):
        """ Supprime un test de la base de données """
        db.session.delete(self)
        db.session.commit()

    
    def generer_fiche_reponse(self):
        """ Génère une fiche de réponse avec 200 questions pour ce test """
        from app.models import ReponseOfficielle
        for i in range(1, 201):
            reponse = ReponseOfficielle(numero_question=i, reponse_correcte='', id_test=self.ID_date_groupe)
            db.session.add(reponse)
        db.session.commit()

    # Ajouter une image référente (ex: une consigne en image)
    def ajouter_image_referente(self, chemin_image):
        """ Associe une image référente à un test """
        from app.models import FichierScanner
        fichier = FichierScanner(Nom_fichier="Image Test", Chemin_fichier=chemin_image, id_test=self.ID_date_groupe)
        db.session.add(fichier)
        db.session.commit()

    # Importer un fichier PDF de réponses scannées
    def importer_fichier(self, chemin_fichier):
        """ Enregistre un fichier PDF scanné lié à ce test """
        from app.models import FichierScanner
        fichier = FichierScanner(Nom_fichier="Fiche Réponse", Chemin_fichier=chemin_fichier, id_test=self.ID_date_groupe)
        db.session.add(fichier)
        db.session.commit()

    # Corriger automatiquement un test à partir des réponses scannées
    def corrige_test(self):
        """ Compare les réponses scannées avec les réponses officielles et calcule les scores """
        from app.models import Reponse, ReponseOfficielle, Resultat
        score = 0
        reponses_etudiants = Reponse.query.filter_by(id_test=self.ID_date_groupe).all()
        reponses_correctes = {r.numero_question: r.reponse_correcte for r in ReponseOfficielle.query.filter_by(id_test=self.ID_date_groupe).all()}

        for reponse in reponses_etudiants:
            if reponses_correctes.get(reponse.numero_question) == reponse.choix:
                score += 1

        # Stocker le score dans la table Résultat
        resultat = Resultat(ID_test=self.ID_date_groupe, Score_totale=score)
        db.session.add(resultat)
        db.session.commit()
        return score

    def __repr__(self):
        return f"<Test {self.Titre} - {self.Type} - {self.Date}>"



class ReponseOfficielle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_question = db.Column(db.Integer, nullable=False)
    reponse_correcte = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    id_test = db.Column(db.Integer, db.ForeignKey('test.ID_date_groupe'), nullable=False)

    def __repr__(self):
        return f"<ReponseOfficielle Q{self.numero_question}: {self.reponse_correcte}>"


