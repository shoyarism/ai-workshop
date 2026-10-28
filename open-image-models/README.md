# Open-Source Image Generation Models Suite (BentoML Guide & Multi-Engine)

> Implementasi lengkap panduan resmi BentoML: [A Guide to Open-Source Image Generation Models (2026)](https://www.bentoml.com/blog/a-guide-to-open-source-image-generation-models), terintegrasi dengan ekosistem **Centralized Workshop OS**.

---

## 🌟 Fitur & Arsitektur Sistem

Sistem ini menggabungkan dua pilar utama sesuai panduan BentoML dan profil hardware host:

### 1. Local Diffusion Engine (Dioptimasi untuk GPU GTX 1650 4GB VRAM)
- **ComfyUI**: Visual node-based pipeline engine untuk kontrol penuh atas alur difusi, LoRA, sampling, dan chaining. Dikonfigurasi otomatis dengan flag `--lowvram` dan preview realtime.
- **SDXL-Lightning (ByteDance)**: Menghasilkan gambar resolusi tinggi hanya dalam **4 step** (dibandingkan 20-50 step pada SD standar), dengan `enable_model_cpu_offload` dan `enable_attention_slicing` untuk mencegah CUDA Out-of-Memory.
- **BentoML Service & comfy-pack**:
  - `service.py`: Menjadikan pipeline model difusi sebagai REST API siap produksi dengan OpenAPI/Swagger docs otomatis di port `3000`.
  - `pack_workflow.py`: Memaketkan workflow ComfyUI menjadi file `.cpack.zip` yang dapat di-share atau di-serve langsung sebagai microservice.

### 2. Cloud Engines (Gemini Imagen 3, FLUX Cloud, & Nano Banana)
Untuk model generasi gambar raksasa (seperti FLUX.2 32B atau Qwen-Image 20B) yang membutuhkan 24GB+ VRAM:
- **Google Imagen 3 / Gemini**: Kualitas fotorealisme dan render teks terbaik tanpa beban GPU lokal.
- **FLUX Cloud (FLUX.1 / FLUX.2)**: Mengakses model FLUX tercanggih langsung dari cloud endpoint berlatensi rendah.
- **Nano Banana**: Preset generasi gambar estetik ultra-cepat.

---

## 🚀 Panduan Penggunaan Cepat

### 1. Menjalankan ComfyUI (Local Node Interface)
Cukup double-click `run_comfyui.bat` atau jalankan:
```powershell
.\run_comfyui.bat
```
Buka browser di: **`http://127.0.0.1:8188`**.

---

### 2. Menjalankan Generator CLI (`generate.py`)

Gunakan virtual environment yang telah disediakan (`.venv`):

#### A. Cloud Mode (Rekomendasi untuk Kualitas SOTA & Render Cepat):
```powershell
# FLUX Cloud
.\.venv\Scripts\python.exe generate.py --prompt "futuristic cyberpunk city in neon rain" --provider cloud_flux

# Google Gemini / Imagen 3 (menggunakan GEMINI_API_KEY)
.\.venv\Scripts\python.exe generate.py --prompt "hyperrealistic portrait of a wise old sailor" --provider gemini

# Nano Banana (Creative Fast)
.\.venv\Scripts\python.exe generate.py --prompt "ethereal crystal forest at twilight" --provider nano_banana
```

#### B. Local Mode (SDXL-Lightning di GPU Lokal):
```powershell
.\.venv\Scripts\python.exe generate.py --prompt "modern minimalist villa by the cliff" --provider local --steps 4
```
Hasil gambar otomatis tersimpan di folder: `open-image-models\output\`.

---

### 3. Menjalankan BentoML REST API Service
Untuk menyajikan model sebagai API produksi:
```powershell
.\run_bento_service.bat
```
Akses Swagger UI interaktif di: **`http://127.0.0.1:3000`**.

---

### 4. Memaketkan Workflow ComfyUI (`comfy-pack`)
Sesuai rekomendasi artikel BentoML, Anda dapat memaketkan alur kerja ComfyUI:
```powershell
.\.venv\Scripts\python.exe pack_workflow.py pack "workflows/my_workflow.json" "my_workflow.cpack.zip"
.\.venv\Scripts\python.exe pack_workflow.py serve "my_workflow.cpack.zip"
```

---

## 📁 Struktur Direktori

```
open-image-models/
├── .venv/               # Virtual environment Python 3.11 (PyTorch CUDA, Diffusers, BentoML)
├── ComfyUI/             # Repositori resmi ComfyUI node-based engine
├── output/              # Direktori penyimpanan hasil generasi gambar
├── generate.py          # Unified CLI generator (Local & Cloud)
├── service.py           # BentoML production API service
├── bentofile.yaml       # Konfigurasi BentoML packaging
├── pack_workflow.py     # Helper comfy-pack untuk packaging workflow
├── run_comfyui.bat      # Launcher ComfyUI (GTX 1650 4GB Low-VRAM)
├── run_bento_service.bat# Launcher BentoML REST API
└── README.md            # Dokumentasi lengkap
```
