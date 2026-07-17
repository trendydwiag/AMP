# Kabulhaden CMS — Contributing Guidelines

How to contribute to the Kabulhaden CMS project.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Standards](#code-standards)
4. [Project Structure](#project-structure)
5. [Making Changes](#making-changes)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Issues](#reporting-issues)

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 16 (or SQLite for quick start)
- Git
- Docker & Docker Compose (optional but recommended)

### Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/kabulhaden.git
cd kabulhaden
git remote add upstream https://github.com/ORIGINAL-ORG/kabulhaden.git
```

---

## Development Setup

### Option A: Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
npm install
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
npm run watch &
python manage.py runserver 0.0.0.0:8000
```

### Option B: Docker

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml up --build
docker compose -f docker-compose.dev.yml exec web python manage.py migrate
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

---

## Code Standards

### Python

- **Formatter**: Black (line length 88)
- **Linter**: Flake8 with flake8-docstrings
- **Style**: PEP 8
- **Type hints**: Encouraged but not required
- **Docstrings**: Required for public functions and classes

```python
# ✓ Good
def get_published_articles(self, limit: int = 10) -> QuerySet:
    """Get published articles ordered by date."""
    return Article.objects.filter(
        status='published'
    ).order_by('-published_at')[:limit]
```

### JavaScript / Frontend

- **No framework-specific linter** — use consistent style
- **Alpine.js**: Use `x-data`, `x-show`, `@click` patterns
- **HTMX**: Use `hx-get`, `hx-post`, `hx-target` attributes
- **No inline `<script>` blocks** — put JS in static files

### HTML / Templates

- Use Tailwind CSS classes (no custom CSS unless necessary)
- Follow BEM-like naming for custom CSS if needed
- Use Django template inheritance (`{% extends %}`, `{% block %}`)
- Use `{% include %}` for reusable components

---

## Project Structure

```
apps/
├── <app_name>/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py          # Database models
│   ├── views.py           # HTTP views (thin)
│   ├── urls.py            # URL routing
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin registration
│   ├── repositories.py    # Database queries
│   ├── services.py        # Business logic
│   ├── tests.py           # Tests
│   ├── migrations/        # Database migrations
│   └── management/
│       └── commands/       # Custom management commands
```

### Patterns to Follow

- **Repository Pattern**: All database queries go in `repositories.py`
- **Service Layer**: Business logic in `services.py`
- **Thin Views**: Views handle HTTP only, delegate to services
- **Indonesian Labels**: User-facing strings in Indonesian

---

## Making Changes

### 1. Create a Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow the project structure
- Write tests for new features
- Update documentation if needed
- Create migrations for model changes

### 3. Commit

```bash
# Stage specific files
git add apps/news/models.py apps/news/migrations/

# Commit with conventional message
git commit -m "feat(news): add article view counter"

# Push
git push origin feature/your-feature-name
```

### Commit Message Format

```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, perf, test, chore
Scope: app name (news, radio, broadcast, etc.)
Description: imperative mood, lowercase, no period
```

---

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific app
pytest apps/news/

# With coverage
pytest --cov=apps/ --cov-report=html

# Verbose output
pytest -v
```

### Write Tests For

- Models (field validation, methods, properties)
- Views (HTTP methods, permissions, responses)
- Forms (validation, cleaning)
- Services (business logic)
- Repositories (query correctness)

### Test Example

```python
import pytest
from apps.news.models import Article

@pytest.mark.django_db
def test_article_str():
    article = Article(title="Test Article", slug="test-article")
    assert str(article) == "Test Article"

@pytest.mark.django_db
def test_published_articles():
    Article.objects.create(title="Published", status="published")
    Article.objects.create(title="Draft", status="draft")
    published = Article.objects.filter(status="published")
    assert published.count() == 1
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows project style (run `black .` and `flake8 .`)
- [ ] Tests pass (`pytest`)
- [ ] No new warnings or errors
- [ ] Migrations are created and tested
- [ ] Documentation is updated if needed

### PR Description

```markdown
## What
Brief description of changes.

## Why
Reason for the change.

## How
Implementation approach.

## Testing
How to test the changes.

## Checklist
- [ ] Tests pass
- [ ] Code formatted with Black
- [ ] No linting errors
- [ ] Migrations tested
```

### Review Process

1. At least 1 approval required
2. All CI checks must pass
3. Address review feedback
4. Squash merge for clean history

---

## Reporting Issues

### Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, Django version)
- Screenshots if applicable
- Error logs if applicable

### Feature Requests

Include:
- Problem statement
- Proposed solution
- Alternatives considered
- Use cases

### Security Issues

**Do not** open public issues for security vulnerabilities. Email security concerns directly to the maintainers.
