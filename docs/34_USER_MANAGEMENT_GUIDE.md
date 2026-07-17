# 34. User Management Guide

## Overview

This guide covers user lifecycle management in Kabulhaden CMS, including registration, profile management, role assignment, and account administration.

---

## User Model

### CustomUser Fields

```python
# apps/users/models.py
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.VIEWER)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## User Lifecycle

### Registration Flow

```
┌─────────────────────────────────┐
│  1. User Registration            │
│     POST /akun/register/         │
│     - Validate email unique      │
│     - Hash password              │
│     - Create user (inactive)     │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  2. Email Verification           │
│     - Send verification email    │
│     - Token expires: 24 hours    │
│     - User clicks link           │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  3. Account Active               │
│     - is_email_verified = True   │
│     - Default role: VIEWER       │
│     - Can now login              │
└─────────────────────────────────┘
```

### Admin-Created User Flow

```
┌─────────────────────────────────┐
│  1. Admin Creates User           │
│     POST /akun/pengguna/tambah/  │
│     - Set email, name, role      │
│     - Generate temp password     │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  2. Welcome Email Sent           │
│     - Temporary password         │
│     - Login link                 │
│     - Forced password change     │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  3. First Login                  │
│     - Must change password       │
│     - @force_password_change_    │
│       required decorator         │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  4. Account Fully Active         │
│     - Custom password set        │
│     - Full access per role       │
└─────────────────────────────────┘
```

---

## User Views

### Available Views

| View | URL | Auth Required | Role Required |
|------|-----|:-------------:|---------------|
| `LoginView` | `/akun/masuk/` | ✗ | — |
| `LogoutView` | `/akun/keluar/` | ✓ | Any |
| `ProfileView` | `/akun/profil/` | ✓ | Any |
| `ProfileEditView` | `/akun/profil/edit/` | ✓ | Any |
| `ChangePasswordView` | `/akun/profil/ganti-password/` | ✓ | Any |
| `DashboardView` | `/akun/dashboard/` | ✓ | Any |
| `UserListView` | `/akun/pengguna/` | ✓ | Admin+ |
| `UserCreateView` | `/akun/pengguna/tambah/` | ✓ | Admin+ |
| `UserDetailView` | `/akun/pengguna/<uuid>/` | ✓ | Admin+ |
| `UserUpdateView` | `/akun/pengguna/<uuid>/edit/` | ✓ | Admin+ |
| `UserDeleteView` | `/akun/pengguna/<uuid>/hapus/` | ✓ | Superuser |

---

## Profile Management

### Profile View

```
┌──────────────────────────────────────────────────┐
│  Profil Saya                                      │
│                                                   │
│  ┌─────────────┐                                  │
│  │   [Avatar]   │  John Doe                       │
│  │              │  john@example.com                │
│  └─────────────┘  Role: EDITOR                    │
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │ Biodata                                      │  │
│  │ Lorem ipsum dolor sit amet...                │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │ Informasi Akun                               │  │
│  │ Username: johndoe                            │  │
│  │ Email: john@example.com                      │  │
│  │ Telepon: +62 812-xxxx-xxxx                   │  │
│  │ Bergabung: 1 Januari 2026                    │  │
│  │ Terakhir aktif: 15 Juli 2026                 │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  [Edit Profil]  [Ganti Password]                  │
└──────────────────────────────────────────────────┘
```

### Profile Edit Form

```python
# apps/users/forms.py
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input'}),
        }
```

---

## Password Management

### Change Password Form

```
┌──────────────────────────────────────────────────┐
│  Ganti Password                                   │
│                                                   │
│  Password Saat Ini                                │
│  ┌─────────────────────────────────────────────┐  │
│  │ ••••••••                                     │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  Password Baru                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ ••••••••                                     │  │
│  └─────────────────────────────────────────────┘  │
│  Minimal 8 karakter                               │
│                                                   │
│  Konfirmasi Password Baru                         │
│  ┌─────────────────────────────────────────────┐  │
│  │ ••••••••                                     │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  [Batal]                        [Simpan]          │
└──────────────────────────────────────────────────┘
```

### Password Validation Rules

| Rule | Requirement |
|------|-------------|
| Minimum length | 8 characters |
| Uppercase | At least 1 letter (A-Z) |
| Lowercase | At least 1 letter (a-z) |
| Number | At least 1 digit (0-9) |
| Symbol | At least 1 special character |
| Similarity | Cannot match username/email |
| History | Cannot reuse last 5 passwords |

---

## User List (Admin)

### User Table

```
┌──────────────────────────────────────────────────────────────┐
│  Daftar Pengguna                          [+ Tambah Pengguna] │
│                                                               │
│  🔍 Search...                                                 │
│                                                               │
│  ┌───────────┬─────────────┬──────────────┬───────┬────────┐  │
│  │ Nama      │ Email       │ Role         │ Status│ Aksi   │  │
│  ├───────────┼─────────────┼──────────────┼───────┼────────┤  │
│  │ Admin     │ admin@...   │ SUPERUSER    │ ✓     │ ✏️ 🗑️  │  │
│  │ Editor 1  │ ed1@...     │ EDITOR       │ ✓     │ ✏️ 🗑️  │  │
│  │ Editor 2  │ ed2@...     │ EDITOR       │ ✓     │ ✏️ 🗑️  │  │
│  │ Viewer 1  │ vw1@...     │ VIEWER       │ ✓     │ ✏️ 🗑️  │  │
│  │ Pending   │ pend@...    │ VIEWER       │ ⏳    │ ✏️ 🗑️  │  │
│  └───────────┴─────────────┴──────────────┴───────┴────────┘  │
│                                                               │
│  Showing 1-5 of 25    [< Prev] [1] [2] [3] ... [5] [Next >]  │
└──────────────────────────────────────────────────────────────┘
```

### Filter Options

| Filter | Values |
|--------|--------|
| Role | All, SUPERUSER, ADMINISTRATOR, EDITOR, VIEWER |
| Status | All, Active, Inactive, Email Unverified |
| Search | Name, email, username |

---

## User CRUD Operations

### Create User (Admin)

```python
# apps/users/views.py
class UserCreateView(AdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['temp_password'])
        user.is_email_verified = True  # Admin-created, no verification needed
        user.save()
        
        # Send welcome email
        send_welcome_email(user, form.cleaned_data['temp_password'])
        
        messages.success(self.request, f'Pengguna {user.username} berhasil dibuat.')
        return super().form_valid(form)
```

### Update User (Admin)

```python
class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Pengguna {self.object.username} berhasil diperbarui.')
        return super().form_valid(form)
```

### Delete User

```python
class UserDeleteView(SuperuserRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            messages.error(request, 'Tidak dapat menghapus akun sendiri.')
            return redirect('users:user_list')
        
        username = user.username
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Pengguna {username} berhasil dihapus.')
        return response
```

---

## Role Assignment

### Role Change Flow

```
┌─────────────────────────────────┐
│  Admin opens user detail/edit    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Select new role from dropdown   │
│  - VIEWER                        │
│  - EDITOR                        │
│  - ADMINISTRATOR                 │
│  - SUPERUSER (superuser only)    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Confirm role change             │
│  Warning: Permissions will       │
│  change immediately              │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Role updated, audit logged      │
│  User notified via email         │
└─────────────────────────────────┘
```

### Role Change Restrictions

| Scenario | Allowed |
|----------|---------|
| Change own role | ✗ |
| Superuser → Admin | ✓ (by another superuser) |
| Admin → Editor | ✓ (by superuser) |
| Editor → Viewer | ✓ (by admin+) |
| Viewer → Editor | ✓ (by admin+) |
| Downgrade last superuser | ✗ |

---

## Account Deactivation

### Deactivation vs Deletion

| Aspect | Deactivation | Deletion |
|--------|--------------|----------|
| Visibility | Hidden from list | Removed from DB |
| Login | Blocked | N/A |
| Data | Preserved | Deleted (cascading) |
| Reversible | Yes | No |
| Audit trail | Preserved | Lost |

### Soft Delete Implementation

```python
class CustomUser(AbstractUser):
    # ... existing fields ...
    is_active_deactivated = models.BooleanField(default=False)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    deactivated_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL
    )
    
    def deactivate(self, by_user):
        self.is_active = False
        self.is_active_deactivated = True
        self.deactivated_at = timezone.now()
        self.deactivated_by = by_user
        self.save()
        
        AuditLog.objects.create(
            user=by_user,
            action='DEACTIVATE',
            model_name='CustomUser',
            object_id=str(self.pk),
        )
```

---

## User Services

```python
# apps/users/services.py
class UserService:
    def __init__(self, repository):
        self.repository = repository
    
    def create_user(self, data):
        user = self.repository.create(data)
        send_verification_email(user)
        return user
    
    def update_role(self, user_id, new_role, performed_by):
        user = self.repository.get(user_id)
        old_role = user.role
        user.role = new_role
        user.save()
        
        AuditLog.objects.create(
            user=performed_by,
            action='UPDATE_ROLE',
            model_name='CustomUser',
            object_id=str(user_id),
            changes={'role': {'old': old_role, 'new': new_role}}
        )
        
        send_role_change_email(user, old_role, new_role)
        return user
    
    def deactivate_account(self, user_id, performed_by):
        user = self.repository.get(user_id)
        user.deactivate(performed_by)
        return user
```

---

## Related Documentation

- `32_AUTHENTICATION_AUTHORIZATION_GUIDE.md` - Auth flow
- `33_ROLE_BASED_ACCESS_CONTROL_GUIDE.md` - RBAC details
- `14_FORM_DESIGN.md` - Form patterns
- `17_TOAST_NOTIFICATION.md` - Notification patterns

---

*Last updated: 2026-07-15*
