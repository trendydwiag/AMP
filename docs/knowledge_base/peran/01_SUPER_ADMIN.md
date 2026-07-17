# Super Admin

## Tujuan

Dokumen ini menjelaskan cara kerja Super Admin di AMP Studio. Super Admin memiliki akses penuh ke seluruh sistem.

## Peran Super Admin

Super Admin bertanggung jawab atas:
- Mengelola Partner (stasiun radio)
- Mengelola pengguna sistem
- Mengatur pengaturan teknis
- Memantau seluruh aktivitas
- Menangani masalah teknis

## Yang Bisa Dilakukan Super Admin

| Fitur | Akses |
|-------|-------|
| Kelola Partner | ✓ Penuh |
| Kelola Pengguna | ✓ Penuh |
| Kelola Program | ✓ Penuh |
| Kelola Siaran | ✓ Penuh |
| Kelola Konten | ✓ Penuh |
| Kelola Media | ✓ Penuh |
| Kelola Sponsor | ✓ Penuh |
| Lihat Statistik | ✓ Penuh |
| Pengaturan Sistem | ✓ Penuh |
| Backup & Restore | ✓ Penuh |
| Akses Django Admin | ✓ Ya |

## Menu yang Tersedia

Sidebar Super Admin menampilkan semua menu:
- Beranda
- Siaran (Program, Episode, Jadwal, Host, Pengumuman)
- Konten (Artikel, Kategori, Tag, Penulis, SEO)
- Podcast (Program, Episode)
- Komunitas
- Iklan
- Media (Semua File, Upload, Folder, Tag)
- Analytics
- Partner
- Radio
- Pengaturan (Situs, Tampilan, Email, Bahasa, Keamanan, Pengguna)

[Gambar Sidebar Super Admin]

## Kapan Digunakan

- Saat membuat Partner baru
- Saat mengatur pengguna
- Saat mengatur pengaturan teknis
- Saat menangani masalah sistem
- Saat melakukan backup

## Tips

- Selalu periksa dashboard secara berkala
- Buat backup secara rutin
- Dokumentasikan setiap perubahan pengaturan
- Gunakan role yang sesuai untuk setiap pengguna

## Catatan

- Super Admin bisa mengakses Django Admin di `/admin/`
- Hanya Super Admin yang bisa membuat Partner baru
- Hanya Super Admin yang bisa menghapus data secara permanen
- Selalu konfirmasi sebelum melakukan tindakan destructif

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Partner tidak bisa diakses | Periksa status aktif Partner |
| Pengguna tidak bisa login | Periksa status akun dan role |
| Backup gagal | Periksa ruang penyimpanan |
| Sistem lambat | Periksa beban server |

## FAQ

**Q: Bagaimana cara membuat Partner baru?**
A: Lihat [Panduan Super Admin](../panduan/SUPER_ADMIN_GUIDE.md) bagian "Membuat Partner Baru".

**Q: Apakah Super Admin bisa melihat semua data?**
A: Ya, Super Admin bisa melihat semua data di seluruh Partner.

**Q: Bagaimana cara menghapus Partner?**
A: Gunakan menu Partner > Pilih Partner > Hapus. Konfirmasi diperlukan.

## Best Practice

1. **Buat backup sebelum perubahan besar**
2. **Gunakan password yang kuat dan unik**
3. **Aktifkan verifikasi dua langkah jika tersedia**
4. **Dokumentasikan semua perubahan pengaturan**
5. **Periksa log aktivitas secara berkala**
6. **Jangan berikan akses Super Admin kepada sembarang orang**
7. **Uji perubahan di lingkungan testing terlebih dahulu**

## Screenshot Placeholder

- [Gambar Dashboard Super Admin]
- [Gambar Menu Partner]
- [Gambar Form Buat Partner]
- [Gambar Menu Pengaturan Sistem]
- [Gambar Menu Backup]
- [Gambar Log Aktivitas]
