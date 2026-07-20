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
## 💾 Jalur Pintas: Instalasi Otomatis (Khusus Windows)

Bagi pengguna awam yang ingin memasang aplikasi ini tanpa perlu mengetik perintah terminal satu per satu, Anda bisa menggunakan skrip installer otomatis berbasis deteksi hardware.

### Langkah-langkah Penggunaan:
1. Unduh atau buat file baru bernama `installer.bat` di **Desktop** atau direktori pilihan Anda (misal: `C:\`).
2. Masukkan kode skrip otomatis di bawah ini ke dalam file tersebut menggunakan Notepad, lalu simpan.
3. **Klik kanan** pada file `installer.bat` tersebut, lalu pilih **"Run as administrator"** (Penting: Jalur Drive C membutuhkan izin akses sistem).
4. **Duar!** Skrip akan otomatis mendeteksi kartu grafis Anda (NVIDIA/AMD/Intel Arc), mengkloning kode, menyiapkan Virtual Environment, mengunduh model AI ke Ollama, dan langsung meluncurkan antarmuka Streamlit.

### Kode Skrip `installer.bat`:
```batch
@echo off
title LegalAI-Agent Auto-Installer & GPU Detector
color 0A
cls

echo ===================================================
echo 🔥 LEGALAI-AGENT: AUTO-INSTALLER + DETEKSI GPU 🔥
echo ===================================================
echo [*] Memeriksa spesifikasi perangkat keras Anda...
echo ---------------------------------------------------

:: 1. DETEKSI GPU OTOMATIS
set "GPU_VENDOR=UNKNOWN"

wmic path win32_VideoController get Name /value | findstr /I "NVIDIA" >nul
if %errorlevel% equ 0 (
    set "GPU_VENDOR=NVIDIA"
    goto GPU_FOUND
)

wmic path win32_VideoController get Name /value | findstr /I "AMD" >nul
if %errorlevel% equ 0 (
    set "GPU_VENDOR=AMD"
    goto GPU_FOUND
)

wmic path win32_VideoController get Name /value | findstr /I "Intel" >nul
if %errorlevel% equ 0 (
    wmic path win32_VideoController get Name /value | findstr /I "Arc" >nul
    if %errorlevel% equ 0 (
        set "GPU_VENDOR=INTEL_ARC"
    ) else (
        set "GPU_VENDOR=INTEL_INTEGRATED"
    )
    goto GPU_FOUND
)

:GPU_FOUND
echo ---------------------------------------------------
if "%GPU_VENDOR%"=="NVIDIA" (
    echo [v] GPU Terdeteksi: NVIDIA GeForce / RTX Series!
    echo [!] Akselerasi penuh via CUDA Aktif Otomatis.
) else if "%GPU_VENDOR%"=="AMD" (
    echo [v] GPU Terdeteksi: AMD Radeon Series!
    echo [!] Akselerasi via ROCm / DirectML diaktifkan.
) else if "%GPU_VENDOR%"=="INTEL_ARC" (
    echo [v] GPU Terdeteksi: Intel Arc Dedicated GPU!
    echo [!] Akselerasi via Intel oneAPI / Level Zero diaktifkan.
) else if "%GPU_VENDOR%"=="INTEL_INTEGRATED" (
    echo [!] GPU Terdeteksi: Intel Integrated Graphics (Onboard).
    echo [!] Aplikasi tetap berjalan, namun beban penalaran akan dialihkan ke CPU.
) else (
    echo [?] GPU Spesifik Tidak Terdeteksi (Standard Display Adapter).
    echo [!] Sistem akan berjalan dalam Mode Komputasi CPU murni.
)
echo ---------------------------------------------------
echo.
timeout /t 3 >nul

:: 2. VERIFIKASI GIT DAN PYTHON
echo [*] Memeriksa komponen sistem pendukung...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Eror: Git belum terpasang di komputer ini!
    echo [!] Silakan pasang Git terlebih dahulu agar skrip dapat mengunduh repositori.
    pause
    exit
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Eror: Python belum terpasang di komputer ini!
    echo [!] Silakan pasang Python 3.10+ terlebih dahulu.
    pause
    exit
)

:: 3. PROSES UNDUH & EKSTRAK REPOSITORI
set "FOLDER_NAME=LegalAI-Agent-App"
if not exist "%FOLDER_NAME%" (
    echo [*] Mengkloning repositori duhemen/regulasi-agentik dari GitHub...
    git clone https://github.com/duhemen/regulasi-agentik %FOLDER_NAME%
)
cd %FOLDER_NAME%

:: 4. BUAT VIRTUAL ENVIRONMENT & PIP INSTALL
if not exist "env-agentik" (
    echo [*] Membuat ruang virtual Python lokal (env-agentik)...
    python -m venv env-agentik
)

echo [*] Memasang pustaka dependensi (Proses download dimulai)...
call .\env-agentik\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

:: 5. MEMASTIKAN MODEL OLLAMA TERPASANG DAN BERJALAN
echo [*] Memeriksa konektivitas ke server lokal Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Eror: Aplikasi Ollama tidak merespons!
    echo [!] Harap buka aplikasi Ollama Anda di Windows terlebih dahulu.
    pause
    exit
)

echo [*] Mengunduh/Memverifikasi model kecerdasan buatan (Ini memerlukan waktu)...
echo [*] Menyiapkan Analis Hukum (Qwen 2.5 7B)...
ollama pull qwen2.5:7b-instruct
echo [*] Menyiapkan Pengecek Kepatuhan (DeepSeek-R1 8B)...
ollama pull deepseek-r1:8b

:: 6. DUAR! JALANKAN STREAMLIT
echo ===================================================
echo 🎉 SELESAI! SEMUA KEBUTUHAN TELAH SIAP.
echo 🎉 MELUNCURKAN ANTARMUKA STREAMLIT UI... DUAR!
echo ===================================================
timeout /t 2 >nul
streamlit run app.py

pause
```


## 🖥️ Panduan Operasional Antarmuka (Streamlit UI)

Setelah jendela browser terbuka otomatis, ikuti skema pengujian berikut untuk memulai analisis hukum:

1. **Panel Samping (Sidebar Left)**:
   * Anda akan melihat tombol unggah dokumen. Sistem sudah menyediakan beberapa sampel berkas PDF regulasi nasional di dalam folder utama.
   * Unggah dokumen tersebut, lalu tunggu hingga indikator berubah menjadi *Success* (Proses pembuatan database vektor lokal selesai).
2. **Kolom Studi Kasus (Main Chat)**:
   * Masukkan skenario pelanggaran atau pertanyaan hukum pada kolom chat bawah.
   * *Contoh Pertanyaan*: "Sebuah startup fintech tidak sengaja membocorkan 10.000 data KTP pengguna ke forum publik karena kelalaian sistem cloud. Apa pasal yang dilanggar dan bagaimana analisis sanksinya?"
3. **Simulasi Ruang Sidang Digital**:
   * **Analis_Hukum** akan mengetik terlebih dahulu untuk menampilkan pasal spesifik dari UU PDP No. 27/2022.
   * **Pengecek_Kepatuhan** (DeepSeek-R1) akan melanjutkan analisis secara mendalam untuk merinci denda materiil hingga sanksi administratif institusional.

> ⚠️ **CATATAN PENTING UNTUK BERKAS PDF**: 
> Pastikan dokumen regulasi yang Anda unggah berbentuk **Soft-File PDF Asli (Text-Based PDF)**, b**bukan dokumen hasil cetak yang di-scan atau difoto (Image-Based PDF)**. 
> Sistem RAG lokal saat ini memerlukan teks digital mentah agar dapat melakukan screening, pemecahan bab (chunking), dan ekstraksi pasal secara akurat tanpa memerlukan komponen OCR tambahan.

---
*Dikembangkan dengan penuh dedikasi By YourSelf - Ingat LUCA sebagai pelopor kepatuhan AI lokal di Indonesia.* 🇮🇩
