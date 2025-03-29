from flask_cors import CORS
from app import create_app, db
import mysql.connector
from sqlalchemy.exc import OperationalError

app = create_app()

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

# Fonction pour créer la base de données si elle n'existe pas
def create_database():
    try:
        # Se connecter directement à MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  
        )
        cursor = connection.cursor()
        
        # Créer la base de données si elle n'existe pas
        cursor.execute("CREATE DATABASE IF NOT EXISTS toeic_app;")
        connection.commit()
        
        print("Base de données 'toeic_app' créée avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de la création de la base de données: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Créer toutes les tables à partir des modèles définis dans votre code
 # Crée toutes les tables en fonction des classes définies dans app/models.py

if __name__ == "__main__":
    print("Lancement de l'application Flask...")
    app.run(port=app.config['FLASK_APP_PORT'], debug=True)

