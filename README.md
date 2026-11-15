# CHAR SOCIETY LINUX NETWORK SECURITY

Toolkit CLI defensif untuk Kali Linux. Fitur:
- Informasi interface dan routing lokal.
- Cache ARP lokal.
- Host discovery subnet milik sendiri dengan `nmap -sn`.
- Audit port/versi layanan pada aset yang Anda miliki atau punya izin.
- Monitor delta byte RX/TX dari `/proc/net/dev`.
- Daftar koneksi/socket menggunakan `ss`.
- HTTP smoke/load test terbatas ke loopback saja (maksimal 100 request, satu per 0,1 detik).

## Instalasi di Kali Linux

Buka Terminal, lalu:

```bash
sudo apt update
sudo apt install -y git python3
```

Ekstrak ZIP, masuk ke folder:

```bash
cd char_society_linux_network_security
chmod +x install.sh
./install.sh
```

Jalankan:

```bash
python3 char_society.py
```

## Contoh penggunaan

1. Pilih `1` untuk melihat alamat IP dan route.
2. Pilih `2` untuk melihat cache ARP.
3. Pilih `3`, lalu masukkan subnet LAN milik sendiri, misalnya `192.168.1.0/24`.
4. Pilih `4` untuk audit layanan pada host yang Anda miliki/diizinkan.
5. Pilih `5` untuk memantau perubahan byte jaringan; tekan `Ctrl+C` untuk berhenti.
6. Pilih `6` untuk melihat koneksi lokal.
7. Untuk menguji aplikasi web yang berjalan di komputer sendiri, pilih `7` dan masukkan port localhost aplikasi tersebut.

## Catatan keamanan

Tool ini **bukan** alat DDoS, penyadapan, pencurian data, atau akses jarak jauh ke ponsel. Modul load test hanya mengirim request terbatas ke `localhost`/`127.0.0.1`/`::1`. Discovery dan audit hanya boleh diarahkan ke jaringan/perangkat milik sendiri atau yang secara eksplisit mengizinkan pengujian. Jangan menjalankan scan pada jaringan publik tanpa izin.

## Troubleshooting

- `nmap belum terpasang`: jalankan `sudo apt install nmap`.
- `Permission denied`: jalankan `chmod +x install.sh char_society.py`.
- Tidak ada host ditemukan: pastikan subnet benar dan perangkat berada pada jaringan yang sama; beberapa perangkat memblokir ping discovery.

## Nmap Pro (menu [8])

Menu Nmap Pro menyediakan profil praktis:
- Host discovery (`-sn`)
- Quick scan (top 100 TCP ports)
- Common ports (top 1.000 TCP ports)
- Service/version detection (`-sV`)
- Full TCP ports (`-p-`)
- OS detection (`-O`)
- UDP top 20 (`-sU`)

Laporan disimpan otomatis ke folder `reports/` dengan nama berbasis tanggal dan waktu.
Mulai dari Quick Scan untuk pemeriksaan awal. Full TCP, OS detection, dan UDP dapat
lebih lambat; beberapa mode membutuhkan hak akses root. Jalankan hanya pada aset
milik sendiri atau target yang secara eksplisit mengizinkan pengujian.

## Terminal splash & UI v1.2

Saat dijalankan di terminal interaktif, aplikasi menampilkan splash screen bertema
Kali Linux, ilustrasi ASCII bergaya naga, status Nmap, menu berbingkai, dan warna ANSI.
Tidak membutuhkan library Python tambahan. Warna otomatis nonaktif saat output
diarahkan ke file atau terminal tidak mendukung warna.
