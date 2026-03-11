# Veille CI/CD

---

## La CI/CD c'est quoi

En gros la CI (intégration continue) c'est le fait de pousser son code souvent sur un dépôt partagé et qu'à chaque push des vérifs se lancent automatiquement : tests, lint, sécurité etc. Le but c'est de choper les bugs tout de suite, pas 3 semaines après quand on merge et que tout pète.

Ca résout deux trucs principaux :
- le fameux "ça marchait sur ma machine" vu que la CI tourne sur un serveur neutre
- les gros merges galère parce que si tout le monde pousse souvent les branches divergent pas trop

Le CD c'est la suite logique. Y a deux variantes :
- **Continuous Delivery** = le code est prêt à partir en prod mais un humain valide avant
- **Continuous Deployment** = si les tests passent ça part en prod direct, tout seul

La diff c'est le niveau de confiance dans les tests en fait. Si on a une bonne couverture on peut se permettre le déploiement auto.

Comme outils y a GitHub Actions (c'est ce qu'on utilise), GitLab CI, Jenkins (un peu vieux mais encore beaucoup utilisé en boite), CircleCI...

Le truc bien c'est que quand la CI pète, on sait direct quel commit a cassé. Pas besoin de chercher pendant des heures.

---

## uv

uv c'est un gestionnaire de paquets Python fait en Rust par Astral (ceux qui font Ruff). Ca remplace pip, virtualenv et pip-tools en un seul outil.

Le truc c'est que c'est hyper rapide. En CI ou pip peut mettre 2-3 min pour installer les deps, uv le fait en quelques secondes grâce au cache. C'est pas négligeable quand la CI tourne à chaque push.

Il génère un fichier `uv.lock` qui fige les versions exactes, un peu comme `poetry.lock`. Comme ça tout le monde a les mêmes versions, que ce soit en dev ou en CI.

Les commandes que j'utilise :

```bash
uv sync               # install les deps
uv sync --all-groups  # avec les deps de dev aussi
uv run pytest         # lance une commande dans le venv
uv add requests       # ajoute un paquet
```

En CI on utilise `astral-sh/setup-uv@v4` qui gère le cache automatiquement avec `uv.lock`.

Comparé à poetry : uv utilise le `pyproject.toml` standard (PEP 621) alors que poetry a son propre format. Et c'est beaucoup plus rapide.

---

## Versionnage sémantique

Le format c'est `MAJEUR.MINEUR.CORRECTIF` :

```
v2.4.1
  │ │ └── fix sans casser l'existant
  │ └──── nouvelle feature rétrocompatible
  └────── changement cassant
```

Quand MINEUR monte, CORRECTIF repasse à 0. Pareil pour MAJEUR.

### Conventional Commits

C'est une convention pour les messages de commit qui permet d'automatiser le versionnage :

```
<type>(<scope>): <description>
```

Ce qui change la version :
- `feat:` → bump MINEUR
- `fix:` ou `perf:` → bump CORRECTIF
- `feat!:` ou footer `BREAKING CHANGE:` → bump MAJEUR

Les autres (`docs`, `chore`, `ci`, `test`...) changent pas la version.

```bash
git commit -m "feat(items): add price filter"          # 0.1.0 → 0.2.0
git commit -m "fix(db): prevent connection pool leak"  # 0.2.0 → 0.2.1
git commit -m "feat!: redesign API response format"    # 0.2.1 → 1.0.0
```

### python-semantic-release

L'outil lit l'historique des commits depuis le dernier tag, calcule la prochaine version, met à jour `pyproject.toml`, génère le `CHANGELOG.md`, crée le tag et la release GitHub. Tout automatique.

Config dans `pyproject.toml` sous `[tool.semantic_release]`. `main` fait des releases stables, `dev` des pré-releases avec le suffixe `rc`.

---

## MkDocs (bonus)

MkDocs transforme des fichiers Markdown en site web. Avec `mkdocstrings` ça génère aussi la doc API depuis les docstrings du code Python :

```markdown
::: app.services.item_service.ItemService
```

Le déploiement sur GitHub Pages se fait avec `mkdocs gh-deploy --force`, ça crée une branche `gh-pages` que GitHub publie. C'est automatisé dans le workflow `docs.yml`.
