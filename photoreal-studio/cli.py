# -*- coding: utf-8 -*-
"""
Command-Line Interface for the Photoreal Realism Studio.
Allows direct synthesis and generation of ultra-realistic AI images from the terminal.
"""

import os
import sys
import argparse
import json

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.photoreal_engine import PhotorealEngine
from engine.prompt_enhancer import RealismPromptEnhancer
from backend.generator import PhotorealGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Photoreal Studio CLI: Generate Ultra-Realistic AI Images with Optics & Physics Simulation"
    )
    parser.add_argument("subject", nargs="?", default=None, help="Photographic subject or concept")
    parser.add_argument("--preset", "-p", default=None, help="Preset key (e.g. national_geographic_portrait, high_fashion_editorial, candid_street_reportage)")
    parser.add_argument("--camera", "-c", default="leica_m11", help="Camera body key (hasselblad_h6d, leica_m11, sony_a7rv, arri_alexa35, canon_eos_r5, analog_35mm)")
    parser.add_argument("--lens", "-l", default="zeiss_otus_85", help="Lens profile (zeiss_otus_85, leica_noctilux_50, canon_85_ds, cooke_anamorphic_40, voigtlander_35, nikon_plena_135)")
    parser.add_argument("--aperture", "-a", default="f/1.8", help="Aperture (f/0.95, f/1.4, f/1.8, f/2.8, etc.)")
    parser.add_argument("--lighting", default="rembrandt", help="Lighting key (rembrandt, golden_hour, diffused_window, studio_softbox, chiaroscuro, cinematic_neon)")
    parser.add_argument("--film", default="kodak_portra_400", help="Film stock (kodak_portra_400, cinestill_800t, kodak_tri_x_400, fujifilm_provia_100f, kodachrome_64, digital_raw)")
    parser.add_argument("--aspect", default="3:4", help="Aspect ratio (1:1, 4:5, 3:4, 16:9, 21:9, 9:16)")
    parser.add_argument("--enhance", "-e", action="store_true", help="Enhance subject with sensory/biometric micro-details before generating")
    parser.add_argument("--provider", default="flux_dev_realism", help="Inference provider (flux_dev_realism, hf_flux_schnell, imagen3)")
    parser.add_argument("--seed", type=int, default=0, help="Random seed (0 for random)")
    parser.add_argument("--list-presets", action="store_true", help="List all available master presets")
    parser.add_argument("--prompt-only", action="store_true", help="Synthesize and display the photographic prompt without calling generator")

    args = parser.parse_args()

    engine = PhotorealEngine()
    enhancer = RealismPromptEnhancer()
    generator = PhotorealGenerator()

    if args.list_presets:
        print("\n=== MASTER PHOTOREAL PRESETS ===")
        for key, p in engine.presets.items():
            print(f"[{key}] - {p['title']}")
            print(f"  Description: {p['description']}")
            print(f"  Default: {p['camera']} + {p['lens']} @ {p['aperture']} ({p['lighting']})")
            print(f"  Suggested subject: {p['subject_hint']}\n")
        return

    if not args.subject and not args.preset:
        parser.print_help()
        return

    subject = args.subject

    # Load from preset if specified
    if args.preset:
        try:
            preset = engine.presets[args.preset]
            if not subject:
                subject = preset["subject_hint"]
            args.camera = preset["camera"]
            args.lens = preset["lens"]
            args.aperture = preset["aperture"]
            args.lighting = preset["lighting"]
            args.film = preset["film_stock"]
            args.aspect = preset.get("aspect_ratio", "3:4")
            print(f"\nLoaded Preset: {preset['title']}")
        except KeyError:
            print(f"Error: Unknown preset '{args.preset}'. Use --list-presets to view options.")
            return

    if args.enhance and subject:
        print("\nEnhancing subject with photographic physics...")
        enh_res = enhancer.enhance(subject)
        subject = enh_res["enhanced_subject"]
        print(f"Enhanced Subject: {subject}\n")

    # Synthesize master prompt
    synth = engine.synthesize_prompt(
        subject=subject,
        camera_key=args.camera,
        lens_key=args.lens,
        aperture=args.aperture,
        lighting_key=args.lighting,
        film_stock_key=args.film,
        aspect_ratio=args.aspect
    )

    print("=" * 70)
    print("PHOTOREAL SYNTHESIZED POSITIVE PROMPT:")
    print("-" * 70)
    print(synth["positive_prompt"])
    print("\n" + "=" * 70)
    print("ANTI-CGI NEGATIVE REALISM SHIELD:")
    print("-" * 70)
    print(synth["negative_prompt"])
    print("=" * 70)

    if args.prompt_only:
        return

    print(f"\nGenerating master photograph using provider '{args.provider}'...")
    meta = generator.generate(
        synthesized_data=synth,
        provider=args.provider,
        seed=args.seed
    )

    print("\nGeneration Completed Successfully!")
    print(f"  Output Image: {meta['image_url']}")
    print(f"  Saved File  : {os.path.join(generator.output_dir, meta['filename'])}")
    print(f"  Resolution  : {meta['dimensions']['width']}x{meta['dimensions']['height']}")
    print(f"  Render Time : {meta['generation_time_seconds']}s")
    print(f"  Seed        : {meta['seed']}")
    print(f"  Optics      : {meta['camera']} with {meta['lens']} @ {meta['aperture']}")


if __name__ == "__main__":
    main()