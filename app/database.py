"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données PostgreSQL
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

import os
from collections.abc import Generator

from sqlmodel import Session, create_engine

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
