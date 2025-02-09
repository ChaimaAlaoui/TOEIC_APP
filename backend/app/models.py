from app import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # Exemple : "Boulogne", "Calais", etc.
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
        }

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # Exemple : "ING1 2024-2025"
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    site = db.relationship('Site', backref='promotions')
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'site_id': self.site_id,
            'site': self.site.nom
        }

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)  # Exemple : "Cls 1 24-25 PODVIN"
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    promotion = db.relationship('Promotion', backref='groupes')
    site = db.relationship('Site', backref='groupes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'promotion_id': self.promotion_id,
            'promotion': self.promotion.nom,
            'site_id': self.site_id,  
            'site': self.site.nom  
        }


class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupe.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    specialite = db.Column(db.String(100), nullable=False)  # Exemple : "Informatique", "Génie Civil"
    email = db.Column(db.String(150), unique=True, nullable=False)

    promotion = db.relationship('Promotion', backref='etudiants')
    groupe = db.relationship('Groupe', backref='etudiants')
    site = db.relationship('Site', backref='etudiants')

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'promotion': self.promotion.nom,
            'groupe': self.groupe.nom,
            'site': self.site.nom,
            'specialite': self.specialite,
            'email': self.email
        }

    def __repr__(self):
        return f"<Etudiant {self.nom} {self.prenom}, Site: {self.site.nom}, Promo: {self.promotion.nom}>"