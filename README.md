# 💡 Chatbot Analisis Algoritma

Chatbot ini dirancang untuk membantu Anda mempelajari **Analisis Algoritma dan Struktur Data** menggunakan Streamlit dan OpenRouter API.

---

## ✨ Fitur

* **Antarmuka Intuitif:** Chatbot berbasis web dengan Streamlit.
* **Didukung LLM:** Menggunakan model `openai/gpt-4.1-nano` via OpenRouter untuk penjelasan mendalam.
* **Fokus Algoritma:** Memberikan jawaban spesifik tentang algoritma, kompleksitas, dan struktur data.
* **Rekomendasi Sumber Daya:** Menampilkan tautan ke GeeksforGeeks, HackerRank, LeetCode.
* **Riwayat & Hapus Obrolan:** Mengelola sesi percakapan Anda.

---

## 🚀 Memulai

### Prasyarat

* Python 3.8+ terinstal.

### Instalasi

1.  **Siapkan Proyek:** Buat folder proyek dan tempatkan `app.py`, `requirements.txt`, dan `.env` di dalamnya.
2.  **Lingkungan Virtual:**
    ```bash
    python -m venv chatbot_env
    source chatbot_env/bin/activate # macOS/Linux
    chatbot_env\Scripts\activate     # Windows
    ```
3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    (Pastikan `requirements.txt` berisi: `streamlit`, `openai`, `python-dotenv`)

### Konfigurasi API OpenRouter (Ini lumayan ribet, kalau pengen simple pake yg punya gw dlu aja ya guys)

1.  **Dapatkan Kunci API:** Daftar/masuk ke [OpenRouter.ai](https://openrouter.ai/), lalu dapatkan kunci API Anda dari halaman "Keys".
2.  **Buat `.env`:** Di folder proyek Anda, buat file bernama `.env`.
3.  **Tambahkan Kunci:** Masukkan kunci API Anda ke `.env` seperti ini:
    ```
    OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY_HERE"
    ```
    **Penting:** Jangan bagikan file `.env` ini!

### Jalankan Aplikasi

```bash
streamlit run app.py
Aplikasi akan terbuka di browser Anda (biasanya http://localhost:8501).
```

🤖 Cara Menggunakan
Ketik pertanyaan Anda di kotak obrolan.
Dapatkan penjelasan dan rekomendasi tautan.
Gunakan "Clear Chat History" untuk memulai ulang.
📁 Struktur Proyek
.
├── app.py              # Kode utama aplikasi
├── .env                # Kunci API (RAHASIA!)
└── requirements.txt    # Daftar dependensi Python
⚙️ Kustomisasi
Ganti Model LLM: Ubah OPENROUTER_MODEL_NAME di app.py (cek OpenRouter.ai/docs untuk model lain).
Sesuaikan Persona: Edit SYSTEM_INSTRUCTION di app.py.
Perbarui Tautan: Modifikasi kamus ALGORITHM_LINKS di app.py.
🤝 Kontribusi
Selamat datang untuk berkontribusi!

📄 Lisensi