from app.database import Database
import logging

class Animals:
    """
    Classe pour gérer les opérations liées aux animaux dans la base de données.
    """
    def __init__(self, id, nom, espece, race, age, description, email, adresse, ville, code_postal):
        self.id = id
        self.nom = nom
        self.espece = espece
        self.race = race
        self.age = age
        self.description = description
        self.email = email
        self.adresse = adresse
        self.ville = ville
        self.code_postal = code_postal


    """
        Méthode statique pour ajouter un nouvel animal dans la base de données.
    """
    @staticmethod
    def create(nom, espece, race, age, description, email, adresse, ville, code_postal):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            query = """
            INSERT INTO animals (nom, espece, race, age, description, email, adresse, ville, code_postal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (nom, espece, race, age, description, email, adresse, ville, code_postal)
            logging.debug(f"Executing query: {query} with params: {params}")
            cursor.execute(query, params)
            db.commit()
            logging.info("Animal ajouté avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout : {e}")
        finally:
            cursor.close()

    

    """
        Méthode statique pour rechercher un animal par son email.
        Retourne l'animal si trouvé, sinon None.
    """
    @staticmethod
    def find_by_email(email):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM animals WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return dict(row)  # Retourne un dictionnaire au lieu d'une instance ou None
            return None
        except Exception as e:
            logging.error (f"Erreur lors de la recherche : {e}")
            return {"error": f"Erreur lors de la recherche : {e}"}
        finally:
            cursor.close()


    """Retrouver un animal par son id"""
    @staticmethod
    def find_by_id(animal_id):
        """
        Récupère un animal par son ID.
        """
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM animals WHERE id = ?", (animal_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)  # Convertir la ligne en dictionnaire
            return None
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'animal avec ID {animal_id} : {e}")
            return None
        finally:
            cursor.close()


    """
        Méthode statique pour récupérer tous les animaux dans la base de données
        et les afficher dans la console. Retourne aussi les données.
    """
    @staticmethod
    def display_all():
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM animals")
            recovery = cursor.fetchall()
            # Retourner les données sous forme de liste de dictionnaires
            return [dict(row) for row in recovery]
        except Exception as e:
            logging.error(f"Erreur lors de l'affichage : {e}")
            return []
        finally:
            cursor.close()
    
    """
        Méthode statique pour supprimer un animal par son ID.
    """
    @staticmethod
    def delete_by_id(animal_id):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
            db.commit()
            if cursor.rowcount > 0:
                logging.error(f"Animal avec ID {animal_id} supprimé avec succès.")
            else:
                logging.error(f"Aucun animal trouvé avec l'ID {animal_id}.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression : {e}")
        finally:
            cursor.close()


    """
        Méthode statique pour mettre à jour les informations d'un animal.
    """
    @staticmethod
    def update(animal_id, nom, espece, race, age, description, email, adresse, ville, code_postal):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                UPDATE animals
                SET nom = ?, espece = ?, race = ?, age = ?, description = ?, email = ?, adresse = ?, ville = ?, code_postal = ?
                WHERE id = ?
                """,
                (nom, espece, race, age, description, email, adresse, ville, code_postal, animal_id)
            )
            db.commit()
            if cursor.rowcount > 0:
                logging.error(f"Animal avec ID {animal_id} mis à jour avec succès.")
            else:
                logging.error(f"Aucun animal trouvé avec l'ID {animal_id}.")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour : {e}")
        finally:
            cursor.close()
        
    
    """
        Compte le nombre total d'animaux dans la base de données.
    """
    @staticmethod
    def count_animals():
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS count FROM animals")
            result = cursor.fetchone()
            return result["count"]
        except Exception as e:
            logging.error(f"Erreur lors du comptage des animaux : {e}")
            return 0
        finally:
            cursor.close()
    
    
    """
        Récupère une liste d'animaux avec pagination.
    """
    @staticmethod
    def get_paginated_animals(page, per_page):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            offset = (page - 1) * per_page  # Calcul du décalage
            cursor.execute("SELECT * FROM animals LIMIT ? OFFSET ?", (per_page, offset))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des animaux paginés : {e}")
            return []
        finally:
            cursor.close()
            
    
    """
        Recherche des animaux avec pagination en fonction d'un mot-clé.
    """
    @staticmethod
    def search_paginated(query, page, per_page):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            search_query = f"%{query}%"
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT * FROM animals
                WHERE nom LIKE ?
                OR espece LIKE ?
                OR email LIKE ?
                OR description LIKE ?
                LIMIT ? OFFSET ?
            """, (search_query, search_query, search_query, search_query, per_page, offset))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Erreur lors de la recherche paginée : {e}")
            return []
        finally:
            cursor.close()
            
    
    """
        Compte le nombre total de résultats pour une recherche donnée.
    """
    @staticmethod
    def count_search_results(query):
        db = Database.get_connection()
        cursor = db.cursor()
        try:
            search_query = f"%{query}%"
            cursor.execute("""
                SELECT COUNT(*) AS count FROM animals
                WHERE nom LIKE ?
                OR espece LIKE ?
                OR email LIKE ?
                OR description LIKE ?
                OR race LIKE ?
            """, (search_query, search_query, search_query, search_query, search_query))
            result = cursor.fetchone()
            return result["count"]
        except Exception as e:
            logging.error(f"Erreur lors du comptage des résultats : {e}")
            return 0
        finally:
            cursor.close()