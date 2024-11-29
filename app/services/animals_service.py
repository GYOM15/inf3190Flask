import re
import logging
from app.models import Animals

class AnimalsService:
    """
    Service pour gérer les opérations métier liées aux animaux.
    """
    EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"  # Regex pour valider les emails
    """
        Valide que tous les champs requis sont fournis.
    """
    @staticmethod
    def validate_required_fields(fields):
        
        missing_fields = [field for field, value in fields.items() if not value]
        if missing_fields:
            return {"status": "error", "message": f"Champs manquants : {', '.join(missing_fields)}.", "fields": missing_fields}
        return {"status": "success"}

    @staticmethod
    def register_animal(nom, espece, race, age, description, email, adresse, ville, code_postal):
        """
        Enregistre un nouvel animal après vérification.
        """
        try:
            # Champs requis
            required_fields = {
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

            # Validation des champs requis
            validation_result = AnimalsService.validate_required_fields(required_fields)
            if validation_result["status"] == "error":
                return validation_result

            # Validation de l'email
            if not re.match(AnimalsService.EMAIL_REGEX, email):
                return {"status": "error", "message": "L'email fourni n'est pas valide.", "field": "email"}

            # Vérification de l'existence d'un animal avec le même email
            if Animals.find_by_email(email):
                return {"status": "error", "message": "Un animal avec cet email existe déjà.", "field": "email"}

            # Création de l'animal
            Animals.create(
                nom=nom,
                espece=espece,
                race=race,
                age=age,
                description=description,
                email=email,
                adresse=adresse,
                ville=ville,
                code_postal=code_postal,
            )

            return {"status": "success", "message": "Animal enregistré avec succès."}

        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement de l'animal ({nom}, {email}): {e}")
            return {"status": "error", "message": "Une erreur interne s'est produite. Veuillez réessayer plus tard."}