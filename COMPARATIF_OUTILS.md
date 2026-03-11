# Comparatif des outils

Choix faits pour le projet.

---

## Linter

J'ai regardé **Ruff**, **Flake8** et **Pylint**.

Flake8 c'était la ref pendant longtemps, mais faut installer plein de plugins à côté (flake8-bugbear, isort...) et chacun a sa propre config. Pylint est plus poussé dans l'analyse mais il est lent et sort beaucoup de faux positifs, faut passer du temps à configurer pour que ce soit utilisable.

Ruff c'est écrit en Rust, c'est 10 à 100x plus rapide. Et il regroupe les règles de Flake8, isort, pyupgrade etc. Un seul outil, une seule config dans `pyproject.toml`. Y a pas photo.

**Choix : Ruff.** Rapide, tout en un, facile à configurer.

---

## Formateur

**Black** c'est le formateur "opinionated" qui a un peu standardisé le formatage Python. Tu configures quasi rien, il formate et c'est tout. Ca évite les débats de style en équipe.

**Ruff format** fait pareil et est compatible Black à 99%. Comme on utilise déjà Ruff pour le lint autant pas rajouter un outil.

**autopep8** corrige juste les violations PEP 8, c'est trop permissif du coup les devs peuvent quand même avoir des styles différents.

**Choix : Ruff format.** Déjà inclus avec Ruff, compatible Black.

---

## Vérificateur de types

**Mypy** c'est la ref pour le typage statique Python. Y a des plugins pour SQLAlchemy, Django etc.

**Pyright** c'est celui de Microsoft, intégré dans VS Code via Pylance. Plus rapide que Mypy mais moins de plugins.

**Pyre** c'est Meta, conçu pour du très gros projet. Peu utilisé en dehors.

**Choix : Mypy.** Le plugin SQLAlchemy est important vu qu'on utilise SQLModel (qui repose sur SQLAlchemy).

---

## Tests

**pytest** vs **unittest**.

unittest c'est dans la stdlib mais l'API est verbeuse (héritage JUnit de Java). Faut faire `self.assertEqual()` partout.

pytest tu fais juste `assert x == y`. Le système de fixtures est bien plus flexible et y a plein de plugins (coverage, async, parallélisation...).

**Choix : pytest.** C'est le standard, les tests sont plus lisibles.

---

## Sécurité

Deux aspects : le code et les dépendances.

**Bandit** scanne le code Python pour trouver des patterns dangereux (injections, secrets en dur, etc.).

**pip-audit** vérifie les dépendances contre les CVE connues.

**Snyk** et **Trivy** sont plus complets mais overkill pour ce projet. Snyk est payant pour les repos privés.

**Choix : Bandit + pip-audit.** Ca couvre l'essentiel sans compliquer la config.

---

## Récap

| Catégorie | Outil | Raison |
|-----------|-------|--------|
| Lint | Ruff | Rapide, tout-en-un |
| Format | Ruff format | Inclus, compatible Black |
| Types | Mypy | Plugin SQLAlchemy |
| Tests | pytest | Standard, fixtures composables |
| Sécu code | Bandit | Léger, dédié Python |
| Sécu deps | pip-audit | Vérifie les CVE |
