# Veille Technologique — CI/CD, uv, Semantic Release & MkDocs

---

## Mission 1 : Comprendre CI/CD

### 1. Qu'est-ce que la CI (Continuous Integration) ?

La **Continuous Integration** est une pratique de développement où chaque développeur intègre son code dans un dépôt partagé **plusieurs fois par jour**. Chaque intégration est vérifiée automatiquement par un build et des tests, ce qui permet de détecter les problèmes rapidement.

#### Problèmes résolus par la CI

- **L'enfer des merges** : sans CI, les équipes travaillent en isolation longtemps, puis tentent de fusionner des branches divergentes — source de conflits massifs et de régressions.
- **"Ça marche sur ma machine"** : la CI exécute les tests dans un environnement neutre et standardisé, ce qui garantit que le code fonctionne indépendamment de l'environnement local.
- **Détection tardive des bugs** : sans CI, les bugs sont découverts en production. Avec CI, ils sont détectés à chaque commit.
- **Manque de visibilité** : la CI fournit un état en temps réel de la santé du code.

#### Principes clés

1. **Maintenir un dépôt unique** : tout le code source est centralisé dans un VCS (Git).
2. **Automatiser le build** : le projet doit pouvoir être compilé/installé par une seule commande.
3. **Automatiser les tests** : la suite de tests s'exécute à chaque commit sans intervention humaine.
4. **Commit fréquent** : chaque développeur intègre au moins une fois par jour.
5. **Build rapide** : le feedback doit être quasi-immédiat (< 10 minutes).
6. **Corriger les builds cassés en priorité** : un build rouge bloque tout.
7. **Environnement de test identique à la production** : pas de surprise lors du déploiement.

#### 3 exemples d'outils de CI

| Outil | Description |
|-------|-------------|
| **GitHub Actions** | CI/CD intégré à GitHub, basé sur des workflows YAML, gratuit pour les repos publics |
| **GitLab CI/CD** | Solution native GitLab, très puissante avec les pipelines `.gitlab-ci.yml` |
| **Jenkins** | Outil open-source auto-hébergé, très configurable via des plugins, utilisé en entreprise |

---

### 2. Qu'est-ce que le CD (Continuous Deployment / Delivery) ?

#### Continuous Delivery

Le **Continuous Delivery** assure que le code est **toujours dans un état déployable**. Chaque changement passe par le pipeline (tests, qualité, intégration) et peut être déployé en production **à tout moment** d'une simple pression d'un bouton.

> Le déploiement reste **manuel** — c'est un humain qui décide quand livrer.

#### Continuous Deployment

Le **Continuous Deployment** va plus loin : chaque commit qui passe tous les tests automatiques est **déployé automatiquement en production**, sans intervention humaine.

#### Différence clé

| | Continuous Delivery | Continuous Deployment |
|---|---|---|
| **Déploiement** | Manuel (décision humaine) | Automatique |
| **Fréquence** | À la demande | À chaque commit |
| **Confiance requise** | Haute | Très haute |
| **Cas d'usage** | Applis critiques, réglementées | SaaS, startups, web apps |

#### Risques et bénéfices

**Bénéfices :**
- Feedback ultra-rapide : les bugs sont découverts et corrigés en heures, pas en semaines
- Réduction du risque : les petits changements fréquents sont moins risqués que les grosses releases
- Satisfaction client : les nouvelles fonctionnalités arrivent plus vite
- Moins de stress : pas de "release day" stressant avec des centaines de changements

**Risques :**
- Nécessite une couverture de tests très élevée (sinon on déploie des bugs automatiquement)
- Infrastructure de monitoring obligatoire pour détecter les problèmes post-déploiement
- Culture d'équipe à faire évoluer (discipline sur les commits, conventions)
- Coût initial élevé pour mettre en place le pipeline complet

---

### 3. Pourquoi CI/CD est important ?

#### Impact sur la qualité du code

- Les outils de linting, formatage et analyse statique s'exécutent à chaque commit → le code dégradé est bloqué avant même la review
- Les tests de régression automatiques évitent de casser ce qui fonctionnait
- La couverture de code est mesurée et peut être imposée comme seuil minimum

#### Impact sur la vitesse de développement

- **Sans CI/CD** : un développeur peut attendre des jours avant de savoir si son code fonctionne en intégration
- **Avec CI/CD** : le feedback arrive en moins de 10 minutes → le développeur peut enchaîner
- Le temps de "context switching" est réduit : on corrige le bug pendant qu'on a encore le contexte en tête

#### Impact sur la collaboration en équipe

- Tout le monde a une visibilité sur l'état du projet (badge CI vert/rouge)
- Les conventions de commits (Conventional Commits) améliorent la lisibilité de l'historique
- Les PR reviews sont plus faciles car le CI a déjà filtré les problèmes évidents
- La documentation (CHANGELOG) est générée automatiquement à partir des commits

---

## Mission 2 : Maîtriser uv

### 1. Qu'est-ce que uv ?

**uv** est un gestionnaire de packages et d'environnements Python ultra-rapide, développé par [Astral](https://astral.sh/) (les créateurs de Ruff). Il est écrit en **Rust** et vise à remplacer pip, pip-tools, pipx, poetry, pyenv et virtualenv par un seul outil unifié.

#### Comparaison avec les alternatives

| Critère | pip | poetry | pipenv | uv |
|---------|-----|--------|--------|----|
| **Vitesse** | Lent | Moyen | Lent | **10-100x plus rapide** |
| **Lock file** | Non (pip-compile) | `poetry.lock` | `Pipfile.lock` | `uv.lock` |
| **Résolution deps** | Basic | SAT solver | SAT solver | **Résolution ultra-rapide** |
| **Gestion Python** | Non | Non | Non | **Oui (pyenv-like)** |
| **Standard pyproject.toml** | Oui | Partiel | Non | **Oui (PEP 517/518/621)** |
| **Environnements virtuels** | Manuel | Automatique | Automatique | **Automatique** |
| **Compatibilité pip** | - | Partielle | Partielle | **Totale** |

#### Avantages clés de uv

- **Vitesse** : installation des dépendances 10 à 100 fois plus rapide que pip grâce à la parallélisation et au cache agressif
- **Unique binaire** : un seul outil pour tout (gestion Python, venvs, packages, scripts)
- **Résolution déterministe** : le `uv.lock` garantit que tous les développeurs et la CI ont exactement les mêmes versions
- **Compatibilité** : utilise le standard `pyproject.toml` (PEP 621), compatible avec l'écosystème Python existant
- **Cache global** : les packages téléchargés sont partagés entre tous les projets → gain de temps énorme en CI

---

### 2. Comment uv fonctionne avec pyproject.toml ?

#### Structure du fichier

```toml
[project]
name = "mon-projet"
version = "1.0.0"
description = "Description du projet"
requires-python = ">=3.13"

# Dépendances de production
dependencies = [
    "fastapi[standard]>=0.121.0",
    "sqlmodel>=0.0.27",
]

[dependency-groups]
# Dépendances de développement (non installées en prod)
dev = [
    "pytest>=8.3.0",
    "ruff>=0.9.0",
    "mypy>=1.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### Gestion des dépendances par sections

- `[project].dependencies` : dépendances de **production**, installées par défaut
- `[dependency-groups].dev` : dépendances de **développement** uniquement
- `uv sync` → installe uniquement les dépendances de production
- `uv sync --all-groups` → installe tout (prod + dev)
- `uv add <package>` → ajoute une dépendance et met à jour `uv.lock`
- `uv add --dev <package>` → ajoute en groupe `dev`

#### Build backend

uv peut utiliser différents backends de build (hatchling, setuptools, flit...). Il agit comme **frontend** standardisé qui délègue la construction de la wheel au backend configuré dans `[build-system]`.

Pour un projet sans distribution de wheel (comme un service web), on peut désactiver le build :

```toml
[tool.semantic_release]
build_command = false
```

---

### 3. Comment utiliser uv dans GitHub Actions ?

#### Installation via l'action officielle

```yaml
- name: Set up uv
  uses: astral-sh/setup-uv@v4
  with:
    enable-cache: true                        # Active le cache GitHub Actions
    cache-dependency-glob: "uv.lock"         # Invalide le cache si uv.lock change
```

#### Cache des dépendances

Le cache est stocké dans le cache GitHub Actions et **partagé entre les runs**. Si `uv.lock` n'a pas changé, les dépendances ne sont pas re-téléchargées → gain de 30 à 60 secondes par job.

#### Exécution de commandes

```yaml
# Installer toutes les dépendances (prod + dev)
- run: uv sync --all-groups

# Lancer un outil
- run: uv run pytest
- run: uv run ruff check .
- run: uv run mypy app/

# Sans créer de venv (pour les scripts one-shot)
- run: uv run --no-sync python script.py
```

L'avantage de `uv run` est qu'il utilise automatiquement l'environnement virtuel du projet.

---

## Mission 3 : Comprendre Semantic Release

### 1. Qu'est-ce que le versionnage sémantique (SemVer) ?

Le **Semantic Versioning** (SemVer) est un système de versionnage sous la forme `MAJOR.MINOR.PATCH` défini sur [semver.org](https://semver.org/).

#### Format MAJOR.MINOR.PATCH

```
v2.4.1
│ │ └── PATCH : correction de bug rétrocompatible
│ └──── MINOR : nouvelle fonctionnalité rétrocompatible
└────── MAJOR : changement incompatible avec l'API précédente
```

#### Quand bumper chaque niveau ?

| Niveau | Quand ? | Exemple |
|--------|---------|---------|
| **PATCH** | Bug fix, correction sans impact sur l'API | `1.0.0` → `1.0.1` |
| **MINOR** | Nouvelle fonctionnalité, ajout rétrocompatible | `1.0.0` → `1.1.0` |
| **MAJOR** | Changement cassant (breaking change), suppression d'API | `1.0.0` → `2.0.0` |

> Règle : quand MINOR est bumped, PATCH revient à 0. Quand MAJOR est bumped, MINOR et PATCH reviennent à 0.

---

### 2. Qu'est-ce que Conventional Commits ?

**Conventional Commits** est une convention de messages de commit structurés qui permet l'automatisation du versionnage et de la génération de CHANGELOG.

#### Format des messages

```
<type>(<scope>): <description courte>

[corps optionnel - détails sur le changement]

[footer optionnel - références issues, BREAKING CHANGE]
```

#### Types de commits et impact sur le versionnage

| Type | Description | Version bump |
|------|-------------|-------------|
| `feat` | Nouvelle fonctionnalité | **MINOR** (0.1.0 → 0.2.0) |
| `fix` | Correction de bug | **PATCH** (0.1.0 → 0.1.1) |
| `perf` | Amélioration de performance | **PATCH** |
| `refactor` | Refactoring sans nouvelle feature ni fix | Aucun |
| `docs` | Documentation uniquement | Aucun |
| `style` | Formatage, whitespace, point-virgule | Aucun |
| `test` | Ajout ou modification de tests | Aucun |
| `chore` | Maintenance, mise à jour de dépendances | Aucun |
| `ci` | Modifications du pipeline CI/CD | Aucun |
| `build` | Système de build, dépendances externes | Aucun |

#### Breaking Changes → MAJOR bump

```bash
# Option 1 : avec le suffixe !
git commit -m "feat!: redesign complète de l'API REST"

# Option 2 : avec le footer BREAKING CHANGE
git commit -m "feat: nouvelle architecture API

BREAKING CHANGE: les endpoints /api/v1/* sont supprimés,
migrer vers /api/v2/*"
```

---

### 3. Comment python-semantic-release fonctionne ?

**python-semantic-release** est un outil qui automatise le versionnage en analysant les messages de commits depuis la dernière version taguée.

#### Flux de fonctionnement

```
1. Analyse les commits depuis le dernier tag Git
2. Détermine le type de bump (MAJOR / MINOR / PATCH)
3. Met à jour la version dans pyproject.toml
4. Génère / met à jour CHANGELOG.md
5. Crée un commit "chore(release): v1.2.0"
6. Crée un tag Git (ex: v1.2.0)
7. Pousse le commit et le tag sur le remote
8. Crée une GitHub Release avec les notes de release
```

#### Configuration dans pyproject.toml

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]  # Où bumper la version
branch = "main"
changelog_file = "CHANGELOG.md"
build_command = false  # Pas de wheel à publier

[tool.semantic_release.branches.main]
match = "main"
prerelease = false  # Releases stables

[tool.semantic_release.branches.develop]
match = "develop"
prerelease = true
prerelease_token = "rc"  # ex: v1.2.0-rc.1

[tool.semantic_release.changelog]
exclude_commit_patterns = ["^chore", "^ci", "^docs", "^style", "^test"]

[tool.semantic_release.commit_parser_options]
minor_tags = ["feat"]
patch_tags = ["fix", "perf"]

[tool.semantic_release.publish]
upload_to_vcs_release = true  # Crée une GitHub Release
```

#### Génération du CHANGELOG

Le CHANGELOG est généré automatiquement en regroupant les commits par type :

```markdown
## v1.2.0 (2025-03-08)

### Features
- feat(items): add pagination endpoint (#12)
- feat(api): add filtering by price (#14)

### Bug Fixes
- fix(database): fix connection pool leak (#11)
```

#### Utilisation dans GitHub Actions

```yaml
- name: Python Semantic Release
  uses: python-semantic-release/python-semantic-release@v9
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Mission 5 (Bonus) : MkDocs & GitHub Pages

### Comment MkDocs génère de la documentation ?

**MkDocs** est un générateur de documentation statique pour Python. Il convertit des fichiers **Markdown** en un site web HTML élégant.

Avec le plugin **mkdocstrings**, il extrait automatiquement les **docstrings** du code source Python et les intègre dans la documentation :

```markdown
# Dans docs/api/services.md
::: app.services.item_service.ItemService
    options:
      show_source: true
```

Cela génère automatiquement la documentation de la classe `ItemService` avec tous ses paramètres, types et descriptions.

### Comment déployer sur GitHub Pages ?

```bash
# En local
uv run mkdocs gh-deploy --force
```

Cette commande :
1. Build le site statique dans `site/`
2. Crée/met à jour la branche `gh-pages` avec le contenu généré
3. Push vers GitHub → GitHub Pages publie automatiquement

En CI avec GitHub Actions :
```yaml
- name: Build and deploy
  run: uv run mkdocs gh-deploy --force
```

Il faut activer GitHub Pages dans Settings → Pages → Source : branche `gh-pages`.

### Qu'est-ce que mkdocstrings ?

**mkdocstrings** est un plugin MkDocs qui permet de générer automatiquement la documentation API à partir des docstrings Python. Il supporte plusieurs handlers (Python, shell...) et plusieurs formats de docstrings (Google, NumPy, reStructuredText).

Configuration dans `mkdocs.yml` :

```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            docstring_style: google
```

Format Google des docstrings :

```python
def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    """Récupère une liste paginée d'articles.

    Args:
        db: Session de base de données active.
        skip: Nombre d'articles à ignorer.
        limit: Nombre maximum d'articles à retourner.

    Returns:
        Liste d'objets Item.

    Raises:
        DatabaseError: Si la connexion échoue.
    """
```
