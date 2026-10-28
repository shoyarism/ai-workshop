#!/usr/bin/env python3
"""
sound.py — Generate background music + SFX for motion video.
Creates atmospheric drone, whooshes, and hits using Web Audio API synthesis.
"""
import subprocess
import json
import os

# Scene timings (seconds)
SCENES = [
    {"name": "title", "start": 0, "end": 4},
    {"name": "problem", "start": 4, "end": 8},
    {"name": "solution", "start": 8, "end": 13},
    {"name": "features", "start": 13, "end": 18},
    {"name": "stats", "start": 18, "end": 22},
    {"name": "cta", "start": 22, "end": 26},
]

def generate_music(output_path):
    """Generate ambient music using Tone.js in browser."""
    html = '''<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
</head>
<body>
<script>
async function generate() {
  await Tone.start();
  
  // Create ambient pad
  const pad = new Tone.PolySynth(Tone.Synth, {
    oscillator: { type: "fatsine" },
    envelope: { attack: 0.5, decay: 0.3, sustain: 0.8, release: 1 }
  }).toDestination();
  pad.volume.value = -18;
  
  // Create sub bass
  const sub = new Tone.MembraneSynth({
    pitchDecay: 0.05,
    octaves: 4,
    envelope: { attack: 0.01, decay: 0.4, sustain: 0.1, release: 1 }
  }).toDestination();
  sub.volume.value = -12;
  
  // Create high sparkle
  const sparkle = new Tone.Synth({
    oscillator: { type: "sine" },
    envelope: { attack: 0.01, decay: 0.3, sustain: 0, release: 0.5 }
  }).toDestination();
  sparkle.volume.value = -24;
  
  const now = Tone.now();
  
  // Ambient chord progression (Cmaj7 - Am7 - Fmaj7 - G)
  // Scene 1 (0-4s): Title - sparse, mysterious
  pad.triggerAttackRelease(["C3", "E3", "G3", "B3"], "4n", now);
  pad.triggerAttackRelease(["D3", "F3", "A3", "C4"], "4n", now + 2);
  
  // Scene 2 (4-8s): Problem - tense, minor feel
  sub.triggerAttackRelease("C2", "2n", now + 4);
  pad.triggerAttackRelease(["A2", "C3", "E3", "G3"], "2n", now + 4);
  pad.triggerAttackRelease(["G2", "B2", "D3", "F3"], "2n", now + 6);
  
  // Scene 3 (8-13s): Solution - opening up
  sub.triggerAttackRelease("F2", "1n", now + 8);
  pad.triggerAttackRelease(["C3", "E3", "G3", "B3"], "1n", now + 8);
  sparkle.triggerAttackRelease("E5", "8n", now + 9);
  sparkle.triggerAttackRelease("G5", "8n", now + 10);
  
  // Scene 4 (13-18s): Features - building energy
  sub.triggerAttackRelease("C2", "4n", now + 12);
  sub.triggerAttackRelease("G2", "4n", now + 13);
  pad.triggerAttackRelease(["C3", "E3", "G3"], "2n", now + 12);
  pad.triggerAttackRelease(["F3", "A3", "C4"], "2n", now + 14);
  sparkle.triggerAttackRelease("C5", "16n", now + 15);
  sparkle.triggerAttackRelease("E5", "16n", now + 16);
  
  // Scene 5 (18-22s): Stats - confident, punchy
  sub.triggerAttackRelease("C2", "8n", now + 18);
  sub.triggerAttackRelease("C2", "8n", now + 19);
  sub.triggerAttackRelease("C2", "8n", now + 20);
  pad.triggerAttackRelease(["C3", "E3", "G3", "B3"], "1n", now + 18);
  
  // Scene 6 (22-26s): CTA - resolve, hopeful
  sub.triggerAttackRelease("F2", "1n", now + 22);
  pad.triggerAttackRelease(["C3", "E3", "G3", "B3"], "2n", now + 22);
  sparkle.triggerAttackRelease("C5", "4n", now + 23);
  sparkle.triggerAttackRelease("E5", "4n", now + 24.5);
  
  // Fade out
  const master = Tone.Destination;
  master.volume.rampTo(-20, 4, now + 24);
  
  // Render
  const rec = new Tone.Recorder();
  Tone.Destination.connect(rec);
  rec.record();
  
  setTimeout(() => {
    rec.stop();
    const blob = rec.getBlob();
    const url = URL.createObjectURL(blob);
    console.log(url);
    window.location.href = url;
  }, 26000);
}
generate();
</script>
</body>
</html>'''
    
    # Write HTML and use browser to generate
    html_path = os.path.join(os.path.dirname(output_path), 'sound_gen.html')
    with open(html_path, 'w') as f:
        f.write(html)
    
    print(f"HTML written to {html_path}")
    print("Open this in a browser to generate audio, then export to MP3.")
    return html_path

def generate_sfx():
    """Generate whoosh and hit SFX as WAV files."""
    # This would use Web Audio API or a synthesized approach
    print("SFX generation requires Tone.js or external audio tools.")
    return None

if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
    generate_music(output)
