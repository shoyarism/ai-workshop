---
name: tts-voice-generation
description: Text-to-speech and voice generation — ElevenLabs, OpenAI TTS, Kokoro TTS, Edge TTS, Azure Speech, Polly, and local Piper/Whisper. Use when the user needs AI voiceovers, narration, podcast audio, audiobook generation, or conversational agent speech. Triggers on: text to speech, tts, voiceover, narration, podcast audio, audiobook, elevenlabs, kokoro, edge tts, azure speech, piper, voice cloning, speech synthesis, spoken audio, read aloud.
---

# TTS Voice Generation

Generate spoken audio from text using cloud APIs or fully local models. Covers provider selection, voice cloning, SSML, streaming, and production best practices for voiceovers, narration, podcasts, and audiobooks.

## When to trigger

- User needs text converted to spoken audio
- User mentions voiceover, narration, podcast, audiobook, TTS, speech synthesis
- User wants voice cloning or custom voices
- User is building a conversational agent that needs spoken output
- User needs multilingual or accented speech

## Provider comparison

| Provider | Type | Quality | Cost | Best for |
|---|---|---|---|---|
| ElevenLabs | Cloud | Premium (emotive, cloning) | Paid + free tier | Voiceovers, characters, audiobooks |
| OpenAI TTS | Cloud | High | Paid | General TTS, streaming, low latency |
| Kokoro TTS | Local | High | Free | Local, fast, open-weight (82M params) |
| Edge TTS | Local/Free | Good | Free (Microsoft) | Quick local TTS, many voices |
| Azure Speech | Cloud | Enterprise | Paid | Enterprise, SSML, custom neural voices |
| Amazon Polly | Cloud | Good | Paid | AWS ecosystems, SSML |
| Piper | Local | Good | Free | Fully offline, low resource |
| Google TTS | Cloud | Good | Paid | Android, multilingual |

## ElevenLabs (premium, voice cloning)

Install: `pip install elevenlabs`

```python
from elevenlabs import ElevenLabs, Voice, VoiceSettings
import os

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.text_to_speech.convert(
    text="Hello, this is a professional voiceover.",
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.2,
        use_speaker_boost=True
    ),
    output_format="mp3_44100_128"
)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Voice cloning (instant)
```python
voice = client.voices.add_from_files(
    name="My Voice",
    files=["sample1.mp3", "sample2.mp3"],
    description="Cloned from clean 1-minute samples"
)
```

## OpenAI TTS (cloud, streaming)

Install: `pip install openai`

```python
from openai import OpenAI
client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",  # or tts-1-hd for higher quality
    voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
    input="Hello, this is OpenAI TTS streaming.",
    response_format="mp3"
)

response.stream_to_file("output.mp3")
```

### Streaming (real-time)
```python
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="nova",
    input="This is streaming audio..."
) as response:
    response.stream_to_file("streaming.mp3")
```

## Kokoro TTS (local, open-weight, fast)

Install: `pip install kokoro` or `pip install kokoro-onnx`

```python
from kokoro import KModel
import soundfile as sf

model = KModel("kokoro-v0_19.onnx", voices="voices.bin")
audio, sample_rate = model.generate(
    "Hello, this is local Kokoro TTS.",
    voice="af_bella",  # or af_sarah, am_adam, bf_emma, etc.
    speed=1.0,
    lang="en-us"
)
sf.write("output.wav", audio, sample_rate)
```

## Edge TTS (free, Microsoft, local)

Install: `pip install edge-tts`

```bash
# CLI
edge-tts --voice en-US-AriaNeural --text "Hello world" --write-media output.mp3

# List voices
edge-tts --list-voices
```

```python
import edge_tts
import asyncio

async def main():
    communicate = edge_tts.Communicate("Hello world", "en-US-AriaNeural")
    await communicate.save("output.mp3")

asyncio.run(main())
```

## Azure Speech (enterprise, SSML, custom neural)

Install: `pip install azure-cognitiveservices-speech`

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("AZURE_SPEECH_KEY"),
    region=os.getenv("AZURE_SPEECH_REGION")
)
speech_config.set_speech_synthesis_voice("en-US-AriaNeural")

audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

result = synthesizer.speak_text_async("Hello from Azure Speech").get()
```

### SSML for control
```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-AriaNeural">
    <prosody rate="slow" pitch="+2st">Hello.</prosody>
    <break time="500ms"/>
    <say-as interpret-as="characters">TTS</say-as>
  </voice>
</speak>
```

## Piper (fully local, low resource)

Install: `pip install piper-tts` or download piper binary

```bash
# Download a voice model (e.g., en_US-lessac-medium)
wget https://github.com/rhasspy/piper/releases/download/v0.1.0/en_US-lessac-medium.onnx

# CLI
echo "Hello world" | piper --model en_US-lessac-medium.onnx --output_file output.wav
```

## Decision checklist

- [ ] Quality requirement: premium (ElevenLabs) vs good (OpenAI/Kokoro) vs basic (Edge/Piper)
- [ ] Latency requirement: streaming (OpenAI/Edge) vs batch (ElevenLabs)
- [ ] Privacy: local only (Kokoro/Piper/Edge) vs cloud (ElevenLabs/OpenAI/Azure)
- [ ] Voice cloning needed: ElevenLabs only
- [ ] SSML control needed: Azure/Amazon Polly
- [ ] Multilingual: ElevenLabs multilingual v2, Azure, Google
- [ ] Budget: free tier (Edge, Piper, Kokoro) vs paid

## Production best practices

- **Voice selection**: Match voice to content (calm for audiobooks, energetic for marketing, neutral for narration)
- **Sample rate**: 44.1kHz MP3 for music/podcasts, 22.05kHz for voice-only
- **Normalization**: Normalize loudness (-16 LUFS for podcasts, -23 LUFS for broadcast)
- **Pauses**: Use SSML `<break>` for natural pacing between sections
- **Caching**: Cache generated audio for repeated text to save API costs
- **Fallback**: Have a local TTS fallback (Piper/Edge) if cloud API fails

## Related Workshop skills

- `audio-editing-processing` — edit, mix, and process the generated audio
- `music-to-video` — combine TTS audio with video
- `ai-podcast-creation` — full podcast production with TTS
- `elevenlabs-music-generation` — music generation companion
- `media-use` — resolve and manage audio assets
