from flask import Flask, render_template, request
from app.database import Database
from app.routes.animals_routes import animals_routes
from app.models import Animals
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    """
    Initialise l'application Flask et configure les routes, logs et base de données.
    """
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    # Initialisation des tables de la base de données (si nécessaire)
    with app.app_context():
        Database.initialize_tables()

    # Enregistrement des blueprints
    app.register_blueprint(animals_routes, url_prefix='/animals')

    # Fermeture de la connexion à la base de données à la fin de chaque requête
    @app.teardown_appcontext
    def close_db(exception):
        Database.close_connection()

    # Configuration du journal
    logging.basicConfig(
        filename='app.log',
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    # Route principale
    @app.route('/')
    def home():
        """
        Gère la route principale '/'.
        Affiche une liste paginée des animaux.
        """
        # Récupérer les paramètres de la requête pour la pagination
        page = request.args.get('page', 1, type=int)  # Par défaut : page 1
        per_page = request.args.get('per_page', 4, type=int)  # Par défaut : 4 éléments par page

        # Récupérer les animaux paginés
        animals = Animals.get_paginated_animals(page=page, per_page=per_page)

        # Rendre le template avec les données des animaux
        return render_template('index.html', animals=animals, page=page, per_page=per_page)

    return app


# Lancement de l'application
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)