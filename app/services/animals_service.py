import re
import logging
from app.models import Animals

class AnimalsService:
    """
    Service pour gérer les opérations métier liées aux animaux.
    
    """
    EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

    ERROR_MESSAGES = {
        "missing_fields": "Champs manquants : {fields}.",
        "invalid_email": "L'email fourni n'est pas valide.",
        "email_exists": "Un animal avec cet email existe déjà.",
        "not_found": "Animal introuvable.",
        "internal_error": "Une erreur interne s'est produite. Veuillez réessayer plus tard.",
    }

    @staticmethod
    def is_valid_email(email):
        return re.match(AnimalsService.EMAIL_REGEX, email) is not None

    @staticmethod
    def validate_required_fields(fields):
        missing_fields = [field for field, value in fields.items() if not value]
        errors = {}

        if missing_fields:
            errors["missing_fields"] = f"Champs manquants : {', '.join(missing_fields)}."

        if "email" in fields and fields["email"] and not AnimalsService.is_valid_email(fields["email"]):
            errors["invalid_email"] = "Le format de l'email est invalide."

        if errors:
            return {
                "status": "error",
                "message": "; ".join(errors.values()),
                "fields": errors,
            }

        return {"status": "success"}

    @staticmethod
    def register_animal(nom, espece, race, age, description, email, adresse, ville, code_postal):
        try:
            data = {
                "nom": nom,
                "espece": espece,
                "race": race,
                "age": age,
                "description": description,
                "email": email,
                "adresse": adresse,
                "ville": ville,
                "code_postal": code_postal,
            }
            validation_result = AnimalsService.validate_required_fields(data)
            if validation_result["status"] == "error":
                return validation_result

            if Animals.find_by_email(email):
                logging.warning(f"Tentative d'enregistrement avec un email existant : {email}")
                return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["email_exists"]}

            Animals.create(**data)
            logging.info(f"Animal enregistré avec succès : {data}")
            return {"status": "success", "message": "Animal enregistré avec succès."}
        except Exception as e:
            logging.exception(f"Erreur lors de l'enregistrement de l'animal : {str(e)}")
            return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["internal_error"]}




    @staticmethod
    def get_animal_by_id(animal_id):
        """Récupère les détails d'un animal par son ID."""
        try:
            animal = Animals.find_by_id(animal_id)
            if animal:
                return {"status": "success", "data": animal}
            return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["not_found"]}
        except Exception:
            logging.error(f"Erreur lors de la récupération de l'animal ID {animal_id}")
            return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["internal_error"]}



    @staticmethod
    def update_animal(animal_id, form_data):
        """Met à jour les informations d'un animal."""
        try:
            # Valider les champs requis
            validation_result = AnimalsService.validate_required_fields(form_data)
            if validation_result["status"] == "error":
                return validation_result

            # Vérifier si l'email existe déjà dans la base de données
            existing_animal = Animals.find_by_email(form_data["email"])
            if existing_animal and existing_animal["id"] != animal_id:
                logging.warning(f"Email déjà utilisé par un autre animal : {form_data['email']}")
                return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["email_exists"]}

            # Mettre à jour les informations
            Animals.update(animal_id=animal_id, **form_data)
            return {"status": "success", "message": "Animal mis à jour avec succès."}
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de l'animal ID {animal_id}: {str(e)}")
            return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["internal_error"]}



    @staticmethod
    def delete_animal(animal_id):
        """Supprime un animal par son ID."""
        try:
            animal = Animals.find_by_id(animal_id)
            if not animal:
                return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["not_found"]}
            Animals.delete_by_id(animal_id)
            return {"status": "success", "message": "Animal supprimé avec succès."}
        except Exception:
            logging.error(f"Erreur lors de la suppression de l'animal ID {animal_id}")
            return {"status": "error", "message": AnimalsService.ERROR_MESSAGES["internal_error"]}



    @staticmethod
    def get_paginated_animals(page, per_page):
        """Récupère une liste paginée d'animaux."""
        try:
            animals = Animals.get_paginated_animals(page, per_page)
            return animals
        except Exception:
            logging.error("Erreur lors de la récupération des animaux paginés.")
            return []



    @staticmethod
    def search_paginated(query, page, per_page):
        """Recherche paginée des animaux par mot-clé."""
        try:
            animals = Animals.search_paginated(query, page, per_page)
            return animals
        except Exception:
            logging.error("Erreur lors de la recherche paginée.")
            return []



    @staticmethod
    def count_animals():
        """Compte le nombre total d'animaux."""
        try:
            return Animals.count_animals()
        except Exception:
            logging.error("Erreur lors du comptage des animaux.")
            return 0



    @staticmethod
    def count_search_results(query):
        """Compte le nombre total de résultats pour une recherche donnée."""
        try:
            return Animals.count_search_results(query)
        except Exception:
            logging.error("Erreur lors du comptage des résultats de recherche.")
            return 0
    
    
    @staticmethod
    def display_all():
        """Affiche tous les animaux."""
        try:
            animals = Animals.display_all()
            return animals
        except Exception:
            logging.error("Erreur lors de l'affichage de tous les animaux.")
            return []