# Comparatif des outils

Choix effectués pour ce projet avec justifications.

---

## Analyseur de code (linter)

Trois outils principaux existent : **Ruff**, **Flake8** et **Pylint**.

Flake8 a longtemps été la référence — il est extensible via des modules complémentaires (flake8-bugbear, isort...) mais ça implique de gérer plusieurs outils et fichiers de configuration séparés. Pylint est plus complet dans son analyse sémantique mais il est lent et génère beaucoup de faux positifs, ce qui nécessite une configuration longue pour être utilisable.

Ruff est écrit en Rust et tourne 10 à 100x plus vite que les deux autres. Il regroupe à lui seul les règles de Flake8, isort, pyupgrade et d'autres. Un seul outil, un seul fichier de configuration dans `pyproject.toml`.

**Choix : Ruff.** La vitesse est déterminante en pré-commit et en CI. Le fait de remplacer plusieurs outils par un seul simplifie aussi la maintenance.

---

## Formateur de code

**Black** est devenu le standard depuis quelques années — son principe "le formateur qui ne négocie pas" a mis fin aux débats de style en équipe. Le résultat est cohérent même si on n'a presque aucune option de configuration.

**Ruff format** fait la même chose avec les mêmes performances que le linter Ruff, et est compatible à 99% avec Black.

**autopep8** ne fait que corriger les violations PEP 8, ce qui laisse trop de marge pour des styles différents entre développeurs. Il est en perte de vitesse.

**Choix : Ruff format.** Puisqu'on utilise déjà Ruff pour l'analyse, ajouter Black serait redondant. La compatibilité avec Black garantit qu'une équipe habituée à Black ne verra pas de différence.

---

## Vérificateur de types

**Mypy** est la référence historique du typage statique en Python. Il a le meilleur support de modules complémentaires pour les frameworks (SQLAlchemy, Django, FastAPI) et gère toutes les fonctionnalités du module `typing`.

**Pyright** est développé par Microsoft et est intégré dans VS Code via Pylance. Il est plus rapide que Mypy et tout aussi précis, mais son écosystème de modules complémentaires est moins développé.

**Pyre** vient de Meta, conçu pour de très grandes bases de code. Il est peu utilisé en dehors de Meta et sa documentation est plus limitée.

**Choix : Mypy.** Le support du module complémentaire SQLAlchemy est important ici puisque SQLModel repose dessus. La configuration `ignore_missing_imports = true` évite les faux positifs sur les dépendances sans annotations de types.

---

## Cadre de tests

Le choix se pose entre **pytest** et **unittest** (bibliothèque standard).

unittest existe depuis Python 2, son API est calquée sur JUnit (Java) — ça donne des tests verbeux avec `self.assertEqual()`, `self.assertIsNone()`, etc. Les accessoires de test (`setUp`/`tearDown`) sont limités au niveau de la classe.

pytest permet d'écrire `assert x == y` directement, utilise un système d'accessoires de test composables et hiérarchiques (`@pytest.fixture`), et dispose de plus d'un millier de modules complémentaires (couverture, tests asynchrones, parallélisation...).

**Choix : pytest.** C'est le standard actuel dans l'écosystème Python. La lisibilité des tests est bien meilleure et les accessoires de test permettent d'organiser les dépendances proprement (voir `conftest.py`).

---

## Analyse de sécurité

Deux angles : le code source et les dépendances.

**Bandit** analyse le code Python à la recherche de patterns dangereux : injections, algorithmes de hachage faibles, secrets en dur, appels système non contrôlés. C'est un outil léger dédié Python.

**Safety** vérifie les dépendances déclarées dans `uv.lock` contre une base de données de vulnérabilités connues (CVE). L'option `--continue-on-error` évite de bloquer la CI sur des vulnérabilités non critiques.

**Snyk** et **Trivy** sont plus complets (conteneurs, infrastructure...) mais surdimensionnés pour ce projet. Snyk est payant pour les dépôts privés.

**Choix : Bandit + Safety.** Les deux couvrent les vecteurs d'attaque principaux sans alourdir la configuration. Trivy pourrait être ajouté au pipeline de construction d'image Docker pour les projets qui en ont besoin.

---

## Récapitulatif

| Catégorie | Outil retenu | Principale raison |
|-----------|-------------|-------------------|
| Analyse de code | Ruff | Vitesse, tout-en-un |
| Formatage | Ruff format | Déjà inclus, compatible Black |
| Typage statique | Mypy | Module complémentaire SQLAlchemy |
| Tests | pytest | Standard actuel, accessoires composables |
| Sécurité code | Bandit | Dédié Python, léger |
| Sécurité dépendances | Safety | Vérifie le fichier de verrouillage |
