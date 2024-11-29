from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import RegistrationForm
from app.services.animals_service import AnimalsService
from app.models import Animals

# Définir le blueprint pour les animaux
animals_routes = Blueprint('animals_routes', __name__)

@animals_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
        except (ValueError, KeyError):
            age = None

        """On recupère les informations """
        form = RegistrationForm(
            nom=request.form['nom'],
            espece=request.form['espece'],
            race=request.form['race'],
            age=age,
            description=request.form['description'],
            email=request.form['email'],  
            adresse=request.form['adresse'],
            ville=request.form['ville'],
            code_postal=request.form['code_postal'],
        )

        if not form.validate():
            return render_template('register.html', form=form, errors=form.errors)

        # On appel le service pour enregistrer l'animal
        result = AnimalsService.register_animal(
            form.nom, form.espece, form.race, form.age,
            form.description, form.email, form.adresse, form.ville, form.code_postal
        )

        if result["status"] == "error":
            return render_template('register.html', form=form, errors={"global": result["message"]})

        flash(result["message"], "success")
        return redirect(url_for('animals_routes.list'))

    # Pour la méthode GET : on initialise des variables
    return render_template('register.html', form=None, errors={})


"""Nous affichons 9 éléments par pages"""
@animals_routes.route('/list', methods=['GET'])
def list():
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Nombre d'animaux par page
    query = request.args.get('query', '')  # On récupère la clé que nous allons utiliser pour la recherche depuis les paramètres GET

    try:
        if query: 
            animals = Animals.search_paginated(query, page, per_page)
            total_animals = Animals.count_search_results(query)
        else:
            animals = Animals.get_paginated_animals(page, per_page)
            total_animals = Animals.count_animals()

        total_pages = (total_animals + per_page - 1) // per_page
    except Exception as e:
        return render_template('list.html', errors={"global": f"Erreur lors de la récupération des données : {e}"})

    return render_template(
        'list.html',
        animals=animals,
        page=page,
        total_pages=total_pages,
        query=query,
    )