import logging

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, FormView

from apps.users.decorators import (
    login_required_custom, guest_only, admin_required,
    force_password_change_required,
)
from apps.users.forms import (
    LoginForm, RegisterForm, ProfileForm, UserProfileForm,
    AvatarUploadForm, AdminPasswordResetForm, TwoFactorSetupForm,
    TwoFactorVerifyForm, ForgotPasswordForm, UserAdminCreationForm,
)
from apps.users.models import UserProfile, TOTPHelper
from apps.users.repositories import (
    UserRepository, LoginHistoryRepository, AuditLogRepository,
    EmailVerificationRepository, TwoFactorDeviceRepository,
    UserProfileRepository,
)
from apps.users.services import (
    UserService, LoginHistoryService, AuditLogService,
    EmailVerificationService, TwoFactorService, UserProfileService,
    PasswordHistoryService,
)
from utils.choices import LoginStatus, AuditAction, UserRole, AccountStatus

User = get_user_model()
security_logger = logging.getLogger('security')


class LoginRequiredMixinCustom:
    """Mixin for class-based views requiring authentication with account checks."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('users:login')}?next={request.path}")
        if not request.user.is_active:
            messages.error(request, "Akun Anda tidak aktif.")
            return redirect('users:login')
        if hasattr(request.user, 'is_suspended') and request.user.is_suspended:
            messages.error(request, "Akun Anda ditangguhkan.")
            return redirect('users:login')
        if hasattr(request.user, 'is_account_locked') and request.user.is_account_locked:
            messages.error(request, "Akun Anda dikunci sementara.")
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    """User login view with brute-force protection and 2FA support."""

    form_class = LoginForm
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data.get('remember_me', False)
        ip_addr = self._get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]

        user = form.user

        if not user.can_login:
            if user.is_suspended:
                messages.error(self.request, "Akun Anda ditangguhkan. Hubungi administrator.")
            elif user.is_account_locked:
                messages.error(self.request, "Akun dikunci sementara. Coba lagi nanti.")
            else:
                messages.error(self.request, "Akun tidak aktif.")
            LoginHistoryService().record_login_attempt(
                username=username, ip_address=ip_addr,
                status=LoginStatus.FAILED, user_agent=user_agent,
                failure_reason='Akun tidak dapat login', user=user,
            )
            return self.form_invalid(form)

        if user.two_factor_enabled:
            self.request.session['pending_2fa_user_id'] = str(user.id)
            self.request.session['pending_2fa_remember'] = remember_me
            return redirect('users:two_factor_verify')

        self._complete_login(user, remember_me, ip_addr, user_agent)
        return redirect(self._get_next_url())

    def _complete_login(self, user, remember_me, ip_addr, user_agent):
        """Perform the actual login and record the event."""
        login(self.request, user)
        user.reset_failed_login()

        if not remember_me:
            self.request.session.set_expiry(0)

        LoginHistoryService().record_login_attempt(
            username=user.username, ip_address=ip_addr,
            status=LoginStatus.SUCCESS, user_agent=user_agent, user=user,
        )
        AuditLogService().log(
            action=AuditAction.LOGIN, user=user,
            resource=f"User: {user.username}",
            ip_address=ip_addr,
        )
        security_logger.info(f"[LOGIN SUCCESS] User: {user.username} | IP: {ip_addr}")

    def _get_next_url(self) -> str:
        """Get the redirect URL after login — always land on AMP Studio."""
        next_url = self.request.GET.get('next', '')
        # Honor explicit next= param, but never send users back into /admin/ directly
        if next_url and next_url.startswith('/') and not next_url.startswith('/admin'):
            return next_url
        return reverse('studio:dashboard')

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context


class LogoutView(View):
    """User logout view with audit logging."""

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            ip_addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
            username = request.user.username
            AuditLogService().log(
                action=AuditAction.LOGOUT, user=request.user,
                resource=f"User: {username}", ip_address=ip_addr,
            )
            security_logger.info(f"[LOGOUT] User: {username} | IP: {ip_addr}")
            logout(request)
            messages.success(request, "Anda telah berhasil keluar.")
        return redirect('users:login')


class TwoFactorVerifyView(FormView):
    """View for verifying TOTP token during login 2FA flow."""

    form_class = TwoFactorVerifyForm
    template_name = 'users/two_factor_verify.html'

    def dispatch(self, *args, **kwargs):
        if 'pending_2fa_user_id' not in self.request.session:
            return redirect('users:login')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        token = form.cleaned_data['token']
        user_id = self.request.session.get('pending_2fa_user_id')
        remember_me = self.request.session.get('pending_2fa_remember', False)

        user = UserRepository().get_by_id(user_id)
        if not user:
            messages.error(self.request, "Sesi tidak valid. Silakan login kembali.")
            return redirect('users:login')

        two_factor_svc = TwoFactorService()
        if not two_factor_svc.verify_token(user, token):
            ip_addr = self._get_client_ip()
            LoginHistoryService().record_login_attempt(
                username=user.username, ip_address=ip_addr,
                status=LoginStatus.FAILED, user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                failure_reason='2FA token salah', user=user,
            )
            messages.error(self.request, "Kode autentikasi salah.")
            return self.form_invalid(form)

        del self.request.session['pending_2fa_user_id']
        del self.request.session['pending_2fa_remember']

        ip_addr = self._get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]

        login(self.request, user)
        user.reset_failed_login()

        if not remember_me:
            self.request.session.set_expiry(0)

        LoginHistoryService().record_login_attempt(
            username=user.username, ip_address=ip_addr,
            status=LoginStatus.SUCCESS, user_agent=user_agent, user=user,
        )
        AuditLogService().log(
            action=AuditAction.LOGIN, user=user,
            resource=f"User: {user.username} (2FA)", ip_address=ip_addr,
        )
        return redirect(self._get_next_url())

    def _get_next_url(self) -> str:
        next_url = self.request.GET.get('next', '')
        if next_url and next_url.startswith('/') and not next_url.startswith('/admin'):
            return next_url
        return reverse('studio:dashboard')

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')


class RegisterView(FormView):
    """User registration view."""

    form_class = RegisterForm
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        first_name = form.cleaned_data.get('first_name', '')
        last_name = form.cleaned_data.get('last_name', '')

        try:
            user = UserService().register_new_user(
                username=username,
                email=email,
                raw_password=password,
                first_name=first_name,
                last_name=last_name,
            )
            ip_addr = self._get_client_ip()

            EmailVerificationService().create_verification(user)
            AuditLogService().log(
                action=AuditAction.USER_CREATE, user=user,
                resource=f"User: {user.username}",
                details="Registrasi mandiri.", ip_address=ip_addr,
            )
            security_logger.info(f"[REGISTER] New user: {user.username} | Email: {email} | IP: {ip_addr}")

            login(self.request, user)
            messages.success(self.request, "Registrasi berhasil! Silakan verifikasi email Anda.")
            return redirect('users:verify_email_notice')
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')


class ProfileView(LoginRequiredMixinCustom, TemplateView):
    """View for displaying and editing user profile."""
    template_name = 'users/profile.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile, _ = UserProfileRepository().get_or_create(request.user)
        context = {
            'profile_form': ProfileForm(instance=request.user),
            'user_profile_form': UserProfileForm(instance=profile),
            'avatar_form': AvatarUploadForm(),
            'profile': profile,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile, _ = UserProfileRepository().get_or_create(request.user)

        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            user_profile_form = UserProfileForm(request.POST, instance=profile)
            if profile_form.is_valid() and user_profile_form.is_valid():
                profile_form.save()
                user_profile_form.save()
                AuditLogService().log(
                    action=AuditAction.PROFILE_UPDATE, user=request.user,
                    resource=f"User: {request.user.username}",
                    details="Profil diperbarui.",
                )
                messages.success(request, "Profil berhasil diperbarui.")
                return redirect('users:profile')
        elif 'upload_avatar' in request.POST:
            avatar_form = AvatarUploadForm(request.POST, request.FILES)
            if avatar_form.is_valid():
                UserProfileService().update_avatar(request.user, avatar_form.cleaned_data['avatar'])
                messages.success(request, "Avatar berhasil diupdate.")
                return redirect('users:profile')

        return redirect('users:profile')


class ChangePasswordView(LoginRequiredMixinCustom, FormView):
    """View for changing password (force password change or voluntary)."""

    form_class = DjangoPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = '/akun/profil/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        UserService().change_user_password(self.request.user, form.cleaned_data['new_password1'])
        AuditLogService().log(
            action=AuditAction.PASSWORD_CHANGE, user=self.request.user,
            resource=f"User: {self.request.user.username}",
            details="Password diubah.",
        )
        messages.success(self.request, "Password berhasil diubah.")
        return super().form_valid(form)


class ForgotPasswordView(FormView):
    """View for requesting a password reset link."""

    form_class = ForgotPasswordForm
    template_name = 'users/forgot_password.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        email = form.cleaned_data['email']
        user = UserRepository().get_by_email(email)
        if user:
            EmailVerificationService().create_verification(user)
            security_logger.info(
                f"[PASSWORD RESET REQUEST] User: {user.username} | Email: {email}"
            )
        messages.success(
            self.request,
            "Jika email terdaftar, tautan reset password telah dikirim."
        )
        return redirect('users:login')


class VerifyEmailNoticeView(TemplateView):
    """View displayed after registration to prompt email verification."""
    template_name = 'users/verify_email_notice.html'


class VerifyEmailView(View):
    """View for verifying email via token link."""

    def get(self, request: HttpRequest, token: str) -> HttpResponse:
        user = EmailVerificationService().verify_email(token)
        if user:
            messages.success(request, "Email berhasil diverifikasi!")
            return redirect('core:home')
        messages.error(request, "Token verifikasi tidak valid atau sudah kadaluarsa.")
        return redirect('users:login')


class TwoFactorSetupView(LoginRequiredMixinCustom, FormView):
    """View for setting up two-factor authentication."""

    form_class = TwoFactorSetupForm
    template_name = 'users/two_factor_setup.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        two_factor_svc = TwoFactorService()
        if request.user.two_factor_enabled:
            device = TwoFactorDeviceRepository().get_by_user(request.user)
            context = {
                'form': self.get_form(),
                'enabled': True,
                'device': device,
            }
            return render(request, self.template_name, context)

        secret = two_factor_svc.generate_secret()
        request.session['pending_2fa_secret'] = secret
        provisioning_uri = request.user.get_totp_provisioning_uri(secret)
        context = {
            'form': self.get_form(),
            'secret': secret,
            'provisioning_uri': provisioning_uri,
            'enabled': False,
        }
        return render(request, self.template_name, context)

    def form_valid(self, form) -> HttpResponse:
        token = form.cleaned_data['token']
        secret = self.request.session.get('pending_2fa_secret')
        if not secret:
            messages.error(self.request, "Sesi tidak valid. Silakan coba lagi.")
            return redirect('users:two_factor_setup')

        if TOTPHelper.verify(secret, token):
            two_factor_svc = TwoFactorService()
            two_factor_svc.setup_2fa(self.request.user, "Authenticator App")
            device = TwoFactorDeviceRepository().get_by_user(self.request.user)
            if device:
                device.secret = secret
                device.save(update_fields=['secret'])
            self.request.user.two_factor_enabled = True
            self.request.user.save(update_fields=['two_factor_enabled'])
            del self.request.session['pending_2fa_secret']
            messages.success(self.request, "Autentikasi dua faktor berhasil diaktifkan!")
            return redirect('users:profile')

        messages.error(self.request, "Kode verifikasi salah. Silakan coba lagi.")
        return self.form_invalid(form)


class TwoFactorDisableView(LoginRequiredMixinCustom, View):
    """View for disabling two-factor authentication."""

    def post(self, request: HttpRequest) -> HttpResponse:
        TwoFactorService().disable_2fa(request.user)
        messages.success(request, "Autentikasi dua faktor telah dinonaktifkan.")
        return redirect('users:profile')


class AdminUserListView(LoginRequiredMixinCustom, TemplateView):
    """View for admin to list and manage all users."""
    template_name = 'users/admin/user_list.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        query = request.GET.get('q', '')
        role_filter = request.GET.get('role', '')
        status_filter = request.GET.get('status', '')

        users = User.objects.all()
        if query:
            users = users.filter(
                models.Q(username__icontains=query) |
                models.Q(email__icontains=query) |
                models.Q(first_name__icontains=query) |
                models.Q(last_name__icontains=query)
            )
        if role_filter:
            users = users.filter(role=role_filter)
        if status_filter:
            users = users.filter(account_status=status_filter)

        context = {
            'users': users,
            'query': query,
            'role_filter': role_filter,
            'status_filter': status_filter,
            'roles': UserRole.choices,
            'statuses': AccountStatus.choices,
        }
        return render(request, self.template_name, context)


class AdminUserCreateView(LoginRequiredMixinCustom, FormView):
    """View for admin to create a new user."""
    form_class = UserAdminCreationForm
    template_name = 'users/admin/user_create.html'

    def form_valid(self, form) -> HttpResponse:
        try:
            user = UserService().register_new_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                raw_password=form.cleaned_data['password'],
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
                role=form.cleaned_data['role'],
                is_staff=form.cleaned_data.get('is_staff', False),
            )
            ip_addr = self._get_client_ip()
            AuditLogService().log(
                action=AuditAction.USER_CREATE, user=self.request.user,
                resource=f"User: {user.username}",
                details=f"User dibuat oleh {self.request.user.username}.",
                ip_address=ip_addr,
            )
            messages.success(self.request, f"User {user.username} berhasil dibuat.")
            return redirect('users:admin_user_list')
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')


class AdminUserDetailView(LoginRequiredMixinCustom, TemplateView):
    """View for admin to view user details and manage the account."""
    template_name = 'users/admin/user_detail.html'

    def get(self, request: HttpRequest, user_id: str, *args, **kwargs) -> HttpResponse:
        target_user = UserRepository().get_by_id(user_id)
        if not target_user:
            messages.error(request, "User tidak ditemukan.")
            return redirect('users:admin_user_list')

        profile, _ = UserProfileRepository().get_or_create(target_user)
        login_history = LoginHistoryRepository().get_user_history(target_user, limit=20)
        audit_logs = AuditLogRepository().get_user_logs(target_user, limit=20)
        password_history = PasswordHistoryService().repository.get_recent_passwords(target_user, limit=5)

        context = {
            'target_user': target_user,
            'profile': profile,
            'login_history': login_history,
            'audit_logs': audit_logs,
            'password_history': password_history,
            'password_form': AdminPasswordResetForm(),
            'roles': UserRole.choices,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, user_id: str, *args, **kwargs) -> HttpResponse:
        target_user = UserRepository().get_by_id(user_id)
        if not target_user:
            messages.error(request, "User tidak ditemukan.")
            return redirect('users:admin_user_list')

        action = request.POST.get('action', '')
        ip_addr = self._get_client_ip()
        user_svc = UserService()

        if action == 'suspend':
            user_svc.suspend_user(target_user, request.user, ip_addr)
            messages.success(request, f"User {target_user.username} ditangguhkan.")
        elif action == 'activate':
            user_svc.activate_user(target_user, request.user, ip_addr)
            messages.success(request, f"User {target_user.username} diaktifkan.")
        elif action == 'deactivate':
            user_svc.deactivate_user(target_user, request.user, ip_addr)
            messages.success(request, f"User {target_user.username} dinonaktifkan.")
        elif action == 'lock':
            user_svc.lock_account(target_user, request.user, ip_addr)
            messages.success(request, f"Akun {target_user.username} dikunci.")
        elif action == 'unlock':
            user_svc.unlock_account(target_user, request.user, ip_addr)
            messages.success(request, f"Akun {target_user.username} dibuka.")
        elif action == 'assign_role':
            new_role = request.POST.get('role', '')
            if new_role in dict(UserRole.choices):
                user_svc.assign_role(target_user, new_role, request.user, ip_addr)
                messages.success(request, f"Peran {target_user.username} diubah ke {new_role}.")
        elif action == 'reset_password':
            password_form = AdminPasswordResetForm(request.POST)
            if password_form.is_valid():
                user_svc.change_user_password(target_user, password_form.cleaned_data['new_password'])
                user_svc.force_password_reset(target_user, request.user, ip_addr)
                AuditLogService().log(
                    action=AuditAction.PASSWORD_RESET, user=request.user,
                    resource=f"User: {target_user.username}",
                    details=f"Password direset oleh {request.user.username}.",
                    ip_address=ip_addr,
                )
                messages.success(request, f"Password {target_user.username} direset. User wajib ganti password saat login.")

        return redirect('users:admin_user_detail', user_id=user_id)

    def _get_client_ip(self) -> str:
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')
