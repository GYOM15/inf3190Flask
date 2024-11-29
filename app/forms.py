import re

class RegistrationForm:
    def __init__(self, nom: str, espece: str, race: str, age: int, description: str,
                 email: str, adresse: str, ville: str, code_postal: str):
        self.nom = nom
        self.espece = espece
        self.race = race
        self.age = age
        self.description = description
        self.email = email
        self.adresse = adresse
        self.ville = ville
        self.code_postal = code_postal
        self.errors = {}

    """Retourne un booleen en fonction de la taille du tableau d'erreurs"""
    def validate(self) -> bool:
        self.errors.clear()  # Réinitialise les erreurs avant une nouvelle validation

        # Validation des champs requis
        self.validate_presence("nom", self.nom, 25)
        self.validate_presence("espece", self.espece, 25)
        self.validate_presence("race", self.race, 25)
        self.validate_presence("description", self.description, 500)
        self.validate_presence("adresse", self.adresse, 75)
        self.validate_presence("ville", self.ville, 75)
        
        # Validation spécifique
        self.validate_age()
        self.validate_email()
        self.validate_postal_code()

        return len(self.errors) == 0

    """Nous vérifions qu'un champ est présent et respecte une longueur maximale."""
    def validate_presence(self, field: str, value: str, max_length: int = None):
        if not value:
            self.errors[field] = f"{field.capitalize()} est requis."
        elif max_length and len(value) > max_length:
            self.errors[field] = f"{field.capitalize()} ne doit pas dépasser {max_length} caractères."

    """Nous vérifions que l'email est valide."""
    def validate_email(self):
        if not self.email:
            self.errors["email"] = "L'email est requis."
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.errors["email"] = "Le format de l'email est invalide."
    
    """Nous vérifions que l'âge est un entier positif."""
    def validate_age(self):
        if self.age is None:
            self.errors["age"] = "L'âge est requis."
        elif not isinstance(self.age, int):
            self.errors["age"] = "L'âge doit être un entier."
        elif self.age < 0:
            self.errors["age"] = "L'âge doit être un entier positif."
      
    """Nous vérifions que le code postal est valide (exemple : 5 chiffres)."""
    def validate_postal_code(self):
        if not self.code_postal:
            self.errors["code_postal"] = "Le code postal est requis."
        elif not re.match(r"^\d{5}$", self.code_postal):
            self.errors["code_postal"] = "Le code postal doit contenir 5 chiffres."