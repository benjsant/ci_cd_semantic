# Veille CI/CD

---

## La CI/CD c'est quoi

La CI c'est le fait d'intégrer son code régulièrement dans un dépôt partagé et de déclencher des vérifications automatiques à chaque push : tests, lint, sécurité. L'objectif c'est de trouver les bugs le plus tôt possible, pas lors d'un merge catastrophique trois semaines après.

Deux problèmes concrets que ça résout :
- "ça marchait sur ma machine" — la CI tourne dans un environnement neutre, pas celui du dev
- les merges qui partent en vrille — si tout le monde pousse souvent, les branches ne divergent pas pendant des semaines

Le CD c'est la suite : soit on est en *livraison continue* (le code est toujours prêt à partir en prod, mais c'est un humain qui décide), soit en *déploiement continu* (ça part automatiquement si les tests passent). La différence c'est surtout le niveau de confiance qu'on a dans sa couverture de tests.

Outils qu'on voit souvent : GitHub Actions (c'est ce qu'on utilise ici), GitLab CI, Jenkins (vieux mais encore très présent en entreprise).

L'avantage au quotidien : quand la CI casse, on sait exactement quel commit a tout cassé. On corrige dans la foulée plutôt que de chasser un bug introduit il y a deux semaines.

---

## uv

uv est un gestionnaire de paquets Python écrit en Rust, développé par Astral (les mêmes que Ruff). Il remplace pip, virtualenv et pip-tools en un seul binaire.

Le gros avantage c'est la vitesse. Sur une CI qui repart de zéro à chaque run, l'installation des dépendances avec pip peut prendre 2-3 minutes. Avec uv et le cache, c'est souvent sous les 10 secondes.

Il génère un `uv.lock` qui fige les versions exactes de tous les paquets — même principe que `poetry.lock`. Ça garantit que tout le monde installe exactement la même chose, dev comme CI.

Commandes utilisées dans ce projet :

```bash
uv sync               # installe les dépendances dans .venv/
uv sync --all-groups  # installe aussi les dépendances de dev
uv run pytest         # lance une commande dans le venv sans l'activer manuellement
uv add requests       # ajoute une dépendance et met à jour uv.lock
```

En CI, l'action `astral-sh/setup-uv@v4` gère le cache sur le contenu de `uv.lock` automatiquement.

Par rapport à poetry : uv s'appuie sur le format `pyproject.toml` standard (PEP 621) alors que poetry a son propre format de métadonnées. Et uv est nettement plus rapide.

---

## Versionnage sémantique

Le format c'est `MAJEUR.MINEUR.CORRECTIF` :

```
v2.4.1
  │ │ └── bug fix sans casser l'existant
  │ └──── nouvelle fonctionnalité rétrocompatible
  └────── changement cassant (l'API change)
```

Quand MINEUR monte, CORRECTIF repasse à 0. Quand MAJEUR monte, les deux repassent à 0.

### Commits conventionnels

C'est une convention de messages de commit pour permettre l'automatisation du versionnage :

```
<type>(<portée>): <description>
```

Ce qui fait évoluer la version :
- `feat:` → incrément MINEUR
- `fix:` ou `perf:` → incrément CORRECTIF
- `feat!:` ou `BREAKING CHANGE:` dans le pied de message → incrément MAJEUR

Le reste (`docs`, `chore`, `ci`, `test`, `refactor`...) ne change pas la version.

```bash
git commit -m "feat(items): add price filter"          # 0.1.0 → 0.2.0
git commit -m "fix(db): prevent connection pool leak"  # 0.2.0 → 0.2.1
git commit -m "feat!: redesign API response format"    # 0.2.1 → 1.0.0
```

### python-semantic-release

L'outil lit l'historique des commits depuis le dernier tag, calcule le prochain numéro de version, met à jour `pyproject.toml`, génère le `CHANGELOG.md`, crée le tag et publie une release GitHub. Tout ça sans intervention manuelle.

Dans ce projet : `main` → releases stables, `dev` → pré-releases avec suffixe `rc`. La config est dans `pyproject.toml` sous `[tool.semantic_release]`.

---

## MkDocs (bonus)

MkDocs convertit des fichiers Markdown en site statique. Avec le module `mkdocstrings`, il génère aussi la doc de l'API depuis les docstrings directement dans le code :

```markdown
::: app.services.item_service.ItemService
```

Le déploiement sur GitHub Pages se fait avec `mkdocs gh-deploy --force` — ça crée la branche `gh-pages` et GitHub Pages la publie. Dans ce projet c'est automatisé dans `docs.yml` à chaque push sur `main`.
