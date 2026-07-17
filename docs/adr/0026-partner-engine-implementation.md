# ADR-0026: Partner Engine Implementation

## Status
Accepted

## Context
Sprint 3.1 established the architectural foundation (Partner models, Provider Pattern, Feature Flags, Plugins, Themes). Sprint 3.2 implements the **working Partner Engine** — making the system truly partner-aware with:

- Soft delete for partners
- Partner Service with full CRUD, switching, and config loading
- Tenant isolation via partner FK on all business entities
- Partner Switcher in AMP Studio (visible to admins only)
- Domain Engine with multi-strategy resolution
- Security module with tenant isolation enforcement
- Management command for seeding first partner and feature flags

## Decision

### 1. Soft Delete Pattern
We use `is_deleted` boolean + `deleted_at` timestamp on Partner model, with a custom `PartnerManager` that excludes soft-deleted by default. Rationale: partners have associated data (articles, podcasts, media) that must be preserved. Hard delete would cascade and lose data.

### 2. Partner Service Pattern
Created `PartnerService` class following the existing `BaseService` pattern. Provides:
- CRUD operations with atomic transactions
- Partner switching via session storage
- Configuration loading (merged config dict for views/templates)
- Member management (add/remove/list)

### 3. Tenant Isolation via Nullable FK
Added nullable `partner` FK to all business entities (Article, Podcast, RadioStation, Program, Episode, Folder, MediaFile). Nullable because:
- Existing data has no partner association (backward compatible)
- New data will be assigned a partner during creation
- Web public content (website app) may remain global

### 4. Admin Session Override
PartnerMiddleware checks for admin session override BEFORE the standard 5-layer resolution. This allows SUPERUSER/ADMINISTRATOR users to switch partners via AMP Studio without changing domains/headers.

### 5. Domain Engine
Created `DomainEngine` service that supports:
- Direct domain (primary_domain on Partner)
- Custom domain (PartnerDomain table)
- Subdomain (*.PLATFORM_BASE_DOMAIN)
- Localhost development (returns default partner)
- DNS verification for custom domains

### 6. Security Module
Created `TenantIsolation` utility class with:
- Queryset filtering by partner
- Object-level access checking
- `@require_partner_access` decorator for views
- `AuditLogger` for security-relevant action logging

## Consequences
- All new content should be assigned a partner during creation
- Existing content (without partner FK) remains accessible globally
- Admin users can switch partners without re-authentication
- Domain resolution supports development (localhost), staging (subdomain), and production (custom domain)
- Future partners can be onboarded without code changes
