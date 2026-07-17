# Kabulhaden CMS — Git Workflow & Branching Strategy

Git conventions, branching model, and collaboration workflow.

---

## Table of Contents

1. [Branching Model](#branching-model)
2. [Branch Naming](#branch-naming)
3. [Commit Conventions](#commit-conventions)
4. [Pull Request Process](#pull-request-process)
5. [Release Process](#release-process)
6. [Hotfix Process](#hotfix-process)

---

## Branching Model

```
main (production)
 │
 ├── develop (staging)
 │    │
 │    ├── feature/user-management
 │    ├── feature/radio-enhancements
 │    └── feature/news-cms
 │
 ├── hotfix/critical-auth-fix
 │
 └── release/v1.2.0
```

### Branch Types

| Branch | Purpose | Merges Into | Deploys To |
|--------|---------|-------------|------------|
| `main` | Production-ready code | — | Production |
| `develop` | Integration branch | `main` | Staging |
| `feature/*` | New features | `develop` | Dev environment |
| `hotfix/*` | Emergency fixes | `main` + `develop` | Production |
| `release/*` | Release preparation | `main` + `develop` | Staging |
| `fix/*` | Bug fixes | `develop` | Dev environment |

---

## Branch Naming

```
feature/<short-description>     # feature/radio-streaming
fix/<issue-number>-<description>  # fix/42-login-redirect
hotfix/<description>            # hotfix/auth-timeout
release/v<version>              # release/v1.2.0
chore/<description>             # chore/update-dependencies
docs/<description>              # docs/deployment-guide
```

Examples:
```
feature/podcast-rss-feed
fix/15-empty-state-icons
hotfix/csrf-token-error
release/v1.0.0
chore/upgrade-django-5.0.7
docs/api-endpoints
```

---

## Commit Conventions

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |
| `build` | Build system changes |

### Examples

```
feat(news): add article pagination
fix(auth): prevent session fixation on login
docs(deployment): add Docker Compose production config
refactor(radio): extract stream health check to service
perf(query): add index to Article.published_at
chore(deps): upgrade Django to 5.0.7
test(users): add login view tests
```

### Rules

- Use imperative mood ("add feature" not "added feature")
- Keep subject line under 72 characters
- Reference issues: `fixes #42` or `closes #42`
- Separate subject from body with blank line

---

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/radio-health-check
```

### 2. Make Changes & Commit

```bash
git add .
git commit -m "feat(radio): add stream health monitoring endpoint"
```

### 3. Push & Create PR

```bash
git push origin feature/radio-health-check
```

Create PR on GitHub/GitLab targeting `develop`.

### 4. PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions identified

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log/print statements left
```

### 5. Code Review

- At least 1 approval required
- All CI checks must pass
- Resolve review comments

### 6. Merge

- **Squash merge** for feature branches (clean history)
- **Merge commit** for release/hotfix branches (preserve history)

---

## Release Process

### 1. Create Release Branch

```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
```

### 2. Prepare Release

```bash
# Update version numbers
# Update CHANGELOG.md
# Final testing

git add .
git commit -m "chore(release): v1.2.0 preparation"
```

### 3. Merge to Main

```bash
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags
```

### 4. Merge Back to Develop

```bash
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop
```

### 5. Deploy

```bash
# Production
./scripts/deploy.sh main

# Or for Docker
git checkout v1.2.0
docker compose down
docker compose up -d --build
```

### 6. Clean Up

```bash
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

---

## Hotfix Process

### 1. Create Hotfix from Main

```bash
git checkout main
git pull origin main
git checkout -b hotfix/auth-timeout-fix
```

### 2. Make Fix & Commit

```bash
# Make minimal changes
git add .
git commit -m "fix(auth): increase session timeout to prevent premature logout"
```

### 3. Merge to Main & Develop

```bash
# To main
git checkout main
git merge --no-ff hotfix/auth-timeout-fix
git tag -a v1.2.1 -m "Hotfix: auth timeout"
git push origin main --tags

# To develop
git checkout develop
git merge --no-ff hotfix/auth-timeout-fix
git push origin develop
```

### 4. Deploy Immediately

```bash
./scripts/deploy.sh main
```

### 5. Clean Up

```bash
git branch -d hotfix/auth-timeout-fix
git push origin --delete hotfix/auth-timeout-fix
```

---

## Git Hooks (Pre-commit)

Already configured via `.pre-commit-config.yaml`:

```yaml
# Pre-commit hooks run automatically on commit:
# - Black (code formatting)
# - Flake8 (linting)
# - Trailing whitespace
# - End-of-file fixer
# - YAML validation
```

### Setup

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Run on all files
```

### Bypass (Emergency Only)

```bash
git commit --no-verify -m "emergency: bypass hooks"
```
