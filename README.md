# Palabola

Palabola adalah game sepak bola kepala (*head soccer*) 2D berbasis Python dan library `pygame-ce`. Game ini mendukung mode pertandingan 1 lawan 1 secara lokal, baik dimainkan berdua secara manual maupun melawan AI bot.

## Fitur Utama

- **Fisika Pantulan Realistis**: Simulasi pantulan bola pada tanah, dinding lapangan, tiang sudut, dan atap mistar gawang.
- **AI Bot Dinamis**: Algoritma bot dengan simulasi proyeksi titik jatuh bola untuk menentukan posisi bertahan, menyapu bola, dan menendang ke arah gawang lawan.
- **Sistem Pertandingan**: Papan skor digital dan timer 60 detik dengan deteksi gol serta penentuan pemenang saat waktu habis.
- **Toggle AI Instan**: Fleksibilitas mengubah Player 2 antara kontrol manual keyboard atau AI bot kapan saja di tengah permainan.

## Kontrol Permainan

| Pemain / Fungsi | Kontrol |
| :--- | :--- |
| **Player 1 (Biru)** | `A` (Kiri), `D` (Kanan), `W` (Lompat), `S` (Tendang) |
| **Player 2 (Merah)** | `Panah Kiri` (Kiri), `Panah Kanan` (Kanan), `Panah Atas` (Lompat), `Panah Bawah` (Tendang) |
| **Toggle Mode AI** | `TAB` (Beralih antara mode BOT AI atau MANUAL untuk Player 2) |
| **Mulai Ulang** | `R` (Mengulang pertandingan setelah waktu habis) |

## Struktur Proyek

Proyek ini menggunakan arsitektur modular dengan pembagian tanggung jawab sebagai berikut:

- `main.py`: Titik masuk (*entry point*) utama permainan.
- `palabola.py`: File *wrapper* ringkas agar game tetap dapat dijalankan langsung melalui skrip lama.
- `game.py`: Memuat `Game` untuk siklus *game loop*, *event handling*, dan pengaturan alur pertandingan.
- `config.py`: Konfigurasi global (dimensi layar, konstanta fisika gravitasi/gesekan, dan palet warna).
- `physics.py`: Perhitungan tabrakan antar pemain serta interaksi tendangan dan sundulan bola.
- `renderer.py`: Memuat `Renderer` untuk visual stadion, tribun penonton, papan skor, dan teks status.
- `entities/`: Folder kumpulan objek permainan:
  - `gawang.py`: Memuat `Gawang` (struktur tiang, mistar, dan jaring).
  - `pemain.py`: Memuat `Pemain` (koordinat, animasi sepatu, hitbox, dan lompatan).
  - `bola.py`: Memuat `Bola` (kecepatan, gravitasi bola, dan deteksi bola masuk gawang).
  - `bot_ai.py`: Memuat `BotAI` (prediksi lintasan bola dan navigasi otomatis).

## Cara Menjalankan

### 1. Prasyarat & Instalasi
Pastikan Python telah terinstal, lalu instal dependensi dari `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Permainan
Jalankan game melalui file `main.py` atau `palabola.py`:
```bash
python main.py
```
atau:
```bash
python palabola.py
```
