# 0015. Use Indonesian for UI Strings

**Status:** Accepted
**Date:** 2024-07-15

## Context

Kabulhaden CMS targets radio stations in Indonesia. The primary users are:

- Station administrators who may not be comfortable with English
- Content editors writing Indonesian-language articles and programs
- End users visiting the public website (Indonesian audience)

All user-facing text should be in Bahasa Indonesia for consistency and accessibility.

## Decision

- **All UI strings** (labels, buttons, messages, form help text, navigation) are in Indonesian.
- **All code identifiers** (variables, functions, classes, modules) remain in English.
- **All documentation** is written in English for developer accessibility.
- **Configuration** uses `LANGUAGE_CODE = 'id'` and `TIME_ZONE = 'Asia/Jakarta'`.

Examples from the codebase:

```python
# Settings view titles
'Pengaturan Situs'          # Site Settings
'Pengaturan Keamanan'       # Security Settings
'Pengaturan Tampilan'       # Appearance Settings
'Media Sosial'              # Social Media
'Bahasa & Lokal'            # Language & Locale

# Messages
'{title} berhasil diperbarui.'   # "{title} updated successfully."
'Sesi Anda telah berakhir karena tidak ada aktivitas.'  # "Your session has ended due to inactivity."

# Model help_text
"Username wajib diisi."          # "Username is required."
"Foto profil user (format: JPG, PNG, max 5MB)."  # "User profile photo (format: JPG, PNG, max 5MB)."
```

## Consequences

**Positive:**

- Indonesian-speaking administrators can use the CMS without language barriers.
- Consistent language creates a professional, localized experience.
- Django's `LANGUAGE_CODE = 'id'` enables built-in i18n features for date/time formatting.
- `verbose_name` and `verbose_name_plural` on models display correctly in Django admin.

**Negative:**

- Django's default admin interface strings are translated via Django's i18n, but custom strings must be manually translated.
- New features require Indonesian strings to be written alongside English code comments.
- Searching documentation for error messages requires knowing both English (docs) and Indonesian (UI).

**Mitigations:**

- All user-facing strings are hardcoded in templates and views (no `.po` file translation overhead).
- Code comments and docstrings are in English for developer comprehension.
- Error messages in the security log use English for consistency in monitoring.
