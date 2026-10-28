# Photoreal Studio — Ultra-Realistic AI Image Generation System

> An advanced optical physics, biometric micro-texture, and prompt synthesis engine designed to bridge the "uncanny valley" and produce AI-generated images indistinguishable from real photography.

![Photoreal Studio Banner](/static/style.css)

---

## 🌟 Key Features

1. **Optics & Gear Profiler**:
   - **Camera Bodies**: Hasselblad H6D-100c (Medium Format), Leica M11-P (Rangefinder), Sony α7R V, ARRI Alexa 35 (Cinema), Canon EOS R5, Classic 35mm SLR.
   - **Prime Lenses**: Carl Zeiss Otus 85mm f/1.4, Leica Noctilux-M 50mm f/0.95 ASPH, Canon RF 85mm f/1.2L DS, Cooke Anamorphic /i 40mm, Voigtländer Nokton 35mm f/1.2, Nikon Plena 135mm f/1.8.
   - **Aperture & Shutter Physics**: f/0.95 to f/11 with realistic circle of confusion (CoC), lens breathing, and bokeh discs.

2. **Biometric & Material Physics Engine**:
   - **Skin Micro-Pores & SSS**: Simulates genuine epidermal pores, fine vellus hair (peach fuzz), and subsurface scattering through tissue (ears, nose bridge).
   - **Eye Realism**: Iris radial crypts, natural moisture waterline meniscus, and corneal specular catchlights geometrically aligned with lighting sources.
   - **Surface & Fabric Physics**: Textile thread weave, natural garment folds, surface dust motes, and physical Fresnel reflection laws.

3. **Anti-CGI Realism Shield**:
   - Systematically purges artificial artifacts: plastic doll skin, wax-figure sheen, airbrushed textures, 3D render cliches, and hyper-smoothed filters.

4. **Multi-Provider Architecture**:
   - **Flux Realism Cloud Engine (Default)**: Instant high-fidelity cloud generation with **zero API keys** and **no local GPU load**.
   - **Google Imagen 3 / Gemini**: Ultra-photorealistic commercial studio generation via your Google API key.
   - **Hugging Face FLUX.1**: Connect your Hugging Face inference tokens.

5. **Modern Interactive Web Studio**:
   - Dark-mode glassmorphic interface inspired by Leica and cinema grading suites.
   - **300% Micro-Detail Loupe**: Inspect individual pores, eyelashes, and optical bokeh directly on the canvas.
   - **Photographic EXIF Slate**: Automatically tags and displays virtual camera, lens, aperture, shutter, ISO, film stock, and seed.
   - **Session Gallery**: Automatically logs all generated photographs with full metadata sidecars.

---

## 🚀 Quick Start

### 1. Launch the Web Studio
Double-click `run_studio.bat` or run:
```powershell
python run_studio.py
```
This boots the server and automatically opens `http://127.0.0.1:8000` in your browser.

---

### 2. Command-Line Interface (CLI)
You can also synthesize prompts and generate images directly from PowerShell:

#### Generate using a Master Preset:
```powershell
python cli.py "elderly fisherman in Greenland" --preset national_geographic_portrait
```

#### Custom Photographic Rig:
```powershell
python cli.py "fashion model in silk trench coat" --camera hasselblad_h6d --lens nikon_plena_135 --aperture f/2.0 --lighting studio_softbox --film kodak_portra_400
```

#### Enhance Concept with AI Prompt Expander:
```powershell
python cli.py "rainy night alley in Shinjuku" --enhance --aspect 16:9
```

#### List Available Presets:
```powershell
python cli.py --list-presets
```

#### Preview Synthesized Prompt Only (No Generation):
```powershell
python cli.py "monk in Tibetan monastery" --prompt-only
```

---

## 📸 Master Realism Presets

| Preset | Camera | Lens | Lighting | Film Stock | Description |
|---|---|---|---|---|---|
| **National Geographic** | Leica M11-P | Zeiss Otus 85mm | Rembrandt Key | Kodachrome 64 | Weathered character portrait, lifelike skin folds & storytelling eyes |
| **Vogue Editorial** | Hasselblad H6D | Nikon Plena 135mm | Octabox Softbox | Kodak Portra 400 | Medium-format separation, fabric weave clarity & haute couture elegance |
| **Rainy Tokyo Street** | Leica M11-P | Voigtländer 35mm | Practical Neon | CineStill 800T | Candid 35mm urban reportage with asphalt reflections & neon halation |
| **Anamorphic Cinema** | ARRI Alexa 35 | Cooke Anamorphic 40mm | Golden Hour | Digital RAW | Widescreen cinema frame with horizontal oval bokeh & organic flare |
| **Macro Biology** | Sony α7R V | Zeiss Otus 85mm | Diffused Window | Digital RAW | Microscopic surface physics, dewdrop surface tension & cellular detail |
| **Magnum B&W** | Leica M11-P | Leica Noctilux 50mm | Chiaroscuro | Kodak Tri-X 400 | Timeless photojournalism with deep silver-halide grain & dramatic shadows |

---

## 🧪 Project Structure

```
ultra-realistic-image-studio/
├── engine/
│   ├── photoreal_engine.py    # Optics, lenses, sensors, lighting, film stocks & synthesis
│   └── prompt_enhancer.py     # Director-grade sensory prompt expander & category detector
├── backend/
│   ├── generator.py           # Multi-provider generator (Flux Realism, Imagen 3, HuggingFace)
│   └── server.py              # FastAPI REST API & static file server
├── frontend/
│   ├── index.html             # Studio UI layout & control panels
│   ├── style.css              # Glassmorphism dark photography theme
│   └── app.js                 # Interactive controls, 300% detail loupe, gallery manager
├── output/                    # Generated high-res photographs & JSON metadata sidecars
├── cli.py                     # Developer command-line interface
├── run_studio.py              # Web studio launcher
├── run_studio.bat             # Windows one-click launcher
├── test_system.py             # Automated unit & integration verification suite
└── README.md                  # System documentation
```

---

## 🔑 Adding Optional API Keys

Photoreal Studio works **completely out of the box** without any keys using the built-in Flux Realism cloud engine.

If you wish to enable Google Imagen 3 or Hugging Face FLUX.1:
1. Open the Web Studio and click **API Keys** in the top right.
2. Enter your `GEMINI_API_KEY` or `HF_TOKEN`.
3. Or set them in your environment:
   ```powershell
   $env:GEMINI_API_KEY="your-gemini-key"
   $env:HF_TOKEN="your-hf-token"
   ```

---

## 🛠️ Verification & Automated Tests
Run the test suite anytime:
```powershell
python test_system.py
```