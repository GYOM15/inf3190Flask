from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    DATABASE = os.getenv("DATABASE", "database.db")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"