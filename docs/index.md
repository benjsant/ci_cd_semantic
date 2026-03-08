# Items API

Bienvenue sur la documentation de l'**Items CRUD API**.

## Description

API REST pour la gestion d'articles, construite avec **FastAPI**, **SQLModel** et **PostgreSQL**.

## Fonctionnalités

- ✅ CRUD complet sur les articles
- ✅ Validation des données avec Pydantic
- ✅ Base de données PostgreSQL
- ✅ Documentation interactive (Swagger UI)
- ✅ Pipeline CI/CD complète

## Installation rapide

```bash
# Cloner le projet
git clone https://github.com/votre-username/training-ci-cd-semantic-release
cd training-ci-cd-semantic-release

# Installer les dépendances
uv sync

# Lancer avec Docker
docker-compose up
```

## Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/items` | Lister les articles |
| `POST` | `/items` | Créer un article |
| `GET` | `/items/{id}` | Récupérer un article |
| `PUT` | `/items/{id}` | Mettre à jour un article |
| `DELETE` | `/items/{id}` | Supprimer un article |
| `GET` | `/health` | Health check |
