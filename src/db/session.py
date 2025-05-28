from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..core.config import settings
from ..utils import logging  # Importer le module de journalisation

# Création de l'URL de connexion à partir des paramètres de configuration
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Pour SQLite, il est nécessaire d'activer le support des clés étrangères
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
    echo=settings.SQL_ECHO  # Activer l'écho SQL en fonction de la configuration
)

# Création de la classe SessionLocal pour les sessions de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de la classe de base pour les modèles déclaratifs
Base = declarative_base()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Ajoutez l'option SQL_ECHO à la configuration :
# src/core/config.py
class Settings(BaseSettings):
    # ...
    SQL_ECHO: bool = False  # Activer l'écho SQL pour le débogage
    # ...