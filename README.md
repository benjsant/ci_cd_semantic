# items-ci-cd

API REST CRUD en FastAPI avec PostgreSQL, mise en place dans le cadre d'un projet CI/CD complet.

![CI](https://github.com/drawile/ci_cd_semantic/workflows/CI/badge.svg)
![Build](https://github.com/drawile/ci_cd_semantic/workflows/Build%20%26%20Push%20Docker%20Image/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

---

## Stack

- **Python 3.13** + **FastAPI**
- **PostgreSQL** via SQLModel / SQLAlchemy
- **uv** pour la gestion des dépendances
- **Docker** + **GitHub Container Registry**
- **GitHub Actions** pour la CI/CD
- **python-semantic-release** pour le versionnage automatique

## Lancer le projet

```bash
# Dépendances
uv sync

# Avec Docker Compose (API + PostgreSQL)
docker compose up -d

# En local (nécessite une DB PostgreSQL active)
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/items_db
uv run fastapi dev app/main.py
```

L'API est accessible sur `http://localhost:8000`.
La doc Swagger est sur `http://localhost:8000/docs`.

## Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/health` | Health check |
| GET | `/items/` | Liste des items (pagination : `skip`, `limit`) |
| GET | `/items/{id}` | Récupérer un item |
| POST | `/items/` | Créer un item |
| PUT | `/items/{id}` | Modifier un item |
| DELETE | `/items/{id}` | Supprimer un item |

## Tests

```bash
uv run pytest -v
```

Les tests utilisent SQLite en mémoire, aucune dépendance externe nécessaire.
Couverture actuelle : **97%**.

## Qualité du code

```bash
uv run ruff check .       # linting
uv run ruff format .      # formatage
uv run mypy app/          # types
uv run bandit -r app/ -ll # sécurité
```

Les mêmes checks s'exécutent automatiquement à chaque push via GitHub Actions.

## Workflow Git

- `main` → production, releases stables
- `dev` → intégration, prereleases (`rc`)
- Feature branches → `feature/nom`, PR vers `dev`

Les commits suivent la convention [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/).
Le versionnage est automatique à chaque merge dans `main`.

## Structure

```
app/
├── main.py          # point d'entrée FastAPI
├── database.py      # config SQLModel + session
├── models/          # modèles SQLModel (table=True)
├── schemas/         # schémas Pydantic (entrée/sortie API)
├── services/        # logique métier
└── routes/          # endpoints FastAPI
tests/
├── conftest.py      # fixtures pytest
└── test_items.py    # tests des endpoints
```
