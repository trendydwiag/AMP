# Panduan Operator Radio

## Tujuan

Dokumen ini menjelaskan cara kerja Operator Radio secara detail.

## Kapan Digunakan

- Saat menyiapkan siaran
- Saat memantau status stream
- Saat menangani masalah teknis
- Saat mengganti stream URL

---

## 1. Menghubungkan RadioBoss

### Langkah 1: Buka Pengaturan Radio

1. Klik **Radio** di sidebar
2. Klik **Station**
3. Pilih station yang ingin dikonfigurasi
4. Klik **Edit**

### Langkah 2: Isi Pengaturan Stream

- **Stream URL**: URL dari RadioBoss
- **Backup Stream URL**: URL cadangan (opsional)
- **Default Volume**: Volume awal
- **Auto DJ**: Aktifkan jika ingin putaran otomatis

### Langkah 3: Simpan dan Uji

1. Klik **Simpan**
2. Klik **Test Koneksi**
3. Pastikan status: **PLAYING**

[Gambar Pengaturan Radio]

---

## 2. Mengganti Stream

### Langkah 1: Buka Pengaturan

1. Buka **Radio > Station > Edit**
2. Ubah **Stream URL** yang baru

### Langkah 2: Simpan

1. Klik **Simpan**
2. Periksa status stream
3. Pastikan audio berjalan

[Gambar Form Stream URL]

---

## 3. Melihat Status

### Dari Dashboard Radio

1. Buka **Radio > Dashboard**
2. Lihat indikator **Status Stream**:
   - **PLAYING**: Stream aktif
   - **STOPPED**: Stream berhenti
   - **UNKNOWN**: Status tidak diketahui

### Dari Health Check

1. Buka **Radio > Dashboard**
2. Lihat bagian **Health Check**
3. Periksa:
   - Response time
   - HTTP status
   - Bitrate

[Gambar Dashboard Radio Status]

---

## 4. Restart Stream

### Dari AMP Studio

1. Buka **Radio > Dashboard**
2. Klik **Restart Stream**
3. Tunggu hingga status berubah

### Dari RadioBoss

1. Buka RadioBoss
2. Klik **Stop**
3. Tunggu 5 detik
4. Klik **Start**

[Gambar Tombol Restart Stream]

---

## 5. Troubleshooting Radio

### Stream Tidak Aktif

1. Periksa koneksi internet server
2. Periksa URL stream di pengaturan
3. Restart RadioBoss
4. Hubungi penyedia hosting stream

### Audio Terputus

1. Periksa koneksi internet
2. Periksa kuota bandwidth
3. Restart stream dari RadioBoss
4. Periksa log error di RadioBoss

### Status Tidak Update

1. Muat ulang halaman AMP Studio
2. Periksa koneksi ke API
3. Hubungi tim teknis

### RadioBoss Tidak Terhubung

1. Buka RadioBoss
2. Periksa pengaturan API
3. Pastikan API URL dan Key benar
4. Test koneksi

[Gambar Halaman Troubleshooting Radio]

---

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

**Q: Bagaimana cara mengganti stream URL?**
A: Buka Radio > Station > Edit > Ubah Stream URL > Simpan.

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
- [Gambar Troubleshooting]
