import uuid
import secrets
import hmac
import hashlib
import struct
import time
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from utils.choices import UserRole, AccountStatus, LoginStatus, AuditAction
from utils.mixins import UUIDPrimaryKeyMixin, TimeStampedModel


class UserManager(BaseUserManager):
    """Custom manager for User model to handle creation of accounts with UUID keys and system roles."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a standard User with the given username, email, and password."""
        if not username:
            raise ValueError("Username wajib diisi.")
        if not email:
            raise ValueError("Alamat email wajib diisi.")

        email = self.normalize_email(email)
        extra_fields.setdefault('role', UserRole.VIEWER)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a Superuser with administrative capabilities."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.SUPERUSER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser harus memiliki is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser harus memiliki is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(UUIDPrimaryKeyMixin, TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """Custom identity User model representing Kabulhaden CMS accounts.

    Uses UUIDv4 primary keys and supports Role-Based Access Control (RBAC) classifications.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Wajib diisi. Maksimal 150 karakter. Huruf, angka, dan @/./+/-/_ saja."
    )
    email = models.EmailField(
        unique=True,
        help_text="Alamat email aktif untuk komunikasi dan reset password."
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Nama depan user."
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Nama belakang user."
    )
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.VIEWER,
        help_text="Klasifikasi peran (RBAC) user di dalam sistem."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Menentukan apakah user ini aktif. Hapus centang daripada menghapus akun."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Menentukan apakah user dapat masuk ke situs admin Django."
    )
    email_verified = models.BooleanField(
        default=False,
        help_text="Menentukan apakah email user telah diverifikasi."
    )
    force_password_change = models.BooleanField(
        default=False,
        help_text="Jika aktif, user dipaksa mengganti password saat login berikutnya."
    )
    last_activity = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp terakhir user berinteraksi dengan sistem."
    )
    two_factor_enabled = models.BooleanField(
        default=False,
        help_text="Menentukan apakah autentikasi dua faktor aktif untuk akun ini."
    )
    account_status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
        help_text="Status operasional akun user."
    )
    account_locked_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Akun dikunci sementara sampai waktu ini (dari axes)."
    )
    failed_login_attempts = models.PositiveIntegerField(
        default=0,
        help_text="Jumlah percobaan login gagal berturut-turut."
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Daftar User'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"

    @property
    def get_full_name(self) -> str:
        """Construct full name string or default to username."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    @property
    def get_short_name(self) -> str:
        """Return the first name or username."""
        return self.first_name if self.first_name else self.username

    @property
    def is_account_locked(self) -> bool:
        """Check if the account is currently locked due to failed login attempts."""
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False

    @property
    def is_suspended(self) -> bool:
        """Check if the account is suspended."""
        return self.account_status == AccountStatus.SUSPENDED

    @property
    def can_login(self) -> bool:
        """Determine if user is permitted to authenticate."""
        return self.is_active and not self.is_account_locked and not self.is_suspended

    def increment_failed_login(self) -> None:
        """Increment the failed login counter."""
        self.failed_login_attempts += 1
        self.save(update_fields=['failed_login_attempts'])

    def reset_failed_login(self) -> None:
        """Reset the failed login counter after successful login."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])

    def lock_account(self, duration_minutes: int = 30) -> None:
        """Lock the account for a specified duration."""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])

    def unlock_account(self) -> None:
        """Unlock the account immediately."""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['account_locked_until', 'failed_login_attempts'])

    def suspend(self) -> None:
        """Suspend the user account."""
        self.account_status = AccountStatus.SUSPENDED
        self.is_active = False
        self.save(update_fields=['account_status', 'is_active'])

    def activate(self) -> None:
        """Activate the user account."""
        self.account_status = AccountStatus.ACTIVE
        self.is_active = True
        self.save(update_fields=['account_status', 'is_active'])

    def generate_totp_secret(self) -> str:
        """Generate a new TOTP secret for two-factor authentication."""
        return secrets.token_hex(20)

    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify a TOTP token against the given secret."""
        return TOTPHelper.verify(secret, token)

    def get_totp_provisioning_uri(self, secret: str) -> str:
        """Generate a provisioning URI for TOTP authenticator apps."""
        return f"otpauth://totp/Kabulhaden:{self.username}?secret={secret}&issuer=Kabulhaden"


class TOTPHelper:
    """Helper class for Time-based One-Time Password (TOTP) operations using RFC 6238."""

    TIME_STEP = 30
    DIGITS = 6

    @classmethod
    def generate_token(cls, secret: str) -> str:
        """Generate a TOTP token for the current time step."""
        counter = int(time.time()) // cls.TIME_STEP
        counter_bytes = struct.pack('>Q', counter)
        key = bytes.fromhex(secret) if len(secret) == 40 and all(c in '0123456789abcdef' for c in secret) else secret.encode()
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0f
        truncated = struct.unpack('>I', hmac_hash[offset:offset + 4])[0]
        truncated &= 0x7fffffff
        return str(truncated % (10 ** cls.DIGITS)).zfill(cls.DIGITS)

    @classmethod
    def verify(cls, secret: str, token: str, tolerance: int = 1) -> bool:
        """Verify a TOTP token with a time window tolerance."""
        for offset in range(-tolerance, tolerance + 1):
            counter = (int(time.time()) // cls.TIME_STEP) + offset
            counter_bytes = struct.pack('>Q', counter)
            key = bytes.fromhex(secret) if len(secret) == 40 and all(c in '0123456789abcdef' for c in secret) else secret.encode()
            hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
            idx = hmac_hash[-1] & 0x0f
            truncated = struct.unpack('>I', hmac_hash[idx:idx + 4])[0]
            truncated &= 0x7fffffff
            expected = str(truncated % (10 ** cls.DIGITS)).zfill(cls.DIGITS)
            if hmac.compare_digest(token, expected):
                return True
        return False


class UserProfile(UUIDPrimaryKeyMixin, TimeStampedModel, models.Model):
    """Extended user profile storing personal details and avatar."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="User terkait dengan profil ini."
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        help_text="Foto profil user (format: JPG, PNG, max 5MB)."
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Deskripsi singkat tentang diri user."
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Nomor telepon aktif."
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Tanggal lahir user."
    )
    address = models.TextField(
        max_length=500,
        blank=True,
        help_text="Alamat domisili user."
    )

    class Meta:
        verbose_name = 'Profil User'
        verbose_name_plural = 'Profil User'

    def __str__(self) -> str:
        return f"Profil: {self.user.username}"


class LoginHistory(UUIDPrimaryKeyMixin, models.Model):
    """Record of every login attempt (successful or failed) for audit purposes."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='login_history',
        help_text="User yang melakukan percobaan login."
    )
    username_attempted = models.CharField(
        max_length=150,
        help_text="Username yang dicoba saat login."
    )
    ip_address = models.GenericIPAddressField(
        help_text="Alamat IP dari percobaan login."
    )
    user_agent = models.TextField(
        max_length=500,
        blank=True,
        help_text="User-Agent browser dari percobaan login."
    )
    status = models.CharField(
        max_length=10,
        choices=LoginStatus.choices,
        help_text="Status percobaan login."
    )
    failure_reason = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alasan kegagalan login jika ada."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Waktu terjadinya percobaan login."
    )

    class Meta:
        verbose_name = 'Riwayat Login'
        verbose_name_plural = 'Riwayat Login'
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"{self.username_attempted} - {self.status} - {self.timestamp}"


class PasswordHistory(UUIDPrimaryKeyMixin, models.Model):
    """Tracks previously used passwords to prevent reuse during password changes."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_history',
        help_text="User yang memiliki riwayat password ini."
    )
    password = models.CharField(
        max_length=128,
        help_text="Hash password yang pernah digunakan."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Waktu password ini digunakan."
    )

    class Meta:
        verbose_name = 'Riwayat Password'
        verbose_name_plural = 'Riwayat Password'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Password history: {self.user.username} - {self.created_at}"


class AuditLog(UUIDPrimaryKeyMixin, models.Model):
    """System-wide audit log tracking all significant user and admin actions."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        help_text="User yang melakukan aksi."
    )
    action = models.CharField(
        max_length=30,
        choices=AuditAction.choices,
        help_text="Jenis aksi yang dilakukan."
    )
    resource = models.CharField(
        max_length=200,
        blank=True,
        help_text="Resource atau objek yang terpengaruh."
    )
    details = models.TextField(
        blank=True,
        help_text="Detail tambahan mengenai aksi."
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Alamat IP saat aksi dilakukan."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Waktu terjadinya aksi."
    )

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Log'
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"{self.user} - {self.action} - {self.timestamp}"


class EmailVerification(UUIDPrimaryKeyMixin, models.Model):
    """Token-based email verification for confirming user email addresses."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_verifications',
        help_text="User yang melakukan verifikasi email."
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        help_text="Token unik untuk verifikasi email."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Waktu token dibuat."
    )
    expires_at = models.DateTimeField(
        help_text="Waktu kadaluarsa token."
    )
    verified = models.BooleanField(
        default=False,
        help_text="Menentukan apakah token sudah digunakan untuk verifikasi."
    )

    class Meta:
        verbose_name = 'Verifikasi Email'
        verbose_name_plural = 'Verifikasi Email'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Verifikasi: {self.user.email} - {'Terverifikasi' if self.verified else 'Menunggu'}"

    @property
    def is_expired(self) -> bool:
        """Check if the verification token has expired."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if the token is still usable (not expired and not verified)."""
        return not self.is_expired and not self.verified

    @staticmethod
    def generate_token() -> str:
        """Generate a cryptographically secure verification token."""
        return secrets.token_hex(32)


class TwoFactorDevice(UUIDPrimaryKeyMixin, TimeStampedModel, models.Model):
    """Stores TOTP secrets for users who have enabled two-factor authentication."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='two_factor_devices',
        help_text="User yang memiliki device 2FA ini."
    )
    name = models.CharField(
        max_length=100,
        help_text="Nama device atau aplikasi autentikator."
    )
    secret = models.CharField(
        max_length=64,
        help_text="Secret key TOTP yang dienkripsi."
    )
    is_primary = models.BooleanField(
        default=True,
        help_text="Menentukan apakah ini device 2FA utama."
    )

    class Meta:
        verbose_name = 'Device 2FA'
        verbose_name_plural = 'Device 2FA'

    def __str__(self) -> str:
        return f"2FA: {self.user.username} - {self.name}"

    def verify_token(self, token: str) -> bool:
        """Verify a TOTP token against this device's secret."""
        return TOTPHelper.verify(self.secret, token)
