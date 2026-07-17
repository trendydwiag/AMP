# Admin Menu Structure

## Sidebar Navigation

```
Kabulhaden CMS
├── Dashboard
├── Pengaturan Situs          (Settings - Admin only)
│   ├── Pengaturan Situs
│   ├── Pengaturan SEO
│   ├── Pengaturan Email
│   ├── Pengaturan Keamanan
│   ├── Pengaturan Tampilan
│   ├── Pengaturan Notifikasi
│   ├── Media Sosial
│   ├── Pengaturan Konten
│   ├── Bahasa & Lokal
│   └── Pengaturan Media
├── Manajemen Media           (Media Manager - Admin only)
│   ├── Dashboard Media
│   ├── Semua File
│   ├── Upload
│   ├── Folder
│   └── Tag
├── User Management           (Admin only)
│   ├── Daftar User
│   └── Buat User
├── Profil
└── Keluar
```

## Django Admin Models

### Users App
- User
- User Profiles
- Login History
- Password History
- Audit Log
- Email Verification
- Two-Factor Devices

### Settings App
- Site Settings (singleton)
- SEO Settings (singleton)
- Email Settings (singleton)
- Security Settings (singleton)
- Appearance Settings (singleton)
- Notification Settings (singleton)
- Social Media Settings (singleton)
- Content Settings (singleton)
- Language Settings (singleton)
- Media Settings (singleton)

### Media Manager App
- Folders
- Tags
- Media Files
