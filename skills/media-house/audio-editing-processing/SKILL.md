---
name: audio-editing-processing
description: Edit, mix, process, and master audio — trim, cut, concatenate, normalize, EQ, compress, denoise, fade, crossfade, pitch/tempo shift, stem separation, and format conversion. Use when the user needs to clean up recordings, create music beds, voiceover carves, podcasts, or audio for video. Triggers on: audio editing, audio processing, trim audio, normalize audio, denoise, EQ, compress, fade, crossfade, stem separation, audio mastering, podcast editing, audio conversion, ffmpeg audio, pydub, audio mixing.
---

# Audio Editing & Processing

Process, edit, and master audio files using ffmpeg, pydub, and specialized tools. Covers trimming, cutting, concatenating, normalizing, EQ, compression, denoising, fading, crossfading, pitch/tempo shifting, stem separation, format conversion, and voiceover carving (ducking music under speech).

## When to trigger

- User needs to trim, cut, or join audio files
- User wants to clean up a recording (denoise, normalize, de-ess)
- User needs a music bed with voiceover carving (ducking)
- User wants to convert audio formats (mp3, wav, ogg, flac, aac)
- User needs to adjust volume, pitch, or tempo
- User wants stem separation (vocals, drums, bass, other)
- User is preparing audio for video or podcast

## Core operations with ffmpeg

### Trim / cut
```bash
# Cut from 0:30 to 1:45
ffmpeg -i input.mp3 -ss 00:00:30 -to 00:01:45 -c copy output.mp3

# Re-encode cut (more precise, slower)
ffmpeg -i input.mp3 -ss 00:00:30 -to 00:01:45 -c:a libmp3lame output.mp3
```

### Concatenate
```bash
# Create file list for concatenation
echo "file 'part1.mp3'" > files.txt
echo "file 'part2.mp3'" >> files.txt
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp3
```

### Normalize volume (loudness)
```bash
# Loudness normalization to -16 LUFS (podcast standard)
ffmpeg -i input.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 output.wav
```

### Fade in / fade out
```bash
# Fade in first 3 seconds, fade out last 3 seconds
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3,afade=t=out:st=60:d=3" output.mp3
```

### Crossfade between two tracks
```bash
# Crossfade track A into track B over 5 seconds
ffmpeg -i track_a.mp3 -i track_b.mp3 -filter_complex \
  "[0:a][1:a]acrossfade=d=5:c1=tri:c2=tri" output.mp3
```

### Denoise (afftdn)
```bash
# Reduce background noise
ffmpeg -i noisy.wav -af "afftdn=nt=w:nn=n" clean.wav
```

### EQ (equalization)
```bash
# Boost bass (60Hz) and cut harshness (3kHz)
ffmpeg -i input.wav -af "equalizer=f=60:t=q:w=100:g=5,equalizer=f=3000:t=q:w=200:g=-3" output.wav
```

### Compressor (dynamic range)
```bash
# Compress to even out loud/quiet parts
ffmpeg -i input.wav -af "compand=attacks=0:points=-80/-80|-40/-40|-20/-20|0/-3" output.wav
```

### Pitch / tempo shift (independent)
```bash
# Change pitch without changing tempo
ffmpeg -i input.wav -af "asetrate=44100*1.05,atempo=1/1.05" output.wav

# Change tempo without changing pitch
ffmpeg -i input.wav -af "atempo=1.25" output.wav
```

### Format conversion
```bash
# MP3 to WAV
ffmpeg -i input.mp3 output.wav

# WAV to MP3 (128k)
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3

# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec copy audio.aac
```

### Voiceover carving (duck music under speech)
```bash
# Sidechain-compress music so it ducks when voiceover plays
ffmpeg -i music.wav -i voiceover.wav -filter_complex \
  "[1:a]astats=metadata=reset,ametadata=print:key=lavfi.rms.statistics[RMS];[0:a][RMS]sidechaincompress=threshold=0.05:ratio=4:attack=10:release=500[mixed]" \
  -map "[mixed]" output.wav
```

## Python processing with pydub

Install: `pip install pydub` (also needs ffmpeg on PATH)

```python
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize, compress_dynamic_range

# Load
song = AudioSegment.from_mp3("input.mp3")
voice = AudioSegment.from_wav("voiceover.wav")

# Trim
clip = song[30000:105000]  # 30s to 105s (milliseconds)

# Fade
clip = clip.fade_in(3000).fade_out(3000)

# Normalize
clip = normalize(clip)

# Overlay voice on music (with ducking)
ducked_music = song - 12  # lower music by 12dB
mixed = ducked_music.overlay(voice)

# Export
mixed.export("output.mp3", format="mp3", bitrate="192k")
```

### Batch normalize a folder
```python
from pathlib import Path
from pydub import AudioSegment
from pydub.effects import normalize

for f in Path("input/").glob("*.wav"):
    audio = AudioSegment.from_wav(f)
    audio = normalize(audio)
    audio.export(Path("output/") / f.name, format="wav")
```

## Stem separation (vocals / instruments)

### With demucs (high quality)
```bash
pip install demucs
demucs input.mp3 --two-stems=vocals
# Output: separated/htdemucs/input/vocals.wav, no_vocals.wav
```

### With UVR5 / Ultimate Vocal Remover
GUI-based, best for music stems (vocals, instrumental, drums, bass, other).

## Loudness standards

| Platform | Target Loudness | True Peak |
|---|---|---|
| Podcast | -16 LUFS | -1.5 dBTP |
| YouTube | -14 LUFS | -1.0 dBTP |
| Spotify | -14 LUFS | -1.0 dBTP |
| Apple Music | -16 LUFS | -1.0 dBTP |
| Broadcast (EBU R128) | -23 LUFS | -1.0 dBTP |
| Audiobook (Audible) | -18 to -23 LUFS | -3.0 dBTP |

## Sample rates & bit depths

| Use case | Sample rate | Bit depth | Format |
|---|---|---|---|
| Music production | 44.1kHz or 48kHz | 24-bit | WAV / FLAC |
| Podcast | 44.1kHz | 16-bit | MP3 (128-192kbps) |
| Voiceover | 44.1kHz | 16-bit | WAV / MP3 |
| Audiobook | 44.1kHz | 16-bit | MP3 (64-128kbps) |
| Telephony | 8kHz or 16kHz | 16-bit | WAV / mu-law |

## Decision checklist

- [ ] Input format identified (mp3, wav, video, etc.)
- [ ] Operations needed (trim, normalize, denoise, mix, convert)
- [ ] Output format and quality target
- [ ] Loudness standard for target platform
- [ ] Whether stem separation is needed
- [ ] Whether voiceover ducking/carving is needed

## Related Workshop skills

- `tts-voice-generation` — generate voiceover audio to then edit here
- `music-to-video` — combine processed audio with video
- `ai-podcast-creation` — full podcast production pipeline
- `media-use` — resolve BGM, SFX, voice assets
- `video-edit` — audio is part of video editing workflows
