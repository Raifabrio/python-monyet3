🐵 Gesture Reaction Monkey
Aplikasi deteksi gesture tangan real-time yang menampilkan gambar reaksi monyet berdasarkan gerakan tangan. Dibangun menggunakan OpenCV dan MediaPipe.
✨ Fitur Utama
Deteksi gesture tangan secara real-time
Menampilkan gambar reaksi yang sesuai dengan gesture
Visualisasi landmark tangan dan pose tubuh
Performa cepat dan responsif
🎮 Daftar Gesture
Gesture
Cara Melakukan
Output
🖕 Finger
Angkat jari telunjuk
react1.png
😮 Mouth
Dekatkan tangan ke mulut
react2.png
🙏 Pray
Pertemukan kedua tangan
react3.png
🤙 Phone/OK
Tempelkan jempol dan telunjuk dekat mulut
react4.png
😐 Idle
Tanpa gesture
react_idle.png
📦 Prasyarat
Python 3.7 atau lebih tinggi
OpenCV
MediaPipe
NumPy
📥 Instalasi
Clone repository ini:
bash
12
git clone https://github.com/username-kamu/gesture-reaction-monkey.git
cd gesture-reaction-monkey
Install dependensi:
bash
1
Siapkan gambar reaksi di folder gesture_react_image.py/:
react1.png (gesture finger)
react2.png (gesture mouth)
react3.png (gesture pray)
react4.png (gesture phone/OK)
react_idle.png (idle state)
🚀 Cara Menjalankan
bash
1
Kontrol:
Tekan ESC untuk keluar
📂 Struktur Folder
12345678910
gesture-reaction-monkey/
├── main.py                     # File utama program
├── gesture_react_image.py/     # Folder gambar reaksi
│   ├── react1.png
│   ├── react2.png
│   ├── react3.png
│   ├── react4.png
│   └── react_idle.png
├── requirements.txt            # Daftar dependensi
└── README.md                   # Dokumentasi
⚙️ Pengaturan
Sesuaikan sensitivitas deteksi pada fungsi detect_gesture():
python
12345
# Sensitivitas gesture pinch (jempol + telunjuk)
pinch_distance < 0.05  # Nilai lebih kecil = lebih presisi

# Jarak tangan ke wajah
distance(wrist, mouth) < 0.2  # Sesuaikan dengan jarak kamera
🔧 Troubleshooting
Gambar tidak muncul?
Pastikan path folder gesture_react_image.py sudah benar
Periksa apakah file gambar tersedia
Gesture sulit terdeteksi?
Sesuaikan nilai threshold pada kode
Pastikan pencahayaan cukup
Posisikan tangan dengan jelas di depan kamera
Performa lambat?
Turunkan resolusi kamera
Tutup aplikasi lain yang berat
🤝 Kontribusi
Kontribusi sangat diapresiasi! Silakan:
Fork repository
Buat branch fitur baru
Commit perubahan
Push dan buat Pull Request
📄 Lisensi
MIT License - lihat file LICENSE untuk informasi lebih lanjut.
🙏 Terima Kasih
MediaPipe - Library hand dan pose tracking
OpenCV - Computer vision library
NumPy - Numerical computing library
