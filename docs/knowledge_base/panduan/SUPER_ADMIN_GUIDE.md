# Panduan Super Admin

## Tujuan

Dokumen ini menjelaskan secara detail semua yang bisa dilakukan Super Admin di AMP Studio.

## Kapan Digunakan

- Saat membuat Partner baru
- Saat mengelola pengguna
- Saat mengatur pengaturan teknis
- Saat melakukan backup/restore
- Saat menangani masalah sistem

---

## 1. Cara Membuat Partner Baru

### Langkah 1: Buka Menu Partner

1. Login sebagai Super Admin
2. Klik **Partner** di sidebar
3. Klik **Tambah Partner**

[Gambar Menu Partner]

### Langkah 2: Isi Informasi Partner

Isi formulir berikut:
- **Nama Partner**: Nama stasiun radio (contoh: "Radio Suara Harapan")
- **Singkatan**: Nama pendek (contoh: "RSH")
- **Email**: Alamat email partner
- **Telepon**: Nomor telepon
- **Alamat**: Alamat lengkap

[Gambar Form Partner Baru]

### Langkah 3: Simpan

Klik **Simpan**. Partner baru akan muncul di daftar.

---

## 2. Cara Membuat Tenant Baru

Tenant adalah instance terpisah untuk setiap Partner. Saat membuat Partner, tenant otomatis dibuat.

### Langkah 1: Pilih Partner

1. Buka **Partner**
2. Pilih Partner yang ingin diaktifkan

### Langkah 2: Aktifkan Tenant

1. Klik **Edit** pada Partner
2. Ubah status menjadi **Aktif**
3. Simpan

[Gambar Status Tenant]

---

## 3. Cara Mengaktifkan Partner

### Langkah 1: Buka Daftar Partner

1. Klik **Partner** di sidebar
2. Cari Partner yang ingin diaktifkan

### Langkah 2: Aktifkan

1. Klik **Edit** pada Partner
2. Ubah status dari **Nonaktif** menjadi **Aktif**
3. Klik **Simpan**

Partner sekarang bisa diakses oleh penggunanya.

---

## 4. Cara Mengubah Branding Partner

### Logo

1. Buka **Partner > Edit**
2. Klik **Ubah Logo**
3. Pilih gambar dari komputer
4. Klik **Simpan**

### Warna

1. Buka **Partner > Edit**
2. Pilih warna tema
3. Klik **Simpan**

### Nama

1. Buka **Partner > Edit**
2. Ubah nama Partner
3. Klik **Simpan**

[Gambar Pengaturan Branding]

---

## 5. Cara Mengatur Logo

### Logo Utama

1. Buka **Partner > Edit**
2. Scroll ke bagian **Logo**
3. Klik **Pilih Logo**
4. Unggah gambar (format: PNG atau JPG, maks 2 MB)
5. Klik **Simpan**

### Logo untuk Dark Mode

1. Buka **Partner > Edit**
2. Klik **Logo Dark Mode**
3. Unggah gambar dengan latar transparan
4. Simpan

[Gambar Upload Logo]

---

## 6. Cara Mengatur Domain

### Langkah 1: Buka Pengaturan Partner

1. Buka **Partner > Edit**
2. Scroll ke bagian **Domain**

### Langkah 2: Isi Domain

1. Ketik domain yang akan digunakan (contoh: `radio.example.com`)
2. Klik **Simpan**

### Langkah 3: Konfigurasi DNS

Hubungi tim teknis untuk mengatur DNS server agar mengarah ke AMP Studio.

[Gambar Pengaturan Domain]

---

## 7. Cara Mengatur SMTP

SMTP digunakan untuk mengirim email otomatis (notifikasi, reset password, dll).

### Langkah 1: Buka Pengaturan Email

1. Klik **Pengaturan** di sidebar
2. Klik **Email**

### Langkah 2: Isi Pengaturan SMTP

- **SMTP Host**: `smtp.example.com`
- **SMTP Port**: `587`
- **Username**: `email@example.com`
- **Password**: `password-email`
- **Encryption**: TLS

### Langkah 3: Kirim Email Uji

1. Klik **Kirim Email Uji**
2. Periksa apakah email masuk
3. Jika berhasil, klik **Simpan**

[Gambar Pengaturan SMTP]

---

## 8. Cara Mengatur Stream URL

### Langkah 1: Buka Pengaturan Radio

1. Klik **Radio** di sidebar
2. Klik **Station**
3. Pilih station yang ingin dikonfigurasi
4. Klik **Edit**

### Langkah 2: Isi Stream URL

- **Stream URL**: URL utama dari RadioBoss (contoh: `http://server:8000/stream`)
- **Backup Stream URL**: URL cadangan (opsional)

### Langkah 3: Simpan

Klik **Simpan**. Periksa status stream di Dashboard Radio.

[Gambar Pengaturan Stream URL]

---

## 9. Cara Mengatur RadioBoss

### Hubungkan RadioBoss ke AMP Studio

1. Buka program **RadioBoss** di komputer
2. Buka **Pengaturan > API**
3. Isi **API URL** dari AMP Studio
4. Isi **API Key** dari AMP Studio
5. Klik **Test Koneksi**
6. Jika berhasil, klik **Simpan**

### Pengaturan di AMP Studio

1. Buka **Radio > Station > Edit**
2. Isi pengaturan berikut:
   - **Auto DJ**: Aktifkan jika ingin RadioBoss mengatur putaran otomatis
   - **Auto Restart**: Aktifkan jika ingin stream restart otomatis
3. Simpan

[Gambar Pengaturan RadioBoss]

---

## 10. Cara Mengatur Theme

### Theme Default

1. Buka **Pengaturan > Tampilan**
2. Pilih **Theme Default**: Terang / Gelap
3. Simpan

### Theme per Partner

1. Buka **Partner > Edit**
2. Pilih **Theme**: Terang / Gelap / Kopi
3. Simpan

[Gambar Pengaturan Theme]

---

## 11. Cara Mengatur Warna

### Warna Primer

1. Buka **Partner > Edit**
2. Klik **Sesuaikan Warna**
3. Pilih **Warna Primer** (warna utama untuk tombol dan link)
4. Klik **Simpan**

### Warna Sekunder

1. Buka **Partner > Edit**
2. Klik **Sesuaikan Warna**
3. Pilih **Warna Sekunder**
4. Simpan

[Gambar Pengaturan Warna]

---

## 12. Cara Mengatur Hak Akses

### Melihat Daftar Role

1. Buka **Pengaturan > Keamanan**
2. Lihat daftar role yang tersedia

### Mengubah Hak Akses Role

1. Pilih role yang ingin diubah
2. Centang/hapus centang fitur yang diizinkan/dilarang
3. Klik **Simpan**

[Gambar Pengaturan Hak Akses]

### Membuat Role Kustom

1. Klik **Tambah Role Baru**
2. Isi nama role
3. Centang semua fitur yang diizinkan
4. Simpan

---

## 13. Cara Menambah Administrator Partner

### Langkah 1: Buka Menu Pengguna

1. Klik **Pengaturan** di sidebar
2. Klik **Pengguna**
3. Klik **Tambah Pengguna**

### Langkah 2: Isi Informasi Pengguna

- **Nama Lengkap**: Nama administrator
- **Email**: Alamat email
- **Kata Sandi**: Kata sandi sementara
- **Role**: Pilih **Partner Admin** atau **Administrator**
- **Partner**: Pilih Partner yang dikelola

### Langkah 3: Simpan

Klik **Simpan**. Pengguna baru akan menerima email undangan.

[Gambar Form Tambah Admin Partner]

---

## 14. Cara Suspend Partner

### Langkah 1: Pilih Partner

1. Buka **Partner**
2. Cari Partner yang ingin disuspend

### Langkah 2: Suspend

1. Klik **Edit** pada Partner
2. Ubah status menjadi **Suspended**
3. Isi alasan suspend
4. Klik **Simpan**

### Efek Suspend

- Seluruh pengguna tidak bisa login
- Website Partner tidak bisa diakses
- Siaran radio berhenti
- Data tetap tersimpan

[Gambar Tombol Suspend]

---

## 15. Cara Backup Partner

### Backup Manual

1. Buka **Partner > Edit**
2. Klik **Backup**
3. Pilih jenis backup:
   - **Full Backup**: Semua data
   - **Backup Database**: Hanya data
   - **Backup Media**: Hanya file
4. Klik **Mulai Backup**
5. Tunggu hingga selesai
6. File backup akan diunduh

### Backup Otomatis

1. Buka **Pengaturan > Keamanan**
2. Aktifkan **Backup Otomatis**
3. Atur jadwal (harian/mingguan)
4. Simpan

[Gambar Menu Backup]

---

## 16. Cara Restore Partner

### Peringatan

Restore akan menggantikan semua data dengan data backup. Pastikan Anda yakin.

### Langkah 1: Pilih File Backup

1. Buka **Partner > Edit**
2. Klik **Restore**
3. Pilih file backup dari komputer

### Langkah 2: Konfirmasi

1. Ketik nama Partner untuk konfirmasi
2. Klik **Restore Sekarang**
3. Tunggu hingga selesai

### Langkah 3: Verifikasi

1. Periksa data setelah restore
2. Pastikan semua data lengkap

[Gambar Menu Restore]

---

## 17. Cara Menghapus Partner

### Peringatan

Menghapus Partner akan menghapus SEMUA data secara permanen. Tidak bisa dikembalikan.

### Langkah 1: Pilih Partner

1. Buka **Partner**
2. Cari Partner yang ingin dihapus

### Langkah 2: Konfirmasi

1. Klik **Hapus** pada Partner
2. Ketik nama Partner untuk konfirmasi
3. Klik **Hapus Permanen**
4. Masukkan kata sandi Super Admin

### Langkah 3: Verifikasi

1. Periksa daftar Partner
2. Pastikan Partner sudah tidak ada

[Gambar Tombol Hapus]

---

## 18. Checklist Sebelum Partner Go Live

Sebelum Partner bisa digunakan, pastikan semua ini sudah selesai:

### Pengaturan Dasar
- [ ] Partner dibuat dan aktif
- [ ] Logo Partner diunggah
- [ ] Warna tema diatur
- [ ] Domain dikonfigurasi
- [ ] SMTP dikonfigurasi dan diuji

### Pengaturan Radio
- [ ] Station dibuat
- [ ] Stream URL diatur
- [ ] RadioBoss terhubung
- [ ] Status stream: PLAYING

### Pengaturan Pengguna
- [ ] Administrator Partner ditambahkan
- [ ] Role pengguna ditetapkan
- [ ] PenyiAR ditambahkan
- [ ] Editor ditambahkan

### Konten
- [ ] Program siaran dibuat
- [ ] Jadwal siaran diatur
- [ ] Artikel pertama ditulis
- [ ] Logo dan banner diunggah

### Pengaturan Teknis
- [ ] SSL certificate aktif (https)
- [ ] DNS terkonfigurasi
- [ ] Backup otomatis aktif
- [ ] Email notifikasi aktif

### Pengujian
- [ ] Login berhasil
- [ ] Siaran radio berjalan
- [ ] Website bisa diakses
- [ ] Artikel bisa dibaca
- [ ] Email notifikasi terkirim

[Gambar Checklist Go Live]

---

## Tips

- Buat dokumentasi untuk setiap perubahan pengaturan
- Uji setiap perubahan sebelum diterapkan ke production
- Selalu buat backup sebelum perubahan besar
- Gunakan role yang sesuai untuk setiap pengguna
- Pantau log aktivitas secara berkala

## Catatan

- Super Admin adalah role paling berkuasa di sistem
- Hanya Super Admin yang bisa membuat/menghapus Partner
- Semua tindakan Super Admin dicatat oleh sistem
- Gunakan hak akses dengan bijak

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Partner tidak bisa diakses | Periksa status aktif Partner |
| Stream tidak berjalan | Periksa RadioBoss dan Stream URL |
| Email tidak terkirim | Periksa pengaturan SMTP |
| Backup gagal | Periksa ruang penyimpanan |
| Logo tidak tampil | Periksa format dan ukuran file |

## FAQ

**Q: Bagaimana cara membuat Partner baru?**
A: Ikuti langkah di bagian "Cara Membuat Partner Baru" di atas.

**Q: Bisa menghapus Partner yang sudah aktif?**
A: Ya, tapi sangat tidak disarankan. Backup terlebih dahulu.

**Q: Bagaimana jika lupa kata sandi?**
A: Hubungi tim teknis untuk reset dari database.

**Q: Berapa banyak Partner yang bisa dibuat?**
A: Tidak ada batasan. Buat sesuai kebutuhan.

**Q: Bagaimana cara mengembalikan data yang terhapus?**
A: Gunakan fitur Restore dari file backup terakhir.

## Best Practice

1. **Buat backup sebelum setiap perubahan besar**
2. **Gunakan password yang kuat dan unik**
3. **Dokumentasikan semua perubahan pengaturan**
4. **Uji perubahan di lingkungan testing**
5. **Pantau log aktivitas setiap hari**
6. **Jangan berikan akses Super Admin kepada sembarang orang**
7. **Atur backup otomatis untuk setiap Partner**

## Screenshot Placeholder

- [Gambar Dashboard Super Admin]
- [Gambar Menu Partner]
- [Gambar Form Buat Partner]
- [Gambar Pengaturan Logo]
- [Gambar Pengaturan Domain]
- [Gambar Pengaturan SMTP]
- [Gambar Pengaturan Stream]
- [Gambar Pengaturan RadioBoss]
- [Gambar Pengaturan Theme]
- [Gambar Pengaturan Warna]
- [Gambar Pengaturan Hak Akses]
- [Gambar Form Tambah Admin]
- [Gambar Menu Backup]
- [Gambar Menu Restore]
- [Gambar Tombol Hapus]
- [Gambar Checklist Go Live]
