# Future Extensions

## Short Term

### Media Manager Enhancements
- **Bulk Upload Progress** — WebSocket/HTMX progress bar for large batch uploads
- **Image Editing** — Crop, rotate, flip tools in browser using Canvas API
- **Folder Move** — Drag-and-drop files between folders
- **Version Control** — File versioning with rollback capability
- **Storage Backends** — S3, Google Cloud Storage, Azure Blob integration

### Settings Enhancements
- **Settings History** — Track who changed what and when
- **Settings Export/Import** — JSON/YAML export and import
- **Environment Override** — Show which settings are overridden by env vars
- **Live Preview** — Real-time preview of appearance settings

### Authentication Enhancements
- **OAuth2/OIDC** — Google, GitHub, Microsoft SSO integration
- **LDAP Backend** — Enterprise directory integration
- **Session Management** — View/revoke active sessions
- **API Keys** — Programmatic access tokens

## Medium Term

### Content Management
- **Page Builder** — Drag-and-drop page composition
- **Blog/CMS** — Rich text editor with media embedding
- **Categories & Tags** — Taxonomy for content
- **SEO Toolkit** — Sitemap generation, robots.txt management
- **Revision History** — Content versioning with diff view

### Workflow
- **Content Workflow** — Draft → Review → Publish pipeline
- **Roles & Permissions v2** — Granular per-model permissions
- **Scheduled Publishing** — Queue content for future publish
- **Notifications v2** — In-app notifications, webhooks

### Performance
- **CDN Integration** — CloudFront/Cloudflare for static + media
- **Redis Cache** — Object caching, session store
- **Celery Tasks** — Async thumbnail generation, compression
- **Database Optimization** — Read replicas, connection pooling

## Long Term

### Multi-tenancy
- **Organization Model** — Multi-tenant CMS
- **Per-org Settings** — Isolated configurations
- **Subdomain Routing** — tenant1.kabulhaden.com

### API Layer
- **REST API** — DRF-based public API
- **GraphQL** — Flexible query interface
- **Webhooks** — Event-driven integrations

### Analytics
- **Dashboard Analytics** — Usage stats, content metrics
- **User Activity** — Detailed engagement tracking
- **A/B Testing** — Content variant testing
