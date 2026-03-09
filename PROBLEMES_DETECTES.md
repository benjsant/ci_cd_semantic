# Problèmes détectés — Audit qualité

Audit réalisé avec `ruff check`, `mypy` et relecture manuelle du code.

---

## Formatage / Style

1. Imports non triés dans `app/schemas/__init__.py` (ruff I001)
2. Imports non triés dans `app/services/item_service.py` (ruff I001)
3. Imports non triés dans `tests/conftest.py` (ruff I001)
4. `Generator[Session, None, None]` dans `app/database.py` — arguments de type par défaut inutiles, `Generator[Session]` suffit (ruff UP043)
5. `README.md` vide — juste "A REMPLIR"

## Imports

6. `pytest` importé mais jamais utilisé dans `tests/test_items.py` (ruff F401)
7. `ItemResponse` importé dans `app/routes/items.py` sans être utilisé comme type de retour réel

## Types

8. `lifespan()` dans `app/main.py` — pas d'annotation de retour sur une fonction async generator (mypy no-untyped-def)
9. `get_items()` dans `app/routes/items.py` — annotée `-> list[ItemResponse]` mais retourne `list[Item]` (mypy return-value)
10. `get_item()` — même problème, annotée `-> ItemResponse` mais retourne `Item`
11. `create_item()` — même problème
12. `update_item()` — même problème
13. `get_db()` dans `app/database.py` — annotation `Generator[Session, None, None]` avec les arguments `None, None` qui sont les valeurs par défaut, inutile de les préciser

## Tests

14. `conftest.py` — `DATABASE_URL` forcée en PostgreSQL (localhost:5432) alors que les tests sont censés tourner en mémoire sans dépendance externe
15. Du coup les tests cassent si PostgreSQL n'est pas lancé localement — impossible d'utiliser `uv run pytest` directement
16. La fixture `session_fixture` crée l'engine avec l'URL PostgreSQL au lieu de SQLite en mémoire, ce qui contredit le commentaire "en mémoire pour les tests"

## Sécurité

17. `conftest.py` ligne 9 — credentials PostgreSQL en clair dans le code (`postgres:postgres`) même si c'est pour les tests
18. `.env.example` présent mais pas de vérification que `.env` n'est pas commité (pas de `.secrets.baseline`)
19. Pas de scan de secrets automatisé configuré (pas de `detect-secrets` dans pre-commit)

## Documentation

20. Aucune docstring sur `root()` et `health()` dans `app/main.py`
21. Pas de docstring sur la fixture `client_fixture` dans `conftest.py` (la fixture `session_fixture` en a une mais pas `client_fixture`)
22. `app/database.py` — `get_db()` n'a pas de docstring expliquant que c'est un générateur pour la dependency injection FastAPI

## Qualité générale

23. `app/routes/items.py` — les fonctions de route utilisent `Depends()` dans les arguments par défaut, ce que ruff B008 considère comme une mauvaise pratique (même si c'est le pattern officiel FastAPI)
24. Pas de `CHANGELOG.md` — aucune release n'a été faite
25. Branche `dev` non pushée sur le remote au moment de l'audit

---

## Corrections appliquées

| # | Problème | Corrigé ? | Moyen |
|---|----------|-----------|-------|
| 1-3 | Imports non triés | ✅ | `ruff check --fix` |
| 4 | UP043 database.py | ✅ | `ruff check --fix` |
| 6 | pytest inutilisé | ✅ | `ruff check --fix` |
| 8 | lifespan sans type retour | ✅ | Manuel |
| 9-12 | Return type Item vs ItemResponse | ✅ | Manuel |
| 14-16 | Conftest PostgreSQL → SQLite | ✅ | Manuel |
| 23 | B008 Depends() | ✅ | Ignoré via `pyproject.toml` (pattern FastAPI valide) |
| 19 | Pas de detect-secrets | ❌ | Non fait (optionnel) |
| 20-22 | Docstrings manquantes | ❌ | Partiel |
