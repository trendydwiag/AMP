from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from apps.users.models import (
    User, UserProfile, LoginHistory, PasswordHistory,
    AuditLog, EmailVerification, TwoFactorDevice,
)


class UserAdminChangeForm(UserChangeForm):
    """Custom change form for User model in Django Admin."""

    class Meta(UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(UserCreationForm):
    """Custom creation form for User model in Django Admin."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("Username sudah terdaftar.")
        except User.DoesNotExist:
            return username


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model including UUID fields and system role settings."""

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        'username', 'email', 'role', 'account_status',
        'email_verified', 'two_factor_enabled', 'is_staff', 'is_active', 'created_at',
    )
    list_filter = ('role', 'account_status', 'is_staff', 'is_active', 'email_verified', 'two_factor_enabled', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name', 'last_name', 'email')}),
        ('Hak Akses (RBAC)', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Keamanan & Verifikasi', {'fields': ('email_verified', 'two_factor_enabled', 'force_password_change', 'account_status', 'account_locked_until', 'failed_login_attempts')}),
        ('Audit Log Sistem', {'fields': ('last_login', 'last_activity', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'role', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login', 'last_activity', 'account_locked_until', 'failed_login_attempts')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""

    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user',)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for LoginHistory model."""

    list_display = ('username_attempted', 'status', 'ip_address', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('username_attempted', 'ip_address')
    readonly_fields = ('user', 'username_attempted', 'ip_address', 'user_agent', 'status', 'failure_reason', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for PasswordHistory model."""

    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'password', 'created_at')
    ordering = ('-created_at',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin configuration for AuditLog model."""

    list_display = ('user', 'action', 'resource', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'resource', 'details')
    readonly_fields = ('user', 'action', 'resource', 'details', 'ip_address', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """Admin configuration for EmailVerification model."""

    list_display = ('user', 'verified', 'created_at', 'expires_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('user', 'token', 'created_at', 'expires_at', 'verified')
    ordering = ('-created_at',)


@admin.register(TwoFactorDevice)
class TwoFactorDeviceAdmin(admin.ModelAdmin):
    """Admin configuration for TwoFactorDevice model."""

    list_display = ('user', 'name', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('user__username', 'name')
    readonly_fields = ('user', 'secret', 'created_at')
