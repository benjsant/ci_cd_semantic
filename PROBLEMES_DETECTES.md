# Problèmes détectés

Audit fait avec `ruff check`, `mypy` et en relisant le code manuellement.

---

## Formatage / Style

1. Imports pas triés dans `app/schemas/__init__.py` (ruff I001)
2. Imports pas triés dans `app/services/item_service.py` (ruff I001)
3. Imports pas triés dans `tests/conftest.py` (ruff I001)
4. `Generator[Session, None, None]` dans `app/database.py` — les deux `None` sont inutiles, `Generator[Session]` suffit (ruff UP043)
5. `README.md` vide, juste "A REMPLIR"

## Imports

6. `pytest` importé mais jamais utilisé dans `tests/test_items.py` (ruff F401)
7. `ItemResponse` importé dans `app/routes/items.py` sans être vraiment utilisé en retour

## Types

8. `lifespan()` dans `app/main.py` — pas d'annotation de retour (mypy)
9. `get_items()` dans `app/routes/items.py` — annotée `-> list[ItemResponse]` mais retourne `list[Item]`
10. `get_item()` — pareil, `-> ItemResponse` mais retourne `Item`
11. `create_item()` — pareil
12. `update_item()` — pareil
13. `get_db()` dans `app/database.py` — `Generator[Session, None, None]` avec les None inutiles

## Tests

14. `conftest.py` force `DATABASE_URL` en PostgreSQL (localhost:5432) alors que les tests tournent en SQLite mémoire
15. Du coup les tests cassent si PostgreSQL est pas lancé
16. La fixture `session_fixture` crée l'engine SQLite mais le module importe quand même avec l'URL PostgreSQL

## Sécurité

17. `conftest.py` — credentials PostgreSQL en clair (`postgres:postgres`) même si c'est pour les tests
18. `.env.example` présent mais pas de vérif que `.env` est bien gitignored
19. Pas de scan de secrets automatisé (pas de detect-secrets)

## Documentation

20. Pas de docstring sur `root()` et `health()` dans `app/main.py`
21. Pas de docstring sur `client_fixture` dans `conftest.py`
22. `get_db()` dans `app/database.py` pas documentée

## Qualité

23. `app/routes/items.py` — `Depends()` dans les args par défaut, ruff B008 flag ça (mais c'est le pattern FastAPI standard)
24. Pas de `CHANGELOG.md` — aucune release faite encore
25. Branche `dev` pas pushée sur le remote au moment de l'audit

---

## Corrections appliquées

| # | Problème | Corrigé ? | Comment |
|---|----------|-----------|---------|
| 1-3 | Imports pas triés | oui | `ruff check --fix` |
| 4 | UP043 database.py | oui | `ruff check --fix` |
| 6 | pytest inutilisé | oui | `ruff check --fix` |
| 8 | lifespan sans type retour | oui | ajouté manuellement |
| 9-12 | Return type Item vs ItemResponse | oui | corrigé manuellement |
| 14-16 | Conftest PostgreSQL vs SQLite | oui | refait le conftest |
| 23 | B008 Depends() | oui | ignoré dans pyproject.toml (pattern FastAPI) |
| 19 | Pas de detect-secrets | non | optionnel |
| 20-22 | Docstrings manquantes | partiel | |
