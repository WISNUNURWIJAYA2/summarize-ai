# SummaAI — Ringkas Dokumen dengan MT5

Aplikasi web untuk meringkas dokumen PDF, DOCX, dan TXT menggunakan model MT5 (Multilingual Text-to-Text Transfer Transformer). Mendukung Bahasa Indonesia dan Bahasa Inggris.

---

## Arsitektur Proyek

```
SUMAARIZE-mt5/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── documents.py
│   │   │       └── summaries.py
│   │   └── utils/
│   │       └── file_utils.py
│   ├── models/
│   │   └── MT5V6.2/
│   ├── main.py
│   └── requirements.txt
└── Frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| Frontend | HTML, Bootstrap 5, Vanilla JS |
| Backend | Python, FastAPI, Uvicorn |
| Model AI | MT5 (mT5ForConditionalGeneration) |
| Parser | PyMuPDF (PDF), python-docx (DOCX) |
| Output | PDF generation, Salin text |

---

## Cara Instalasi & Menjalankan

### Prasyarat

- Python 3.9 atau lebih baru
- pip
- Browser Chrome / Edge

---

### 1. Clone atau ekstrak proyek
---

### 2. Buat Virtual Environment

```bash
# Buat venv
python -m venv .venv
```

Aktifkan venv:

```bash
# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mac / Linux
source .venv/bin/activate
---

### 3. Install Dependencies Backend

```bash
cd backend
pip install -r requirements.txt
```

> Proses ini mungkin memakan waktu cukup lama karena mengunduh library ML seperti transformers dan torch.

---

### 4. Jalankan Backend

Pastikan masih berada di folder `backend` dan venv sudah aktif, lalu jalankan:

```bash
uvicorn app.main:app --reload
```

Backend akan berjalan di:
```
http://127.0.0.1:8000
```

Verifikasi backend berjalan dengan membuka:
```
http://127.0.0.1:8000/docs
```
Halaman Swagger UI akan muncul jika backend berhasil berjalan.

> **Catatan:** Saat pertama kali dijalankan, model MT5 akan dimuat ke memori. Proses ini membutuhkan beberapa detik. Tunggu hingga terminal menampilkan pesan `Model loaded successfully` sebelum menggunakan aplikasi.

---

### 5. Jalankan Frontend

> ⚠️ **JANGAN gunakan Live Server atau VS Code Live Preview** untuk membuka frontend. Kedua extension tersebut memiliki fitur auto-reload yang akan me-refresh halaman browser secara otomatis setiap kali backend menyimpan file PDF hasil ringkasan ke disk, menyebabkan proses fetch terputus dan hasil ringkasan tidak pernah ditampilkan.

**Cara yang benar — buka langsung dari File Explorer:**

1. Buka Windows File Explorer
2. Navigasi ke folder `Frontend`
3. Double-click file `index.html`
4. klik Reveal in file explorer dan klik fiel `index.html`
   

## Cara Penggunaan

1. Pastikan backend sudah berjalan di `http://127.0.0.1:8000`
2. Buka `index.html` via File Explorer seperti langkah di atas
3. Upload dokumen PDF, DOCX, atau TXT (maks. 10 MB)
4. Pilih rasio ringkasan: **30%** (Singkat), **50%** (Sedang), atau **80%** (Lengkap)
5. Klik tombol **Ringkas Dokumen**
6. Tunggu proses selesai — model MT5 memproses dokumen per chunk
7. Hasil ringkasan akan muncul otomatis
8. Gunakan tombol **Unduh PDF** atau **Salin** untuk menyimpan hasil

---

## Endpoint API

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/documents/summarize` | Upload & ringkas dokumen |
| GET | `/documents/download/pdf/{filename}` | Download hasil PDF |

---

## Catatan Penting

- Model hanya mendukung **Bahasa Indonesia** dan **Bahasa Inggris**
- Dokumen dengan teks yang sangat panjang akan diproses per chunk (setiap 3000 karakter)
- Waktu proses bergantung pada panjang dokumen dan spesifikasi hardware
- Pastikan RAM mencukupi sebelum memproses dokumen berukuran besar
