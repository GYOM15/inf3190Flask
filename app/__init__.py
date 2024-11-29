# Initialisation de l'application Flask
from flask import Flask, render_template
from app.database import Database
from app.routes.animals_routes import animals_routes
from app.models import Animals
import logging

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    # Initialisation des tables (optionnelle)
    with app.app_context():
        Database.initialize_tables()

    # Enregistrement des blueprints
    app.register_blueprint(animals_routes, url_prefix='/animals')

    # Fermeture de la connexion à la base de données à la fin de chaque requête
    @app.teardown_appcontext
    def close_db(exception):
        Database.close_connection()
        
    # Route principale
    @app.route('/')
    def home():
        try:
            animals = Animals.get_paginated_animals(page=1, per_page=4)
        except Exception as e:
            app.logger.error(f"Erreur lors de la récupération des animaux : {e}")
            return render_template('index.html', errors={"global": "Désolé, une erreur s'est produite lors de la récupération des données."})
        return render_template('index.html', animals=animals)
    
    # Configuration des logs
    app.logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    
    return app

# Lancement de l'application
app = create_app()

if __name__ == '__main__':
    app.run()