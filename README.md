# ⚖️ LegalAI-Agent: Analis Regulasi & Kepatuhan AI Lokal

Aplikasi asisten hukum pintar berbasis **Multi-Agent Simulation** dan **Dinamis RAG (Retrieval-Augmented Generation)** yang berjalan 100% secara lokal (*on-premise*). Proyek ini dirancang untuk mematuhi **UU PDP No. 27/2022** dengan memastikan tidak ada satu pun data dokumen sensitif atau riwayat obrolan pengguna yang bocor ke server luar negeri.

Aplikasi ini mengombinasikan kekuatan **Qwen 2.5 7B** (sebagai analis teks regulasi) dan **DeepSeek-R1 8B** (sebagai pemikir sanksi mendalam) melalui kerangka kerja *round-robin* dari **Microsoft AutoGen (AG2)**.

---

## ⚡ Fitur Utama: Kustomisasi Agnostik Instansi & Regulasi (Customizable Context)
Kelebihan utama dari arsitektur **LegalAI-Agent** ini adalah sifatnya yang **modular dan adaptif**. Agen ini dapat dikostumisasi dengan sangat mudah untuk menyesuaikan kebutuhan berbagai jenis instansi, korporasi, institusi pemerintahan, maupun organisasi sektor swasta.

### 🏢 Contoh Skenario Implementasi Spesifik:
Aplikasi ini tidak hanya terbatas pada hukum publik digital nasional, tetapi juga dapat dialihfungsikan sebagai:

1. **Divisi Kepatuhan Internal (KI) Korporasi**:
   * **Cara Kerja**: Pengguna tinggal mengunggah dokumen Standard Operating Procedure (SOP), pakta integritas, peraturan direksi, kode etik karyawan, hingga Surat Keputusan (SK) internal perusahaan ke dalam sistem RAG lewat Sidebar.
   * **Output Agen**: Tim Agen AI otomatis akan menjelma menjadi auditor internal perusahaan. Mereka akan menganalisis apakah sebuah tindakan bisnis karyawan melanggar klausul kepatuhan internal (KI) perusahaan, serta mendeteksi risiko sanksi surat peringatan (SP) hingga pemutusan hubungan kerja (PHK) secara internal.
2. **Kepatuhan Sektoral Medis / Perbankan**:
   * Sistem dapat dipasangi dokumen regulasi ketat seperti aturan OJK (untuk Fintech/Bank) atau regulasi Kemenkes (untuk Rumah Sakit) agar agen bertindak sebagai penasihat kepatuhan kepatuhan sektoral khusus.
3. **Institusi Akademik / Kampus**:
   * Sistem dapat dipasangi peraturan rektor, pedoman plagiarisme, dan etika riset akademik untuk menyaring draf jurnal atau tindakan civitas akademika dari pelanggaran integritas ilmiah.

---

## 🛠️ Arsitektur Tim Agen AI
Sistem ini menggunakan metode komunikasi `round_robin` kaku untuk menjamin akurasi analisis tanpa adanya bias atau interupsi acak:
1. **Emen_Proxy (User Agent)**: Melemparkan studi kasus hukum atau pertanyaan pengguna ke ruang sidang digital.
2. **Analis_Hukum (Qwen 2.5 7B - GPU Bounded)**: Membedah basis data vektor RAG lokal dan menyajikan pasal-pasal undang-undang, dokumen kebijakan, atau aturan Kepatuhan Internal (KI) yang relevan secara presisi.
3. **Pengecek_Kepatuhan (DeepSeek-R1 8B - CPU Bounded)**: Melakukan penalaran mendalam (*chain-of-thought*) untuk mengidentifikasi potensi pelanggaran etika, sanksi administrasi/disiplin, denda materiil, hingga risiko pemutusan hak akses atau sanksi internal instansi terkait.


---

## 💻 Spesifikasi Sistem Minimum (Tested on Emen's Rig)
* **Prosesor (CPU)**: Intel Core i5 (Gen 11+) / AMD Ryzen 5 (Seri 5000+)
* **Kartu Grafis (GPU) Lintas Vendor**:
  * **NVIDIA**: GeForce RTX 3050 / 3060 / 4050 dengan minimal **VRAM 6GB - 8GB** (Mendukung akselerasi CUDA bawaan)
  * **AMD**: Radeon RX 6600 / 7600 atau seri di atasnya dengan **VRAM 8GB** (Didukung penuh oleh Ollama via arsitektur ROCm)
  * **Intel**: Intel Arc A580 / A750 / A770 dengan **VRAM 8GB** (Didukung oleh Ollama via akselerasi driver Intel oneAPI)
* **Memori RAM**: 16GB RAM (Dibutuhkan untuk memuat model penalaran di CPU)
* **Penyimpanan**: SSD dengan sisa ruang minimal 20GB (Untuk database vektor dan file model)
* **Backend LLM**: Ollama Lokal Server

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Kloning Repositori
```bash
git clone https://github.com/duhemen/regulasi-agentik
cd regulasi-agentik
```

### 2. Setup Virtual Environment
```powershell
# Membuat virtual environment
python -m venv env-agentik

# Mengaktifkan di Windows (PowerShell)
.\env-agentik\Scripts\Activate.ps1
```

### 3. Instalasi Modul Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server Model Lokal (Ollama)
Pastikan Anda sudah mengunduh kedua model ini di Ollama:
```bash
ollama run qwen2.5:7b-instruct
ollama run deepseek-r1:8b
```

### 5. Eksekusi Aplikasi Antarmuka (Streamlit UI)
```bash
streamlit run app.py
```
Buka peramban browser Anda dan akses halaman `http://localhost:8501`. Unggah 5 berkas PDF regulasi Anda di panel samping kiri (Sidebar) untuk melakukan proses *ingest* perdana!

---
*Dikembangkan dengan penuh dedikasi By YourSelf - Ingat LUCA sebagai pelopor kepatuhan AI lokal di Indonesia.* 🇮🇩
