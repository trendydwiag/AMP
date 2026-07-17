# Kabulhaden CMS — AI-Assisted Development Guidelines

Guidelines for using AI tools (Claude, GPT, Copilot, Cursor) effectively in the Kabulhaden CMS project.

---

## Table of Contents

1. [Project Context for AI](#project-context-for-ai)
2. [Prompting Best Practices](#prompting-best-practices)
3. [Code Generation Guidelines](#code-generation-guidelines)
4. [Common AI Workflows](#common-ai-workflows)
5. [Quality Assurance](#quality-assurance)
6. [What AI Should NOT Do](#what-ai-should-not-do)

---

## Project Context for AI

When prompting AI tools, always provide this context:

```
Project: Kabulhaden CMS — Radio station content management system
Framework: Django 5.0.x, Python 3.10
Database: PostgreSQL 16 (SQLite locally)
Frontend: Tailwind CSS + Alpine.js + HTMX
WSGI: Gunicorn, Reverse Proxy: Nginx
Static Files: WhiteNoise with Brotli
Auth: django-axes for brute force protection
Settings: Split into base.py, development.py, production.py
Apps: users, core, settings, media_manager, radio, broadcast, podcast, news, sponsor, community, website, content
Patterns: Repository pattern, Service layer, Custom management commands
```

---

## Prompting Best Practices

### Always Include

1. **File path and line numbers** — reference specific code
2. **Django version** — 5.0.x (not 3.x or 4.x)
3. **Python version** — 3.10
4. **Project conventions** — repository pattern, Indonesian language for user-facing strings
5. **Existing patterns** — show an example from the codebase

### Good Prompt Examples

```
In apps/news/models.py, I need to add a Comment model that has:
- ForeignKey to Article
- author_name CharField
- body TextField
- created_at DateTimeField (auto_now_add)
- status choices (pending, approved, rejected)
Follow the same pattern as Article model in the same file.
```

```
The file apps/news/views.py has an ArticleListView. Add a search feature
using Django Q objects. Follow the existing pattern of using the
repository layer (apps/news/repositories.py) for database queries.
```

### Bad Prompt Examples

```
Make a CMS feature (too vague)
```

```
Fix this bug (without showing the code or error)
```

---

## Code Generation Guidelines

### Model Generation

When AI generates models, verify:

```python
# ✓ Correct: Uses BigAutoField (project convention)
class MyModel(models.Model):
    id = models.BigAutoField(primary_key=True)

# ✓ Correct: Uses choices from choices.py or inline
class MyModel(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

# ✓ Correct: Has __str__ and Meta
    class Meta:
        verbose_name = 'My Model'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

### View Generation

When AI generates views, verify:

```python
# ✓ Uses repository pattern
from apps.news.repositories import ArticleRepository

class ArticleListView(ListView):
    def get_queryset(self):
        return ArticleRepository.get_published()
```

### Template Generation

When AI generates templates, verify:

```django
{# ✓ Uses Tailwind classes (not Bootstrap) #}
<div class="bg-white rounded-lg shadow p-6">

{# ✓ Uses Alpine.js for interactivity #}
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open" x-cloak>Content</div>
</div>

{# ✓ Uses HTMX for AJAX #}
<button hx-get="{% url 'news:detail' article.pk %}"
        hx-target="#modal-content">
    View
</button>
```

---

## Common AI Workflows

### 1. Creating a New Django App

```
Prompt: Create a new Django app called "events" for the Kabulhaden CMS project.
It should follow the same structure as apps/news/ with models.py, views.py,
repositories.py, services.py, forms.py, urls.py, admin.py, apps.py.
The app should have Event and EventVenue models.
Include migration files. Follow the project's existing patterns.
```

### 2. Writing Tests

```
Prompt: Write tests for apps/news/views.py ArticleListView.
Use pytest-django. Test:
- Anonymous user can view published articles
- Draft articles are not shown
- Search functionality works
- Pagination works correctly
Follow the test patterns in apps/content/tests/.
```

### 3. Database Optimization

```
Prompt: Analyze this queryset in apps/news/repositories.py line 45.
It's causing N+1 queries. Optimize it using select_related and prefetch_related.
Also suggest any missing database indexes.
```

### 4. Refactoring

```
Prompt: Refactor apps/radio/views.py to extract business logic into
apps/radio/services.py. The view should only handle HTTP concerns.
Follow the service layer pattern already used in apps/broadcast/services.py.
```

### 5. Writing Documentation

```
Prompt: Write API documentation for the radio health check endpoint
in apps/radio/views.py. Include request/response examples,
error codes, and authentication requirements.
```

---

## Quality Assurance

### AI-Generated Code Checklist

- [ ] Follows project code style (Black formatter)
- [ ] Uses repository pattern for database access
- [ ] Includes type hints where appropriate
- [ ] Has proper error handling
- [ ] Uses Django's built-in features (not reinventing)
- [ ] Follows naming conventions (snake_case Python, kebab-case URLs)
- [ ] User-facing strings are in Indonesian where appropriate
- [ ] No hardcoded secrets or credentials
- [ ] No `print()` statements (use logging)
- [ ] Migrations are created
- [ ] Admin is registered if needed

### Testing AI Code

```bash
# Run linting
black --check .
flake8 .

# Run type checking
mypy apps/ --ignore-missing-imports

# Run tests
pytest apps/ -v

# Check for security issues
python manage.py check --deploy
```

---

## What AI Should NOT Do

1. **Generate secrets** — Never ask AI for SECRET_KEY, passwords, API keys
2. **Skip code review** — Always review AI-generated code before committing
3. **Auto-commit** — Never commit AI-generated code without human review
4. **Replace understanding** — Understand what the code does, don't blindly use it
5. **Break patterns** — If AI suggests a different pattern, question why
6. **Ignore security** — Verify security implications of every change

### Red Flags in AI Code

- Using `select *` or equivalent (Django ORM handles this)
- Raw SQL without parameterization
- Hardcoded values that should be in settings
- Missing CSRF protection
- Missing permission checks
- Unused imports or dead code
- Comments that explain what (not why)

---

## Useful AI Prompts Library

### Django Management Commands

```
Create a Django management command called "cleanup_sessions" in
apps/core/management/commands/. It should delete expired sessions
from the session table. Follow the pattern of existing commands
in apps/core/management/commands/.
```

### Migration Help

```
I'm adding a new field to an existing model. Write a data migration
that populates the new field based on existing data. The migration
should be reversible.
```

### Performance Analysis

```
Analyze this Django template for performance issues:
- Missing select_related/prefetch_related
- N+1 query potential
- Unnecessary template includes
- Missing cache opportunities
```
