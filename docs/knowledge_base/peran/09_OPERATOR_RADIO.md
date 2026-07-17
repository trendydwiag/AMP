# Operator Radio

## Tujuan

Dokumen ini menjelaskan cara kerja Operator Radio di AMP Studio. Operator Radio mengatur perangkat teknis siaran radio.

## Peran Operator Radio

Operator Radio bertanggung jawab atas:
- Menghubungkan RadioBoss
- Mengatur stream audio
- Memantau status siaran
- Menangani masalah teknis
- Melakukan restart jika perlu

## Yang Bisa Dilakukan Operator Radio

| Fitur | Akses |
|-------|-------|
| Dashboard | ✓ Lihat |
| Radio Status | ✓ Penuh |
| Radio Settings | ✓ Penuh |
| Stream Settings | ✓ Penuh |
| Health Check | ✓ Penuh |
| Kelola Program | ✓ Lihat |
| Kelola Konten | ✗ Tidak |

## Menu yang Tersedia

- Beranda
- Radio (Dashboard, Station, Provider)
- Analytics

[Gambar Sidebar Operator Radio]

## Kapan Digunakan

- Saat menyiapkan siaran
- Saat memantau status stream
- Saat menangani masalah teknis
- Saat mengganti stream URL

## Cara Menghubungkan RadioBoss

### Langkah 1: Buka Pengaturan Radio

1. Klik **Radio** di sidebar
2. Klik **Station**

### Langkah 2: Pilih Station

1. Pilih station yang ingin dikonfigurasi
2. Klik **Edit**

### Langkah 3: Isi Pengaturan Stream

1. Isi **Stream URL** dari RadioBoss
2. Isi **Backup Stream URL** (opsional)
3. Atur **Default Volume**
4. Simpan

[Gambar Form Pengaturan Radio]

## Cara Mengganti Stream

1. Buka **Radio > Station > Edit**
2. Ubah **Stream URL** yang baru
3. Klik **Simpan**
4. Periksa status stream

[Gambar Form Stream URL]

## Cara Melihat Status

1. Buka **Radio > Dashboard**
2. Lihat indikator **Status Stream**
3. Periksa **Health Check** terakhir

[Gambar Dashboard Radio Status]

Status yang mungkin:
- **PLAYING** — Stream aktif dan berjalan
- **STOPPED** — Stream berhenti
- **UNKNOWN** — Status tidak diketahui

## Cara Restart Stream

### Dari AMP Studio
1. Buka **Radio > Dashboard**
2. Klik **Restart Stream**
3. Tunggu hingga status berubah

### Dari RadioBoss
1. Buka program RadioBoss
2. Klik **Stop**
3. Tunggu 5 detik
4. Klik **Start**

[Gambar Tombol Restart Stream]

## Troubleshooting

### Stream Tidak Aktif
1. Periksa koneksi internet
2. Periksa URL stream di pengaturan
3. Restart RadioBoss
4. Hubungi penyedia hosting stream

### Audio Terputus
1. Periksa koneksi internet di server
2. Periksa kuota bandwidth
3. Restart stream dari RadioBoss
4. Periksa log error di RadioBoss

### Status Tidak Update
1. Muat ulang halaman AMP Studio
2. Periksa koneksi ke API
3. Hubungi tim teknis

[Gambar Halaman Troubleshooting Radio]

## Tips

- Selalu periksa status sebelum jam siaran
- Siapkan backup stream URL
- Pantau health check secara berkala
- Catat semua perubahan pengaturan
- Komunikasikan masalah ke tim segera

## Catatan

- Operator Radio tidak bisa mengubah jadwal siaran
- Operator Radio tidak bisa menghapus program
- Semua perubahan stream dicatat oleh sistem

## FAQ

**Q: Bagaimana cara mengetahui stream sudah aktif?**
A: Lihat indikator LIVE di header AMP Studio atau di Dashboard Radio.

**Q: Berapa kali restart diperbolehkan?**
A: Tidak ada batasan. Restart sesuai kebutuhan.

**Q: Apakah ada backup stream?**
A: Ya, siapkan Backup Stream URL di pengaturan station.

**Q: Bagaimana jika stream sering putus?**
A: Periksa kuota bandwidth dan koneksi internet server.

## Best Practice

1. **Periksa status stream 30 menit sebelum siaran**
2. **Siapkan backup stream URL**
3. **Pantau health check setiap jam**
4. **Catat semua masalah dan solusi**
5. **Komunikasikan masalah teknis ke tim segera**

## Screenshot Placeholder

- [Gambar Dashboard Operator Radio]
- [Gambar Menu Station]
- [Gambar Form Edit Station]
- [Gambar Status Stream]
- [Gambar Health Check]
- [Gambar Tombol Restart]
- [Gambar Log Error]
