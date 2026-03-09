# Comparatif des Outils — Choix pour le Projet CI/CD

---

## 1. Linters Python

Un **linter** analyse le code statiquement pour détecter les erreurs, les mauvaises pratiques et les problèmes de style sans exécuter le programme.

### Comparatif

| Outil | Langage | Vitesse | Règles disponibles | Config | Communauté | Note /10 | Choix ? |
|-------|---------|---------|-------------------|--------|------------|----------|---------|
| **Ruff** | Rust | ⚡ Très rapide (10-100x) | 800+ règles (remplace Flake8, isort, pyupgrade...) | `pyproject.toml` | En forte croissance | **9/10** | ✅ |
| **Flake8** | Python | Moyen | ~200 règles natives + plugins | `setup.cfg` / `.flake8` | Mature, largement adopté | 7/10 | ❌ |
| **Pylint** | Python | Lent | Très complète, analyse profonde | `pylintrc` | Très mature, verbeux | 6/10 | ❌ |

### Détail des outils

#### Ruff
- Écrit en **Rust** → performance incomparable (lint d'un projet entier en < 1 seconde)
- Remplace à lui seul : Flake8, isort, pyupgrade, pydocstyle, et 20+ autres plugins
- Intégration native avec `pyproject.toml`
- Auto-fix disponible (`ruff check --fix`)
- Utilisé par des projets majeurs : FastAPI, Pydantic, Airflow

#### Flake8
- Standard de l'industrie pendant des années
- Extensible via plugins (flake8-bugbear, flake8-comprehensions...)
- Plus lent que Ruff mais reste un bon choix pour les projets existants
- Ne gère pas le formatage (besoin de Black en complément)

#### Pylint
- L'outil le plus complet en termes d'analyse sémantique
- Détecte des erreurs que Ruff et Flake8 manquent (variables non utilisées, attributs manquants)
- Très lent sur de grands projets
- Taux de faux positifs élevé → configuration complexe pour les réduire

### Justification du choix : **Ruff**

Ruff offre le meilleur rapport qualité/vitesse/simplicité. Sa vitesse le rend idéal en CI et en pre-commit (feedback quasi-immédiat). Il consolide plusieurs outils en un seul, simplifiant la configuration.

---

## 2. Formatters Python

Un **formatter** reformate automatiquement le code pour garantir un style uniforme dans toute l'équipe.

### Comparatif

| Outil | Vitesse | Style | Customisation | Adoption | Note /10 | Choix ? |
|-------|---------|-------|---------------|----------|----------|---------|
| **Ruff format** | ⚡ Très rapide | Compatible Black | Minimale (intentionnel) | Croissante | **9/10** | ✅ |
| **Black** | Rapide | Opinionated, cohérent | Très limitée | Très large | 8/10 | ❌ |
| **autopep8** | Moyen | PEP 8 uniquement | Large | Déclinante | 5/10 | ❌ |

### Détail des outils

#### Ruff format
- Mêmes performances que Ruff linter (Rust)
- **Compatible Black** à 99.9% → migration sans douleur
- Avantage majeur : un seul outil pour linting ET formatage
- Moins de 6 options de configuration → cohérence garantie

#### Black
- Le formateur "opinionated" de référence : peu d'options, mais résultats cohérents
- "Le formateur qui ne négocie pas" → fin des débats de style en équipe
- Plus lent que Ruff mais reste rapide
- Adoption massive dans l'open source Python

#### autopep8
- Se limite à corriger les violations PEP 8
- Très permissif → chaque développeur peut avoir un style légèrement différent
- Ne résout pas les débats de style en équipe
- En déclin face à Black et Ruff

### Justification du choix : **Ruff format**

Puisqu'on utilise déjà Ruff pour le linting, utiliser Ruff format évite d'ajouter une dépendance supplémentaire. Compatible Black garantit que les équipes venant de Black n'ont pas de friction.

---

## 3. Type Checkers

Un **type checker** vérifie statiquement que les annotations de types Python sont cohérentes, sans exécuter le code.

### Comparatif

| Outil | Vitesse | Précision | Intégration IDE | Support Python | Note /10 | Choix ? |
|-------|---------|-----------|-----------------|----------------|----------|---------|
| **Mypy** | Moyen | Très haute | Bonne (via plugin) | Excellent | **8/10** | ✅ |
| **Pyright** | ⚡ Rapide | Très haute | Excellente (VS Code natif) | Excellent | 9/10 | ❌ |
| **Pyre** | Rapide | Haute | Basique | Partiel | 6/10 | ❌ |

### Détail des outils

#### Mypy
- La **référence absolue** du type checking Python, créé par les équipes de Python et Dropbox
- Support complet de toutes les fonctionnalités de typing Python (generics, protocols, TypeVar...)
- Plugins pour frameworks : SQLAlchemy, Django, FastAPI
- Légèrement lent sur les grands projets mais très précis
- Le standard de facto dans l'industrie

#### Pyright
- Développé par **Microsoft**, utilisé dans VS Code via Pylance
- Plus rapide que Mypy et aussi précis
- Excellent en mode "watch" (recheck à chaque modification)
- Moins de plugins tiers disponibles que Mypy
- Idéal si l'équipe est entièrement sur VS Code

#### Pyre
- Développé par **Facebook/Meta** pour Instagram (millions de lignes Python)
- Très rapide grâce à une architecture de serveur daemon
- Moins utilisé hors de Meta, écosystème de plugins limité
- Documentation moins complète que Mypy/Pyright

### Justification du choix : **Mypy**

Mypy est le standard de l'industrie avec le meilleur support de plugins (dont SQLAlchemy utilisé via SQLModel dans ce projet). La configuration `ignore_missing_imports = true` évite les faux positifs sur les dépendances sans stubs.

---

## 4. Frameworks de Tests

Un **framework de tests** fournit les outils pour écrire, organiser et exécuter des tests automatisés.

### Comparatif

| Outil | Facilité | Fixtures | Plugins | Assertions | Parallélisation | Note /10 | Choix ? |
|-------|----------|----------|---------|------------|-----------------|----------|---------|
| **pytest** | ⭐⭐⭐ Simple | Puissantes et flexibles | 1000+ plugins | Natives (assert) | Via pytest-xdist | **10/10** | ✅ |
| **unittest** | ⭐⭐ Verbeux | setUp/tearDown basiques | Limités | Méthodes dédiées | Limitée | 6/10 | ❌ |

### Détail des outils

#### pytest
- **Syntaxe minimale** : un simple `assert` suffit pour une assertion
- **Fixtures** : système de dépendances puissant et composable (`@pytest.fixture`)
- **Plugins** : pytest-cov (coverage), pytest-asyncio (async), pytest-xdist (parallèle), pytest-mock...
- **Paramétrage** : `@pytest.mark.parametrize` pour tester plusieurs cas facilement
- **Discovery automatique** : trouve les tests dans tous les fichiers `test_*.py`
- Adopté par FastAPI, Django, Pydantic et la quasi-totalité de l'écosystème Python

#### unittest
- **Standard library** : aucune installation nécessaire
- Héritage de JUnit (Java) → syntaxe orientée objet, plus verbeuse
- `self.assertEqual()`, `self.assertRaises()` → moins lisible que `assert`
- Fixtures limitées : `setUp`/`tearDown` au niveau classe uniquement
- Bien pour les projets sans dépendances externes, mais inférieur à pytest en pratique

### Justification du choix : **pytest**

pytest est le standard absolu de l'industrie Python. Sa syntaxe simple, ses fixtures composables et son écosystème de plugins en font l'outil incontournable. L'intégration avec pytest-cov pour la couverture de code est native et simple à configurer.

---

## 5. Security Scanners (Optionnel)

Les **scanners de sécurité** détectent les vulnérabilités dans le code et les dépendances.

### Comparatif

| Outil | Type d'analyse | Faux positifs | Coût | Intégration CI | Note /10 | Choix ? |
|-------|---------------|---------------|------|----------------|----------|---------|
| **Bandit** | Analyse statique du code | Moyen | Gratuit | Excellente | **8/10** | ✅ |
| **Safety** | Vulnérabilités des dépendances | Faible | Gratuit (limité) | Excellente | **8/10** | ✅ |
| **Snyk** | Code + deps + containers | Faible | Freemium | Bonne | 9/10 | ❌ |
| **Trivy** | Containers + IaC + deps | Faible | Gratuit | Excellente | 9/10 | ❌ |

### Détail des outils

#### Bandit
- Analyse le code Python à la recherche de **patterns de sécurité dangereux** : injections SQL, hashage faible (MD5/SHA1), secrets en dur, subprocess sans validation...
- Fonctionne en analyse statique → ne nécessite pas d'exécuter le code
- Niveaux de sévérité : LOW, MEDIUM, HIGH
- Utilisé avec `-ll` pour ignorer les LOW dans ce projet

#### Safety
- Vérifie les dépendances listées dans `uv.lock` contre la base de données **PyUp.io** des CVE Python
- Détecte les packages avec des vulnérabilités connues
- Version gratuite limitée en nombre de scans, version commerciale illimitée
- Utilisé avec `--continue-on-error` pour ne pas bloquer la CI sur des vulnérabilités non critiques

#### Snyk
- Solution commerciale très complète : code, dépendances, containers, IaC
- Interface web intuitive avec suggestions de correctifs
- Gratuit pour les repos publics, payant pour les privés
- Trop complexe pour un projet d'apprentissage

#### Trivy
- Scanner open-source de **Aqua Security** orienté containers
- Scanne les images Docker, les systèmes de fichiers, les dépôts Git
- Idéal pour valider la sécurité d'une image Docker avant de la pousser sur GHCR
- Peut être ajouté au workflow `build.yml` pour scanner l'image produite

### Justification des choix : **Bandit + Safety**

La combinaison Bandit (code) + Safety (dépendances) couvre les deux vecteurs d'attaque principaux à moindre coût. Ces deux outils sont légers, s'intègrent parfaitement en CI avec uv, et sont suffisants pour un projet de ce type.

---

## Tableau récapitulatif des choix

| Catégorie | Outil choisi | Alternative écartée | Raison du choix |
|-----------|-------------|--------------------|-----------------|
| **Linter** | Ruff | Flake8, Pylint | Vitesse, tout-en-un, pyproject.toml |
| **Formatter** | Ruff format | Black, autopep8 | Déjà inclus dans Ruff, compatible Black |
| **Type checker** | Mypy | Pyright, Pyre | Standard industrie, plugins SQLAlchemy/FastAPI |
| **Tests** | pytest | unittest | Syntaxe simple, fixtures, écosystème de plugins |
| **Sécurité code** | Bandit | Snyk, Trivy | Gratuit, léger, dédié Python |
| **Sécurité deps** | Safety | Snyk | Gratuit, intégration uv directe |
