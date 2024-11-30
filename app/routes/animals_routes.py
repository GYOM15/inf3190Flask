from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.animals_service import AnimalsService
import logging
import traceback

# Définir le blueprint pour les animaux
animals_routes = Blueprint('animals_routes', __name__)

def validate_form_data(data):
    """
    Valide les données du formulaire et retourne un dictionnaire d'erreurs.
    """
    errors = {}

    # Validation des champs obligatoires
    if not data.get("nom"):
        errors["nom"] = "Le nom est requis."
    if not data.get("espece"):
        errors["espece"] = "L'espèce est requise."
    if not data.get("race"):
        errors["race"] = "La race est requise."
    if not data.get("age") or not isinstance(data["age"], int) or data["age"] < 0:
        errors["age"] = "L'âge doit être un entier positif."
    if not data.get("email"):
        errors["email"] = "L'email est requis."
    if not data.get("adresse"):
        errors["adresse"] = "L'adresse est requise."
    if not data.get("ville"):
        errors["ville"] = "La ville est requise."
    if not data.get("code_postal"):
        errors["code_postal"] = "Le code postal est requis."

    # Validation supplémentaire
    if data.get("email") and "@" not in data["email"]:
        errors["email"] = "Le format de l'email est invalide."

    return errors



@animals_routes.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route pour enregistrer un nouvel animal.
    """
    if request.method == 'POST':
        try:
            form_data = {
                "nom": request.form['nom'],
                "espece": request.form['espece'],
                "race": request.form['race'],
                "age": int(request.form['age']) if request.form['age'].isdigit() else None,
                "description": request.form['description'],
                "email": request.form['email'],
                "adresse": request.form['adresse'],
                "ville": request.form['ville'],
                "code_postal": request.form['code_postal'],
            }

            errors = validate_form_data(form_data)

            # Appeler le service pour enregistrer l'animal
            result = AnimalsService.register_animal(**form_data)

            if result["status"] == "error":
                if result["message"] == AnimalsService.ERROR_MESSAGES["email_exists"]:
                    errors["email"] = result["message"]
                else:
                    errors["global"] = result["message"]

            if errors:
                return render_template('register.html', form=form_data, errors=errors)

            flash(result["message"], "success")
            return redirect(url_for('animals_routes.list'))

        except Exception as e:
            logging.error("Une erreur s'est produite : %s", str(e))
            logging.error(traceback.format_exc())

            return render_template('register.html', form={}, errors={"global": "Une erreur inattendue s'est produite. Vérifiez les logs pour plus de détails."})

    # Méthode GET - afficher le formulaire vide avec `errors`
    return render_template('register.html', form={}, errors={})



@animals_routes.route('/list', methods=['GET'])
def list():
    """
    Route pour afficher une liste paginée des animaux avec recherche.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 9
    query = request.args.get('query', '')

    try:
        if query:
            animals = AnimalsService.search_paginated(query, page, per_page)
            total_animals = AnimalsService.count_search_results(query)
        else:
            animals = AnimalsService.get_paginated_animals(page, per_page)
            total_animals = AnimalsService.count_animals()

        total_pages = (total_animals + per_page - 1) // per_page
        return render_template('list.html', animals=animals, page=page, total_pages=total_pages, query=query)

    except Exception:
        flash("Erreur lors de la récupération des données. Veuillez réessayer plus tard.", "error")
        return render_template('list.html', animals=[], page=1, total_pages=0, query=query)


@animals_routes.route('/admin', methods=['GET'])
def admin_panel():
    """
    Affiche une page d'administration avec tous les animaux et leurs actions.
    """
    try:
        animals = AnimalsService.display_all()
        return render_template('admin.html', animals=animals)
    except Exception:
        flash("Erreur lors de la récupération des données. Veuillez réessayer plus tard.", "error")
        return render_template('admin.html', animals=[])


@animals_routes.route('/delete/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    """
    Supprime un animal par son ID.
    """
    result = AnimalsService.delete_animal(animal_id)
    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}, 200
    else:
        return {"status": "error", "message": result["message"]}, 400


@animals_routes.route('/update/<int:animal_id>', methods=['GET', 'POST'])
def update_animal(animal_id):
    """
    Met à jour les informations d'un animal.
    """
    result = AnimalsService.get_animal_by_id(animal_id)
    if result["status"] == "error":
        flash(result["message"], "error")
        return redirect(url_for('animals_routes.admin_panel'))

    animal = result["data"]

    if request.method == 'POST':
        form_data = {
            "nom": request.form['nom'],
            "espece": request.form['espece'],
            "race": request.form['race'],
            "age": int(request.form['age']) if request.form['age'].isdigit() else None,
            "description": request.form['description'],
            "email": request.form['email'],
            "adresse": request.form['adresse'],
            "ville": request.form['ville'],
            "code_postal": request.form['code_postal'],
        }

        # Valider les données
        errors = validate_form_data(form_data)
        if errors:
            return render_template('update.html', animal=animal, errors=errors)

        # Appeler le service pour mettre à jour l'animal
        result = AnimalsService.update_animal(animal_id, form_data)
        if result["status"] == "success":
            flash(result["message"], "success")
            return redirect(url_for('animals_routes.admin_panel'))
        else:
            flash(result["message"], "error")
            return render_template('update.html', animal=animal)

    return render_template('update.html', animal=animal)