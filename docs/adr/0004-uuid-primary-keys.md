# 0004. Use UUID Primary Keys

**Status:** Accepted
**Date:** 2024-07-01

## Context

Auto-incrementing integer primary keys expose:

- Sequential ID enumeration attacks (guessing `/users/2/`, `/users/3/`)
- ID collisions in distributed or multi-database setups
- Information leakage about record counts and creation order

The CMS manages sensitive user data and public-facing content where these risks are unacceptable.

## Decision

All models use UUIDv4 primary keys via an abstract mixin:

```python
# utils/mixins.py
class UUIDPrimaryKeyMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Universally unique identifier (UUIDv4) primary key."
    )

    class Meta:
        abstract = True
```

Usage on concrete models:

```python
class RadioStation(UUIDPrimaryKeyMixin, TimeStampedModel):
    station_name = models.CharField(max_length=200)
    # id is automatically a UUID
```

The only exception is `SiteSettings` and other singleton models, which use `pk=1` for their single-instance pattern (see ADR-0011).

## Consequences

**Positive:**

- URLs like `/radio/station/a3f8b2c1-.../` are not enumerable.
- Safe for distributed systems and future multi-database replication.
- UUIDs are globally unique, preventing conflicts across environments.
- No migration ordering issues when merging branches.

**Negative:**

- UUIDs are 36 characters in URLs vs. short integer IDs (worse readability).
- 16-byte storage per PK vs. 4-8 bytes for integers (negligible at scale).
- UUIDv4 is random, meaning slightly slower B-tree index inserts vs. sequential integers.
- Foreign key joins require UUID comparison rather than integer comparison.

**Mitigations:**

- Use slugs for user-facing URLs where possible (`/program/my-show/`).
- PostgreSQL handles UUID indexing efficiently with native `uuid` type.
- Storage overhead is negligible for a radio station CMS (thousands, not billions, of records).
