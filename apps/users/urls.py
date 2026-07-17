from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('masuk/', views.LoginView.as_view(), name='login'),
    path('keluar/', views.LogoutView.as_view(), name='logout'),
    path('daftar/', views.RegisterView.as_view(), name='register'),

    # Password
    path('lupa-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('ganti-password/', views.ChangePasswordView.as_view(), name='change_password'),

    # Profile
    path('profil/', views.ProfileView.as_view(), name='profile'),

    # Email Verification
    path('verifikasi-email/', views.VerifyEmailNoticeView.as_view(), name='verify_email_notice'),
    path('verifikasi-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify_email'),

    # Two-Factor Authentication
    path('2fa/verifikasi/', views.TwoFactorVerifyView.as_view(), name='two_factor_verify'),
    path('2fa/setup/', views.TwoFactorSetupView.as_view(), name='two_factor_setup'),
    path('2fa/nonaktifkan/', views.TwoFactorDisableView.as_view(), name='two_factor_disable'),

    # Admin User Management
    path('admin/pengguna/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/pengguna/buat/', views.AdminUserCreateView.as_view(), name='admin_user_create'),
    path('admin/pengguna/<uuid:user_id>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
]
