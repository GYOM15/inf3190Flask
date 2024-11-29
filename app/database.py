# Gestion de la connexion à la base de données
import sqlite3
from flask import g
import logging

"""

    Références : https://flask.palletsprojects.com/en/stable/patterns/sqlite3/

"""
class Database:

    DATABASE = 'database.db'

    @staticmethod
    def get_connection():
        """
        Retourne une connexion SQLite stockée dans Flask's g pour la requête courante.
        """
        if 'db' not in g:
            g.db = sqlite3.connect(Database.DATABASE)
            g.db.row_factory = sqlite3.Row
        return g.db


    """
    Ferme la connexion SQLite à la fin de la requête.
    """
    @staticmethod
    def close_connection():
 
        db = g.pop('db', None)
        if db is not None:
            db.close()


    """
    Vérifie si une table existe dans la base de données.
    """
    @staticmethod
    def table_exists(table_name):
        try:
            db = Database.get_connection()
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Erreur lors de la vérification de la table {table_name}: {e}")
            return False
        finally:
            Database.close_connection()
    
    
    """
    Initialise les tables nécessaires uniquement si elles n'existent pas.
    """
    @staticmethod
    def initialize_tables():

        if not Database.table_exists("animals"):  # Vérifie si la table existe
            try:
                db = Database.get_connection()
                cursor = db.cursor()
                cursor.execute("""
                CREATE TABLE animals (
                    id INTEGER PRIMARY KEY,
                    nom VARCHAR(25) NOT NULL,
                    espece VARCHAR(25) NOT NULL,
                    race VARCHAR(25) NOT NULL,
                    age INTEGER NOT NULL,
                    description VARCHAR(500),
                    email VARCHAR(80) NOT NULL UNIQUE,
                    adresse VARCHAR(75) NOT NULL,
                    ville VARCHAR(75) NOT NULL,
                    cp VARCHAR(7) NOT NULL
                )
                """)
                db.commit()
                logging.info("Table 'animals' créée avec succès.")
            except sqlite3.Error as e:
                logging.error(f"Erreur lors de la création de la table 'animals': {e}")
            finally:
                Database.close_connection()
        else:
            logging.info("La table 'animals' existe déjà. Aucune action nécessaire.")