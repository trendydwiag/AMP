# Kabulhaden CMS — Changelog

All notable changes to the Kabulhaden CMS project.

---

## [Unreleased]

### Added
- Deployment documentation suite (25+ files)
- Multi-stage Dockerfile with health checks
- Production docker-compose with Nginx, Gunicorn, PostgreSQL
- Development docker-compose with Tailwind watcher
- Nginx reverse proxy configuration
- Gunicorn tuning configuration
- Systemd service unit for bare-metal deployment
- Operational scripts: deploy, backup, restore, setup, health_check
- Security hardening guide with CSP, HSTS, Axes configuration
- Performance optimization guide
- Backup and disaster recovery procedures
- Operations runbook for incident response
- Git workflow and branching strategy
- AI-assisted development guidelines

### Changed
- Updated Dockerfile to target Python 3.10-slim (from 3.13-slim)
- Enhanced entrypoint script with production/development server switching
- Improved logging configuration with structured log format

---

## [1.0.0] - 2025-01-15

### Added
- **Core System**
  - Custom user model with role-based access control
  - Session timeout middleware
  - Last activity tracking middleware
  - Audit logging middleware
  - Global settings context processor
  - Custom error handlers (400, 403, 404, 500)

- **Users App**
  - Custom authentication with session management
  - Password reset flow with email verification
  - User profile management
  - Avatar upload with validation
  - Brute force protection via django-axes

- **Radio App**
  - Live radio streaming engine
  - Stream health monitoring
  - Listener tracking
  - Now playing API

- **Broadcast App**
  - Program scheduling
  - Episode management
  - Broadcast calendar

- **Podcast App**
  - Podcast episode management
  - RSS feed generation
  - Author and metadata support

- **News App**
  - Article CRUD with rich text
  - Category and tag management
  - Author assignment
  - Comment system with moderation
  - SEO metadata

- **Sponsor App**
  - Sponsor management
  - Campaign tracking

- **Community App**
  - Community features

- **Website App**
  - Public-facing pages
  - Responsive design

- **Content App**
  - General content management
  - Page builder capabilities

- **Media Manager**
  - File upload and organization
  - Image optimization
  - Storage backend abstraction

- **Settings App**
  - System settings management
  - Site configuration

- **Infrastructure**
  - Django 5.0.x with split settings (base/development/production)
  - PostgreSQL 16 support with SQLite fallback
  - WhiteNoise with Brotli compression
  - django-environ for environment variables
  - django-csp for Content Security Policy
  - django-axes for brute force protection
  - Tailwind CSS 3.x with Alpine.js and HTMX
  - Docker multi-stage build
  - docker-compose for development and production
  - Nginx reverse proxy
  - Gunicorn WSGI server
  - Pre-commit hooks (Black, Flake8)

- **Management Commands**
  - `create_superadmin` — Create superadmin user
  - `reset_admin` — Reset admin password
  - `reset_password` — Reset any user's password
  - `unlock_user` — Unlock locked user accounts
  - `repair_permissions` — Repair role permissions

- **Design System**
  - Tailwind CSS configuration
  - Component library (buttons, modals, toasts, tables)
  - Dashboard layout system
  - Navigation system
  - Form design patterns
  - Empty states and loading states
  - Error pages
  - Dark mode support
  - Responsive design guide
  - Accessibility (WCAG) compliance

---

## [0.1.0] - 2025-01-01

### Added
- Initial project setup
- Django project scaffolding
- Basic app structure
- Docker configuration
- CI/CD pipeline basics
