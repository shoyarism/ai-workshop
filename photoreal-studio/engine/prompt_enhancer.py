# -*- coding: utf-8 -*-
"""
Intelligent Photorealism Prompt Enhancer:
Expands basic concepts into natural, immersive photographic narratives for modern diffusion/flow models.
"""

import os
from typing import Dict, Optional


class RealismPromptEnhancer:
    def detect_category(self, text: str) -> str:
        lower = text.lower()
        if any(k in lower for k in ["man", "woman", "girl", "boy", "person", "elderly", "old", "portrait", "face", "fisherman", "captain", "chef", "model", "mechanic", "musician", "artisan", "monk"]):
            return "human_portrait"
        if any(k in lower for k in ["street", "city", "alley", "tokyo", "paris", "night", "neon", "rain", "market"]):
            return "urban_street"
        if any(k in lower for k in ["lion", "tiger", "wolf", "dog", "cat", "bird", "eagle", "bear", "fox", "deer", "animal"]):
            return "wildlife"
        if any(k in lower for k in ["coffee", "watch", "camera", "flower", "macro", "cocktail", "bowl", "car", "shoe"]):
            return "macro_object"
        if any(k in lower for k in ["mountain", "forest", "tree", "river", "ocean", "sea", "desert", "landscape", "sunset"]):
            return "landscape"
        return "general_photoreal"

    def enhance(self, raw_prompt: str, gemini_api_key: Optional[str] = None) -> Dict[str, str]:
        raw_prompt = raw_prompt.strip()
        if not raw_prompt:
            return {"enhanced_subject": "", "reasoning": "Empty input"}

        api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                llm_result = self._enhance_with_gemini(raw_prompt, api_key)
                if llm_result:
                    return llm_result
            except Exception:
                pass

        return self._enhance_with_rules(raw_prompt)

    def _enhance_with_rules(self, text: str) -> Dict[str, str]:
        category = self.detect_category(text)
        clean = text.rstrip(". ")

        if category == "human_portrait":
            enhanced = (
                f"{clean}, captured in a natural candid moment. "
                "The person has an unposed, contemplative expression with genuine eye contact and realistic catchlights. "
                "Authentic skin texture shows fine pores, subtle laugh lines, and natural tone variations without artificial smoothing. "
                "Their clothing has genuine fabric wrinkles and texture. "
                "The background is softly blurred in natural ambient lighting."
            )
            reasoning = "Structured as a natural language portrait: candid expression, genuine skin micro-textures, and realistic fabric folds."

        elif category == "urban_street":
            enhanced = (
                f"{clean}, captured as an authentic 35mm street snapshot. "
                "Natural ambient light from nearby shops and streetlamps illuminates the scene, "
                "casting gentle reflections across wet pavement. "
                "Weathered building facades and authentic urban details create deep environmental storytelling with gentle motion blur in the distance."
            )
            reasoning = "Structured as authentic street photojournalism: 35mm perspective, wet pavement bounce, and natural atmospheric depth."

        elif category == "wildlife":
            enhanced = (
                f"{clean}, photographed in its natural untamed habitat. "
                "Sharp telephoto focus on the eyes revealing clear crystalline reflections, "
                "individual strands of fur or feathers resolved with crisp rim light, "
                "and a soft, creamy natural background providing dramatic subject isolation."
            )
            reasoning = "Structured for wildlife telephoto capture: crystalline eye sharpness and creamy organic background bokeh."

        elif category == "macro_object":
            enhanced = (
                f"{clean}, photographed with extreme close-up macro clarity. "
                "Reveals microscopic surface textures, natural tactile abrasions, "
                "crisp specular reflections adhering to physical light angles, "
                "and an ultra-shallow depth of field smoothly melting into the background."
            )
            reasoning = "Structured for macro physics: microscopic tactile textures and shallow focal plane."

        elif category == "landscape":
            enhanced = (
                f"{clean}, captured in sweeping landscape photography. "
                "Raking low-angle sunlight reveals natural geological relief and atmospheric layers, "
                "with authentic cloud volume and deep tonal gradation stretching to the horizon."
            )
            reasoning = "Structured for environmental landscape: low-angle raking light and atmospheric layers."

        else:
            enhanced = (
                f"{clean}, photographed with natural light and documentary clarity. "
                "Features realistic tactile textures, authentic shadow roll-off, and honest physical depth."
            )
            reasoning = "Structured with natural lighting, tactile texture, and authentic depth."

        return {
            "enhanced_subject": enhanced,
            "category": category,
            "reasoning": reasoning
        }

    def _enhance_with_gemini(self, text: str, api_key: str) -> Dict[str, str]:
        import json
        import requests

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": (
                        "You are a master National Geographic photographer. Rewrite this simple concept into a 2-3 sentence natural language photographic scene description for FLUX: "
                        f"'{text}'. "
                        "Focus on natural candid moments, realistic skin/material textures, and authentic lighting. Do NOT use buzzwords like '8k, unreal engine, masterpiece'. "
                        "Return JSON with 'enhanced_subject' and 'reasoning'."
                    )
                }]
            }],
            "generationConfig": {"response_mime_type": "application/json"}
        }
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            cand = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            res = json.loads(cand)
            return {
                "enhanced_subject": res.get("enhanced_subject", text),
                "category": "ai_enhanced",
                "reasoning": res.get("reasoning", "Enhanced via Gemini Director")
            }
        return self._enhance_with_rules(text)