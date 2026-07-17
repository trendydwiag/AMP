from django import forms
from .models import (
    SiteSettings, SEOSettings, EmailSettings, SecuritySettings,
    AppearanceSettings, NotificationSettings, SocialMediaSettings,
    ContentSettings, LanguageSettings, MediaSettings
)


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_tagline', 'site_description', 'site_url',
            'site_logo', 'site_favicon', 'maintenance_mode', 'maintenance_message'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-input'}),
            'site_tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'site_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'site_url': forms.URLInput(attrs={'class': 'form-input'}),
            'site_logo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'site_favicon': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'maintenance_mode': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'maintenance_message': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class SEOSettingsForm(forms.ModelForm):
    class Meta:
        model = SEOSettings
        fields = [
            'meta_title', 'meta_description', 'meta_keywords',
            'og_title', 'og_description', 'og_image',
            'twitter_card', 'twitter_site', 'twitter_creator',
            'robots_meta', 'google_analytics_id', 'google_tag_manager_id',
            'custom_head_scripts', 'custom_footer_scripts'
        ]
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-input'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-input'}),
            'og_title': forms.TextInput(attrs={'class': 'form-input'}),
            'og_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'og_image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'twitter_card': forms.Select(attrs={'class': 'form-select'}),
            'twitter_site': forms.TextInput(attrs={'class': 'form-input'}),
            'twitter_creator': forms.TextInput(attrs={'class': 'form-input'}),
            'robots_meta': forms.Select(attrs={'class': 'form-select'}),
            'google_analytics_id': forms.TextInput(attrs={'class': 'form-input'}),
            'google_tag_manager_id': forms.TextInput(attrs={'class': 'form-input'}),
            'custom_head_scripts': forms.Textarea(attrs={'class': 'form-input font-mono', 'rows': 4}),
            'custom_footer_scripts': forms.Textarea(attrs={'class': 'form-input font-mono', 'rows': 4}),
        }


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = [
            'email_backend', 'email_host', 'email_port', 'email_use_tls',
            'email_use_ssl', 'email_host_user', 'email_host_password',
            'default_from_name', 'default_from_email'
        ]
        widgets = {
            'email_backend': forms.TextInput(attrs={'class': 'form-input'}),
            'email_host': forms.TextInput(attrs={'class': 'form-input'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-input'}),
            'email_use_tls': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'email_use_ssl': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'email_host_user': forms.EmailInput(attrs={'class': 'form-input'}),
            'email_host_password': forms.PasswordInput(attrs={'class': 'form-input'}, render_value=True),
            'default_from_name': forms.TextInput(attrs={'class': 'form-input'}),
            'default_from_email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class SecuritySettingsForm(forms.ModelForm):
    class Meta:
        model = SecuritySettings
        fields = [
            'session_timeout_minutes', 'max_login_attempts', 'lockout_duration_minutes',
            'password_min_length', 'require_uppercase', 'require_lowercase',
            'require_numbers', 'require_special_chars', 'password_expiry_days',
            'enable_2fa', 'force_2fa_admin', 'allowed_ip_ranges', 'csrf_trusted_origins'
        ]
        widgets = {
            'session_timeout_minutes': forms.NumberInput(attrs={'class': 'form-input'}),
            'max_login_attempts': forms.NumberInput(attrs={'class': 'form-input'}),
            'lockout_duration_minutes': forms.NumberInput(attrs={'class': 'form-input'}),
            'password_min_length': forms.NumberInput(attrs={'class': 'form-input'}),
            'require_uppercase': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'require_lowercase': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'require_numbers': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'require_special_chars': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'password_expiry_days': forms.NumberInput(attrs={'class': 'form-input'}),
            'enable_2fa': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'force_2fa_admin': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'allowed_ip_ranges': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'csrf_trusted_origins': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }


class AppearanceSettingsForm(forms.ModelForm):
    class Meta:
        model = AppearanceSettings
        fields = [
            'primary_color', 'secondary_color', 'accent_color', 'dark_mode',
            'sidebar_collapsed', 'sidebar_theme', 'font_family', 'font_size',
            'border_radius', 'compact_mode', 'show_breadcrumbs', 'show_welcome_message'
        ]
        widgets = {
            'primary_color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'sidebar_collapsed': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'sidebar_theme': forms.Select(attrs={'class': 'form-select'}),
            'font_family': forms.Select(attrs={'class': 'form-select'}),
            'font_size': forms.Select(attrs={'class': 'form-select'}),
            'border_radius': forms.Select(attrs={'class': 'form-select'}),
            'compact_mode': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_breadcrumbs': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_welcome_message': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = [
            'email_on_user_register', 'email_on_user_login',
            'email_on_password_change', 'email_on_role_change',
            'email_on_account_lock', 'email_on_system_error',
            'email_on_maintenance', 'notify_admins_on_error',
            'notify_superusers_on_critical'
        ]
        widgets = {f: forms.CheckboxInput(attrs={'class': 'form-checkbox'}) for f in fields}


class SocialMediaSettingsForm(forms.ModelForm):
    class Meta:
        model = SocialMediaSettings
        fields = [
            'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url',
            'tiktok_url', 'linkedin_url', 'github_url',
            'whatsapp_number', 'telegram_username'
        ]
        widgets = {
            'facebook_url': forms.URLInput(attrs={'class': 'form-input'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-input'}),
            'tiktok_url': forms.URLInput(attrs={'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-input'}),
            'telegram_username': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ContentSettingsForm(forms.ModelForm):
    class Meta:
        model = ContentSettings
        fields = [
            'posts_per_page', 'excerpt_length', 'enable_comments',
            'moderate_comments', 'allow_guest_comments', 'default_post_status',
            'enable_revision_history', 'max_upload_size_mb', 'allowed_upload_types'
        ]
        widgets = {
            'posts_per_page': forms.NumberInput(attrs={'class': 'form-input'}),
            'excerpt_length': forms.NumberInput(attrs={'class': 'form-input'}),
            'enable_comments': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'moderate_comments': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'allow_guest_comments': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'default_post_status': forms.Select(attrs={'class': 'form-select'}),
            'enable_revision_history': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'max_upload_size_mb': forms.NumberInput(attrs={'class': 'form-input'}),
            'allowed_upload_types': forms.TextInput(attrs={'class': 'form-input'}),
        }


class LanguageSettingsForm(forms.ModelForm):
    class Meta:
        model = LanguageSettings
        fields = ['site_language', 'date_format', 'time_format', 'timezone']
        widgets = {
            'site_language': forms.Select(attrs={'class': 'form-select'}),
            'date_format': forms.Select(attrs={'class': 'form-select'}),
            'time_format': forms.Select(attrs={'class': 'form-select'}),
            'timezone': forms.TextInput(attrs={'class': 'form-input'}),
        }


class MediaSettingsForm(forms.ModelForm):
    class Meta:
        model = MediaSettings
        fields = [
            'storage_backend', 'max_file_size_mb', 'image_max_width',
            'image_max_height', 'image_compression_quality',
            'auto_generate_thumbnails', 'thumbnail_width', 'thumbnail_height',
            'allowed_extensions', 'enable_image_optimization'
        ]
        widgets = {
            'storage_backend': forms.Select(attrs={'class': 'form-select'}),
            'max_file_size_mb': forms.NumberInput(attrs={'class': 'form-input'}),
            'image_max_width': forms.NumberInput(attrs={'class': 'form-input'}),
            'image_max_height': forms.NumberInput(attrs={'class': 'form-input'}),
            'image_compression_quality': forms.Select(attrs={'class': 'form-select'}),
            'auto_generate_thumbnails': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'thumbnail_width': forms.NumberInput(attrs={'class': 'form-input'}),
            'thumbnail_height': forms.NumberInput(attrs={'class': 'form-input'}),
            'allowed_extensions': forms.TextInput(attrs={'class': 'form-input'}),
            'enable_image_optimization': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
