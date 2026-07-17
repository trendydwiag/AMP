# Permission Matrix

## Role-Based Access Control

| Feature | SUPERUSER | ADMINISTRATOR | EDITOR | VIEWER |
|---|---|---|---|---|
| **Dashboard** | ✅ | ✅ | ✅ | ✅ |
| **User Management** | | | | |
| View User List | ✅ | ✅ | ❌ | ❌ |
| Create User | ✅ | ✅ | ❌ | ❌ |
| View User Detail | ✅ | ✅ | ❌ | ❌ |
| Edit User Roles | ✅ | ❌ | ❌ | ❌ |
| Suspend/Deactivate User | ✅ | ✅ | ❌ | ❌ |
| **System Settings** | | | | |
| View Settings | ✅ | ✅ | ❌ | ❌ |
| Edit Settings | ✅ | ✅ | ❌ | ❌ |
| **Media Manager** | | | | |
| View Media Library | ✅ | ✅ | ❌ | ❌ |
| Upload Media | ✅ | ✅ | ❌ | ❌ |
| Delete Media | ✅ | ✅ | ❌ | ❌ |
| Create Folders | ✅ | ✅ | ❌ | ❌ |
| Create Tags | ✅ | ✅ | ❌ | ❌ |
| **Profile** | | | | |
| View Own Profile | ✅ | ✅ | ✅ | ✅ |
| Edit Own Profile | ✅ | ✅ | ✅ | ✅ |
| Change Password | ✅ | ✅ | ✅ | ✅ |
| **Authentication** | | | | |
| Login | ✅ | ✅ | ✅ | ✅ |
| Register | ✅ | ✅ | ✅ | ✅ |
| Forgot Password | ✅ | ✅ | ✅ | ✅ |
| Enable 2FA | ✅ | ✅ | ✅ | ✅ |

## Access Control Implementation

- `@login_required` — All authenticated views
- `@admin_required` — Settings, Media Manager, User Management
- `@role_required(SUPERUSER, ADMINISTRATOR)` — Same as admin_required
- `@email_verified_required` — Email-gated features
- `@guest_only` — Login/Register pages
- `@force_password_change_required` — Post-login password change
