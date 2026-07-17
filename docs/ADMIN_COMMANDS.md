# Admin Management Commands - Kabulhaden CMS

## Ringkasan

Dokumentasi ini menjelaskan lima perintah manajemen administratif yang tersedia di Kabulhaden CMS. Perintah-perintah ini digunakan untuk mengelola akun administrator, super administrator, reset password, membuka kunci akun, serta memperbaiki dan menyinkronkan permission pengguna.

Perintah-perintah ini dijalankan dari command line menggunakan `python manage.py` di dalam environment Django.

---

## Catatan Penggunaan

### Environment Variables

| Variable | Perintah | Deskripsi |
|---|---|---|
| `DJANGO_ADMIN_USERNAME` | `reset_admin` | Username admin (default: `admin`) |
| `DJANGO_ADMIN_PASSWORD` | `reset_admin` | Password admin (jika tidak diisi, diminta interaktif) |
| `DJANGO_ADMIN_EMAIL` | `reset_admin` | Email admin (default: `admin@kabulhaden.com`) |
| `DJANGO_SUPERUSER_USERNAME` | `create_superadmin` | Username super admin |
| `DJANGO_SUPERUSER_EMAIL` | `create_superadmin` | Email super admin |
| `DJANGO_SUPERUSER_PASSWORD` | `create_superadmin` | Password super admin |

### Pertimbangan Keamanan

- **Hindari** menggunakan environment variables dengan password di dalam `.env` yang di-commit ke repository.
- Gunakan **interactive mode** (tanpa env var) di production jika memungkinkan.
- **Jangan jalankan** perintah ini di public CI/CD pipeline.
- Selalu pastikan hanya **Super Administrator** atau **Administrator** yang menjalankan perintah ini.

---

## Daftar Perintah

### 1. `reset_admin`

**Deskripsi:** Mereset password akun admin default atau membuatnya jika belum ada.

Perintah ini mencari user berdasarkan username (default: `admin`). Jika ditemukan, password direset. Jika tidak ditemukan, user baru dibuat dengan role `ADMINISTRATOR`.

**Sintaks:**

```bash
python manage.py reset_admin
```

**Opsi:**
Perintah ini tidak memiliki opsi command-line. Semua konfigurasi dilakukan melalui environment variable atau input interaktif.

**Environment Variables:**

| Variable | Default | Deskripsi |
|---|---|---|
| `DJANGO_ADMIN_USERNAME` | `admin` | Username yang akan direset/dibuat |
| `DJANGO_ADMIN_PASSWORD` | _(diminta interaktif)_ | Password admin |
| `DJANGO_ADMIN_EMAIL` | `admin@kabulhaden.com` | Email admin (hanya saat membuat baru) |

**Contoh Penggunaan:**

Dengan environment variable:
```bash
export DJANGO_ADMIN_USERNAME=admin
export DJANGO_ADMIN_PASSWORD=secretpassword123
export DJANGO_ADMIN_EMAIL=admin@kabulhaden.com
python manage.py reset_admin
```

Mode interaktif (jika `DJANGO_ADMIN_PASSWORD` tidak di-set):
```bash
python manage.py reset_admin
# Akan diminta:
# Masukkan password baru: ********
# Konfirmasi password: ********
```

**Contoh Output:**
```
Password untuk user "admin" berhasil direset.
```
atau (jika user belum ada):
```
User admin "admin" berhasil dibuat dengan role ADMINISTRATOR.
```

---

### 2. `create_superadmin`

**Deskripsi:** Membuat akun Super Administrator baru dengan role `SUPERUSER`.

Perintah ini melakukan validasi duplikasi username dan email sebelum membuat user. User akan dibuat dengan role `SUPERUSER` menggunakan `create_superuser()`.

**Sintaks:**

```bash
python manage.py create_superadmin
```

**Opsi:**
Perintah ini tidak memiliki opsi command-line. Semua input dilakukan melalui environment variable atau input interaktif.

**Environment Variables:**

| Variable | Default | Deskripsi |
|---|---|---|
| `DJANGO_SUPERUSER_USERNAME` | _(diminta interaktif)_ | Username super admin |
| `DJANGO_SUPERUSER_EMAIL` | _(diminta interaktif)_ | Email super admin |
| `DJANGO_SUPERUSER_PASSWORD` | _(diminta interaktif)_ | Password super admin |

**Contoh Penggunaan:**

Dengan environment variable:
```bash
export DJANGO_SUPERUSER_USERNAME=superadmin
export DJANGO_SUPERUSER_EMAIL=superadmin@kabulhaden.com
export DJANGO_SUPERUSER_PASSWORD=verysecret123
python manage.py create_superadmin
```

Mode interaktif:
```bash
python manage.py create_superadmin
# Akan diminta:
# Username: superadmin
# Email: superadmin@kabulhaden.com
# Password: ********
# Konfirmasi password: ********
```

**Contoh Output:**
```
Super administrator "superadmin" berhasil dibuat.
```

Jika username/email sudah ada:
```
Username "superadmin" sudah digunakan.
```
```
Email "superadmin@kabulhaden.com" sudah digunakan.
```

---

### 3. `reset_password`

**Deskripsi:** Mereset password untuk user tertentu berdasarkan username.

**Sintaks:**

```bash
python manage.py reset_password <username> [--password <password>] [--unlock]
```

**Argumen:**

| Argumen | Wajib | Deskripsi |
|---|---|---|
| `username` | Ya | Username pengguna yang akan direset passwordnya |

**Opsi:**

| Opsi | Default | Deskripsi |
|---|---|---|
| `--password <password>` | _(diminta interaktif)_ | Password baru secara langsung |
| `--unlock` | `false` | Buka kunci akun bersamaan dengan reset password |

**Contoh Penggunaan:**

Reset password secara interaktif:
```bash
python manage.py reset_password editor1
# Akan diminta:
# Masukkan password baru untuk "editor1": ********
# Konfirmasi password: ********
```

Reset password dengan flag unlock:
```bash
python manage.py reset_password editor1 --unlock
```

Reset password dengan password langsung:
```bash
python manage.py reset_password editor1 --password=newpass123
```

Kombinasi password langsung dan unlock:
```bash
python manage.py reset_password editor1 --password=newpass123 --unlock
```

**Contoh Output:**
```
Password untuk user "editor1" berhasil direset.
```
dengan `--unlock`:
```
Password untuk user "editor1" berhasil direset. Akun juga telah dibuka kuncinya.
```

Jika user tidak ditemukan:
```
User "editor1" tidak ditemukan.
```

---

### 4. `unlock_user`

**Deskripsi:** Membuka kunci akun pengguna yang terkunci.

Perintah ini mereset status akun: `is_active` diaktifkan, `account_status` diubah ke `ACTIVE`, `failed_login_attempts` direset ke 0, dan `account_locked_until` dihapus.

**Sintaks:**

```bash
python manage.py unlock_user [username] [--unlock-all]
```

**Argumen:**

| Argumen | Wajib | Deskripsi |
|---|---|---|
| `username` | Tidak* | Username pengguna yang akan dibuka kuncinya |

\* `username` wajib kecuali menggunakan `--unlock-all`.

**Opsi:**

| Opsi | Default | Deskripsi |
|---|---|---|
| `--unlock-all` | `false` | Buka kunci semua akun yang terkunci (`LOCKED` atau `is_active=False`) |

**Contoh Penggunaan:**

Buka kunci satu user:
```bash
python manage.py unlock_user editor1
```

Buka kunci semua akun yang terkunci:
```bash
python manage.py unlock_user --unlock-all
```

**Contoh Output:**
```
Akun "editor1" berhasil dibuka kuncinya.
```
```
3 akun berhasil dibuka kuncinya.
```

Jika tidak ada akun terkunci:
```
Tidak ada akun yang terkunci ditemukan.
```

Jika username tidak diberikan dan tidak ada flag `--unlock-all`:
```
Harap masukkan username atau gunakan flag --unlock-all.
```

---

### 5. `repair_permissions`

**Deskripsi:** Memperbaiki dan menyinkronkan permission pengguna berdasarkan role mereka.

Perintah ini mendeteksi ketidaksesuaian antara role user dan field permission-nya, lalu memperbaikinya secara otomatis (kecuali dalam mode dry-run).

**Deteksi masalah:**

| Role | Pemeriksaan | Perbaikan |
|---|---|---|
| `SUPERUSER` | `is_superuser` harus `True` | Set `is_superuser=True`, `is_staff=True` |
| `SUPERUSER` | `is_staff` harus `True` | Set `is_staff=True` |
| `ADMINISTRATOR` | `is_staff` harus `True` | Set `is_staff=True` |
| Semua | `is_active=False` dengan `account_status=ACTIVE` | Set `account_status=SUSPENDED` |
| Semua | `failed_login_attempts` negatif | Set `failed_login_attempts=0` |

**Sintaks:**

```bash
python manage.py repair_permissions [--username <username>] [--dry-run]
```

**Opsi:**

| Opsi | Default | Deskripsi |
|---|---|---|
| `--username <username>` | _(semua user)_ | Periksa user spesifik berdasarkan username |
| `--dry-run` | `false` | Tampilkan perubahan tanpa menerapkannya |

**Contoh Penggunaan:**

Periksa semua user (dry-run):
```bash
python manage.py repair_permissions --dry-run
```

Perbaiki semua user:
```bash
python manage.py repair_permissions
```

Periksa user spesifik:
```bash
python manage.py repair_permissions --username editor1 --dry-run
```

Perbaiki user spesifik:
```bash
python manage.py repair_permissions --username editor1
```

**Contoh Output:**

Tidak ada masalah:
```
Semua permission sudah sinkron. Tidak ada masalah ditemukan.
```

Ditemukan masalah (dry-run):
```
Ditemukan 2 user dengan masalah:

  superadmin (SUPERUSER):
    - is_staff seharusnya True

  editor1 (EDITOR):
    - account_status seharusnya SUSPENDED (akun tidak aktif)

[DRY RUN] 2 user dengan masalah ditemukan. Tidak ada perubahan yang diterapkan.
```

Ditemukan masalah (applied):
```
Ditemukan 2 user dengan masalah:

  superadmin (SUPERUSER):
    - is_staff seharusnya True

  editor1 (EDITOR):
    - account_status seharusnya SUSPENDED (akun tidak aktif)

2 user berhasil diperbaiki.
```

Jika user tidak ditemukan:
```
User "unknown" tidak ditemukan.
```

---

## Praktik Keamanan Terbaik

1. **Gunakan `--dry-run` terlebih dahulu** pada `repair_permissions` untuk melihat perubahan sebelum diterapkan.
2. **Hindari menuliskan password di command line** — gunakan mode interaktif atau environment variable yang aman.
3. **Gunakan `reset_admin` hanya saat pemulihan** — bukan untuk pembuatan user sehari-hari. Gunakan `create_superadmin` untuk akun super administrator.
4. **Batasi akses** — hanya user dengan role `SUPERUSER` atau `ADMINISTRATOR` yang boleh menjalankan perintah ini.
5. **Audit setelah perubahan** — setelah reset password atau unlock akun, periksa audit log untuk memastikan perubahan tercatat.
6. **Jangan gunakan `--unlock-all` di production** tanpa memahami dampaknya — pastikan tidak ada akun yang seharusnya tetap terkunci.

---

## Pemecahan Masalah

### User tidak ditemukan
```
User "xxx" tidak ditemukan.
```
**Solusi:** Periksa username menggunakan `python manage.py shell` lalu jalankan `User.objects.values_list('username', flat=True)`.

### Password tidak cocok
```
Password tidak cocok.
```
**Solusi:** Masukkan password yang sama pada konfirmasi. Password harus identik, termasuk spasi dan kapitalisasi.

### Username/Email sudah digunakan (saat `create_superadmin`)
```
Username "xxx" sudah digunakan.
```
**Solusi:** Gunakan username lain, atau reset password user yang sudah ada menggunakan `reset_password`.

### Tidak ada akun yang terkunci ditemukan (saat `unlock_user --unlock-all`)
```
Tidak ada akun yang terkunci ditemukan.
```
**Solusi:** Tidak perlu tindakan — semua akun sudah aktif.

### Permission tidak sinkron (saat `repair_permissions`)
```
Ditemukan N user dengan masalah:
```
**Solusi:** Jalankan `repair_permissions --dry-run` terlebih dahulu untuk melihat detail masalah, lalu jalankan tanpa `--dry-run` untuk memperbaiki.
