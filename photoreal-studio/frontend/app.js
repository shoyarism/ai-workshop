// Photoreal Studio Frontend Controller

let appState = {
  options: null,
  presets: null,
  activePresetKey: null,
  selectedAperture: "f/1.8",
  currentImage: null,
  currentMeta: null,
  loupeEnabled: true,
  debounceTimer: null,
  loadingInterval: null
};

// DOM Elements
const subjectInput = document.getElementById("subjectInput");
const enhancePromptBtn = document.getElementById("enhancePromptBtn");
const enhancementReasoning = document.getElementById("enhancementReasoning");
const cameraSelect = document.getElementById("cameraSelect");
const lensSelect = document.getElementById("lensSelect");
const lightingSelect = document.getElementById("lightingSelect");
const filmStockSelect = document.getElementById("filmStockSelect");
const aperturePills = document.getElementById("aperturePills");
const shutterInput = document.getElementById("shutterInput");
const isoInput = document.getElementById("isoInput");
const aspectRatioSelect = document.getElementById("aspectRatioSelect");
const skinRealismCheck = document.getElementById("skinRealismCheck");
const materialPhysicsCheck = document.getElementById("materialPhysicsCheck");
const providerSelect = document.getElementById("providerSelect");
const seedInput = document.getElementById("seedInput");
const randomSeedBtn = document.getElementById("randomSeedBtn");

const cameraDetails = document.getElementById("cameraDetails");
const lensDetails = document.getElementById("lensDetails");
const lightingDetails = document.getElementById("lightingDetails");
const filmDetails = document.getElementById("filmDetails");

const positivePromptText = document.getElementById("positivePromptText");
const negativePromptText = document.getElementById("negativePromptText");
const promptCharCount = document.getElementById("promptCharCount");

const generateBtn = document.getElementById("generateBtn");
const generateBtnText = document.getElementById("generateBtnText");
const loadingOverlay = document.getElementById("loadingOverlay");
const loadingStageText = document.getElementById("loadingStageText");
const emptyState = document.getElementById("emptyState");
const renderedImage = document.getElementById("renderedImage");
const magnifierLoupe = document.getElementById("magnifierLoupe");
const loupeContent = document.getElementById("loupeContent");
const toggleLoupeBtn = document.getElementById("toggleLoupeBtn");
const loupeStatusText = document.getElementById("loupeStatusText");
const downloadBtn = document.getElementById("downloadBtn");

const exifCard = document.getElementById("exifCard");
const exifCamera = document.getElementById("exifCamera");
const exifLens = document.getElementById("exifLens");
const exifExposure = document.getElementById("exifExposure");
const exifFilm = document.getElementById("exifFilm");
const generationTimeBadge = document.getElementById("generationTimeBadge");

const presetPillContainer = document.getElementById("presetPillContainer");
const galleryBtn = document.getElementById("galleryBtn");
const galleryCount = document.getElementById("galleryCount");
const galleryModal = document.getElementById("galleryModal");
const galleryGrid = document.getElementById("galleryGrid");
const closeGalleryBtn = document.getElementById("closeGalleryBtn");

const settingsBtn = document.getElementById("settingsBtn");
const settingsModal = document.getElementById("settingsModal");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const geminiKeyInput = document.getElementById("geminiKeyInput");
const hfTokenInput = document.getElementById("hfTokenInput");

// Initialize Application
async function initApp() {
  try {
    const [optRes, presRes, statusRes] = await Promise.all([
      fetch("/api/options").then(r => r.json()),
      fetch("/api/presets").then(r => r.json()),
      fetch("/api/status").then(r => r.json())
    ]);

    appState.options = optRes;
    appState.presets = presRes;

    renderOptions();
    renderPresets();
    updateGalleryCount();

    // Default to National Geographic Portrait preset
    loadPreset("national_geographic_portrait");

    if (statusRes.has_gemini_key) {
      geminiKeyInput.placeholder = "•••••••••••••••• (Active in .env)";
    }
    if (statusRes.has_hf_token) {
      hfTokenInput.placeholder = "•••••••••••••••• (Active in .env)";
    }

    setupEventListeners();
  } catch (err) {
    console.error("Initialization error:", err);
    showToast("Failed to connect to backend", "⚠️");
  }
}

function renderOptions() {
  const { cameras, lenses, lighting, film_stocks, apertures } = appState.options;

  // Populate Cameras
  cameraSelect.innerHTML = cameras.map(c => 
    `<option value="${c.id}">${c.name}</option>`
  ).join("");

  // Populate Lenses
  lensSelect.innerHTML = lenses.map(l => 
    `<option value="${l.id}">${l.name}</option>`
  ).join("");

  // Populate Lighting
  lightingSelect.innerHTML = lighting.map(li => 
    `<option value="${li.id}">${li.name}</option>`
  ).join("");

  // Populate Film Stocks
  filmStockSelect.innerHTML = film_stocks.map(f => 
    `<option value="${f.id}">${f.name}</option>`
  ).join("");

  // Populate Aperture Pills
  aperturePills.innerHTML = apertures.map(ap => 
    `<button type="button" data-aperture="${ap}" class="aperture-pill px-2.5 py-1 text-xs rounded-lg font-mono border border-slate-700 bg-slate-900/90 text-slate-300 hover:border-amber-400/60 ${ap === appState.selectedAperture ? 'active' : ''}">${ap}</button>`
  ).join("");

  updateDescriptions();
}

function renderPresets() {
  const keys = Object.keys(appState.presets);
  presetPillContainer.innerHTML = keys.map(k => {
    const p = appState.presets[k];
    const icon = getPresetIcon(k);
    return `<button data-preset="${k}" class="preset-pill px-2.5 py-1 text-xs font-medium text-slate-300 hover:text-white rounded-lg border border-transparent hover:border-slate-700 transition flex items-center space-x-1">
      <span>${icon}</span>
      <span>${p.title.split(" ")[0]}</span>
    </button>`;
  }).join("");
}

function getPresetIcon(key) {
  switch (key) {
    case "national_geographic_portrait": return "📸";
    case "kyoto_artisan_workshop": return "🍵";
    case "high_fashion_editorial": return "👗";
    case "candid_street_reportage": return "🌧️";
    case "cinematic_movie_still": return "🎬";
    case "macro_hyperrealism": return "🔬";
    default: return "✨";
  }
}

function updateDescriptions() {
  const cam = appState.options.cameras.find(c => c.id === cameraSelect.value);
  if (cam) cameraDetails.textContent = cam.sensor;

  const lens = appState.options.lenses.find(l => l.id === lensSelect.value);
  if (lens) lensDetails.textContent = `${lens.focal_length} • ${lens.optical || lens.bokeh || ''}`;

  const light = appState.options.lighting.find(l => l.id === lightingSelect.value);
  if (light) lightingDetails.textContent = light.phrase || light.catchlight || '';

  const film = appState.options.film_stocks.find(f => f.id === filmStockSelect.value);
  if (film) filmDetails.textContent = film.phrase || `${film.tone || ''} • ${film.color || ''}`;
}

function setupEventListeners() {
  // Option Change Listeners
  [cameraSelect, lensSelect, lightingSelect, filmStockSelect, aspectRatioSelect].forEach(el => {
    el.addEventListener("change", () => {
      updateDescriptions();
      scheduleSynthesis();
    });
  });

  [shutterInput, isoInput].forEach(el => {
    el.addEventListener("input", scheduleSynthesis);
  });

  [skinRealismCheck, materialPhysicsCheck].forEach(el => {
    el.addEventListener("change", scheduleSynthesis);
  });

  subjectInput.addEventListener("input", scheduleSynthesis);

  // Aperture Pills Click
  aperturePills.addEventListener("click", e => {
    const btn = e.target.closest("[data-aperture]");
    if (!btn) return;
    appState.selectedAperture = btn.dataset.aperture;
    document.querySelectorAll(".aperture-pill").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    scheduleSynthesis();
  });

  // Preset Pills Click
  presetPillContainer.addEventListener("click", e => {
    const btn = e.target.closest("[data-preset]");
    if (!btn) return;
    loadPreset(btn.dataset.preset);
  });

  // Idea Chips Click
  document.querySelectorAll(".idea-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      subjectInput.value = chip.textContent;
      enhancementReasoning.classList.add("hidden");
      scheduleSynthesis();
      showToast(`Loaded idea: "${chip.textContent}"`, "💡");
    });
  });

  // Magic Prompt Enhancer
  enhancePromptBtn.addEventListener("click", async () => {
    const subject = subjectInput.value.trim();
    if (!subject) {
      showToast("Please enter a subject first", "⚠️");
      return;
    }
    enhancePromptBtn.disabled = true;
    enhancePromptBtn.innerHTML = `<span>⏳ Enhancing...</span>`;
    try {
      const res = await fetch("/api/enhance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject })
      });
      const data = await res.json();
      if (data.enhanced_subject) {
        subjectInput.value = data.enhanced_subject;
        if (data.reasoning) {
          enhancementReasoning.textContent = `Director Note: ${data.reasoning}`;
          enhancementReasoning.classList.remove("hidden");
        }
        scheduleSynthesis();
        showToast("Concept enhanced with photographic sensory physics!", "✨");
      }
    } catch (err) {
      showToast("Enhancement failed", "❌");
    } finally {
      enhancePromptBtn.disabled = false;
      enhancePromptBtn.innerHTML = `<span>✨ Magic Enhance</span>`;
    }
  });

  // Random Seed
  randomSeedBtn.addEventListener("click", () => {
    seedInput.value = Math.floor(Math.random() * 90000000) + 100000;
  });

  // Generate Action
  generateBtn.addEventListener("click", generateImage);

  // Loupe Toggle
  toggleLoupeBtn.addEventListener("click", () => {
    appState.loupeEnabled = !appState.loupeEnabled;
    loupeStatusText.textContent = appState.loupeEnabled ? "ON" : "OFF";
    loupeStatusText.className = appState.loupeEnabled ? "text-amber-400" : "text-slate-500";
    if (!appState.loupeEnabled) magnifierLoupe.classList.add("hidden");
  });

  // Magnifier Loupe Mousemove
  const viewportFrame = document.getElementById("viewportFrame");
  viewportFrame.addEventListener("mousemove", handleLoupeMove);
  viewportFrame.addEventListener("mouseleave", () => {
    magnifierLoupe.classList.add("hidden");
  });

  // Download Button
  downloadBtn.addEventListener("click", () => {
    if (!appState.currentImage) return;
    const a = document.createElement("a");
    a.href = appState.currentImage;
    a.download = appState.currentMeta?.filename || "photoreal_master.jpg";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });

  // Gallery Modal
  galleryBtn.addEventListener("click", openGallery);
  closeGalleryBtn.addEventListener("click", () => galleryModal.classList.add("hidden"));

  // Settings Modal
  settingsBtn.addEventListener("click", () => settingsModal.classList.remove("hidden"));
  closeSettingsBtn.addEventListener("click", () => settingsModal.classList.add("hidden"));
  saveSettingsBtn.addEventListener("click", saveSettings);
}

function loadPreset(presetKey) {
  const preset = appState.presets[presetKey];
  if (!preset) return;

  appState.activePresetKey = presetKey;
  document.querySelectorAll(".preset-pill").forEach(p => {
    p.classList.toggle("active", p.dataset.preset === presetKey);
  });

  subjectInput.value = preset.subject_hint;
  cameraSelect.value = preset.camera;
  lensSelect.value = preset.lens;
  lightingSelect.value = preset.lighting;
  filmStockSelect.value = preset.film_stock;
  shutterInput.value = preset.shutter;
  isoInput.value = preset.iso;
  aspectRatioSelect.value = preset.aspect_ratio || "3:4";

  appState.selectedAperture = preset.aperture;
  document.querySelectorAll(".aperture-pill").forEach(p => {
    p.classList.toggle("active", p.dataset.aperture === preset.aperture);
  });

  enhancementReasoning.classList.add("hidden");
  updateDescriptions();
  scheduleSynthesis();
  showToast(`Loaded Preset: ${preset.title}`, "📸");
}

function scheduleSynthesis() {
  clearTimeout(appState.debounceTimer);
  appState.debounceTimer = setTimeout(synthesizePrompts, 180);
}

async function synthesizePrompts() {
  const payload = {
    subject: subjectInput.value.trim() || "unspecified subject",
    camera_key: cameraSelect.value,
    lens_key: lensSelect.value,
    aperture: appState.selectedAperture,
    lighting_key: lightingSelect.value,
    film_stock_key: filmStockSelect.value,
    include_skin_realism: skinRealismCheck.checked,
    include_material_physics: materialPhysicsCheck.checked,
    aspect_ratio: aspectRatioSelect.value,
    custom_shutter: shutterInput.value,
    custom_iso: parseInt(isoInput.value) || 200
  };

  try {
    const res = await fetch("/api/synthesize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    positivePromptText.value = data.positive_prompt;
    negativePromptText.value = data.negative_prompt;
    promptCharCount.textContent = `${data.positive_prompt.length} chars`;
  } catch (err) {
    console.error("Synthesis error:", err);
  }
}

async function generateImage() {
  const subject = subjectInput.value.trim();
  if (!subject) {
    showToast("Please describe a subject to photograph", "⚠️");
    return;
  }

  // UI state: Loading
  generateBtn.disabled = true;
  generateBtnText.textContent = "Capturing Master Photograph...";
  loadingOverlay.classList.remove("hidden");
  renderedImage.classList.add("hidden");
  magnifierLoupe.classList.add("hidden");

  // Cycle loading messages for realism feedback
  const stages = [
    "Simulating sensor dynamic range & ISO acutance...",
    "Computing epidermal subsurface scattering (SSS)...",
    "Tracing Fresnel reflections & corneal specular highlights...",
    "Rendering prime lens spherical bokeh & chromatic purity...",
    "Applying organic film emulsion tone curve..."
  ];
  let stageIdx = 0;
  loadingStageText.textContent = stages[0];
  appState.loadingInterval = setInterval(() => {
    stageIdx = (stageIdx + 1) % stages.length;
    loadingStageText.textContent = stages[stageIdx];
  }, 3500);

  const payload = {
    subject: subject,
    camera_key: cameraSelect.value,
    lens_key: lensSelect.value,
    aperture: appState.selectedAperture,
    lighting_key: lightingSelect.value,
    film_stock_key: filmStockSelect.value,
    include_skin_realism: skinRealismCheck.checked,
    include_material_physics: materialPhysicsCheck.checked,
    aspect_ratio: aspectRatioSelect.value,
    custom_shutter: shutterInput.value,
    custom_iso: parseInt(isoInput.value) || 200,
    provider: providerSelect.value,
    seed: parseInt(seedInput.value) || 0,
    custom_positive_prompt: positivePromptText.value,
    custom_negative_prompt: negativePromptText.value
  };

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }

    const data = await res.json();
    displayGeneratedImage(data);
    updateGalleryCount();
    showToast("Master photograph generated successfully!", "✨");
  } catch (err) {
    console.error("Generation error:", err);
    showToast("Generation encountered an error", "❌");
  } finally {
    clearInterval(appState.loadingInterval);
    loadingOverlay.classList.add("hidden");
    generateBtn.disabled = false;
    generateBtnText.textContent = "Generate Master Photograph";
  }
}

function displayGeneratedImage(meta) {
  appState.currentImage = meta.image_url;
  appState.currentMeta = meta;

  emptyState.classList.add("hidden");
  renderedImage.src = meta.image_url;
  renderedImage.classList.remove("hidden");

  // Update EXIF slate
  exifCard.classList.remove("hidden");
  exifCamera.textContent = `${meta.camera} (${meta.provider})`;
  exifLens.textContent = `${meta.lens}`;
  exifExposure.textContent = `${meta.aperture} • ${meta.shutter} • ISO ${meta.iso}`;
  exifFilm.textContent = meta.film_stock;

  generationTimeBadge.textContent = `${meta.generation_time_seconds}s • ${meta.dimensions.width}x${meta.dimensions.height}`;
  generationTimeBadge.classList.remove("hidden");

  // Pre-cache image for Loupe
  loupeContent.style.backgroundImage = `url('${meta.image_url}')`;

  if (meta.warning) {
    setTimeout(() => {
      showToast(meta.warning, "⚠️");
    }, 800);
  }
}

function handleLoupeMove(e) {
  if (!appState.loupeEnabled || !appState.currentImage || renderedImage.classList.contains("hidden")) {
    magnifierLoupe.classList.add("hidden");
    return;
  }

  const rect = renderedImage.getBoundingClientRect();
  const frameRect = document.getElementById("viewportFrame").getBoundingClientRect();

  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  // Only show when hovering directly over the image
  if (mouseX < 0 || mouseY < 0 || mouseX > rect.width || mouseY > rect.height) {
    magnifierLoupe.classList.add("hidden");
    return;
  }

  magnifierLoupe.classList.remove("hidden");

  // Position loupe centered at cursor relative to viewport frame
  const loupeX = e.clientX - frameRect.left - 96;
  const loupeY = e.clientY - frameRect.top - 96;
  magnifierLoupe.style.left = `${loupeX}px`;
  magnifierLoupe.style.top = `${loupeY}px`;

  // Magnify 3.5x
  const zoom = 3.5;
  const bgX = -((mouseX / rect.width) * (rect.width * zoom) - 96);
  const bgY = -((mouseY / rect.height) * (rect.height * zoom) - 96);

  loupeContent.style.width = `${rect.width * zoom}px`;
  loupeContent.style.height = `${rect.height * zoom}px`;
  loupeContent.style.transform = `translate(${bgX}px, ${bgY}px)`;
  loupeContent.style.backgroundSize = `${rect.width * zoom}px ${rect.height * zoom}px`;
}

async function updateGalleryCount() {
  try {
    const res = await fetch("/api/gallery");
    const items = await res.json();
    galleryCount.textContent = items.length;
  } catch (e) {}
}

async function openGallery() {
  galleryModal.classList.remove("hidden");
  try {
    const res = await fetch("/api/gallery");
    const items = await res.json();
    if (items.length === 0) {
      galleryGrid.innerHTML = `<div class="col-span-2 text-center text-slate-500 py-12 text-sm">No photographs saved yet.</div>`;
      return;
    }
    galleryGrid.innerHTML = items.map(item => `
      <div class="bg-[#161a24] border border-slate-800 rounded-xl overflow-hidden hover:border-amber-400/60 transition cursor-pointer group" onclick='loadGalleryItem(${JSON.stringify(item).replace(/'/g, "&#39;")})'>
        <div class="aspect-[4/3] bg-black relative overflow-hidden">
          <img src="${item.image_url}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
          <div class="absolute bottom-1 right-1 px-1.5 py-0.5 bg-black/70 rounded text-[10px] font-mono text-amber-300">${item.aperture}</div>
        </div>
        <div class="p-3 text-xs">
          <p class="font-medium text-slate-200 truncate">${item.subject}</p>
          <p class="text-slate-500 text-[11px] mt-0.5">${item.camera} • ${item.created_at}</p>
        </div>
      </div>
    `).join("");
  } catch (err) {
    console.error("Gallery load error:", err);
  }
}

window.loadGalleryItem = function(item) {
  displayGeneratedImage(item);
  subjectInput.value = item.subject;
  positivePromptText.value = item.positive_prompt;
  negativePromptText.value = item.negative_prompt;
  galleryModal.classList.add("hidden");
  showToast("Loaded image from gallery", "🖼️");
};

async function saveSettings() {
  const payload = {
    gemini_api_key: geminiKeyInput.value.trim() || null,
    hf_token: hfTokenInput.value.trim() || null
  };
  try {
    await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    settingsModal.classList.add("hidden");
    showToast("API credentials updated", "🔑");
  } catch (err) {
    showToast("Failed to save credentials", "❌");
  }
}

function showToast(msg, icon = "✨") {
  const toast = document.getElementById("toast");
  document.getElementById("toastText").textContent = msg;
  document.getElementById("toastIcon").textContent = icon;
  toast.classList.remove("translate-y-20", "opacity-0");
  toast.classList.add("translate-y-0", "opacity-100");
  setTimeout(() => {
    toast.classList.add("translate-y-20", "opacity-0");
    toast.classList.remove("translate-y-0", "opacity-100");
  }, 3000);
}

// Kick off app
initApp();