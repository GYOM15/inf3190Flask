import logging
from flask import Flask, render_template, request
from app.database import Database
from app.routes.animals_routes import animals_routes
from app.models import Animals

# Configuration du journal
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,  # Inclut INFO, WARNING, ERROR
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

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

    # Rediriger les logs de Flask vers logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.ERROR)

    # Route principale
    @app.route('/')
    def home():
        """
        Gère la route principale '/'.
        Affiche une liste paginée des animaux.
        """
        try:
            # Récupérer les paramètres de la requête pour la pagination
            page = request.args.get('page', 1, type=int)  # Par défaut : page 1
            per_page = request.args.get('per_page', 4, type=int)  # Par défaut : 4 éléments par page

            # Récupérer les animaux paginés
            animals = Animals.get_paginated_animals(page=page, per_page=per_page)

            # Rendre le template avec les données des animaux
            return render_template('index.html', animals=animals, page=page, per_page=per_page)
        except Exception as e:
            logging.error(f"Erreur dans la route principale : {e}")
            return render_template('error.html'), 500  # Page d'erreur

    return app


# Lancement de l'application
app = create_app()