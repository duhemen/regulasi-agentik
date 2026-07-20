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

:: Cek NVIDIA
wmic path win32_VideoController get Name /value | findstr /I "NVIDIA" >nul
if %errorlevel% equ 0 (
    set "GPU_VENDOR=NVIDIA"
    goto GPU_FOUND
)

:: Cek AMD
wmic path win32_VideoController get Name /value | findstr /I "AMD" >nul
if %errorlevel% equ 0 (
    set "GPU_VENDOR=AMD"
    goto GPU_FOUND
)

:: Cek Intel Arc / Intel Graphics
wmic path win32_VideoController get Name /value | findstr /I "Intel" >nul
if %errorlevel% equ 0 (
    :: Memastikan apakah ini Intel HD biasa atau Intel Arc diskrit
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
    git clone https://github.com %FOLDER_NAME%
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
