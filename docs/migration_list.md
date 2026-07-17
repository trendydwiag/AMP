# Migration List

## Users App
1. `apps/users/migrations/0001_initial.py` — User model, UserProfile, LoginHistory, PasswordHistory, AuditLog, EmailVerification, TwoFactorDevice
2. `apps/users/migrations/0002_user_account_locked_until_user_account_status_and_more.py` — Extended User fields (account_status, email_verified, 2FA, etc.)

## Settings App
3. `apps/settings/migrations/0001_initial.py` — SiteSettings, SEOSettings, EmailSettings, SecuritySettings, AppearanceSettings, NotificationSettings, SocialMediaSettings, ContentSettings, LanguageSettings, MediaSettings

## Media Manager App
4. `apps/media_manager/migrations/0001_initial.py` — Folder, Tag, MediaFile

## Radio App
5. `apps/radio/migrations/0001_initial.py` — RadioStation, RadioProvider, NowPlayingCache, LiveSession, ListenerStatistic, StreamHealth

## Django Built-in
- `admin/0001_initial.py` through `admin/0003_logentry_add_action_flag_choices.py`
- `auth/0001_initial.py` through `auth/0012_alter_user_first_name_max_length.py`
- `contenttypes/0001_initial.py` through `contenttypes/0002_remove_content_type_name.py`
- `sessions/0001_initial.py`
- `axes/0001_initial.py` through `axes/0010_accessattemptexpiration.py`
