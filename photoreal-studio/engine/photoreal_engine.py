# -*- coding: utf-8 -*-
"""
Photoreal Realism Engine: Optics, Physics, and Natural Language Synthesis for FLUX and Modern Diffusion Models.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CameraProfile:
    name: str
    body: str
    sensor_phrase: str


@dataclass
class LensProfile:
    name: str
    focal_length: str
    optical_phrase: str


@dataclass
class LightingProfile:
    name: str
    phrase: str


@dataclass
class FilmStock:
    name: str
    phrase: str


CAMERA_PROFILES: Dict[str, CameraProfile] = {
    "leica_m11": CameraProfile(
        name="Leica M11-P",
        body="Leica M11-P rangefinder",
        sensor_phrase="candid documentary style with organic Leica color fidelity and subtle highlight roll-off"
    ),
    "hasselblad_h6d": CameraProfile(
        name="Hasselblad H6D-100c",
        body="Hasselblad H6D-100c medium format camera",
        sensor_phrase="medium format depth of field, exceptional tonal gradations, and ultra-sharp texture rendering"
    ),
    "sony_a7rv": CameraProfile(
        name="Sony α7R V",
        body="Sony α7R V mirrorless camera",
        sensor_phrase="crisp high-resolution digital clarity, sharp edge acutance, and true-to-life colors"
    ),
    "arri_alexa35": CameraProfile(
        name="ARRI Alexa 35",
        body="ARRI Alexa 35 cinema camera",
        sensor_phrase="cinematic filmic color science, smooth logarithmic highlight transitions, and lifelike skin tones"
    ),
    "canon_eos_r5": CameraProfile(
        name="Canon EOS R5",
        body="Canon EOS R5 camera",
        sensor_phrase="editorial commercial color balance and warm organic skin undertones"
    ),
    "analog_35mm": CameraProfile(
        name="35mm Mechanical SLR",
        body="classic 35mm SLR camera",
        sensor_phrase="authentic analog grain, gentle halation, and nostalgic film warmth"
    )
}

LENS_PROFILES: Dict[str, LensProfile] = {
    "zeiss_otus_85": LensProfile(
        name="Carl Zeiss Otus 85mm f/1.4",
        focal_length="85mm prime lens",
        optical_phrase="creamy spherical bokeh discs and pristine corner-to-corner micro-contrast"
    ),
    "leica_noctilux_50": LensProfile(
        name="Leica Noctilux-M 50mm f/0.95",
        focal_length="50mm prime lens",
        optical_phrase="dreamy painterly background separation and iconic shallow depth of field"
    ),
    "canon_85_ds": LensProfile(
        name="Canon RF 85mm f/1.2L DS",
        focal_length="85mm prime lens",
        optical_phrase="defocus smoothing with velvety blur circles and flattering facial perspective"
    ),
    "cooke_anamorphic_40": LensProfile(
        name="Cooke Anamorphic 40mm",
        focal_length="40mm anamorphic lens",
        optical_phrase="horizontal oval bokeh, subtle anamorphic lens flare, and widescreen cinematic perspective"
    ),
    "voigtlander_35": LensProfile(
        name="Voigtländer Nokton 35mm f/1.2",
        focal_length="35mm prime lens",
        optical_phrase="natural documentary perspective and gentle vintage optical character"
    ),
    "nikon_plena_135": LensProfile(
        name="Nikon NIKKOR Z 135mm f/1.8 Plena",
        focal_length="135mm telephoto lens",
        optical_phrase="circular bokeh edge-to-edge with strong telephoto subject isolation"
    )
}

LIGHTING_PROFILES: Dict[str, LightingProfile] = {
    "rembrandt": LightingProfile(
        name="Rembrandt Portrait Lighting",
        phrase="directional 45-degree key light casting a soft triangle of light on the cheek, with natural catchlights in the eyes"
    ),
    "golden_hour": LightingProfile(
        name="Golden Hour Sunlight",
        phrase="warm low-angle late afternoon sunlight casting soft elongated shadows with golden rim highlights"
    ),
    "diffused_window": LightingProfile(
        name="Diffused Window Daylight",
        phrase="soft natural daylight streaming from a nearby window, illuminating the subject with gentle wrap-around light"
    ),
    "studio_softbox": LightingProfile(
        name="Commercial Studio Octabox",
        phrase="diffused large studio softbox lighting with balanced fill and circular catchlights in the pupils"
    ),
    "chiaroscuro": LightingProfile(
        name="Dramatic Chiaroscuro",
        phrase="high-contrast theatrical lighting inspired by Caravaggio, with a single light source emerging from rich deep shadows"
    ),
    "cinematic_neon": LightingProfile(
        name="Cinematic Night & Neon",
        phrase="nocturnal ambient street lighting with subtle neon reflections, damp pavement bounce, and moody practical lamps"
    )
}

FILM_STOCKS: Dict[str, FilmStock] = {
    "kodak_portra_400": FilmStock(
        name="Kodak Portra 400",
        phrase="warm golden skin tones, natural contrast, and fine organic film grain characteristic of Kodak Portra 400"
    ),
    "cinestill_800t": FilmStock(
        name="CineStill 800T",
        phrase="cool teal shadows, warm tungsten skin rendition, and signature red halation around specular highlights of CineStill 800T"
    ),
    "kodak_tri_x_400": FilmStock(
        name="Kodak Tri-X 400 (B&W)",
        phrase="classic monochrome black and white with deep punchy blacks and gritty silver-halide grain of Kodak Tri-X 400"
    ),
    "fujifilm_provia_100f": FilmStock(
        name="Fujifilm Provia 100F",
        phrase="neutral faithful colors, clean natural whites, and fine slide film tonality of Fujifilm Provia 100F"
    ),
    "kodachrome_64": FilmStock(
        name="Kodachrome 64 (Vintage)",
        phrase="rich warm color saturation and documentary character reminiscent of vintage 1970s Kodachrome slide film"
    ),
    "digital_raw": FilmStock(
        name="Pristine Digital RAW",
        phrase="clean digital sensor capture with wide dynamic range, neutral color grading, and zero artificial smoothing"
    )
}

MASTER_PRESETS = {
    "national_geographic_portrait": {
        "title": "National Geographic Human Portrait",
        "description": "Authentic, weathered documentary portrait capturing profound human character with lifelike skin texture and environmental depth.",
        "camera": "leica_m11",
        "lens": "zeiss_otus_85",
        "aperture": "f/1.8",
        "lighting": "diffused_window",
        "film_stock": "kodak_portra_400",
        "shutter": "1/250s",
        "iso": 200,
        "aspect_ratio": "3:4",
        "subject_hint": "An authentic candid photograph of an old sea captain in Maine, weathered skin, gray beard, looking out from a wooden boat. Natural skin texture, subtle wrinkles, genuine fabric folds on a dark wool sweater, soft overcast coastal daylight, shallow depth of field.",
        "tags": ["documentary", "portrait", "weathered", "leica"]
    },
    "kyoto_artisan_workshop": {
        "title": "Kyoto Artisan Workshop",
        "description": "Intimate environmental portrait of a master craftsman in his traditional studio with warm ambient daylight.",
        "camera": "leica_m11",
        "lens": "voigtlander_35",
        "aperture": "f/2.0",
        "lighting": "diffused_window",
        "film_stock": "kodak_portra_400",
        "shutter": "1/125s",
        "iso": 400,
        "aspect_ratio": "1:1",
        "subject_hint": "A candid natural photograph of a Japanese ceramicist in his Kyoto workshop, inspecting a tea bowl in warm afternoon window light. Authentic skin texture, fine wrinkles, dusty linen apron with clay stains, wooden shelves with ceramics softly blurred in background.",
        "tags": ["artisan", "kyoto", "workshop", "portrait"]
    },
    "high_fashion_editorial": {
        "title": "Vogue Studio Editorial",
        "description": "Crisp medium-format fashion portrait with rich fabric weave textures and clean editorial lighting.",
        "camera": "hasselblad_h6d",
        "lens": "nikon_plena_135",
        "aperture": "f/2.8",
        "lighting": "studio_softbox",
        "film_stock": "digital_raw",
        "shutter": "1/160s",
        "iso": 100,
        "aspect_ratio": "3:4",
        "subject_hint": "Editorial fashion photograph of an elegant model wearing a textured camel wool overcoat against a minimalist brutalist concrete wall. Sharp fabric weave, natural skin texture with subtle freckles, relaxed editorial pose, diffused studio softbox light.",
        "tags": ["fashion", "hasselblad", "studio", "editorial"]
    },
    "candid_street_reportage": {
        "title": "Rainy Night Street Photography",
        "description": "Atmospheric 35mm street photography with wet pavement reflections and authentic urban glow.",
        "camera": "leica_m11",
        "lens": "voigtlander_35",
        "aperture": "f/1.4",
        "lighting": "cinematic_neon",
        "film_stock": "cinestill_800t",
        "shutter": "1/60s",
        "iso": 800,
        "aspect_ratio": "16:9",
        "subject_hint": "Candid 35mm street photograph taken in a narrow rain-slicked Tokyo alleyway at night. A person with a clear umbrella walking past a glowing ramen stall, steam rising into damp night air, wet asphalt reflecting amber lanterns, authentic motion blur in background.",
        "tags": ["street", "tokyo", "neon", "cinestill", "rain"]
    },
    "cinematic_movie_still": {
        "title": "Anamorphic Cinema Frame",
        "description": "35mm widescreen cinematic frame with horizontal bokeh and organic atmosphere.",
        "camera": "arri_alexa35",
        "lens": "cooke_anamorphic_40",
        "aperture": "f/2.0",
        "lighting": "golden_hour",
        "film_stock": "digital_raw",
        "shutter": "1/48s",
        "iso": 800,
        "aspect_ratio": "21:9",
        "subject_hint": "A cinematic widescreen film still of a lone wanderer standing on an arid desert ridge at dusk, golden sunlight catching the rim of their dusty linen scarf, vast canyon landscape stretching to horizon, anamorphic lens flare.",
        "tags": ["cinema", "arri", "anamorphic", "widescreen"]
    },
    "macro_hyperrealism": {
        "title": "Macro Biology & Surface Detail",
        "description": "Macro photography with extreme clarity on physical surfaces and liquid droplets.",
        "camera": "sony_a7rv",
        "lens": "zeiss_otus_85",
        "aperture": "f/4.0",
        "lighting": "diffused_window",
        "film_stock": "digital_raw",
        "shutter": "1/200s",
        "iso": 100,
        "aspect_ratio": "1:1",
        "subject_hint": "Macro photograph of clear morning water droplets resting on a veined dark green monstera leaf. Microscopic water surface tension, crisp reflection of a garden window within the droplets, natural leaf texture with wax cuticle sheen.",
        "tags": ["macro", "nature", "physics", "sharp"]
    }
}


class PhotorealEngine:
    def __init__(self):
        self.cameras = CAMERA_PROFILES
        self.lenses = LENS_PROFILES
        self.lighting = LIGHTING_PROFILES
        self.film_stocks = FILM_STOCKS
        self.presets = MASTER_PRESETS

    def synthesize_prompt(
        self,
        subject: str,
        camera_key: str = "leica_m11",
        lens_key: str = "zeiss_otus_85",
        aperture: str = "f/1.8",
        lighting_key: str = "rembrandt",
        film_stock_key: str = "kodak_portra_400",
        include_skin_realism: bool = True,
        include_material_physics: bool = True,
        aspect_ratio: str = "3:4",
        custom_shutter: str = "1/250s",
        custom_iso: int = 200,
        extra_mood: Optional[str] = None
    ) -> Dict:
        cam = self.cameras.get(camera_key, self.cameras["leica_m11"])
        lens = self.lenses.get(lens_key, self.lenses["zeiss_otus_85"])
        light = self.lighting.get(lighting_key, self.lighting["rembrandt"])
        film = self.film_stocks.get(film_stock_key, self.film_stocks["kodak_portra_400"])

        # Natural language photographic narrative
        import re
        clean_subj = subject.strip().rstrip(". ")
        # Strip redundant leading photo prefixes to avoid stuttering
        clean_subj = re.sub(
            r'^(an?|the)\s+(natural|authentic|candid|photorealistic|sharp|cinematic|detailed|documentary)?\s*(photograph|photo|picture|image|portrait|shot)\s+of\s+',
            '',
            clean_subj,
            flags=re.IGNORECASE
        )
        
        sentences = [
            f"A natural, authentic photograph of {clean_subj}."
        ]

        # Lighting & Optics in natural prose
        sentences.append(
            f"Shot on a {cam.body} with a {lens.name} ({lens.focal_length}) at {aperture}. "
            f"Lighting is {light.phrase}. "
            f"The image features {lens.optical_phrase} with {cam.sensor_phrase}."
        )

        # Film tone & color
        sentences.append(
            f"Color grading and grain profile: {film.phrase}."
        )

        # Micro-texture cues in natural prose (avoiding keyword dumps)
        realism_cues = []
        if include_skin_realism:
            realism_cues.append("authentic skin texture with visible natural pores, fine facial lines, and realistic unretouched complexion")
        if include_material_physics:
            realism_cues.append("natural fabric weave, subtle surface imperfections, and authentic interaction of light with physical materials")

        if realism_cues:
            sentences.append(f"Subtle details include {' and '.join(realism_cues)}.")

        if extra_mood and extra_mood.strip():
            sentences.append(f"Atmosphere: {extra_mood.strip()}.")

        full_prompt = " ".join(sentences)

        aspect_resolutions = {
            "1:1": (1024, 1024),
            "3:4": (896, 1152),
            "4:5": (864, 1080),
            "16:9": (1280, 720),
            "21:9": (1344, 576),
            "9:16": (720, 1280),
            "3:2": (1200, 800),
            "2:3": (800, 1200)
        }
        width, height = aspect_resolutions.get(aspect_ratio, (1024, 1024))

        return {
            "subject": subject,
            "positive_prompt": full_prompt,
            "negative_prompt": "cartoon, 3d render, CGI, painting, illustration, plastic skin, doll, artificial oversaturated colors, watermark, signature",
            "camera": cam.name,
            "camera_key": camera_key,
            "lens": lens.name,
            "lens_key": lens_key,
            "aperture": aperture,
            "lighting": light.name,
            "lighting_key": lighting_key,
            "film_stock": film.name,
            "film_stock_key": film_stock_key,
            "aspect_ratio": aspect_ratio,
            "dimensions": {"width": width, "height": height},
            "shutter": custom_shutter,
            "iso": custom_iso
        }

    def load_preset(self, preset_key: str, custom_subject: Optional[str] = None) -> Dict:
        preset = self.presets.get(preset_key)
        if not preset:
            raise ValueError(f"Unknown preset key: {preset_key}.")

        subject = custom_subject if custom_subject and custom_subject.strip() else preset["subject_hint"]

        synth = self.synthesize_prompt(
            subject=subject,
            camera_key=preset["camera"],
            lens_key=preset["lens"],
            aperture=preset["aperture"],
            lighting_key=preset["lighting"],
            film_stock_key=preset["film_stock"],
            aspect_ratio=preset.get("aspect_ratio", "3:4"),
            custom_shutter=preset.get("shutter", "1/250s"),
            custom_iso=preset.get("iso", 200)
        )
        synth["preset_title"] = preset["title"]
        synth["preset_description"] = preset["description"]
        synth["preset_key"] = preset_key
        return synth