# Démarrage

## Prérequis

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL 16+ (ou Docker)

## Installation

```bash
# Installer uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Synchroniser les dépendances
uv sync

# Copier les variables d'environnement
cp .env.example .env
```

## Lancer avec Docker Compose

```bash
docker-compose up
```

## Lancer en local

```bash
# Démarrer PostgreSQL
docker-compose up db -d

# Lancer l'API
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/items_db \
  uv run fastapi dev app/main.py
```

## Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# Créer un article
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"nom": "Laptop", "prix": 999.99}'

# Lister les articles
curl http://localhost:8000/items/
```

Documentation interactive disponible sur : `http://localhost:8000/docs`
