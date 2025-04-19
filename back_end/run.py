from flask_cors import CORS
from app import create_app, db
import mysql.connector
from sqlalchemy.exc import OperationalError
import os

app = create_app()



CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "http://localhost:4200",
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS toeic_app;")
        connection.commit()
        print("✅ Base de données 'toeic_app' vérifiée ou créée avec succès.")
    except mysql.connector.Error as e:
        print(f" Erreur lors de la création de la base de données: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_all_tables():
    try:
        # Important : exécuter create_all() **dans un app context**
        with app.app_context():
            db.create_all()
            print("✅ Toutes les tables ont été créées avec succès.")
    except OperationalError as e:
        print(f" Erreur lors de la création des tables : {e}")


if __name__ == "__main__":
    print(" Lancement de l'application Flask...")
    create_database()
    create_all_tables()
    
    port = app.config.get('FLASK_APP_PORT', 5000)
    app.run(port=port, debug=True)
