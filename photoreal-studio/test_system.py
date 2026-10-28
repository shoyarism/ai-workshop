# -*- coding: utf-8 -*-
"""
Automated Verification Suite for Photoreal Studio (v2.0 with Hugging Face FLUX-Realism).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.photoreal_engine import PhotorealEngine
from engine.prompt_enhancer import RealismPromptEnhancer
from backend.generator import PhotorealGenerator
from backend.server import app
from starlette.testclient import TestClient


class TestPhotorealSystem(unittest.TestCase):
    def setUp(self):
        self.engine = PhotorealEngine()
        self.enhancer = RealismPromptEnhancer()
        self.generator = PhotorealGenerator()
        self.client = TestClient(app)

    def test_01_engine_synthesis(self):
        synth = self.engine.synthesize_prompt(
            subject="elderly fisherman in Iceland",
            camera_key="leica_m11",
            lens_key="zeiss_otus_85",
            aperture="f/1.4",
            lighting_key="rembrandt",
            film_stock_key="kodak_portra_400"
        )
        self.assertIn("Leica M11-P", synth["positive_prompt"])
        self.assertIn("Zeiss Otus 85mm", synth["positive_prompt"])
        self.assertIn("Kodak Portra 400", synth["positive_prompt"])
        self.assertIn("plastic skin", synth["negative_prompt"])
        print("[PASS] Natural language engine synthesis test passed.")

    def test_02_presets(self):
        for key in self.engine.presets:
            preset_data = self.engine.load_preset(key)
            self.assertTrue(len(preset_data["positive_prompt"]) > 50)
            self.assertIn("preset_title", preset_data)
        print(f"[PASS] All {len(self.engine.presets)} master presets loaded and verified.")

    def test_03_enhancer(self):
        res = self.enhancer.enhance("old cobbler at work")
        self.assertEqual(res["category"], "human_portrait")
        self.assertTrue(len(res["enhanced_subject"]) > len("old cobbler at work"))
        self.assertIn("pores", res["enhanced_subject"])
        print("[PASS] Natural language Prompt Enhancer test passed.")

    def test_04_server_endpoints(self):
        r_status = self.client.get("/api/status")
        self.assertEqual(r_status.status_code, 200)
        self.assertEqual(r_status.json()["default_provider"], "flux_dev_realism")

        r_opt = self.client.get("/api/options")
        self.assertEqual(r_opt.status_code, 200)
        self.assertTrue(len(r_opt.json()["cameras"]) >= 5)

        r_presets = self.client.get("/api/presets")
        self.assertEqual(r_presets.status_code, 200)

        payload = {
            "subject": "cyberpunk alleyway in neo-tokyo",
            "camera_key": "sony_a7rv",
            "lens_key": "voigtlander_35",
            "aperture": "f/1.4"
        }
        r_synth = self.client.post("/api/synthesize", json=payload)
        self.assertEqual(r_synth.status_code, 200)
        self.assertIn("positive_prompt", r_synth.json())

        r_enh = self.client.post("/api/enhance", json={"subject": "female model"})
        self.assertEqual(r_enh.status_code, 200)
        self.assertIn("enhanced_subject", r_enh.json())

        print("[PASS] Server API endpoints verified.")

    def test_05_generation(self):
        print("\nTesting image generation pipeline with Hugging Face FLUX...")
        synth = self.engine.synthesize_prompt(
            subject="extreme macro of a dewdrop on a green leaf",
            camera_key="sony_a7rv",
            lens_key="zeiss_otus_85",
            aperture="f/2.8",
            aspect_ratio="1:1"
        )
        meta = self.generator.generate(synth, provider="hf_flux_schnell", seed=42)
        self.assertTrue(os.path.exists(os.path.join(self.generator.output_dir, meta["filename"])))
        self.assertTrue(os.path.getsize(os.path.join(self.generator.output_dir, meta["filename"])) > 1000)
        print(f"[PASS] Generation pipeline passed. Generated: {meta['filename']} ({meta['dimensions']['width']}x{meta['dimensions']['height']}) in {meta['generation_time_seconds']}s via {meta['provider']}.")


if __name__ == "__main__":
    unittest.main()