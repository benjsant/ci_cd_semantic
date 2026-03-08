# Pipeline CI/CD

## Vue d'ensemble

La pipeline CI/CD est composée de 4 workflows GitHub Actions.

## Workflows

### CI (`ci.yml`)

Déclenché sur chaque push et pull request vers `main` ou `develop`.

**Jobs parallèles :**

| Job | Outils | Description |
|-----|--------|-------------|
| `lint` | Ruff | Vérification du style et formatage |
| `typecheck` | Mypy | Vérification des types |
| `security` | Bandit, Safety | Analyse de sécurité |
| `tests` | Pytest | Tests avec couverture |
| `pre-commit` | Pre-commit | Vérification des hooks |

### Build (`build.yml`)

Déclenché sur push vers `main`/`develop` et sur les tags `v*`.

- Build de l'image Docker (multi-stage)
- Push vers GitHub Container Registry (GHCR)
- Tags automatiques : branche, SHA, version sémantique

### Release (`release.yml`)

Déclenché après succès de la CI sur `main` ou `develop`.

- Analyse des commits depuis la dernière release
- Calcul automatique de la version (SemVer)
- Création du tag Git et de la GitHub Release
- Génération du CHANGELOG.md

### Sync Develop (`sync-develop.yml`)

Déclenché après chaque push sur `main`.

- Merge automatique de `main` dans `develop`
- Maintient `develop` synchronisé après les releases

## Stratégie de branches

```
main ──────────────────────────── production
  ↑                                  ↑
  └── develop ────── intégration     │
          ↑                          │
          └── feature/* ─────────────┘
```

## Conventional Commits

| Type | Version bump | Exemple |
|------|-------------|---------|
| `feat` | MINOR | `feat(items): add pagination` |
| `fix` | PATCH | `fix(api): handle null values` |
| `feat!` | MAJOR | `feat!: redesign API` |
| `docs`, `style`, `test`, `chore` | Aucun | - |
