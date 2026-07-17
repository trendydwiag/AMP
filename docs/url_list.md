# URL List - Kabulhaden CMS

## Authentication & User Management (`/akun/`)
| URL Pattern | View | Name | Method |
|---|---|---|---|
| `/akun/masuk/` | LoginView | `users:login` | GET/POST |
| `/akun/keluar/` | LogoutView | `users:logout` | POST |
| `/akun/daftar/` | RegisterView | `users:register` | GET/POST |
| `/akun/profil/` | ProfileView | `users:profile` | GET/POST |
| `/akun/profil/ubah-password/` | ChangePasswordView | `users:change_password` | GET/POST |
| `/akun/lupa-password/` | ForgotPasswordView | `users:forgot_password` | GET/POST |
| `/akun/reset-password/<uidb64>/<token>/` | ResetPasswordView | `users:reset_password` | GET/POST |
| `/akun/verifikasi-email/<token>/` | EmailVerificationView | `users:verify_email` | GET |
| `/akun/2FA/setup/` | TwoFactorSetupView | `users:two_factor_setup` | GET/POST |
| `/akun/2FA/verifikasi/` | TwoFactorVerifyView | `users:two_factor_verify` | GET/POST |
| `/akun/2FA/nonaktifkan/` | TwoFactorDisableView | `users:two_factor_disable` | POST |
| `/akun/admin/users/` | AdminUserListView | `users:admin_user_list` | GET |
| `/akun/admin/users/buat/` | AdminUserCreateView | `users:admin_user_create` | GET/POST |
| `/akun/admin/users/<uuid:pk>/` | AdminUserDetailView | `users:admin_user_detail` | GET/POST |

## System Settings (`/pengaturan/`)
| URL Pattern | View | Name | Method |
|---|---|---|---|
| `/pengaturan/` | SiteSettingsView | `settings:site` | GET/POST |
| `/pengaturan/seo/` | SEOSettingsView | `settings:seo` | GET/POST |
| `/pengaturan/email/` | EmailSettingsView | `settings:email` | GET/POST |
| `/pengaturan/keamanan/` | SecuritySettingsView | `settings:security` | GET/POST |
| `/pengaturan/tampilan/` | AppearanceSettingsView | `settings:appearance` | GET/POST |
| `/pengaturan/notifikasi/` | NotificationSettingsView | `settings:notification` | GET/POST |
| `/pengaturan/media-sosial/` | SocialMediaSettingsView | `settings:social_media` | GET/POST |
| `/pengaturan/konten/` | ContentSettingsView | `settings:content` | GET/POST |
| `/pengaturan/bahasa/` | LanguageSettingsView | `settings:language` | GET/POST |
| `/pengaturan/media/` | MediaSettingsView | `settings:media` | GET/POST |

## Media Manager (`/media/`)
| URL Pattern | View | Name | Method |
|---|---|---|---|
| `/media/` | MediaDashboardView | `media_manager:dashboard` | GET |
| `/media/file/` | MediaListView | `media_manager:list` | GET |
| `/media/upload/` | MediaUploadView | `media_manager:upload` | GET/POST |
| `/media/file/<uuid:pk>/` | MediaDetailView | `media_manager:detail` | GET/POST |
| `/media/file/<uuid:pk>/hapus/` | MediaDeleteView | `media_manager:delete` | POST |
| `/media/bulk-delete/` | MediaBulkDeleteView | `media_manager:bulk_delete` | POST |
| `/media/folder/` | FoldersView | `media_manager:folders` | GET |
| `/media/folder/buat/` | FolderCreateView | `media_manager:folder_create` | GET/POST |
| `/media/folder/<uuid:pk>/hapus/` | FolderDeleteView | `media_manager:folder_delete` | POST |
| `/media/tag/` | TagsView | `media_manager:tags` | GET |
| `/media/tag/buat/` | TagCreateView | `media_manager:tag_create` | GET/POST |
| `/media/tag/<uuid:pk>/hapus/` | TagDeleteView | `media_manager:tag_delete` | POST |
| `/media/api/search/` | MediaSearchAPIView | `media_manager:api_search` | GET |

## Radio Engine (`/radio/`)
| URL Pattern | View | Name | Method |
|---|---|---|---|
| `/radio/` | RadioDashboardView | `radio:dashboard` | GET |
| `/radio/station/` | RadioStationListView | `radio:station_list` | GET |
| `/radio/station/buat/` | RadioStationCreateView | `radio:station_create` | GET/POST |
| `/radio/station/<uuid:pk>/edit/` | RadioStationEditView | `radio:station_edit` | GET/POST |
| `/radio/provider/` | RadioProviderListView | `radio:provider_list` | GET |
| `/radio/provider/buat/` | RadioProviderCreateView | `radio:provider_create` | GET/POST |
| `/radio/provider/<uuid:pk>/edit/` | RadioProviderEditView | `radio:provider_edit` | GET/POST |
| `/radio/analytics/` | RadioAnalyticsView | `radio:analytics` | GET |
| `/radio/export/csv/<uuid:station_id>/` | ExportCSVView | `radio:export_csv` | GET |
| `/radio/export/excel/<uuid:station_id>/` | ExportExcelView | `radio:export_excel` | GET |
| `/radio/api/status/` | RadioStatusAPIView | `radio:api_status` | GET |
| `/radio/api/player/` | RadioPlayerAPIView | `radio:api_player` | GET |
| `/radio/api/now-playing/` | RadioNowPlayingAPIView | `radio:api_now_playing` | GET |
| `/radio/api/listener/` | RadioListenerAPIView | `radio:api_listener` | GET |
| `/radio/api/health/` | RadioHealthAPIView | `radio:api_health` | GET |
| `/radio/api/current-program/` | RadioCurrentProgramAPIView | `radio:api_current_program` | GET |

## Django Admin (`/admin/`)
| URL Pattern | Description |
|---|---|
| `/admin/` | Django Admin Panel |
